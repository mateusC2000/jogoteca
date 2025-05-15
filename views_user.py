from jogoteca import app
from flask import render_template, request, redirect, session, flash, url_for
from models import Users
from helpers import FormUser

@app.route('/login')
def login():
    next_page = request.args.get('next')
    form = FormUser()
    return render_template('login.html', next=next_page, form=form)

@app.route('/authenticate', methods=['POST'])
def authenticate():
    form = FormUser(request.form)
    user = Users.query.filter_by(username=form.username.data).first()
    if user:
        if form.password.data == user.password:
            session['current_user'] = user.username
            flash('Bem vindo, ' + user.username + '!')
            next_page = request.form['next']
            return redirect('/{}'.format(next_page))
        else:
            flash('Senha incorreta')
            return redirect(url_for('login'))
    else:
        flash('Erro ao logar')
        return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session['current_user'] = None
    flash('Logout efetuado com sucesso!')
    return redirect(url_for('login'))
