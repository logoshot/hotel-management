'''
此类用于用户登入注册
'''

import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, escape
)
from werkzeug.security import check_password_hash, generate_password_hash


from models import *
from forms import *
import uuid

from app import db
from api import *


bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/login',methods=['GET','POST'])
def login():
    if request.method == 'POST':
        _type = request.form.get('type')
        if _type=='admin':
            idCard = request.form.get('idCard')
            admin = Admin.query.filter_by(Id=idCard).first()
            if not admin:
                flash("admin not exist")
                return redirect(url_for('auth.login'))
            if admin.password == request.form.get('password'):
                session['username'] = admin.name
                session['id'] = admin.Id
                session['type'] = 'admin'
                return redirect(url_for('main.home'))
            else:
                flash("incorrect password")
                return redirect(url_for('auth.login'))
        elif _type=='customer':
            idCard = request.form.get('idCard')
            customer = Customer.query.filter_by(Id=idCard).first()
            if not customer:
                flash("customer not exist")
                return redirect(url_for('auth.login'))
            if customer.password == request.form.get('password'):
                session['username'] = customer.name
                session['id'] = customer.Id
                session['type'] = 'customer'
                return redirect(url_for('main.home'))
            else:
                flash("incorrect password")
                return redirect(url_for('auth.login'))
        else:
            flash('type error'+str(_type))
    form = LoginForm(request.form)
    return render_template('forms/login.html', form=form)

@bp.route('/logout')
def logout():
    session.pop('username',None)
    session.pop('id',None)
    return redirect(url_for('main.home'))

@bp.route('/register',methods=['GET','POST'])
def register():
    if request.method == 'POST':
        name = request.form.get('name')
        idCard = request.form.get('idCard')
        check = Admin.query.filter_by(Id=idCard).first()
        if check:
            flash('admin already exist')
            return redirect(url_for('auth.register'))
        password = request.form.get('password')
        if not all([name,password,idCard]):
            flash ('参数不完整')
            return redirect(url_for('auth.register'))
        admin = Admin(Id=idCard,name=name,password=password)
        db.session.add(admin)
        db.session.commit()
        return redirect(url_for('auth.login'))
    form = RegisterForm(request.form)
    return render_template('forms/register.html', form=form)


@bp.route('/forgot')
def forgot():
    form = ForgotForm(request.form)
    return render_template('forms/forgot.html', form=form)

@bp.route('/profile',methods=['GET','POST'])
def update_profile():
    _type = session.get('type')
    if _type == "admin":
        form = Admin.query.filter_by(Id=session.get('id')).first()
    elif _type == "customer":
        form = Customer.query.filter_by(Id=session.get('id')).first()
    else:
        form = None
    if request.method == 'POST':
        if not form:
            flash('something went wrong')
            return redirect(url_for('main.home'))
        new = request.form
        form.name = new.get('name') if new.get('name') else form.name
        form.age = new.get('age') if new.get('age') else form.age
        form.email = new.get('email') if new.get('email') else form.email
        form.birthday = new.get('birthday') if new.get('birthday') else form.birthday
        form.address = new.get('address') if new.get('address') else form.address
        db.session.commit()
        flash('succeed')
        return redirect(url_for('main.home'))
    return render_template('forms/profile.html',form=form)

@bp.route('/change_password',methods=['GET','POST'])
def change_password():
    if request.method == 'POST':
        people = None
        if session.get('type')=="admin":
            people = Admin.query.filter_by(Id=session.get('id')).first()
        if session.get('type')=="customer":
            people = Customer.query.filter_by(Id=session.get('id')).first()
        if not people:
            return redirect(url_for('main.home'))
        if request.form.get('old_password')==people.password:
            if request.form.get('new_password'):
                people.password = request.form.get('new_password')
                db.session.commit()
                flash('change successfully')
                return redirect(url_for('main.home'))
            else:
                return redirect(url_for('main.home'))
        else:
            flash('incorrect old password '+request.form.get('old_password'))
            redirect(url_for('auth.change_password'))
    return render_template('forms/change_password.html')