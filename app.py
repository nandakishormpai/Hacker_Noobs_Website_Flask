from flask import Flask, render_template, request, redirect,flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy import desc

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///posts.db'
app.config['SECRET_KEY'] = '2166fsfsdfdsfthesd'
db = SQLAlchemy(app)

class BlogPost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    author = db.Column(db.String(20), nullable=False, default='N/A')
    github=db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return 'Blog post ' + str(self.id)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/posts', methods=['GET', 'POST'])
def posts():
    if request.method == 'POST':
        if(request.form['sort']=="date"):
            all_posts = BlogPost.query.order_by(desc(BlogPost.date_posted)).all()
        elif(request.form['sort']=="name"):
            all_posts = BlogPost.query.order_by(BlogPost.title).all()
        else:
            all_posts = BlogPost.query.order_by(BlogPost.author).all()
    else:
        all_posts = BlogPost.query.order_by(BlogPost.date_posted).all()
    return render_template('posts.html',posts=all_posts)

@app.route('/posts/delete/<int:id>' , methods=['GET', 'POST'])
def delete(id):
    post = BlogPost.query.get_or_404(id)
    if request.method == 'POST':
        if(request.form['dev_id']=="noobhacker001"  and  request.form['dev_key']=="!123hack456me!") :
            post = BlogPost.query.get_or_404(id)
            db.session.delete(post)
            db.session.commit()
            return redirect('/posts')
        else:
            flash('Invalid Developer Credentials !', 'danger')     

    return render_template('delete.html', post=post)


@app.route('/posts/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    
    post = BlogPost.query.get_or_404(id)

    if request.method == 'POST':
        post.title = request.form['title']
        post.author = request.form['author']
        post.content = request.form['content']
        post.github = request.form['github']
        if(request.form['dev_id']=="noobhacker001"  and  request.form['dev_key']=="!123hack456me!") :
            db.session.commit()
            return redirect('/posts')
        else:
            flash('Invalid Developer Credentials !', 'danger')     
    return render_template('edit.html', post=post)

@app.route('/posts/new', methods=['GET', 'POST'])
def new():
    if request.method == 'POST':
        post_title = request.form['title']
        post_content = request.form['content']
        post_author = request.form['author']
        post_github=request.form['github'] 
        if(request.form['dev_id']=="noobhacker001"  and  request.form['dev_key']=="!123hack456me!") :
            new_post = BlogPost(title=post_title, content=post_content, author=post_author, github=post_github)
            db.session.add(new_post)
            db.session.commit()
            return redirect('/posts')
        else:
            flash('Invalid Developer Credentials !', 'danger') 
            return render_template('new.html')
    else:
        return render_template('new.html')

@app.route('/about')
def about():
    return render_template('about.html')

if __name__ == "__main__":
    app.run(debug=True)