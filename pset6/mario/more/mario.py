from cs50 import get_int


# declare height variable
height = 0

# get hieght from user enforcing it be between 1 and 8
while height < 1 or height > 8:
    height = get_int("how tall?\n")

# create dummy variable for height to manipulate
h = height

# loop through height number of times to create pyramid
for i in range(1, height+1):
    # print spaces
    print(" " * (h - 1), end="")

    # reduce h to reduce spaces to print
    h -= 1

    # print first block
    print("#" * i, end="")

    # print space divider
    print("  ", end="")

    # print second set of blocks
    print("#" * i)

# can be done neater with recurssion
