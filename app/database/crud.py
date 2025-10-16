from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, insert
from datetime import datetime
from typing import Optional

from app.database.models import Lead, UserEvent, Calculation


async def create_user_event(
        db: AsyncSession,
        user_id: int,
        event_type: str,
        event_data: dict
) -> UserEvent:
    """Создание события пользователя"""
    event = UserEvent(
        user_id=user_id,
        event_type=event_type,
        event_data=event_data,
        created_at=datetime.now()
    )

    db.add(event)
    await db.commit()
    await db.refresh(event)
    return event


async def create_lead(
        db: AsyncSession,
        name: str,
        phone: str,
        email: Optional[str] = None,
        company: Optional[str] = None,
        service_type: Optional[str] = None,
        calculated_price: Optional[float] = None,
        source: str = "telegram"
) -> Lead:
    """Создание лида с информацией об услуге"""
    lead = Lead(
        name=name,
        phone=phone,
        email=email,
        company=company,
        service_type=service_type,
        calculated_price=calculated_price,
        source=source,
        created_at=datetime.now()
    )

    db.add(lead)
    await db.commit()
    await db.refresh(lead)
    return lead


async def create_calculation(
        db: AsyncSession,
        user_id: int,
        service_type: str,
        parameters: dict,
        result: str,
        price: float
) -> Calculation:
    """Создание записи расчета"""
    calculation = Calculation(
        user_id=user_id,
        service_type=service_type,
        parameters=parameters,
        result=result,
        price=price,
        created_at=datetime.now()
    )

    db.add(calculation)
    await db.commit()
    await db.refresh(calculation)
    return calculation


async def get_service_statistics(db: AsyncSession, days: int = 30):
    """Получение статистики по услугам"""
    from datetime import datetime, timedelta

    start_date = datetime.now() - timedelta(days=days)

    # Статистика по выборам услуг
    service_stats = await db.execute(
        select(UserEvent.event_data, UserEvent.event_type, UserEvent.created_at)
        .where(
            UserEvent.created_at >= start_date,
            UserEvent.event_type.in_(['service_select', 'subservice_select', 'final_service_select'])
        )
    )

    return service_stats.all()


async def get_leads_by_service(db: AsyncSession):
    """Получение лидов с группировкой по услугам"""
    leads = await db.execute(
        select(Lead.service_type, Lead.calculated_price, Lead.created_at)
        .where(Lead.service_type.isnot(None))
    )

    return leads.all()