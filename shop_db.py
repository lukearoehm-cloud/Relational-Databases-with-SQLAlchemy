from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

engine = create_engine('sqlite:///shop.db',)
Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()

class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    
    orders = relationship('Order', back_populates='user', cascade='all, delete-orphan')

    def __repr__(self):
        return f"<User(id={self.id}, name='{self.name}', email='{self.email}')>"


class Product(Base):
    __tablename__ = 'products'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    price = Column(Integer, nullable=False)
    
    orders = relationship('Order', back_populates='product')

    def __repr__(self):
        return f"<Product(id={self.id}, name='{self.name}', price={self.price})>"


class Order(Base):
    __tablename__ = 'orders'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    product_id = Column(Integer, ForeignKey('products.id'), nullable=False)
    quantity = Column(Integer, nullable=False)
    
    user = relationship('User', back_populates='orders')
    product = relationship('Product', back_populates='orders')

    def __repr__(self):
        return f"<Order(id={self.id}, user_id={self.user_id}, product_id={self.product_id}, qty={self.quantity})>"


Base.metadata.create_all(engine)
print("✅ Tables created successfully!\n")


user1 = User(name="Alice Johnson", email="alice@example.com")
user2 = User(name="Bob Smith", email="bob@example.com")
session.add_all([user1, user2])
session.commit()

product1 = Product(name="Laptop", price=1200)
product2 = Product(name="Smartphone", price=800)
product3 = Product(name="Wireless Headphones", price=150)
session.add_all([product1, product2, product3])
session.commit()

order1 = Order(user_id=user1.id, product_id=product1.id, quantity=1)
order2 = Order(user_id=user1.id, product_id=product2.id, quantity=2)
order3 = Order(user_id=user2.id, product_id=product3.id, quantity=3)
order4 = Order(user_id=user2.id, product_id=product1.id, quantity=1)
session.add_all([order1, order2, order3, order4])
session.commit()

print("✅ Sample data inserted (2 users, 3 products, 4 orders)\n")



print("=== All Users ===")
users = session.query(User).all()
for user in users:
    print(user)
print()

print("=== All Products ===")
products = session.query(Product).all()
for prod in products:
    print(f"{prod.name} - ${prod.price}")
print()

print("=== All Orders (with User & Product) ===")
orders = session.query(Order).join(User).join(Product).all()
for order in orders:
    print(f"{order.user.name} bought {order.quantity}x {order.product.name} (${order.product.price})")
print()

print("=== Updating Laptop price to $999 ===")
laptop = session.query(Product).filter(Product.name == "Laptop").first()
if laptop:
    laptop.price = 999
    session.commit()
    print(f"Updated: {laptop}\n")

print("=== Deleting Bob Smith (ID 2) ===")
bob = session.query(User).filter(User.email == "bob@example.com").first()
if bob:
    session.delete(bob)
    session.commit()
    print("Bob and his orders have been deleted.\n")

print("=== Remaining Users ===")
for user in session.query(User).all():
    print(user)

print("\n🎉 All tasks completed! Check shop.db file in your directory.")