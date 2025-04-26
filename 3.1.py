class Worker:
    def __init__(self, name, surname, rate, days):
        self.name = name
        self.surname = surname
        self.rate = rate
        self.days = days

    def GetSalary(self):
        print(self.rate * self.days)

w = Worker("Иван", "Иванов", 1000, 15)
w.GetSalary()
