from cs50 import get_int

while True:
    height = get_int("Pyramid Height: ")  # ask user for height
    if height > 0 and height <= 8:  # height has to be between 1 and 8 inclusive
        break

for i in range(height):
    spaces = height - i - 1  # print spaces
    bricks = i + 1  # print bricks
    for k in range(spaces):
        print(" ", end="")
    for j in range(bricks):
        print("#", end="")
    print()
