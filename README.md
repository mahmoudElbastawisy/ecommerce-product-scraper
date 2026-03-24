# E-commerce Product Scraper

A Python-based product scraping toolkit for collecting product data from e-commerce websites using two different approaches:

- **Selenium-based scraping** for visible product data on dynamic pages
- **Shopify-specific scraping** using sitemap discovery and Shopify product JSON endpoints for full-store extraction

## Why I built this
This project was built to simulate real-world competitor monitoring and product analysis workflows. The goal was to reduce manual product tracking by automating the extraction of product names, pricing, product URLs, and variant data across e-commerce stores.

## Project Structure
```text
ecommerce-product-scraper/
│
├── selenium_scraper.py
├── shopify_scraper.py
├── requirements.txt
└── README.md