class Student:
    def __init__(self, last_name, birth_date, group_number, grades):
        self.last_name = last_name
        self.birth_date = birth_date
        self.group_number = group_number
        self.grades = grades

    def change_last_name(self, new_name):
        self.last_name = new_name

    def change_birth_date(self, new_date):
        self.birth_date = new_date

    def change_group_number(self, new_group):
        self.group_number = new_group

    def print_info(self):
        print("Фамилия:", self.last_name)
        print("Дата рождения:", self.birth_date)
        print("Номер группы:", self.group_number)
        print("Оценки:", self.grades)

# Создаем студентов
students = [
    Student("Иванов", "01.01.2000", "101", [5,4,3,4,5]),
    Student("Петров", "02.02.2001", "102", [4,4,4,5,5]),
    Student("Сидоров", "03.03.2002", "103", [3,3,4,4,4])
]

students[0].change_last_name("Иванов-Смирнов")
students[0].change_birth_date("05.01.2000")
students[0].change_group_number("201")

last_name_input = input("Введите фамилию студента: ")
birth_date_input = input("Введите дату рождения студента (дд.мм.гггг): ")

found = False
for student in students:
    if student.last_name == last_name_input and student.birth_date == birth_date_input:
        print("\nИнформация о студенте:")
        student.print_info()
        found = True
        break

if not found:
    print("Студент не найден.")
