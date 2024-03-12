from datetime import datetime, timedelta
from glQiwiApi import YooMoneyAPI, QiwiP2PClient
from aiohttp import ClientSession
import json
import config as cfg



async def create_invoice(method, summ, comment):
    # if method == 'qiwi':
    #     # async with QiwiP2PClient(secret_p2p=cfg.QIWI_PRIV_KEY, shim_server_url=cfg.REFERER_SERVER) as p2p:
    #     async with QiwiP2PClient(secret_p2p=cfg.QIWI_PRIV_KEY) as p2p:
    #         invoice = await p2p.create_p2p_bill(amount=summ, expire_at=datetime.now() + timedelta(hours=1),
    #                                             comment=comment, pay_source_filter=['qw'])
    #         # return p2p.create_shim_url(invoice), invoice.id, summ
    #         return invoice.pay_url, invoice.id, summ
    if method == 'yoomoney':
        return YooMoneyAPI.create_pay_form(
            receiver=cfg.YOOMONEY_WALLET,
            quick_pay_form="small",
            targets="Mustela_VPN",
            payment_type="PC",
            amount=int(summ) * 1.031,
            label=comment), comment, summ
    elif method == 'card':
        # async with QiwiP2PClient(secret_p2p=cfg.QIWI_PRIV_KEY, shim_server_url=cfg.REFERER_SERVER) as p2p:
        # async with QiwiP2PClient(secret_p2p=cfg.QIWI_PRIV_KEY) as p2p:
        #     invoice = await p2p.create_p2p_bill(amount=summ, expire_at=datetime.now() + timedelta(hours=1),
        #                                         comment=comment, pay_source_filter=[method])
        #     # return p2p.create_shim_url(invoice), invoice.id, summ
        #     return invoice.pay_url, invoice.id, summ
        return YooMoneyAPI.create_pay_form(
            receiver=cfg.YOOMONEY_WALLET,
            quick_pay_form="small",
            targets="Mustela_VPN",
            payment_type="AC",
            amount=int(summ) * 1.031,
            label=comment), comment, summ

    elif method == 'crypta':
        raw_link = 'https://api.crystalpay.io/v2/invoice/create/'
        param_dict = {'auth_login': 'Mustela',
                      'auth_secret': 'e4355ecad2143fd1f016a9db024dbe9e2ceadfe3',
                      'amount': summ,
                      'type': 'purchase',
                      'lifetime': '120',
                      'extra': comment}
        async with ClientSession() as session:
            async with session.post(raw_link, data=json.dumps(param_dict)) as response:
                return json.loads(await response.text())['url'], json.loads(await response.text())['id'], summ


async def check_payment(invoice_data):
    # if invoice_data['chosen_method'] in ('qiwi', 'card'):
    #     async with QiwiP2PClient(secret_p2p=cfg.QIWI_PRIV_KEY) as p2p:
    #         if (await p2p.get_bill_by_id(bill_id=invoice_data['created_invoice'][1])).status.value == 'PAID':
    #             return True
    if invoice_data['chosen_method'] in ('yoomoney', 'card'):
        async with YooMoneyAPI(api_access_token=cfg.YOOMONEY_PRIV_KEY) as w:
            history = await w.operation_history()
            summ = int(invoice_data['created_invoice'][2])
            for operation in history:
                if invoice_data['created_invoice'][1] and "status='success'" and "direction='in'" \
                        and f'amount={summ*0.97}' in str(operation):
                    return True
    elif invoice_data['chosen_method'] == 'crypta':
        pay_id = invoice_data['created_invoice'][1]
        raw_link = 'https://api.crystalpay.io/v2/invoice/info/'
        param_dict = {'auth_login': 'Mustela',
                      'auth_secret': 'e4355ecad2143fd1f016a9db024dbe9e2ceadfe3',
                      'id': pay_id}
        async with ClientSession() as session:
            async with session.post(raw_link, data=json.dumps(param_dict)) as response:
                if json.loads(await response.text())['state'] == 'payed':
                    return True
    return False


async def close_invoice(invoice_data):
    if invoice_data['chosen_method'] in ('qiwi', 'card'):
        async with QiwiP2PClient(secret_p2p=cfg.QIWI_PRIV_KEY) as p2p:
            await p2p.reject_p2p_bill(bill_id=invoice_data['created_invoice'][1])

