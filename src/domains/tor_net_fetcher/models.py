from sqlalchemy import Column, Integer, String, DateTime
import datetime
from src.database import Base

class TorRelay(Base):
    __tablename__ = "tor_relays"
    fingerprint = Column(String, primary_key=True)
    nickname = Column(String)
    last_seen = Column(DateTime)

    CREATE TABLE internet_tor_activity (
    id SERIAL PRIMARY KEY,
    country_id INTEGER NOT NULL REFERENCES countries(country_id),
    measurement_date DATE NOT NULL,
    tor_http_requests BIGINT DEFAULT 0,
    total_http_requests BIGINT DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(country_id, measurement_date)
);

class Tor_vs_Web_Country_Stats(Base):
    __tablename__ = "tor_vs_web_country_stats"


