from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm, cm
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from io import BytesIO
import os

# 📌 РЕГИСТРАЦИЯ КИРИЛЛИЧЕСКОГО ШРИФТА (Обязательно для корректного отображения)
# Положи файл шрифта (например, arial.ttf) в папку assets/fonts/
FONT_PATH = os.path.join(os.path.dirname(__file__), "../../../../assets/fonts/arial.ttf")
if os.path.exists(FONT_PATH):
    pdfmetrics.registerFont(TTFont('Cyrillic', FONT_PATH))
    FONT_NAME = 'Cyrillic'
else:
    # Фоллбэк: если шрифта нет, кириллица может отображаться квадратами
    FONT_NAME = 'Helvetica'


def generate_order_pdf(order, db):
    buffer = BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=15 * mm, leftMargin=15 * mm,
        topMargin=15 * mm, bottomMargin=15 * mm
    )
    story = []
    styles = getSampleStyleSheet()

    # Базовый стиль текста
    base_style = ParagraphStyle('Base', fontName=FONT_NAME, fontSize=10, leading=12)

    # 1. Заголовок
    title_style = ParagraphStyle('Title', fontName=FONT_NAME, fontSize=16, alignment=TA_CENTER, spaceAfter=8 * mm)
    story.append(Paragraph(f"ЗАКАЗ-НАРЯД № {order.id}", title_style))

    date_str = order.created_at.strftime('%d.%m.%Y %H:%M') if order.created_at else '-'
    story.append(Paragraph(f"Дата формирования: {date_str}", base_style))
    story.append(Spacer(5 * mm, 5 * mm))

    # 2. Блок информации (Поставщик / Заказчик)
    user = order.user
    fio = f"{user.lastname} {user.firstname} {user.patronymic}" if user else "Не указан"
    user_phone = getattr(user, 'phone', '-') or '-'

    info_data = [
        ["Поставщик:",
         "ООО «РельсыШпалы»\nИНН: 7700000000\nБанк: ПАО ЖДБАНК\nАдрес: г. Москва, ул. Железнодорожная, 1"],
        ["Заказчик:", f"{fio}\nТел.: {user_phone}"]
    ]
    info_table = Table(info_data, colWidths=[3.5 * cm, 13 * cm])
    info_table.setStyle(
        TableStyle(
            [
                ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
                ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                ('FONTNAME', (0, 0), (-1, -1), FONT_NAME),
                ('FONTSIZE', (0, 0), (-1, -1), 10),
                ('LEFTPADDING', (0, 0), (-1, -1), 4),
                ('RIGHTPADDING', (0, 0), (-1, -1), 4),
                ('TOPPADDING', (0, 0), (-1, -1), 4),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
            ]
        )
    )
    story.append(info_table)
    story.append(Spacer(5 * mm, 5 * mm))

    # 3. Заголовок раздела
    story.append(Paragraph("Заказаны комплектующие:", base_style))
    story.append(Spacer(3 * mm, 3 * mm))

    # Разделяем позиции на OEM (Работы/Комплектующие) и Аналоги (Запчасти)
    oem_items = [i for i in order.items if i.oem_part]
    analogue_items = [i for i in order.items if i.analogue_part]

    def make_table(title, items, get_name):
        data = [[title, "Кол-во"]]
        for item in items:
            data.append([get_name(item), str(item.quantity)])

        t = Table(data, colWidths=[13 * cm, 3 * cm])
        t.setStyle(
            TableStyle(
                [
                    ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
                    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#f8f9fa')),
                    ('FONTNAME', (0, 0), (-1, 0), FONT_NAME),
                    ('FONTNAME', (0, 1), (-1, -1), FONT_NAME),
                    ('FONTSIZE', (0, 0), (-1, -1), 10),
                    ('ALIGN', (1, 0), (1, -1), 'CENTER'),
                    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                    ('LEFTPADDING', (0, 0), (-1, -1), 4),
                    ('RIGHTPADDING', (0, 0), (-1, -1), 4),
                ]
            )
        )
        return t

    if oem_items:
        story.append(
            make_table(
                "Список комплектующих (OEM)", oem_items,
                lambda i: f"{i.oem_part.name} ({i.oem_part.oem_num})"
                )
            )
        story.append(Spacer(2 * mm, 2 * mm))

    if analogue_items:
        story.append(
            make_table(
                "Запчасти и материалы (Аналоги)", analogue_items,
                lambda i: f"{i.analogue_part.name} ({i.analogue_part.analogue_num})"
                )
            )

    # 4. Футер (без сумм, как просил)
    story.append(Spacer(5 * mm, 5 * mm))
    footer_style = ParagraphStyle('Footer', fontName=FONT_NAME, fontSize=9, alignment=TA_LEFT, textColor=colors.grey)
    story.append(Paragraph("Документ сформирован автоматически в системе РельсыШпалы.", footer_style))

    doc.build(story)
    buffer.seek(0)
    return buffer