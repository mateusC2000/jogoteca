import os
from jogoteca import app

def recover_image(name):
    for file_name in os.listdir(app.config['UPLOAD_PATH']):
        if f'{name}' in file_name:
            return file_name
    
    return 'capa_padrão.jpg'

def delete_file(name):
    file = recover_image(name)
    if file != 'capa_padrão.jpg':
        os.remove(os.path.join(app.config['UPLOAD_PATH'], file))