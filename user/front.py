from flask import Flask
from flask import render_template, flash, redirect, url_for, request
from user import views
from flask import Blueprint

from flask import jsonify

#user = Blueprint('user',__name__)
#from .. import conf


bp = Blueprint("mul", __name__, url_prefix="/bookstore")
#player1 = auth.Auth("http://127.0.0.1:5000/")
player1 = views.Auth()

@bp.route("/register",methods=['GET', 'POST'])
def register():
    from user.form import RegisterForm
    forms = RegisterForm(request.form)
    if request.method == 'POST' and forms.validate():
        # flash('Thanks for registering')
        # return redirect(url_for('login'))
        return str(player1.register(forms.username.data, forms.password.data))#返回值要修改
    return render_template('register.html', form=forms)

@bp.route("/login",methods=['GET','POST'])
def login():
    from user.form import LoginForm
    forms = LoginForm(request.form)
    if request.method == 'POST' and forms.validate():
        player1.login(forms.username.data, forms.password.data, "xx")#终端要修改
        return "success"
    return render_template('login.html',form = forms)











