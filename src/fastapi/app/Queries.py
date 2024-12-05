from fastapi import FastAPI
from time_it import time_def
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
import pandas as pd
from app.SQLsetup import mysql_conn_str
from app.SQLClasses import Product

app = FastAPI()

# Set up the engine and sessionmaker globally (synchronous)
engine = create_engine(mysql_conn_str(), pool_size=5, max_overflow=10, pool_timeout=30, pool_recycle=3600)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@time_def(log_name="profiler")
def stock_list(limit: int = 10, skip: int = 0, term: str = "") -> pd.DataFrame:
    query = text(f"""SELECT symbol, price FROM orderbook.Product
    WHERE symbol NOT LIKE '%\.%' AND symbol NOT LIKE '%1%'
    AND symbol LIKE '{term}%'
    ORDER BY symbol
    LIMIT {limit} OFFSET {skip}
    """)

    with SessionLocal() as session:
        df = pd.read_sql(query, session.bind)

    return df

@time_def(log_name="profiler")
def stock_quote(symbol: str = None) -> float:
    query = text(f"""SELECT price FROM orderbook.Product
                WHERE symbol='{symbol}'""")

    with SessionLocal() as session:
        df = pd.read_sql(query, session.bind)

    return round(float(df['price'][0]), 2) if not df.empty else 0.0

@time_def(log_name="profiler")
def num_stocks(term: str = "") -> int:
    query = text(f"""SELECT COUNT(*) as number FROM orderbook.Product
    WHERE symbol NOT LIKE '%\.%' AND symbol NOT LIKE '%1%'
    AND symbol LIKE '{term}%'
    """)

    with SessionLocal() as session:
        df = pd.read_sql(query, session.bind)

    return int(df['number'][0]) if not df.empty else 0
