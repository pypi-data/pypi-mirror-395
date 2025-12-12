from pro_craft import Intel
from pro_craft.log import Log
from pro_craft.utils import extract_
from typing import List, Dict, Any
from modusched.core import BianXieAdapter
import re
import json

logger = Log.logger

intel = Intel(model_name="doubao-1-5-pro-256k-250115")

class CoderHelper():
    def __init__(self):
        self.bx = BianXieAdapter()


    @intel.intellect_remove_warp(prompt_id ="代码修改-最小化改动001")
    def minedit_prompt(self,input:dict):
        # 可以做pydantic 的校验
        input = extract_(input, pattern_key = r"python")
        return input

    @intel.intellect_remove_warp(prompt_id ="高定制化自由函数修改_001")
    def free_function_prompt(self,input:dict,kwargs):
        # 可以做pydantic 的校验
        result_ = extract_(input, pattern_key = r"python")
        if not result_:
            return None
        
        complet_code = result_ + "\n" + f'result = Function(**{kwargs})'
            
        rut = {"result": ""}
        # 使用exec执行代码，并捕获可能的错误
        try:
            exec(
                complet_code, globals(), rut
            )  # 将globals()作为全局作用域，避免依赖外部locals()
        except Exception as e:
            logger.error(f"执行动态生成的代码时发生错误: {e}")
            return None  # 返回None或抛出异常

        return rut.get("result")
    
    def min_edit(self,code:str, edit_demand:str):
        input_ = {"源码":code,
                "功能需求":edit_demand
                }
        data = self.minedit_prompt(input = input_)
        return data
    
    def free_function(self,function: str ="帮我将 日期 2025/12/03 向前回退12天", 
                      **kwargs):
        # params = locals()
        prompt_user_part = f"{function}"
        if kwargs:
            prompt_user_part += "入参 : \n"
            prompt_user_part += json.dumps(kwargs,ensure_ascii=False)

        exec_result = self.free_function_prompt(input = prompt_user_part,kwargs = kwargs)

        return exec_result

        
    def free_function_advanced(self):
        pass

class Paper():
    def __init__(self,content):
        self.content = content

    @intel.intellect_remove_warp(prompt_id ="白板编辑-修改画板001")
    def system_prompt(self,data):
        return data
        
    def talk(self,prompt:str):
        data = {"data":self.content+ prompt}
        result = self.system_prompt(data = data)
        # result = bx.product(system_prompt+ self.content+ prompt)
        print(result,'result')
        result_json = json.loads(extract_(result,pattern_key = r"json"))
        print(result_json,'result_json')
        for ops in result_json:
            self.deal(ops.get('type'), ops.get('operations'))
            
    
    def deal(self, type_, operations:str):
        if type_ == "add":
            self.add(operations)
        elif type_ == "delete":
            self.delete(operations)
        else:
            print('error')

    def add(self, operations:str):
        print('add running')
        match_tips = re.search(r'<mark>(.*?)</mark>', operations, re.DOTALL)
        positon_ = operations.replace(f"<mark>{match_tips.group(1)}</mark>","")
        # 锁定原文
        positon_frist = operations.replace('<mark>',"").replace('</mark>',"")
        print(positon_frist,'positon_frist')
        print('==========')
        print(positon_,'positon__')
        self.content = self.content.replace(positon_,positon_frist)

    def delete(self, operations:str):   
        # 制定替换内容
        print('delete running')
        match_tips = re.search(r'<mark>(.*?)</mark>', operations, re.DOTALL)
        positon_ = operations.replace(f"<mark>{match_tips.group(1)}</mark>","")
        # 锁定原文
        positon_frist = operations.replace('<mark>',"").replace('</mark>',"")
        print(positon_frist,'positon_frist')
        assert positon_frist in self.content
        print('==========')
        print(positon_,'positon__')
        
        self.content = self.content.replace(positon_frist,positon_)



mermaid_format = """
```mermaid
{result}
```"""

class ProgramChart():
    '''
    # ## 有一个原始的程序框图, -> 可以通过需求来调整程序框图 -> 结合数据库来调度程序框图
    # 一个新的任务, => 基本需求, -> 根据需求调取之前的程序框图, -> 融合程序框图 -> 调整程序框图到完成满意,-> 由程序框图实现代码, 并拉取出待实现函数
    # -> 用知识库中获取代码与对应的测试, 整合到待实现函数中, -> 剩余的使用封装好的包进行补充, -> 创新的补充, -> ...


    inputs = """
    帮我实现一个文件读取的逻辑
    """
    program_chart = init_program_chart_mermaid(inputs) # TODO 类图另做吧
    # 一直循环, 直到满意
    program_chart = finetune_program_chart(program_chart + "如果文件不存在, 就创建")
    codes = fill_code_frame_program_chart(program_chart) #TODO 可以尝试配置对应的pytest

    '''

    # TODO 数据用例等, 只是保存, 真正做统计的时候可以导出选择合适的数据

    @intel.intellect_remove_warp(prompt_id="程序框图-根据需求创建")
    def init_program_chart_mermaid(self,input_data:str,
                                   output_format:str):
        result = extract_(input_data,r"mermaid")
        input_ = mermaid_format.format(result = result)

        with open("/Users/zhaoxuefeng/GitHub/obsidian/工作/TODO/1根据需求创建.md",'w') as f:
            f.write(input_)
        return input_

    @intel.intellect_remove_warp(prompt_id="程序框图-白板微调")
    def finetune_program_chart(self,input_data:str,
                                   output_format:str):
        print(input_data,'input_datainput_datainput_data')
        result = extract_(input_data,r"mermaid")
        input_ = mermaid_format.format(result = result)
        with open("/Users/zhaoxuefeng/GitHub/obsidian/工作/TODO/1根据需求创建.md",'w') as f:
            f.write(input_)
        return input_

    @intel.intellect_remove_warp(prompt_id="程序框图-框架实现")
    def fill_code_frame_program_chart(self,input:dict):
        # result = extract_(input.get("program_chart"),r"python")
        code = input.get("program_chart")

        with open("/Users/zhaoxuefeng/GitHub/obsidian/工作/TODO/3框架实现.md",'w') as f:
            f.write(code)
        return code

    def pc_work(self,chat,fill = False):
        self.init_program_chart_mermaid(chat)

        program_chart = self.finetune_program_chart

        code = self.fill_code_frame_program_chart(input = {
            "program_chart":program_chart
        })

