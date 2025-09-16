from flask import Flask, render_template,request,redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
db_path = os.path.join(basedir, "todo.db")
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///todo.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# sqlalchemy is an  ORM mapper it provides facilty to  make changes in database through python 

class Todo(db.Model):
    SNo = db.Column(db.Integer,primary_key = True)
    title = db.Column(db.String(200),nullable = False)
    desc = db.Column(db.String(500),nullable = False)
    date_created = db.Column(db.DateTime,default = datetime.utcnow)
    
    # this method is used when you want to print object TODO and what do you want print like title and SNO
    def __repr__(self) -> str:   
        return f"{self.SNo}  - {self.title}"
    
@app.route("/",methods=['GET','POST'])
def hello_world():
    if request.method == "POST":
        title=request.form['title']
        desc=request.form['desc']
        todo = Todo(title=title,desc = desc)
        db.session.add(todo)
        db.session.commit()
    all_todos = Todo.query.all()
    return render_template('index.html',all_todos=all_todos)

@app.route("/update/<int:SNo>",methods=["GET", "POST"])
def update(SNo):
    if request.method == 'POST':
        title = request.form['title']
        desc = request.form['desc']
        todo = Todo.query.filter_by(SNo = SNo).first()
        todo.title = title
        todo.desc = desc
        db.session.add(todo)
        db.session.commit()
        return redirect('/')
        
    todo = Todo.query.filter_by(SNo = SNo).first()
    return render_template('update.html',todo=todo)

@app.route("/delete/<int:SNo>",methods=["GET", "POST"])
def delete(SNo):
    todo = Todo.query.filter_by(SNo = SNo).first()
    if todo:
        db.session.delete(todo)
        db.session.commit()
    return redirect('/')


if __name__ == '__main__':
    with app.app_context():
        db.create_all()

    # app.run(debug=True,port=5000)
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)), debug=False)
