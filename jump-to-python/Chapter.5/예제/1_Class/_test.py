# calculator3.py
class Calculator:
    def __init__(self):
        self.result = 0
        self.first = 0
        self.second = 0
        
    def setmeta(self, first, second):
        self.first = first
        self.second = second
        return self.first, self.second
    def add(self):
        result = self.first + self.second
        return result
    def sub(self):
        result = self.first - self.second
        return self.result
    def mul(self):
        result = self.first * self.second
        return self.result
    def div(self):
        result = self.first / self.second
        return self.result
        
cal1 = Calculator()


cal1.setmeta(1, 2)
print(f"a of cal1: {cal1.first}\nb of cal1: {cal1.first}")
cal1.setmeta(3, 4)
print(f"a of cal1: {cal1.first}\nb of cal1: {cal1.first}")

result = cal1.add()
print(result)

cal2 = Calculator()
result2 = cal2.add()
print(f"ca2 result: {result2}")

# print(cal1.add(3))
# print(cal1.add(4))
# # print(cal2.add(3))
# # print(cal2.add(7))
# print(cal1.sub(3))

class Calculator_upgrage(Calculator):
    def pow(self, first, second):
        result = self.first ** self.second
        return result
    
cal3 = Calculator_upgrage()
cal3.setmeta(2, 3)
result3 = cal3.pow(2, 3)
print(f"result3: {result3}")

class Calculator_safe(Calculator):
    def div(self):
        if self.second == 0:# 나누는 값이 0인 경우 0을 리턴하도록 수정
            return 0
        else:
            return self.first / self.second

cal4 = Calculator_safe()
cal4.setmeta(4, 0)
result4 = cal4.div()
print(f"result4: {result4}")