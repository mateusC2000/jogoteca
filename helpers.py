import os
from jogoteca import app

def recover_image(name):
    for file_name in os.listdir(app.config['UPLOAD_PATH']):
        if f'{name}.jpg' == file_name:
            return file_name
    
    return 'capa_padrão.jpg'