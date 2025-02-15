from src.infrastructure.websocket.manager import ConnectionManager

manager = ConnectionManager()


async def get_manager() -> ConnectionManager:
    return manager
