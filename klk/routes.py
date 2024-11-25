from flask import render_template, url_for, redirect, flash, request
from klk import app, db,  bcrypt
from klk.form import RegistrationForm, LoginForm, StudentForm, HighForm
from klk.models import User, Student, High
from flask_login import login_user, current_user, logout_user, login_required
import secrets, os

@app.route("/campus")
@login_required
def campus():
    students = Student.query.filter_by(user_id=current_user.id).all()
    picture_file = url_for('static', filename='images/' + Student.picture)
    return render_template('campus.html', students=students, picture=picture_file)

@app.route("/high")
@login_required
def high():
    students = High.query.filter_by(user_id=current_user.id).all()
    picture_file = url_for('static', filename='images/' + High.picture)
    return render_template('high.html', students=students, picture=picture_file)

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

@app.route("/search_h", methods=['GET'])
@login_required
def search_h():
    query = request.args.get('query', '').strip()
    if query:
        first_letter = query[0].lower()
        results = High.query.filter(High.studentname.ilike(f'{first_letter}%')).all()
    else:
        results = []
    return render_template('search_h.html', results=results)


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/images', picture_fn)
    form_picture.save(picture_path)

    return picture_fn
    

@app.route("/campus_beneficiary", methods=['GET', 'POST'])
@login_required
def campus_beneficiary():
    form = StudentForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)

        student = Student(
            studentname=form.studentname.data, 
            user_id=current_user.id, 
            addmission=form.addmission.data,
            school=form.school.data, 
            year=form.year.data, 
            course=form.course.data, 
            description=form.description.data,
            picture = picture_file
        )
        db.session.add(student)
        db.session.commit()
        flash(f'The student as been added successfully!', 'success')
        return redirect(url_for('campus'))
    return render_template('campus_beneficiary.html', title ='campus_beneficiary', form=form)

@app.route("/highschool_beneficiary", methods=['GET', 'POST'])
@login_required
def high_beneficiary():
    form = HighForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)

        student = High(
            studentname=form.studentname.data, 
            user_id=current_user.id, 
            addmission=form.addmission.data,
            school=form.school.data, 
            form=form.form.data, 
            description=form.description.data,
            picture = picture_file
        )
        db.session.add(student)
        db.session.commit()
        flash(f'The student as been added successfully!', 'success')
        return redirect(url_for('high'))
    return render_template('high_beneficiary.html', title ='high_beneficiary', form=form)

@app.route("/campus/<int:beneficiary_id>")
@login_required
def beneficiary(beneficiary_id):
    beneficiary = Student.query.filter_by(id=beneficiary_id, user_id=current_user.id).first_or_404()
    return render_template('beneficiary.html', title=beneficiary.studentname, beneficiary=beneficiary)

@app.route("/high/<int:beneficiary_id>")
@login_required
def beneficiary_h(beneficiary_id):
    beneficiary = High.query.filter_by(id=beneficiary_id, user_id=current_user.id).first_or_404()
    return render_template('beneficiary_h.html', title=beneficiary.studentname, beneficiary=beneficiary)

@app.route("/register", methods=['GET', 'POST']) 
def register():
    if current_user.is_authenticated:
        return redirect(url_for('campus'))
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
        return redirect(url_for('campus'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            flash(f"Your are logged in as { form.username.data }", 'success')
            login_user(user, remember=form.remember.data)
            return redirect(url_for('campus'))
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
    students = Student.query.filter_by(user_id=current_user.id).all()
    return render_template('description.html', students=students)


@app.route("/campus/<int:beneficiary_id>/delete")
@login_required
def delete_beneficiary(beneficiary_id):
    beneficiary = Student.query.filter_by(id=beneficiary_id, user_id=current_user.id).first_or_404()
    db.session.delete(beneficiary)
    db.session.commit()
    flash(f'Student {beneficiary.studentname} successfullly deleted', 'success')
    return redirect(url_for('campus'))

@app.route("/high/<int:beneficiary_id>/delete")
@login_required
def delete_beneficiary_h(beneficiary_id):
    beneficiary = High.query.filter_by(id=beneficiary_id, user_id=current_user.id).first_or_404()
    db.session.delete(beneficiary)
    db.session.commit()
    flash(f'Student {beneficiary.studentname} successfullly deleted', 'success')
    return redirect(url_for('high'))


# @app.route("/campus/<int:beneficiary_id>/update")
# @login_required
# def update_beneficiary(beneficiary_id):
#     beneficiary = Student.query.filter_by(id=beneficiary_id, user_id=current_user.id).first_or_404()
#     form = StudentForm()
#     if form.validate_on_submit():
#         if form.picture.data:
#             picture_file = save_picture(form.picture.data)

#         student = Student(
#             studentname=form.studentname.data, 
#             user_id=current_user.id, 
#             addmission=form.addmission.data,
#             school=form.school.data, 
#             year=form.year.data, 
#             course=form.course.data, 
#             description=form.description.data,
#             picture = picture_file
#         )
#         db.session.add(student)
#         db.session.commit()
#         flash(f'The student as been added successfully!', 'success')
#         return redirect(url_for('campus'))
#     db.session.update(beneficiary)
#     db.session.commit()
#     flash(f"Student {beneficiary.studentname}'s deatils successfullly updated", 'success')
#     return redirect(url_for('campus'))