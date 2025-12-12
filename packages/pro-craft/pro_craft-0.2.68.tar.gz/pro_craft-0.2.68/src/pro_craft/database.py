
from sqlalchemy import Column, Integer, String, Text, DateTime, text, UniqueConstraint, Boolean, func, Float, Double
from sqlalchemy.orm import declarative_base

from datetime import datetime, timedelta
from pro_craft_infer.database import UseCase, Prompt,PromptBase

class SyncMetadata(PromptBase):
    """用于存储同步元数据的表模型"""
    __tablename__ = "ai_sync_metadata"
    id = Column(Integer, primary_key=True, autoincrement=True)
    last_sync_time = Column(DateTime, default=datetime(1970, 1, 1))
    table_name = Column(String(255), unique=True)

    def __repr__(self):
        return f"<SyncMetadata(table_name='{self.table_name}', last_sync_time='{self.last_sync_time}')>"




FileBase = declarative_base()

class Content(FileBase):
    __tablename__ = 'content' # 数据库中的表名，你可以改成你希望的名字

    # id (int, primary_key=True, autoincrement=True)
    # 你的属性表中 id 为 int, true (not null), true (primary key), 0 (length), ASC (key order), true (auto increment)
    id = Column(
        Integer,
        primary_key=True,
        autoincrement=True, # 自动递增
        nullable=False,     # 不能为空
        comment="自增"
    )

    # prompt_id (varchar 255, not null, unique)
    # 你的属性表中 prompt_id 为 varchar, 255 (length), true (not null)
    embed_name_id = Column(
        String(255),        # VARCHAR 类型，长度 255
        nullable=False,     # 不能为空    # 必须是唯一的，这会创建唯一索引
        comment="Unique identifier for the prompt"
    )

    # version (varchar 50, not null)
    # 你的属性表中 version 为 varchar, 50 (length), true (not null)
    name = Column(
        String(255),         # VARCHAR 类型，长度 50
        nullable=False,     # 不能为空
        comment="Version of the prompt"
    )

    # version (varchar 50, not null)
    # 你的属性表中 version 为 varchar, 50 (length), true (not null)
    version = Column(
        String(50),         # VARCHAR 类型，长度 50
        nullable=False,     # 不能为空
        comment="版本"
    )
    timestamp = Column(
        DateTime,
        nullable=False,      # 不能为空
        server_default=text('CURRENT_TIMESTAMP'),
        onupdate=text('CURRENT_TIMESTAMP'),
        comment="时间戳"
    )
    content = Column(
        Text,               # TEXT 类型，适用于长文本
        nullable=False,     # 不能为空
        comment="内容"
    )
    type = Column(
        Integer,
        nullable=True,      # 可以为空 (因为你的表格中 Not Null 为 false)
        comment="类型"      # 列注释
    )

    # 定义 __repr__ 方法以便打印对象时有清晰的表示
    def __repr__(self):
        return (f"<Prompt(id={self.id}, prompt_id='{self.prompt_id}', "
                f"version='{self.version}', timestamp='{self.timestamp}', "
                f"prompt='{self.prompt[:50]}...', use_case='{self.use_case}')>")

