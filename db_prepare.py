import mysql.connector
from mysql.connector import errorcode

print('Conectando...')

try:
    conn = mysql.connector.connect(
        host='127.0.0.1',
        user='root',
        password='admin'
    )

except mysql.connector.Error as err:
    if err.errno == errorcode.ERACCESS_DENIED_ERROR:
        print('Existe algo errado no nome de usuário ou senha')
    else:
        print(err)
else:
    print('Conectado')

cursor = conn.cursor()

cursor.execute("DROP DATABASE IF EXISTS jogoteca;")

cursor.execute("CREATE DATABASE jogoteca;")

cursor.execute("USE jogoteca")

# criando tabelas
TABLES = {}

TABLES['games'] = ('''
    CREATE TABLE `jogoteca`.`games` (
      `id` INT NOT NULL AUTO_INCREMENT,
      `nome` VARCHAR(50) NOT NULL,
      `categoria` VARCHAR(40) NOT NULL,
      `console` VARCHAR(20) NOT NULL,
      PRIMARY KEY (`id`))
    ENGINE = InnoDB
    DEFAULT CHARACTER SET = utf8
    COLLATE = utf8_bin; ''')

TABLES['users'] = ('''
    CREATE TABLE `jogoteca`.`users` (      
      `nome` VARCHAR(50) NOT NULL,
      `nickname` VARCHAR(10) NOT NULL,
      `senha` VARCHAR(100) NOT NULL,
      PRIMARY KEY (`nickname`))
    ENGINE = InnoDB
    DEFAULT CHARACTER SET = utf8
    COLLATE = utf8_bin;  ''')

for tabela_nome in TABLES:
    tabela_sql = TABLES[tabela_nome]
    try:
        print(f'Criando tabela {tabela_nome}')
        cursor.execute(tabela_sql)
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
            print('Tabela já existe')
        else:
            print(err.msg)
    else:
        print('ok')

# inserindo usuários
usuario_sql = 'INSERT INTO users (nome, nickname, senha) values (%s,%s,%s)'

users = [
    ('mateus@campos.com', 'Teu', 'breakingbad'),
    ('julia@campos.com', 'Maju', 'narutinho'),
]

cursor.executemany(usuario_sql,users)

cursor.execute('select * from jogoteca.users')
print('---------------- Usuários ----------------')
for user in cursor.fetchall():
    print(user[0])

# inserindo games
jogo_sql = 'INSERT INTO games (nome, categoria, console) values (%s,%s,%s)'

games = [
    ('God Of War Ragnarök', 'Rack n Slash', 'PS5'),
    ('The Sims', 'Teen', 'PS4'),
    ('Free Fire', 'Royale', 'Mobile'),
    ('Pro Evolution Soccer 2009', 'Sport', 'PS2'),
    ('Call Of Duty', 'FPS', 'PC'),
    ('Mortal Kombat', 'Fight', 'PS3'),
]

cursor.executemany(jogo_sql,games)

cursor.execute('select * from jogoteca.games')
print('---------------- games ----------------')
for jogo in cursor.fetchall():
    print(jogo[1])

# commitando pra gravar no banco
conn.commit()

cursor.close()
conn.close()