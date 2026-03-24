from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, current_user
from app.models import User

bp = Blueprint('auth', __name__)

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if username == 'feizi' and password == 'feizi':
            user = User(id=1, username='feizi')
            login_user(user)
            flash('登录成功！', 'success')
            return redirect(url_for('main.index'))
        else:
            flash('用户名或密码错误', 'error')

    return render_template('auth/login.html')

@bp.route('/logout')
def logout():
    logout_user()
    flash('已退出登录', 'info')
    return redirect(url_for('main.index'))
