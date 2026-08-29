from flask import Flask
from pathlib import Path
from config import Config
from .extensions import db
from .routes.public import public_bp
from .routes.admin import admin_bp
from .utils import slugify

def create_app():
    app=Flask(__name__, instance_relative_config=True)
    app.config.from_object(Config)
    Path(app.instance_path).mkdir(parents=True, exist_ok=True)
    db.init_app(app)
    app.register_blueprint(public_bp); app.register_blueprint(admin_bp)
    with app.app_context():
        from .models import Product
        db.create_all(); seed(Product)
    return app

def seed(Product):
    data=[
    ('Crayfish',35.3,'5KG','Seafood','images/products/crayfish.jpeg',1),('Bitterleaf',42.7,'5KG','Food Products','images/products/bitterleaf.jpeg',1),('Cashew Nuts',59.6,'5KG','Nuts & Seeds','images/products/cashew-nuts.jpeg',1),('Dried Hibiscus Flowers',19.9,'5KG','Food Products','images/products/dried-hibiscus-flowers.jpeg',1),('Egusi',13.3,'5KG','Nuts & Seeds','images/products/egusi.jpeg',1),('Garlic',14.7,'5KG','Spices','images/products/garlic.jpeg',0),('Ginger',27.3,'5KG','Spices','images/products/ginger.jpeg',0),('Groundnuts',8.9,'5KG','Nuts & Seeds','images/products/groundnuts.jpeg',0),('Negro Pepper',39.7,'5KG','Pepper & Spices','images/products/negro-pepper.jpeg',0),('Palm Kernel Oil',22.1,'5L','Oils','images/products/palm-kernel-oil.jpeg',0),('Red Oil',17,'5L','Oils','images/products/red-oil.jpeg',0),('Tiger Nut',20,'5KG','Nuts & Seeds','images/products/tiger-nut.jpeg',0),('Uziza Seeds',176.6,'5KG','Spices','images/products/uziza-seeds.jpeg',0)]
    # Seed new products and repair image paths for existing installations.
    # This is important when the database was created by an earlier project
    # version that did not store the bundled product images.
    for name,price,unit,cat,image,featured in data:
        p=Product.query.filter_by(name=name).first()
        if p is None:
            p=Product(name=name,slug=slugify(name),price=price,currency='$',unit=unit,category=cat)
            db.session.add(p)
        p.price=price
        p.currency='$'
        p.unit=unit
        p.category=cat
        p.image=image
        p.featured=bool(featured)
        p.availability='Available'
        if not p.description:
            p.description=f'{name} catalogue listing. Contact CRISVIOLA RESOURCES LTD on WhatsApp for availability, quantity, delivery and final pricing.'
    db.session.commit()
