from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine


DB_USER = 'test'
DB_PASS = 'asdasas123ASas112HJKAS'
DB_HOST = '89.19.217.67'
DB_NAME = 'attested-guiders-abkhazia'

DATABASE_URL = f'mysql+asyncmy://{DB_USER}:{DB_PASS}@{DB_HOST}/{DB_NAME}'

engine = create_async_engine(DATABASE_URL, echo=True)
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)

class Base(DeclarativeBase):
    pass

async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)