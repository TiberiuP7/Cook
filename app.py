import os

from datetime import datetime
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash
from helpers import error, login_required

#application
app= Flask(__name__)

#configure sqlite database
db = SQL("sqlite:///project.db")

app.config["TEMPLATES_AUTO_RELOAD"] = True
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

@app.route("/", methods=["GET", "POST"])
@login_required
def home():
    """Show saved recipes and select one if you want"""
    if request.method == "POST":
        title= request.form.get("title")
        id= session["user_id"]

        recipes = db.execute("SELECT * FROM recipes WHERE id= ? AND title= ?", id, title)
        items= db.execute("SELECT * FROM recipes WHERE id= ?", id)

        return render_template("home.html", recipes = recipes, items=items)
    else:
        id= session["user_id"]
        recipes= db.execute("SELECT * FROM recipes WHERE id= ?", id)
        return render_template("select.html", recipes = recipes)

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        if not request.form.get("username"):
            return error("username")
        if not request.form.get("password"):
            return error("password")

        if request.form.get("password") != request.form.get("confirmation"):
            return error("confirmation")

        name = request.form.get("username")
        password = request.form.get("password")
        user = db.execute("SELECT id FROM users WHERE name=?", name)
        print(user)
        if len(user) != 0:
             return error

        hash= generate_password_hash(password)
        db.execute("INSERT INTO users (name, hash) VALUES (?, ?)", name, hash)
        rows = db.execute("SELECT id FROM users WHERE hash= ?", hash)
        for x in rows:
            col= x
            break
        id= col["id"]
        session["user_id"]= id
        return redirect("/")
    else:
         return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    session.clear()
    if request.method == "POST":
        if not request.form.get("username"):
            return error("Please provide Username")
        if not request.form.get("password"):
            return error("Please enter a password")

        rows = db.execute("SELECT * FROM users WHERE name=?", request.form.get("username"))
        #Check for correct username and password
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
             return error("Username and/or password incorrect!")

        session["user_id"]= rows[0]["id"]

        return redirect("/")
    else:
         return render_template("login.html")


@app.route("/logout")
@login_required
def logout():
     session.clear()
    #redirect user to login form
     return redirect("/")

@app.route("/create", methods=["GET", "POST"])
@login_required
def create():
    if request.method == "POST":
        id = session["user_id"]
        title = request.form.get("title")
        ingredients = request.form.get("ingredients")
        step1 = request.form.get("step1")
        step2 = request.form.get("step2")
        step3 = request.form.get("step3")
        step4 = request.form.get("step4")
        if len(ingredients) < 80 and step4 == None:
            #if less ingredients and not many steps the recipe is easy
            difficulty = "Easy"
        else:
            #means recipe is hard
            difficulty = "Hard/Moderate"
        time = request.form.get("time")

        db.execute("INSERT INTO recipes(title, steps, step2, step3, step4, time, difficulty, id, ingredients) VALUES (?, ?, ?, ? ,?, ?, ?, ?, ?)", title, step1, step2, step3, step4, time, difficulty, id, ingredients)
        return redirect("/")
    else:
        return render_template("create.html")

@app.route("/converter")
@login_required
def converter():
    return render_template("converter.html")

@app.route("/converter/cups-grams", methods=["GET", "POST"])
@login_required
def cups():
    if request.method== "POST":
        cups= request.form.get("cups")
        ingredient= request.form.get("ingredient")
        #so I know which form the data comes from on results page
        page=1

        if ingredient == "flour":
            grams= float(cups) * 120
        elif ingredient == "liquids":
            grams= float(cups) * 240
        elif ingredient == "oil/fats":
            grams= float(cups) * 217
        else:
            #if ingredient is sugar
            grams = float(cups) * 200

        return render_template("converted.html", grams = grams, ingredient= ingredient, cups =cups, page=page)
    else:
        return render_template("converter.html")

@app.route("/converter/grams-cups", methods=["GET", "POST"])
@login_required
def grams():
    if request.method== "POST":
        grams= request.form.get("grams")
        ingredient= request.form.get("ingredient")
        #so I know which form the data comes from on results page
        page=2
        if ingredient == "Flour":
            cups= int(grams) / 120
        elif ingredient == "Liquids":
            cups= int(grams) / 240
        elif ingredient == "Oil/Fats":
            cups= int(grams) / 217
        else:
            #if ingredient is sugar
            cups = int(grams) / 200

        return render_template("converted.html", cups=cups, ingredient= ingredient, grams=grams, page=page)
    else:
        return render_template("converter.html")

@app.route("/converter/ounces-grams", methods=["GET", "POST"])
@login_required
def ounces():
    if request.method== "POST":
        ounces= request.form.get("ounces")
        ingredient= request.form.get("substance")
        #so I know which form the data comes from on results page
        page=3
        if ingredient == "Flour":
            grams= float(ounces) * 28.35
        elif ingredient == "milk and cream":
            grams= float(ounces) * 30
        elif ingredient == "Oil/Fats":
            grams= float(ounces) * 27
        else:
            #if ingredient is sugar
            grams= float(ounces) * 25

        return render_template("converted.html", ounces=ounces, ingredient= ingredient, grams=grams, page=page)
    else:
        return render_template("converter.html")


@app.route("/list", methods=["GET", "POST"])
@login_required
def list():
    if request.method== "POST":
        id=session["user_id"]

        veg= request.form.get("vegetables")
        if veg == None:
            veg=1
        # Split the vegetables input by each comma, getting separate items
        else:
            veg= veg.split(",")

        meat= request.form.get("meat")
        if meat == None:
            meat=1
        #Split each item from the input so it can be shown individually
        else:
            meat= meat.split(",")

        dairy= request.form.get("dairy")
        dairy= dairy.split(",")

        spices= request.form.get("spices")
        spices= spices.split(",")

        sweets= request.form.get("sweets")
        if sweets == None:
            sweets= false
        else:
            sweets= sweets.split(",")

        drinks= request.form.get("drinks")
        drinks= drinks.split(",")

        today= request.form.get("today")
        user= db.execute("SELECT name FROM users WHERE id= ?", id)
        for x in user:
            col= x
            break
        name= col["name"]

        return render_template("listed.html", veg=veg, meat=meat, dairy=dairy, spices=spices, sweets=sweets, drinks=drinks, today=today, name= name)
    else:
        return render_template("list.html")


