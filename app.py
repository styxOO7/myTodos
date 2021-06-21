from flask import Flask, render_template, request, redirect     
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///todo.db"
app.config['SQLACHMEY_TRACK_NOTIFICATIONS'] = False

db = SQLAlchemy(app)

class Todo(db.Model):
    __searchable__ = ['title', 'desc']
    
    sno = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(200), nullable = False)
    desc = db.Column(db.String(500), nullable = False)
    date_created = db.Column(db.DateTime, default = datetime.utcnow)
    # displaying queries of db
    def __repr__(self) -> str:
        return f"{self.sno} - {self.title}"


@app.route('/', methods = ['GET', 'POST'])
def home():
    if request.method == 'POST':
        title = request.form['title']
        desc = request.form['desc']
        todo = Todo(title = title, desc = desc)
        db.session.add(todo)
        db.session.commit()
    allTodo = Todo.query.all()
    return render_template('index.html', allTodo = allTodo)
    
# UD
@app.route('/update/<int:sno>', methods = ['GET', 'POST'])
def update(sno):
    if request.method=='POST':
        title = request.form['title']
        desc = request.form['desc']
        todo = Todo.query.filter_by(sno = sno).first()
        # saving
        todo.title = title
        todo.desc = desc
        db.session.add(todo)
        db.session.commit()
        return redirect("/")
    todo = Todo.query.filter_by(sno = sno).first()
    return render_template('update.html', todo = todo)

@app.route('/delete/<int:sno>')
def delete(sno):
    this = Todo.query.filter_by(sno = sno).first()
    db.session.delete(this)
    db.session.commit()
    return redirect("/")


if __name__ == "__main__":
    app.run(debug = True, port = 8000)