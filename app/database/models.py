from datetime import datetime

from sqlalchemy import Column, Integer, String, Text, Float, DateTime, JSON

from app.database.base import Base, TimestampMixin


class Lead(Base):
    __tablename__ = "bot_leads"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    phone = Column(String, nullable=False)
    email = Column(String)
    company = Column(String)
    service_type = Column(String)  # Тип выбранной услуги
    calculated_price = Column(Float)  # Рассчитанная цена
    source = Column(String, default="telegram")
    created_at = Column(DateTime, default=datetime.now())


class UserEvent(Base):
    __tablename__ = "bot_user_events"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer)
    event_type = Column(String, index=True)
    event_data = Column(JSON)
    created_at = Column(DateTime, default=datetime.now())


class Calculation(Base):
    __tablename__ = "bot_calculations"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer)
    service_type = Column(String)
    parameters = Column(JSON)
    result = Column(Text)
    price = Column(Float)
    created_at = Column(DateTime, default=datetime.now())