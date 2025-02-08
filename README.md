
# Django Project Setup with Tailwind CSS

## 1. Clone the Repository
```bash
git clone https://github.com/vedant2863/ShopSphere
cd myproject
```

## 2. Create a Virtual Environment
```bash
python -m venv venv
```

## 3. Activate Virtual Environment
- **Linux/macOS:**
  ```bash
  source venv/bin/activate
  ```
- **Windows:**
  ```bash
  venv\Scripts\activate
  ```

## 4. Install Dependencies
```bash
pip install -r requirements.txt
```

``

## 5. Apply Migrations and Start Tailwind
```bash
python manage.py migrate
python manage.py tailwind install
python manage.py tailwind start
```

## 6. Run the Django Development Server
```bash
python manage.py runserver
```

## 7. Create a Superuser
To access the Django admin panel, create a superuser:
```bash
python manage.py createsuperuser
```
Follow the prompts to enter a username, email, and password.

## 8. Run the Django Development Server
```bash
python manage.py runserver
```

Now, your Django project is set up with Tailwind CSS! 🎉

