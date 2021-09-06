import sqlite3


class Keys:
    def __init__(self, database_file):
        self.connection = sqlite3.connect(database_file, timeout=10)
        self.cursor = self.connection.cursor()

    def write_keys(self, key):
        with self.connection:
            ID = len(self.cursor.execute("SELECT * FROM Keys").fetchall())
            return self.cursor.execute(f"INSERT INTO Keys VALUES(?,?)",(ID+1,key))
    def chek_keys(self, key):
        with self.connection:
            keys = self.cursor.execute("SELECT * FROM Keys").fetchall()
            if len(keys) == 0:
                return True
            for i in range(0, len(keys)):
                have = keys[i][-1]

                if have == key:
                    print('Bad')
                    return False
                else:
                    return True

    def get_key(self):
        with self.connection:
            ID = len(self.cursor.execute("SELECT * FROM Keys").fetchall())
            key = self.cursor.execute("SELECT * FROM Keys WHERE id = ?", (ID,)).fetchone()[-1]
            self.cursor.execute("DELETE  FROM Keys WHERE key = ?", (key,))
            return key

class Orders:
    def __init__(self, database_file):
        self.connection = sqlite3.connect(database_file,timeout=10)
        self.cursor = self.connection.cursor()
    def registration(self, user_id):
        with self.connection:
            ID = len(self.cursor.execute("SELECT * FROM Orders").fetchall())
            self.cursor.execute("INSERT INTO Orders VALUES(?,?,?,?);",(ID+1, user_id, None, None))

    def get_params(self, sum, key, user_id):
        with self.connection:
            self.cursor.execute("UPDATE Orders SET sum = ?, key = ? WHERE user_id = ?", (sum, key, user_id))


    def chek_order(self, user_id):
        with self.connection:
            order_info = self.cursor.execute("SELECT * FROM Orders WHERE user_id=?", (user_id,)).fetchone()[-1]
            print(order_info)
            if order_info == None:
                return True
            else:
                return False

    def get_order(self, user_id):
        with self.connection:
            info = self.cursor.execute("SELECT * FROM Orders WHERE user_id = ?", (user_id,)).fetchone()
            print(info)
            sum = info[2]
            key = info[-1]
            return sum, key

class Members:

    def __init__(self, database_file):
        self.connection = sqlite3.connect(database_file, timeout=10)
        self.cursor = self.connection.cursor()


    def chek_registration(self, user_id):
        with self.connection:
            if self.cursor.execute("SELECT * FROM `Members` WHERE `user_id` = ?;", (user_id,)).fetchall():
                return True
            else:
                return False


    def registration(self, message):
        with self.connection:
            id = len(self.cursor.execute("SELECT * FROM Members;").fetchall())
            user_id = message.from_user.id
            user_name = message.from_user.username
            first_name = message.from_user.first_name
            if message.text == 'Пропустить🔜':
                phone_number = None
            else:
                phone_number = message.text
            return self.cursor.execute(f"INSERT INTO Members VALUES (?, ?, ?, ?, ?)", (id+1, user_id, first_name, user_name, phone_number))
            #Basket.create_basket(message.from_user.id)

    def edit_phone_number(self, phone_number, user_id):
        with self.connection:
            id = len(self.cursor.execute("SELECT * FROM Members;").fetchall())
            self.cursor.execute(f"UPDATE `Members` SET `phone_number` = ? WHERE user_id = ?", (phone_number, user_id))



    def get_profile(self, user_id):
        with self.connection:
            return self.cursor.execute("SELECT * FROM `Members` WHERE `user_id` = ?;", (user_id,)).fetchall()


    def get_members(self):
        with self.connection:
            return self.cursor.execute("SELECT * FROM `Members`").fetchall()

class Product:

    def __init__(self, database_file):
        self.connection = sqlite3.connect(database_file, timeout=10)
        self.cursor = self.connection.cursor()

    def add_product(self, product_name, product_price, product_count):
        with self.connection:
            print('ddd'+product_name, product_price, product_count)
            ID = self.cursor.execute("SELECT id FROM Product;").fetchall()
            if len(ID) == 0:
                ID = 0
            else:
                ID = list(max(ID))[0]


            return self.cursor.execute(f"INSERT INTO Product VALUES (?, ?, ?, ?)",
                                       (ID + 1, product_name, product_price, product_count))


    def show_products(self):
        with self.connection:
            return self.cursor.execute("SELECT * FROM `Product`").fetchall()


    def del_product(self, id, count):
        with self.connection:
            if count.isdigit():
                print('=====')
                self.cursor.execute(f"UPDATE `Product` SET `count` = `count`- ? WHERE id = ?", (count, id))
            elif count == 'all':
                print('all')
                # self.cursor.execute(f"UPDATE `Product` SET `count` = 0 WHERE id = ?", (id))
                self.cursor.execute(f"DELETE FROM `Product` WHERE id = ?", (id,))

class Basket:

    def __init__(self, database_file):
        self.connection = sqlite3.connect(database_file, timeout=10)
        self.cursor = self.connection.cursor()

    def create_basket(self, user_id):
        with self.connection:
            id = len(self.cursor.execute("SELECT * FROM Basket;").fetchall())
            return self.cursor.execute(f"INSERT INTO Basket VALUES (?, ?, ?, ?)",
                                       (id + 1, user_id, '0', 0))

    def add_in_basket(self, user_id, product_price, product_name):
        with self.connection:
            basket_text = self.cursor.execute("SELECT `basket` FROM `Basket` WHERE user_id = ?;", (user_id, )).fetchone()[0]
            basket_text = str(basket_text) + '\n'+product_name
            self.cursor.execute(f"UPDATE `Basket` SET `price` = `price`+ ? WHERE user_id = ?", (float(product_price), user_id))
            self.cursor.execute(f"UPDATE `Basket` SET `basket` =  ? WHERE user_id = ?", (basket_text, user_id))

    def get_basket(self, user_id):
        with self.connection:
            return self.cursor.execute("SELECT * FROM basket WHERE user_id = ?", (user_id, )).fetchone()

    def clear_basket(self, user_id):
        with self.connection:
            return self.cursor.execute("UPDATE Basket SET `basket` = ?, `price` = ? WHERE user_id = ?", ('0', 0, user_id))