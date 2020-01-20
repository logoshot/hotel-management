#coding=utf-8
'''
数据库模型文件
运行此文件可创建数据库表
'''
CREATE = 1
if __name__ == '__main__':
    CREATE = 0
if CREATE:
    from app import db
else:
    from flask import Flask 
    from flask_sqlalchemy import SQLAlchemy
    import pymysql
    # from flask.ext.sqlalchemy import SQLAlchemy
    db = SQLAlchemy()
    app = Flask(__name__)
    app.config.from_object('config')
    db.__init__(app)

class Customer(db.Model):
    __tablename__ = "customers"
    Id = db.Column(db.String(30), primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    phone = db.Column(db.String(20), nullable=True)
    password = db.Column(db.String(50))
    gender = db.Column(db.String(20))
    email = db.Column(db.String(50))
    age = db.Column(db.String(30))
    birthday = db.Column(db.String(50))
    address = db.Column(db.String(100))

    def __init__(self,Id='0',name=None,phone=None,password=None,gender=None,email=None,age=None,birthday=None,address=None,info=None):
        if info:
            self.Id = info.get('Id')
            self.name = info.get('name')
            self.phone = info.get('phone')
            self.password = info.get('password')
            self.gender = info.get('gender')
            self.email = info.get('email')
            self.age = info.get('age')
            self.birthday = info.get('birthday')
            self.address = info.get('address')
            return
        self.Id = Id
        self.name = name
        self.phone = phone
        self.password = password
        self.gender = gender
        self.email = email
        self.age = age
        self.birthday = birthday
        self.address = address

class Admin(db.Model):
    __tablename__ = "admins"
    Id = db.Column(db.String(30), primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    phone = db.Column(db.String(20), nullable=True)
    password = db.Column(db.String(50))
    gender = db.Column(db.String(20))
    email = db.Column(db.String(50))
    age = db.Column(db.String(30))
    birthday = db.Column(db.String(50))
    address = db.Column(db.String(100))

    def __init__(self,Id='0',name=None,phone=None,password=None,gender=None,email=None,age=None,birthday=None,address=None,info=None):
        if info:
            self.Id = info.get('Id')
            self.name = info.get('name')
            self.phone = info.get('phone')
            self.password = info.get('password')
            self.gender = info.get('gender')
            self.email = info.get('email')
            self.age = info.get('age')
            self.birthday = info.get('birthday')
            self.address = info.get('address')
            return
        self.Id = Id
        self.name = name
        self.phone = phone
        self.password = password
        self.gender = gender
        self.email = email
        self.age = age
        self.birthday = birthday
        self.address = address

class Room_type(db.Model):
    '''
    name : single double king triple
    '''
    __tablename__ = "room_types"
    name = db.Column(db.String(50), primary_key=True)
    price = db.Column(db.String(30), nullable=True)
    types = ['single','double','king','triple']

    def __init__(self,Id='0',name=None,price=None,info=None):
        if info:
            try:
                self.name = info.get('name')
                self.price = info.get('price')
            except:
                pass
            return
        self.name = name
        self.price = price

class Room(db.Model):
    __tablename__ = "rooms"
    Id = db.Column(db.String(30), primary_key=True)
    roomType = db.Column(db.String(50),nullable=True)

    def __init__(self,Id='0',roomType='single',info=None):
        if info:
            try:
                self.Id = info.get('Id')
                self.roomType = info.get('roomType')
            except:
                pass
            return
        self.Id = Id
        self.roomType = roomType

class Order(db.Model):
    __tablename__ = 'orders'
    RESERVATION = "0"
    CURRENT = "1"
    END = "2"
    Id = db.Column(db.String(30), primary_key=True) # 订单号
    state = db.Column(db.String(10), nullable=False) #订单状态 0:reservation 1:in 2:history
    roomId = db.Column(db.String(30), nullable=False) #房间号
    roomType = db.Column(db.String(30), nullable=False) #房间类型
    price = db.Column(db.String(20), nullable=True) #总价
    beginDate = db.Column(db.String(30), nullable=True) #入住日期
    endDate = db.Column(db.String(30), nullable=True) #离店日期
    days = db.Column(db.String(30), nullable=True) # 入住天数
    beginTime = db.Column(db.String(30), nullable=True) #入住时间，精确到分
    endTime = db.Column(db.String(30), nullable=True) #离店时间，精确到分
    phone = db.Column(db.String(30), nullable=True) #顾客联系方式
    reserveId = db.Column(db.String(50), nullable=True) #预订人id
    Id1 = db.Column(db.String(50), nullable=True) #住客id
    Id2 = db.Column(db.String(50), nullable=True) #住客id
    Id3 = db.Column(db.String(50), nullable=True) #住客id
    paid = db.Column(db.String(30), nullable=True) #是否付款
    adminId = db.Column(db.String(30), nullable=True) #操作管理员id

    def __init__(self,Id='0',state=None,roomId=None,roomType=None,price=None,\
        beginDate=None,endDate=None,beginTime=None,endTime=None,Id1=None,Id2=None,Id3=None,\
        phone=None,reserveId=None,customerId=None,paid='0',adminId=None,info=None):
        if info:
            try:
                self.Id = info.get('Id')
                self.state = info.get('state')
                self.roomId = info.get('roomId')
                self.roomType = info.get('roomType')
                self.price = info.get('price')
                self.beginDate = info.get('beginDate')
                self.endDate = info.get('endDate')
                self.beginTime = info.get('beginTime')
                self.endTime = info.get('endTime')
                self.phone = info.get('phone')
                self.reserveId = info.get('reserveId')
                self.customerId = info.get('customerId')
                self.paid = info.get('paid')
                self.adminId = info.get('adminId')
                self.Id1 = info.get('Id1')
                self.Id2 = info.get('Id2')
                self.Id3 = info.get('Id3')
            except:
                pass
            return
        self.Id = Id
        self.state = state
        self.roomId = roomId
        self.roomType = roomType
        self.price = price
        self.beginDate = beginDate
        self.endDate = endDate
        self.beginTime = beginTime
        self.endTime = endTime
        self.phone = phone
        self.reserveId = reserveId
        self.customerId = customerId
        self.paid = paid
        self.adminId = adminId
        self.Id1 = Id1
        self.Id2 = Id2
        self.Id3 = Id3


'''
class Check_in(db.Model):
    __tablename__ = "check_in"
    Id = db.Column(db.String(30), primary_key=True)
    roomId = db.Column(db.String(30), nullable=False)
    price = db.Column(db.String(30), nullable=False)
    beginDate = db.Column(db.String(30), nullable=True)
    endDate = db.Column(db.String(30), nullable=True)
    customerId = db.Column(db.String(30), nullable=True) #多个住客时用逗号隔开姓名
    paid = db.Column(db.String(30), nullable=True) #已付款金额
    endFlag = db.Column(db.String(5), nullable=False)



class User(db.Model)
    __tablename__ = "users"
    Id = db.Column(db.String(50), primary_key=True)
    name = db.Column(db.String(50), nullable=True,unique=True) #不一定是姓名
    sex = db.Column(db.String(20), nullable=True)
    phone = db.Column(db.String(20), nullable=True)
    idCard = db.Column(db.String(30), nullable=True)
    password = db.Column(db.String(30), nullable=True)
    email = db.Column(db.String(30),nullable=True)

    def __init__(self,Id='0',name=None,sex=None,phone=None,idCard=None,password=None,email=None,info=None):
        if info:
            self.Id = info['Id']
            self.name = info['name']
            self.sex = info['sex']
            self.phone = info['phone']
            self.idCard = info['idCard']
            self.password = info['password']
            self.email = info['email']
            return
        self.Id = Id
        self.name = name
        self.sex = sex
        self.phone = phone
        self.idCard = idCard
        self.password = password
        self.email = email

    def to_dict(self):
        dic = {
            "Id": self.Id,
            "name": self.name,
            "sex": self.sex,
            "phone": self.phone,
            "idCard": self.idCard,
            "password": self.password
        }
        return dic
        '''

if not CREATE:
    db.drop_all()
    db.create_all()
    from random import choice
    def create_rooms():
        names = ['single','double','king','triple']

        num = 10
        for i in range(num):
            room = Room(Id=str(i),roomType=choice(names))
            db.session.add(room)
    
        for name in names:
            cur = Room_type(name=name,price='111')
            db.session.add(cur)

        admin = Admin(Id='1',name='first',phone='111',password='123')
        db.session.add(admin)
    
        db.session.commit()
    create_rooms()