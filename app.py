from flask import Flask, request, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db=SQLAlchemy(app)

class Todo(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    content=db.Column(db.String(200),nullable=False)
    completed=db.Column(db.Integer,default=0)
    date_created=db.Column(db.DateTime,default=datetime.utcnow)

    def __repr__(self):
        return '<Task %r>' % self.id
    




@app.route('/',methods=['POST','GET'])
def index():
    if request.method=='POST':
        task=request.form['content'].strip()
        if not task:
            return 'Task cannot be empty'
        
        
        new_task=Todo(content=task)       
        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue adding your task'
    
    else:
        task=Todo.query.order_by(Todo.date_created).all()
        return render_template('index.html',tasks=task)




@app.route('/search')
def search():
    value=request.args.get('term')
    if value=='sex':
        return f'Your searched for, {value}\nThere was none to be found'
    else:
        return f'Your searched for, {value}'




@app.route('/delete/<int:id>')
def delete(id):
    task_to_delete=Todo.query.get_or_404(id)
    print(1)
    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'There was a problem deleting that task'




@app.route('/update/<int:id>',methods=['GET','POST'])
def update(id):
    task=Todo.query.get_or_404(id)
    if request.method=='POST':
        task.content=request.form['content']
        try:
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue updating your task'
    else:
        return render_template('update.html',task=task)




@app.route('/user/<username>')
def user(username):
    return f'Hello there, {username}'

#this edit is to make the code line to version 3

if __name__=='__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)






