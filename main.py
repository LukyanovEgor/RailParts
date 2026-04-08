from dash import html

import dash
from app.pages_registration import page_registration




app = dash.Dash(__name__, use_pages=True, pages_folder='app/pages')



page_registration()

app.layout = dash.page_container


server = app.server


#---------------------------------------------
import os
from flask import send_from_directory
IMAGES_DIR = os.path.join(os.getcwd(), 'test_images')
# Создаём маршрут для раздачи файлов
@server.route('/test_images/<path:filename>')
def serve_image(filename):
    return send_from_directory(IMAGES_DIR, filename)


app.config.suppress_callback_exceptions = False
#---------------------------------------------


app.config.suppress_callback_exceptions = True

if __name__ == '__main__':
    app.run(debug=True, threaded=True)
