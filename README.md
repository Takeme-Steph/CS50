My problem sets and projects from taking the cs50 classes.

# Organized - Final Project
  Organized is a planning & budgeting web app. It has 3 levels **Event** > **Umbrellas** > **Todos**. You can use it to make todo lists, plan budgeted events etc.
  It lets you know when you are under or overbudget, you can also assign tasks and todo's to other people *(this is function is still in a very basic form and is yet to be           properly expended upon)*
  It has a wide range of uses from budgeting monthly expenses to planing big events & projects or just a simple todo list.
  Made with python(Flask) and sqlite, html, css, javascript, jquery. Please read it's readme file for more info and instal the packages in the requirements file befor running.

# Finance- 
  it's a basic stock exchange app made with python(Flask) and sqlite, html, css, javascript, jquery and Ajax. Live quotes from IEX and Payment hosted by Rave from flutterwave, you would need to create an account with both of them to get your API keys and set them as global variables, the app won't run without them. You can use the app without an email address but you can't top up your wallet balance without it. 
  PS. You can get dummy cards and dummy API keys from flutterwave's documentation. The recharge amount is in naira becasue the dummy API keys have a limit, a lower value currency lets me run more tests.

# Lab9 - 
  it's a birthday app, you can add, edit and delete birthdays. It's made with python(Flask) and sqlite,html,css and javascript.

# Pset6
DNA - this app takes a sequence of DNA and a CSV file containing STR counts for a list of individuals as a command line argument, and then matches the STR repeats to determine whom the DNA (most likely) belongs to.

# Pset1
**Mario** - it prompts the user for a positive integer between 1 & 8 inclusive via a command line prompt and creates a pyramid of block (like in the super mario game) according to the number inputed. It's built with C.
**Credit** - checks the authenticity of a credit/debit card using Luhn's Algorithm. It prompts the user for a card number and returns the card type (American Express, MasterCard,Visa) or invalid for an invalid card number, via command line. It's built with C.

# Pset2
**Readability** - Uses the Coleman-Liau index to calculate the U.S grade reading level of the inputed text. It prompts the user for a text and outputs the grade level of the text (e.g grade 5, grade 7 etc) via the command line. It is built with C.
**Substitution** - This ia s substitution cipher program. It encrypts a message using the provided encyption key, It is executed with a single command line argument which is the encryption key, the program then prompts the user for the plain text to be encrypted and returns the encrypted text. It is built with C.

# Pset3
**Plurality** - This is a voting program that runs a plurality voting system, each voter gets one vote and candidate with the highest vote wins. The candidate names are inputed as individual command line arguments when the program is executed (./plurality Alice Bob Sharon) up to a maximum of 9 candidates. The program then prompts the user for the number of voters (integer), then the prpgram prompts each voter for thier preffered candidate, then returns the winner. This was built with C
**Tideman** - This is a tideman election program. It is a ranked-choice voting method that’s guaranteed to produce the Condorcet winner of the election if one exists. The candidate names are inputed as individual command line arguments when the program is executed (./tideman Alice Bob Sharon) up to a maximum of 9 candidates. The program then prompts the user for the number of voters (integer), then it prompts each voter for the names of thier i'th choice (first, second, third, etc choice) based on the number of candidates, the program will then tally, sort and lock the votes and return the winner of the election. This was built with C (this problem set in particular nearly broke me).

# Pset 4
**Filter** - This is an image filtering program, it has 4 filters - **Grayscale** (converts the image into black and white) - **Reflection** (returns a mirror image), - **Blur** ( uses the blur box formula to create a blured image), - **Edges** (Uses the Sorbel operator to detect edges in the image, useful in AI algorithms for image processing). It takes 3 command line arguments, the filter name, image path and the filtered image path, and stores the filtered image in the specified filtered image path. (e.g ./filter -g images/yard.bmp out.bmp). Filter names are; -g = grayscale, -r = reflected, -b = blur, -e = edge. It was built in C.
**Recover** - 
