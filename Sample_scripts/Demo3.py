# demo3.py - Parse a file, switch sessions, adjust appearance (75 lines)

DATA_FILE = "sessions_data.txt"
RAW_TEXT = """session_a
3.5,2
10,1
session_b
7.25,3
2.0,5
"""


class AppearanceSettings:
    def __init__(self, currency="$", decimals=2, theme="light"):
        self.currency, self.decimals, self.theme = currency, decimals, theme

    def format_amount(self, amount):
        return f"{self.currency}{amount:.{self.decimals}f}"

    def describe(self):
        return f"[theme={self.theme}, currency={self.currency}]"


class SessionManager:
    def __init__(self, sessions):
        self.sessions = sessions
        self.active = next(iter(sessions))

    def switch(self, name):
        if name not in self.sessions:
            raise ValueError(f"Unknown session: {name}")
        self.active = name

    def items(self):
        return self.sessions[self.active]


def write_data_file(path, text):
    with open(path, "w") as f:
        f.write(text)


def parse_file(path):
    """Read plain text lines: a line with no comma starts a session,
    'price,qty' lines add items to the current session."""
    sessions = {}
    current = None
    with open(path, "r") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
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


def summarize(items, tax_rate=0.08):
    subtotal = total_price(items)
    tax = subtotal * tax_rate
    return subtotal, tax, subtotal + tax


def show(manager, appearance):
    print(f"Active session: {manager.active}")
    subtotal, tax, total = summarize(manager.items())
    print(f"  Subtotal: {appearance.format_amount(subtotal)}")
    print(f"  Tax:      {appearance.format_amount(tax)}")
    print(f"  Total:    {appearance.format_amount(total)}")


def main():
    write_data_file(DATA_FILE, RAW_TEXT)
    sessions = parse_file(DATA_FILE)
    manager = SessionManager(sessions)
    appearance = AppearanceSettings(theme="dark")
    print(f"Appearance: {appearance.describe()}")
    show(manager, appearance)
    manager.switch("session_b")
    appearance.currency = "€"
    print(f"\nSwitched to session: {manager.active}")
    show(manager, appearance)


if __name__ == "__main__":
    main()# Demo 3: a longer flow for stepping through execution.
