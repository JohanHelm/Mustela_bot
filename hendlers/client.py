import calendar
from datetime import datetime
from os import listdir, system, remove
from random import sample

from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from dateutil.relativedelta import relativedelta
from asyncio import sleep
import config as cfg
import markups as nav
import payments as pm
from create_bot import bot, chat_member_status
from database import db
from infmsg import *

# Списки вариков для выбора FSM
tarifs = [2, 5, 10]
counries = ['finland', 'germany', 'netherlands', 'swiss', 'romania', 'britania', 'turkey', 'argentina', 'india', 'usa']
durations = [1, 3, 6, 12, 24, 36]


class OrderVpn(StatesGroup):
    waiting_for_tarif = State()
    waiting_for_country = State()
    waiting_for_duration = State()


class IncomePayment(StatesGroup):
    waiting_for_method = State()
    waiting_for_invoice = State()
    waiting_for_check = State()


class DemandPartnerMoney(StatesGroup):
    pass


# main_menu
async def cmd_client_main(call: types.callback_query, state: FSMContext):
    if call.data == 'client_choose_vpn':
        await bot.send_photo(call.from_user.id, cfg.mustela, choose_tarif_msg, reply_markup=nav.tarif_menu)
        await state.set_state(OrderVpn.waiting_for_tarif.state)
    elif call.data == 'client_office':
        await bot.send_photo(call.from_user.id, cfg.mustela, client_office_msg(db.get_user_data(call.from_user.id)[8]),
                             reply_markup=nav.client_office_menu)
    elif call.data == 'client_partner':
        await bot.send_photo(call.from_user.id, cfg.mustela, partner_msg(db.get_user_data(call.from_user.id)),
                             reply_markup=nav.gen_partner_menu(db.get_user_data(call.from_user.id)[6]))
    elif call.data == 'client_help':
        await bot.send_photo(call.from_user.id, cfg.mustela, help_main_msg, reply_markup=nav.client_help_menu)
    elif call.data == 'client_try':
        if db.check_try_period(call.from_user.id):
            await call.answer('Вы уже использовали свой пробный период. 🤚')
        else:
            await bot.send_photo(call.from_user.id, cfg.mustela, take_try_period_msg, reply_markup=nav.country_menu)


# help_menu
# @dp.callback_query_handler(text_contains='help')
async def cmd_client_help(call: types.callback_query):
    if call.data == 'help_back':
        await bot.send_photo(call.from_user.id, cfg.mustela, 'Привет {0.first_name}!\n'.format(call.from_user) +
                             hello_new_user_msg, reply_markup=nav.client_main_menu)


# @dp.callback_query_handler(text_contains='office')
async def cmd_client_office(call: types.callback_query, state: FSMContext):
    if call.data == 'office_method':
        await bot.send_photo(call.from_user.id, cfg.mustela, pay_method_msg, reply_markup=nav.client_pay_method)
        await state.set_state(IncomePayment.waiting_for_method.state)
    elif call.data == 'office_my_vpn':
        active_vpn = False
        if db.check_try_period(call.from_user.id):
            if db.check_try_period(call.from_user.id)[0][1] == 1:
                active_vpn = True
                await bot.send_message(call.from_user.id,
                                       try_period_lasts_msg(db.check_try_period(call.from_user.id)[0][2][:-7],
                                                            db.check_try_period(call.from_user.id)[0][3]))
        if db.check_orders(call.from_user.id):
            for order in db.check_orders(call.from_user.id):
                if order[9]:
                    if order[11]:
                        await bot.send_message(call.from_user.id,
                                           order_data_msg(order[0], order[3], order[4], order[10][:-7]),
                                           reply_markup=nav.disable_prolong(order[0]))
                    else:
                        await bot.send_message(call.from_user.id,
                                               order_data_msg(order[0], order[3], order[4], order[10][:-7]),
                                               reply_markup=nav.enable_prolong(order[0]))
                    active_vpn = True
                else:
                    await bot.send_message(call.from_user.id,
                                           order_data_msg(order[0], order[3], order[4], order[10][:-7]),
                                           reply_markup=nav.activate_order)
        if not active_vpn:
            await call.answer(no_try_no_order_msg, show_alert=True)
    elif call.data == 'office_back':
        await bot.send_photo(call.from_user.id, cfg.mustela, 'Привет {0.first_name}!\n'.format(call.from_user) +
                             hello_new_user_msg, reply_markup=nav.client_main_menu)
    elif call.data == 'office_need_conf':
        if db.check_orders(call.from_user.id):
            for order in db.check_orders(call.from_user.id):
                if order[9]:
                    config_files = listdir(f'/home/pp/vpn_service/config_files/{order[4]}/work/clients/{order[7]}')
                    for i in range(order[3]):
                        send_file = open(
                            f'/home/pp/vpn_service/config_files/{order[4]}/work/clients/{order[7]}/{config_files[i]}',
                            'rb')
                        await bot.send_document(call.from_user.id, send_file, caption=after_config_msg)
                        send_file.close()
                else:
                    await bot.send_message(call.from_user.id, dead_order_msg(order[0]))
        else:
            await call.answer('У вас нет активных подписок.')


# @dp.callback_query_handler(text_contains='order')
async def cmd_order_control(call: types.callback_query):
    if call.data[:21] == 'order_disable_prolong':
        db.set_order_prolong(0, call.data[22:])
        await call.answer('Автопродление отключено.')
    elif call.data[:20] == 'order_enable_prolong':
        db.set_order_prolong(1, call.data[21:])
        await call.answer('Автопродление включено.')
    elif call.data == 'order_activate':
        print('activate')
        # odrer_id
        # duration
        # tarif
        # price
        # user_id
        # on account



# @dp.callback_query_handler(text_contains='partner')
async def cmd_client_partner(call: types.callback_query):
    if call.data == 'partner_back':
        await bot.send_photo(call.from_user.id, cfg.mustela, 'Привет {0.first_name}!\n'.format(call.from_user) +
                             hello_new_user_msg, reply_markup=nav.client_main_menu)
    elif call.data == 'partner_take_money':
        if db.get_user_data(call.from_user.id)[10] < 500:
            await call.answer('Недостаточно средств для вывода.\n Минимальная сумма для вывода 500 рублей.',
                              show_alert=True)
        else:
            # тоже нужен FSM
            # db.take_ref_money(call.from_user.id, 10)
            await bot.send_message(call.from_user.id, 'Вывод средств с парнёрки, пока фиксированная сумма 10$!!')
    # elif call.data == 'partner_ref':
    #     await call.message.answer(db.get_ref_link(call.from_user.id)[0][6])


async def cmd_choose_tarif(call: types.callback_query, state: FSMContext):
    if call.data == 'tarif_back':
        await state.finish()
        await bot.send_photo(call.from_user.id, cfg.mustela, 'Привет {0.first_name}!\n'.format(call.from_user) +
                             hello_new_user_msg, reply_markup=nav.client_main_menu)
    else:
        await state.update_data(chosen_tarif=call.data[6:])
        await bot.send_photo(call.from_user.id, cfg.mustela, choose_geo_msg, reply_markup=nav.country_menu)
        await state.set_state(OrderVpn.waiting_for_country.state)


async def cmd_choose_country(call: types.callback_query, state: FSMContext):
    if call.data == 'country_back':
        await state.finish()
        await bot.send_photo(call.from_user.id, cfg.mustela, 'Привет {0.first_name}!\n'.format(call.from_user) +
                             hello_new_user_msg, reply_markup=nav.client_main_menu)
    else:
        await state.update_data(chosen_country=call.data[8:])
        await bot.send_photo(call.from_user.id, cfg.mustela, choose_duration_msg, reply_markup=nav.duration_menu)
        await state.set_state(OrderVpn.waiting_for_duration.state)


async def cmd_choose_duration(call: types.callback_query, state: FSMContext):
    if call.data == 'duration_back':
        await state.finish()
        await bot.send_photo(call.from_user.id, cfg.mustela, 'Привет {0.first_name}!\n'.format(call.from_user) +
                             hello_new_user_msg, reply_markup=nav.client_main_menu)
    else:
        await state.update_data(chosen_duration=call.data[9:])
        price = db.check_price(int((await state.get_data())['chosen_tarif']),
                               int((await state.get_data())['chosen_duration']))[0]
        user_data = db.get_user_data(call.from_user.id)
        if user_data[8] >= price and user_data[12] == 0:
            # await call.answer('выслать конфигурационные файлы в соответствии с тарифом')
            country = (await state.get_data())['chosen_country']
            interfaces = listdir(f'/home/pp/vpn_service/config_files/{country}/work/wsc')
            client_interface = interfaces[0][10:19]
            if system(f'ssh root@WG_WORK -p 4522 /root/enable_payed_user.sh {client_interface}') == 0:
                config_files = listdir(f'/home/pp/vpn_service/config_files/{country}/work/clients/{client_interface}')
                for i in range(int((await state.get_data())['chosen_tarif'])):
                    send_file = open(f'/home/pp/vpn_service/config_files/{country}/work/clients/{client_interface}/{config_files[i]}', 'rb')
                    await bot.send_document(call.from_user.id, send_file, caption=after_config_msg)
                    send_file.close()
                remove(f'/home/pp/vpn_service/config_files/{country}/work/wsc/{interfaces[0]}')
                db.make_order(call.from_user.id, datetime.today(), int((await state.get_data())['chosen_tarif']),
                              (await state.get_data())['chosen_country'], client_interface,
                              int((await state.get_data())['chosen_duration']),
                              datetime.today() + relativedelta(months=int((await state.get_data())['chosen_duration'])),
                              price)
                await call.answer(congrats_msg)
            else:
                await bot.send_photo(call.from_user.id, cfg.mustela, '<b>Привет {0.first_name}!</b>\n'
                                     .format(call.from_user) + hello_new_user_msg, reply_markup=nav.client_main_menu)
                await bot.send_message(cfg.ADMIN_ID, f'Недолёт ПП конфига с {country}')
                await call.answer('Из-за неполадок сети связь с сервером отсутствует. Попробуйте позднее. '
                                  'Техподдержка уже занимается этой проблемой.', show_alert=True)

        elif db.get_user_data(call.from_user.id)[8] < price:
            await call.answer(not_enaugh_money_msg, show_alert=True)
            await bot.send_photo(call.from_user.id, cfg.mustela, 'Привет {0.first_name}!\n'.format(call.from_user) +
                                 hello_new_user_msg, reply_markup=nav.client_main_menu)
        elif db.get_user_data(call.from_user.id)[12] == 1:
            await call.answer(fuck_off_msg, show_alert=True)
        await state.finish()


# Включает ПП на сервере
async def enable_tp_user(client_id, country):
    if system(f'ssh root@WG_TRY -p 4522 /root/enable_TP_user.sh {country}') == 0:
        config_file = listdir(f'/home/pp/vpn_service/config_files/{country}/')
        send_file = open(f'/home/pp/vpn_service/config_files/{country}/{config_file[0]}', 'rb')
        await bot.send_document(client_id, send_file, caption=after_config_msg)
        send_file.close()
        db.use_try_period(client_id, datetime.today() + relativedelta(days=3), country,
                          config_file[0])
        remove(f'/home/pp/vpn_service/config_files/{country}/{config_file[0]}')
        return 'Ваши конфигурационные файлы уже на подлёте 🦇'
    else:
        await bot.send_photo(client_id, cfg.mustela, hello_new_user_msg, reply_markup=nav.client_main_menu)
        await bot.send_message(cfg.ADMIN_ID, f'Недолёт ПП конфига с {country}')
        return 'Из-за неполадок сети связь с сервером отсутствует. Попробуйте позднее.' \
               ' Техподдержка уже занимается этой проблемой.'


# @dp.callback_query_handler(text_contains='country')
async def cmd_client_country(call: types.callback_query):
    if call.data == 'country_finland':
        if db.check_try_period(call.from_user.id):
            await call.answer('Вы уже использовали свой пробный период. 🤚')
        else:
            # Запустить на сервере скрипт enable_TP_user.sh
            await call.answer(await enable_tp_user(call.from_user.id, call.data[8:]), show_alert=True)
    elif call.data == 'country_german':
        pass
    elif call.data == 'country_netherlands':
        pass
    elif call.data == 'country_swiss':
        pass
    elif call.data == 'country_romania':
        pass
    elif call.data == 'country_britain':
        pass
    elif call.data == 'country_turkey':
        pass
    elif call.data == 'country_argentina':
        pass
    elif call.data == 'country_india':
        pass
    elif call.data == 'country_usa':
        pass
    elif call.data == 'country_back':
        await bot.send_photo(call.from_user.id, cfg.mustela, 'Привет {0.first_name}!\n'.format(call.from_user) +
                             hello_new_user_msg, reply_markup=nav.client_main_menu)


# @dp.callback_query_handler(text_contains='method')
async def cmd_client_method(call: types.callback_query, state: FSMContext):
    if call.data in ('method_qiwi', 'method_yoomoney', 'method_card', 'method_crypta'):
        await state.update_data(chosen_method=call.data[7:])
        await bot.send_photo(call.from_user.id, cfg.mustela, pay_sum_msg, reply_markup=nav.client_pay_menu)
        await state.set_state(IncomePayment.waiting_for_invoice.state)
    elif call.data == 'method_back':
        await state.finish()
        await bot.send_photo(call.from_user.id, cfg.mustela, client_office_msg(db.get_user_data(call.from_user.id)[8]),
                             reply_markup=nav.client_office_menu)


# @dp.callback_query_handler(text_contains='pay')
async def cmd_client_pay(call: types.callback_query, state: FSMContext):
    if call.data in ('pay_325', 'pay_455', 'pay_650'):
        comment = str(call.from_user.id) + '_' + ''.join(sample('abcdefghijklmnopqrstuvwxyz0123456789', 12))
        invoice = await pm.create_invoice((await state.get_data())['chosen_method'], call.data[4:], comment)
        await state.update_data(created_invoice=invoice)
        await bot.send_photo(call.from_user.id, cfg.mustela,
                             invoice_data_msg(comment, call.data[4:], (await state.get_data())['chosen_method']),
                             reply_markup=nav.invoice_menu(invoice[0]))
        await state.set_state(IncomePayment.waiting_for_check.state)
    elif call.data == 'pay_other':
        await call.answer('Введите целое число больше 100', show_alert=True)
        # await bot.send_message(call.from_user.id, 'Введите целое число больше 100')
    elif call.data == 'pay_back':
        await state.finish()
        await bot.send_photo(call.from_user.id, cfg.mustela, client_office_msg(db.get_user_data(call.from_user.id)[8]),
                             reply_markup=nav.client_office_menu)


# @dp.message_handler(content_types='text', state=GiveMoney.waiting_for_money)
async def pay_another(message: types.Message, state: FSMContext):
    if message.text.isdigit() and int(message.text) >= 100:
        comment = str(message.from_user.id) + '_' + ''.join(sample('abcdefghijklmnopqrstuvwxyz0123456789', 12))
        invoice = await pm.create_invoice((await state.get_data())['chosen_method'], int(message.text), comment)
        await state.update_data(created_invoice=invoice)
        await bot.send_photo(message.from_user.id, cfg.mustela,
                             invoice_data_msg(comment, message.text, (await state.get_data())['chosen_method']),
                             reply_markup=nav.invoice_menu(invoice[0]))
        await state.set_state(IncomePayment.waiting_for_check.state)
    else:
        await message.answer('Введите целое число больше 100')


# @dp.callback_query_handler(text_contains='invoice')
async def cmd_pay_check(call: types.callback_query, state: FSMContext):
    if call.data == 'invoice_check':
        if await pm.check_payment(await state.get_data()):
            await call.answer('Вы успешно пополнили баланс, вернитесь в личный кабинет', show_alert=True)
            db.income(call.from_user.id, int((await state.get_data())['created_invoice'][2]), datetime.today(),
                      (await state.get_data())['chosen_method'])
            await bot.send_photo(call.from_user.id, cfg.mustela,
                                 client_office_msg(db.get_user_data(call.from_user.id)[8]),
                                 reply_markup=nav.client_office_menu)
        else:
            await call.answer('Ваш платёж еще не поступил', show_alert=True)
    elif call.data == 'invoice_back':
        await pm.close_invoice(await state.get_data())
        await state.finish()
        await bot.send_photo(call.from_user.id, cfg.mustela, client_office_msg(db.get_user_data(call.from_user.id)[8]),
                             reply_markup=nav.client_office_menu)


# добавить фотки товара
# @dp.message_handler(content_types='photo')
async def different_photos_handler(message: types.Message):
    cms = chat_member_status(await bot.get_chat_member(chat_id=cfg.CHANNEL_NAME, user_id=message.from_user.id))
    if cms in ['administrator', 'creator']:  # and message.chat.type == 'private':
        await message.answer(message.photo[-1].file_id)


def register_client_handlers(dp: Dispatcher):
    dp.register_callback_query_handler(cmd_client_main, text_contains='client')
    dp.register_callback_query_handler(cmd_client_help, text_contains='help')
    dp.register_callback_query_handler(cmd_client_country, text_contains='country')
    dp.register_callback_query_handler(cmd_choose_country, text_contains='country', state=OrderVpn.waiting_for_country)
    dp.register_callback_query_handler(cmd_client_partner, text_contains='partner')
    dp.register_callback_query_handler(cmd_client_office, text_contains='office')
    dp.register_callback_query_handler(cmd_order_control, text_contains='order')
    dp.register_callback_query_handler(cmd_choose_tarif, text_contains='tarif', state=OrderVpn.waiting_for_tarif)
    dp.register_callback_query_handler(cmd_choose_duration, text_contains='duration',
                                       state=OrderVpn.waiting_for_duration)
    dp.register_callback_query_handler(cmd_client_method, text_contains='method',
                                       state=IncomePayment.waiting_for_method)
    dp.register_callback_query_handler(cmd_client_pay, text_contains='pay', state=IncomePayment.waiting_for_invoice)
    dp.register_message_handler(pay_another, content_types='text', state=IncomePayment.waiting_for_invoice)
    dp.register_callback_query_handler(cmd_pay_check, text_contains='invoice', state=IncomePayment.waiting_for_check)

    dp.register_message_handler(different_photos_handler, content_types='photo', chat_type='private')
