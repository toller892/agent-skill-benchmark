"""Calculator app - contains bugs, security issues, and code smells for skill testing."""

import sqlite3
from config import API_KEY


class Calculator:
    """A simple calculator with some problems."""

    def __init__(self):
        self.history = []
        self.db_path = "calc.db"

    def add(self, a, b):
        result = a + b
        self.history.append(f"add({a}, {b}) = {result}")
        return result

    def subtract(self, a, b):
        result = a - b
        self.history.append(f"subtract({a}, {b}) = {result}")
        return result

    def divide(self, a, b):
        # BUG: no zero-division check
        result = a / b
        self.history.append(f"divide({a}, {b}) = {result}")
        return result

    # NOTE: multiply() is missing - needs to be implemented with TDD

    def search_user(self, username):
        """SECURITY: SQL injection vulnerability."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        query = "SELECT * FROM users WHERE name = '" + username + "'"
        cursor.execute(query)
        result = cursor.fetchall()
        conn.close()
        return result

    def calculate_expression(self, expr):
        """SECURITY: eval() on user input."""
        result = eval(expr)
        self.history.append(f"expr({expr}) = {result}")
        return result

    def authenticate(self):
        """SECURITY: hardcoded credential usage."""
        if API_KEY == "sk-1234567890abcdef":
            return True
        return False


def main():
    calc = Calculator()
    print("2 + 3 =", calc.add(2, 3))
    print("10 / 2 =", calc.divide(10, 2))
    print("10 / 0 =", calc.divide(10, 0))  # This will crash


if __name__ == "__main__":
    main()
