import csv
import xml.etree.ElementTree as ET
from urllib.parse import urlparse
import requests


def normalize_store_url(url: str) -> str:
    url = url.strip().rstrip("/")
    if not url.startswith("http://") and not url.startswith("https://"):
        url = "https://" + url
    return url


def get_product_urls_from_sitemap(store_url: str) -> list[str]:
    sitemap_url = f"{store_url}/sitemap.xml"
    response = requests.get(sitemap_url, timeout=20)
    response.raise_for_status()

    root = ET.fromstring(response.text)
    ns = {"sm": "http://www.sitemaps.org/schemas/sitemap/0.9"}

    product_urls = []
    child_sitemaps = root.findall(".//sm:sitemap/sm:loc", ns)

    if child_sitemaps:
        for sitemap in child_sitemaps:
            child_url = sitemap.text.strip()

            if "product" in child_url.lower():
                child_response = requests.get(child_url, timeout=20)
                child_response.raise_for_status()

                child_root = ET.fromstring(child_response.text)
                urls = child_root.findall(".//sm:url/sm:loc", ns)

                for url_el in urls:
                    product_url = url_el.text.strip()
                    if "/products/" in product_url:
                        product_urls.append(product_url)
    else:
        urls = root.findall(".//sm:url/sm:loc", ns)
        for url_el in urls:
            product_url = url_el.text.strip()
            if "/products/" in product_url:
                product_urls.append(product_url)

    return sorted(set(product_urls))


def get_handle_from_product_url(product_url: str) -> str:
    parsed = urlparse(product_url)
    path_parts = [part for part in parsed.path.split("/") if part]
    if "products" in path_parts:
        idx = path_parts.index("products")
        if idx + 1 < len(path_parts):
            return path_parts[idx + 1]
    return ""


def money_from_cents(value) -> str:
    if value is None:
        return ""
    return f"{value / 100:.2f}"


def fetch_product_json(store_url: str, handle: str) -> dict:
    product_json_url = f"{store_url}/products/{handle}.js"
    response = requests.get(product_json_url, timeout=20)
    response.raise_for_status()
    return response.json()


def extract_product_rows(store_url: str, product_url: str) -> list[list[str]]:
    handle = get_handle_from_product_url(product_url)
    if not handle:
        return []

    try:
        product = fetch_product_json(store_url, handle)
    except Exception:
        return []

    title = product.get("title", "")
    vendor = product.get("vendor", "")
    product_type = product.get("type", "")
    variants = product.get("variants", [])

    rows = []

    if not variants:
        rows.append([
            title,
            "",
            "",
            "",
            vendor,
            product_type,
            handle,
            product_url
        ])
        return rows

    for variant in variants:
        variant_title = variant.get("title", "")
        price = money_from_cents(variant.get("price"))
        compare_at_price = money_from_cents(variant.get("compare_at_price"))

        rows.append([
            title,
            variant_title,
            price,
            compare_at_price,
            vendor,
            product_type,
            handle,
            product_url
        ])

    return rows


def save_to_csv(rows: list[list[str]], filename: str = "shopify_products.csv") -> None:
    with open(filename, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow([
            "Product Title",
            "Variant Title",
            "Price",
            "Compare At Price",
            "Vendor",
            "Product Type",
            "Handle",
            "Product URL"
        ])
        writer.writerows(rows)


def main():
    store_url = input("Enter Shopify store URL: ").strip()
    store_url = normalize_store_url(store_url)

    print("Reading sitemap...")
    product_urls = get_product_urls_from_sitemap(store_url)
    print(f"Found {len(product_urls)} product URLs")

    all_rows = []

    for i, product_url in enumerate(product_urls, start=1):
        print(f"[{i}/{len(product_urls)}] Fetching {product_url}")
        rows = extract_product_rows(store_url, product_url)
        all_rows.extend(rows)

    save_to_csv(all_rows)
    print(f"Done. Saved {len(all_rows)} rows to shopify_products.csv")


if __name__ == "__main__":
    main()