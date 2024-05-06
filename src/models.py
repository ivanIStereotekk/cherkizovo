from sqlalchemy import Integer,String, Date, Float
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
import datetime



class Base(DeclarativeBase):
    pass


class Item(Base):
    __tablename__= "item"
    id: Mapped[int] = mapped_column(Integer,primary_key=True)
    dt: Mapped[datetime.date] = mapped_column(Date)
    article: Mapped[int] = mapped_column(Integer)
    kg: Mapped[int] = mapped_column(Integer)
    def __repr__(self) -> str:
        return f"item:  {self.dt} - {self.article} - {self.kg}"
