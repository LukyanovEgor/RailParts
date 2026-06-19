from dash import html, dcc
from app.db import get_db
from app.models import Users


class ProfileBar:
    def __init__(self, user_id=None):

        if user_id is None:
            self.links = [
                html.P("Произошла ошибка!", className="profile-link")
            ]
        else:

            db = get_db()

            user = db.query(Users).filter(Users.user_id == user_id).first()

            self.links = [
                dcc.Link('Профиль', href=f"/profile/{user_id}", className="profile-link"),
            ]

            if user and user.is_admin:
                self.links.append(
                    dcc.Link('Администрирование', href="/admin", className="profile-link")
                )

            self.links.append(
                html.A('Выйти', href="/auth/logout", className="profile-link")
            )

        self.profile_bar = html.Div([
            html.H2("Меню", className="profile-title"),

            # Ссылки выстроены в столбик
            html.Div(self.links, className="profile-links"),

            # Кнопка под ссылками
            html.Button("Закрыть", id="close-profile-btn", className="btn_style_profile")
        ], className="profile-bar")

    def __call__(self, *args, **kwargs):
        return self.profile_bar