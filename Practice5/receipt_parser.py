import re
import json

# 1 Extract all prices from the receipt
def normalize_price(price_str):
    price_str = price_str.replace(" ", "").replace(",", ".")
    return float(price_str)

with open("raw.txt", "r", encoding="utf-8") as f:
    text = f.read()

# 2 Find all product names
item_pattern = re.compile(r"\d+\.\s*\n(.+?)\n\d+,\d{3}\s*x\s*[\d\s]+,\d{2}\n([\d\s]+,\d{2})", re.MULTILINE)
items = []

for match in item_pattern.finditer(text):
    name = match.group(1).strip()
    price = normalize_price(match.group(2))
    items.append({
        "name": name,
        "price": price
    })

# 3 Calculate total amount
total_match = re.search(r"ИТОГО:\s*\n([\d\s]+,\d{2})", text)
total = normalize_price(total_match.group(1)) if total_match else None

# 4 Extract date and time information
datetime_match = re.search(r"Время:\s*(\d{2}\.\d{2}\.\d{4})\s*(\d{2}:\d{2}:\d{2})", text)
date = datetime_match.group(1) if datetime_match else None
time = datetime_match.group(2) if datetime_match else None

# 5 Find payment method
payment_match = re.search(r"(Банковская карта|Наличные)", text)
payment_method = payment_match.group(1) if payment_match else None

# 6 Structured output (JSON or formatted text)
result = {
    "date": date,
    "time": time,
    "payment_method": payment_method,
    "total": total,
    "items": items
}
print(json.dumps(result, ensure_ascii=False, indent=4))