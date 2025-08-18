from sqlalchemy import Column, String, Boolean,Integer, BigInteger, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from src.database import Base
from src.domains.shared.model import Country

class TorVsWebCountryStats(Base):
    __tablename__ = "tor_vs_web_country_stats"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    country_code = Column(String(2), ForeignKey('countries.code'), nullable=False)  # Foreign key
    tor_traffic = Column(Boolean, nullable=False)
    internet_traffic = Column(Boolean, nullable=False)
    avg_http_request = Column(BigInteger, nullable=False)
    
        # Timestamp columns
    created_at = Column(DateTime, default=func.now(), nullable=False)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)

    # Relationship to Country (many stats belong to one country)
    country = relationship("Country", back_populates="stats")







