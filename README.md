# CookingBud
#### Video Demo:  https://www.youtube.com/watch?v=DdUwVHKZ7Y0
#### Description:

This project is a web app, created in **Python with Flask and with a SQL database connected**.
It's called *Cooking Bud*, because it has functionalities that help in the kitchen, like measurements converter, saving a recipe and others.
Cooking is one of my hobbies and I wanted to create a web application that would help me keep track of my favourite recipes and save a new one once I found it.

*Features* of the **Cooking Bud** are:
-View a saved recipe
-Save a new recipe
-Converter from cups to grams
                *grams to cups
                *ounces to grams
-Shopping list
-And of course register, login, logout

In [app.py](project/app.py) I setup my app to use SQL database and created an app and routes with Flask.
There are more routes, like */register* where a new user can be registered, *home* where you can select and view one of the saved recipes,  main *converter* route and 3 *converter* routes from it, for each measurement converter.
Also a *create* route, where you can save your new recipes and a *list* route which can create a shopping list to have on your device.

The features are pretty basic, but the idea can be developed with more details and features and create a very useful web app.

Folders:
1. In templates are stored all the html pages I used.
2. In static is a styles.css file that designed the appearance of the web app and several blocks from different pages.
3. In helpers.py it's a function that designed some pages to require login to access, like in Finance.

**When you click to save a recipe, that recipe is stored in _project.db_, where I created 2 tables: users and recipes. The recipe details are saved in _recipes_ table in different columns.**
>Then, on the home page runs a _select_ form which shows the titles of all the saved recipes and lets you choose one to view.

**For the converter, I hardcoded some values for each converting operation, for example: in cups to grams form, 1 cup of liquids equals 240 grams of liquids.**
> In order to know which converting operation of the 3 was made, I assigned arbitrary page= 1 for cups to grams, page=2 for grams to cups and page=3 for ounces to grams. This way I could know which conversion to make.

**For the sopping list it was easier, I put a form on the html page with inputs for each cattegory of groceries, and on submitting the form, I convert the input from each box, splitting it by commas using the _split(",")__ function, to show each item individually on the actual shopping list.**
> As design, I used the _styles.css_ to show borders of the list, lower the width, change background color to be different from the edges of the page and margins 0 auto for the list to be centered on the page. I liked it like this because it resembles an actual piece of paper.

<sub>The base of the web app design was inspired from Finance, but I chose green and other similar colours to be closer to idea of food and for the app to be more lively.</sub>

>In converter.html I created a _nav nav-tab_ with 3 submenus, because I wanted all 3 options to be on the same page.


<sub> create.html, convert.html, list.html, select.html each have a form with an action to the right app route, and after submitting the form it redirects to a new page where you will find the needed informations</sub>

This was the principal idea of my app, hope it will be found useful.
                  **Thanks! `#0969DA`**
