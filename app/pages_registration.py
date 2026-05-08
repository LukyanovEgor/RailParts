import dash
from app.pages import (home_layout,
                    catalog_layout,
                    types_docs_layout,
                    register_layout,
                    login_layout)


def page_registration():

    dash.register_page('RailParts', path='/', title='RailParts', layout=home_layout)
    dash.register_page('Catalog', path='/original_catalogs', title='Catalog', layout=catalog_layout)

    dash.register_page('Types', path_template='/original_catalogs/<train_type_id>', title='Catalog', layout=types_docs_layout)

    dash.register_page('Auth-register', path='/signup', title='Регистрация', layout=register_layout)
    dash.register_page('Auth-login', path='/signin', title='Вход в аккаунт', layout=login_layout)