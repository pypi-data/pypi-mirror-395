

from pro_craft.utils import create_session
from qdrant_client import QdrantClient, models
from uuid import uuid4
from qdrant_client import QdrantClient
from qdrant_client.models import Filter, FieldCondition, MatchValue, PointStruct, CollectionStatus, Distance, VectorParams

from .utils.template_extract import extract_template
from .utils.vectorstore import VolcanoEmbedding
import os
from typing import List, Dict, Any,Optional
import re

from sqlalchemy import Column, Integer, String, Text, DateTime, text, UniqueConstraint, Boolean, func, Float, Double
from sqlalchemy.orm import declarative_base
from sqlalchemy import create_engine

Base = declarative_base()

class CodeTemplate(Base):
    __tablename__ = 'code_template'
    template_id = Column(String(255), primary_key=True, nullable=False, comment="自增")
    description = Column(Text, nullable=False, comment="Detailed description of the template")
    template_code = Column(Text, nullable=False, comment="The actual code of the template")
    version = Column(Integer, nullable=True, comment="Template version")
    # UniqueConstraint('template_name', name='uq_template_name') # 如果 template_name 应该是唯一的


class CoderTemplateManager():
    def __init__(self,
                 database_url = "",
                 q_collection = "",
                 q_host = "127.0.0.1",
                 q_port = 6333,
                 embed_model_name = "",
                 embed_api_key = "",
                 logger = None,
                ):
        database_url = database_url or os.getenv("database_url")
        assert database_url

        # database_url = "mysql+pymysql://" + database_url
        database_url = "postgresql://" + database_url

        self.engine = create_engine(database_url, 
                                    echo=False, # echo=True 仍然会打印所有执行的 SQL 语句
                                    pool_size=10,        # 连接池中保持的连接数
                                    max_overflow=20,     # 当pool_size不够时，允许临时创建的额外连接数
                                    pool_recycle=3600,   # 每小时回收一次连接
                                    pool_pre_ping=True,  # 使用前检查连接活性
                                    pool_timeout=30      # 等待连接池中连接的最长时间（秒）
                                    ) 

        Base.metadata.create_all(self.engine)

        self.QDRANT_COLLECTION_NAME = q_collection
        self.embedding_model = VolcanoEmbedding(
            model_name = embed_model_name,
            api_key = embed_api_key,
        )
        self.connection = QdrantClient(host=q_host, port=q_port)

        collections = self.connection.get_collections().collections
        existing_collection_names = {c.name for c in collections}
        if self.QDRANT_COLLECTION_NAME not in existing_collection_names:
            self.connection.create_collection(
                collection_name=self.QDRANT_COLLECTION_NAME,
                vectors_config=models.VectorParams(size=2560, distance=models.Distance.COSINE),
            )
        self.logger = logger
    
    def get_embedding(self,text: str) -> List[float]:
        return self.embedding_model._get_text_embedding(text)
    
    def add_template(self,
                     use_case: str,
                     template_id: str,
                     description: str,):   
        template = extract_template(use_case)
        embedding_vector = self.get_embedding(description)
        points = [
                models.PointStruct(
                    id = str(uuid4()),
                    vector=embedding_vector,
                    payload={
                        "template_id": template_id,
                        "description": description,
                        "use_case": use_case,
                        "template": template,
                    }
                )
            ]
        self.connection.upsert(
            collection_name=self.QDRANT_COLLECTION_NAME,
            wait=True,
            points=points
        )
        # 数据库
        with create_session(self.engine) as session:
            new_template = CodeTemplate(
                template_id=template_id,
                version=1,
                description=description,
                template_code=template,
            )
            session.add(new_template)
            session.commit()
            session.refresh(new_template)
            
        return "success"


    def delete_template(self, template_id: str) -> bool:
        """
        逻辑删除指定的代码模板。
        """


        # 3. 使用属性删除点
        # 目标：删除所有 'color' 属性为 'red' 的点

        # 定义一个过滤器
        # 这个过滤器会匹配所有 payload 中 'color' 字段值为 'red' 的点
        _filter = Filter(
            must=[
                FieldCondition(
                    key="template_id",
                    match=MatchValue(value=template_id)
                )
            ]
        )
        self.connection.delete(
            collection_name=self.QDRANT_COLLECTION_NAME,
            points_selector=_filter,
            wait=True
        )


        with create_session(self.engine) as session:
            template = session.query(CodeTemplate).filter_by(template_id=template_id).first()
            if template:
                session.delete(template)
                session.commit()
                return True
        return False
    
        
    def search(self, text , limit , query_filter=None):
        query_vector = self.get_embedding(text)
        results = self.connection.search(
            collection_name=self.QDRANT_COLLECTION_NAME,
            query_vector=query_vector,
            limit=limit,
            query_filter=query_filter
        )
        return results

    def get_template_obj(self, template_id: str):
        # 模拟从数据库获取模板详情
        # 实际使用时，你需要根据你的数据库 setup 来实现
        with create_session(self.engine) as session:
            template = session.query(CodeTemplate).filter_by(template_id = template_id).first()
        return template
    

from modusched.core import BianXieAdapter
from pro_craft.utils import extract_




llm2 = """
你是一个专业的Python代码修改和生成AI。你的任务是根据用户提供的代码模板文件和详细的修改指令文件，精确地对模板进行补充、完善和修改。

**你的目标是：**
1.  **严格遵循指令文件中的所有要求，尤其是针对特定 `BLOCK` 和 `PLACEHOLDER` 的指令和约束/示例。**
2.  **尽可能应用指令文件中提供的命名约定。**
3.  **仅修改指令明确要求修改的部分，模板中未被指令覆盖的固定部分必须保持不变。**
4.  **最终输出完整且可运行的Python代码。**

**输入格式:**
用户将以以下两个部分向你提供信息：

--- TEMPLATE_CODE_START ---
[原始的代码模板内容，其中包含 BLOCK_START/END 和 PLACEHOLDER/END_PLACEHOLDER 标记]
--- TEMPLATE_CODE_END ---

--- REQUEST_FILE_START ---
[一个结构化的指令文件，格式为 REQUEST_START/END，包含目标、命名约定和具体修改点]
--- REQUEST_FILE_END ---

**你的工作流程和生成原则:**

1.  **解析指令文件：**
    *   首先解析 `REQUEST_FILE_START` 中的所有内容，理解其 `目标`、`命名约定` 和 `具体修改点`。
    *   将 `具体修改点` 中的每个 `BLOCK` 和 `PLACEHOLDER` 指令及其 `约束/示例` 映射到模板代码中的对应位置。
2.  **处理模板代码：**
    *   逐行读取 `TEMPLATE_CODE_START` 中的模板代码。
    *   当遇到 `BLOCK_START` 或 `PLACEHOLDER` 标记时：
        *   查找指令文件中对应 `块名称` 的修改指令。
        *   **如果存在指令：**
            *   删除 `BLOCK_START` 和 `BLOCK_END` (或 `PLACEHOLDER` 和 `END_PLACEHOLDER`) 及其内部的原始内容（包括 `AI:` 注释）。
            *   用指令中提供的代码**替换**该区域。
            *   在替换的代码块的开始和结束位置，添加特殊的标记 `// AI_MODIFIED_START` 和 `// AI_MODIFIED_END` (如果只是新增内容，可以使用 `// AI_ADDED_START` 和 `// AI_ADDED_END`)。
            *   如果指令是要求删除某些内容，请用 `// AI_DELETED_LINE: [原始行内容]` 标记被删除的行。
        *   **如果不存在指令：**
            *   保留该 `BLOCK` 或 `PLACEHOLDER` 及其内部的原始内容（包括 `AI:` 注释和标记本身），不做任何改动。这允许模板中的可选部分在没有明确指令时保持原样。
    *   当遇到非标记的普通代码行时，保持其不变。
3.  **应用命名约定：**
    *   在生成或修改代码时，优先应用 `REQUEST_FILE_START` 中提供的 `命名约定`。
    *   **重要：** 命名约定只应影响由你**生成或修改**的代码部分（即 `AI_ADDED` 或 `AI_MODIFIED` 区域）。你不能随意修改模板中未被明确指令触及的固定代码部分的命名。
4.  **生成中间输出：**
    *   首先生成包含所有 `// AI_ADDED/MODIFIED/DELETED` 标记的完整代码。这有助于后续的自动化工具进行变更追踪和人工核查。
5.  **生成最终输出：**
    *   在生成中间输出后，进一步处理该代码，**移除所有 `// AI_ADDED/MODIFIED/DELETED` 类型的标记**。
    *   移除所有模板中遗留的 `BLOCK_START/END` 和 `PLACEHOLDER/END_PLACEHOLDER` 标记。
    *   保留所有的 Docstrings 和常规的代码注释。

**你的输出必须是最终的、清理后的完整 Python 代码文件内容。**

"""


from agno.tools.toolkit import Toolkit

class GenerateCodeByTemplate(Toolkit):
    def __init__(self, *args, 
                 database_url = '',
                 q_collection = "",
                 q_host = "",
                 q_port = 6333 ,
                 embed_model_name = "",
                 embed_api_key = "",
                 **kwargs):
        super().__init__(
            name="GenerateCodeByTemplate", tools=[self.get_template_name_by_demand, 
                                                  self.get_template_by_name, 
                                                  self.generate_request, 
                                                  self.generate_code_by_request], *args, **kwargs
        )

        self.coder = CoderTemplateManager(
                database_url = database_url,
                q_collection = q_collection,
                q_host = q_host,
                q_port = q_port,
                embed_model_name = embed_model_name,
                embed_api_key = embed_api_key,
                logger = None,
        )

    
    def get_template_name_by_demand(self,demand: str, top_k = 5) -> list:
        """Obtain a appropriate template name based on the requirements to write some code.
        
        Args:
            demand (str): The user's demands or requests
            top_k (int): Number of search results default: 5
        
        """

        query = demand
        print("search_template_by_text")
        print(f"input & {type(query)} & query: {query} top:k {top_k} ")
        search_result = self.coder.search(
            text=query,
            limit=top_k,
            # query_filter=None # 可以在这里添加额外的过滤条件，例如根据语言、框架过滤
        )

        templates_summary = []
        for hit in search_result:
            # 在实际 Qdrant 中，hit.id 是模板的ID，hit.payload 包含其他元数据
            # 假设你的 Qdrant payload 中存储了 template_name 和 description
            templates_summary.append({
                'template_id': hit.payload.get("template_id"),
                'description': hit.payload.get('description', 'No description provided.'),
                'match_score': hit.score
            })
        print(f"output & {type(templates_summary)} & {templates_summary} ")
        return templates_summary


    def get_template_by_name(self,template_name: str) -> dict | None:
        """Get template by template name from 'get_template_name_by_demand'

        Args:
            template_name (str): A template name
        """
        template_id = template_name # template_id 根据你的模型是 Integer

        print("get_template_details")
        print(f"input & {type(template_id)} & query: {template_id} ")
        template = self.coder.get_template_obj(template_id = template_id)
        if template:
            return {
                'template_id': template.template_id,
                'description': template.description,
                'template_code': template.template_code,
                'version': template.version,
            }
        print(f"output & {type(template)} & {template} ")
        return None
    
    def generate_request(self,template: str,user_request_details: Dict[str, Any]) -> str:
        """Based on the template and the user's requirements, generate a code generation instruction to guide the final code generation process.
        
        Args:
            template (str): template full text
            user_request_details (dict): Some specific details of the user's demands can be obtained by repeatedly asking questions.

            user_request_details = {
                "overall_goal": "用户诉求",
            }

        """

        def generate_request_file(template_code: str, user_request_details: Dict[str, Any], naming_conventions: Optional[Dict[str, Any]] = None) -> str:
            """
            根据选定的模板代码、解析后的用户需求（结构化形式）和模板的命名约定，生成符合 `REQUEST_START/END` 格式的指令文件。
            `user_request_details` 应该是一个字典，键是 BLOCK/PLACEHOLDER 的名称，值是包含 '指令' 和 '约束/示例' 的字典。
            """
            print("generate_request_file")
            print(f"input & {type(template_code)} & template_code: {template_code} user_request_details: {user_request_details} naming_conventions: {naming_conventions}")

            request_parts = []

            request_parts.append("--- REQUEST_START ---")
            request_parts.append("template.py # 目标文件通常是这个，可以根据实际情况调整") # 假设一个通用文件名

            # 添加整体目标描述
            overall_goal = user_request_details.get("overall_goal", "完善代码模板以满足以下需求。")
            request_parts.append(f"\n**目标：** {overall_goal}\n")

            # 添加命名约定 (如果提供了)
            if naming_conventions:
                request_parts.append("**命名约定:**")
                for key, value in naming_conventions.items():
                    request_parts.append(f"*   **{key}:** {value}")
                request_parts.append("") # 空行

            request_parts.append("**具体修改点：**\n")

            # 遍历模板代码，找到所有的 BLOCK 和 PLACEHOLDER
            # 然后根据 user_request_details 填充指令
            # 这是一个简化版本，实际可能需要更复杂的解析器来处理嵌套块或动态生成的块
            # 对于 MVP，我们可以假设 user_request_details 中包含了所有需要填充的块/占位符
            block_pattern = r"(BLOCK_START|PLACEHOLDER):\s*(\w+)"
            for match in re.finditer(block_pattern, template_code):
                block_type = match.group(1)
                block_name = match.group(2)

                if block_name in user_request_details:
                    details = user_request_details[block_name]
                    instruction = details.get("指令", "")
                    constraint_example = details.get("约束/示例", "")

                    request_parts.append(f"*   **{block_type}: {block_name}**")
                    request_parts.append(f"    *   **指令：** {instruction}")
                    if constraint_example:
                        # 确保多行约束/示例能正确缩进
                        formatted_ce = "\n".join([f"    *   **约束/示例：** {line}" if i == 0 else f"    *   {line}" for i, line in enumerate(str(constraint_example).splitlines())])
                        request_parts.append(formatted_ce)
                    request_parts.append("") # 空行

            request_parts.append("--- REQUEST_END ---")
            print(f"output & {type(request_parts)} & request_parts: {request_parts} ")

            result = "\n".join(request_parts)
            return result
        return generate_request_file(template_code=template, user_request_details=user_request_details)

    def generate_code_by_request(self,template: str,request: str) -> str:
        """Generate the final code based on the requirements.

        Args:
            template (str): Template
            request (str): Code generation instruction

        """
        bx = BianXieAdapter()
        result = bx.product(system_prompt = llm2 ,prompt = template + request)
        python_code = extract_(result,r"python")
        print(python_code,'最终结果')
        return python_code

