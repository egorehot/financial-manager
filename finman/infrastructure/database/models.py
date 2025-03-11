from sqlalchemy import ForeignKey, MetaData, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    __abstract__ = True
    metadata = MetaData()

    id: Mapped[int] = mapped_column(primary_key=True)
    created_at: Mapped[int] = mapped_column(server_default=func.now())
    updated_at: Mapped[int] = mapped_column(server_default=func.now())

    def __repr__(self) -> str:
        res = f"<{self.__class__.__name__}: "
        for col_name, _ in self.__mapper__.columns.items():  # noqa: PERF102
            val = getattr(self, col_name)
            res += f"{col_name}={val!r} "
        return res[:-1] + ">"


class Transaction(Base):
    __tablename__ = "transactions"

    date: Mapped[int]
    type: Mapped[int]
    amount: Mapped[float]
    currency: Mapped[str]
    transactor_id: Mapped[int] = mapped_column(ForeignKey("transactors.id"))
    category_id: Mapped[int] = mapped_column(ForeignKey("categories.id"))
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
