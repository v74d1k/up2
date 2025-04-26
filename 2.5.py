class MyClass:
    def __init__(self, a='x', b='y'):
        self.a = a
        self.b = b

    def __del__(self):
        print("Объект удален")

obj1 = MyClass('test1', 'test2')
obj2 = MyClass()
del obj1
del obj2
