def partner_msg(user_data):
    if round(user_data[10], 2) >= 10:
        avialable = round(user_data[10], 2)
    else:
        avialable = 0.0
    return f'🤝 Парнёрская программа\n\nПриводи друзей и зарабатывай 10% с их пополнений.\n\n' \
           f'👇Твоя реферальная ссылка👇 {user_data[6]}\n\n📑 Cтатистика:\nℹ️ приведено друзей: {user_data[11]}\n' \
           f'ℹ️ всего заработано: {user_data[9]}\nℹ️ доступно к выводу: {avialable}\n\n' \
           f'⚡⚡ Перед отправкой реферальной ссылки обязательно удалите имя бота из сообщения⚡⚡'


def client_office_msg(on_accaunt, promo_money):
    return f'На вашем счету {on_accaunt} рублей\n' \
           f'Средства от промо кодов {promo_money} рублей'


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
           f'Страна: {order_data[4]}\nНомер клиента: {order_data[7]}\nДлительность: {order_data[8]}\n' \
           f'Статус: {order_data[9]}\nДействует до: {order_data[10][:-7]}\nАвтопродление: {order_data[11]}'


def invoice_data_msg(comment, summ, method):
    return f'Платёж: <b>{comment}</b>\nСумма: <b>{summ}</b> рублей\nМетод оплаты: <b>{method.upper()}</b>\n\n' \
           f'⚡️После оплаты обязательно проверьте ваш платёж⚡️'


def block_payed_config_msg(expire_date, country, tarif):
    tarif_name = {'2': '⚡ Тариф базовый ⚡', '5': '⚡ Тариф оптимальный ⚡', '10': '⚡ Тариф большая семья ⚡'}
    countries = {'Hels': '🇫🇮 Хельсинки', 'Falc': '🇩🇪 Фалькенштайн', 'Amst': '🇳🇱 Амстердам', 'Vien': '🇦🇹 Вена',
                 'Toro': '🇦 Торонто', 'Lond': '🇬🇧 Лондон', 'Madr': '🇪🇸 Мадрид', 'Atla': '🇺🇸 Атланта'}
    return f'Ваша подписка на {tarif_name[tarif]} в локации {countries[country]} оплачена до {expire_date} ' \
           f'и больше не активна. ' \
           f'Для дальнейшего использования ВПН <a href="https://t.me/mustela_vpn/98">пополните счёт</a>\n' \
           f' и <a href="https://t.me/mustela_vpn/88">приобретите подписку</a>.'


def days_payed_left_msg(days, order_id, expire_date, country, tarif):
    tarif_name = {'2': '⚡ Тариф базовый ⚡', '5': '⚡ Тариф оптимальный ⚡', '10': '⚡ Тариф большая семья ⚡'}
    countries = {'Hels': '🇫🇮 Хельсинки', 'Falc': '🇩🇪 Фалькенштайн', 'Amst': '🇳🇱 Амстердам', 'Vien': '🇦🇹 Вена',
                 'Toro': '🇦 Торонто', 'Lond': '🇬🇧 Лондон', 'Madr': '🇪🇸 Мадрид', 'Atla': '🇺🇸 Атланта'}
    if days == '1':
        return f'Осталось менее суток до окончания вашей подписки № {order_id} на {tarif_name[tarif]} в локации ' \
               f'{countries[country]}. Подписка активна до {expire_date}. ' \
               f'Для дальнейшего использования ВПН <a href="https://t.me/mustela_vpn/98">пополните счёт</a>\n' \
               f' и <a href="https://t.me/mustela_vpn/88">приобретите подписку</a>.'

    elif days == '2':
        return f'Осталось менее двух суток до окончания вашей подписки № {order_id} на {tarif_name[tarif]} в локации ' \
               f'{countries[country]}. Подписка активна до {expire_date}. ' \
               f'Для дальнейшего использования ВПН <a href="https://t.me/mustela_vpn/98">пополните счёт</a>\n' \
               f' и <a href="https://t.me/mustela_vpn/88">приобретите подписку</a>.'


def dead_order_msg(order_id):
    return f'Ваш заказ номер: {order_id} неактивен, вы можете активировать его в разделе\n 💼 Кабинет/☔️ Мои впн'


def plat_instr_msg(platform):
    platforms = {'android':
            '1️⃣ Скачайте приложение <a href="https://play.google.com/store/apps/details?id=com.wireguard.android"> '
            'WireGuard</a> из Google Play и установите на ваше андроид устройство.\n',
                 'iphone':
            '1️⃣ Скачайте приложение <a href="https://itunes.apple.com/us/app/wireguard/id1441195209?ls=1&mt=8"> '
            'WireGuard</a> из App Store и установите на ваш IPHONE.\n',
                'macos':
            '1️⃣ Скачайте приложение <a href="https://apps.apple.com/us/app/wireguard/id1451685025?ls=1&mt=12">' \
            'WireGuard</a> из Mac App Store и установите на ваш MACBOOK.\n',
                 'windows':
            '1️⃣ Скачайте утановщик <a href="https://download.wireguard.com/windows-client/wireguard-installer.exe">' \
            'WireGuard</a> клиента для windows с сайта WIREGUARD и установите его на ваш компьютер.\n'}
    return f'{platforms[platform]} '\
           f'2️⃣ Бот пришлёт вам конфигурационный файл. Сохраните этот файл на ваше устройство (Нажать на три точки ' \
           f'на сообщении с файлом и выбрать \"сохранить в загрузки\")\n ' \
           f'3️⃣ Откройте приложение Wireguard и нажмите плюсик, дальше выберите импорт из файла или архива. ' \
           f'Найдите файл с конфигом VPN в каталоге Загрузки.\n ' \
           f'4️⃣ Для включения / отключения VPN просто перемещайте ползунок напротив конфига в приложении Wireguard ' \
           f'вправо и влево'



    # if platform == 'android':
    #     return f'1️⃣ Скачайте приложение <a href="https://play.google.com/store/apps/details?id=com.wireguard.android">' \
    #            f'WireGuard</a> из Google Play и установите на ваше андроид устройство.\n' \
    #            f'2️⃣ Затем возвращайтесь и переходите к выбору локации 👇'
    # elif platform == 'iphone':
    #     return f'1️⃣ Скачайте приложение <a href="https://itunes.apple.com/us/app/wireguard/id1441195209?ls=1&mt=8">' \
    #            f'WireGuard</a> из App Store и установите на ваш IPHONE.\n' \
    #            f'2️⃣ Затем возвращайтесь и переходите к выбору локации 👇'
    # elif platform == 'macos':
    #     return f'1️⃣ Скачайте приложение <a href="https://apps.apple.com/us/app/wireguard/id1451685025?ls=1&mt=12">' \
    #            f'WireGuard</a> из Mac App Store и установите на ваш MACBOOK.\n' \
    #            f'2️⃣ Затем возвращайтесь и переходите к выбору локации 👇'
    # elif platform == 'windows':
    #     return f'1️⃣ Скачайте утановщик ' \
    #            f'<a href="https://download.wireguard.com/windows-client/wireguard-installer.exe">' \
    #            f'WireGuard</a> клиента для windows с сайта WIREGUARD и установите его на ваш компьютер.\n' \
    #            f'2️⃣ Затем возвращайтесь и переходите к выбору локации 👇'





pick_location_msg = f'После выбора локации бот пришлёт вам конфигурационный файл. Далее:\n' \
                    f'1️⃣ Сохраните этот файл на ваше устройство (Нажать на три точки на сообщении с файлом' \
                    f' и выбрать \"сохранить в загрузки\")\n' \
                    f'2️⃣ Откройте приложение Wireguard и нажмите плюсик, дальше выберите импорт из файла или архива.' \
                    f' Найдите файл с конфигом VPN в каталоге Загрузки.\n' \
                    f'3️⃣ Для включения / отключения VPN просто перемещайте ползунок напротив конфига в приложении Wireguard вправо и влево'


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

choose_tarif_msg = 'Выберите один из имеющихся тарифов.\n Напоминаю:\n' \
                   ' ⚡<b>простой</b> 1️⃣ устройство - 180р./мес.\n' \
                   ' ⚡<b>базовый</b> ️2️⃣ устройства - 325р./мес.\n' \
                   ' ⚡<b>оптимальный</b> 5️⃣ устройств - 455 р./мес.\n' \
                   ' ⚡<b>большая семья</b> 🔟 устройств - 650 р./мес.\n' \
                   'Все тарифы <a href="https://t.me/mustela_vpn/90">ЗДЕСЬ</a>!'

choose_geo_msg = 'Выберите страну для вашего VPN.\n' \
                 'Не нашли интересующую вас страну !!?\n' \
                 'Пишите в <a href="https://t.me/mustela_vpn_sup">ПОДЕРЖКУ</a> и мы обязательно её добавим!'

pick_plat_msg = 'Вы можете взять любой VPN на пробный период на 3 дня.\n' \
                'Для этого выберите вашу платформу и дальше действуйте по инструкции.'

take_try_period_msg = 'Вы можете взять любой VPN на пробный период на 3 дня.\n' \
                      'Для этого выберите вашу платформу и дальше действуйте по инструкции.'
                      # 'страну, которая вас интересует.'\
                      # ' Бот пришлёт вам конфигурационные файлы. Активируйте туннели в соответствии с' \
                      # ' инструкциями для ваших устройств.'
close_try_period_msg = 'Ваш пробный период закончился, для дальнейшего использования VPN\n' \
                       ' <a href="https://t.me/mustela_vpn/98">пополните счёт</a>\n' \
                       ' и <a href="https://t.me/mustela_vpn/88">приобретите подписку</a>.'

one_d_left_try_period_msg = 'Осталось менее суток до окончания вашего пробного периода,\n' \
                            ' <a href="https://t.me/mustela_vpn/98">пополните счёт</a>\n' \
                            ' и <a href="https://t.me/mustela_vpn/88">приобретите подписку</a>.'


two_d_left_try_period_msg = 'Осталось менее двух суток до окончания вашего пробного периода,\n' \
                            ' <a href="https://t.me/mustela_vpn/98">пополните счёт</a>\n' \
                            ' и <a href="https://t.me/mustela_vpn/88">приобретите подписку</a>.'

not_enaugh_money_msg = 'На вашем счёте недостаточно средств для получения VPN с выбранными вами параметрами.' \
                       ' Вам нужно либо пополнить счёт, либо выбрать VPN с другими параметрами.'

congrats_msg = '🎊 Поздравляю!!!. Вы приобрели отличную защиту для вашей сетевой активности.'

no_try_no_order_msg = 'У вас нет активных VPN'

promo_code_msg = 'Введите промо код в поле для сообщений и отправьте боту.'

after_config_msg = 'Для активации VPN воспользуйтесь\n <a href="https://t.me/mustela_vpn/83">инструкцией</a> ️ для вашей платформы'

choose_duration_msg = 'Выберите продолжительность периода, на который вы хотите оплатить VPN.\n' \
                      'После этого с вашего счёта будут списаны средства и вы получите от бота конфигурационные файлы.'

fuck_off_msg = 'Вы нарушили правила использования сервиса. Ваш аккаунт заблокирован.' \
               ' Вы больше не можете пользоваться нашими услугами.'


def show_all_users_msg(user):
    return f'id                     <b>{user[1]}</b>\n'\
           f'full_name            <b>{user[2]}</b>\n' \
           f'mention           {user[4]}\n' \
           f'on_accaunt         <b>{user[8]}</b>\n' \
           f'reg_date          <b>{user[13][:19]}</b>'


def show_all_tp_msg(tp):
    return f'id             <b>{tp[0]}</b>\n'\
           f'server         <b>{tp[3]}_{tp[5]}_{tp[6]}</b>\n' \
           f'expires_at     <b>{tp[2][:19]}</b>'


def show_all_orders_msg(order):
    return f'id             <b>{order[1]}</b>\n' \
           f'tarif          <b>{order[3]}</b>\n'\
           f'server         <b>{order[4]}_{order[5]}_{order[6]}</b>\n' \
           f'expires_at     <b>{order[10][:19]}</b>'


def show_all_incomes_msg(income):
    return f'id                 <b>{income[0]}</b>\n' \
           f'user_id        <b>{income[1]}</b>\n' \
           f'summ           <b>{income[2]}</b>\n'\
           f'method         <b>{income[4]}</b>\n' \
           f'date_time      <b>{income[3][:19]}</b>'

