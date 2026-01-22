from app.db.models import Base
from app.db.session import get_engine


def init_db(db_url: str | None = None) -> None:
    engine = get_engine(db_url)
    Base.metadata.create_all(bind=engine)
