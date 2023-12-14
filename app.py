from markupsafe import escape
import datetime
from flask import Flask, abort, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy



app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.datetime.utcnow())

    def __repr__(self):
        return '<Task %r>' % self.id


@app.route('/', methods=['POST','GET'])
def index():
    if request.method == 'POST':
        task_content = request.form['content']
        new_task = Todo(content=task_content)

        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue adding your task.'

    else:
        tasks = Todo.query.order_by(Todo.date_created).all()
        return render_template('index.html', utc_dt=datetime.datetime.utcnow(), tasks=tasks)

@app.route('/delete/<int:id>')
def delete(id):
    task_to_delete = Todo.query.get_or_404(id)

    try: 
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        'There was a problem deleting that task'

@app.route('/about/')
def about():
    return render_template('about.html')

@app.route('/comments/')
def comments():
    comments = [
    'This is the first comment',
    'This is the second comment.',
    'This is the third comment.',
    'DONT QUIT YOUR DAY JOB!'
    ] 

    return render_template('comments.html', comments=comments)

@app.route('/capitalize/<word>/')
def capitalize(word):
    return '<h1>{}</h1>'.format(escape(word.capitalize()))

@app.route('/add/<int:n1>/<int:n2>/')
def add(n1, n2):
    return '<h1>{}</h1>'.format(escape(n1+n2))

@app.route('/users/<int:user_id>/')
def greet_user(user_id):
    users = ['Bob', 'Jane', 'Adam']
    try:
        return '<h2>Hi {}</h2>'.format(users[user_id])
    except:
        abort(404)

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        app.run(debug=True)
