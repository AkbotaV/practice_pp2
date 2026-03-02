import json
import re

with open("raw.txt",encoding="utf-8") as f:
  text=f.read()

dt=re.search(r"(\d{2}\.\d{2}\.\d{4})\s(\d{2}:\d{2}:\d{2})",text)
date=dt.group(1)
time=dt.group(2)

price=re.findall(r"Стоимость\n([\d\s]+,\d{2})",text)

clean_price=[]
for p in price:
  p=p.replace(" ","")
  p=p.replace(",",".")
  clean_price.append(float(p))

total=sum(clean_price)

paym=re.search(r"(Банковская карта|Наличные)", text)

prodnames=re.findall(r"\d+\.\n(.+)",text)

products = []
for name, price in zip(prodnames, clean_price):
    products.append({
        "name": name,
        "price": price
    })

receipt = {
    "date": date,
    "time": time,
    "payment_method": paym.group(1),
    "total": total,
    "products": products
}

with open("receipt_output.json", "w", encoding="utf-8") as ff:
    json.dump(receipt, ff, ensure_ascii=False, indent=2)
