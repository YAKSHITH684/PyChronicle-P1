def total_price(items):
    total = 0
    for item in items:
        total += item["price"] * item["qty"]
    return total


items = [
    {"price": 3.5, "qty": 2},
    {"price": 10, "qty": 1},
]

subtotal = total_price(items)
tax_rate: float = 0.08
tax = subtotal * tax_rate
grand_total = subtotal + tax

print(f"Total: {grand_total:.2f}")