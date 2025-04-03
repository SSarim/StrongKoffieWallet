# ☕ StrongKoffie Blockchain Wallet

A lightweight, decentralized blockchain wallet built using FastAPI. Users can register, login, manage their balances, and make peer-to-peer cryptocurrency transactions — all within a stylish and intuitive interface.

🌐 Live Demo: [StrongKoffee Wallet](https://blockchainwallet-ece5ghd7gvc7gpec.canadaeast-01.azurewebsites.net/)
---

## 🚀 Features

- 🧑‍💻 User Registration & Login with hashed passwords
- 💼 Balance management and validation
- 🔐 Session-based authentication (no token juggling)
- 💸 Secure peer-to-peer crypto-style transactions
- 🧾 Transaction history: per-user & network-wide
- 🖥️ Responsive front-end (HTML + JS + Pico.css)
- ✅ Unit test suite for backend routes and models

---

## 🧰 Tech Stack

- **Backend:** FastAPI, Uvicorn, Pydantic, Passlib
- **Frontend:** HTML, JavaScript, Pico.css
- **Deployment:** Azure
- **Security:** SHA-256 Address Hashing
- **Optional DB:** SQLAlchemy ORM (currently disabled)
- **Testing:** Pytest

---
## 📁 Project Structure

```
.
├── app/
│   ├── auth.py              # Auth & session utils
│   ├── blockchain.py        # SQLAlchemy models (optional DB backend)
│   ├── database.py          # DB engine/init (unused)
│   ├── models.py            # Pydantic models
│   ├── routes.py            # API logic
│   ├── security.py          # SHA256 hashing
│   ├── store.py             # In-memory data store
│   ├── static/
│   │   ├── design.css
│   │   └── script.js
│   └── templates/
│       └── index.html
├── images/
│   └── StrongKoffie.png     # UI screenshot
├── tests/
│   ├── test_blockchain.py
│   ├── test_models.py
│   └── test_routes.py
├── Dockerfile
├── main.py
├── README.md
└── requirements.txt
```
```## ⚙️ Local Development

### 1. Clone and Setup

```bash
git clone https://github.com/your-username/StrongKoffieWallet.git
cd StrongKoffieWallet
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## ⚙️ Local Development

### 1. Clone and Setup

```bash
git clone https://github.com/SSarim/StrongKoffieWallet.git
cd StrongKoffieWallet
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 2. Run the App

```bash
uvicorn main:app --reload
```

Visit: [http://localhost:8000](http://localhost:8000)

---

## 🐳 Docker Deployment

```bash
docker build -t strongkoffie-wallet .
docker run -p 8000:8000 strongkoffie-wallet
```

To start the container again:

```bash
docker start strongkoffie-wallet
```

---

## 🔧 API Overview

| Method | Endpoint                  | Description                          |
|--------|---------------------------|--------------------------------------|
| POST   | `/register`               | Create new user                      |
| POST   | `/login`                  | Authenticate and start session       |
| POST   | `/logout`                 | Logout user                          |
| POST   | `/transaction/`           | Send balance to another user         |
| GET    | `/balance/`               | Retrieve your balance                |
| GET    | `/transactions/`          | View personal transactions           |
| GET    | `/transactions_network/`  | View all transactions in system      |

---

## 🧪 Testing the App

- Register a user through the UI.
- Login and check your balance (100₿ default).
- Send crypto to another registered user.
- View personal and network-wide transaction histories.

---

## 🧠 Developer Notes

- All user and transaction data are stored in an in-memory Python `dict` for simplicity.
- There is support for using a SQLAlchemy-based backend, but it's currently commented out in the code (`blockchain.py`, `routes.py`, `auth.py`), due to deployment expenses.
- All usernames are hashed using SHA-256 when stored in transactions for privacy.

---

## 📸 Screenshots

![StrongKoffie Wallet UI](/images/StrongKoffie.png)

---
## Contact
For inquiries or support, please reach out to:
- **Project Maintainer:**  SSarim
  [GitHub](https://github.com/SSarim)
- **Project Maintainer:**  shaheryar-abid 
  [GitHub](https://github.com/shaheryar-abid)
- **Project Maintainer:**  Brandon Wong
- **Project Maintainer:**  Christian Sorto
---
## 📃 License

MIT License — feel free to fork, remix, and build upon this.

---

Built with ❤️ by StrongKoffie Wallet☕!

---


