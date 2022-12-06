from pyqiwip2p import AioQiwiP2P
from pyqiwip2p.p2p_types import QiwiCustomer, QiwiDatetime, PaymentMethods
from glQiwiApi import YooMoneyAPI
from aiohttp import ClientSession
import json
import config as cfg


p2p = AioQiwiP2P(auth_key=cfg.QIWI_PRIV_KEY)


async def create_invoice(method, summ, comment):
    if method == 'qiwi':
        invoice = await p2p.bill(amount=summ, lifetime=60, comment=comment, pay_sources=[PaymentMethods.qiwi])
        return invoice.pay_url, invoice.bill_id, summ
    elif method == 'yoomoney':
        return YooMoneyAPI.create_pay_form(
            receiver=cfg.YOOMONEY_WALLET,
            quick_pay_form="small",
            targets="Mustela_VPN",
            payment_type="PC",
            amount=summ,
            label=comment), comment, summ
    elif method == 'card':
        invoice = await p2p.bill(amount=summ, lifetime=60, comment=comment, pay_sources=[PaymentMethods.card])
        return invoice.pay_url, invoice.bill_id, summ
    elif method == 'crypta':
        raw_link = f'https://api.crystalpay.ru/v1/?s=e4355ecad2143fd1f016a9db024dbe9e2ceadfe3&n=Mustela&' \
                   f'o=invoice-create&amount={summ}&lifetime=60&extra={comment}'
        async with ClientSession() as session:
            async with session.get(raw_link) as response:
                pay_id = json.loads(await response.text())['id']
                # pay_id = (await response.text()).split(',')[0].split(':')[1].replace('"', '')
                # pay_url = f'https://pay.crystalpay.ru/?i={pay_id}'
                return f'https://pay.crystalpay.ru/?i={pay_id}', pay_id, summ


async def check_payment(invoice_data):
    if invoice_data['chosen_method'] in ('qiwi', 'card'):
        if (await p2p.check(bill_id=invoice_data['created_invoice'][1])).status == 'PAID':
            return True
    elif invoice_data['chosen_method'] == 'yoomoney':
        async with YooMoneyAPI(api_access_token=cfg.YOOMONEY_PRIV_KEY) as w:
            history = await w.operation_history()
            summ = int(invoice_data['created_invoice'][2])
            for operation in history:
                if invoice_data['created_invoice'][1] and "status='success'" and "direction='in'" \
                        and f'amount={summ*0.97}' in str(operation):
                    return True
    elif invoice_data['chosen_method'] == 'crypta':
        pay_id = invoice_data['created_invoice'][1]
        raw_link = f'https://api.crystalpay.ru/v1/?s=e4355ecad2143fd1f016a9db024dbe9e2ceadfe3&n=Mustela&' \
                   f'o=invoice-check&i={pay_id}'
        async with ClientSession() as session:
            async with session.get(raw_link) as response:
                if json.loads(await response.text())['state'] == 'payed':
                    return True
    return False


async def close_invoice(invoice_data):
    if invoice_data['chosen_method'] in ('qiwi', 'card'):
        await p2p.reject(bill_id=invoice_data['created_invoice'][1])
