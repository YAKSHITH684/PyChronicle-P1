# demo2.py - Parse items from a plain text file + switch sessions (50 lines)

RAW_DATA = """session_a
3.5,2
10,1
session_b
7.25,3
2.0,5
"""


def parse_sessions(text):
    """Parse plain text into a dict of sessions -> item lists.
    Lines with no comma start a new session; 'price,qty' lines add items."""
    sessions = {}
    current = None
    for line in text.strip().splitlines():
        line = line.strip()
        if "," not in line:
            current = line
            sessions[current] = []
        else:
            price, qty = line.split(",")
            sessions[current].append({"price": float(price), "qty": int(qty)})
    return sessions


def total_price(items):
    total = 0
    for item in items:
        total += item["price"] * item["qty"]
    return total


def summarize_session(name, items, tax_rate=0.08):
    subtotal = total_price(items)
    tax = subtotal * tax_rate
    return {"session": name, "subtotal": round(subtotal, 2),
            "tax": round(tax, 2), "total": round(subtotal + tax, 2)}


def main():
    sessions = parse_sessions(RAW_DATA)
    active = "session_a"
    print(f"Active session: {active}")
    print(summarize_session(active, sessions[active]))

    active = "session_b"
    print(f"\nSwitched to session: {active}")
    print(summarize_session(active, sessions[active]))


if __name__ == "__main__":
    main()