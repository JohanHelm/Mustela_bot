from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton  # , KeyboardButton, ReplyKeyboardMarkup

import config as cfg

'''Общие кнопки'''
btn_to_store = InlineKeyboardButton(text='⛺️ Наша хатка', url=cfg.CHANNEL_URL)
btn_subscribed = InlineKeyboardButton(text='👥 Я подписался', callback_data='new_subscribed')
btn_help_support = InlineKeyboardButton(text='🥷 Поддержка', url=cfg.CHAT_URL)
btn_to_bot = InlineKeyboardButton(text='🤖 Бот', url=cfg.BOT_URL)

'''Общие клавиатуры'''
# redirect to shop
ch_menu = InlineKeyboardMarkup()
ch_menu.row(btn_to_store, btn_subscribed)

'''Клавиатура в канале'''
to_bot_and_sup = InlineKeyboardMarkup()
to_bot_and_sup.row(btn_to_bot, btn_help_support)

'''Кнопки клиента'''
# client_menu
btn_choose_geo = InlineKeyboardButton(text='🛡 Выбрать VPN', callback_data='client_choose_vpn')  # 🗺
btn_cient_office = InlineKeyboardButton(text='💼 Кабинет', callback_data='client_office')
btn_partner = InlineKeyboardButton(text='🤝 Партнёрка', callback_data='client_partner')
btn_help = InlineKeyboardButton(text='🆘 Помощь', callback_data='client_help')
btn_try_period = InlineKeyboardButton(text='🫴 Пробный период', callback_data='client_try')

# help_menu
btn_help_instr = InlineKeyboardButton(text='📄 Инструкции', url=cfg.instructions)
btn_help_faq = InlineKeyboardButton(text='❓ Вопросняк', url=cfg.faq)
btn_help_back = InlineKeyboardButton(text='🔙 Назад', callback_data='help_back')

# client_office
btn_pay = InlineKeyboardButton(text='💴 Пополнить баланс', callback_data='office_method')
btn_need_conf = InlineKeyboardButton(text='📑 Запросить конфиг. файлы', callback_data='office_need_conf')
btn_my_vpn = InlineKeyboardButton(text='☔️ Мои впн', callback_data='office_my_vpn')
btn_office_back = InlineKeyboardButton(text='🔙 Назад', callback_data='office_back')

# client_partner


# client_countries_menu
btn_country1 = InlineKeyboardButton(text='Финляндия', callback_data='country_finland')
btn_country2 = InlineKeyboardButton(text='Германия', callback_data='country_german')
btn_country3 = InlineKeyboardButton(text='Нидерланды', callback_data='country_netherlands')
btn_country4 = InlineKeyboardButton(text='Швеция', callback_data='country_swiss')
btn_country5 = InlineKeyboardButton(text='Румыния', callback_data='country_romania')
btn_country6 = InlineKeyboardButton(text='Великобритания', callback_data='country_britain')
btn_country7 = InlineKeyboardButton(text='Турция', callback_data='country_turkey')
btn_country8 = InlineKeyboardButton(text='Аргентина', callback_data='country_argentina')
btn_country9 = InlineKeyboardButton(text='Индия', callback_data='country_india')
btn_country10 = InlineKeyboardButton(text='США', callback_data='country_usa')
btn_country_back = InlineKeyboardButton(text='🔙 Назад', callback_data='country_back')

# client_pay_method
btn_client_method_card = InlineKeyboardButton(text='💳 Картой', callback_data='method_card')
btn_client_method_qiwi = InlineKeyboardButton(text='💰 QIWI', callback_data='method_qiwi')
btn_client_method_yoomoney = InlineKeyboardButton(text='💰 YOOMONEY', callback_data='method_yoomoney')
btn_client_method_crypta = InlineKeyboardButton(text='🤑 Криптовалютой', callback_data='method_crypta')
btn_client_method_back = InlineKeyboardButton(text='🔙 Назад', callback_data='method_back')

# client_pay_menu
btn_client_pay_5 = InlineKeyboardButton(text='💴 325 рублей', callback_data='pay_325')
btn_client_pay_12 = InlineKeyboardButton(text='💴 455 рублей', callback_data='pay_455')
btn_client_pay_20 = InlineKeyboardButton(text='💴 650 рублей', callback_data='pay_650')
btn_client_pay_other = InlineKeyboardButton(text='💴 Другую сумму', callback_data='pay_other')
btn_client_pay_back = InlineKeyboardButton(text='🔙 Назад', callback_data='pay_back')

# tarif_menu
btn_tarif_2 = InlineKeyboardButton(text='👌 базовый', callback_data='tarif_2')
btn_tarif_5 = InlineKeyboardButton(text='👍 оптимальный', callback_data='tarif_5')
btn_tarif_10 = InlineKeyboardButton(text='👨‍👨‍👦‍👦 большая семья', callback_data='tarif_10')
btn_tarif_back = InlineKeyboardButton(text='🔙 назад', callback_data='tarif_back')

# duration_menu
btn_duration_1 = InlineKeyboardButton(text='Один месяц', callback_data='duration_1')
btn_duration_3 = InlineKeyboardButton(text='Три месяца', callback_data='duration_3')
btn_duration_6 = InlineKeyboardButton(text='Шесть месяцев', callback_data='duration_6')
btn_duration_12 = InlineKeyboardButton(text='Один год', callback_data='duration_12')
btn_duration_24 = InlineKeyboardButton(text='Два года', callback_data='duration_24')
btn_duration_36 = InlineKeyboardButton(text='Три года', callback_data='duration_36')
btn_duration_back = InlineKeyboardButton(text='🔙 назад', callback_data='duration_back')

'''Клавиатуры Клиента'''
# client_menu
client_main_menu = InlineKeyboardMarkup()
client_main_menu.row(btn_help, btn_cient_office)
client_main_menu.row(btn_partner, btn_to_store)
client_main_menu.row(btn_choose_geo, btn_try_period)

# help_menu
client_help_menu = InlineKeyboardMarkup()
client_help_menu.row(btn_help_instr, btn_help_faq)
client_help_menu.row(btn_help_support, btn_help_back)

# client_office
client_office_menu = InlineKeyboardMarkup()
client_office_menu.row(btn_pay)
client_office_menu.row(btn_need_conf)
client_office_menu.row(btn_my_vpn, btn_office_back)


# client_partner
def gen_partner_menu(ref_link):
    btn_share_link = InlineKeyboardButton(text='📣 Поделиться ссылкой', switch_inline_query=ref_link)
    btn_take_money = InlineKeyboardButton(text='💴 Вывод средств', callback_data='partner_take_money')
    btn_partner_back = InlineKeyboardButton(text='🔙 Назад', callback_data='partner_back')
    client_partner_menu = InlineKeyboardMarkup(row_width=1)
    client_partner_menu.insert(btn_share_link)
    client_partner_menu.insert(btn_take_money)
    client_partner_menu.insert(btn_partner_back)
    return client_partner_menu


# client_countries
country_menu = InlineKeyboardMarkup()
country_menu.row(btn_country1, btn_country2)
country_menu.row(btn_country3, btn_country4)
country_menu.row(btn_country5, btn_country6)
country_menu.row(btn_country7, btn_country8)
country_menu.row(btn_country9, btn_country10)
country_menu.row(btn_country_back)

# client_pay_method
client_pay_method = InlineKeyboardMarkup()
client_pay_method.row(btn_client_method_card, btn_client_method_yoomoney)
client_pay_method.row(btn_client_method_crypta, btn_client_method_qiwi)
client_pay_method.row(btn_client_method_back)

# client_pay_menu
client_pay_menu = InlineKeyboardMarkup()
client_pay_menu.row(btn_client_pay_5, btn_client_pay_12).row(btn_client_pay_20, btn_client_pay_other)
client_pay_menu.add(btn_client_pay_back)

# tarif_menu
tarif_menu = InlineKeyboardMarkup()
tarif_menu.row(btn_tarif_2, btn_tarif_5)
tarif_menu.row(btn_tarif_10, btn_tarif_back)

# duraion_menu
duration_menu = InlineKeyboardMarkup()
duration_menu.row(btn_duration_1, btn_duration_3)
duration_menu.row(btn_duration_6, btn_duration_12)
duration_menu.row(btn_duration_24, btn_duration_36)
duration_menu.row(btn_duration_back)


# order menu
def disable_prolong(order_id):
    # disable autoprolongation
    btn_dis_prolong = InlineKeyboardButton(text='Отключить автопродление',
                                           callback_data=f'order_disable_prolong_{order_id}')
    disable_prolong_menu = InlineKeyboardMarkup()
    disable_prolong_menu.insert(btn_dis_prolong)
    return disable_prolong_menu


def enable_prolong(order_id):
    # enable autoprolongation
    btn_en_prolong = InlineKeyboardButton(text='Включить автопродление',
                                          callback_data=f'order_enable_prolong_{order_id}')
    enable_prolong_menu = InlineKeyboardMarkup()
    enable_prolong_menu.insert(btn_en_prolong)
    return enable_prolong_menu


def activate_order(odrer_id):
    btn_activate_order = InlineKeyboardButton(text='Активировать', callback_data=f'order_activate_{odrer_id}')
    activate_order_menu = InlineKeyboardMarkup()
    activate_order_menu.insert(btn_activate_order)
    return activate_order_menu


def invoice_menu(pay_link):
    btn_pay_invoice = InlineKeyboardButton(text='Внести средства', url=pay_link)
    btn_check_invoice = InlineKeyboardButton(text='Проверить платёж', callback_data='invoice_check')
    btn_back_inoice = InlineKeyboardButton(text='Отменить платёж', callback_data='invoice_back')
    check_pay_menu = InlineKeyboardMarkup()
    check_pay_menu.row(btn_pay_invoice, btn_check_invoice)
    check_pay_menu.row(btn_back_inoice)
    return check_pay_menu


"""Кнопки админа"""
btn_to_channel = InlineKeyboardButton(text='В канал', switch_inline_query_current_chat='В канал:\n')
btn_msg_to_all = InlineKeyboardButton(text='Рассылка', switch_inline_query_current_chat='Рассылка:\n')
btn_customer_data = InlineKeyboardButton(text='Данные', switch_inline_query_current_chat='Данные:\n')
btn_customer_orders = InlineKeyboardButton(text='Заказы', switch_inline_query_current_chat='Заказы:\n')
btn_customer_income = InlineKeyboardButton(text='Платежи', switch_inline_query_current_chat='Платежи:\n')

'''Клавиатуры админа'''
admin_main_menu = InlineKeyboardMarkup()
admin_main_menu.row(btn_to_channel, btn_msg_to_all)
admin_main_menu.row(btn_customer_data, btn_customer_orders)
admin_main_menu.row(btn_customer_income)
