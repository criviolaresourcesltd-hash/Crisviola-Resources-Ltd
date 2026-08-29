from datetime import datetime
from .extensions import db
class Product(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(160),nullable=False)
    slug=db.Column(db.String(180),unique=True,nullable=False)
    price=db.Column(db.Float,nullable=False,default=0)
    currency=db.Column(db.String(8),nullable=False,default='$')
    unit=db.Column(db.String(40),nullable=False,default='')
    description=db.Column(db.Text,nullable=False,default='')
    category=db.Column(db.String(100),nullable=False,default='Other Products')
    image=db.Column(db.String(255))
    specifications=db.Column(db.Text,nullable=False,default='')
    availability=db.Column(db.String(30),nullable=False,default='Available')
    featured=db.Column(db.Boolean,default=False,nullable=False)
    created_at=db.Column(db.DateTime,default=datetime.utcnow,nullable=False)
    updated_at=db.Column(db.DateTime,default=datetime.utcnow,onupdate=datetime.utcnow,nullable=False)
    @property
    def price_display(self):
        return f"{self.currency}{self.price:,.2f}".rstrip('0').rstrip('.')
