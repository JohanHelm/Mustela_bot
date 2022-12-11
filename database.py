import sqlite3


class Database:
    def __init__(self, db_file):
        self.connection = sqlite3.connect(db_file)
        self.cursor = self.connection.cursor()

    def user_exists(self, user_id):
        with self.connection:
            result = self.cursor.execute("SELECT * FROM users WHERE user_id = ?", (user_id,)).fetchmany(1)
            return bool(len(result))

    def add_user(self, user_id, full_name, lang, mention, ref_link, whos_ref):
        with self.connection:
            self.cursor.execute("INSERT INTO users ('user_id', 'full_name', 'lang', 'mention', 'ref_link','whos_ref')"
                                " VALUES (?, ?, ?, ?, ?, ?)", (user_id, full_name, lang, mention, ref_link, whos_ref,))

    def set_active(self, user_id, active):
        with self.connection:
            return self.cursor.execute("UPDATE users SET active = ? WHERE user_id = ?", (active, user_id,))

    def get_users(self):
        with self.connection:
            return self.cursor.execute("SELECT mention, user_id, full_name, active FROM users").fetchall()

    def check_try_period(self, user_id):
        with self.connection:
            return self.cursor.execute("SELECT * FROM try_period WHERE user_id = ?", (user_id,)).fetchmany(1)

    def use_try_period(self, user_id, try_period_expires, country, client_name):
        with self.connection:
            self.cursor.execute("INSERT INTO try_period ('user_id', 'expires_at', 'country', 'client_name')"
                                " VALUES (?, ?, ?, ?)", (user_id, try_period_expires, country, client_name,))

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

    def make_order(self, customer_id, today_d_t, tarif, country, client_interface, duration, expires_at, price):
        with self.connection:
            self.cursor.execute(
                "INSERT INTO orders ('customer_id', 'date_time', 'tarif', 'country', 'interface', 'duration',"
                " 'expires_at') VALUES (?, ?, ?, ?, ?, ?, ?)",
                (customer_id, today_d_t, tarif, country, client_interface, duration, expires_at,))
            on_accaunt = (self.cursor.execute("SELECT on_accaunt FROM users WHERE user_id = ?",
                                              (customer_id,)).fetchone())[0]
            self.cursor.execute("UPDATE users SET on_accaunt = ? WHERE user_id = ?", (on_accaunt - price, customer_id,))

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

    def income(self, customer_id, summ, date_time, method):
        with self.connection:
            self.cursor.execute("INSERT INTO income ('customer_id', 'summ', 'date_time', 'method') VALUES (?, ?, ?, ?)",
                                (customer_id, summ, date_time, method,))
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

    def prolong_order(self, user_id, on_accaunt, price, order_id, expires_at):
        with self.connection:
            self.cursor.execute("UPDATE users SET on_accaunt = ? WHERE user_id = ?", (on_accaunt - price, user_id,))
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

    def activate_order(self, expires_at, order_id, on_accaunt, price, customer_id):
        with self.connection:
            self.cursor.execute("UPDATE orders SET active = ?, expires_at = ? WHERE id = ?", (1, expires_at, order_id,))
            self.cursor.execute("UPDATE users SET on_accaunt = ? WHERE user_id = ?", (on_accaunt - price, customer_id,))

db = Database('vpn_service.db')
