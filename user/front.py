from flask import render_template, request
from test import auth
from flask import Blueprint
bp = Blueprint("mul", __name__, url_prefix="/bookstore")
player1 = auth.Auth("http://127.0.0.1:5000/")

@bp.route("/register",methods=['GET', 'POST'])
def register():
    from test import RegisterForm
    forms = RegisterForm(request.form)
    if request.method == 'POST' and forms.validate():
        # flash('Thanks for registering')
        # return redirect(url_for('login'))
        return str(player1.register(forms.username.data, forms.password.data))#返回值要修改
    return render_template('register.html', form=forms)

@bp.route("/unregister",methods=['GET','POST'])
def unregister():
    from test import UnregisterForm
    forms = UnregisterForm(request.form)
    if request.method == 'POST' and forms.validate():
        player1.unregister(forms.username.data,forms.password.data)
        return 'success'
    return render_template('unregister.html',form=forms)

@bp.route("/login",methods=['GET','POST'])
def login():
    from test import LoginForm
    forms = LoginForm(request.form)
    if request.method == 'POST' and forms.validate():
        player1.login(forms.username.data, forms.password.data, "xx")#终端要修改
        return "success"
    return render_template('login.html',form = forms)

@bp.route("/logout",methods=['GET','POST'])
def logout():
    from test import LogoutForm
    forms = LogoutForm(request.form)
    if request.method == 'POST' and forms.validate():
        token = player1.getToken(forms.username.data)
        player1.logout(forms.username.data,token)
        return 'success'
    return render_template('logout.html',form=forms)

@bp.route("/password",methods=['GET','POST'])
def password():
    from test import PasswordForm
    forms = PasswordForm(request.form)
    if request.method == 'POST' and forms.validate():
        player1.password(forms.username.data,forms.oldpassword.data,forms.newpassword.data)
        return 'success'
    return render_template('password.html',form=forms)

@bp.route("/homepage",methods=['GET'])
def homepage():
    return render_template('homepage.html')













