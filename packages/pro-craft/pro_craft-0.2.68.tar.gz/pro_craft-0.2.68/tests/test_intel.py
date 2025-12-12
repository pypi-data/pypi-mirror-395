from pro_craft import Intel
from pro_craft import AsyncIntel,Intel
from pro_craft.utils import create_async_session
import pytest
from dotenv import load_dotenv
load_dotenv(".env", override=True)

from pro_craft import logger

class Test_Intel():

    @pytest.fixture
    def intels(self):
        intels = Intel("mysql+pymysql://zxf_root:Zhf4233613%40@rm-2ze0793c6548pxs028o.mysql.rds.aliyuncs.com:3306/serverz")
        return intels
    
    def test_intel_init(self):
        intels = Intel("")

    def test_sync_prompt_data_to_database(self,intels):
        intels.sync_prompt_data_to_database("mysql+pymysql://zxf_root:Zhf4233613%40@rm-2ze0793c6548pxs028o.mysql.rds.aliyuncs.com:3306/serverz3")


    def test_push_action_order(self,intels):

        result = intels.push_action_order(
            prompt_id = "自动编写Test2",
            demand = "这是一个不错的角度 加油啊aab",
            action_type = "train",
                )
        print(result)

    def test_intellect_remove(self,intels):
        result = intels.intellect_remove(input_data =  "你好a",
                            output_format = """```json
{
"text":一些内容
}
```
""",
                              prompt_id = "自动编写Test2",
                           )
        print(result,'result')


    def test_intellect_remove_format(self,intels):
        from pydantic import BaseModel

        class Varit(BaseModel):
            material : str
            protagonist: str

        result = intels.intellect_remove_format(
            input_data =  "你好a",
            prompt_id = "自动编写Test2",
            OutputFormat = Varit,
                           )
        print(result,'result')

    def test_intellect_remove_warp(self,intels):
        from pydantic import BaseModel

        class Output(BaseModel):
            text : str
        
        @intels.intellect_remove_warp(prompt_id = "自动编写Test2")
        def work1(input_data,OutputFormat:BaseModel):
            result_dict = input_data
            return result_dictc
            
        result = work1(input_data =  "你好 我叫赵雪峰",OutputFormat = Output )
        print(result,'result')



class Test_AsyncIntel():

    @pytest.fixture
    def intels(self):
        intels = AsyncIntel(database_url = "mysql+aiomysql://zxf_root:Zhf4233613%40@rm-2ze0793c6548pxs028o.mysql.rds.aliyuncs.com:3306/serverz",
                            model_name="doubao-1-5-pro-256k-250115")
        return intels
    
    async def test_create_main_database(self,intels):
        # 创建数据库
        intels = AsyncIntel(database_url = "mysql+aiomysql://zxf_root:Zhf4233613%40@rm-2ze0793c6548pxs028o.mysql.rds.aliyuncs.com:3306/serverz",
                            model_name="doubao-1-5-pro-256k-250115")
        await intels.create_main_database()

    async def test_sync_use_case(self,intels):
        # 上传日志
        async with create_async_session(intels.engine) as session:
            await intels.save_use_case(log_file = "/Users/zhaoxuefeng/GitHub/digital_life/logs/app_info.log",
                                       session = session)

    async def test_sync_prompt_data_to_database(self,intels):
        # 同步数据到生产库
        await intels.sync_prompt_data_to_database("mysql+aiomysql://zxf_root:Zhf4233613%40@rm-2ze0793c6548pxs028o.mysql.rds.aliyuncs.com:3306/serverz3")

    async def test_get_prompt(self,intels):
        intels = AsyncIntel(database_url = "mysql+aiomysql://zxf_root:Zhf4233613%40@rm-2ze0793c6548pxs028o.mysql.rds.aliyuncs.com:3306/serverz",
                    model_name="doubao-1-5-pro-256k-250115")
        async with create_async_session(intels.engine) as session:
            x = await intels._get_latest_prompt_version(target_prompt_id = "自动编写Test2",session = session)
            
            print(x.version,'x')
            y = await intels.get_prompt(prompt_id = "自动编写Test2",version = "1.20",session = session)
            # _get_latest_prompt_version22
            print(y,'y')

    
    async def test_apush_action_order(self,intels):

        result = await intels.push_action_order(
            prompt_id = "自动编写Test1",
            demand = "这是一个测试",
            action_type = "train",
                )
        print(result)

    async def test_aintellect_remove(self,intels):
        result = await intels.intellect_remove(input_data =  "你好b",
                            output_format = """```json
{
"text":一些内容
}
```
""",
                              prompt_id = "自动编写Test1",
                              inference_save_case = True,
                           )
        print(result,'result')

    async def test_aintellect_stream_remove(self,intels):
        result = intels.aintellect_stream_remove(input_data =  "你好b",
                            output_format = """```json
{
"text":一些内容
}
```
""",
                              prompt_id = "自动编写Test2",
                           )
        async for i in result:
            print(i,'result')

    async def test_aintellect_remove_format(self,intels):
        from pydantic import BaseModel

        class Varit(BaseModel):
            material : str
            protagonist: str

        result = await intels.aintellect_remove_format(
            input_data =  "你好abb",
            prompt_id = "自动编写Test2",
            OutputFormat = Varit,
                           )
        print(result,'result')

    async def test_aintellect_remove_warp(self,intels):
        from pydantic import BaseModel

        class Output(BaseModel):
            text : str
        
        @intels.aintellect_remove_warp(prompt_id = "自动编写Test2")
        async def work1(input_data,OutputFormat:BaseModel):
            result_dict = input_data
            return result_dict
            
        result = await work1(input_data =  "你好 我叫赵雪峰",OutputFormat = Output )
        print(result,'result')

    async def test_aintellect_remove_eval(self,intels):
        from pydantic import BaseModel

        class Output(BaseModel):
            text : str
        
        result = await intels.intellect_remove_format_eval(
            prompt_id = "自动编写Test2",
            OutputFormat = Output,)
        print(result,'result')
            

# 整体测试, 测试未通过, 大模型调整再测试, 依旧不通过, 大模型裂变, 仍不通过, 互换人力

