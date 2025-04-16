# common iterator example 

print("printing numbers 0 - 9")
for i in range(0, 10): 
    print(i)

# iteration is controlled externally 
# general iterator pattern
# while not iterator.done(): 
#     print(iterator.next())

# # iteration controlled internally



lst = [1, 2, 3, 4, 5]
for i, x in enumerate(lst):
    print(f"i, {i}")
    if x == 2:
        lst.remove(2)
    print(x)