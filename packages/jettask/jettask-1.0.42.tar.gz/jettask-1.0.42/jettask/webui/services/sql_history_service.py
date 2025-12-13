"""
SQL 历史查询服务

提供 SQL WHERE 条件的历史记录管理、模糊搜索和使用统计功能
"""
from datetime import datetime, timezone
from typing import Optional, List, Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete, and_, or_, desc, func
from sqlalchemy.dialects.postgresql import insert

from jettask.db.models import SQLHistory
from jettask.utils.task_logger import get_task_logger

logger = get_task_logger(__name__)


class SQLHistoryService:
    """SQL 历史查询服务"""

    @classmethod
    async def search(
        cls,
        pg_session: AsyncSession,
        namespace: str,
        keyword: Optional[str] = None,
        category: Optional[str] = None,
        limit: int = 10
    ) -> List[Dict[str, Any]]:
        """
        模糊搜索 SQL 历史记录

        Args:
            pg_session: PostgreSQL 会话
            namespace: 命名空间
            keyword: 搜索关键词（模糊匹配 where_clause 和 alias）
            category: 类别过滤（system/user，为空则返回所有）
            limit: 返回数量限制

        Returns:
            匹配的 SQL 历史记录列表，按使用次数和创建时间降序排列
        """
        try:
            # 构建基础条件
            conditions = [SQLHistory.namespace == namespace]

            # 类别过滤
            if category:
                conditions.append(SQLHistory.category == category)

            # 关键词模糊搜索（使用 ILIKE 进行不区分大小写的模糊匹配）
            if keyword and keyword.strip():
                keyword_pattern = f"%{keyword.strip()}%"
                conditions.append(
                    or_(
                        SQLHistory.where_clause.ilike(keyword_pattern),
                        SQLHistory.alias.ilike(keyword_pattern)
                    )
                )

            # 构建查询
            stmt = select(SQLHistory).where(
                and_(*conditions)
            ).order_by(
                desc(SQLHistory.usage_count),
                desc(SQLHistory.created_at)
            ).limit(limit)

            result = await pg_session.execute(stmt)
            rows = result.scalars().all()

            return [row.to_dict() for row in rows]

        except Exception as e:
            logger.error(f"搜索 SQL 历史失败: {e}", exc_info=True)
            return []

    @classmethod
    async def save_or_update(
        cls,
        pg_session: AsyncSession,
        namespace: str,
        where_clause: str,
        alias: Optional[str] = None
    ) -> Optional[Dict[str, Any]]:
        """
        保存或更新 SQL 历史记录

        如果记录已存在，则更新使用次数和最后使用时间；
        如果不存在，则创建新记录。

        Args:
            pg_session: PostgreSQL 会话
            namespace: 命名空间
            where_clause: SQL WHERE 条件
            alias: 查询别名（可选）

        Returns:
            保存的记录信息
        """
        if not where_clause or not where_clause.strip():
            return None

        where_clause = where_clause.strip()

        try:
            # 使用 UPSERT：如果存在则更新使用次数，不存在则插入
            now = datetime.now(timezone.utc)

            stmt = insert(SQLHistory).values(
                namespace=namespace,
                where_clause=where_clause,
                alias=alias,
                category='user',
                usage_count=1,
                created_at=now,
                last_used_at=now
            )

            # 冲突时更新使用次数和最后使用时间
            stmt = stmt.on_conflict_do_update(
                index_elements=['namespace', 'where_clause'],
                set_={
                    'usage_count': SQLHistory.usage_count + 1,
                    'last_used_at': now,
                    # 如果提供了新别名且原来没有，则更新
                    'alias': func.coalesce(stmt.excluded.alias, SQLHistory.alias)
                }
            ).returning(SQLHistory)

            result = await pg_session.execute(stmt)
            row = result.scalar_one_or_none()
            await pg_session.commit()

            if row:
                logger.debug(f"SQL 历史记录已保存/更新: {where_clause[:50]}...")
                return row.to_dict()

            return None

        except Exception as e:
            logger.error(f"保存 SQL 历史失败: {e}", exc_info=True)
            await pg_session.rollback()
            return None

    @classmethod
    async def increment_usage(
        cls,
        pg_session: AsyncSession,
        history_id: int
    ) -> bool:
        """
        增加使用次数

        当用户从建议列表中选择一条记录时调用

        Args:
            pg_session: PostgreSQL 会话
            history_id: 历史记录 ID

        Returns:
            是否更新成功
        """
        try:
            stmt = update(SQLHistory).where(
                SQLHistory.id == history_id
            ).values(
                usage_count=SQLHistory.usage_count + 1,
                last_used_at=datetime.now(timezone.utc)
            )

            result = await pg_session.execute(stmt)
            await pg_session.commit()

            if result.rowcount > 0:
                logger.debug(f"SQL 历史记录使用次数已更新: id={history_id}")
                return True

            return False

        except Exception as e:
            logger.error(f"更新使用次数失败: {e}", exc_info=True)
            await pg_session.rollback()
            return False

    @classmethod
    async def delete_history(
        cls,
        pg_session: AsyncSession,
        history_id: int
    ) -> bool:
        """
        删除历史记录（仅用户历史可删除，系统内置不可删除）

        Args:
            pg_session: PostgreSQL 会话
            history_id: 历史记录 ID

        Returns:
            是否删除成功
        """
        try:
            # 只删除用户历史记录（category='user'），系统内置不可删除
            stmt = delete(SQLHistory).where(
                and_(
                    SQLHistory.id == history_id,
                    SQLHistory.category == 'user'
                )
            )

            result = await pg_session.execute(stmt)
            await pg_session.commit()

            if result.rowcount > 0:
                logger.info(f"SQL 历史记录已删除: id={history_id}")
                return True

            logger.warning(f"无法删除 SQL 历史记录（不存在或为系统内置）: id={history_id}")
            return False

        except Exception as e:
            logger.error(f"删除 SQL 历史失败: {e}", exc_info=True)
            await pg_session.rollback()
            return False

    @classmethod
    async def copy_system_templates(
        cls,
        pg_session: AsyncSession,
        target_namespace: str,
        template_namespace: str = 'default'
    ) -> int:
        """
        从模板命名空间复制系统内置查询到目标命名空间

        Args:
            pg_session: PostgreSQL 会话
            target_namespace: 目标命名空间
            template_namespace: 模板命名空间（默认为 'default'）

        Returns:
            复制的记录数
        """
        try:
            # 1. 查询模板命名空间的系统内置记录
            stmt = select(SQLHistory).where(
                and_(
                    SQLHistory.namespace == template_namespace,
                    SQLHistory.category == 'system'
                )
            )
            result = await pg_session.execute(stmt)
            templates = result.scalars().all()

            if not templates:
                logger.warning(f"模板命名空间 '{template_namespace}' 中没有系统内置查询")
                return 0

            # 2. 批量插入到目标命名空间（使用 UPSERT 避免冲突）
            now = datetime.now(timezone.utc)
            copied_count = 0

            for template in templates:
                stmt = insert(SQLHistory).values(
                    namespace=target_namespace,
                    where_clause=template.where_clause,
                    alias=template.alias,
                    category='system',
                    usage_count=0,
                    created_at=now,
                    last_used_at=now
                )

                # 如果已存在则跳过（不更新）
                stmt = stmt.on_conflict_do_nothing(
                    index_elements=['namespace', 'where_clause']
                )

                result = await pg_session.execute(stmt)
                if result.rowcount > 0:
                    copied_count += 1

            await pg_session.commit()

            logger.info(
                f"从命名空间 '{template_namespace}' 复制了 {copied_count} 条系统内置查询到 '{target_namespace}'"
            )

            return copied_count

        except Exception as e:
            logger.error(f"复制系统内置查询失败: {e}", exc_info=True)
            await pg_session.rollback()
            return 0

    @classmethod
    async def cleanup_old_records(
        cls,
        pg_session: AsyncSession,
        namespace: str,
        days: int = 90,
        max_records: int = 1000
    ) -> int:
        """
        清理旧的用户历史记录

        删除超过指定天数未使用的记录，或者当记录数超过限制时删除使用次数最少的

        Args:
            pg_session: PostgreSQL 会话
            namespace: 命名空间
            days: 保留天数
            max_records: 最大记录数

        Returns:
            删除的记录数
        """
        try:
            deleted_count = 0

            # 1. 删除长期未使用的记录
            cutoff_date = datetime.now(timezone.utc) - timezone.timedelta(days=days)
            stmt = delete(SQLHistory).where(
                and_(
                    SQLHistory.namespace == namespace,
                    SQLHistory.category == 'user',
                    SQLHistory.last_used_at < cutoff_date
                )
            )
            result = await pg_session.execute(stmt)
            deleted_count += result.rowcount

            # 2. 如果记录数仍超过限制，删除使用次数最少的
            count_stmt = select(func.count(SQLHistory.id)).where(
                and_(
                    SQLHistory.namespace == namespace,
                    SQLHistory.category == 'user'
                )
            )
            count_result = await pg_session.execute(count_stmt)
            total_count = count_result.scalar() or 0

            if total_count > max_records:
                # 获取要保留的记录 ID
                keep_stmt = select(SQLHistory.id).where(
                    and_(
                        SQLHistory.namespace == namespace,
                        SQLHistory.category == 'user'
                    )
                ).order_by(
                    desc(SQLHistory.usage_count),
                    desc(SQLHistory.last_used_at)
                ).limit(max_records)

                keep_result = await pg_session.execute(keep_stmt)
                keep_ids = [row[0] for row in keep_result.fetchall()]

                # 删除不在保留列表中的记录
                if keep_ids:
                    delete_stmt = delete(SQLHistory).where(
                        and_(
                            SQLHistory.namespace == namespace,
                            SQLHistory.category == 'user',
                            ~SQLHistory.id.in_(keep_ids)
                        )
                    )
                    result = await pg_session.execute(delete_stmt)
                    deleted_count += result.rowcount

            await pg_session.commit()

            if deleted_count > 0:
                logger.info(f"清理了 {deleted_count} 条旧的 SQL 历史记录")

            return deleted_count

        except Exception as e:
            logger.error(f"清理 SQL 历史失败: {e}", exc_info=True)
            await pg_session.rollback()
            return 0
