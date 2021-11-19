My problem sets and projects from taking the cs50 classes.

## Organized - Final Project
  Organized is a planning & budgeting web app. It has 3 levels **Event** > **Umbrellas** > **Todos**. You can use it to make todo lists, plan budgeted events etc.
  It lets you know when you are under or overbudget, you can also assign tasks and todo's to other people *(this is function is still in a very basic form and is yet to be           properly expended upon)*
  It has a wide range of uses from budgeting monthly expenses to planing big events & projects or just a simple todo list.
  Made with python(Flask) and sqlite, html, css, javascript, jquery. Please read it's readme file for more info and instal the packages in the requirements file befor running.

## Finance- 
  it's a basic stock exchange app made with python(Flask) and sqlite, html, css, javascript, jquery and Ajax. Live quotes from IEX and Payment hosted by Rave from flutterwave, you would need to create an account with both of them to get your API keys and set them as global variables, the app won't run without them. You can use the app without an email address but you can't top up your wallet balance without it. 
  PS. You can get dummy cards and dummy API keys from flutterwave's documentation. The recharge amount is in naira becasue the dummy API keys have a limit, a lower value currency lets me run more tests.

## Lab9 - 
  it's a birthday app, you can add, edit and delete birthdays. It's made with python(Flask) and sqlite,html,css and javascript.

## Pset1
#### **Mario** - it prompts the user for a positive integer between 1 & 8 inclusive via a command line prompt and creates a pyramid of block (like in the super mario game) according to the number inputed. It's built with C.
#### **Credit** - checks the authenticity of a credit/debit card using Luhn's Algorithm. It prompts the user for a card number and returns the card type (American Express, MasterCard,Visa) or invalid for an invalid card number, via command line. It's built with C.

## Pset2
#### **Readability** - Uses the Coleman-Liau index to calculate the U.S grade reading level of the inputed text. It prompts the user for a text and outputs the grade level of the text (e.g grade 5, grade 7 etc) via the command line. It is built with C.
#### **Substitution** - This ia s substitution cipher program. It encrypts a message using the provided encyption key, It is executed with a single command line argument which is the encryption key, the program then prompts the user for the plain text to be encrypted and returns the encrypted text. It is built with C.

## Pset3
#### **Plurality** - This is a voting program that runs a plurality voting system, each voter gets one vote and candidate with the highest vote wins. The candidate names are inputed as individual command line arguments when the program is executed (./plurality Alice Bob Sharon) up to a maximum of 9 candidates. The program then prompts the user for the number of voters (integer), then the prpgram prompts each voter for thier preffered candidate, then returns the winner. This was built with C
#### **Tideman** - This is a tideman election program. It is a ranked-choice voting method that’s guaranteed to produce the Condorcet winner of the election if one exists. The candidate names are inputed as individual command line arguments when the program is executed (./tideman Alice Bob Sharon) up to a maximum of 9 candidates. The program then prompts the user for the number of voters (integer), then it prompts each voter for the names of thier i'th choice (first, second, third, etc choice) based on the number of candidates, the program will then tally, sort and lock the votes and return the winner of the election. This was built with C (this problem set in particular nearly broke me).

## Pset4
#### **Filter** - This is an image filtering program, it has 4 filters 
- **Grayscale** (converts the image into black and white) 
- **Reflection** (returns a mirror image), 
- **Blur** ( uses the blur box formula to create a blured image), 
- **Edges** (Uses the Sorbel operator to detect edges in the image, useful in AI algorithms for image processing). 
It takes 3 command line arguments, the filter name, image path and the filtered image path, and stores the filtered image in the specified filtered image path. (e.g ./filter -g images/yard.bmp out.bmp). Filter names are; -g = grayscale, -r = reflected, -b = blur, -e = edge. It was built in C.
#### **Recover** - This is a program that recovers deleted JPEGs from a forensic image. The program is executed with only 1 command line argument which is the name of the forensic image to recover the images from (e.g ./recover card.raw) it then stores the recovered images in the program's directory. It was built in C.

## Pset5
#### **Speller** - This program spellchecks a file using a hash table, the assignment was to build the fastest spellchecker i could in terms of clock time and space. It checks the provided text against a dictionary to check for misspelled words. The program excecutes with 2 command line argeuments, the dictionary path and the text to spellcheck, structured as such: ./speller dictionaries/small text, (e.g ./speller dictionaries/small texts/lalaland.txt). It returns the below:
- WORDS MISSPELLED:
- WORDS IN DICTIONARY:
- WORDS IN TEXT:
- TIME IN load:
- TIME IN check:
- TIME IN size:
- TIME IN unload:
- TIME IN TOTAL:
This was built in C

## Pset6
#### **DNA** - this app takes a sequence of DNA and a CSV file containing STR counts for a list of individuals, and then matches the STR repeats to determine whom the DNA (most likely) belongs to. The program is executed with 2 command line arguments, the path to the database of people and thier DNA sequence and the path to the file containing the STR repeats to be matched (e.g dna.py databases/large.csv sequences/5.txt). This was built with python.
#### **Credit**, **Mario**, **Readability** are python remakes of earlier psets with the same name.

## Pset7
#### **Movies** - SQL queries to gain insights from a copy of IMDb's database of movies, the database is not included in this repo but you can doenload a copy from IMDb's website. The questioned answerd by each sql query is as seen below:
1. write a SQL query to list the titles of all movies released in 2008.
   - Your query should output a table with a single column for the title of each movie.
2. write a SQL query to determine the birth year of Emma Stone.
   - Your query should output a table with a single column and a single row (not including the header) containing Emma Stone’s birth year.
   - You may assume that there is only one person in the database with the name Emma Stone.
3. write a SQL query to list the titles of all movies with a release date on or after 2018, in alphabetical order.
   - Your query should output a table with a single column for the title of each movie.
   - Movies released in 2018 should be included, as should movies with release dates in the future.
4. write a SQL query to determine the number of movies with an IMDb rating of 10.0.
   - Your query should output a table with a single column and a single row (not including the header) containing the number of movies with a 10.0 rating.
5. write a SQL query to list the titles and release years of all Harry Potter movies, in chronological order.
   - Your query should output a table with two columns, one for the title of each movie and one for the release year of each movie.
   - You may assume that the title of all Harry Potter movies will begin with the words “Harry Potter”, and that if a movie title begins with the words “Harry Potter”, it is a Harry Potter movie.
6. write a SQL query to determine the average rating of all movies released in 2012.
   - Your query should output a table with a single column and a single row (not including the header) containing the average rating.
7. write a SQL query to list all movies released in 2010 and their ratings, in descending order by rating. For movies with the same rating, order them alphabetically by title.
   - Your query should output a table with two columns, one for the title of each movie and one for the rating of each movie.
   - Movies that do not have ratings should not be included in the result.
8. write a SQL query to list the names of all people who starred in Toy Story.
   - Your query should output a table with a single column for the name of each person.
   - You may assume that there is only one movie in the database with the title Toy Story.
9. write a SQL query to list the names of all people who starred in a movie released in 2004, ordered by birth year.
   - Your query should output a table with a single column for the name of each person.
   - People with the same birth year may be listed in any order.
   - No need to worry about people who have no birth year listed, so long as those who do have a birth year are listed in order.
   - If a person appeared in more than one movie in 2004, they should only appear in your results once.
10. write a SQL query to list the names of all people who have directed a movie that received a rating of at least 9.0.
    - Your query should output a table with a single column for the name of each person.
    - If a person directed more than one movie that received a rating of at least 9.0, they should only appear in your results once.
11. write a SQL query to list the titles of the five highest rated movies (in order) that Chadwick Boseman starred in, starting with the highest rated.
    - Your query should output a table with a single column for the title of each movie.
    - You may assume that there is only one person in the database with the name Chadwick Boseman.
12. write a SQL query to list the titles of all movies in which both Johnny Depp and Helena Bonham Carter starred.
    - Your query should output a table with a single column for the title of each movie.
    - You may assume that there is only one person in the database with the name Johnny Depp.
    - You may assume that there is only one person in the database with the name Helena Bonham Carter.
13. write a SQL query to list the names of all people who starred in a movie in which Kevin Bacon also starred.
    - Your query should output a table with a single column for the name of each person.
    - There may be multiple people named Kevin Bacon in the database. Be sure to only select the Kevin Bacon born in 1958.
    - Kevin Bacon himself should not be included in the resulting list.
#### **Houses** - I honestly can't really remember what this program was meant to do, but i beleive *import.py* is meant to import a list of students names, houses and date of birth from a csv file into a central database (students.db), and *roaster.py* is meant to prompt the user for a house name and print out all students in the central database that belong to that house via the command line. This was built in python.

## **Homepage** 
A basic webpage using HTML,CSS and Javascript, and some elements from bootstrap.
