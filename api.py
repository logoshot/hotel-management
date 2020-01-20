from flask import flash
from models import *
from app import db
import uuid

def customer_not_in_db(Id):
    cus = Customer.query.filter_by(Id=Id).all()
    if len(cus):
        return False
    return True

def new_customer(info):
    if not info.get('password'):
        info['password'] = info['Id'][-6:]
    cus = Customer(info=info)
    db.session.add(cus)
    db.session.commit()
'''
def get_password(name):

    name = str(name)
    user = User.query.filter_by(name=name).first()
    if user:
        return user.password
    else:
        return None
'''
def save(object):
    db.session.add(object)
    db.session.commit()

def to_dict(info):
    '''
    默认为json格式
    '''
    if type(info)==dict:
        return info
    return info.loads()

def customer_register(info):
    '''
    顾客api
    刷身份证时注册
    注册成功返回true，并且修改数据库
    注册失败返回false,失败原因为顾客已存在
    '''
    info = to_dict(info)
    customer = Customer.query.filter_by(idCard=info.idCard).first()
    if customer:
        return False
    else :
        customer = Customer(info=info)
        save(customer)
        return True
'''
def user_register(info):

    info = to_dict(info)
    user = User.query.filter_by(idCard=info.idCard).first()
    if user:
        return False
    else :
        user = User(info=info)
        save(user)
        return True
'''
def get_room_price_all():
    '''
    获取所有房间类型的房价
    return : dict [房型] = 房价
    '''
    prices = Room_type.query.all()
    rooms = dict()
    for i in prices:
        if i.price:
            rooms[i.name] = int(i.price)
        else:
            rooms[i.name] = 0
    return rooms

def get_room_remain_all(info):
    '''获取所有房间剩余数量
    return : dict [房型] = 数量(int)
    '''
    ret = dict()
    for room in configure.roomtypes:
        ask = info
        ask['roomType'] = room
        ret[room] = len(get_empty_room(ask))
    return ret


def get_empty_room(info):
    '''
    查
    获取指定类型,指定时间内的剩余空房间号
    入住时用于选择房间
    return : string list
    '''
    info = to_dict(info)
    res = db.session.query(Room.Id).filter(Room.roomType==info['roomType']).all()
    all_room = [i.Id for i in res] # 所有该类型房间号
    res = db.session.query(Order.roomId).filter(Order.beginDate<info['endDate'], Order.endDate>info['beginDate']).all()
    for i in res:
        if i.roomId in all_room:
            all_room.remove(i.roomId)
    return all_room

def check_in(info):
    '''
    增
    入住确认函数，将入住信息写入数据库
    '''
    info = to_dict(info)
    order = Order(info=info)
    try:
        Order.query.get(info['Id']).delete()
    except:
        pass
    save(order)

def check_out(info):
    '''
    退房，修改数据库中订单状态
    '''
    info = to_dict(info)
    order = Order(info=info)
    try:
        Order.query.get(info['Id']).delete()
    except:
        pass
    save(order)

def new_room(info):
    '''
    新增房间
    return True: 新增成功
    return False: 新增失败
    '''
    info = to_dict(info)
    room = Room(info=info)
    print (info)
    print ()
    print ()
    try:
        save(room)
        flash('succeed to insert home')
    except :
        flash('failed to insert home')
        return False
    return True

def change_price(info):
    '''
    修改room_type房型房价
    '''
    info = to_dict(info)
    room_type = Room_type(info=info)
    print (room_type.name, room_type.price)
    try:
        ret = Room_type.query.filter_by(name=room_type.name).first()
        db.session.delete(ret)
        #flash('succeed to change room price')
    except:
        #flash('failed to change room price')
        return False
    save(room_type)
    return True

def check_order(info):
    '''
    info : roomId
    查询某个房间的当前订单
    退房时用
    '''
    info = to_dict(info)
    res = Order.query.filter(Order.roomId==info['roomId'])
    return res

def delete_reservation(Id):
    '''
    删除预定订单
    '''
    try:
        Order.query.get(Id).delete()
    except:
        return False
    return True

def query_reservation(userId):
    '''
    查询用户预定订单
    '''
    res = Order.query.filter(Order.userId==userId, Order.state==Order.RESERVATION).all()
    return res

def generator_id():
    ret = str(uuid.uuid1())
    ret = ret[:15]
    return ret