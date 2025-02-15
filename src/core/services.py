from math import ceil

from sqlalchemy.ext.asyncio import AsyncSession

from src.core.exceptions import PageNotFoundException


class CustomService:
    def __init__(self, session: AsyncSession):
        self.session = session

    @staticmethod
    async def _paginate(page: int, limit: int, total_items: int):
        if limit <= 0:
            raise ValueError("Limit должен быть больше 0 для пагинации.")

        total_pages = ceil(total_items / limit) if total_items > 0 else 0
        current_page = page if total_items > 0 else 0

        if current_page > total_pages:
            raise PageNotFoundException

        prev_page = None if current_page <= 1 else f"?page={current_page}&limit={limit}"
        next_page = (
            None
            if current_page >= total_pages
            else f"?page={current_page + 2}&limit={limit}"
        )

        return {
            "total_items": total_items,
            "total_pages": total_pages,
            "current_page": current_page,
            "prev_page": prev_page,
            "next_page": next_page,
        }
