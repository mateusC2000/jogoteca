import os
from jogoteca import app
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, validators

class FormGame(FlaskForm):
    name = StringField('Nome do Jogo', [validators.DataRequired(), validators.Length(min=1, max=50)])
    category = StringField('Categoria', [validators.DataRequired(), validators.Length(min=1, max=40)])
    console = StringField('Console', [validators.DataRequired(), validators.Length(min=1, max=20)])
    salvar = SubmitField('Salvar')
    
def recover_image(name):
    for file_name in os.listdir(app.config['UPLOAD_PATH']):
        if f'{name}' in file_name:
            return file_name
    
    return 'capa_padrão.jpg'

def delete_file(name):
    file = recover_image(name)
    if file != 'capa_padrão.jpg':
        os.remove(os.path.join(app.config['UPLOAD_PATH'], file))