class Numbers:
    def __init__(self, a, b):
        self.a = a
        self.b = b

    def show(self):
        print(self.a, self.b)

    def change(self, a, b):
        self.a = a
        self.b = b

    def summa(self):
        print(self.a + self.b)

    def max_value(self):
        print(max(self.a, self.b))

n = Numbers(3, 7)
n.show()
n.change(10, 5)
n.show()
n.summa()
n.max_value()
