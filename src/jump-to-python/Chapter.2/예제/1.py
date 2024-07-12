# 정수형
a = 123
a = -178
a = 0

# 실수형
a = 1.2
a = -3.45
a = 4.24E10
a = 4.24e-10

# 8진수
a = 0o177

# 16진수
a = 0x8ff
a = 0xABC

# 복소수
a = 1 + 2j
b = 3 - 4J

a.real # 1.0
a.imag # 2.0
a.conjugate() # (1 - 2j) 켤레 복소수 리턴
abs(a) # 2.2360679664997898 복소수의 절댓값 리턴

# 사칙 연산
a = 3
b = 4
a + b # 7
a * b # 12
a / b # 0.75

# x의 y제곱을 나타내는 ** 연산자
a = 3
b = 4
a ** b # 81

# 나눗셈후 나머지를 반환하는 % 연산
7 % 3 # 1
3 % 7 # 3

# 나눗셈 후 소수점 아랫자리를 버리는 // 연산자
7 / 4 # 1.75
7 // 4 # 1
