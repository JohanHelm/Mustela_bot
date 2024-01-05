import sqlite3


class Database:
    def __init__(self, db_file):
        self.connection = sqlite3.connect(db_file)
        self.cursor = self.connection.cursor()

    def user_exists(self, user_id):
        with self.connection:
            result = self.cursor.execute("SELECT * FROM users WHERE user_id = ?", (user_id,)).fetchmany(1)
            return bool(len(result))

    def add_user(self, user_id, full_name, lang, mention, ref_link, whos_ref, reg_date):
        with self.connection:
            self.cursor.execute(
                "INSERT INTO users ('user_id', 'full_name', 'lang', 'mention', 'ref_link','whos_ref', 'reg_date')"
                " VALUES (?, ?, ?, ?, ?, ?, ?)", (user_id, full_name, lang, mention, ref_link, whos_ref, reg_date,))

    def set_active(self, user_id, active):
        with self.connection:
            return self.cursor.execute("UPDATE users SET active = ? WHERE user_id = ?", (active, user_id,))

    def get_users(self):
        with self.connection:
            return self.cursor.execute("SELECT * FROM users").fetchall()

    def check_try_period(self, user_id):
        with self.connection:
            return self.cursor.execute("SELECT * FROM try_period WHERE user_id = ?", (user_id,)).fetchmany(1)

    def use_try_period(self, user_id, try_period_expires, country, client_name, full_name):
        with self.connection:
            self.cursor.execute("INSERT INTO try_period ('user_id', 'expires_at', 'country', 'client_name', 'city',"
                                " 'num', 'full_name') VALUES (?, ?, ?, ?, ?, ?, ?)",
                                (user_id, try_period_expires, country.split('_')[0], client_name, country.split('_')[1],
                                 '0', full_name,))

    def check_price(self, tarif, duration):
        with self.connection:
            if duration == 1:
                return self.cursor.execute("SELECT one_month FROM tarifs WHERE tarif = ?", (tarif,)).fetchone()
            elif duration == 3:
                return self.cursor.execute("SELECT three_months FROM tarifs WHERE tarif = ?", (tarif,)).fetchone()
            elif duration == 6:
                return self.cursor.execute("SELECT six_months FROM tarifs WHERE tarif = ?", (tarif,)).fetchone()
            elif duration == 12:
                return self.cursor.execute("SELECT one_year FROM tarifs WHERE tarif = ?", (tarif,)).fetchone()
            elif duration == 24:
                return self.cursor.execute("SELECT two_years FROM tarifs WHERE tarif = ?", (tarif,)).fetchone()
            elif duration == 36:
                return self.cursor.execute("SELECT three_years FROM tarifs WHERE tarif = ?", (tarif,)).fetchone()

    def make_order(self, customer_id, today_d_t, tarif, country, num, client_interface, duration, expires_at,
                   on_accaunt, promo_on_acc, full_name):
        with self.connection:
            self.cursor.execute(
                "INSERT INTO orders ('customer_id', 'date_time', 'tarif', 'country', 'city', 'num', 'interface', "
                "'duration', 'expires_at', 'full_name') VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                (customer_id, today_d_t, tarif, country.split('_')[0], country.split('_')[1], num, client_interface,
                 duration, expires_at, full_name,))
            # on_accaunt = (self.cursor.execute("SELECT on_accaunt FROM users WHERE user_id = ?",
            #                                   (customer_id,)).fetchone())[0]
            # self.cursor.execute("UPDATE users SET on_accaunt = ? WHERE user_id = ?", (on_accaunt - price, customer_id,))
            self.cursor.execute("UPDATE users SET on_accaunt = ?, promo_on_acc = ? WHERE user_id = ?",
                                (on_accaunt, promo_on_acc, customer_id,))

    def check_orders(self, user_id):
        with self.connection:
            return self.cursor.execute("SELECT * FROM orders WHERE customer_id = ?", (user_id,)).fetchall()

    def get_user_data(self, user_id):
        with self.connection:
            return self.cursor.execute("SELECT * FROM users where user_id = ?", (user_id,)).fetchone()

    def add_refs_amount(self, user_id):
        with self.connection:
            refs_amount = (
                self.cursor.execute("SELECT refs_amount FROM users where user_id = ?", (user_id,)).fetchone())
            self.cursor.execute("UPDATE users SET refs_amount = ? WHERE user_id = ?", (refs_amount[0] + 1, user_id,))

    def income(self, customer_id, summ, date_time, method, full_name):
        with self.connection:
            self.cursor.execute(
                "INSERT INTO income ('customer_id', 'summ', 'date_time', 'method', 'full_name') VALUES (?, ?, ?, ?, ?)",
                (customer_id, summ, date_time, method, full_name,))
            on_acc = (self.cursor.execute("SELECT whos_ref, on_accaunt FROM users WHERE user_id = ?",
                                          (customer_id,)).fetchone())
            self.cursor.execute("UPDATE users SET on_accaunt = ? WHERE user_id = ?", (on_acc[1] + summ, customer_id,))
            if on_acc[0]:
                whos_ref_on_acc = (
                    self.cursor.execute("SELECT on_accaunt, from_refs, avialable FROM users WHERE user_id = ?",
                                        (on_acc[0],)).fetchone())
                self.cursor.execute("UPDATE users SET on_accaunt = ?, from_refs = ?, avialable = ? WHERE user_id = ?", (
                    whos_ref_on_acc[0] + 0.1 * summ, whos_ref_on_acc[1] + 0.1 * summ, whos_ref_on_acc[2] + 0.1 * summ,
                    on_acc[0],))

    def check_income(self, customer_id):
        with self.connection:
            return self.cursor.execute("SELECT * FROM income WHERE customer_id = ?", (customer_id,)).fetchall()

    def take_ref_money(self, customer_id, summ):
        with self.connection:
            user_data = (self.cursor.execute("SELECT on_accaunt, avialable FROM users where user_id = ?",
                                             (customer_id,)).fetchone())
            self.cursor.execute("UPDATE users SET on_accaunt = ?, avialable = ? WHERE user_id = ?",
                                (user_data[0] - summ, user_data[1] - summ, customer_id,))

    def try_period_data(self):
        with self.connection:
            return self.cursor.execute('SELECT * FROM try_period WHERE active = ? ORDER BY expires_at', (1,)).fetchall()

    def block_try_period(self, user_id):
        with self.connection:
            self.cursor.execute("UPDATE try_period SET active = ? WHERE user_id = ?", (0, user_id,))

    def payed_config_data(self):
        with self.connection:
            return self.cursor.execute('SELECT * FROM orders WHERE active = ? ORDER BY expires_at', (1,)).fetchall()

    def prolong_order(self, user_id, on_accaunt, promo_on_acc, order_id, expires_at):
        with self.connection:
            self.cursor.execute("UPDATE users SET on_accaunt = ?, promo_on_acc = ? WHERE user_id = ?",
                                (on_accaunt, promo_on_acc, user_id,))
            self.cursor.execute("UPDATE orders SET expires_at = ? WHERE id = ?", (expires_at, order_id,))

    def mark_order_inactive(self, order_id):
        with self.connection:
            self.cursor.execute("UPDATE orders SET active = ? WHERE id = ?", (0, order_id,))

    def set_order_prolong(self, prolong, order_id):
        with self.connection:
            self.cursor.execute("UPDATE orders SET prolong = ? WHERE id = ?", (prolong, order_id,))

    def get_order_data(self, order_id):
        with self.connection:
            return self.cursor.execute("SELECT * FROM orders WHERE id = ?", (order_id,)).fetchone()

    def activate_order(self, expires_at, order_id, on_accaunt, promo_on_acc, customer_id):
        with self.connection:
            self.cursor.execute("UPDATE orders SET active = ?, expires_at = ? WHERE id = ?", (1, expires_at, order_id,))
            self.cursor.execute("UPDATE users SET on_accaunt = ?, promo_on_acc = ? WHERE user_id = ?",
                                (on_accaunt, promo_on_acc, customer_id,))

    def incomes_data(self):
        with self.connection:
            return self.cursor.execute("SELECT * FROM income").fetchall()

    def pick_work_server(self, country, servers_amount):
        with self.connection:
            servers_list = []
            for i in range(servers_amount):
                servers_list.append(self.cursor.execute(
                    "SELECT COUNT(num) FROM orders WHERE country = ? AND city = ? AND active = ? AND num =?",
                    (country.split('_')[0], country.split('_')[1], 1, i,)).fetchone()[0])
            return servers_list.index(min(servers_list))

    def check_promos(self):
        with self.connection:
            return self.cursor.execute("SELECT * FROM promos WHERE active = ?", (1,)).fetchone()

    def check_used_promos(self, user_id):
        with self.connection:
            return self.cursor.execute("SELECT promo_code FROM used_promos WHERE user_id = ?", (user_id,)).fetchall()

    def use_promo_code(self, user_id, promo_code, promo_money, used_times, promo_on_acc):
        with self.connection:
            self.cursor.execute("UPDATE promos SET used_times = ? WHERE promo_code = ?", (used_times + 1, promo_code,))
            self.cursor.execute("INSERT INTO used_promos ('user_id', 'promo_code') VALUES (?, ?)",
                                (user_id, promo_code,))
            self.cursor.execute("UPDATE users SET promo_on_acc = ? WHERE user_id = ?",
                                (promo_money + promo_on_acc, user_id,))

    def set_promo_inactive(self, promo_code):
        with self.connection:
            self.cursor.execute("UPDATE promos SET active = ? WHERE promo_code = ?", (0, promo_code,))

    def show_my_refs(self, user_id):
        with self.connection:
            return self.cursor.execute("SELECT full_name, mention FROM users WHERE whos_ref = ?", (user_id,)).fetchall()


db = Database('vpn_service.db')

