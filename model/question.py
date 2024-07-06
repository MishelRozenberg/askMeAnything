from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import Mapped


class Base(DeclarativeBase):
    pass
class Question(Base):
    __tablename__ = "questions"

    id: Mapped[int] = mapped_column("id", primary_key=True, autoincrement=True)
    question_data: Mapped[str] = mapped_column("question_data", nullable=False)
    answer_data: Mapped[str] = mapped_column("answer_data", nullable=False)
