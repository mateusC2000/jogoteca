from flask import render_template, request, redirect, session, flash, url_for, send_from_directory
from jogoteca import app, db
from models import Games, Users

@app.route('/')
def index():
    game_list = Games.query.order_by(Games.id)
    return render_template('list.html', title='Jogos', games=game_list)

@app.route('/new')
def new():
    if 'current_user' not in session or session['current_user'] == None:
        return redirect(url_for('login', next=url_for('new')))
    return render_template('new.html', title='New Game')

@app.route('/create', methods=['POST'])
def create():
    name = request.form['name']
    category = request.form['category']
    console = request.form['console']

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
    file.save(f'{upload_path}/{new_game.name}.jpg')

    return redirect(url_for('index'))

@app.route('/edit/<int:id>')
def edit(id):
    if 'current_user' not in session or session['current_user'] == None:
        return redirect(url_for('login', next=url_for('edit', id=id)))
    game = Games.query.filter_by(id=id).first()
    return render_template('edit.html', title='Edit Game', game=game)

@app.route('/update', methods=['POST'])
def update():
    game = Games.query.filter_by(id=request.form['id']).first()
    game.name = request.form['name']
    game.category = request.form['category']
    game.console = request.form['console']

    db.session.add(game)
    db.session.commit()
    flash('Jogo atualizado com sucesso!')

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