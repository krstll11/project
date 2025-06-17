# seed.py
from sqlalchemy.orm import Session
from database import SessionLocal, engine
from models import Base, Role, User, Category, Ad, Response, Favorite
from routers.auth import get_password_hash  as hashed_password
def seed_data(db: Session):
    
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    
    admin_role = Role(name="admin")
    user_role = Role(name="user")
    mod_role = Role(name="moderator")
    db.add_all([admin_role, user_role, mod_role])
    db.commit()

    
    admin = User(email="admin@example.com", nickname="admin", password=hashed_password("admin"), role=admin_role)
    user1 = User(email="moderator@example.com", nickname="Анна", password=hashed_password("admin"), role=mod_role)
    user2 = User(email="user@example.com", nickname="Ежовый", password=hashed_password("admin"), role=user_role)
    db.add_all([admin, user1, user2])
    db.commit()

   
    cat1 = Category(name="Electronics")
    cat2 = Category(name="Books")
    cat3= Category(name="Cars")
    db.add_all([cat1, cat2])
    db.commit()

 
    ad1 = Ad(title="Ноутбук Dell" , description= "Новый не использовался i5 32gb", price=500.0, author=admin, category=cat1)
    ad2 = Ad(title="Гарри поттер", description="Полный набор", price=100.0, author=user1, category=cat2)
    ad3 = Ad(title="Mercedes", description="Полный набор", price=100.0, author=user2, category=cat3)
    ad4 = Ad(title="Audi", description="Полный набор", price=100.0, author=user2, category=cat3)
    db.add_all([ad1, ad2, ad3, ad4])
    db.commit()

 
    resp1 = Response(message="Все еще продаете", ad=ad1, user=user1)
    resp2 = Response(message="Есть ли торг", ad=ad2, user=user2)
    db.add_all([resp1, resp2])
    db.commit()

    fav1 = Favorite(user=user2, ad=ad1)
    fav2 = Favorite(user=user1, ad=ad2)
    db.add_all([fav1, fav2])
    db.commit()

    print("Database seeded successfully.")

if __name__ == "__main__":
    db = SessionLocal()
    try:
        seed_data(db)
    finally:
        db.close()
