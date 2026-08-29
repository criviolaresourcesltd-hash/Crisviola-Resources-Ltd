# CRISVIOLA RESOURCES LTD Flask Catalogue

## Run on Windows

```powershell
python -m venv env
env\Scripts\activate
pip install -r requirements.txt
python run.py
```

Open `http://127.0.0.1:5000`.

Admin: `http://127.0.0.1:5000/admin/login`

The project includes all 13 bundled product images under:

`app/static/images/products/`

The application automatically creates `instance/catalogue.db` and repairs the seeded products' image paths when it starts.

Business settings are stored in `.env` so you do not need to edit Python files.
