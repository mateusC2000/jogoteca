from flask import Flask, render_template, request, redirect, session, flash, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = 'alura'

app.config['SQLALCHEMY_DATABASE_URI'] = \
    '{SGBD}://{user}:{password}@{server}/{database}'.format(
        SGBD = 'mysql+mysqlconnector',
        user = 'root',
        password = 'admin',
        server = 'localhost',
        database = 'jogoteca'
    )

db = SQLAlchemy(app)

class Games(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False )
    category = db.Column(db.String(40), nullable=False )
    console = db.Column(db.String(20), nullable=False )

    def __repr__(self):
        return '<Name %r>' % self.name

class Users(db.Model):
    username = db.Column(db.String(10), primary_key=True)
    email = db.Column(db.String(50), nullable=False )
    password = db.Column(db.String(100), nullable=False )

    def __repr__(self):
        return '<Email %r>' % self.email

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
        flash('Erro ao logar')
        return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session['current_user'] = None
    flash('Logout efetuado com sucesso!')
    return redirect(url_for('login'))


app.run(debug=True)