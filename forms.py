from flask_wtf import Form
from wtforms import TextField, PasswordField, SelectField, RadioField
from wtforms.validators import DataRequired, EqualTo, Length

# Set your classes here.


class RegisterForm(Form):
    idCard = TextField(
        'idCard', validators=[DataRequired(), Length(min=6, max=18)]
    )
    name = TextField(
        'Username', validators=[DataRequired(), Length(min=6, max=25)]
    )
    password = PasswordField(
        'Password', validators=[DataRequired(), Length(min=6, max=40)]
    )
    confirm = PasswordField(
        'Repeat Password',
        [DataRequired(),
        EqualTo('password', message='Passwords must match')]
    )

class LoginForm(Form):
    idCard = TextField('idCard', [DataRequired(), Length(min=6, max=18)])
    password = PasswordField('Password', [DataRequired()])
    typ = RadioField('type',choices=[('admin','admin'),('customer','customer')])

class ForgotForm(Form):
    email = TextField(
        'Email', validators=[DataRequired(), Length(min=6, max=40)]
    )

class InsertRoom(Form):
    Id = TextField('Id', [DataRequired()])
    roomType = SelectField('roomType',
     choices=[('single','single'),('double','double'),('king','king'),('triple','triple')],
     validators=[DataRequired()]
    )

class ChangeRoomPrice(Form):
    single = TextField('single', [DataRequired()])
    double = TextField('double', [DataRequired()])
    king = TextField('king', [DataRequired()])
    triple = TextField('triple', [DataRequired()])

class ReverseRoom(Form):
    beginDate = TextField(label='beginDate',validators=[DataRequired()])
    endDate = TextField(label='endDate',validators=[DataRequired()])

class ReverseInfo(Form):
    '''
    name:预订人姓名
    phone:预订人电话
    roomId:想要预订的房间id
    Id:预订人身份证号
    '''
    name = TextField(label='name',validators=[DataRequired()])
    phone = TextField(label='phone',validators=[DataRequired()])
    roomId = SelectField(label='roomId',validators=[DataRequired()])
    Id = TextField(label='IdCard',validators=[DataRequired(), Length(min=6, max=18)])

class TenantInfo(Form):
    '''
    name:住客姓名
    Id:住客身份证号
    '''
    name1 = TextField(label='name',validators=[DataRequired()])
    Id1 = TextField(label='IdCard',validators=[DataRequired(), Length(min=6, max=18)])
    name2 = TextField(label='name')
    Id2 = TextField(label='IdCard',validators=[DataRequired(), Length(min=6, max=18)])
    name3 = TextField(label='name')
    Id3 = TextField(label='IdCard',validators=[DataRequired(), Length(min=6, max=18)])

class CheckOut(Form):
    roomId = TextField(label='roomId',validators=[DataRequired()])
