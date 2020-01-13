'''
此类用于预定酒店,查询有关信息
'''
import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, escape
)
from werkzeug.security import check_password_hash, generate_password_hash
from forms import *
from functools import wraps

from app import db
from api import *
import uuid

from models import *

bp = Blueprint('main', __name__)

# Login required decorator.
def login_required(test):
    @wraps(test)
    def wrap(*args, **kwargs):
        if 'username' in session:
            return test(*args, **kwargs)
        else:
            flash('You need to login first.',category='error')
            return redirect(url_for('auth.login'))
    return wrap

@bp.route('/')
def home():
    return render_template('pages/placeholder.home.html')

@bp.route('/about')
def about():
    return render_template('pages/placeholder.about.html')


@bp.route('/insert_room',methods=['GET','POST'])
@login_required
def insert_room():
    form = InsertRoom(request.form)
    if request.method == 'POST':
        Id = request.form.get('Id')
        roomType = request.form.get('roomType')
        if not all([roomType,Id]):
            flash ('参数不完整',category='error')
            return redirect(url_for('main.insert_room'))
        info = {
            'Id' : Id,
            'roomType' : roomType
        }
        new_room(info)
    return render_template('forms/insert_room.html',form=form)

@bp.route('/change_room_price',methods=['GET','POST'])
@login_required
def change_room_price():
    form = ChangeRoomPrice(request.form)
    names = ['single','double','king','triple']
    previous = get_room_price_all()
    if request.method == 'POST':
        for name in names:
            #获取表单数据
            price = request.form.get(name,None)
            #如果price为None，表示没有输入，则不修改
            if not price:
                continue
            info = {
                'name' : name,
                'price' : price
            }
            change_price(info)
        return render_template('pages/placeholder.home.html')
    return render_template('forms/change_room_price.html',form=form,previous=previous)

@bp.route('/reserve',methods=['GET','POST'])
@login_required
def reserve():
    '''
    确定预订订单的入住时间，离店时间，房间类型
    '''
    if request.method == 'POST':
        session['beginDate']=request.form.get('beginDate')
        session['endDate'] =request.form.get('endDate')
        return redirect(url_for('main.choose_room_type'))
    form = ReverseRoom(request.form)
    rooms=get_room_price_all()
    return render_template('forms/reserve.html', rooms=rooms,form=form)

@bp.route('/choose_room_type',methods=['GET','POST'])
@login_required
def choose_room_type():
    rooms=get_room_price_all() #获取每种房间类型对应的价格
    beginDate = str(escape(session['beginDate']))
    endDate = str(escape(session['endDate']))
    types = Room_type.types
    remains = dict()
    for tp in types:
        info = {
            'roomType' : tp,
            'beginDate': beginDate,
            'endDate': endDate
        }
        remain=get_empty_room(info) #获得所选类型的空房间房号
        remains[tp] = len(remain) #获得空房间数量
    return render_template('forms/choose_room_type.html',rooms=rooms,remains=remains)

@bp.route('/reserve_info',methods=['GET','POST'])
@login_required
def reserve_info():
    '''
    获取预定人的信息
    '''
    if request.method == 'POST':
        name = request.form.get('name',None)
        phone = request.form.get('phone',None)
        roomId = request.form.get('roomId',None)
        Id = request.form.get('Id',None) #顾客身份证号

        #如果用户还不再数据库中
        if customer_not_in_db(Id):
            new_customer({
                'Id':Id,
                'name':name,
                'phone':phone
            })

        #生成订单
        print (session['roomType'])
        print ()
        print ()
        print ()
        order = Order(
            Id=generator_id(), #生成订单号
            state=Order.RESERVATION,
            roomId=roomId,
            roomType=session['roomType'],
            beginDate=session['beginDate'],
            endDate=session['endDate'],
            phone=phone,
            adminId=session['id'],
            reserveId=Id,
            paid='0'
        )
        db.session.add(order)
        db.session.commit()
        flash("reserve successfully",category='info')
        return redirect(url_for('main.home'))

    form = ReverseInfo(request.form)
    rooms=get_room_price_all()
    beginDate = str(escape(session['beginDate']))
    endDate = str(escape(session['endDate']))
    roomType = request.args.get('roomType')
    session['roomType'] = roomType
    info = {
        'roomType' : roomType,
        'beginDate': beginDate,
        'endDate': endDate
    }
    remain=get_empty_room(info) #获得所选类型的空房间房号
    form.roomId.choices = []
    for i in remain:
        form.roomId.choices.append((i,i))
    return render_template('forms/reserve_info.html', rooms=rooms,form=form)

@bp.route('/checkIn',methods=['GET','POST'])
@login_required
def checkIn():
    '''
    登记入住
    '''
    Id = None #预订者身份证号
    try:
        Id = request.form.get('Id')
    except:
        flash('no reservation or wrong id',category='error')
        return redirect(url_for('main.checkIn'))
    if Id:
        orders = Order.query.filter_by(reserveId=Id,state='0').all()
        if not len(orders):
            return redirect(url_for('main.checkIn'))
        return render_template('forms/checkIn.html',orders=orders)
    return render_template('forms/checkIn.html')

@bp.route('/get_tenant_info',methods=['GET','POST'])
@login_required
def get_tenant_info():
    '''
    获取入住人信息 姓名和身份证号
    '''
    if request.method=='POST':
        orderId = request.args.get('orderId',None)
        res = Order.query.filter_by(Id=orderId).first()

        name = request.form.get('name1',None)
        Id = request.form.get('Id1',None)
        if name:
            if customer_not_in_db(Id):
                new_customer({
                    'Id':Id,
                    'name':name
                })
            res.Id1 = Id

        name = request.form.get('name2',None)
        Id = request.form.get('Id2',None)
        if name:
            if customer_not_in_db(Id):
                new_customer({
                    'Id':Id,
                    'name':name
                })
            res.Id2 = Id

        name = request.form.get('name3',None)
        Id = request.form.get('Id3',None)
        if name:
            if customer_not_in_db(Id):
                new_customer({
                    'Id':Id,
                    'name':name
                })
            res.Id3 = Id

        res.state = Order.CURRENT #修改订单状态为已入住
        db.session.commit()
        flash("入住成功",category='info')
        return redirect(url_for('main.home'))

    form=TenantInfo(request.form)
    return render_template('forms/get_tenant_info.html',form=form)

@bp.route('/checkOut',methods=['GET','POST'])
@login_required
def checkOut():
    if request.method=='POST':
        roomId = request.form.get('roomId')
        order = Order.query.filter_by(roomId=roomId,state=Order.CURRENT).first()
        if not order:
            flash('该房间无订单',category='error')
            return redirect(url_for('main.checkOut'))
        order.state = Order.END
        db.session.commit()
        flash('check out successfully',category='info')
        return redirect(url_for('main.home'))
    form=CheckOut(request.form)
    return render_template('forms/checkOut.html',form=form)