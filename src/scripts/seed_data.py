from src.database import engine, Base, get_db
from domains.shared.model import Country
from domains.tor_net_fetcher.model import TorVsWebCountryStats  # Import both!


def seed_countries():
    countries = [
        {"code": "US", "name": "United States"},
        {"code": "DE", "name": "Germany"},
        {"code": "RU", "name": "Russia"},
        {"code": "FR", "name": "France"},
        {"code": "NL", "name": "Netherlands"},
        {"code": "GB", "name": "United Kingdom"},
        {"code": "CA", "name": "Canada"},
        {"code": "SE", "name": "Sweden"},
        {"code": "CH", "name": "Switzerland"},
        {"code": "NO", "name": "Norway"},
        {"code": "FI", "name": "Finland"},
        {"code": "AT", "name": "Austria"},
        {"code": "JP", "name": "Japan"},
        {"code": "AU", "name": "Australia"},
        {"code": "BR", "name": "Brazil"},
        {"code": "IT", "name": "Italy"},
        {"code": "ES", "name": "Spain"},
        {"code": "PL", "name": "Poland"},
        {"code": "DK", "name": "Denmark"},
        {"code": "BE", "name": "Belgium"},
        {"code": "IN", "name": "India"},
        {"code": "CN", "name": "China"},
        {"code": "KR", "name": "South Korea"},
        {"code": "SG", "name": "Singapore"},
        {"code": "MX", "name": "Mexico"}
    ]
    
    db = next(get_db())
    try:
        for country in countries:
            db.merge(Country(**country))
        
        db.commit()  # Move this OUTSIDE the loop
        print(f"Seeded {len(countries)} countries")  # Better message
        
    except Exception as e:
        db.rollback()
        print(f"Error: {e}")
        raise
    finally:
        db.close()
    
if __name__ == "__main__":
    seed_countries()