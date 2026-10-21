from sqlmodel import create_engine

DATABASE_URL = "postgresql://naija_user:naija_password@localhost:5432/naija_marketplace"

engine = create_engine(DATABASE_URL)