from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import csv
import re


def clean_text(text: str) -> str:
    return " ".join(text.split()).strip()


def extract_shopify_price(text: str) -> str:
    text = clean_text(text)

    sale_patterns = [
        r"Sale price\s*(LE\s*[\d,.]+)",
        r"Sale price\s*([\d,.]+\s*EGP)",
        r"Regular price\s*~~[\d,.]+\s*EGP~~\s*Sale price\s*([\d,.]+\s*EGP)",
        r"Regular price\s*~~LE\s*[\d,.]+~~\s*Sale price\s*(LE\s*[\d,.]+)",
    ]

    regular_patterns = [
        r"Regular price\s*(LE\s*[\d,.]+)",
        r"Regular price\s*([\d,.]+\s*EGP)",
    ]

    for pattern in sale_patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            return clean_text(match.group(1))

    for pattern in regular_patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            return clean_text(match.group(1))

    return ""


def scrape_visible_products(url: str) -> list[list[str]]:
    driver = webdriver.Chrome()

    try:
        driver.get(url)
        wait = WebDriverWait(driver, 10)

        product_links = wait.until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "a[href*='/products/']"))
        )

        data = []
        seen = set()

        for link in product_links:
            try:
                name = clean_text(link.text)
                href = link.get_attribute("href")

                if not name or not href or "/products/" not in href:
                    continue

                price = ""

                for level in range(1, 8):
                    try:
                        container = link.find_element(
                            By.XPATH,
                            f"./ancestor::*[self::div or self::li][{level}]"
                        )
                        container_text = clean_text(container.text)
                        price = extract_shopify_price(container_text)
                        if price:
                            break
                    except Exception:
                        continue

                key = (name, price, href)
                if key not in seen:
                    seen.add(key)
                    data.append([name, price, href])

            except Exception:
                continue

        return data

    finally:
        driver.quit()


def save_to_csv(data: list[list[str]], filename: str = "products.csv") -> None:
    with open(filename, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["Product Name", "Price", "Product URL"])
        writer.writerows(data)


def main():
    url = input("Enter page URL: ").strip()
    data = scrape_visible_products(url)
    save_to_csv(data)
    print(f"Done. Saved {len(data)} rows to products.csv")


if __name__ == "__main__":
    main()