import re
from functools import wraps
from flask import current_app,redirect,session,url_for
from werkzeug.utils import secure_filename
def slugify(v): return re.sub(r'[^a-z0-9]+','-',v.lower()).strip('-')
def admin_required(view):
    @wraps(view)
    def w(*a,**k): return view(*a,**k) if session.get('admin_authenticated') else redirect(url_for('admin.login'))
    return w
def safe_upload_name(filename):
    n=secure_filename(filename)
    if not n:return None
    ext='.'+n.rsplit('.',1)[1].lower() if '.' in n else ''
    return n if ext in current_app.config['UPLOAD_EXTENSIONS'] else None
