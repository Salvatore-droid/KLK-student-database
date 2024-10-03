from flask import render_template, url_for, redirect, flash, request
from klk import app, db,  bcrypt
from klk.form import RegistrationForm, LoginForm, StudentForm
from klk.models import User, Student
from flask_login import login_user, current_user, logout_user, login_required
# import secrets


@app.route("/home")
@login_required
def home():
    students = Student.query.all()
    image_file = url_for('static', filename='images/' + current_user.image)
    return render_template('home.html', students=students, image_file=image_file)

@app.route("/search", methods=['GET'])
@login_required
def search():
    query = request.args.get('query', '').strip()
    if query:
        first_letter = query[0].lower()
        results = Student.query.filter(Student.studentname.ilike(f'{first_letter}%')).all()
    else:
        results = []
    return render_template('search.html', results=results)

# def save_picture(form_picture):
#     random = secrets.token_hex(8)
    

@app.route("/add_beneficiary", methods=['GET', 'POST'])
@login_required
def add_beneficiary():
    form = StudentForm()
    if form.validate_on_submit():
        student = Student(studentname=form.studentname.data, school=form.school.data, year=form.year.data, course=form.course.data, description=form.description.data)
        db.session.add(student)
        db.session.commit()
        flash(f'The student as been added successfully!', 'success')
        return redirect(url_for('home'))
    return render_template('add_beneficiary.html', title ='add_beneficiary', form=form)

@app.route("/home/<int:beneficiary_id>")
@login_required
def beneficiary(beneficiary_id):
    beneficiary = Student.query.get_or_404(beneficiary_id)
    return render_template('beneficiary.html', title=beneficiary.studentname, beneficiary=beneficiary)

@app.route("/register", methods=['GET', 'POST']) 
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=password)
        db.session.add(user)
        db.session.commit()
        flash(f"Account created for username { form.username.data } successfully, you are now able to login!", 'success')
        return redirect(url_for('login'))
    return render_template("register.html", title='register', form=form)


@app.route("/", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            flash(f"Your are logged in as { form.username.data }", 'success')
            login_user(user, remember=form.remember.data)
            return redirect(url_for('home'))
        else:
            flash(f'Incorrect username or password', 'danger')
    return render_template("login.html", title='login', form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route("/description")
@login_required
def description():
    students = Student.query.all()
    return render_template('description.html', students=students)
