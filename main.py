from app.pages_registration import page_registration
from flask import Flask, send_from_directory, request, redirect
from app.routes.auth import auth_bp
import dash
import os



server = Flask(__name__)
server.secret_key = os.urandom(24)  # В продакшене используйте фиксированный секрет

server.register_blueprint(auth_bp)

app = dash.Dash(__name__, use_pages=True, server=server, pages_folder='app/pages')


page_registration()

app.layout = dash.page_container


server = app.server


@server.before_request
def protect_catalog_route():
    if request.method == 'GET' and request.path.startswith('/original_catalogs'):
        if not request.cookies.get('auth_token'):
            return redirect('/signin')

#---------------------------------------------
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
