from src.database import get_db
from domains.shared.models import Country

def seed_countries():
    countries= {
        {"code": "US", "name": "United States"},
        {"code": "DE", "name": "Germany"},       
    }


    db = next(get_db())
    try:
        for country in countries:
            db.merge(Country(**country))
        db.commit()
        print(f"Seeded Countries")
    except Exception as e:
        db.rollback()
        print(f"Error: {e}")
        raise
    finally:
        db.close()

if __name__ == "__main__":
    seed_countries()