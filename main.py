# Import flask and necessary modules
from flask import Flask, render_template, request, redirect, url_for, session
app = Flask(__name__)
app.secret_key = 'anyrandomstring123'  # Needed for session management

# Import SQLAlchemy for database
from flask_sqlalchemy import SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///user.db'
# Initialize the database
db = SQLAlchemy(app)

# Importing encryption library for password hashing
from werkzeug.security import generate_password_hash, check_password_hash




#1 Authentication logic for user credentials
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)

    def __repr__(self):
        return f"<User {self.username}>"
    



#2 Creating notes model
class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)



    

#3 Create the database tables
with app.app_context():
    db.create_all()



#4 First Interface to user
@app.route("/")
def index():
    return render_template("index.html")




#5 Registration page for new users
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = generate_password_hash(request.form["password"])
        
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            return "Username already taken"
        
        new_user = User(username=username, password=password)
        db.session.add(new_user)
        db.session.commit()
        
        return redirect(url_for("index"))
    return render_template("register.html")



#6 Login logic to authenticate users
@app.route("/login", methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]

    user = User.query.filter_by(username=username).first()
    if user and check_password_hash(user.password, password):
        session["user_id"] = user.id
        session["username"] = username
        return redirect(url_for("menu"))
    else:
        return "Invalid credentials"




#7 Menu route after successful login
@app.route("/menu")
def menu():
    if "user_id" not in session:
        return redirect(url_for("index"))
    return render_template("menu.html", username=session["username"])



#8 Logout route to clear session
@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))




#9 Create_Note route
@app.route("/createnote", methods=["GET", "POST"])
def create_note():
    if "user_id" not in session:
        return redirect(url_for("index"))
    
    if request.method == "POST":
        title = request.form["title"]
        content = request.form["content"]
        
        new_note = Note(title=title, content=content, user_id=session["user_id"])
        db.session.add(new_note)
        db.session.commit()
        
        return redirect(url_for("menu"))
    return render_template("createnote.html")






@app.route("/displaynote")
def display_note():
    if "user_id" not in session:
        return redirect(url_for("index"))
    
    notes = Note.query.filter_by(user_id=session["user_id"]).all()
    return render_template("displayNote.html", notes=notes)







@app.route("/delete/<int:note_id>", methods=["POST"])
def delete_note(note_id):
    if "user_id" not in session:
        return redirect(url_for("index"))
    
    note = Note.query.get(note_id)
    if note and note.user_id == session["user_id"]:
        db.session.delete(note)
        db.session.commit()
    
    return redirect(url_for("display_note"))






if __name__ == "__main__":
    app.run(debug=True)