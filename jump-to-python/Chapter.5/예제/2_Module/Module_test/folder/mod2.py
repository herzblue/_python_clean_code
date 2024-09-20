# mod2.py
PI = 3.141592

# class Math:
#     def init(self):
#         self.r = 0
#     def circle_area(self, r):
#         r = self.r
#         return PI * (r ** 2)
    
class Math:
    def __init__(self):
        self.r = 0
        self.a = 0
        self.b = 0
    def solv(self, r):
        return PI * (r ** 2)
    def rectangle(self, a, b):
        return a * b
def add(a, b):
    return a+b

if __name__ == "__main__": 
    math1 = Math()
    print(math1.rectangle(2, 4))
