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
        idCard = request.form.get('idCard')
        admin = Admin.query.filter_by(Id=idCard).first()
        if not admin:
            flash("admin not exist")
            return redirect(url_for('auth.login'))
        if admin.password == request.form.get('password'):
            session['username'] = admin.name
            session['id'] = admin.Id
            return redirect(url_for('main.home'))
        else:
            flash("incorrect password")
            return redirect(url_for('auth.login'))
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