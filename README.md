# 🚗 AutoRIA Parser

This project is a **web scraping application** built to extract car listing data from a marketplace website. It collects structured vehicle information daily, using an asynchronous and headless browser-based approach, and stores it in a **PostgreSQL database** with automatic backups.


## 📌 Features

- 🔍 **Scrapes car listings** from multiple pages
- ⚡ **Asynchronous fetching** using `aiohttp` and `playwright`
- 🌐 **Headless browser automation** for dynamic content
- 🧠 **BeautifulSoup** for HTML parsing
- 🗃️ **PostgreSQL** database with SQLAlchemy ORM
- 🔁 **Daily scheduling** with `schedule`
- 📦 **Automatic PostgreSQL database dumps**
- 🐳 **Dockerized for easy setup**


## ⚙️ Technologies Used

| Purpose               | Library               |
|-----------------------|------------------------|
| HTML parsing          | `beautifulsoup4`       |
| Async HTTP requests   | `aiohttp`              |
| Dynamic interaction   | `playwright` (async)   |
| Task scheduling       | `schedule`             |
| ORM + DB              | `SQLAlchemy`, `psycopg2-binary` |
| Env config            | `python-dotenv`        |
| Database dump         | `pg_dump` via `subprocess` |
| Containerization      | `Docker`, `docker-compose` |


## ⚙️ How It Works

1. **Catalog Pages**  
   The scraper asynchronously fetches listing pages (`parse_catalog`) using `aiohttp`.

2. **Item Details**  
   Each item's detailed page is opened using `playwright`, which allows interaction with dynamic content (e.g. "show phone number").

3. **HTML Parsing**  
   `BeautifulSoup` extracts structured data from the page's HTML.

4. **Data Storage**  
   Parsed items are added to a PostgreSQL database using SQLAlchemy models.

5. **Backups**  
   Once a day, the `scheduler.py` script also triggers a `pg_dump` to save a database backup.


## 🛠️ Setup & Run Locally

### 1. Clone the repo

```bash
git clone https://github.com/korovkincode/autoria-test
cd autoria-test
```

### 2. Add `.env` file

Create a `.env` file in the root:

```env
TARGET_PAGE=https://auto.ria.com/car/used
PAGE_LIMIT=1
START_TIME=12:00

DATABASE_URL=postgresql://caruser:carpassword@db:5432/carparser
PGUSER=caruser
PGPASSWORD=carpassword
PGNAME=carparser
```

### 3. Run with Docker

Make sure Docker and Docker Compose are installed.

```bash
docker-compose up --build
```

> This starts both the PostgreSQL database and your scraping container. The scraper runs once a day at `START_TIME`.

### 4. Run Manually (if needed)

If you want to manually run the scraper inside Docker:

```bash
docker-compose exec app python main.py
```

Or trigger the scheduler script:

```bash
docker-compose exec app python scheduler.py
```


## 📦 Daily Backups

Backups are saved as `.dump` files in the `dumps/` folder, named by date:

```
dumps/
└── 13-06-2025.dump
```


## ✅ Test Coverage & Logging

- Logs are printed to the console using Python's `logging` module.
- Errors are handled gracefully with custom exceptions for parsing and startup checks.