from src.database import Base, engine
from src.domains.shared.models import Country #country table to migrate to db
from src.domains.tor_net_fetcher.models import TorVsWebCountryStats

def create_all_tables():
    print("Creating all tables...")
    Base.metadata.create_all(bind=engine)
    print("Tables created successfully")

if __name__ == "__main__":
    create_all_tables()