import psutil
import sqlite3
import datetime

class MonitorDB:
    def __init__(self):
        self.conn = sqlite3.connect("../PythonProject/monitor.db")
        self.cur = self.conn.cursor()
        self.cur.execute('''CREATE TABLE IF NOT EXISTS data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            time TEXT,
            cpu REAL,
            ram REAL,
            disk REAL
        )''')
        self.conn.commit()

    def add(self, cpu, ram, disk):
        t = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.cur.execute("INSERT INTO data VALUES (NULL, ?, ?, ?, ?)", (t, cpu, ram, disk))
        self.conn.commit()

    def get_all(self):
        self.cur.execute("SELECT * FROM data")
        return self.cur.fetchall()

    def close(self):
        self.conn.close()

def get_stats():
    cpu = psutil.cpu_percent(interval=1)
    ram = psutil.virtual_memory().percent
    disk = psutil.disk_usage('/').percent
    return cpu, ram, disk

def main():
    db = MonitorDB()
    while True:
        print("1. Сохранить мониторинг")
        print("2. Показать все данные")
        print("0. Выход")
        c = input("Выбор: ")
        if c == "1":
            cpu, ram, disk = get_stats()
            db.add(cpu, ram, disk)
            print("Сохранено:", cpu, ram, disk)
        elif c == "2":
            for row in db.get_all():
                print(row)
        elif c == "0":
            db.close()
            break
        else:
            print("Ошибка")

if __name__ == "__main__":
    main()
