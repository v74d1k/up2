class Calculation:
    def __init__(self):
        self.calculationLine = ""

    def SetCalculationLine(self, line):
        self.calculationLine = line

    def SetLastSymbolCalculationLine(self, symbol):
        self.calculationLine = self.calculationLine + symbol

    def GetCalculationLine(self):
        print(self.calculationLine)

    def GetLastSymbol(self):
        if len(self.calculationLine) > 0:
            print(self.calculationLine[-1])
        else:
            print("Пустая строка")

    def DeleteLastSymbol(self):
        self.calculationLine = self.calculationLine[:-1]

c = Calculation()
c.SetCalculationLine("123+45")
c.GetCalculationLine()
c.SetLastSymbolCalculationLine("6")
c.GetCalculationLine()
c.GetLastSymbol()
c.DeleteLastSymbol()
c.GetCalculationLine()
