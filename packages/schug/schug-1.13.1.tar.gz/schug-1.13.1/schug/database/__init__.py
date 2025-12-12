from sqlmodel import SQLModel, create_engine

from schug.config import DEMO_DB, settings

DEMO_CONNECT_ARGS: dict = {"check_same_thread": False}

if settings.db_uri == DEMO_DB:
    engine = create_engine(settings.db_uri, connect_args=DEMO_CONNECT_ARGS, echo=True)
else:
    engine = create_engine(settings.db_uri, echo=True)

SQLModel.metadata.create_all(engine)
