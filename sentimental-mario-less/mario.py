from cs50 import get_int

# Ask for suitable int for height and re-prompt
while True:
    height = get_int("Height: ")
    if height > 0 and height < 9:
        break

# Print pyramids
for i in range(height):
    for j in range(height):
        if i + j < height - 1:
            print(" ", end="")
        else:
            print("#", end="")
    print()
