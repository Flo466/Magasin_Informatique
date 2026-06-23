# 🛒 Magasin Informatique - E-commerce Web App

A complete, Dockerized e-commerce web application built with Flask and MySQL. This project simulates a computer hardware store, featuring user authentication, shopping cart management, simulated secure checkout, and an administration dashboard.

## ✨ Features

* **User Authentication:** Secure signup with password hashing (bcrypt) and simulated email verification via code.
* **Shopping Cart:** Add, review, and remove items dynamically.
* **Checkout Simulation:** Stock validation, simulated credit card payment processing, and order confirmation.
* **Admin Dashboard:** Dedicated interface to manage products, view registered clients, and track orders.
* **Fully Dockerized:** Seamless deployment using Docker and Docker Compose (App, Database, and Database Management).

## 🛠️ Tech Stack

* **Backend:** Python 3.11, Flask
* **Database:** MySQL 8.0
* **Frontend:** HTML5, CSS3 (Custom responsive UI)
* **Infrastructure:** Docker, Docker Compose
* **Tools:** Adminer (Database Management)

## 🚀 Getting Started

### Prerequisites

You only need to have [Docker](https://docs.docker.com/get-docker/) and [Docker Compose](https://docs.docker.com/compose/install/) installed on your machine.

### Installation & Run

1.  **Clone the repository** (if applicable) or navigate to the project directory:
    ```bash
    cd Magasin_Informatique
    ```

2.  **Build and start the containers:**
    ```bash
    docker compose up -d --build
    ```
    *Note: On the first run, MySQL will automatically initialize the database schema and populate dummy data using the scripts mapped from the `initdb/` directory.*

### 🌐 Access Points

Once the containers are up and running, you can access the services via your web browser:

* **Main Web Application:** [http://localhost:5000](http://localhost:5000)
* **Database Management (Adminer):** [http://localhost:8080](http://localhost:8080)
    * *System:* MySQL
    * *Server:* `db`
    * *Username:* `root`
    * *Password:* `ton_mot_de_passe`
    * *Database:* `magasin_informatique`

## 🧪 Testing the Application

### Admin Access
To access the administration dashboard and view global statistics, products, and orders:
* **Email:** `admin`
* **Password:** `1234`

### Client Access & Checkout Flow
1.  Navigate to the signup page and create a new account.
2.  Use the generated verification code to activate the account.
3.  Log in, browse the catalog, and add items to your cart.
4.  Proceed to payment. You can use the following dummy credit card details for testing:
    * **Card Number:** `1111 2222 3333 4444`
    * **Expiration:** `12/28`
    * **CVV:** `123`

## 📁 Project Structure

```text
Magasin_Informatique/
├── app.py                 # Main Flask application and routing
├── requirements.txt       # Python dependencies
├── Dockerfile             # App container build instructions
├── docker-compose.yml     # Multi-container orchestration
├── initdb/
│   └── init.sql           # Database schema and initial data
├── static/
│   ├── style.css          # Global stylesheet
│   └── fond.jpg           # Background image
└── templates/             # HTML templates (login, cart, checkout, etc.)