from datetime import datetime
from os import listdir, system, remove, rename
from random import sample
import asyncio
import math
from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from dateutil.relativedelta import relativedelta

import config as cfg
import markups as nav
import payments as pm
from create_bot import bot
from database import db
from infmsg import *


class OrderVpn(StatesGroup):
    waiting_for_tarif = State()
    waiting_for_country = State()
    waiting_for_duration = State()


class IncomePayment(StatesGroup):
    waiting_for_method = State()
    waiting_for_invoice = State()
    waiting_for_check = State()


class UsePromoCode(StatesGroup):
    waiting_for_promocode = State()


class DemandPartnerMoney(StatesGroup):
    pass


# main_menu
async def cmd_client_main(call: types.callback_query, state: FSMContext):
    if call.data == 'client_choose_vpn':
        await call.bot.edit_message_media(types.InputMediaPhoto(cfg.mustela, choose_tarif_msg), call.from_user.id,
                                          call.message.message_id, reply_markup=nav.tarif_menu)
        await state.set_state(OrderVpn.waiting_for_tarif.state)
    elif call.data == 'client_office':
        user_money = db.get_user_data(call.from_user.id)
        await call.bot.edit_message_media(
            types.InputMediaPhoto(cfg.mustela, client_office_msg(user_money[8], user_money[14])),
            call.from_user.id, call.message.message_id, reply_markup=nav.client_office_menu)
    elif call.data == 'client_partner':
        await call.bot.edit_message_media(
            types.InputMediaPhoto(cfg.mustela, partner_msg(db.get_user_data(call.from_user.id))), call.from_user.id,
            call.message.message_id, reply_markup=nav.gen_partner_menu(db.get_user_data(call.from_user.id)[6]))
    elif call.data == 'client_help':
        await call.bot.edit_message_media(types.InputMediaPhoto(cfg.mustela, help_main_msg), call.from_user.id,
                                          call.message.message_id, reply_markup=nav.client_help_menu)
    elif call.data == 'client_try':
        if db.check_try_period(call.from_user.id):
            await call.answer('Вы уже использовали свой пробный период. 🤚')
        else:
            await call.bot.edit_message_media(types.InputMediaPhoto(cfg.mustela, pick_plat_msg), call.from_user.id,
                                              call.message.message_id, reply_markup=nav.try_plat_menu)


# pick platform menu
async def cmd_client_try(call: types.callback_query):
    if call.data == 'try_back':
        await call.bot.edit_message_media(
            types.InputMediaPhoto(cfg.mustela, 'Привет {0.first_name}!\n'.format(call.from_user) +
                                  hello_new_user_msg), call.from_user.id, call.message.message_id,
            reply_markup=nav.client_main_menu)
    else:
        if db.check_try_period(call.from_user.id):
            await call.answer('Вы уже использовали свой пробный период. 🤚')
        else:
            await call.bot.edit_message_media(
                types.InputMediaPhoto(cfg.mustela, plat_instr_msg(call.data[4:])), call.from_user.id,
                call.message.message_id,
                reply_markup=nav.pick_location_menu)


# pick location menu
async def cmd_client_pick(call: types.callback_query):
    if call.data == 'pick_location':
        if db.check_try_period(call.from_user.id):
            await call.answer('Вы уже использовали свой пробный период. 🤚')
        else:
            await call.bot.edit_message_media(types.InputMediaPhoto(cfg.mustela, pick_location_msg),
                                              call.from_user.id, call.message.message_id,
                                              reply_markup=nav.location_menu)
    elif call.data == 'pick_back':
        await call.bot.edit_message_media(types.InputMediaPhoto(cfg.mustela, pick_plat_msg),
                                          call.from_user.id, call.message.message_id, reply_markup=nav.try_plat_menu)


# help_menu
# @dp.callback_query_handler(text_contains='help')
async def cmd_client_help(call: types.callback_query):
    if call.data == 'help_back':
        await call.bot.edit_message_media(
            types.InputMediaPhoto(cfg.mustela, 'Привет {0.first_name}!\n'.format(call.from_user) +
                                  hello_new_user_msg), call.from_user.id, call.message.message_id,
            reply_markup=nav.client_main_menu)


# @dp.callback_query_handler(text_contains='office')
async def cmd_client_office(call: types.callback_query, state: FSMContext):
    if call.data == 'office_method':
        await call.bot.edit_message_media(types.InputMediaPhoto(cfg.mustela, pay_method_msg), call.from_user.id,
                                          call.message.message_id, reply_markup=nav.client_pay_method)
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
                                               order_data_msg(order[0], order[3], order[4], order[10][:-7], order[8]),
                                               reply_markup=nav.disable_prolong(order[0]))
                    else:
                        await bot.send_message(call.from_user.id,
                                               order_data_msg(order[0], order[3], order[4], order[10][:-7], order[8]),
                                               reply_markup=nav.enable_prolong(order[0]))
                    active_vpn = True
                else:
                    await bot.send_message(call.from_user.id,
                                           order_data_msg(order[0], order[3], order[4], order[10][:-7], order[8]),
                                           reply_markup=nav.activate_order(order[0]))
        if not active_vpn:
            await call.answer(no_try_no_order_msg, show_alert=True)
    elif call.data == 'office_back':
        await call.bot.edit_message_media(
            types.InputMediaPhoto(cfg.mustela, 'Привет {0.first_name}!\n'.format(call.from_user) +
                                  hello_new_user_msg), call.from_user.id,
            call.message.message_id, reply_markup=nav.client_main_menu)
    elif call.data == 'office_need_conf':
        if db.check_orders(call.from_user.id):
            for order in db.check_orders(call.from_user.id):
                if order[9]:
                    config_files = listdir(f'/root/{order[4]}_{order[5]}/work/{order[6]}/clients/{order[7]}')
                    for i in range(int(order[3])):
                        send_file = open(
                            f'/root/{order[4]}_{order[5]}/work/{order[6]}/clients/{order[7]}/{config_files[i]}', 'rb')
                        await bot.send_document(call.from_user.id, send_file, caption=after_config_msg)
                        send_file.close()
                else:
                    await bot.send_message(call.from_user.id, dead_order_msg(order[0]))
        else:
            await call.answer('У вас нет активных подписок.')
    elif call.data == 'office_promocode':
        if db.check_promos():
            await call.bot.edit_message_media(
                types.InputMediaPhoto(cfg.mustela, promo_code_msg), call.from_user.id,
                call.message.message_id, reply_markup=nav.promo_back_menu)
            await state.set_state(UsePromoCode.waiting_for_promocode.state)
            await state.update_data(msg_id=call.message.message_id)
        else:
            await call.answer('Сейчас нет активных промо кодов')


async def cmd_promo_back(call: types.callback_query, state: FSMContext):
    if call.data == 'promo_back':
        await state.finish()
        user_data = db.get_user_data(call.from_user.id)
        print(user_data)
        await call.bot.edit_message_media(
            types.InputMediaPhoto(cfg.mustela, client_office_msg(user_data[8], user_data[14])),
            call.from_user.id, call.message.message_id, reply_markup=nav.client_office_menu)


async def cmd_promo_code(message: types.Message, state: FSMContext):
    promos_data = db.check_promos()
    if message.text == promos_data[0]:
        await message.delete()
        # проверить активен ли промокод
        promo_active = True
        if promos_data[4]:
            if datetime.today() >= datetime.fromisoformat(promos_data[4]):
                promo_active = False
        elif promos_data[5]:
            if promos_data[3] >= promos_data[5]:
                promo_active = False
        if promo_active:
            if tuple([message.text]) in db.check_used_promos(message.from_user.id):
                msg = await message.answer('Вы уже использовали этот промокод.')
            else:
                user_data = db.get_user_data(message.from_user.id)
                db.use_promo_code(message.from_user.id, promos_data[0], promos_data[2], promos_data[3], user_data[14])
                await bot.delete_message(message.from_user.id, (await state.get_data())['msg_id'])
                # print((await state.get_data())['msg_id'])
                await state.finish()
                user_data = db.get_user_data(message.from_user.id)
                msg = await message.answer('Промокод принят!!')
                await bot.send_photo(message.from_user.id, cfg.mustela, client_office_msg(user_data[8], user_data[14]),
                                     reply_markup=nav.client_office_menu)
        else:
            msg = await message.answer('Вы ввели неактивный промокод.')
            db.set_promo_inactive(promos_data[0])
            await state.finish()
            user_data = db.get_user_data(message.from_user.id)
            await bot.send_photo(message.from_user.id, cfg.mustela, client_office_msg(user_data[8], user_data[14]),
                                 reply_markup=nav.client_office_menu)
    else:
        await message.delete()
        msg = await message.answer('Вы ввели неверный или неактивный промокод.')
    asyncio.create_task(delete_message(msg, 3))


# @dp.callback_query_handler(text_contains='order')
async def cmd_order_control(call: types.callback_query):
    if call.data[:21] == 'order_disable_prolong':
        db.set_order_prolong(0, call.data[22:])
        await call.answer(f'Автопродление заказа {call.data[22:]} отключено.')
    elif call.data[:20] == 'order_enable_prolong':
        db.set_order_prolong(1, call.data[21:])
        await call.answer(f'Автопродление заказа {call.data[21:]} включено.')
    elif call.data[:14] == 'order_activate':
        order_data = db.get_order_data(call.data[15:])
        user_data = db.get_user_data(call.from_user.id)
        price = db.check_price(order_data[3], order_data[8])[0]
        can_buy = await check_can_buy(user_data[8], user_data[12], user_data[14], price)
        if can_buy[0]:
            if system(f'ssh root@{order_data[4]}_{order_data[5]}_WORK_{order_data[6]} -p 4522 '
                      f'/root/enable_payed_user.sh {order_data[7]}') == 0:
                db.activate_order(datetime.today() + relativedelta(months=order_data[8]), order_data[0], can_buy[1],
                                  can_buy[2], call.from_user.id)
                await call.answer(f'Ваш заказ номер {order_data[0]} успешно активирован')
            else:
                await call.answer('Из-за неполадок сети связь с сервером отсутствует. Попробуйте позднее.'
                                  ' Техподдержка уже занимается этой проблемой.')
                await bot.send_message(cfg.ADMIN_ID, f'Сервер {order_data[4:6]} недоступен')
        elif not can_buy[0] and not can_buy[1]:
            await call.answer(f'Недостаточно средств для активации выбранного заказа. Пополните пожалуйста счёт.')
        elif not can_buy[0] and can_buy[1]:
            await call.answer(fuck_off_msg, show_alert=True)


# @dp.callback_query_handler(text_contains='partner')
async def cmd_client_partner(call: types.callback_query):
    if call.data == 'partner_back':
        await call.bot.edit_message_media(
            types.InputMediaPhoto(cfg.mustela, 'Привет {0.first_name}!\n'.format(call.from_user) +
                                  hello_new_user_msg), call.from_user.id,
            call.message.message_id, reply_markup=nav.client_main_menu)
    elif call.data == 'partner_take_money':
        if db.get_user_data(call.from_user.id)[10] < 500:
            await call.answer('Недостаточно средств для вывода.\n Минимальная сумма для вывода 500 рублей.',
                              show_alert=True)
        else:
            # тоже нужен FSM
            # db.take_ref_money(call.from_user.id, 10)
            await bot.send_message(call.from_user.id, 'Вывод средств с парнёрки, пока фиксированная сумма 10$!!')
    elif call.data == 'partner_my_refs':
        my_refs = db.show_my_refs(call.from_user.id)
        if my_refs:
            for ref in my_refs:
                await bot.send_message(call.from_user.id, f'Имя:         {ref[0]}\n'
                                                          f'Имя пользователя в телеграм:\n'
                                                          f'{ref[1]}')
        else:
            await call.answer('У вас ещё нет рефералов.')



async def cmd_choose_tarif(call: types.callback_query, state: FSMContext):
    if call.data == 'tarif_back':
        await state.finish()
        await call.bot.edit_message_media(
            types.InputMediaPhoto(cfg.mustela, 'Привет {0.first_name}!\n'.format(call.from_user) + hello_new_user_msg),
            call.from_user.id, call.message.message_id, reply_markup=nav.client_main_menu)
    else:
        await state.update_data(chosen_tarif=call.data[6:])
        await call.bot.edit_message_media(types.InputMediaPhoto(cfg.mustela, choose_geo_msg), call.from_user.id,
                                          call.message.message_id, reply_markup=nav.country_menu)
        await state.set_state(OrderVpn.waiting_for_country.state)


async def cmd_choose_country(call: types.callback_query, state: FSMContext):
    if call.data == 'country_back':
        await state.finish()
        await call.bot.edit_message_media(
            types.InputMediaPhoto(cfg.mustela, 'Привет {0.first_name}!\n'.format(call.from_user) + hello_new_user_msg),
            call.from_user.id, call.message.message_id, reply_markup=nav.client_main_menu)
    else:
        await state.update_data(chosen_country=call.data[8:])
        await call.bot.edit_message_media(types.InputMediaPhoto(cfg.mustela, choose_duration_msg), call.from_user.id,
                                          call.message.message_id, reply_markup=nav.duration_menu)
        await state.set_state(OrderVpn.waiting_for_duration.state)


async def cmd_choose_duration(call: types.callback_query, state: FSMContext):
    if call.data == 'duration_back':
        await state.finish()
        await call.bot.edit_message_media(
            types.InputMediaPhoto(cfg.mustela, 'Привет {0.first_name}!\n'.format(call.from_user) + hello_new_user_msg),
            call.from_user.id, call.message.message_id, reply_markup=nav.client_main_menu)
    else:
        await state.update_data(chosen_duration=call.data[9:])
        price = db.check_price(int((await state.get_data())['chosen_tarif']),
                               int((await state.get_data())['chosen_duration']))[0]
        user_data = db.get_user_data(call.from_user.id)
        can_buy = await check_can_buy(user_data[8], user_data[12], user_data[14], price)
        if can_buy[0]:
            country = (await state.get_data())['chosen_country']
            servers_amount = len(listdir(f'/root/{country}/work'))
            free_work_server = db.pick_work_server(country, servers_amount)
            interfaces = listdir(f'/root/{country}/work/{free_work_server}/wsc')
            client_interface = interfaces[0][10:19]
            if system(f'ssh root@{country}_WORK_{free_work_server} -p 4522 /root/enable_payed_user.sh '
                      f'{client_interface}') == 0:
                config_files = listdir(f'/root/{country}/work/{free_work_server}/clients/{client_interface}')
                for i in range(int((await state.get_data())['chosen_tarif'])):
                    send_file = open(f'/root/{country}/work/{free_work_server}/clients/{client_interface}/'
                                     f'{config_files[i]}', 'rb')
                    await bot.send_document(call.from_user.id, send_file, caption=after_config_msg) #,
                                            # reply_markup=nav.after_config_menu)
                    send_file.close()
                await bot.delete_message(call.from_user.id, call.message.message_id)
                remove(f'/root/{country}/work/{free_work_server}/wsc/{interfaces[0]}')
                db.make_order(call.from_user.id, datetime.today(), int((await state.get_data())['chosen_tarif']),
                              (await state.get_data())['chosen_country'], free_work_server, client_interface,
                              int((await state.get_data())['chosen_duration']),
                              datetime.today() + relativedelta(months=int((await state.get_data())['chosen_duration'])),
                              can_buy[1], can_buy[2], call.from_user.full_name)
                await call.answer(congrats_msg)
            else:
                await call.bot.edit_message_media(
                    types.InputMediaPhoto(cfg.mustela, 'Привет {0.first_name}!\n'.format(call.from_user) +
                                          hello_new_user_msg), call.from_user.id, call.message.message_id,
                    reply_markup=nav.client_main_menu)
                await bot.send_message(cfg.ADMIN_ID, f'Недолёт ПП конфига с {country}_{free_work_server}')
                await call.answer('Из-за неполадок сети связь с сервером отсутствует. Попробуйте позднее. '
                                  'Техподдержка уже занимается этой проблемой.', show_alert=True)

        elif not can_buy[0] and not can_buy[1]:
            await call.answer(not_enaugh_money_msg, show_alert=True)
            await call.bot.edit_message_media(
                types.InputMediaPhoto(cfg.mustela,
                                      'Привет {0.first_name}!\n'.format(call.from_user) + hello_new_user_msg),
                call.from_user.id, call.message.message_id, reply_markup=nav.client_main_menu)
        elif not can_buy[0] and can_buy[1]:
            await call.answer(fuck_off_msg, show_alert=True)
        await state.finish()


# @dp.callback_query_handler(text='to_main_menu')
async def cmd_to_main_menu(call: types.callback_query):
    await bot.send_photo(call.from_user.id, cfg.mustela, '<b>Привет {0.first_name}!</b>\n'
                         .format(call.from_user) + hello_new_user_msg, reply_markup=nav.client_main_menu)


# @dp.callback_query_handler(text_contains='location')
async def cmd_client_location(call: types.callback_query):
    if call.data == 'location_back':
        await call.bot.edit_message_media(
            types.InputMediaPhoto(cfg.mustela, 'Привет {0.first_name}!\n'.format(call.from_user) +
                                  hello_new_user_msg), call.from_user.id, call.message.message_id,
            reply_markup=nav.client_main_menu)
    else:
        if db.check_try_period(call.from_user.id):
            await call.answer('Вы уже использовали свой пробный период. 🤚')
        else:
            config_file = sorted(listdir(f'/root/{call.data[9:]}/try/0'))[0]
            if system(f'ssh root@{call.data[9:]}_TRY_0 -p 4522 /root/enable_TP_user.sh {config_file}') == 0:
                db.use_try_period(call.from_user.id, datetime.today() + relativedelta(days=3), call.data[9:],
                                  config_file, call.from_user.full_name)
                send_file = open(f'/root/{call.data[9:]}/try/0/{config_file}', 'rb')
                await bot.send_document(call.from_user.id, send_file, caption=after_config_msg)
                send_file.close()
                remove(f'/root/{call.data[9:]}/try/0/{config_file}')
            else:
               await call.answer('Cервер недоступен. Техподдержка уже занимается этой проблемой', show_alert=True)
               await bot.send_photo(call.from_user.id, cfg.mustela, hello_new_user_msg,
                                    reply_markup=nav.client_main_menu)
               await bot.send_message(cfg.ADMIN_ID, f'Недолёт ПП конфига с {call.data[9:]}')
            

# @dp.callback_query_handler(text_contains='method')
async def cmd_client_method(call: types.callback_query, state: FSMContext):
    if call.data in ('method_qiwi', 'method_yoomoney', 'method_card', 'method_crypta'):
        await state.update_data(chosen_method=call.data[7:])
        await call.bot.edit_message_media(types.InputMediaPhoto(cfg.mustela, pay_sum_msg), call.from_user.id,
                                          call.message.message_id, reply_markup=nav.client_pay_menu)
        await state.set_state(IncomePayment.waiting_for_invoice.state)
    elif call.data == 'method_back':
        await state.finish()
        user_money = db.get_user_data(call.from_user.id)
        await call.bot.edit_message_media(
            types.InputMediaPhoto(cfg.mustela, client_office_msg(user_money[8], user_money[14])),
            call.from_user.id, call.message.message_id, reply_markup=nav.client_office_menu)


# @dp.callback_query_handler(text_contains='pay')
async def cmd_client_pay(call: types.callback_query, state: FSMContext):
    if call.data in ('pay_180', 'pay_325', 'pay_455', 'pay_650'):
        comment = str(call.from_user.id) + '_' + ''.join(sample('abcdefghijklmnopqrstuvwxyz0123456789', 12))
        invoice = await pm.create_invoice((await state.get_data())['chosen_method'], call.data[4:], comment)
        await state.update_data(created_invoice=invoice)
        await call.bot.edit_message_media(types.InputMediaPhoto(cfg.mustela,
                                                                invoice_data_msg(comment, call.data[4:],
                                                                                 (await state.get_data())[
                                                                                     'chosen_method'])),
                                          call.from_user.id, call.message.message_id,
                                          reply_markup=nav.invoice_menu(invoice[0]))
        await state.set_state(IncomePayment.waiting_for_check.state)
    elif call.data == 'pay_other':
        await state.update_data(msg_id=call.message.message_id)
        await call.answer('Введите целое число больше 100', show_alert=True)
    elif call.data == 'pay_back':
        await state.finish()
        user_money = db.get_user_data(call.from_user.id)
        await call.bot.edit_message_media(
            types.InputMediaPhoto(cfg.mustela, client_office_msg(user_money[8], user_money[14])),
            call.from_user.id, call.message.message_id, reply_markup=nav.client_office_menu)


# @dp.message_handler(content_types='text', state=GiveMoney.waiting_for_money)
async def pay_another(message: types.Message, state: FSMContext):
    if message.text.isdigit() and int(message.text) >= 100:
        await message.delete()
        comment = str(message.from_user.id) + '_' + ''.join(sample('abcdefghijklmnopqrstuvwxyz0123456789', 12))
        invoice = await pm.create_invoice((await state.get_data())['chosen_method'], int(message.text), comment)
        await state.update_data(created_invoice=invoice)
        await bot.delete_message(message.from_user.id, (await state.get_data())['msg_id'])
        await bot.send_photo(message.from_user.id, cfg.mustela,
                             invoice_data_msg(comment, message.text, (await state.get_data())['chosen_method']),
                             reply_markup=nav.invoice_menu(invoice[0]))
        await state.set_state(IncomePayment.waiting_for_check.state)
    else:
        await message.delete()
        msg = await message.answer('Введите целое число больше 100')
        asyncio.create_task(delete_message(msg, 3))


# @dp.callback_query_handler(text_contains='invoice')
async def cmd_pay_check(call: types.callback_query, state: FSMContext):
    if call.data == 'invoice_check':
        if await pm.check_payment(await state.get_data()):
            await call.answer('Вы успешно пополнили баланс, вернитесь в личный кабинет', show_alert=True)
            db.income(call.from_user.id, int((await state.get_data())['created_invoice'][2]), datetime.today(),
                      (await state.get_data())['chosen_method'], call.from_user.full_name)
            user_money = db.get_user_data(call.from_user.id)
            await call.bot.edit_message_media(
                types.InputMediaPhoto(cfg.mustela, client_office_msg(user_money[8], user_money[14])),
                call.from_user.id, call.message.message_id, reply_markup=nav.client_office_menu)
            await state.finish()
        else:
            await call.answer('Ваш платёж еще не поступил', show_alert=True)
    elif call.data == 'invoice_back':
        await pm.close_invoice(await state.get_data())
        await state.finish()
        user_money = db.get_user_data(call.from_user.id)
        await call.bot.edit_message_media(
            types.InputMediaPhoto(cfg.mustela, client_office_msg(user_money[8], user_money[14])),
            call.from_user.id, call.message.message_id, reply_markup=nav.client_office_menu)


async def delete_message(message: types.Message, sleep_time: int = 0):
    await asyncio.sleep(sleep_time)
    await message.delete()


async def check_can_buy(on_accaunt, black_mark, promo_on_acc, price):
    if black_mark:
        return False, black_mark
    elif on_accaunt < math.floor(price/2):
        return False, black_mark
    elif promo_on_acc <= math.ceil(price/2):
        return True, on_accaunt - price + promo_on_acc, 0
    elif promo_on_acc > math.ceil(price/2):
        return True, on_accaunt - price + math.ceil(price/2), promo_on_acc - math.ceil(price/2)


def register_client_handlers(dp: Dispatcher):
    dp.register_callback_query_handler(cmd_client_main, text_contains='client')
    dp.register_callback_query_handler(cmd_client_help, text_contains='help')
    dp.register_callback_query_handler(cmd_client_try, text_contains='try')
    dp.register_callback_query_handler(cmd_client_pick, text_contains='pick')
    dp.register_callback_query_handler(cmd_client_location, text_contains='location')
    dp.register_callback_query_handler(cmd_choose_country, text_contains='country', state=OrderVpn.waiting_for_country)
    dp.register_callback_query_handler(cmd_client_partner, text_contains='partner')
    dp.register_callback_query_handler(cmd_client_office, text_contains='office')
    dp.register_callback_query_handler(cmd_promo_back, text='promo_back', state=UsePromoCode.waiting_for_promocode)
    dp.register_message_handler(cmd_promo_code, content_types='text', state=UsePromoCode.waiting_for_promocode)
    dp.register_callback_query_handler(cmd_order_control, text_contains='order')
    dp.register_callback_query_handler(cmd_choose_tarif, text_contains='tarif', state=OrderVpn.waiting_for_tarif)
    dp.register_callback_query_handler(cmd_choose_duration, text_contains='duration',
                                       state=OrderVpn.waiting_for_duration)
    dp.register_callback_query_handler(cmd_to_main_menu, text='to_main_menu')
    dp.register_callback_query_handler(cmd_client_method, text_contains='method',
                                       state=IncomePayment.waiting_for_method)
    dp.register_callback_query_handler(cmd_client_pay, text_contains='pay', state=IncomePayment.waiting_for_invoice)
    dp.register_message_handler(pay_another, content_types='text', state=IncomePayment.waiting_for_invoice)
    dp.register_callback_query_handler(cmd_pay_check, text_contains='invoice', state=IncomePayment.waiting_for_check)
