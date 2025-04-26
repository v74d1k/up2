class Train:
    def __init__(self, destination, number, time):
        self.destination = destination
        self.number = number
        self.time = time

    def info(self):
        print(f"{self.number}: {self.destination}, {self.time}")

trains = [
    Train("Москва", 1, "10:00"),
    Train("Казань", 2, "12:00"),
    Train("Сочи", 3, "15:00")
]

num = int(input("Введите номер поезда: "))
for t in trains:
    if t.number == num:
        t.info()
