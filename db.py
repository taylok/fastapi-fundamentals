from sqlmodel import create_engine, Session

engine = create_engine(
    "sqlite:///carsharing.db",  # connection string
    connect_args={"check_same_thread": False},  # Needed for SQLite
    echo=True  # Log generator (not in Prod)
)


def get_session():
    with Session(engine) as session:
        yield session
