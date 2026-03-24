# E-commerce Product Scraper

A Python-based tool for extracting product data from e-commerce websites using two different approaches: browser automation and structured data extraction.

---

## Overview

This project provides a flexible way to collect product information such as names, prices, and URLs from online stores.

It supports two scraping strategies:

- **Selenium-based scraping** for extracting visible data from web pages  
- **Shopify-specific scraping** using sitemap discovery and product JSON endpoints for full-store extraction  

The goal is to handle different types of e-commerce websites by using the most reliable method for each case.

---

## Features

- Extracts product names, prices, and URLs  
- Supports dynamic page scraping using Selenium  
- Supports full-store scraping for Shopify websites  
- Handles different website structures with separate strategies  
- Avoids reliance on UI scraping when structured data is available  
- Outputs clean, structured CSV files  

---

## Project Structure

```
ecommerce-product-scraper/
├── selenium_scraper.py
├── shopify_scraper.py
├── requirements.txt
└── README.md
```

---

## Installation

Install dependencies:

```bash
py -3.13 -m pip install -r requirements.txt
```

---

## Usage

### Selenium Scraper

Use this for scraping visible products from a single page.

```bash
py -3.13 selenium_scraper.py
```

Enter a page URL when prompted.

Example:

```text
https://eddiesstudios.com/
```

Output:

```
products.csv
```

---

### Shopify Scraper

Use this for extracting all products from a Shopify store.

```bash
py -3.13 shopify_scraper.py
```

Enter the store URL when prompted.

Example:

```text
https://eddiesstudios.com
```

Output:

```
shopify_products.csv
```

---

## Output

### Selenium Scraper Output

- Product Name  
- Price  
- Product URL  

Saved in:

```
products.csv
```

---

### Shopify Scraper Output

- Product Title  
- Variant Title  
- Price  
- Compare At Price  
- Vendor  
- Product Type  
- Handle  
- Product URL  

Saved in:

```
shopify_products.csv
```

---

## How It Works

### Selenium Scraper

1. Opens the target page in a browser  
2. Locates product elements  
3. Extracts visible product data  
4. Saves results to CSV  

---

### Shopify Scraper

1. Reads the store sitemap  
2. Collects all product URLs  
3. Extracts product handles  
4. Fetches product data using Shopify JSON endpoints  
5. Saves structured data to CSV  

---

## Use Cases

- Product data collection  
- Competitor monitoring  
- Catalog analysis  
- Price tracking  
- E-commerce research  

---

## Tech Stack

- Python  
- Selenium  
- Requests  
- CSV processing  
- XML parsing  

---

## Notes

- The Shopify scraper is designed specifically for Shopify stores  
- The Selenium scraper depends on visible page structure and may require selector adjustments for different websites  
- Non-Shopify websites may require custom scraping logic  
