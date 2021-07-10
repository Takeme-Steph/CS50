from cs50 import get_string

# get crdit card details from user
card = get_string("Please input credit card number\n")

# get card number lenght
cardlen = len(card)

# loop through each number in the card
cardsum = 0
for i in range(cardlen):
    number = int(card[cardlen - (i+1)])
    
    # implement part of the formula
    # multiply every other number by 2 starting from the second to the last digit
    if i % 2 != 0:
        number *= 2
        numlen = len(str(number))
        # seperate the multiplies result into individual digits and add to the cardsum
        for j in range(numlen):
            cardsum += int(str(number)[j])
            
    # add numbers not multiplied to card sum
    else:
        cardsum += number

# check if last digit of cardsum is zero
if cardsum % 10 == 0:
    check = 'y'
else:
    check = 'n'

# get the first 2 card numbers
first = int(card[0])
second = int(card[1])

# check the type of card
if check == 'y':
    if cardlen == 15 and first == 3 and second in [4, 7]:
        print("AMEX")
    elif cardlen == 16 and first == 5 and second in [1, 2, 3, 4, 5]:
        print("MASTERCARD")
    elif cardlen in [13, 16] and first == 4:
        print("VISA")
    else:
        print("INVALID")
    
else:
    print("INVALID")
    