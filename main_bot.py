import config
import requests
from SQLiter import Members, Product, Basket, Orders, Keys
from aiogram import Bot, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.dispatcher import Dispatcher, FSMContext
from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils import executor
from utils import States

ADMIN = config.MAIN_ADMIN
print(ADMIN)
bot = Bot(config.TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())
dp.middleware.setup(LoggingMiddleware())

#########
Members = Members('main.db')
Product = Product('main.db')
Basket = Basket('main.db')
Orders = Orders('main.db')
Keys = Keys('main.db')
author = 1871078732
#########

@dp.message_handler(commands=['start'])
async def start(message: types.Message):

    if Members.chek_registration(message.from_user.id) == False:
        if await enter_state(message, 3) == True:

            await enter_state(message, 1)
    else:
        await main_menu(message)


@dp.message_handler(commands='info')
async def info(message):
    text = '*Boshki 💜Neon💜 -* Сочный микс арбуза и ежевики, украшенный хвойной веточкой.\n➖➖➖\n' \
           '*Boshki 🥥Exotic🥥 -* Коктейль из австралийского манго с мякотью африканской дыни в сочетании с сибирской хвоей.\n➖➖➖\n' \
           '*Boshki 🍎Садовые🍐 -* Вкус сочной клубники в хвойном лесу твоего деда.\n➖➖➖\n' \
           '*Boshki Добрые on ice 🧊 -* Любимый вкус хвойного щербета в глубокой заморозке\n➖➖➖\n' \
           '*Boshki ❤Злые❤️-* Микс от VoodooLab со вкусом хвои, лимонада и смородины. ... Вкус лимонада доминирует на протяжении всей затяжки и напоминает о себе ощущением лимонной свежести на послевкусии.\n➖➖➖\n' \
           '*Boshki 🔅original🔅 -* Что-то похожее на кофейные зерна, небольшая доля сладости, букет лесных ароматов.\n➖➖➖\n' \
           '*Boshki 🌿Целебные🌿 -* Со вкусом травяного чая с мёдом, настоянного на еловых верхушках.\n➖➖➖\n' \
           '*Boshki 👾Добрые🤍 -* Что-то вкусное\n' \

    await message.answer(text=text, parse_mode='Markdown')


@dp.message_handler(commands=['admin'])
async def admin(message: types.Message):
    if await chek_admin(message):
        await admin_panel(message)
    else:
        pass

@dp.message_handler(commands=['add'])
async def add_product(message: types.Message):
    if await chek_admin(message):
        print('a')
        if len(message.text.split()) >= 4:
            product_info = message.text.split()
            product_name = ' '.join(product_info[1:-2])
            product_price = float(product_info[-2])
            product_count = int(product_info[-1])
            print(product_name, product_price, product_count)
            Product.add_product(product_name, product_price, product_count)

            await bot.send_message(message.chat.id, '*Товар успешно добавлен*', parse_mode='Markdown')


@dp.message_handler(commands=['del'])
async def delete_product(message: types.Message):
    print(message.text.split())
    if await chek_admin(message):
        if len(message.text.split()) == 3:
            del_info = message.text.split()

            id = del_info[1]
            if del_info[-1].isdigit():
                count = del_info[-1]
            elif del_info[-1] == 'all':
                count = 'all'
            Product.del_product(id, count)
            await bot.send_message(message.chat.id, 'Товар изменён')


@dp.message_handler(commands=['mailing'])
async def mailing(message: types.Message):
    if await chek_admin(message):
        if len(message.text.split()) >= 2:
            erors = 0
            secc = 0
            for user in Members.get_members():
                try:
                    await bot.send_message(user[1], ' '.join(message.text.split()[1:]), parse_mode='Markdown')
                    secc+=1
                except:
                   erors+=1
            await bot.send_message(author, f'Успешно: {secc}\nОшибки: {erors}')


@dp.message_handler(commands=['newcode'])
async def new_code(message: types.Message):
    if await chek_admin(message):
        if len(message.text.split()) == 2:
            try:
                config.CODE = ''.join(message.text.split()[1:])
                await message.answer('Код изменён')
            except:
                await message.answer('Ошибка')




async def show_products(message: types.Message):
    if await chek_admin(message):
        products_info = Product.show_products()
        text = []
        try:
            for product in products_info:
                t = []
                for i in range(0, len(product)):
                    if i == 0:
                        t.append(f'*[{product[0]}]*')
                    elif i == 1:
                        t.append(f'   _Наименование:_ *{product[i]}*')
                    elif i == 2:
                        t.append(f' 💲_Цена_: *{product[i]}р*')
                    elif i == 3:
                        t.append(f' _Кол-во:_ *{product[i]}*')

                text.append(' '.join(t) + '\n\n')
            await bot.send_message(message.chat.id, ' '.join(text), parse_mode='Markdown')
        except:
            await  bot.send_message(message.chat.id, 'Товаров нет')


@dp.message_handler()
async def echo_message(message: types.Message):
    msg = message.text
    print(msg, message.from_user.id)
    if msg == 'Профиль 👤':
        await get_profile(message=message)

    if msg == 'Поддержка 🗣':
        await bot.send_message(message.chat.id, '*По всем вопросам: @bad_drip_support*', parse_mode='Markdown')

    if msg == 'Корзина 🛒':
        await get_basket(message)
    ###############
    # SHOP#
    if msg == 'Магазин 🏬':
        await shop_menu(message)
    if msg == '💧 Жидкости':
        await all_zizha(message)
    elif msg == '📏 Одноразки':
        await message.answer('*Скоро*', parse_mode='Markdown')
    ###############
    # SHOP#
    if msg == '🔙':
        await main_menu(message)

    #########################
    # ADMIN#
    #########################

    if msg == '📦 Товары' and await chek_admin(message):
        await show_products(message)

    if msg == '🤖 Команды' and await chek_admin(message):
        await bot.send_message(message.chat.id, '_/add <Наиминование товара> <Цена> <Кол-во> -_ *добавляет товар*\n\n'
                                                '_/del <Номер товара> <кол-во> -_ *удаляет товар*(all-всё)\n\n'
                                                '/mailing <Текст> - рассылка\n\n'
                                                '/newcode <Код> - добавление нового ключа для входа',
                               parse_mode='Markdown')

    if msg == '📊 Статистика' and await chek_admin(message):
        print(Product.show_products())
        await bot.send_message(message.chat.id, f'*👤 Всего пользователей: {len(Members.get_members())}*\n\n'
                                                f'*📦 Всего товаров: {len(Product.show_products())}*',
                               parse_mode='Markdown')
    #########################
    # ADMIN#
    #########################


async def enter_state(message, arg):
    if arg == 1:
        mrk = types.ReplyKeyboardMarkup(resize_keyboard=True).add('Пропустить🔜')
        await bot.send_message(message.chat.id,
                               '*Введите ваш номер телефона, это понадобится для доставки*\n_Пример: +375445642275_',
                               parse_mode='Markdown', reply_markup=mrk)
        await States.S1.set()
    elif arg == 2:
        mrk = types.ReplyKeyboardMarkup(resize_keyboard=True).add('Отмена')

        await bot.send_message(message.chat.id, '*Введите номер телефона*\n_Пример: +375445642275_',
                               parse_mode='Markdown', reply_markup=mrk)
        await States.S2.set()
    elif arg == 3:
        await bot.send_message(message.chat.id, '*Введите ключ*',
                               parse_mode='Markdown')
        await States.S3.set()


@dp.message_handler(state=States.S3)
async def get_code(message: types.Message, state: FSMContext):
    if message.text == config.CODE:
        await enter_state(message, 1)
    else:
        await state.reset_state(with_data=True)
        await message.answer('*Неверный код*', parse_mode='Markdown')
        return False


@dp.message_handler(state=States.S1)
async def get_number(message: types.Message, state: FSMContext):
    answer = message.text
    if answer == 'Пропустить🔜':
        Members.registration(message)
        Basket.create_basket(message.from_user.id)
        Orders.registration(message.from_user.id)
        await state.update_data(answer1=answer)
        await state.reset_state(with_data=True)
        await main_menu(message)
    elif answer.startswith('+375'):
        if len(answer) == 13:
            Members.registration(message)
            Basket.create_basket(message.from_user.id)
            Orders.registration(message.from_user.id)
            await state.update_data(answer1=answer)
            await state.reset_state(with_data=True)
            await message.answer('*Номер успешно добавлен*', parse_mode='Markdown')

            await main_menu(message)
        else:
            await bot.send_message(message.chat.id, '*Не коректный номер*', parse_mode='Markdown')
    else:
        await bot.send_message(message.chat.id, '*Отправьте номер по примеру*', parse_mode='Markdown')


@dp.message_handler(state=States.S2)
async def edit_phone_number(message: types.Message, state: FSMContext):
    phone = message.text

    if phone == 'Отмена':
        await state.reset_state(with_data=True)
        await main_menu(message)
    else:

        if phone.startswith('+375'):
            if len(phone) == 13:

                Members.edit_phone_number(phone, message.from_user.id)
                await state.reset_state(with_data=True)
                await main_menu(message)
            else:
                await bot.send_message(message.chat.id, '*Не коректный номер*', parse_mode='Markdown')
        else:
            await bot.send_message(message.chat.id, '*Отправьте номер по примеру*', parse_mode='Markdown')





async def main_menu(message):
    mrp = types.ReplyKeyboardMarkup(resize_keyboard=True)
    basket = 'Корзина 🛒'
    profile = 'Профиль 👤'
    shop = 'Магазин 🏬'
    support = 'Поддержка 🗣'
    mrp.add(shop).add(basket).add(profile, support)

    await bot.send_message(message.chat.id, 'Главное меню', parse_mode='Markdown', reply_markup=mrp)


async def get_profile(message):
    print(message.text)
    print(Members.get_profile(message.from_user.id))
    user_info = Members.get_profile(message.from_user.id)[0]
    ID = user_info[1]
    user_name = user_info[3]
    phone_number = user_info[-1]

    mrk = types.InlineKeyboardMarkup()
    if phone_number:
        mrk.add(types.InlineKeyboardButton(text='Редактировать номер', callback_data='edit_phone_number'))
        await bot.send_message(message.chat.id,
                               f'*👤Профиль\n\n🔅 Имя профиля: {user_name}\n\n🆔 Ваш ID: {ID}\n\n📞 Номер телефона: +{phone_number}\n\nКод для регистрации: {config.CODE}*',
                               reply_markup=mrk, parse_mode='Markdown')

    else:
        mrk.add(types.InlineKeyboardButton(text='Ввести номер телефона', callback_data='enter_phone_number'))
        await bot.send_message(message.chat.id, f'*👤Профиль\n\n🔅 Имя профиля: {user_name}\n\n🆔 Ваш ID: {ID}\n\nКод для регистрации: {config.CODE}*',
                               reply_markup=mrk, parse_mode='Markdown')


async def shop_menu(message):
    mrk = types.ReplyKeyboardMarkup(resize_keyboard=True)
    mrk.add('💧 Жидкости', '📏 Одноразки').add('🔙')
    await bot.send_message(message.chat.id, 'Выберите категорию', parse_mode='Markdown', reply_markup=mrk)


async def get_basket(message):
    mrk = types.InlineKeyboardMarkup()
    clear = types.InlineKeyboardButton('Очистить корзину', callback_data='clear_basket')
    buy = types.InlineKeyboardButton('Купить', callback_data='buy_basket')
    mrk.add(clear).add(buy)

    user_id = message.from_user.id
    basket_info = Basket.get_basket(user_id)
    print(basket_info)
    if basket_info[2] == 0:
        await message.answer('*😳 Здесь пусто!*', parse_mode='Markdown')
    else:
        text = basket_info[2][1:]
        price = basket_info[-1]
        await message.answer(f'*🛒 Корзина\n\nТовары:\n{text}\n\nИтоговая стоимость: {price}р*', parse_mode='Markdown',
                             reply_markup=mrk)


async def all_zizha(message):
    mrk = types.InlineKeyboardMarkup()
    product_info = Product.show_products()
    for product in product_info:
        product_name = product[1]
        product_price = product[2]
        btn = types.InlineKeyboardButton(text=product_name + ' - ' + str(product_price) + 'р',
                                         callback_data=f'| {product_name} {product_price}')
        mrk.add(btn)

    await bot.send_message(message.chat.id, '*Жидкости*', parse_mode='Markdown', reply_markup=mrk)
    await main_menu(message)


@dp.callback_query_handler()
async def process_callback_kb1btn1(call: types.CallbackQuery):
    print(call.data)


    if call.data.startswith('|'):
        product_info = call.data.split()
        product_name = product_info[1]
        product_price = float(product_info[-1])
        Basket.add_in_basket(call.message.chat.id, product_price,
                             f"{' '.join(call.data.split()[1:-1])} - {product_price}р")

        await bot.answer_callback_query(call.id, f"{' '.join(call.data.split()[1:-1])} добавленно в корзину")

    if call.data == 'edit_phone_number':
        await enter_state(message=call.message, arg=2)
    elif call.data == 'enter_phone_number':
        await enter_state(message=call.message, arg=2)

    if call.data == 'clear_basket':
        Basket.clear_basket(call.message.chat.id)
        await call.message.edit_text('*Корзина очищена*', parse_mode='Markdown')
    elif call.data == 'buy_basket':

        chek_order = Orders.chek_order(call.message.chat.id)
        if chek_order == True:
            mrk = types.InlineKeyboardMarkup()
            card = types.InlineKeyboardButton('💳', callback_data='card_pay')
            money = types.InlineKeyboardButton('💴', callback_data='money_pay')
            mrk.add(card, money)
            await call.message.answer('*Выберите способ оплаты*', parse_mode='Markdown', reply_markup=mrk)

        else:
            mrk = types.InlineKeyboardMarkup()
            delet_order = types.InlineKeyboardButton(text='🗑 Удалить заказ', callback_data='delete_order')
            mrk.add(delet_order)
            await call.message.answer('*У вас уже есть заказ\nЖелаете его удалить ?*', parse_mode='Markdown',
                                      reply_markup=mrk)

    if call.data == 'card_pay':
        price = Basket.get_basket(call.message.chat.id)[-1]

        if price != 0:
            mrk = types.InlineKeyboardMarkup()
            pay = types.InlineKeyboardButton('Оплатить', url=await get_order(price, Keys.get_key()))
            chek_pay = types.InlineKeyboardButton('Проверить платёжь 🔄', callback_data='chek_pay')
            mrk.add(pay).add(chek_pay)
            key = Keys.get_key()
            print(key)
            Orders.get_params(price, key, call.message.chat.id)
            await call.message.answer(f'*💳 Оплата заказа\n\n💰 Сумма к оплате: {price}р\n\nВНИМАНИЕ В КОММЕНТАРИЙ К ПЕРЕВОДУ УКАЖИТЕ {key}\nИначе ваш платёж не будет замечен*', parse_mode='Markdown',
                                      reply_markup=mrk)
            await call.message.answer(key)
        else:
            await call.message.answer('*Ваша корзина пуста*', parse_mode='Markdown')

    elif call.data == 'money_pay':
        price = Basket.get_basket(call.message.chat.id)[-1]

        if price != 0:
            user = Members.get_profile(call.message.chat.id)[0]
            print(user)
            phone = user[-1]
            user_name =  user[3]
            if user_name:
                user_name = '@' + user_name

            else:
                user_name = user_name

            first_name = user[2]
            key = Keys.get_key()
            print(key)
            Orders.get_params(price, key, call.message.chat.id)
            await send_author(call.message.chat.id, user_name, first_name, phone)
            await call.message.answer('*✅ Ваша заявка отправлена, ожидайте, в ближайшее время с вами свяжутся*', parse_mode='Markdown')
        else:
            await call.message.answer('*❌ Ваша корзина пуста*', parse_mode='Markdown')




    if call.data == 'delete_order':
        try:
            Orders.get_params(None, None, call.message.chat.id)
            await call.message.answer('*🗑 Заказ удалён*', parse_mode='Markdown')
        except:
            pass

    if call.data == 'chek_pay':
        info = Orders.get_order(call.message.chat.id)
        print(info)
        if await chekk_pay(call.message, info[-1], info[0]) == False:
            await call.message.answer('*❌ Платёжь не найден*', parse_mode='Markdown')
        else:
            await   call.message.answer('*✅ Ваш платёжь успешно обработан*\n_В ближайшие 10 минут с вами свяжутся_',
                                   parse_mode='Markdown')
            user = Members.get_profile(call.message.chat.id)[0]
            print(user)
            phone = user[-1]
            user_name = '@' + user[3]
            first_name = user[2]
            await send_author(call.message.chat.id, user_name, first_name, phone)


async def get_order(price, user_id):
    print(price)
    print(config.KURS)
    print(price*config.KURS)
    print(round(price*config.KURS))
    url = f'https://qiwi.com/payment/form/99999?extra[%27accountType%27]=nickname&extra[%27account%27]=BADDRIPSHOP&amountInteger={round(price * config.KURS)}&amountFraction=0&extra%5B[%27comment%27]%5D={user_id}&currency=643'
    # url1 = f'https://qiwi.com/payment/form/99?extra%5B%27account%27%5D={config.QIWI_PHONE}&amountInteger={price}&amountFraction=0&extra%5B%27comment%27%5D={user_id}&currency=643'

    return url


async def chekk_pay(message, key, price):
    api_access_token = 'a518ca1e92e50254089820a1f136f888'
    s = requests.Session()
    s.headers['authorization'] = 'Bearer ' + api_access_token
    parameters = {'rows': 10}
    h = s.get(f'https://edge.qiwi.com/payment-history/v2/persons/{config.QIWI_PHONE}/payments', params=parameters)

    k = {}

    for i in range(0, len(h.json()['data'])):
        sum = h.json()['data'][i]['sum']['amount']
        comment = h.json()['data'][i]['comment']
        k[comment] = sum
    print(k)
    for o in k.keys():
        print(o, key)
        if o == key:
            print(round(price * config.KURS))
            if k[o] == round(price * config.KURS):
                print(price*config.KURS)
                return True
            break
    await bot.send_message(message.chat.id, 'Карта')
    return False

######################################################
######################################################
######################################################
async def chek_admin(message):
    if message.from_user.id in ADMIN:
        print('f')
        return True
    else:
        return False


async def admin_panel(message):
    mrk = types.ReplyKeyboardMarkup(resize_keyboard=True)

    statistics = '📊 Статистика'
    product = '📦 Товары'
    commands = '🤖 Команды'

    back = '🔙'

    mrk.add(statistics).add(product).add(commands).add(back)

    await bot.send_message(message.chat.id, 'Админка', reply_markup=mrk)

async def send_author(basket_id, user_name, firstname, phone):
    info = Basket.get_basket(basket_id)
    text = f'*➖➖➖➖\n➖Заказ➖\n➖➖➖➖\n\nСодержание:\n{info[2][1:]}\n\nСумма к оплате: {info[3]}\n\nИмя профиля: {user_name}\nИмя пользователя: {firstname}\nНомер телефона: {phone}*'
    await bot.send_message(author, text=text, parse_mode='Markdown')


######################################################
######################################################
######################################################


async def shutdown(dispatcher: Dispatcher):
    await dispatcher.storage.close()
    await dispatcher.storage.wait_closed()


if __name__ == '__main__':
    executor.start_polling(dp, on_shutdown=shutdown)
