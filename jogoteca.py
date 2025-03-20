from flask import Flask, render_template

class Game:
    def __init__(self, name, category, console):
        self.name=name
        self.category=category
        self.console=console

app = Flask(__name__)

@app.route('/home')
def hello():
    game1= Game('God Of War Ragnarök', 'Rack n Slash', 'PS5')
    game2= Game('The Sims', 'Teen', 'PS4')
    game3= Game('Free Fire', 'Royale', 'Mobile')
    game4= Game('Pro Evolution Soccer 2009', 'Sport', 'PS2')
    game5= Game('Call Of Duty', 'FPS', 'PC')
    game6= Game('Mortal Kombat', 'Fight', 'PS3')
    


    game_list = [game1, game2, game3, game4, game5, game6]

    return render_template('list.html', title='Jogos', games=game_list)

app.run()