from psycopg_pool import ConnectionPool
from langgraph.checkpoint.postgres import PostgresSaver as BasePostgresSaver
from config.settings import settings

# Initialize PostgreSQL connection pool
pool = ConnectionPool(conninfo=settings.DATABASE_URI)


class CustomPostgresSaver(BasePostgresSaver):
    def put(self, config, checkpoint, metadata, new_versions=None):
        """
        Override the default put method to ensure new_versions is always defined.
        """
        if new_versions is None:
            new_versions = {}
        return super().put(config, checkpoint, metadata, new_versions)


def get_checkpointer() -> CustomPostgresSaver:
    """
    Returns a CustomPostgresSaver instance for LangGraph checkpointing.
    """
    return CustomPostgresSaver(pool)


def get_connection():
    """
    Returns a raw connection from the PostgreSQL connection pool.
    """
    return pool.connection()
