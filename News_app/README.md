This is a Django web application project that includes two main apps:

* **account**: Handles account interactions.
* **content**: Basic news functionality with articles, newsletters, and publishers.

---

## Table of Contents

- [Table of Contents](#table-of-contents)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Database Setup](#database-setup)
- [Running the Project](#running-the-project)
- [Usage](#usage)
- [Troubleshooting](#troubleshooting)
- [Project Structure](#project-structure)

---

## Prerequisites

Before you begin, ensure you have met the following requirements:

* Python 3.9 or later installed. [Download Python](https://www.python.org/downloads/)
* MySQL installed and running on your machine.
* Basic knowledge of using the command line / terminal.
* Git installed to clone the repository (optional but recommended).

---

## Installation

1. **Clone the repository** (or download the ZIP and extract):

   ```bash
   git clone https://github.com/jayden-lockhart/news_app.git
   cd news
   ```

2. **Create and activate a virtual environment** (recommended):

   * On Windows:

     ```bash
     python -m venv venv
     venv\Scripts\activate
     ```
   * On macOS/Linux:

     ```bash
     python3 -m venv venv
     source venv/bin/activate
     ```

3. **Install the required Python packages:**

   ```bash
   pip install -r requirements.txt
   ```


---

## Database Setup

1. **Create MariaDB  database:**

   Login to your MariaDB  server and create the database:

   ```sql
   CREATE DATABASE news_app_db;
   ```

2. **Update database credentials in `news/settings.py`** if your MariaDB username or password differ:

   ```python
   DATABASES = {
       'default': {
           'ENGINE': 'django.db.backends.mysql',
           'NAME': 'news_app_db',
           'USER': 'root',
           'PASSWORD': 'root',
           'HOST': 'localhost',
           'PORT': '',
       }
   }
   ```

3. **Install MySQL Python adapter** if not already installed:

   ```bash
   pip install mysqlclient
   ```

---

## Running the Project

1. **Apply migrations:**

   Run the following commands to create the necessary database tables:

   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

2. **Create a superuser** (for admin access):

   ```bash
   python manage.py createsuperuser
   ```

   Follow the prompts to create a user with admin privileges.

3. **Run the development server:**

   ```bash
   python manage.py runserver
   ```

4. **Access the application:**

   * Open your browser and go to: [http://127.0.0.1:8000/](http://127.0.0.1:8000/)
   * You can login, register new users, browse articles, and newsletters.

---

## Usage

* **Authentication (`accounts` app):**

  * Login at `/` (root URL)
  * Register at `/register/`
  

* **News_app (`news` app):**

  * View all approved articles and newsletters at `/` (root URL, depending on project URL setup)
  * View article and newsletter details, change their content (if authorized), add articles and newsletters.

---



## Troubleshooting

* **MySQL Client Missing Error:**

  If you get `ModuleNotFoundError: No module named 'mysqlclient'`, install it with:

  ```bash
  pip install mysqlclient
  ```

* **SMTP Authentication Error:**

  Make sure you use correct email and password. For Gmail, you might need to use App Passwords instead of your regular password.

* **Static files not loading:**

  During development, Django serves static files automatically. For production, you need to configure static files properly.

---

## Project Structure

```
News_app/
├── news/
│   ├── settings.py          # Project settings (DB, email, apps)
│   ├── urls.py              # Root URL routing
│   └── wsgi.py
├── account/              # account app
│   ├── models.py
│   ├── views.py
│   ├── templates/
│   ├── urls.py
│   └── ...
├── content/               # content app
│   ├── models.py
│   ├── views.py
│   ├── templates/
│   └── urls.py
├── manage.py                # Django CLI utility
└── requirements.txt         # Python dependencies
```

---
