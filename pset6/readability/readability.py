from cs50 import get_string


# get user input
text = get_string("Text: \n")

# set counts
letters = 0
for c in text:
    if c.isalpha():
        letters += 1
        
words = 1  # +1 for the final period in the text
words += text.count(" ") 

sentences = text.count(".")
sentences += text.count("?")
sentences += text.count("!")

# calc average letters per words
avglw = (100 / words) * letters
# calc average sentences per words
avgsw = (100 / words) * sentences

# calc index
index = 0.0588 * avglw - 0.296 * avgsw - 15.8

# print results
if index >= 16:
    print("Grade 16+")
    
elif index < 1:
    print("Before Grade 1")

else:
    print("Grade", format(index, ".0f"))
