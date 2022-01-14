from flask import Flask, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, validators
from wtforms.validators import DataRequired

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://test:password@localhost/flask-tutorial'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'secret_key'
db = SQLAlchemy(app)

# Post class, including id, title and content
class Posts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), nullable=False, unique=False)
    content = db.Column(db.Text)

# Post form
class PostForm(FlaskForm):
    title = StringField('標題', validators=[DataRequired()])
    content = TextAreaField('内容',validators=[DataRequired()])
    submit = SubmitField('送出')

# Index page, rendering all posts out in the page
@app.route('/')
def index():
    posts = Posts.query.order_by(Posts.id).all()
    return render_template('index.html', posts=posts)

# Create post page
@app.route('/post', methods=['GET', 'POST'])
def create_post():
    form = PostForm()
    title = None
    content = None
    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data
        post = Posts(title=title, content=content)
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('create_post.html', form=form, title=title, content=content)

if __name__ == '__main__':
    app.run(debug=True)