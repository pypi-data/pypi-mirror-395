

from pro_craft.code.file_manager import ContentManager, TextType
import pytest


# 内容池
class Test_ContentManager():

    @pytest.fixture
    def content_manager(self):
        return ContentManager()
    
    def test_save_content(self, content_manager):
        result =content_manager.save_content(
            name = "数据库--001",
            type = TextType.Tips,
            text = '''
```python
如何使用数据库同步数据
''',
        )
        print(result,'result')

    def test_save_content_auto(self, content_manager):
        result =content_manager.save_content_auto(
            text = '''

''')

        print(result,'result')

    def test_search(self, content_manager):
        result = content_manager.search(
            name = "装饰器-struct",
        )
        print("=="*20)
        print(result["content"])
        print("=="*20)

    def test_similarity(self,content_manager):
        result = content_manager.similarity(
            content = "每日资讯还是要具备的, 你要知道的内容和111",
            limit = 2
        )
        print(result[0].payload.get('content'),'result')
        print(type(result[0]),'result22')

