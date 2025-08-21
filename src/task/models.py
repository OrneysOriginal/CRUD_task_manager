from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Enum
import enum

from src.database import Base


class StatusEnum(str, enum.Enum):
    created = "created"
    in_work = "in_work"
    finished = "finished"


class Task(Base):
    __tablename__ = "task"

    uuid: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True)
    description: Mapped[str]
    status: Mapped[str] = mapped_column(Enum(StatusEnum))
