from flask import render_template, request, redirect, session, flash, url_for, send_from_directory
from jogoteca import app, db
from models import Games, Users
from helpers import recover_image, delete_file, FormGame
import time 

@app.route('/')
def index():
    game_list = Games.query.order_by(Games.id)
    return render_template('list.html', title='Jogos', games=game_list)

@app.route('/new')
def new():
    if 'current_user' not in session or session['current_user'] == None:
        return redirect(url_for('login', next=url_for('new')))

    form = FormGame()
    return render_template('new.html', title='New Game', form=form)

@app.route('/create', methods=['POST'])
def create():

    form = FormGame(request.form)

    if not form.validate_on_submit():
        return redirect(url_for('new'))

    name = form.name.data
    category = form.category.data
    console = form.console.data

    game = Games.query.filter_by(name=name).first()

    if game:
        flash('Jogo já existente')
        return redirect(url_for('index'))
    
    new_game = Games(name=name, category=category, console=console)
    db.session.add(new_game)
    db.session.commit()
    flash('Jogo adicionado com sucesso!')

    file = request.files['file']
    upload_path = app.config['UPLOAD_PATH']
    timestamp = time.time()
    file.save(f'{upload_path}/{new_game.name}-{timestamp}.jpg')

    return redirect(url_for('index'))

@app.route('/edit/<int:id>')
def edit(id):
    if 'current_user' not in session or session['current_user'] == None:
        return redirect(url_for('login', next=url_for('edit', id=id)))
    game = Games.query.filter_by(id=id).first()
    game_cover = recover_image(game.name)
    return render_template('edit.html', title='Edit Game', game=game, game_cover=game_cover)

@app.route('/update', methods=['POST'])
def update():
    game = Games.query.filter_by(id=request.form['id']).first()
    game.name = request.form['name']
    game.category = request.form['category']
    game.console = request.form['console']

    db.session.add(game)
    db.session.commit()
    flash('Jogo atualizado com sucesso!')

    file = request.files['file']
    upload_path = app.config['UPLOAD_PATH']
    timestamp = time.time()
    delete_file(game.name)
    file.save(f'{upload_path}/{game.name}-{timestamp}.jpg')

    return redirect(url_for('index'))

@app.route('/delete/<int:id>')
def delete(id):
    if 'current_user' not in session or session['current_user'] == None:
        return redirect(url_for('login'))
    
    Games.query.filter_by(id=id).delete()
    db.session.commit()
    flash('Jogo deletado com sucesso!')

    return redirect(url_for('index'))

@app.route('/login')
def login():
    next_page = request.args.get('next')
    return render_template('login.html', next=next_page)

@app.route('/authenticate', methods=['POST'])
def authenticate():
    user = Users.query.filter_by(username=request.form['user']).first()
    if user:
        if request.form['password'] == user.password:
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

@app.route('/uploads/<file_name>')
def image(file_name):
    return send_from_directory('uploads', file_name)

