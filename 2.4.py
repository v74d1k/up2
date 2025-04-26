class Counter:
    def __init__(self, value=0):
        self.value = value

    def inc(self):
        self.value += 1

    def dec(self):
        self.value -= 1

    def show(self):
        print(self.value)

c = Counter()
c.inc()
c.inc()
c.dec()
c.show()
