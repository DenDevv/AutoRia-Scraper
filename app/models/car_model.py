from sqlalchemy import Column, Integer, String, BigInteger

from config import config


dev_config = config.get("development")


class CarsModel(dev_config.Base):
    __tablename__ = "cars"
    id = Column(Integer(), primary_key=True)
    message_id = Column(BigInteger(), nullable=False)
    title = Column(String(), nullable=False)
    price = Column(BigInteger(), nullable=False)
    url = Column(String(), nullable=False)
