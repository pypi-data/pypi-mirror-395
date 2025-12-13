# gsc-api-handler

**`gsc-api-handler`** is a lightweight Python package designed to authorize and fetch data from the **Google Search Console API**, storing it directly into a local **SQLite database**.

## 🚀 Features

- 🔐 OAuth 2.0 user authorization with automatic token refresh
- 📊 Data fetching with pagination support
- 🗃️ Stores GSC metrics (clicks, impressions, CTR, position) into SQLite
- 🧩 Easily integrable with Django or other Python-based projects
- ✅ Minimal dependencies and clean, modular structure

---

## 📦 Installation

Install the package in editable mode during development:

```
pip install gsc-api-handler

```

You may want to use a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install gsc-api-handler

```

---

## ⚙️ Configuration

This package uses `python-decouple` to manage environment variables.

1. Create a `.env` file **in the project root**, outside the `src/` folder.
2. Add the following variables:

```dotenv
GSC_CLIENT_SECRET=gsc_credentials/client_secret.json
GSC_TOKEN_PATH=gsc_credentials/token.pickle
```

3. Create a `gsc_credentials/` folder and place your `client_secret.json` file inside.

The token will be created automatically after successful authentication.

> If `.env` is missing, default values `client_secret.json` and `token.pickle` will be used from the current working directory.

---

## ✅ Usage Example

Here is an example script (`test_fetch.py`) that uses the package to fetch GSC data and store it in SQLite:

```
from gsc_api_handler import fetch_and_store_gsc_data
from decouple import config 
from pathlib import Path


CLIENT_SECRETS_FILE = Path(config("GSC_CLIENT_SECRET", default="client_secret.json"))
TOKEN_FILE = Path(config("GSC_TOKEN_PATH", default="token.pickle"))

# BASE_DIR = Path(__file__).resolve().parent # in test_fetch.py 
# CLIENT_SECRETS_FILE = BASE_DIR / "gsc_credentials" / "client_secret.json"
# TOKEN_FILE = BASE_DIR / "gsc_credentials" / "token.pickle"

rows = fetch_and_store_gsc_data(
    site_url='sc-domain:yourdomain.com',
    db_path='gsc_yourdomain.sqlite',
    creds_path=CLIENT_SECRETS_FILE, 
    token_path=TOKEN_FILE,          
    dimensions=['query', 'page', 'date'],
    start_date='2024-06-01',
    end_date='2024-06-15'
)

print(f"{rows} rows fetched and saved.")
```

---

## 📁 Output Table Format

The `gsc_data` table contains:

| Column      | Type    | Description                      |
|-------------|---------|----------------------------------|
| `country`   | TEXT    | User country                     |
| `device`    | TEXT    | Device used                      |
| `query`     | TEXT    | Search query                     |
| `page`      | TEXT    | Landing page                     |
| `date`      | TEXT    | Date of the visit                |
| `clicks`    | INTEGER | Number of clicks                 |
| `impressions` | INTEGER | Number of impressions          |
| `ctr`       | REAL    | Click-through rate               |
| `position`  | REAL    | Average position in search       |

> Table name and dimensions are fully configurable.

---

## 📚 Requirements

This package depends on:

- `google-api-python-client`
- `google-auth`
- `google-auth-oauthlib`
- `python-dateutil`
- `python-decouple`

All dependencies are listed in `pyproject.toml`.

---

## 📝 License

This project is licensed under the [MIT License](LICENSE.txt)

---

## ✨ Author

Developed by [Miki Zivkovic](mailto:zmiroljub.zivkovic@gmail.com)  
© 2025-present
