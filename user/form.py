# from flask_wtf import FlaskForm
from wtforms import TextField, SubmitField, PasswordField, BooleanField
from wtforms.validators import DataRequired, Email, Length, EqualTo

from wtforms import Form, BooleanField, TextField, PasswordField, validators
class RegisterForm(Form):
    password = PasswordField(
        validators=[
            DataRequired(message='密码不可以为空，请输入你的密码'),
            Length(3, 32, message='密码最小3位最长32位')
        ]
    )
    password2 = PasswordField(
        validators=[
            DataRequired(message='确认密码不能为空，请输入你的密码'),
            Length(3, 32, message='密码最小3位最长32位'),
            EqualTo('password', message="两次密码不一致!")
        ]
    )
    username = TextField(
        validators=[
            DataRequired(),
            Length(2, 10, message='昵称至少需要2个字符，最多10个字符')
        ]
    )
    submit = SubmitField('注册')

class UnregisterForm(Form):
    username = TextField(
        validators=[
            DataRequired(message='用户名不可以为空，请输入你的密码'),
            Length(2, 10, message='昵称至少需要2个字符，最多10个字符')
        ]
    )
    password = PasswordField(
        validators=[
            DataRequired(message='密码不可以为空，请输入你的密码'),
            Length(3, 32, message='密码最小3位最长32位')
        ]
    )
    submit = SubmitField('注销')

class LoginForm(Form):
    username = TextField(
        validators=[
            DataRequired(message='用户名不可以为空，请输入你的密码'),
            Length(2, 10, message='昵称至少需要2个字符，最多10个字符')
        ]
    )
    password = PasswordField(
        validators=[
            DataRequired(message='密码不可以为空，请输入你的密码'),
            Length(3, 32, message='密码最小3位最长32位')
        ]
    )
    submit = SubmitField('登录')

class LogoutForm(Form):
    username = TextField(
        validators=[
            DataRequired(message='用户名不可以为空，请输入你的密码'),
            Length(2, 10, message='昵称至少需要2个字符，最多10个字符')
        ]
    )
    submit = SubmitField('退出登录')


class PasswordForm(Form):
    username = TextField(
        validators=[
            DataRequired(message='用户名不可以为空，请输入你的密码'),
            Length(2, 10, message='昵称至少需要2个字符，最多10个字符')
        ]
    )
    oldpassword = PasswordField(
        validators=[
            DataRequired(message='密码不可以为空，请输入你的密码'),
            Length(3, 32, message='密码最小3位最长32位')
        ]
    )
    newpassword = PasswordField(
        validators=[
            DataRequired(message='密码不可以为空，请输入你的密码'),
            Length(3, 32, message='密码最小3位最长32位')
        ]
    )
    submit = SubmitField('修改密码')

