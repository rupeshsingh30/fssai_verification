from flask import Flask,render_template,request,redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
# Add app.app_context().push()

class Todo(db.Model):
    sno = db.Column(db.Integer,primary_key = True)
    title = db.Column(db.String(200),nullable=False)
    desc = db.Column(db.String(500),nullable=False)
    date = db.Column(db.DateTime,default=datetime.utcnow)

    def __repr__(self):
        return f"{self.sno} -- {self.title} -- {self.desc}"

@app.route('/' ,methods=['GET','POST'])
def home(): 
    if request.method=='POST':
        # print(request.form['title'])
        title = request.form['title']
        desc = request.form['desc']
        # todo = Todo(title="first todo",desc="start investing in stock market")
        todo = Todo(title=title,desc=desc)
        db.session.add(todo)
        db.session.commit()
    all_todo = Todo.query.all()
    return render_template('index.html',all_todo=all_todo)

# @app.route('/show')
# def products(): 
#     all_todo = Todo.query.all()
#     print(all_todo)
#     return 'all data'
    
@app.route('/update/<int:sno>',methods=['GET','POST'])
def update(sno):
    if request.method == "POST":
        title = request.form['title']
        desc = request.form['desc']
        todo = Todo.query.filter_by(sno=sno).first()
        todo.title = title
        todo.desc = desc
        db.session.add(todo)
        db.session.commit()
        return redirect('/')
        

    update_todo = Todo.query.filter_by(sno=sno).first()
    # print(update_todo)
    return render_template('update.html',update_todo=update_todo)

@app.route('/delete/<int:sno>')
def delete(sno): 
    delete_todo = Todo.query.filter_by(sno=sno).first()
    db.session.delete(delete_todo)
    db.session.commit()
    print(delete_todo)
    return redirect("/")
    

if __name__ == '__main__':
    # with app.app_context():
    #     db.create_all()
    app.run(debug=True)