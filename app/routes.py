import os
from app import app,db
from datetime import timedelta
from flask import render_template, request, flash,url_for,redirect,session,make_response,send_from_directory
from app.models import User,Post, Comment
from app.stock_function import is_valid_email, check_login
import hashlib
from werkzeug.utils import secure_filename
from config import Config


@app.route('/')
def indexes():
    posts = Post.query.all()
    return render_template('index.html', posts=posts)


@app.route('/details')
def details():
    posts = Post.query.all()
    comments = Comment.query.all()
    return render_template('post-details.html', posts=posts,comments=comments)

@app.route('/about')
def aboutus():
    posts = Post.query.all()
    comments = Comment.query.all()
    return render_template('about.html', posts=posts,comments=comments)



@app.route('/contact')
def contact():
    posts = Post.query.all()
    return render_template('contact.html', posts=posts)

@app.route('/home')
def index():
    user = check_login()
    if user is None:
        return redirect(url_for('login_page'))
    
    
    return render_template("index.html", user=user)


@app.route("/add_comments",  methods=['POST', 'GET'])
def create_comments():
    if request.method =="GET":
        return render_template('post-details.html')
    else:
        name = request.form["name"]
        email = request.form["email"]
        subject = request.form["subject"]
        comment = request.form["comment"]

        validated = False
        if name == '' or email == '' or subject == '' or comment == "":
            flash("All fields are required")
        else:
            validated = True
        if not validated:
            return render_template("post-details.html")
        comment = Comment(name=name,email=email,subject=subject,comment=comment)
        db.session.add(comment)
        db.session.commit()
        return redirect(url_for("details"))




@app.route('/login', methods=['POST', 'GET'])
def login_page():
    if request.method == 'GET':
        return render_template("index1.html")
    else:
        email = request.form['email']
        password = request.form['password']
        print("Submitted email is", email)
        print("Submitted password is", password)
        if email == "":
            flash("Invalid Email")
        elif password == "":
            flash("Invalid Password")
        if email == '' or password == '':
            return render_template("index.html")
        else:
            # hash submitted password
            password_hash = hashlib.sha256(password.encode())
            hashed = password_hash.hexdigest()
            user = User.query.filter(User.email== email)
            user = User.query.filter((User.email == email)&(User.password==hashed)).first()
            if user is None:
                flash("Invalid Email or Password")
                return redirect(url_for("login_page"))
            # set sessions
            session['email']= email
            session['name']= user.name
            session['hashed'] = hashed
            #set cookies
            resp = redirect(url_for("index"))
            resp.set_cookie('UserEmail',email,max_age=timedelta(hours=24))
            resp.set_cookie('Hashed',hashed,max_age=timedelta(hours=24))
            resp.set_cookie('name',user.name,max_age=timedelta(hours=24))
            return resp

@app.route('/sign-up', methods=['POST', 'GET'])
def sign_up():
    if request.method == 'GET':
        return render_template("signup.html")
    else:
        name = request.form['name']
        email = request.form['email']
        phone = request.form['number']
        gender = request.form['gender']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        print("Submitted email is", email)
        print('Submitted name is', name)
        print("submitted phone number is", phone)
        print('submitted gender is', gender)
        print("Submitted password is", password)
        validated = False
        if email == '' or name == '' or password == '' or confirm_password == "":
            flash("All fields are required")
        elif len(password) < 6:
            flash("Password is too short!")
        elif password != confirm_password:
            flash("Password does not match")
        elif len(name) < 3:
            flash("Please enter a valid Name!")
        elif not is_valid_email(email):
            flash('Email is invalid')
        elif len(phone) != 11:
            flash("Invalid Phone Number")
        else:
            validated = True
        if not validated:
            return render_template("signup.html")
        else:
            print("Form submitted")

        # hash submitted password
        password_hash = hashlib.sha256(password.encode())
        hashed = password_hash.hexdigest()
        user = User(name=name, phone=phone,
                    gender=gender, password=hashed, email=email)
        db.session.add(user)
        db.session.commit()
        session['email']= email
        session['name']= user.name
        session['hashed'] = hashed
        return redirect(url_for('success'))
@app.route("/success")
def success():
    user= check_login()
    if not user:
        return redirect(url_for('login_page'))
    return render_template("success.html",name=user.name, email=user.email)
@app.route("/logout")
def logout():
    #remove sessions
    session['email']= None
    session['name']= None
    session['hashed'] = None
    # remove cookies
    resp = redirect(url_for("login_page"))
    resp.set_cookie('UserEmail','',expires=0)
    resp.set_cookie('Hashed','',expires=0)
    resp.set_cookie('name','',expires=0)
    return resp
@app.route("/my-profile")
def profile_page():
    user = check_login()
    if not user:
        return redirect(url_for('login_page'))
    return render_template('profile.html',user=user)
@app.route("/products", methods=['POST', 'GET'])
def list_products():
    check_login()
    post= Post.query.all()
    return render_template('products.html',posts=post)
@app.route("/add_products",  methods=['POST', 'GET'])
def create_products():
    check_login()
    if request.method =="GET":
        return render_template('addproduct.html')
    else:
        title = request.form["title"]
        subtitle = request.form["price"]
        poster = request.form["compare_price"]
        postnote = request.form["description"]
        category =request.form["category"]

        #upload pic
        picture = request.files['file']
        filename = secure_filename(picture.filename)
        picture.save(os.path.join(Config.UPLOAD_FOLDER,filename))

        validated = False
        if title == '' or subtitle == '' or poster == '' or postnote == "" or category == '':
            flash("All fields are required")
        else:
            validated = True
        if not validated:
            return render_template("addproduct.html")
        post = Post(title=title,subtitle=subtitle,poster=poster,postnote=postnote,category=category,pictures=picture.filename)
        db.session.add(post)
        db.session.commit()
        return redirect(url_for("list_products"))

@app.route('/uploads/<path>')
def view_file(path):
    return send_from_directory('uploads',path)


@app.route("/delete/<pid>")
def delete_product(pid):
    user = check_login
    if not user:
        return redirect(url_for('login_page'))
    post = Post.query.filter(Post.id == pid).first()
    if post is None:
        flash('Post not found!!')
        return redirect(url_for('list_products'))

    db.session.delete(post)
    db.session.commit()
    flash('Post deleted successfully!')
    return redirect(url_for('list_products'))
@app.route("/edit/<pid>", methods=['POST','GET'])
def edit_product(pid):
    print(pid)
    user = check_login
    if not user:
        return redirect(url_for('login_page'))
    post = Post.query.filter(Post.id==pid).first()
    if post is None:
        flash('Post not found!!')
        return redirect(url_for('list_products'))

    if request.method =="GET":
        return render_template('edit-product.html', post = post)
    post.title = request.form["title"]
    post.price = request.form["price"]
    post.compare_price = request.form["compare_price"]
    post.description = request.form["description"]
    post.category =request.form["category"]

     #upload pic
    picture = request.files['file']
    filename = secure_filename(picture.filename)
    picture.save(os.path.join(Config.UPLOAD_FOLDER,filename))
    post.pictures == picture.filename
    db.session.commit()
    flash(post.title + 'Updated Successfully')
    return redirect(url_for('list_products'))
