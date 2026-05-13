import dash
from dash import html, dcc, callback, Input, Output, ctx, ALL
from .layout import Layout
import random



# ==========================================
# 📦 ЗАГЛУШКА ДАННЫХ (потом заменишь на SQL/ORM)
# ==========================================
PRODUCTS = [
    {"id": 1, "code": "ZIC 132619", "article": "697988", "name": "Масло моторное ZIC X7 LS 5W-30 синтетическое 1 л",
     "img": "https://placehold.co/150x120/e9ecef/495057?text=ZIC"},
    {"id": 2, "code": "Лукойл 3149287", "article": "1310544",
     "name": "Масло моторное Лукойл Genesis Armortech HK 5W-30 синтетическое 4 л",
     "img": "https://placehold.co/150x120/e9ecef/495057?text=Lukoil"},
    {"id": 3, "code": "SANGSIN SD4204", "article": "421609",
     "name": "Диск тормозной передний NISSAN MURANO 03->/INFINITI M35/45",
     "img": "https://placehold.co/150x120/e9ecef/495057?text=Brake"},
    {"id": 4, "code": "ARNEZI N0002005", "article": "3011108",
     "name": "Антифриз ARNEZI Red G12+ готовый -40 красный 5 л",
     "img": "https://placehold.co/150x120/e9ecef/495057?text=Antifreeze"},
    {"id": 5, "code": "HYUNDAI/KIA 05100-00141", "article": "262324",
     "name": "Масло моторное HYUNDAI/KIA Turbo SYN A5 5W-30 синтетическое 1 л",
     "img": "https://placehold.co/150x120/e9ecef/495057?text=Hyundai"},
    {"id": 6, "code": "ZIC 162612", "article": "709526", "name": "Масло моторное ZIC TOP LS 5W-30 синтетическое 4 л",
     "img": "https://placehold.co/150x120/e9ecef/495057?text=ZIC2"},
    {"id": 7, "code": "Venwell VW-SL-002RU", "article": "887719",
     "name": "Очиститель тормозов 500 мл Venwell VW-SL-002RU",
     "img": "https://placehold.co/150x120/e9ecef/495057?text=Cleaner"},
    {"id": 8, "code": "LIQUI MOLY 7616", "article": "150043",
     "name": "Масло моторное LIQUI MOLY Leichtlauf Special AA 5W-30 синтетическое 4 л",
     "img": "https://placehold.co/150x120/e9ecef/495057?text=Liqui"},
    {"id": 9, "code": "ARNEZI R7950101", "article": "1676202", "name": "Пакет для шин R22 400x750x1100 мм 18 мкм",
     "img": "https://placehold.co/150x120/e9ecef/495057?text=Bag"},
    {"id": 10, "code": "TRW GIC264", "article": "506837", "name": "Датчик износа задних тормозных колодок TRW GIC 264",
     "img": "https://placehold.co/150x120/e9ecef/495057?text=Sensor"},
]

layout = Layout()

def render_cards(items):
    if not items:
        return html.Div("Товары не найдены", className="empty")
    cards = []
    for p in items:
        cards.append(
            html.Div(
                [
                    html.Img(src=p["img"], className="card-img"),
                    html.Div(f"{p['code']}  Код товара: {p['article']}", className="meta"),
                    html.Div(p["name"], className="title")
                ], className="card"
            )
        )
    return cards


@callback(
    Output("product-grid", "children"),
    Input("search-input", "value"),
    Input({"type": "filter-btn", "index": ALL}, "n_clicks"),
    prevent_initial_call=False
)
def update_view(search_val, n_clicks_list):
    triggered = ctx.triggered
    if not triggered:
        #  При первой загрузке -> 8 случайных товаров
        return render_cards(random.sample(PRODUCTS, min(8, len(PRODUCTS))))

    # 🔍 Ввод в поиск
    if search_val and search_val.strip():
        query = search_val.lower().strip()
        filtered = [p for p in PRODUCTS if query in (p["name"] + " " + p["code"] + " " + p["article"]).lower()]
        return render_cards(filtered)

    # ⬅️ Очистка поиска -> снова случайные
    return render_cards(random.sample(PRODUCTS, min(8, len(PRODUCTS))))