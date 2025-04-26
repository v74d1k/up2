import sqlite3

class DrinkDB:
    def __init__(self):
        self.conn = sqlite3.connect("drinks.db")
        self.cur = self.conn.cursor()
        self.cur.execute('''CREATE TABLE IF NOT EXISTS drinks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            strength REAL,
            stock REAL
        )''')
        self.cur.execute('''CREATE TABLE IF NOT EXISTS cocktails (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            price REAL
        )''')
        self.cur.execute('''CREATE TABLE IF NOT EXISTS cocktail_ingredients (
            cocktail_id INTEGER,
            drink_id INTEGER,
            amount REAL,
            FOREIGN KEY(cocktail_id) REFERENCES cocktails(id),
            FOREIGN KEY(drink_id) REFERENCES drinks(id)
        )''')
        self.conn.commit()

    def add_drink(self, name, strength, stock):
        self.cur.execute("INSERT INTO drinks (name, strength, stock) VALUES (?, ?, ?)", (name, strength, stock))
        self.conn.commit()

    def add_cocktail(self, name, price, ingredients):
        self.cur.execute("INSERT INTO cocktails (name, price) VALUES (?, ?)", (name, price))
        cid = self.cur.lastrowid
        for did, amt in ingredients.items():
            self.cur.execute("INSERT INTO cocktail_ingredients (cocktail_id, drink_id, amount) VALUES (?, ?, ?)", (cid, did, amt))
        self.conn.commit()

    def get_drinks(self):
        self.cur.execute("SELECT * FROM drinks")
        return self.cur.fetchall()

    def get_cocktails(self):
        self.cur.execute("SELECT * FROM cocktails")
        return self.cur.fetchall()

    def get_ingredients(self, cocktail_id):
        self.cur.execute('''SELECT d.name, d.strength, ci.amount FROM cocktail_ingredients ci
                            JOIN drinks d ON ci.drink_id = d.id WHERE ci.cocktail_id=?''', (cocktail_id,))
        return self.cur.fetchall()

    def calc_strength(self, cocktail_id):
        ingr = self.get_ingredients(cocktail_id)
        total = sum(a for _, _, a in ingr)
        if total == 0:
            return 0
        s = sum(strength * amount for _, strength, amount in ingr)
        return s / total

    def sell_drink(self, drink_id, amount):
        self.cur.execute("SELECT stock FROM drinks WHERE id=?", (drink_id,))
        stock = self.cur.fetchone()
        if stock and stock[0] >= amount:
            self.cur.execute("UPDATE drinks SET stock = stock - ? WHERE id=?", (amount, drink_id))
            self.conn.commit()
            return True
        return False

    def sell_cocktail(self, cocktail_id):
        ingr = self.get_ingredients(cocktail_id)
        for name, strength, amount in ingr:
            self.cur.execute("SELECT stock FROM drinks WHERE name=?", (name,))
            stock = self.cur.fetchone()
            if not stock or stock[0] < amount:
                return False
        for name, strength, amount in ingr:
            self.cur.execute("UPDATE drinks SET stock = stock - ? WHERE name=?", (amount, name))
        self.conn.commit()
        return True

    def restock(self, drink_id, amount):
        self.cur.execute("UPDATE drinks SET stock = stock + ? WHERE id=?", (amount, drink_id))
        self.conn.commit()

    def close(self):
        self.conn.close()

def main():
    db = DrinkDB()
    while True:
        print("1. Добавить напиток")
        print("2. Добавить коктейль")
        print("3. Показать напитки")
        print("4. Показать коктейли")
        print("5. Продать напиток")
        print("6. Продать коктейль")
        print("7. Пополнить запас")
        print("0. Выход")
        c = input("Выбор: ")
        if c == "1":
            n = input("Название: ")
            s = float(input("Крепость: "))
            st = float(input("Запас: "))
            db.add_drink(n, s, st)
            print("Добавлено")
        elif c == "2":
            n = input("Название коктейля: ")
            p = float(input("Цена: "))
            ingr = {}
            print("Ввод ингредиентов (id и количество), пустая строка - конец")
            while True:
                line = input()
                if not line:
                    break
                try:
                    did, amt = line.split()
                    ingr[int(did)] = float(amt)
                except:
                    print("Ошибка")
            db.add_cocktail(n, p, ingr)
            print("Коктейль добавлен")
        elif c == "3":
            for d in db.get_drinks():
                print(d)
        elif c == "4":
            for ckt in db.get_cocktails():
                strength = db.calc_strength(ckt[0])
                print(ckt[0], ckt[1], ckt[2], f"Крепость: {strength:.2f}%")
        elif c == "5":
            did = int(input("ID напитка: "))
            amt = float(input("Количество: "))
            if db.sell_drink(did, amt):
                print("Продано")
            else:
                print("Нет на складе")
        elif c == "6":
            cid = int(input("ID коктейля: "))
            if db.sell_cocktail(cid):
                print("Продано")
            else:
                print("Не хватает ингредиентов")
        elif c == "7":
            did = int(input("ID напитка: "))
            amt = float(input("Количество: "))
            db.restock(did, amt)
            print("Пополнено")
        elif c == "0":
            db.close()
            break
        else:
            print("Ошибка")

if __name__ == "__main__":
    main()
