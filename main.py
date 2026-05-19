from app import pages_registration
from app.pages_registration import page_registration
from flask import Flask, send_from_directory, request, redirect
from app.routes import auth_bp, orders_bp
import dash
import os



server = Flask(__name__)
server.secret_key = os.urandom(24)  # В продакшене используйте фиксированный секрет

server.register_blueprint(auth_bp)
server.register_blueprint(orders_bp)

app = dash.Dash(__name__, use_pages=True, server=server, pages_folder='app/pages')


page_registration()

app.layout = dash.page_container


server = app.server


@server.before_request
def protect_routes():
    # if request.method == 'GET' and request.path.startswith('/original_catalogs'):
    #     if not request.cookies.get('auth_token'):
    #         return redirect('/signin')

    import jwt
    if request.method != 'GET':
        return

    path = request.path

    if path.startswith('/original_catalogs'):
        if not request.cookies.get('auth_token'):
            return redirect('/signin')

        # 2️⃣ Защита админки: проверка user_id внутри JWT
    if path.startswith('/admin'):
        token = request.cookies.get('auth_token')

        if not token:
            return redirect('/signin')  # Токена нет → на вход

        try:

            payload = jwt.decode(
                token,
                "your-secret-key",
                algorithms=['HS256']
            )

            # Проверяем user_id
            user_id = payload.get('user_id')

            if int(user_id) != 1:
                return redirect('/')  # Не админ → на главную

        except jwt.ExpiredSignatureError:
            # Токен истёк
            return redirect('/signin')
        except jwt.InvalidTokenError:
            # Неверный токен


            return redirect('/signin')

IMAGES_DIR = os.path.join(os.getcwd(), 'test_images')
# Создаём маршрут для раздачи файлов
@server.route('/test_images/<path:filename>')
def serve_image(filename):
    return send_from_directory(IMAGES_DIR, filename)


app.config.suppress_callback_exceptions = True


if __name__ == '__main__':
    app.run(debug=True, threaded=True)
