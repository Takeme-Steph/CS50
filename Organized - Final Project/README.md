# Organized
#### Video Demo: https://loom.com/share/5ca4f49766c946d3883577326f1a73ba
#### Description:
Organized is a planning & budgeting web app. It has 3 levels **Event** > **Umbrellas** > **Todos**. You can use it to make todo lists, plan budgeted events etc.
It lets you know when you are under or overbudget, you can also assign tasks and todo's to other people *(this is function is still in a very basic form and is yet to be properly expended upon)*
It has a wide range of uses from budgeting monthly expenses to planing big events & projects or just a simple todo list.

##### Static Folder:
This contains static items such as the favicon and icons used, the css style sheet and the javascript file for custom javacript functions used.
##### Templates Folder:
This contains the html files for the app.
##### application.py :
This is the main flask application.
##### app.db:
This is the datatbase for the application. Stores all neccesarry information and some other information that could be useful for analytics.
##### helpers.py:
This contains custom python functions used in the app.
##### requirements.txt:
This contains the packages needed to run the app.
##### Routing:
Every route checks if the user is loged in and if the item being accessed belongs to the user. This way a user cannot access another users data even if they have the link to the item. If you do not have access you will be redirected to the home page.
##### Frontend Design:
Design is not my strong point so i borrowed some design elements from the internet (sources are referenced) and the rest from bootstrap. It's mostly basic design, nothing fancy.
##### Security:
Passwords are hashed and tried my best to make sure routes are accessed & data reterieved in a way that doesn't expose sensitive information through the url or any other method.
##### Possible improvements & New Features List:
- Improving the **assigned to** feature so that a user can see other todo lists that they do not own but are assigned a task in it.
- A dynamic **assigned to** list, where the assigner can pick from a list of all known contacts or people on thier organisation account and assign a task to them
- Mail alerts for certain actions
- Allow image & document upload
- Allow contributors for events, umbrellas & todos
- Allow the option of signing up for a company account or personal account with specialized User experienxe and design
- Permissions for contributors (read/write)
- A wallet system where one cam fund an event wwith real money and people assingned to the tasks can withraw the money budgeted for it to pay bills
- Special Event templates e.g for household bills with added autopayment functionality where supported 3rd parties are paid with money in users wallet when the bills are due
- Analytics Dashboard
- Abitlity to sort events, umbrellas and todos
- Warning for overdue tasks
