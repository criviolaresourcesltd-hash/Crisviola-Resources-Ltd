from pathlib import Path
from flask import (
    Blueprint,
    current_app,
    flash,
    redirect,
    render_template,
    request,
    session,
    url_for,
)
from ..extensions import db
from ..models import Product
from ..utils import admin_required, safe_upload_name, slugify
import uuid
import cloudinary
import cloudinary.uploader


admin_bp = Blueprint("admin", __name__, url_prefix="/admin")


@admin_bp.route("/login", methods=["GET", "POST"])
def login():
    if (
        request.method == "POST"
        and request.form.get("username") == current_app.config["ADMIN_USERNAME"]
        and request.form.get("password") == current_app.config["ADMIN_PASSWORD"]
    ):
        session["admin_authenticated"] = True
        return redirect(url_for("admin.dashboard"))

    if request.method == "POST":
        flash("Invalid admin credentials.", "error")

    return render_template("admin/login.html")


@admin_bp.get("/logout")
def logout():
    session.pop("admin_authenticated", None)
    return redirect(url_for("admin.login"))


@admin_bp.get("/")
@admin_required
def dashboard():
    return render_template(
        "admin/dashboard.html",
        products=Product.query.order_by(Product.updated_at.desc()).all(),
    )


@admin_bp.route("/products/new", methods=["GET", "POST"])
@admin_required
def new():
    if request.method == "POST":
        p = Product()
        save(p)
        db.session.add(p)
        db.session.commit()
        flash("Product added.", "success")
        return redirect(url_for("admin.dashboard"))

    return render_template(
        "admin/product_form.html",
        product=None,
        title="Add product",
    )


@admin_bp.route("/products/<int:product_id>/edit", methods=["GET", "POST"])
@admin_required
def edit(product_id):
    p = Product.query.get_or_404(product_id)

    if request.method == "POST":
        save(p)
        db.session.commit()
        flash("Product updated.", "success")
        return redirect(url_for("admin.dashboard"))

    return render_template(
        "admin/product_form.html",
        product=p,
        title="Edit product",
    )


@admin_bp.post("/products/<int:product_id>/delete")
@admin_required
def delete(product_id):
    db.session.delete(Product.query.get_or_404(product_id))
    db.session.commit()
    flash("Product deleted.", "success")
    return redirect(url_for("admin.dashboard"))


def configure_cloudinary():
    """Configure Cloudinary using Render environment variables."""
    cloudinary.config(
        cloud_name=current_app.config.get("CLOUDINARY_CLOUD_NAME"),
        api_key=current_app.config.get("CLOUDINARY_API_KEY"),
        api_secret=current_app.config.get("CLOUDINARY_API_SECRET"),
        secure=True,
    )


def upload_to_cloudinary(file, product_name):
    """Upload a product image to Cloudinary and return its secure URL."""
    configure_cloudinary()

    result = cloudinary.uploader.upload(
        file,
        folder="crisviola/products",
        public_id=f"{slugify(product_name)}-{uuid.uuid4().hex[:8]}",
        resource_type="image",
    )

    return result["secure_url"]


def save(p):
    p.name = request.form.get("name", "").strip()
    p.slug = f"{slugify(p.name)}-{p.id or uuid.uuid4().hex[:6]}"
    p.price = float(request.form.get("price") or 0)
    p.currency = request.form.get("currency", "$").strip() or "$"
    p.unit = request.form.get("unit", "").strip()
    p.category = request.form.get("category", "Other Products").strip()
    p.description = request.form.get("description", "").strip()
    p.specifications = request.form.get("specifications", "").strip()
    p.availability = request.form.get("availability", "Available")
    p.featured = request.form.get("featured") == "on"

    f = request.files.get("image")

    if f and f.filename:
        name = safe_upload_name(f.filename)

        if name:
            try:
                # New uploads go to Cloudinary.
                image_url = upload_to_cloudinary(f, p.name)
                p.image = image_url
            except Exception as e:
                current_app.logger.exception("Cloudinary upload failed")
                flash(
                    "Image upload failed. Please check the Cloudinary settings.",
                    "error",
                )
        else:
            flash("Use JPG, JPEG, PNG or WEBP.", "error")