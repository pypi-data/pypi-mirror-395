"""
SQLHistory 模型

存储用户的 SQL WHERE 查询历史记录，支持模糊搜索和自动补全
"""
from sqlalchemy import Column, String, Integer, Text, TIMESTAMP, Index
from datetime import datetime, timezone
from typing import Optional, Dict, Any

from ..base import Base


class SQLHistory(Base):
    """
    SQL 查询历史表

    存储用户输入的 WHERE 条件，支持模糊搜索、使用统计和分类管理
    """
    __tablename__ = 'sql_history'

    # 主键
    id = Column(Integer, primary_key=True, autoincrement=True, comment='主键ID')

    # 命名空间（多租户支持）
    namespace = Column(String(100), nullable=False, comment='命名空间')

    # SQL WHERE 条件内容
    where_clause = Column(Text, nullable=False, comment='SQL WHERE 条件（不含 WHERE 关键字）')

    # 别名（可选，用户自定义的查询名称）
    alias = Column(String(200), nullable=True, comment='查询别名（可选）')

    # 类别：system（系统内置，不可删除）或 user（用户历史，可删除）
    category = Column(
        String(20),
        nullable=False,
        default='user',
        comment='类别: system（系统内置，不可删除）/ user（用户历史，可删除）'
    )

    # 使用次数（用于排序）
    usage_count = Column(Integer, nullable=False, default=1, comment='使用次数')

    # 创建时间
    created_at = Column(
        TIMESTAMP(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
        comment='创建时间'
    )

    # 最后使用时间
    last_used_at = Column(
        TIMESTAMP(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
        comment='最后使用时间'
    )

    # 索引设计：
    # 1. 使用 PostgreSQL 的 GIN 索引配合 pg_trgm 扩展实现高效模糊搜索
    # 2. 复合索引用于排序和过滤
    __table_args__ = (
        # 命名空间 + 类别索引（用于过滤）
        Index('idx_sql_history_namespace_category', 'namespace', 'category'),
        # 命名空间 + 使用次数 + 创建时间索引（用于排序）
        Index('idx_sql_history_namespace_usage_created', 'namespace', 'usage_count', 'created_at'),
        # WHERE 条件的 GIN 索引（需要在 DDL 中使用 pg_trgm 扩展）
        # 这里只定义普通索引，GIN 索引在 DDL 中创建
        Index('idx_sql_history_where_clause', 'where_clause'),
        # 别名索引（用于模糊搜索）
        Index('idx_sql_history_alias', 'alias'),
        # 唯一约束：同一命名空间下的 WHERE 条件不重复
        Index('idx_sql_history_namespace_where_unique', 'namespace', 'where_clause', unique=True),
    )

    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            'id': self.id,
            'namespace': self.namespace,
            'where_clause': self.where_clause,
            'alias': self.alias,
            'category': self.category,
            'usage_count': self.usage_count,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'last_used_at': self.last_used_at.isoformat() if self.last_used_at else None,
        }

    def __repr__(self) -> str:
        return f"<SQLHistory(id={self.id}, category='{self.category}', usage_count={self.usage_count})>"
