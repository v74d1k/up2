import sqlite3

class Student:
    def __init__(self, name, surname, patronymic, group, grades):
        self.name = name
        self.surname = surname
        self.patronymic = patronymic
        self.group = group
        self.grades = grades

    def average(self):
        return sum(self.grades) / len(self.grades)

class StudentDB:
    def __init__(self):
        self.conn = sqlite3.connect("../PythonProject/students.db")
        self.cur = self.conn.cursor()
        self.cur.execute('''CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            surname TEXT,
            patronymic TEXT,
            group_name TEXT,
            grade1 INTEGER,
            grade2 INTEGER,
            grade3 INTEGER,
            grade4 INTEGER
        )''')
        self.conn.commit()

    def add(self, student):
        self.cur.execute("INSERT INTO students VALUES (NULL,?,?,?,?,?,?,?,?)",
                         (student.name, student.surname, student.patronymic, student.group,
                          student.grades[0], student.grades[1], student.grades[2], student.grades[3]))
        self.conn.commit()

    def get_all(self):
        self.cur.execute("SELECT * FROM students")
        return self.cur.fetchall()

    def get(self, id):
        self.cur.execute("SELECT * FROM students WHERE id=?", (id,))
        return self.cur.fetchone()

    def update(self, id, student):
        self.cur.execute('''UPDATE students SET name=?, surname=?, patronymic=?, group_name=?, 
            grade1=?, grade2=?, grade3=?, grade4=? WHERE id=?''',
            (student.name, student.surname, student.patronymic, student.group,
             student.grades[0], student.grades[1], student.grades[2], student.grades[3], id))
        self.conn.commit()

    def delete(self, id):
        self.cur.execute("DELETE FROM students WHERE id=?", (id,))
        self.conn.commit()

    def avg_by_group(self, group):
        self.cur.execute("SELECT grade1, grade2, grade3, grade4 FROM students WHERE group_name=?", (group,))
        rows = self.cur.fetchall()
        if not rows:
            return None
        total = 0
        count = 0
        for r in rows:
            total += sum(r)
            count += 4
        return total / count

    def close(self):
        self.conn.close()

def main():
    db = StudentDB()
    while True:
        print("1. Добавить студента")
        print("2. Показать всех")
        print("3. Показать студента")
        print("4. Редактировать студента")
        print("5. Удалить студента")
        print("6. Средний балл по группе")
        print("0. Выход")
        choice = input("Выбор: ")
        if choice == "1":
            n = input("Имя: ")
            s = input("Фамилия: ")
            p = input("Отчество: ")
            g = input("Группа: ")
            grades = []
            for i in range(4):
                grades.append(int(input(f"Оценка {i+1}: ")))
            st = Student(n, s, p, g, grades)
            db.add(st)
            print("Добавлено")
        elif choice == "2":
            all_st = db.get_all()
            for st in all_st:
                print(st)
        elif choice == "3":
            id = int(input("ID студента: "))
            st = db.get(id)
            if st:
                grades = st[5:9]
                avg = sum(grades)/4
                print(st, "Средний балл:", round(avg, 2))
            else:
                print("Нет такого студента")
        elif choice == "4":
            id = int(input("ID для редактирования: "))
            st = db.get(id)
            if st:
                n = input("Новое имя: ")
                s = input("Новая фамилия: ")
                p = input("Новое отчество: ")
                g = input("Новая группа: ")
                grades = []
                for i in range(4):
                    grades.append(int(input(f"Новая оценка {i+1}: ")))
                new_st = Student(n, s, p, g, grades)
                db.update(id, new_st)
                print("Обновлено")
            else:
                print("Не найден")
        elif choice == "5":
            id = int(input("ID для удаления: "))
            db.delete(id)
            print("Удалено")
        elif choice == "6":
            g = input("Группа: ")
            avg = db.avg_by_group(g)
            if avg:
                print("Средний балл группы:", round(avg, 2))
            else:
                print("Группа не найдена или нет студентов")
        elif choice == "0":
            db.close()
            break
        else:
            print("Ошибка ввода")

if __name__ == "__main__":
    main()
