# Sales and Jokes Applications

This repository contains two Python scripts: `sales_process.py` for processing sales data and `app.py` for managing jokes using a Flask-based web application.

---

## 1. Sales Data Processing (`sales_process.py`)

### Overview
The `sales_process.py` script processes sales data from two Excel files (`order_region_a.xlsx` and `order_region_b.xlsx`), cleans and transforms the data, and stores it in an SQLite database (`sales.db`). It also validates the data using SQL queries.

## 2. Jokes Application (app.py)
### Overview
The `app.py` script is a Flask-based application that fetches jokes from an external API and stores them in an SQLite database (`jokes.db`). It provides endpoints to retrieve and display jokes.
