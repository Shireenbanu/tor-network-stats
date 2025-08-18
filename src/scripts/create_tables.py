from src.database import Base, engine
from domains.shared.model import Country #country table to migrate to db
from domains.tor_net_fetcher.model import TorVsWebCountryStats

def create_all_tables():
    print("Creating all tables...")
    Base.metadata.create_all(bind=engine)
    print("Tables created successfully")

if __name__ == "__main__":
    create_all_tables()