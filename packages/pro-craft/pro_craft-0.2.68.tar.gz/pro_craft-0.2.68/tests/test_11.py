from pro_craft.prompt_craft.async_ import AsyncIntel

import os

async def test_1():
    intels = AsyncIntel(database_url=os.getenv("adatabase_url"),model_name="doubao-1-5-pro-32k-250115")
    # 先使用该函数,实现,创建, 初始化, 训练等等
    result = await intels.push_action_order(
            # demand='以下是一个代码模板, 我希望你做的是, 根据要求微调代码模板来构建代码```pythonfrom pydantic import BaseModel, Fieldfrom pro_craft import AsyncIntelinference_save_case = Falsemodel_name = "doubao-1-5-pro-256k-250115"inters = AsyncIntel(model_name = model_name)## modelsclass Chapter(BaseModel):    """    表示文档中的一个记忆卡片（章节）。    """    title: str = Field(..., description="记忆卡片的标题")    content: str = Field(..., description="记忆卡片的内容")class Document(BaseModel):    """    表示一个包含标题和多个记忆卡片的文档。    """    title: str = Field(..., description="整个文档的标题内容")    chapters: List[Chapter] = Field(..., description="文档中包含的记忆卡片列表")    ## modelsasync def amemory_card_merge(memory_cards: list[str]):    memoryCards_str, memoryCards_time_str = memoryCards2str(memory_cards)    input_data = memoryCards_str + "各记忆卡片的时间" + memoryCards_time_str        result = await inters.intellect_remove_format(        input_data= input_data,        prompt_id = "memorycard-merge",        version = None,        inference_save_case=inference_save_case,        OutputFormat = Document,        ExtraFormats=[Chapter],    )    return result```',
            demand="添加一些注释",
            prompt_id="zxf_code_template_2",
            action_type="to:1.8"
        )
    print(result)



async def test_work():
    intels = AsyncIntel(database_url=os.getenv("adatabase_url"),model_name="doubao-1-5-pro-32k-250115")
    # @intels.intellect_warp("zxf_code_template")
    # async def work_test(input_data, OutputFormat):
    #     print(input_data)
    await intels.create_main_database()
    # 期间不断使用这个函数进行配合
    input_data = "我要一个生成记忆卡片的程序,只包括文本即可"
    result = await intels.intellect(input_data=input_data,
                     output_format="",
                     prompt_id="zxf_code_template_2")
    
    print(result)


async def test_work2():
    intels = AsyncIntel(database_url=os.getenv("adatabase_url"),model_name="doubao-1-5-pro-32k-250115")
    
    @intels.intellect_warp("zxf_code_template_2")
    async def work_test(input_data, OutputFormat):
        print(input_data)
    input_data = "我要一个生成记忆卡片的程序, 记忆卡片包括标题(title), 内容(content), 时间(time), 标签(tag)"
    
    print(await work_test(input_data = input_data,
                          OutputFormat = ""))