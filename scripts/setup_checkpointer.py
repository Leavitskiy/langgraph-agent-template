"""
Setup script to initialize LangGraph checkpointing tables in PostgreSQL.
Run this script once before using the workflow.
"""

from langgraph.checkpoint.postgres import PostgresSaver
from config.settings import settings


def main():
    db_uri = settings.DATABASE_URI

    with PostgresSaver.from_conn_string(db_uri) as checkpointer:
        checkpointer.setup()
        print("Checkpointer setup completed. Required tables have been created.")


if __name__ == "__main__":
    main()
