def partner_msg(user_data):
    if round(user_data[10], 2) >= 10:
        avialable = round(user_data[10], 2)
    else:
        avialable = 0.0
    return f'🤝 Парнёрская программа\n\nПриводи друзей и зарабатывай 10% с их пополнений пожизненно.\n\n' \
           f'👇Твоя реферальная ссылка👇 {user_data[6]}\n\n📑 Cтатистика:\nℹ️ приведено друзей: {user_data[11]}\n' \
           f'ℹ️ всего заработано: {user_data[9]}\nℹ️ доступно к выводу: {avialable}\n\n' \
           f'⚡⚡ Перед отправкой реферальной ссылки обязательно удалите имя бота из сообщения⚡⚡'


def client_office_msg(on_accaunt):
    return f'На вашем счету {on_accaunt} рублей'


def try_period_lasts_msg(expires_at, country):
    return f'Ваш пробный период активен до {expires_at}, вы выбрали VPN в {country.capitalize()}'


def order_data_msg(order_num, tarif, country, expires_at, duration):
    return f'Номер заказа: <b>{order_num}</b>\nТариф на <b>{tarif}</b> устройств\nСтрана:' \
           f' <b>{country.capitalize()}</b>\nАктивен до: <b>{expires_at}</b>\nПродолжительность <b>{duration}</b>' \
           f' месяцев'


def user_data_msg(user_data, try_period):
    if try_period:
        return f'ID: {user_data[1]}\nИмя: {user_data[2]}\nЯзык: {user_data[3]}\nИмя в телеге: {user_data[4]}\n' \
               f'Чей реферал: {user_data[7]}\nНа счету: {user_data[8]}\nОт рефеалов: {user_data[9]}\n' \
               f'Доступно: {user_data[10]}\nКоличество рефералов {user_data[11]}\nЧёрная метка {user_data[12]}\n' \
               f'Статус ПП: {try_period[0][1]}\nДействует до: {try_period[0][2][:-7]}\nСтрана: {try_period[0][3]}'
    else:
        return f'ID: {user_data[1]}\nИмя: {user_data[2]}\nЯзык: {user_data[3]}\nИмя в телеге: {user_data[4]}\n' \
               f'Чей реферал: {user_data[7]}\nНа счету: {user_data[8]}\nОт рефеалов: {user_data[9]}\n' \
               f'Доступно: {user_data[10]}\nКоличество рефералов {user_data[11]}\nЧёрная метка {user_data[12]}\n' \
               f'ПП не использовал'


def user_income_msg(income_data):
    return f'Номер платежа: {income_data[0]}\nСумма: {income_data[2]} рублей\nДата, время: {income_data[3][:-7]}'


def user_orders_msg(order_data):
    return f'Номер заказа: {order_data[0]}\nДата, время: {order_data[2][:-7]}\nТариф: {order_data[3]}\n' \
           f'Страна: {order_data[4]}\nНомер клиента: {order_data[5]}\nДлительность: {order_data[6]}\n' \
           f'Статус: {order_data[7]}\nДействует до: {order_data[8][:-7]}\nАвтопродление: {order_data[9]}'


def invoice_data_msg(comment, summ, method):
    return f'Платёж: <b>{comment}</b>\nСумма: <b>{summ}</b> рублей\nМетод оплаты: <b>{method.upper()}</b>\n\n' \
           f'⚡️После оплаты обязательно проверьте ваш платёж⚡️'


def block_payed_config_msg(expire_date, expire_time, country, tarif):
    tarif_name = ''
    if tarif == '2':
        tarif_name = '⚡ Тариф базовый ⚡'
    elif tarif == '5':
        tarif_name = '⚡ Тариф оптимальный ⚡'
    elif tarif == '10':
        tarif_name = '⚡ Тариф большая семья ⚡'
    return f'Ваша подписка на {tarif_name} в локации {country.title()} оплачена до {expire_date} {expire_time[:8]} ' \
           f'и больше не активна. ' \
           f'Для дальнейшего использования ВПН пополните счёт и продлите подписку.'


def one_d_payed_left_msg(expire_date, expire_time, country, tarif):
    tarif_name = ''
    if tarif == '2':
        tarif_name = '⚡ Тариф базовый ⚡'
    elif tarif == '5':
        tarif_name = '⚡ Тариф оптимальный ⚡'
    elif tarif == '10':
        tarif_name = '⚡ Тариф большая семья ⚡'
    return f'Осталось менее суток до окончания вашей подписки на {tarif_name} в локации {country.title()}. ' \
           f'Подписка активна до {expire_date} {expire_time[:8]}. ' \
           f'Для дальнейшего использования ВПН пополните счёт и продлите подписку.'


def two_d_payed_left_msg(expire_date, expire_time, country, tarif):
    tarif_name = ''
    if tarif == '2':
        tarif_name = '⚡ Тариф базовый ⚡'
    elif tarif == '5':
        tarif_name = '⚡ Тариф оптимальный ⚡'
    elif tarif == '10':
        tarif_name = '⚡ Тариф большая семья ⚡'
    return f'Осталось менее двух суток до окончания вашей подписки на {tarif_name} в локации {country.title()}. ' \
           f'Подписка активна до {expire_date} {expire_time[:8]}. ' \
           f'Для дальнейшего использования ВПН пополните счёт и продлите подписку.'


def dead_order_msg(order_id):
    return f'Ваш заказ номер: {order_id} неактивен, вы можете активировать его в разделе\n 💼 Кабинет/☔️ Мои впн'


hello_new_user_msg = 'Команда <b>mustela nivalis</b> рада приветствовать вас в нашем сервисе'

hello_admin_msg = 'Привет админ'

sub_to_use_msg = 'Для дальнейшего использования бота подпишитесь на канал.'

help_main_msg = 'В разделе <b>иструкции</b> вы найдёте подробные пояснения по установке' \
                ' и запуску тоннеля wireguard на всех актуальных платформах.\n\n' \
                'В разделе <b>вопросняк</b> собраны самые популярные вопросы.\n\n' \
                'Если возникли трудности смело обращайтесь в нашу техническую поддержку' \
                ' и вы получите любые ответы на любые вопросы.'

pay_method_msg = 'Выберите удобный для вас способ пополнения баланса.'

pay_sum_msg = 'Минимальная сумма пополнения 100 рублей.\n' \
              ' Эти средства будут списаны с вашего счёта для приобретения VPN.'

choose_tarif_msg = 'Выберите один из имеющихся тарифов.\n Напоминаю:\n ⚡<b>базовый</b> ️2️⃣ устройства⚡\n' \
                   ' ⚡<b>оптимальный</b> 5️⃣ устройств⚡\n ⚡<b>большая семья</b> 🔟 устройств⚡'

choose_geo_msg = 'Выберите страну для вашего VPN'

take_try_period_msg = 'Вы можете взять любой VPN на пробный период. Для этого выберите страну, которая вас интересует.'\
                      ' Бот пришлёт вам конфигурационные файлы. Активируйте туннели в соответствии с' \
                      ' инструкциями для ваших устройств.'
close_try_period_msg = 'Ваш пробный период закончился, для дальнейшего использования VPN приобретите подписку.'

one_d_left_try_period_msg = 'Осталось менее суток до окончания вашего пробного периода,' \
                            ' для дальнейшего использования VPN приобретите подписку'

two_d_left_try_period_msg = 'Осталось менее двух суток до окончания вашего пробного периода,' \
                            ' для дальнейшего использования VPN приобретите подписку'

not_enaugh_money_msg = 'На вашем счёте недостаточно средств для получения VPN с выбранными вами параметрами.' \
                       ' Вам нужно либо пополнить счёт, либо выбрать VPN с другими параметрами.'

congrats_msg = '🎊 Поздравляю!!!. Вы приобрели отличную защиту для вашей сетевой активности.'

no_try_no_order_msg = 'У вас нет активных VPN'

after_config_msg = 'Для активации VPN воспользуйтесь инструкцией для вашей платформы'

choose_duration_msg = 'Выберите продолжительность периода, на который вы хотите оплатить VPN.\n' \
                      'После этого с вашего счёта будут списаны средства и вы получите от бота конфигурационные файлы.'

fuck_off_msg = 'Вы нарушили правила использования сервиса. Ваш аккаунт заблокирован.' \
               ' Вы больше не можете пользоваться нашими услугами.'
