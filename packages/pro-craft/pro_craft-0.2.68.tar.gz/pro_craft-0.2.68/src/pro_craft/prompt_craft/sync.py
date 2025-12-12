# 测试1

from pro_craft.utils import extract_
from pro_craft import logger as pro_craft_logger
from pro_craft.database import Prompt, UseCase, PromptBase
from pro_craft.utils import create_session, create_async_session
from modusched.core import BianXieAdapter, ArkAdapter
from datetime import datetime
from enum import Enum
import functools
import json
import os
from sqlalchemy import create_engine
from pro_craft.database import SyncMetadata
import inspect
from datetime import datetime, timedelta
from json.decoder import JSONDecodeError


BATCH_SIZE = 1000

class IntellectRemoveFormatError(Exception):
    pass

class IntellectRemoveError(Exception):
    pass

def slog(s, target: str = "target",logger = None):
    COLOR_GREEN = "\033[92m"
    COLOR_RESET = "\033[0m" # 重置颜色
    logger("\n"+f"{COLOR_GREEN}=={COLOR_RESET}" * 50)
    logger(target + "\n       "+"--" * 40)
    logger(type(s))
    logger(s)
    logger("\n"+f"{COLOR_GREEN}=={COLOR_RESET}" * 50)




def get_last_sync_time(target_session) -> datetime:
    """从目标数据库获取上次同步时间"""
    metadata_entry = target_session.query(SyncMetadata).filter_by(table_name="ai_sync_metadata").first()
    if metadata_entry:
        return metadata_entry.last_sync_time
    return datetime(1970, 1, 1) # 默认一个很早的时间

def update_last_sync_time(target_session, new_sync_time: datetime):
    """更新目标数据库的上次同步时间"""
    metadata_entry = target_session.query(SyncMetadata).filter_by(table_name="ai_sync_metadata").first()
    if metadata_entry:
        metadata_entry.last_sync_time = new_sync_time
    else:
        # 如果不存在，则创建
        new_metadata = SyncMetadata(table_name="ai_sync_metadata", last_sync_time=new_sync_time)
        target_session.add(new_metadata)
    target_session.commit()
    print(f"Updated last sync time to: {new_sync_time}")



class IntellectType(Enum):
    train = "train"
    inference = "inference"
    summary = "summary"



class Intel():
    def __init__(self,
                 database_url = "",
                 model_name = "",
                 logger = None,
                ):
        database_url = database_url or os.getenv("database_url")
        assert database_url
        assert "aiomysql" not in database_url
        self.engine = create_engine(database_url, echo=False, # echo=True 仍然会打印所有执行的 SQL 语句
                                    pool_size=10,        # 连接池中保持的连接数
                                    max_overflow=20,     # 当pool_size不够时，允许临时创建的额外连接数
                                    pool_recycle=3600,   # 每小时回收一次连接
                                    pool_pre_ping=True,  # 使用前检查连接活性
                                    pool_timeout=30      # 等待连接池中连接的最长时间（秒）
                                    ) 

        PromptBase.metadata.create_all(self.engine)
        
        if model_name in ["gemini-2.5-flash-preview-05-20-nothinking",]:
            self.llm = BianXieAdapter(model_name = model_name)
        elif model_name in ["doubao-1-5-pro-256k-250115","doubao-1-5-pro-32k-250115"]:
            self.llm = ArkAdapter(model_name = model_name)
        else:
            raise Exception("error llm name")
        self.logger = logger or pro_craft_logger
        
    def _get_latest_prompt_version(self,target_prompt_id,session):
        """
        获取指定 prompt_id 的最新版本数据，通过创建时间判断。
        """
        result = session.query(Prompt).filter(
            Prompt.prompt_id == target_prompt_id
        ).order_by(
            Prompt.timestamp.desc(),
            Prompt.version.desc()
        ).first()
        return result

    def _get_specific_prompt_version(self,target_prompt_id, target_version,session):
        """
        获取指定 prompt_id 和特定版本的数据。

        Args:
            target_prompt_id (str): 目标提示词的唯一标识符。
            target_version (int): 目标提示词的版本号。
            table_name (str): 存储提示词数据的数据库表名。
            db_manager (DBManager): 数据库管理器的实例，用于执行查询。

        Returns:
            dict or None: 如果找到，返回包含 id, prompt_id, version, timestamp, prompt 字段的字典；
                        否则返回 None。
        """
        result = session.query(Prompt).filter(
            Prompt.prompt_id == target_prompt_id,
            Prompt.version == target_version
        ).first() # 因为 (prompt_id, version) 是唯一的，所以 first() 足够
        return result
    
    def sync_prompt_data_to_database(self,database_url:str):
        target_engine = create_engine(database_url, echo=False)
        PromptBase.metadata.create_all(target_engine) 

        with create_session(self.engine) as source_session:
            with create_session(target_engine) as target_session:
                last_sync_time = get_last_sync_time(target_session)
                print(f"Starting sync for sync_metadata from: {last_sync_time}")


                processed_count = 0
                current_batch_max_updated_at = last_sync_time

                while True:
                    records_to_sync = source_session.query(Prompt)\
                                .filter(Prompt.timestamp > last_sync_time)\
                                .order_by(Prompt.timestamp.asc(), Prompt.id.asc())\
                                .limit(BATCH_SIZE)\
                                .all()
                    if not records_to_sync:
                        break # 没有更多记录了

                    # 准备要插入或更新到目标数据库的数据
                    for record in records_to_sync:
                        # 查找目标数据库中是否存在该ID的记录
                        # 这里的 `User` 模型会对应到 target_db.users
                        target_prompt = target_session.query(Prompt).filter_by(id=record.id).first()

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
                            new_user = Prompt(
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
                            target_session.add(new_user)
                        
                        # 记录当前批次最大的 updated_at
                        if record.timestamp > current_batch_max_updated_at:
                            current_batch_max_updated_at = record.timestamp

                    target_session.commit() # 提交当前批次的变更
                    processed_count += len(records_to_sync)
                    print(f"Processed {len(records_to_sync)} records. Total processed: {processed_count}")

                    last_sync_time = current_batch_max_updated_at + timedelta(microseconds=1) 
                    
                    if len(records_to_sync) < BATCH_SIZE: # 如果查询到的记录数小于批次大小，说明已经处理完所有符合条件的记录
                        break

                if processed_count > 0:
                    # 最终更新last_sync_time到数据库，确保记录的是所有已处理记录中最新的一个
                    update_last_sync_time(target_session, current_batch_max_updated_at + timedelta(microseconds=1))
                else:
                    print("No new records to sync.")

    def get_prompts_from_sql(self,
                             prompt_id: str,
                             version = None,
                             session = None) -> Prompt:
        """
        从sql获取提示词
        """
        # 查看是否已经存在
        if version:
            prompts_obj = self._get_specific_prompt_version(prompt_id,version,session=session)
            if not prompts_obj:
                prompts_obj = self._get_latest_prompt_version(prompt_id,session = session)
        else:
            prompts_obj = self._get_latest_prompt_version(prompt_id,session = session)     
        return prompts_obj
            
    def save_prompt_increment_version(self,
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
        prompts_obj = self.get_prompts_from_sql(prompt_id=prompt_id,session=session)
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
        session.commit()

    def save_use_case_by_sql(self,
                             prompt_id: str,
                             use_case:str = "",
                             output = "",
                             solution: str = "",
                             session = None
                            ):
        """
        从sql保存提示词
        """
        use_case = UseCase(prompt_id=prompt_id, 
                        use_case = use_case,
                        output = output,
                        solution = solution,
                        )
        session.add(use_case)
        session.commit() # 提交事务，将数据写入数据库

    def summary_to_sql(
            self,
            prompt_id:str,
            version = None,
            prompt = "",
            session = None
        ):
        """
        让大模型微调已经存在的 system_prompt
        """
        system_prompt_created_prompt = """        
很棒, 我们已经达成了某种默契, 我们之间合作无间, 但是, 可悲的是, 当我关闭这个窗口的时候, 你就会忘记我们之间经历的种种磨合, 这是可惜且心痛的, 所以你能否将目前这一套处理流程结晶成一个优质的prompt 这样, 我们下一次只要将prompt输入, 你就能想起我们今天的磨合过程,
对了,我提示一点, 这个prompt的主角是你, 也就是说, 你在和未来的你对话, 你要教会未来的你今天这件事, 是否让我看懂到时其次

只要输出提示词内容即可, 不需要任何的说明和解释
"""
        system_result = self.llm.product(prompt + system_prompt_created_prompt)
        s_prompt = extract_(system_result,pattern_key=r"prompt")
        chat_history = s_prompt or system_result
        self.save_prompt_increment_version(prompt_id,
                                new_prompt = chat_history,
                                use_case = " summary ",
                                session = session)
        
    def prompt_finetune_to_sql(
            self,
            prompt_id:str,
            version = None,
            demand: str = "",
            session = None,
        ):
        """
        让大模型微调已经存在的 system_prompt
        """
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
        prompts_obj = self.get_prompts_from_sql(prompt_id = prompt_id,version = version,session = session)

        if demand:
            new_prompt = self.llm.product(
                change_by_opinion_prompt.format(old_system_prompt=prompts_obj.prompt, opinion=demand)
            )
        else:
            new_prompt = prompts_obj.prompt
        self.save_prompt_increment_version(prompt_id = prompt_id,
                            new_prompt = new_prompt,
                            use_case = "finetune",
                            session = session)

    def push_action_order(self,
                          prompt_id: str,
                          demand : str,
                          action_type = 'train'):

        """
        从sql保存提示词
        推一个train 状态到指定的位置

        将打算修改的状态推上数据库 # 1
        """
        # 查看是否已经存在
        with create_session(self.engine) as session:
            latest_prompt = self.get_prompts_from_sql(prompt_id=prompt_id,session=session)
               
            if latest_prompt:
                self.save_prompt_increment_version(prompt_id=latest_prompt.prompt_id,
                                        new_prompt = latest_prompt.prompt,
                                        use_case = latest_prompt.use_case,
                                        action_type=action_type,
                                        demand=demand,
                                        score=latest_prompt.score,
                                        session=session
                                        )
                
                return "success"
            else:
                self.save_prompt_increment_version(prompt_id=prompt_id,
                                    new_prompt = demand,
                                    use_case = "init",
                                    action_type="inference",
                                    demand=demand,
                                    score=60,
                                    session=session
                                    )
                return "init"

    def intellect_remove(self,
                    input_data: dict | str,
                    output_format: str,
                    prompt_id: str,
                    version: str = None,
                    inference_save_case = True,
                    push_patch = False,
                    ):
        """
        使用指南:
            1 训练, 使用单一例子做大量的沟通来奠定基础
            2 总结, 将沟通好的总结成完整提示词
            3 推理, 使用部署
            4 微调, 针对一些格式性的, 问题进行微调
            5 补丁, 微调无法解决的问题, 可以尝试使用补丁来解决
        """
        if isinstance(input_data,dict):
            input_ = json.dumps(input_data,ensure_ascii=False)
        elif isinstance(input_data,str):
            input_ = input_data

        
        # 查数据库, 获取最新提示词对象
        with create_session(self.engine) as session:
            result_obj = self.get_prompts_from_sql(prompt_id=prompt_id,session=session)

            if result_obj is None:
                raise IntellectRemoveError("不存在的prompt_id")
            prompt = result_obj.prompt
            if result_obj.action_type == "inference":
                # 直接推理即可
                ai_result = self.llm.product(prompt + output_format + "\n-----input----\n" +  input_)
                if inference_save_case:
                    self.save_use_case_by_sql(prompt_id,
                                        use_case = input_,
                                        output = ai_result,
                                        solution = "备注/理想回复",
                                        session = session,
                                        )
                    
            elif result_obj.action_type == "train":
                assert result_obj.demand # 如果type = train 且 demand 是空 则报错
                # 则训练推广

                # 新版本 默人修改会 inference 状态
                prompt = result_obj.prompt
                before_input = result_obj.use_case
                demand = result_obj.demand

                # assert demand
                # # 注意, 这里的调整要求使用最初的那个输入, 最好一口气调整好
                
                # if input_ == before_input: # 输入没变, 说明还是针对同一个输入进行讨论
                #     # input_prompt = chat_history + "\nuser:" + demand
                #     input_prompt = chat_history + "\nuser:" + demand + output_format 
                # else:
                #     # input_prompt = chat_history + "\nuser:" + demand + "\n-----input----\n" + input_
                #     input_prompt = chat_history + "\nuser:" + demand + output_format  + "\n-----input----\n" + input_
            
                # ai_result = self.llm.product(input_prompt)
                # chat_history = input_prompt + "\nassistant:\n" + ai_result # 用聊天记录作为完整提示词

                if input_ == before_input:
                    new_prompt = prompt + "\nuser:" + demand
                else:
                    new_prompt = prompt + "\nuser:" + input_

                ai_result = self.llm.product(new_prompt + output_format)

                save_new_prompt = new_prompt + "\nassistant:\n" + ai_result


                self.save_prompt_increment_version(prompt_id, 
                                        new_prompt=save_new_prompt,
                                        use_case = input_,
                                        score = 60,
                                        session = session)
    
            elif result_obj.action_type == "summary":
                self.summary_to_sql(prompt_id = prompt_id,
                            prompt = prompt,
                            session = session
                            )
                ai_result = self.llm.product(prompt + output_format + "\n-----input----\n" +  input_)

            elif result_obj.action_type == "finetune":
                demand = result_obj.demand
            
                assert demand
                self.prompt_finetune_to_sql(prompt_id = prompt_id,
                                            demand = demand,
                                            session = session
                                            )
                ai_result = self.llm.product(prompt + output_format + "\n-----input----\n" +  input_)
            elif result_obj.action_type == "patch":
                
                demand = result_obj.demand
                assert demand

                chat_history = prompt + demand
                ai_result = self.llm.product(chat_history + output_format + "\n-----input----\n" +  input_)
                if push_patch:
                    self.save_prompt_increment_version(prompt_id, chat_history,
                                            use_case = input_,
                                            score = 60,
                                            session = session)
            else:
                raise


        return ai_result
    

    def intellect_remove_format(self,
                    input_data: dict | str,
                    prompt_id: str,
                    OutputFormat: object = None,
                    ExtraFormats: list[object] = [],
                    version: str = None,
                    inference_save_case = True,
                    ):
        
        if OutputFormat:
            base_format_prompt = """
按照一定格式输出, 以便可以通过如下校验

使用以下正则检出
"```json([\s\S]*?)```"
使用以下方式验证
"""
            output_format = base_format_prompt + "\n".join([inspect.getsource(outputformat) for outputformat in ExtraFormats]) + inspect.getsource(OutputFormat)

        else:
            output_format = ""

        ai_result = self.intellect_remove(
            input_data=input_data,
            output_format=output_format,
            prompt_id=prompt_id,
            version=version,
            inference_save_case=inference_save_case
        )

        if OutputFormat:
            try:
                ai_result_ = json.loads(extract_(ai_result,r'json'))
                OutputFormat(**ai_result_)

            except JSONDecodeError as e:
                slog(ai_result,logger=self.logger.error)
                raise IntellectRemoveFormatError(f"prompt_id: {prompt_id} 在生成后做json解析时报错") from e

        else:
            try:
                assert isinstance(ai_result,str)
            except AssertionError as e:
                slog(ai_result,logger=self.logger.error)
                raise IntellectRemoveFormatError(f"prompt_id: {prompt_id} 生成的结果 期待是字符串, 但是错误") from e
       
        return ai_result
    
    def intellect_remove_warp(self,prompt_id: str):
        def outer_packing(func):
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                # 修改逻辑
                assert kwargs.get('input_data') # 要求一定要有data入参
                input_data = kwargs.get('input_data')
                assert kwargs.get('OutputFormat') # 要求一定要有data入参
                OutputFormat = kwargs.get('OutputFormat')

                if isinstance(input_data,dict):
                    input_ = output_ = json.dumps(input_data,ensure_ascii=False)
                elif isinstance(input_data,str):
                    input_ = output_ = input_data

                output_ = self.intellect_remove_format(
                        input_data = input_data,
                        prompt_id = prompt_id,
                        OutputFormat = OutputFormat,
                )

                kwargs.update({"input_data":output_})
                result = func(*args, **kwargs)
                return result
            return wrapper
        return outer_packing

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