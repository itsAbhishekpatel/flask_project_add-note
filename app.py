# First we imported the Flask class from the flask library
from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy # import SQLAlchemy class from flask_sqlalchemy library
from datetime import datetime,date

# Next we created the instance of this class 
"""The first argument is the name of the application’s module or package.
 If you are using a single module (as in this example), you should use __name__ 
 because depending on if it’s started as application or 
 imported as module the name will be different ('__main__' versus the actual import name)."""

# Import the render_template function to render html files 
app = Flask(__name__)

# configure the SQLite database, relative to the app instance folder
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///todo.db"
app.config["SQLALCHEMY_TRCAK_MODIFICATION"] = False
# create the extension/ db object of SQLALchemy class 
db = SQLAlchemy(app)

# Define Model, define the table schema 
class Todo(db.Model):
    sno = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(200),nullable = False)
    desc = db.Column(db.String(500),nullable = False)
    date_created = db.Column(db.DateTime, default = datetime.utcnow)

    # def __repr__(self) -> str:
    #     return f"{self.sno} and {self.title}"
# Create the Tables
# After all models and tables are defined, call SQLAlchemy.create_all() 
with app.app_context():
    db.create_all()
# We then use the route() decorator to tell Flask what URL should trigger our function.
# / = home url will trigger the helloword function and then this function return a string or an HTML file 
# and returns the message we want to display in the user’s browser.
@app.route("/",methods = ['GET','POST'])
def helloword():
    # use request to handle form 
    if request.method == "POST":
        # title variable which store values from html form
        title = request.form['title']
        desc = request.form['desc']
    # crate an object of Todo Model Class 
        todo = Todo(title=title,desc=desc)
        db.session.add(todo)
        db.session.commit()
    
    # use render_template function to render html file 
    # create object allTodo and store all todo and pass it into html file
    allTodo = Todo.query.all()
    return render_template("index.html",allTodo=allTodo)


# delete Todo   
@app.route("/delete/<int:sno>")
def delete(sno):
    todo = Todo.query.filter_by(sno=sno).first()
    db.session.delete(todo)
    db.session.commit() #commit the session
    return redirect("/") #redirect to the home page

# update Todo    
@app.route("/update/<int:sno>",methods = ['GET','POST'])
def update(sno):
    if request.method == "POST":
        title = request.form['title']
        desc = request.form['desc']
        todo = Todo.query.filter_by(sno=sno).first()
        todo.title = title
        todo.desc = desc
        db.session.add(todo)
        db.session.commit()
        return redirect("/") #redirect to the home page

    todo = Todo.query.filter_by(sno=sno).first()
    return render_template("update.html",todo = todo)

if __name__ == "__main__":
    app.run(debug = True)