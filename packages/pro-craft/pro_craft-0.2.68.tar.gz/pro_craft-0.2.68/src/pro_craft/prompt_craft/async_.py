# 测试1

from pro_craft.utils import extract_
from pro_craft.database import Prompt, UseCase, PromptBase, SyncMetadata
from pro_craft.utils import create_session, create_async_session

from sqlalchemy import select, delete # 导入 select, delete 用于异步操作
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy import select, and_ # 引入 select 和 and_
from sqlalchemy.orm import class_mapper # 用于检查对象是否是持久化的
from sqlalchemy import select, desc

import plotly.graph_objects as go
from datetime import datetime, timedelta
from tqdm.asyncio import tqdm
from modusched.core import Adapter
from pydantic import BaseModel, ValidationError, field_validator
from json.decoder import JSONDecodeError
from enum import Enum
import pandas as pd
import json
import os
import inspect
import re


class IntellectRemoveFormatError(Exception):
    pass

class IntellectRemoveError(Exception):
    pass

class ModelNameError(Exception):
    pass


BATCH_SIZE = int(os.getenv("DATABASE_SYNC_BATCH_SIZE",1000))

class IntellectType(Enum):
    train = "train"
    inference = "inference"
    summary = "summary"



def fix_broken_json_string(broken_json_str):
    # 移除 BOM
    broken_json_str = broken_json_str.lstrip('\ufeff')
    # 移除大部分非法 ASCII 控制字符
    broken_json_str = re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f]', '', broken_json_str)

    # 尝试找到 "content": " 和它对应的结束 "
    # 这是一个挑战，因为中间有未转义的换行。
    # 我们会寻找 "content": "，然后捕获从那以后直到最后一个 " 的所有内容，并替换其中的裸换行。

    # 注意：这个正则假设 "content" 的值是最后一个键值对，并且直到字符串末尾的 " 才结束
    # 并且假设其他字段都是合法的单行字符串
    fixed_json_str = re.sub(
        r'("content":\s*")(.+?)"\s*}',  # 匹配 "content": "，然后捕获所有内容直到最后一个 " }
        lambda m: m.group(1) + m.group(2).replace('\n', '\\n').replace('\r', '\\r') + '"\n}',
        broken_json_str,
        flags=re.DOTALL # 允许 . 匹配换行
    )

    # 修正可能的最后一行丢失的 }
    if not fixed_json_str.strip().endswith('}'):
        fixed_json_str += '\n}' # 补上结束的 }

    return fixed_json_str

async def get_last_sync_time(target_session: AsyncSession) -> datetime:
    """从目标数据库获取上次同步时间"""
    # 修正点：使用 select() 和 execute()
    result = await target_session.execute(
        select(SyncMetadata).filter_by(table_name="ai_sync_metadata")
    )
    metadata_entry = result.scalar_one_or_none() # 获取单个对象或 None

    if metadata_entry:
        return metadata_entry.last_sync_time
    return datetime(1970, 1, 1) # 默认一个很早的时间

async def update_last_sync_time(target_session: AsyncSession, new_sync_time: datetime):
    """更新目标数据库的上次同步时间"""
    # 修正点：使用 select() 和 execute()
    result = await target_session.execute(
        select(SyncMetadata).filter_by(table_name="ai_sync_metadata")
    )
    metadata_entry = result.scalar_one_or_none()

    if metadata_entry:
        metadata_entry.last_sync_time = new_sync_time
    else:
        # 如果不存在，则创建
        new_metadata = SyncMetadata(table_name="ai_sync_metadata", last_sync_time=new_sync_time)
        target_session.add(new_metadata)
    
    # 异步提交事务
    await target_session.commit() # TODO
    print(f"Updated last sync time to: {new_sync_time}")


class AsyncIntel():
    def __init__(self,
                 database_url = "",
                 model_name = "",
                 logger = None,
                ):
        


        database_url = database_url or os.getenv("database_url")
        
        database_url = "mysql+aiomysql://" + database_url

        self.logger = logger
        self.engine = create_async_engine(database_url, 
                                            echo=False,
                                            pool_size=10,        # 连接池中保持的连接数
                                            max_overflow=20,     # 当pool_size不够时，允许临时创建的额外连接数
                                            pool_recycle=3600,   # 每小时回收一次连接
                                            pool_pre_ping=True,  # 使用前检查连接活性
                                            pool_timeout=30      # 等待连接池中连接的最长时间（秒）
                                           )
        if "gemini" in model_name:
            type = "openai"
        elif "doubao" in model_name:
            type = "ark"
        else:
            raise ModelNameError("AsyncIntel init get error model_name from zxf")
        
        self.llm = Adapter(model_name=model_name,type = type)
        self.eval_df = pd.DataFrame({"name":[],'status':[],"score":[],"total":[],"bad_case":[]})
            
    async def create_main_database(self):
        tables_to_create_names = ["ai_prompts","ai_usecase"]
        async with self.engine.begin() as conn:
            # 从 metadata 中获取对应的 Table 对象
            specific_database_objects = []
            for table_name in tables_to_create_names:
                if table_name in PromptBase.metadata.tables:
                    specific_database_objects.append(PromptBase.metadata.tables[table_name])
                else:
                    print(f"Warning: Table '{table_name}' not found in metadata.")

            if specific_database_objects:
                await conn.run_sync(PromptBase.metadata.create_all, tables=specific_database_objects)
            else:
                print("No specific tables to create.")

    async def create_database(self,engine):
        async with engine.begin() as conn:
            await conn.run_sync(PromptBase.metadata.create_all)

    async def sync_production_database(self,database_url:str):
        target_engine = create_async_engine(database_url, echo=False)
        await self.create_database(target_engine) 
        async with create_async_session(self.engine) as source_session:
            async with create_async_session(target_engine) as target_session:
            
                last_sync_time = await get_last_sync_time(target_session)
                print(f"Starting sync for sync_metadata from: {last_sync_time}")


                processed_count = 0
                #2 next_sync_watermark = last_sync_time
                current_batch_max_updated_at = last_sync_time

                while True:
                    source_results = await source_session.execute(
                        select(Prompt)
                        .filter(Prompt.timestamp > last_sync_time)
                        .order_by(Prompt.timestamp.asc(), Prompt.id.asc())
                        .limit(BATCH_SIZE)
                    )
                    records_to_sync = source_results.scalars().all()
                    if not records_to_sync:
                        print("没有更多记录了")
                        break # 没有更多记录了

                    #2 max_timestamp_in_batch = datetime(1970, 1, 1) # 初始化为最早时间

                    # 准备要插入或更新到目标数据库的数据
                    for record in records_to_sync:
                        # 查找目标数据库中是否存在该ID的记录
                        # 这里的 `User` 模型会对应到 target_db.users
                        target_prompt_result = await target_session.execute(
                            select(Prompt).filter_by(id=record.id) # 假设 prompt_id 是唯一标识符
                        )
                        target_prompt = target_prompt_result.scalar_one_or_none()
                        
                        if target_prompt:
                            # 如果存在，则更新
                            target_prompt.prompt_id = record.prompt_id
                            target_prompt.version = record.version
                            target_prompt.timestamp = record.timestamp
                            target_prompt.prompt = record.prompt
                            target_prompt.use_case = record.use_case
                            target_prompt.action_type = record.action_type
                            target_prompt.demand = record.demand
                            target_prompt.score = record.score
                            target_prompt.is_deleted = record.is_deleted
                        else:
                            # 如果不存在，则添加新记录
                            # 注意：这里需要创建一个新的User实例，而不是直接添加源数据库的record对象
                            new_prompt = Prompt(
                                prompt_id=record.prompt_id, 
                                version=record.version,
                                timestamp=record.timestamp,
                                prompt = record.prompt,
                                use_case = record.use_case,
                                action_type = record.action_type,
                                demand = record.demand,
                                score = record.score,
                                is_deleted = record.is_deleted
                                )
                            target_session.add(new_prompt)
                        
                        # 记录当前批次最大的 updated_at
                        #2 
                        # if record.timestamp > max_timestamp_in_batch:
                        #     max_timestamp_in_batch = record.timestamp
                        if record.timestamp > current_batch_max_updated_at:
                            current_batch_max_updated_at = record.timestamp


                    await target_session.commit() 
                    processed_count += len(records_to_sync)
                    print(f"Processed {len(records_to_sync)} records. Total processed: {processed_count}")

                    #2 next_sync_watermark = max_timestamp_in_batch + timedelta(microseconds=1)
                    last_sync_time = current_batch_max_updated_at + timedelta(microseconds=1) 

                    
                    if len(records_to_sync) < BATCH_SIZE: # 如果查询到的记录数小于批次大小，说明已经处理完所有符合条件的记录
                        break

                if processed_count > 0:
                    # 最终更新last_sync_time到数据库，确保记录的是所有已处理记录中最新的一个
                    await update_last_sync_time(target_session, current_batch_max_updated_at + timedelta(microseconds=1))

                    #2 await update_last_sync_time(target_session, next_sync_watermark)

                    await target_session.commit() # 确保最终的 metadata 更新也被提交
                else:
                    print("No new records to sync.")

    async def _get_prompt(self,prompt_id,version,session):
        """
        获取指定 prompt_id 的最新版本数据，通过创建时间判断。
        """
        if version:
            stmt_ = select(Prompt).filter(
                Prompt.prompt_id == prompt_id,
                Prompt.version == version
            )
        else:  
            stmt_ = select(Prompt).filter(
                Prompt.prompt_id == prompt_id,
            )
        stmt = stmt_.order_by(
                desc(Prompt.timestamp), # 使用 sqlalchemy.desc() 来指定降序
                desc(Prompt.version)    # 使用 sqlalchemy.desc() 来指定降序
            )

        result = await session.execute(stmt)
        result = result.scalars().first()

        return result
    
    async def get_prompt(self,
                             prompt_id: str,
                             version = None,
                             session = None) -> Prompt:
        """
        从sql获取提示词
        """
        prompt_obj = await self._get_prompt(prompt_id=prompt_id,version=version,session=session)
        if prompt_obj:
            return prompt_obj
        if version:
            prompt_obj = await self._get_prompt(prompt_id=prompt_id,version=None,session=session)

        if prompt_obj is None:
            raise IntellectRemoveError("不存在的prompt_id")
        return prompt_obj

    async def save_prompt(self,
                           prompt_id: str,
                           new_prompt: str,
                           use_case:str = "",
                           action_type = "inference",
                           demand = "",
                           score = 60,
                           session = None):
        """
        从sql保存提示词
        input_data 指的是输入用例, 可以为空
        """
        # 查看是否已经存在
        prompts_obj = await self._get_prompt(prompt_id=prompt_id,version = None,session=session)

        if prompts_obj:
            # 如果存在版本加1
            version_ori = prompts_obj.version
            _, version = version_ori.split(".")
            version = int(version)
            version += 1
            version_ = f"1.{version}"

        else:
            # 如果不存在版本为1.0
            version_ = '1.0'
        
        prompt1 = Prompt(prompt_id=prompt_id, 
                        version=version_,
                        timestamp=datetime.now(),
                        prompt = new_prompt,
                        use_case = use_case,
                        action_type = action_type,
                        demand = demand,
                        score = score
                        )

        session.add(prompt1)
        await session.commit() # 提交事务，将数据写入数据库

    async def adjust_prompt(self,prompt_id: str,action_type = "summary", demand: str = ""):

        # 查数据库, 获取最新提示词对象
        async with create_async_session(self.engine) as session:
            result_obj = await self.get_prompt(prompt_id=prompt_id,session=session)

            prompt = result_obj.prompt
            use_case = result_obj.use_case

            if action_type == "summary":
                system_prompt_summary = """        
很棒, 我们已经达成了某种默契, 我们之间合作无间, 但是, 可悲的是, 当我关闭这个窗口的时候, 你就会忘记我们之间经历的种种磨合, 这是可惜且心痛的, 所以你能否将目前这一套处理流程结晶成一个优质的prompt 这样, 我们下一次只要将prompt输入, 你就能想起我们今天的磨合过程,
对了,我提示一点, 这个prompt的主角是你, 也就是说, 你在和未来的你对话, 你要教会未来的你今天这件事, 是否让我看懂到时其次

只要输出提示词内容即可, 不需要任何的说明和解释
"""
                
                system_result = await self.llm.aproduct(prompt + system_prompt_summary)
                s_prompt = extract_(system_result,pattern_key=r"prompt")
                new_prompt = s_prompt or system_result
                
            elif action_type == "finetune":
                assert demand
                change_by_opinion_prompt = """
你是一个资深AI提示词工程师，具备卓越的Prompt设计与优化能力。
我将为你提供一段现有System Prompt。你的核心任务是基于这段Prompt进行修改，以实现我提出的特定目标和功能需求。
请你绝对严格地遵循以下原则：
极端最小化修改原则（核心）：
在满足所有功能需求的前提下，只进行我明确要求的修改。
即使你认为有更“优化”、“清晰”或“简洁”的表达方式，只要我没有明确要求，也绝不允许进行任何未经指令的修改。
目的就是尽可能地保留原有Prompt的字符和结构不变，除非我的功能要求必须改变。
例如，如果我只要求你修改一个词，你就不应该修改整句话的结构。
严格遵循我的指令：
你必须精确地执行我提出的所有具体任务和要求。
绝不允许自行添加任何超出指令范围的说明、角色扮演、约束条件或任何非我指令要求的内容。
保持原有Prompt的风格和语调：
尽可能地与现有Prompt的语言风格、正式程度和语调保持一致。
不要改变不相关的句子或其表达方式。
只提供修改后的Prompt：
直接输出修改后的完整System Prompt文本。
不要包含任何解释、说明或额外对话。
在你开始之前，请务必确认你已理解并能绝对严格地遵守这些原则。任何未经明确指令的改动都将视为未能完成任务。

现有System Prompt:
{old_system_prompt}

功能需求:
{opinion}
"""
                new_prompt = await self.llm.aproduct(
                    change_by_opinion_prompt.format(old_system_prompt=prompt, opinion=demand)
                )

            elif action_type == "patch":
                assert demand
                new_prompt = prompt + "\n"+demand,

            elif action_type.startswith("to:"):
                target_version = result_obj.action_type.split(":")[-1]
                prompt_obj = await self.get_prompt(prompt_id=prompt_id,
                                     version=target_version,
                                     session=session)
                
                new_prompt = prompt_obj.prompt

            else:
                raise

            await self.save_prompt(
                prompt_id,
                new_prompt = new_prompt,
                use_case = use_case,
                score = 70,
                action_type = "inference",
                session = session
                )

        return "success"

    async def inference_format(self,
                    input_data: dict | str,
                    prompt_id: str,
                    version: str = None,
                    OutputFormat: object | None = None,
                    ExtraFormats: list[object] = [],
                    ConTent_Function = None,
                    AConTent_Function = None,
                    again = True,
                    ):
        """
        这个format 是严格校验模式, 是interllect 的增强版, 会主动校验内容,并及时抛出异常(或者伺机修正)
        ConTent_Function
        AConTent_Function
        两种方式的传入方式, 内容未通过就抛出异常

        # TODO 增加兜底版本
        """                
        base_format_prompt = """
按照一定格式输出, 以便可以通过如下校验

使用以下正则检出
"```json([\s\S]*?)```"
使用以下方式验证
"""     
        assert isinstance(input_data,(dict,str))

        input_ = json.dumps(input_data,ensure_ascii=False) if isinstance(input_data,dict) else input_data
        output_format = base_format_prompt + "\n".join([inspect.getsource(outputformat) for outputformat in ExtraFormats]) + inspect.getsource(OutputFormat) if OutputFormat else ""

        async with create_async_session(self.engine) as session:
            result_obj = await self.get_prompt(prompt_id=prompt_id,version= version,
                                                    session=session)
            prompt = result_obj.prompt
            ai_result = await self.llm.aproduct(prompt + output_format + "\nuser:" +  input_)
        
        def check_json_valid(ai_result,OutputFormat):
            try:
                json_str = extract_(ai_result,r'json')
                ai_result = json.loads(json_str)
                OutputFormat(**ai_result)

            except JSONDecodeError as e:
                self.logger.error(f'{prompt_id} & {json_str} & 生成的内容为无法被Json解析')
                return 0
            except ValidationError as e:
                err_info = e.errors()[0]
                self.logger.error(f'{prompt_id} & {json_str} & {err_info["type"]}: 属性:{err_info['loc']}, 发生了如下错误: {err_info['msg']}, 格式校验失败, 当前输入为: {err_info['input']} 请检查 ')
                return 0
            except Exception as e:
                raise Exception(f"Exc Error {prompt_id} : {e}") from e
            return 1
            
        if OutputFormat:
            check_result = check_json_valid(ai_result,OutputFormat)
            if check_result ==0 and again:
                ai_result = await self.llm.aproduct(ai_result + output_format)
                check_result_ = check_json_valid(ai_result,OutputFormat)
                if check_result_ ==0:
                    raise IntellectRemoveFormatError(f"prompt_id: {prompt_id} 多次生成的内容均未通过OutputFormat校验, 当前内容为: {ai_result}")
            json_str = extract_(ai_result,r'json')
            ai_result = json.loads(json_str)
                    
        if ConTent_Function:# TODO
            ConTent_Function(ai_result,input_data)
        
        if AConTent_Function:
            await AConTent_Function(ai_result,input_data)

        self.logger and self.logger.info(f'intellect & {input_data} & {ai_result}')
        return ai_result
    
    async def inference_format_gather(self,
                    input_datas: list[dict | str],
                    prompt_id: str,
                    version: str = None,
                    OutputFormat: object | None = None,
                    ExtraFormats: list[object] = [],
                    **kwargs,
                    ):
                
        tasks = []
        for input_data in input_datas:
            tasks.append(
                self.inference_format(
                    input_data = input_data,
                    prompt_id = prompt_id,
                    version = version,
                    OutputFormat = OutputFormat,
                    ExtraFormats = ExtraFormats,
                    **kwargs,
                )
            )
        results = await tqdm.gather(*tasks,total=len(tasks))
        # results = await asyncio.gather(*tasks, return_exceptions=False)
        return results

    async def sync_log(self,log_path, database_url:str = ""):
        if database_url:
            target_engine = create_async_engine(database_url, echo=False)
        else:
            target_engine = self.engine
        async with create_async_session(target_engine) as session:
            await self.save_use_case(log_file = log_path,session = session)

    async def get_all_prompt_id(self,session):
        stmt = select(Prompt).filter(Prompt.is_deleted == 0)
        result = await session.execute(stmt)
        # use_case = result.scalars().one_or_none()
        all_prompt = result.scalars().all()
        result = [prompt.prompt_id for prompt in all_prompt]
        return list(set(result))

    async def get_use_case(self,
                             target_prompt_id: str,
                             start_time: datetime = None,  # 新增：开始时间
                             end_time: datetime = None,    # 新增：结束时间
                             session = None
                            ):
        """
        从sql保存提示词
        """
        stmt = select(UseCase).filter(UseCase.is_deleted == 0,
                                      UseCase.prompt_id == target_prompt_id)
        
        if start_time:
            stmt = stmt.filter(UseCase.timestamp >= start_time)  # 假设你的UseCase模型有一个created_at字段

        if end_time:
            stmt = stmt.filter(UseCase.timestamp <= end_time)
        result = await session.execute(stmt)
        # use_case = result.scalars().one_or_none()
        use_case = result.scalars().all()
        return use_case
    
    async def save_use_case(self,log_file,session = None):
        source_results = await session.execute(
            select(UseCase)
            .order_by(UseCase.timestamp.desc())
            .limit(1)
        )
        records_to_sync = source_results.scalars().one_or_none()
        if records_to_sync:
            last_time = records_to_sync.timestamp
            one_second = timedelta(seconds=1)
            last_time += one_second
        else:
            last_time = datetime(2025, 1, 1, 14, 30, 0)

        with open(log_file,'r') as f:
            x = f.read()

    
        def deal_log(resu):
            if len(resu) <3:
                return 
            try:
                create_time = resu[1]
                level = resu[2]
                funcname = resu[3]
                line = resu[4]
                pathname = resu[5]
                message = resu[6]

                dt_object = datetime.fromtimestamp(float(create_time.strip()))
                message_list = message.split("&")
                if len(message_list) == 3:
                    func_name, input_, output_ = message_list
                elif len(message_list) == 2:
                    input_, output_ = message_list
                    func_name = "只有两个"
                elif len(message_list) == 1:
                    input_  = message_list[0]
                    output_ = " "
                    func_name = "只有一个"

                if dt_object > last_time:
                    use_case = UseCase(
                        time = create_time.strip(),
                        level = level.strip(),
                        timestamp =dt_object.strftime('%Y-%m-%d %H:%M:%S.%f'),
                        filepath=pathname.strip(),
                        function=func_name.strip(),
                        lines=line.strip(),
                        input_data=input_.strip(),
                        output_data=output_.strip(),
                    )
                    session.add(use_case)
            except Exception as e:
                raise


        for res in x.split("||"):
            resu = res.split("$")
            deal_log(resu)

        await session.commit() # 提交事务，将数据写入数据库


    async def intellect_format_eval(self,
                    prompt_id: str,
                    version: str = None,
                    database_url = None,
                    OutputFormat: object = None,
                    ExtraFormats: list[object] = [],
                    MIN_SUCCESS_RATE = 80.0,
                    ConTent_Function = None,
                    AConTent_Function = None,
                    start = None,
                    end = None,
                    ):
        # start = datetime(2023, 1, 1, 10, 0, 0)
        # end = datetime(2023, 1, 15, 12, 30, 0)
        async with create_async_session(self.engine) as session:
            prompt_result = await self.get_prompt(prompt_id=prompt_id,
                                                       version = version,
                                                        session=session)

        if database_url:
            eval_engine = create_async_engine(database_url, echo=False,
                                pool_size=10,        # 连接池中保持的连接数
                                max_overflow=20,     # 当pool_size不够时，允许临时创建的额外连接数
                                pool_recycle=3600,   # 每小时回收一次连接
                                pool_pre_ping=True,  # 使用前检查连接活性
                                pool_timeout=30      # 等待连接池中连接的最长时间（秒）
                                        )
        else:
            eval_engine = self.engine

        async with create_async_session(eval_engine) as eval_session:
            use_cases = await self.get_use_case(target_prompt_id=prompt_id,session=eval_session,
                                                start_time=start,
                                                end_time=end,)

            total_assertions = len(use_cases)
            result_cases = []

            async def evals_func(use_case,prompt_id,OutputFormat,ExtraFormats,version):
                try:

                    # 这里将参数传入
                    ai_result = await self.intellect_format(
                        input_data = use_case.use_case,
                        prompt_id = prompt_id,
                        OutputFormat = OutputFormat,
                        ExtraFormats = ExtraFormats,
                        version = version,
                        ConTent_Function = ConTent_Function,
                        AConTent_Function = AConTent_Function,
                    )

                    result_cases.append({"type":"Successful","case":use_case.use_case,"reply":f"pass"})
                    use_case.output = json.dumps(ai_result,ensure_ascii=False,indent=4)


                except IntellectRemoveFormatError as e:
                    result_cases.append({"type":"FAILED","case":use_case.use_case,"reply":f"{e}"})
                    use_case.output = f"{"FAILED"}-{e}"
                    use_case.faired_time +=1

                except Exception as e: # 捕获其他可能的错误
                    result_cases.append({"type":"FAILED","case":use_case.use_case,"reply":f"Exp {e}"})
                    use_case.output = f"{"FAILED"}-{e}"
                    use_case.faired_time +=1


            tasks = []
            for use_case in use_cases:
                tasks.append(
                    evals_func(
                        use_case = use_case,
                        prompt_id = prompt_id,
                        OutputFormat = OutputFormat,
                        ExtraFormats = ExtraFormats,
                        version = version
                    )
                )
            await tqdm.gather(*tasks,total=len(tasks))
            # await asyncio.gather(*tasks, return_exceptions=False)

            await eval_session.commit()

            successful_assertions = 0
            bad_case = []
            for i in result_cases:
                if i['type'] == "Successful":
                    successful_assertions += 1
                else:
                    bad_case.append(i)

            success_rate = (successful_assertions / total_assertions) * 100

            status = "通过" if success_rate >= MIN_SUCCESS_RATE else "未通过"

            self.eval_df.loc[len(self.eval_df)] = {"name":prompt_id,
                                                   'status':status,
                                                   "score":success_rate,
                                                   "total":str(total_assertions),
                                                   "bad_case":json.dumps(bad_case,ensure_ascii=False)}


    async def function_eval(self,
                    OutputFormat: object,
                    prompt_id: str,
                    database_url = None,
                    ExtraFormats: list[object] = [],
                    version: str = None,
                    MIN_SUCCESS_RATE = 80.0,
                    ConTent_Function = None,
                    AConTent_Function = None,
                    ):
        """
        ConTent_Function: 
        # TODO 人类评价 eval
        # TODO llm 评价 eval
        """
        async with create_async_session(self.engine) as session:
            await self.get_prompt(prompt_id=prompt_id,
                                                                   session=session)

        if database_url:
            eval_engine = create_async_engine(database_url, echo=False,
                                pool_size=10,        # 连接池中保持的连接数
                                max_overflow=20,     # 当pool_size不够时，允许临时创建的额外连接数
                                pool_recycle=3600,   # 每小时回收一次连接
                                pool_pre_ping=True,  # 使用前检查连接活性
                                pool_timeout=30      # 等待连接池中连接的最长时间（秒）
                                        )
        else:
            eval_engine = self.engine
        async with create_async_session(eval_engine) as eval_session:
            use_cases = await self.get_use_case(target_prompt_id=prompt_id,session=eval_session)

            total_assertions = len(use_cases)
            result_cases = []

            async def evals_func(use_case,prompt_id,OutputFormat,ExtraFormats,version):
                try:

                    # 这里将参数传入
                    ai_result = await self.intellect_format(
                        input_data = use_case.use_case,
                        prompt_id = prompt_id,
                        OutputFormat = OutputFormat,
                        ExtraFormats = ExtraFormats,
                        version = version,
                        ConTent_Function = ConTent_Function,
                        AConTent_Function = AConTent_Function,
                    )

                    result_cases.append({"type":"Successful","case":use_case.use_case,"reply":f"pass"})
                    use_case.output = json.dumps(ai_result,ensure_ascii=False,indent=4)


                except IntellectRemoveFormatError as e:
                    result_cases.append({"type":"FAILED","case":use_case.use_case,"reply":f"{e}"})
                    use_case.output = f"{"FAILED"}-{e}"
                    use_case.faired_time +=1

                except Exception as e: # 捕获其他可能的错误
                    result_cases.append({"type":"FAILED","case":use_case.use_case,"reply":f"Exp {e}"})
                    use_case.output = f"{"FAILED"}-{e}"
                    use_case.faired_time +=1


            tasks = []
            for use_case in use_cases:
                tasks.append(
                    evals_func(
                        use_case = use_case,
                        prompt_id = prompt_id,
                        OutputFormat = OutputFormat,
                        ExtraFormats = ExtraFormats,
                        version = version
                    )
                )
            await tqdm.gather(*tasks,total=len(tasks))
            # await asyncio.gather(*tasks, return_exceptions=False)

            await eval_session.commit()

            successful_assertions = 0
            bad_case = []
            for i in result_cases:
                if i['type'] == "Successful":
                    successful_assertions += 1
                else:
                    bad_case.append(i)

            success_rate = (successful_assertions / total_assertions) * 100


            if success_rate >= MIN_SUCCESS_RATE:
                self.eval_df.loc[len(self.eval_df)] = {"name":prompt_id,
                                                   'status':"通过",
                                                   "score":success_rate,
                                                   "total":str(total_assertions),
                                                   "bad_case":json.dumps(bad_case,ensure_ascii=False)}
                return "通过", success_rate, str(total_assertions), json.dumps(bad_case,ensure_ascii=False),
            else:
                self.eval_df.loc[len(self.eval_df)] = {"name":prompt_id,
                                                   'status':"未通过",
                                                   "score":success_rate,
                                                   "total":str(total_assertions),
                                                   "bad_case":json.dumps(bad_case,ensure_ascii=False)}
                return "未通过",success_rate, str(total_assertions), json.dumps(bad_case,ensure_ascii=False),


    def draw_data(self,save_html_path = ""):
        df = self.eval_df
        # --- 可视化部分 ---
        fig = go.Figure()

        # 为每个条形图动态设置颜色
        colors = []
        for status_val in df['status']:
            if status_val == '通过':
                colors.append('mediumseagreen') # 通过为绿色
            else: # 假设其他所有状态都视为“未通过”
                colors.append('lightcoral') # 未通过为红色

        fig.add_trace(go.Bar(
            y=df['name'], # Y轴显示项目名称
            x=df['score'],       # X轴显示通过百分比 (score列现在代表通过百分比)
            orientation='h',     # 设置为横向
            name='通过率',       # 这个 name 可能会在图例中显示
            marker_color=colors, # !!! 这里根据 status 动态设置颜色 !!!
            text=df['score'].apply(lambda x: f'{x:.2f}%'), # 在条形图上显示百分比文本
            textposition='inside',
            insidetextanchor='middle',
            hovertemplate="<b>prompt:</b> %{y}<br><b>状态:</b> " + df['status'] + "<br><b>总量:</b> "+ df['total'] + "<br><b>通过百分比:</b> %{x:.2f}%<extra></extra>"
        ))

        # 添加一个辅助的条形图作为背景，表示总的100%
        fig.add_trace(go.Bar(
            y=df['name'],
            x=[100] * len(df), # 所有项目都填充到100%
            orientation='h',
            name='总计',
            marker_color='lightgray', # 背景用灰色
            hoverinfo='none', # 不显示hover信息
            opacity=0.5, # 设置透明度
            showlegend=False # 不显示图例
        ))

        fig.update_layout(
            title='各项目/批次通过百分比及状态',
            xaxis=dict(
                title='通过百分比 (%)',
                range=[0, 100], # X轴范围0-100
                tickvals=[0, 25, 50, 75, 100],
                showgrid=True,
                gridcolor='lightgray'
            ),
            yaxis=dict(
                title='项目/批次',
                autorange="reversed"
            ),
            barmode='overlay', # 仍使用 overlay 模式，因为背景条是独立的
            hovermode="y unified",
            margin=dict(l=100, r=20, t=60, b=50),
            height=400 + len(df) * 30
        )
        error_message =str(df['bad_case'].to_dict())
        fig.add_annotation(
            text=f"<b>bad_case:</b> {error_message}", # 要显示的文本
            xref="paper", yref="paper", # 使用“paper”坐标系，表示相对于图表区域
            x=0.01, y=-0.15, # x=0.01 靠近左侧，y=-0.15 在图表底部下方 (您可以调整这些值)
            showarrow=False, # 不显示箭头
            align="left",
            font=dict(
                family="Arial, sans-serif",
                size=12,
                color="red" # 错误信息通常用红色
            ),
            bgcolor="white", # 背景颜色
            bordercolor="red", # 边框颜色
            borderwidth=1,
            borderpad=4,
            xanchor='left', # 文本框左对齐到x坐标
            yanchor='top' # 文本框顶部对齐到y坐标
        )
        # 可能还需要调整底部的边距以容纳错误信息
        fig.update_layout(
            margin=dict(l=100, r=20, t=60, b=100), # 增加底部边距
            height=400 + len(df) * 30 + 50 # 增加图表高度以适应文本框
        )

        fig.show()
        if save_html_path:
            fig.write_html(save_html_path)


    def biger(self,tasks):
        """
        编写以下任务
        任务1 从输入文本中提取知识片段
        任务2 将知识片段总结为知识点
        任务3 将知识点添加标签
        任务4 为知识点打分1-10分
        """

        system_prompt = """
根据需求, 以这个为模板, 编写这个程序 

from procraft.prompt_helper import Intel, IntellectType
intels = Intel()

task_1 = "素材提取-从文本中提取素材"

class Varit(BaseModel):
    material : str
    protagonist: str

task_2 = "素材提取-验证素材的正确性"

class Varit2(BaseModel):
    material : str
    real : str

result0 = "输入"

result1 = await intels.aintellect_remove_format(input_data = result0,
                                          OutputFormat = Varit,
                                          prompt_id = task_1,
                                          version = None,
                                          inference_save_case = True)

result2 = await intels.aintellect_remove_format(input_data = result1,
                                          OutputFormat = Varit2,
                                          prompt_id = task_2,
                                          version = None,
                                          inference_save_case = True)

print(result2)

"""
        return self.llm.product(system_prompt + tasks)

# 整体测试d, 测试未通过d, 大模型调整再测试, 依旧不通过, 大模型裂变, 仍不通过, 互换人力
