from sqlalchemy import Column, String
from src.database import Base
from sqlalchemy.orm import relationship


class Country(Base):
    __tablename__ = "countries"

    code = Column(String(2), primary_key = True)
    name = Column(String(100), nullable = False)

    stats = relationship("TorVsWebCountryStats", back_populates="country")