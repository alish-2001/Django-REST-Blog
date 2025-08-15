# 📝 Django REST Blog API

![Python](https://img.shields.io/badge/Python-3.x-blue?logo=python)
![Django](https://img.shields.io/badge/Django-4.x-green?logo=django)
![DRF](https://img.shields.io/badge/DRF-3.x-red?logo=django)

A clean and simple **Blog API** built with **Django Rest Framework (DRF)**. It provides endpoints for creating, reading, updating, and deleting blog posts with user authentication.

## 🚀 Features
- 🔐 **User Authentication** (Djoser + JWT)
- 📝 **CRUD Operations** for blog posts
- 📄 **Browsable API** with DRF
- 🔍 **Pagination & Filtering** support
- ⚡ **Admin Panel** for easy content management
- 🛠 **Modular & Maintainable Code**


## 📂 Project Structure


## 🛠 Installation & Setup
```bash
# 1️⃣ Clone the repository
git clone https://github.com/your-username/django-rest-blog.git
cd django-rest-blog

# 2️⃣ Create a virtual environment
python -m venv venv
source venv/bin/activate  # Mac/Linux
venv\Scripts\activate     # Windows

# 3️⃣ Install dependencies
pip install -r requirements.txt

# 4️⃣ Apply migrations
python manage.py migrate

# 5️⃣ Create a superuser
python manage.py createsuperuser

# 6️⃣ Run the development server
python manage.py runserver
