from app.database import sessionLocal, engine, Base
from app import models
from app.auth.utils import hash_password

Base.metadata.create_all(bind=engine)

db = sessionLocal()

# Clear existing data
db.query(models.CartItem).delete()
db.query(models.Product).delete()
db.query(models.User).delete()

# Create test users
admin = models.User(
    username="admin",
    email="admin@test.com",
    hashed_password=hash_password("admin123"),
    is_admin=True,
)
user = models.User(
    username="user",
    email="user@test.com",
    hashed_password=hash_password("user123"),
    is_admin=False,
)

# Add sample products
product1 = models.Product(
    name="Laptop",
    description="High-Performance Laptop",
    price=999.99,
    quantity=10,
)
product2 = models.Product(
    name="Desktop PC",
    description="Desktop Personal Computer",
    price=799.99,
    quantity=10,
)
product3 = models.Product(
    name="Monitor",
    description="Computer Monitor",
    price=149.99,
    quantity=10,
)
product4 = models.Product(
    name="TV",
    description="High-End 65-inch Television",
    price=1249.99,
    quantity=10,
)

db.add_all([admin, user, product1, product2, product3, product4])
db.commit()
print("Database seeded successfully.")
