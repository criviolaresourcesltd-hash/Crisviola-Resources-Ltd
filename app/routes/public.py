from flask import Blueprint,render_template,request,jsonify,url_for,current_app
from sqlalchemy import or_
from ..models import Product
public_bp=Blueprint('public',__name__)
@public_bp.app_context_processor
def globals(): return {'whatsapp_number':current_app.config['WHATSAPP_NUMBER'],'hero_video_url':current_app.config['HERO_VIDEO_URL'],'business_email':current_app.config['BUSINESS_EMAIL'],'business_address':current_app.config['BUSINESS_ADDRESS']}
@public_bp.get('/')
def home():
    featured=Product.query.filter_by(featured=True).order_by(Product.updated_at.desc()).limit(8).all(); cats=[x[0] for x in Product.query.with_entities(Product.category).distinct().order_by(Product.category)]
    return render_template('public/home.html',featured=featured,categories=cats)
@public_bp.get('/products')
def products():
    q=request.args.get('q','').strip(); category=request.args.get('category','').strip(); query=Product.query
    if category: query=query.filter_by(category=category)
    if q:
        like=f'%{q}%'; query=query.filter(or_(Product.name.ilike(like),Product.category.ilike(like),Product.description.ilike(like)))
    ps=query.order_by(Product.featured.desc(),Product.name).all(); cats=[x[0] for x in Product.query.with_entities(Product.category).distinct().order_by(Product.category)]
    return render_template('public/products.html',products=ps,categories=cats,active_category=category,q=q)
@public_bp.get('/products/<int:product_id>')
def detail(product_id): return render_template('public/product_detail.html',product=Product.query.get_or_404(product_id))
@public_bp.get('/about')
def about(): return render_template('public/about.html')
@public_bp.get('/contact')
def contact(): return render_template('public/contact.html')
@public_bp.get('/api/products')
def api():
    q=request.args.get('q','').strip(); category=request.args.get('category','').strip(); query=Product.query
    if category: query=query.filter_by(category=category)
    if q:
        like=f'%{q}%'; query=query.filter(or_(Product.name.ilike(like),Product.category.ilike(like),Product.description.ilike(like)))
    return jsonify([{'name':p.name,'price':p.price_display,'unit':p.unit,'category':p.category,'availability':p.availability,'image':url_for('static',filename=p.image) if p.image else None,'detail_url':url_for('public.detail',product_id=p.id)} for p in query.order_by(Product.name).all()])
