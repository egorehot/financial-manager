from sqlalchemy import ForeignKey, MetaData, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    __abstract__ = True
    metadata = MetaData()

    id: Mapped[int] = mapped_column(primary_key=True)
    created_at: Mapped[int] = mapped_column(server_default=func.now())
    updated_at: Mapped[int] = mapped_column(server_default=func.now())

    def __repr__(self) -> str:  # TODO add all column attrs
        return (f"<{self.__class__.__name__}: id={self.id}, "
                f"created_at={self.created_at}, updated_at={self.updated_at}>")


class Transaction(Base):
    __tablename__ = "transactions"

    date: Mapped[int]
    type: Mapped[str]
    amount: Mapped[float]
    currency: Mapped[str]
    transactor_id: Mapped[int] = mapped_column(ForeignKey("transactors.id"))
    description: Mapped[str | None]

    transactor: Mapped["Transactor"] = relationship(lazy="joined")
    category: Mapped["Category"] = relationship(lazy="joined")


class Transactor(Base):
    __tablename__ = "transactors"

    name: Mapped[str] = mapped_column(unique=True)


class Category(Base):
    __tablename__ = "categories"

    name: Mapped[str] = mapped_column(unique=True)
    parent_id: Mapped[int | None] = mapped_column(ForeignKey("categories.id"))

    parent: Mapped["Category"] = relationship(
        "Category",
        remote_side="Category.id",
    )
