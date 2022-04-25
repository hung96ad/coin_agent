# coding: utf-8
from sqlalchemy import CHAR, Column, DECIMAL, Float, Index, String, text, Text
from sqlalchemy.dialects.mysql import BIGINT, INTEGER, SMALLINT, TINYINT
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy import create_engine

SQLALCHEMY_DATABASE_URI = 'mysql://root@localhost:3306/coin'
engine = create_engine(SQLALCHEMY_DATABASE_URI, pool_pre_ping=True, echo=False)
db = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))
Base = declarative_base(bind=engine)


class CoinInfo(Base):
    __tablename__ = 'coin_info'

    id = Column(SMALLINT(6), primary_key=True)
    symbol = Column(CHAR(20), unique=True)
    minQty = Column(DECIMAL(15, 10))
    tickSize = Column(DECIMAL(15, 10))
    status = Column(CHAR(20))
    baseAsset = Column(CHAR(10))
    quoteAsset = Column(CHAR(10))
    Volume = Column(INTEGER(11), server_default=text("0"))
    initial_money = Column(Float(asdecimal=True), server_default=text("0"))
    prediction = Column(Float(asdecimal=True))
    isPrediction = Column(INTEGER(11))
    predictions = Column(Text)
    suggestionType = Column(INTEGER(11))
    suggestionPrice = Column(Float(asdecimal=True))
    suggestionDate = Column(BIGINT(20))
    image = Column(String(255))
    rank = Column(INTEGER(11))
    totalGain = Column(Float(asdecimal=True))


class Kline(Base):
    __tablename__ = 'klines'
    __table_args__ = (
        Index('index', 'id_symbol', 'Close_time', unique=True),
    )

    id = Column(BIGINT(20), primary_key=True)
    id_symbol = Column(INTEGER(11))
    Close_time = Column(BIGINT(20))
    Open = Column(Float(asdecimal=True))
    High = Column(Float(asdecimal=True))
    Low = Column(Float(asdecimal=True))
    Close = Column(Float(asdecimal=True))
    Volume = Column(Float(asdecimal=True))


class Trade(Base):
    __tablename__ = 'trade'
    __table_args__ = (
        Index('index', 'id_symbol', 'close_time', unique=True),
    )

    id = Column(INTEGER(11), primary_key=True)
    id_symbol = Column(INTEGER(11))
    close_time = Column(BIGINT(20))
    status = Column(TINYINT(4), comment='1 buy -1 sell')
    gain = Column(Float(asdecimal=True))
    price = Column(Float(asdecimal=True))
    id_kline = Column(INTEGER(11))
    investment = Column(Float(asdecimal=True))
