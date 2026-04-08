import dash
from .pages import home_layout, catalog_layout, types_docs_layout


def page_registration():

    dash.register_page('RailParts', path='/', title='RailParts', layout=home_layout)
    dash.register_page('Catalog', path='/original_catalogs', title='Catalog', layout=catalog_layout)

    # dash.register_page('Types', path='/original_catalogs/<train_type_id>', title='Catalog', layout=types_docs_layout)

    dash.register_page('Types', path='/original_catalogs/2', title='Catalog', layout=types_docs_layout)





