from contextlib import contextmanager
from logging import getLogger
from pathlib import Path
from typing import Generator

from sqlalchemy.engine.base import Engine
from sqlalchemy.engine.create import create_engine
from sqlalchemy.event.api import listens_for
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

from phystool.config import config


logger = getLogger(__name__)


@listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, _):
    # the sqlite3 driver will not set PRAGMA foreign_keys
    # if autocommit=False; set to True temporarily
    ac = dbapi_connection.autocommit
    dbapi_connection.autocommit = True

    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()

    # restore previous autocommit setting
    dbapi_connection.autocommit = ac


class _PhysQL:
    def __init__(self) -> None:
        self._engine: Engine | None = None
        self._session_maker: sessionmaker[Session] | None = None

    @property
    def _path(self) -> Path:
        return config.db.DB_DIR / ".physql.sqlite"

    @contextmanager
    def __call__(self) -> Generator[Session, None, None]:
        session = self._get_session()
        try:
            yield session
            session.commit()
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()

    def _get_session(self) -> Session:
        if self._session_maker:
            return self._session_maker()

        self._engine = create_engine(
            f"sqlite:///{self._path}",
            connect_args={"autocommit": False},
            echo=False,
        )
        self._session_maker = sessionmaker(self._engine)
        logger.debug(f"SQLite connection to {self._path} successful")
        return self._get_session()

    def reset(self) -> None:
        self._path.unlink(missing_ok=True)

        if self._engine:
            self._engine.dispose()

        self._session_maker = None
        if self._get_session() is None:
            raise ValueError("The database connection to the database failed")

        if self._engine is None:
            raise ValueError("The database engine is not configured")
        BaseModel.metadata.create_all(self._engine)


class BaseModel(DeclarativeBase):
    pass


physql_db = _PhysQL()
