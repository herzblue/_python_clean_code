# import mod1
# result = mod1.add(3, 4)
# print (result)

# import mod1
# from mod1 import add
# result = add(3, 4)
# print (result)

# from mod1 import *
# result = add(3, 4)
# print (result)

# import mod1 
# name = mod1.__name__

# print(f"__name__ : {name}")

import folder.mod2
mod2 = folder.mod2
print(mod2.PI)

math2 = mod2.Math()
# print(math1.solv(1))
print(math2.solv(2))
print(math2.rectangle(2, 4))