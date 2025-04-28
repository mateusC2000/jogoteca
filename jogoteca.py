from flask import Flask, render_template, request, redirect, session, flash, url_for
from flask_sqlalchemy import SQLAlchemy

class Game:
    def __init__(self, name, category, console):
        self.name=name
        self.category=category
        self.console=console
    
game1= Game('God Of War Ragnarök', 'Rack n Slash', 'PS5')
game2= Game('The Sims', 'Teen', 'PS4')
game3= Game('Free Fire', 'Royale', 'Mobile')
game4= Game('Pro Evolution Soccer 2009', 'Sport', 'PS2')
game5= Game('Call Of Duty', 'FPS', 'PC')
game6= Game('Mortal Kombat', 'Fight', 'PS3')



game_list = [game1, game2, game3, game4, game5, game6]

class User:
    def __init__(self, email, username, password):
        self.email=email
        self.username=username
        self.password=password

user1= User('mateus@campos.com', 'Teu', 'breakingbad')
user2= User('julia@campos.com', 'Maju', 'narutinho')
user3= User('vanessa@campos.com', 'Nessa', 'salvejorge')

users = { 
    user1.username : user1,
    user2.username : user2,
    user3.username : user3
}

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

@app.route('/')
def index():
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

    game = Game(name, category, console)
    game_list.append(game)

    return redirect(url_for('index'))

@app.route('/login')
def login():
    next_page = request.args.get('next')
    return render_template('login.html', next=next_page)

@app.route('/authenticate', methods=['POST'])
def authenticate():
    if request.form['user'] in users:
        user = users[request.form['user']]
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