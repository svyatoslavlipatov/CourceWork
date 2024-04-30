import random
import telebot
import webbrowser
import json
from telebot import types

# Считывание токена телеграм бота
file = open('./token.txt')
mytoken = file.read()
# Передача токена
bot = telebot.TeleBot(mytoken)

current_section = None

# Ответы пользователю, если введено что-то непонятное для бота
answers = ['Я не понял, что ты хочешь сказать.',
           'Извини, я тебя не понимаю.',
           'Я не знаю такой команды.',
           'Увы, я не знаю, что отвечать в такой ситуации... >_<'
           ]

# ------- Кнопки -------
start_btns = {
    'catalog': '🛍 Каталог',
    'about': '🛈 О нас',
    'faqs': '📄 Частые вопросы'
}

about_btns = {
    'number': '📞 Номер телефона',
    'address': '🗺️ Адрес'
}

faq_btns = {
    'Являются ли оружием товары?':  'Cогласно Федеральному закону <i>"Об оружии" от 13.12.1996 N 150-ФЗ.</i>  товары в нашем магазине <b>НЕ ЯВЛЯЮТСЯ ОРУЖИЕМ!</b> '
                                    'Airsoft - пневматика, с дульной энергией менее 3Дж, использует только пластиковые шары - 6мм.',
    'Почему наши клиенты лучшие?': 'Потому что они крутые!'
}

back_btns = {
    'back': '↩️ Назад',
    'back_catalog': '↩️ В каталог',
    'back_home': '↩️ Вернуться в меню'
}

buy_btns = {
    'buy': 'Купить',
    'cart': '🛒 Корзина',
    'add_to_cart': '🛒 Добавить в корзину'
}


# Категории товаров
goods_btns = {
    'drives': 'Привода',
    'sights': 'Прицелы',
    'girboxes': 'Гирбоксы',
    'gas': 'Газ',
    'launchers': 'Пусковые устройства',
    'gears': 'Шестерни',
    'hopup_nodes':'Узлы хоп-ап'
}

# ------- Закрытие кнопки -------

# Функция для генерации случайного ответа
def random_answer(message):
    bot.send_message(message.chat.id, answers[random.randint(0, 3)])

# Функция для удобного создания кнопок
def create_markup(buttons):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for row in buttons:
        markup.row(*row)
    return markup

# Создание кнопок для товара
def create_buttons_for_product():
    return [
        [buy_btns['add_to_cart']],
        [buy_btns['cart']],
        [back_btns['back'], back_btns['back_catalog']],
        [back_btns['back_home']]
    ]

# Добавление кнопок в ряд
def add_buttons_to_markup(button_dict, max_buttons_per_row):
    buttons = []
    row = []
    for btn_key, btn_text in button_dict.items():
        row.append(btn_text)
        if len(row) == max_buttons_per_row:
            buttons.append(row)
            row = []
    if row:
        buttons.append(row)
    return buttons

# ------- Создание товара -------

# Привода
def create_drive(name, pic, price, brand, gearbox_version, weight, overall_length, folded_length, inner_barrel_length, initial_velocity, caliber, completeness):
    return {
        "название": name,
        "изображение": pic,
        "цена": price,
        "бренд": brand,
        "версия гирбокса": gearbox_version,
        "вес": weight,
        "длина общая": overall_length,
        "длина со сложенным прикладом": folded_length,
        "длина внутреннего стволика": inner_barrel_length,
        "начальная скорость 0,2 шаром": initial_velocity,
        "калибр": caliber,
        "комплектность": completeness
    }

# Прицелы
def create_sight(name, pic, price, brand, description):
    return {
        "название": name,
        "изображение": pic,
        "цена": price,
        "бренд": brand,
        "описание": description
    }

# Газ
def create_gas(name, pic, price, brand, volume):
    return {
        "название": name,
        "изображение": pic,
        "цена": price,
        "бренд": brand,
        "объём": volume
    }

# Гирбоксы
def create_girbox(name, pic, price, brand, material, description):
    return {
        "название": name,
        "изображение": pic,
        "цена": price,
        "бренд": brand,
        "материал": material,
        "описание": description
    }

# Пусковые устройства
def create_launcher(name, pic, price, brand, material, description):
    return {
        "название": name,
        "изображение": pic,
        "цена": price,
        "бренд": brand,
        "материал": material,
        "описание": description
    }

# Хоп-апы
def create_hopup_node(name, pic, price, brand, material, description):
    return {
        "название": name,
        "изображение": pic,
        "цена": price,
        "бренд": brand,
        "материал": material,
        "описание": description
    }

# Шестерни
def create_gear(name, pic, price, brand, material, description):
    return {
        "название": name,
        "изображение": pic,
        "цена": price,
        "бренд": brand,
        "материал": material,
        "описание": description
    }

# ------- Закрытие создание товара -------


# ------- Загрузка из JSON -------

# Загрузка данных о приводах из JSON файлов
def load_products_from_file(file_path, create_function):
    with open(file_path, 'r', encoding='utf-8') as file:
        products_data = json.load(file)
    return [create_function(**product) for product in products_data]

drives_list = load_products_from_file('catalog/drives/drives_data.json', create_drive)
sights_list = load_products_from_file('catalog/sights/sights_data.json', create_sight)
gas_list = load_products_from_file('catalog/gas/gas_data.json', create_gas)
girboxes_list = load_products_from_file('catalog/girboxes/girboxes_data.json', create_girbox)
launchers_list = load_products_from_file('catalog/launchers/launchers_data.json', create_launcher)
hopup_nodes_list = load_products_from_file('catalog/hopup_nodes/hopup_nodes_data.json', create_hopup_node)
gears_list = load_products_from_file('catalog/gears/gears_data.json', create_gear)
# ------- Закрытие загрузка из JSON -------


# Команда /start
@bot.message_handler(commands=['start'])
def welcome(message):
    # Кнопки после /start
    buttons = [
        [start_btns['catalog']],
        [buy_btns['cart']],
        [start_btns['about'], start_btns['faqs']],
    ]
    markup = create_markup(buttons)

    if message.text == '/start':
        # Отправляю приветственный текст
        bot.send_message(message.chat.id, f'Привет, {message.from_user.first_name}!\n В нашей мастерской "FRW - Fire Rabbit Workshop" ты можешь приобрести качественное снаряжение и экипировку для страйкбола!\n ВК моего владельца: https://vk.com/petrucho_t', reply_markup=markup)
    else:
        bot.send_message(message.chat.id, 'Вернули тебя в главное меню!', reply_markup=markup)

# Обработка фото и стикеров
@bot.message_handler(content_types=['photo', 'sticker', 'audio'])
def get_photo(message):
    bot.send_message(message.chat.id, 'Извини, я не могу обрабатывать фото, стикеры и голосовые :(')


# Переменная для хранения информации о последнем показанном товаре
last_displayed_products = {}

# Словарь для хранения корзин для каждого пользователя
carts = {}

# Обработчик для кнопки "Добавить в корзину"
@bot.message_handler(func=lambda message: message.text == buy_btns.get('add_to_cart'))
def inquire_about_product(message):
    user_id = message.chat.id
    if user_id in last_displayed_products:
        selected_product = last_displayed_products[user_id]
        if user_id not in carts:
            carts[user_id] = []  # Если корзины пользователя еще нет, создаем пустую корзину
        cart_item = {"название": selected_product["название"], "цена": selected_product["цена"]}
        carts[user_id].append(cart_item)  # Добавляем товар в корзину
        bot.send_message(message.chat.id, f'Товар "{selected_product["название"]}" добавлен в корзину.')
        print(carts)
    else:
        bot.send_message(message.chat.id, "Не удалось добавить товар в корзину. Попробуйте заново.")

# Обработчик для кнопки "Корзина"
@bot.message_handler(func=lambda message: message.text == '🛒 Корзина')
def show_cart(message):
    buttons = [
        [buy_btns['buy']],
        [back_btns['back_home']]
    ]
    markup = create_markup(buttons)
    user_id = message.chat.id
    if user_id in carts:
        cart_items = carts[user_id]
        if cart_items:
            response = "Ваша корзина:\n"
            for i, item in enumerate(cart_items, start=1):
                response += f'{i}. Название: {item["название"]}, Цена: {item["цена"]}\n'
            response += "\nЧтобы удалить товар из корзины, отправьте его номер."
            bot.send_message(message.chat.id, response, reply_markup=markup)
        else:
            bot.send_message(message.chat.id, "Ваша корзина пуста.",  reply_markup=markup)
    else:
        bot.send_message(message.chat.id, "Ваша корзина пуста.",  reply_markup=markup)

# Обработчик для удаления товара из корзины
@bot.message_handler(func=lambda message: message.text.isdigit() and int(message.text) > 0 and message.chat.id in carts)
def remove_item_from_cart(message):
    user_id = message.chat.id
    item_number = int(message.text)
    cart_items = carts[user_id]
    if 1 <= item_number <= len(cart_items):
        removed_item = cart_items.pop(item_number - 1)
        bot.send_message(message.chat.id, f'Товар "{removed_item["название"]}" удален из корзины.')
        show_cart(message)  # Показываем обновленное содержимое корзины
    else:
        bot.send_message(message.chat.id, "Неверный номер товара.")


# Обработчик для кнопки "Купить"
@bot.message_handler(func=lambda message: message.text == buy_btns['buy'])
def buy_product(message):
    user_id = message.chat.id
    if user_id in carts:
        cart_items = carts[user_id]
        if cart_items:
            response = "Ваша корзина:\n"
            cart_text = ""
            for i, item in enumerate(cart_items, start=1):
                cart_text += f'{i}. Товар: {item["название"]}, Цена: {item["цена"]}\n'
            response += f'<code>{cart_text}</code>'
            response += "\nДля покупки скопируйте содержимое корзины (нажмите на название товара и все содержимое скопируется) и свяжитесь с нами по ссылке: <a href='https://t.me/liipkka'>Написать в Telegram</a>"
            bot.send_message(message.chat.id, response, parse_mode='HTML')
        else:
            bot.send_message(message.chat.id, "Ваша корзина пуста.")
    else:
        bot.send_message(message.chat.id, "Ваша корзина пуста.")



# ------- Обработка нажатия на товар  -------
# Приводы
@bot.message_handler(func=lambda message: message.text in [drive["название"] for drive in drives_list])
def handle_drive_selection(message):
    selected = next(drive for drive in drives_list if drive["название"] == message.text)
    last_displayed_products[message.chat.id] = selected
    photo = open(selected["изображение"], 'rb')  # Открываем файл изображения
    caption = f''' Название: {selected["название"]}
Цена: {selected["цена"]}
Бренд: {selected["бренд"]}
Версия гирбокса: {selected["версия гирбокса"]}
Вес: {selected["вес"]}
Длина общая: {selected["длина общая"]}
Длина со сложенным прикладом: {selected["длина со сложенным прикладом"]}
Длина внутреннего стволика: {selected["длина внутреннего стволика"]}
Начальная скорость 0,2 шаром: {selected["начальная скорость 0,2 шаром"]}
Калибр: {selected["калибр"]}
Комплектность: {selected["комплектность"]}

НЕ ЯВЛЯЕТСЯ ОРУЖИЕМ!
Согласно Федеральному закону "Об оружии" от 13.12.1996 N 150-ФЗ. Airsoft - пневматика, с дульной энергией менее 3Дж, использует только пластиковые шары - 6мм.
'''
    bot.send_photo(message.chat.id, photo, caption=caption)
    photo.close()

    # Создаем кнопки
    buttons = create_buttons_for_product()

    markup = create_markup(buttons)
    bot.send_message(message.chat.id, "Выберите действие:", reply_markup=markup)

# Прицелы
@bot.message_handler(func=lambda message: message.text in [sight["название"] for sight in sights_list])
def handle_sight_selection(message):
    selected = next(sight for sight in sights_list if sight["название"] == message.text)
    last_displayed_products[message.chat.id] = selected
    photo = open(selected["изображение"], 'rb')  # Открываем файл изображения
    caption = f''' Название: {selected["название"]}
Цена: {selected["цена"]}
Бренд: {selected["бренд"]}
Комплектность: {selected["описание"]}
'''
    bot.send_photo(message.chat.id, photo, caption=caption)
    photo.close()

    # Создаем кнопки
    buttons = create_buttons_for_product()

    markup = create_markup(buttons)
    bot.send_message(message.chat.id, "Выберите действие:", reply_markup=markup)


# Газ
@bot.message_handler(func=lambda message: message.text in [gas["название"] for gas in gas_list])
def handle_gas_selection(message):
    selected = next(gas for gas in gas_list if gas["название"] == message.text)
    last_displayed_products[message.chat.id] = selected
    photo = open(selected["изображение"], 'rb')  # Открываем файл изображения
    caption = f''' Название: {selected["название"]}
Цена: {selected["цена"]}
Бренд: {selected["бренд"]}
Комплектность: {selected["объём"]}
'''
    bot.send_photo(message.chat.id, photo, caption=caption)
    photo.close()

    # Создаем кнопки
    buttons = create_buttons_for_product()

    markup = create_markup(buttons)
    bot.send_message(message.chat.id, "Выберите действие:", reply_markup=markup)

def add_easy_selections(message, product, buttons):
    photo = open(product["изображение"], 'rb')  # Открываем файл изображения
    caption = f''' Название: {product["название"]}
Цена: {product["цена"]}
Бренд: {product["бренд"]}
Материал: {product["материал"]}
Описание: {product["описание"]}
'''
    bot.send_photo(message.chat.id, photo, caption=caption)
    photo.close()

    markup = create_markup(buttons)
    bot.send_message(message.chat.id, "Выберите действие:", reply_markup=markup)
def handle_product_selection(message, product_list):
    selected = next((product for product in product_list if product["название"] == message.text), None)
    last_displayed_products[message.chat.id] = selected
    if selected:
        buttons = create_buttons_for_product()
        add_easy_selections(message, selected, buttons)

@bot.message_handler(func=lambda message: message.text in [product["название"] for product in girboxes_list])
def handle_girbox_selection(message):
    handle_product_selection(message, girboxes_list)

@bot.message_handler(func=lambda message: message.text in [product["название"] for product in launchers_list])
def handle_launcher_selection(message):
    handle_product_selection(message, launchers_list)

@bot.message_handler(func=lambda message: message.text in [product["название"] for product in hopup_nodes_list])
def handle_hopup_node_selection(message):
    handle_product_selection(message, hopup_nodes_list)

@bot.message_handler(func=lambda message: message.text in [product["название"] for product in gears_list])
def handle_gear_selection(message):
    handle_product_selection(message, gears_list)

# ------- Конец обработка нажатия на товар  -------

# Обработка обычных текстовых команд, описанных в кнопках
@bot.message_handler(func=lambda message: True)
def info(message):
    if message.text == start_btns.get('catalog'):
        goodsChapter(message)

    elif message.text == start_btns.get('about'):
        aboutUs(message)

    elif message.text == start_btns.get('faqs'):
        faqAnswer(message)

    elif message.text == about_btns.get('number'):
        bot.send_message(message.chat.id,'<b>Номер телефона:</b> 7 (924) 834-88-86', parse_mode='html')

    elif message.text == about_btns.get('address'):
        bot.send_message(message.chat.id,'<b>Адрес:</b> Иркутск, Декабрьских событий, 102', parse_mode='html')

    elif message.text == goods_btns.get('drives'):
        drives_category(message)

    elif message.text == goods_btns.get('sights'):
        sights_category(message)

    elif message.text == goods_btns.get('gas'):
        gas_category(message)

    elif message.text == goods_btns.get('girboxes'):
        girboxes_category(message)

    elif message.text == goods_btns.get('launchers'):
        launchers_category(message)

    elif message.text == goods_btns.get('hopup_nodes'):
        hopup_nodes_category(message)

    elif message.text == goods_btns.get('gears'):
        gears_category(message)

    elif message.text == buy_btns.get('buy'):
        webbrowser.open('')

    # elif message.text == buy_btns.get('add_to_cart'):
    #     bot.send_message(message.chat.id, "Чтобы добавить товар в корзину, выберите его из каталога.")

    elif message.text == back_btns.get('back'):
        if current_section:
            # Если пользователь находится в каком-то разделе каталога, возвращаем его к списку товаров этого раздела
            if current_section == "drives":
                drives_category(message)
            elif current_section == "sights":
                sights_category(message)
            elif current_section == "gas":
                gas_category(message)
            elif current_section == "girboxes":
                girboxes_category(message)
            elif current_section == "launchers":
                launchers_category(message)
            elif current_section == "hopup_nodes":
                hopup_nodes_category(message)
            elif current_section == "gears":
                gears_category(message)
        else:
            goodsChapter(message)

    elif message.text in faq_btns:
        text = f'{faq_btns[message.text]}'
        bot.send_message(message.chat.id, text, parse_mode='html')

    elif message.text == back_btns.get('back_catalog'):
        goodsChapter(message)

    elif message.text == back_btns.get('back_home'):
        welcome(message)

    else:
        random_answer(message)

# ----- Категории каталога ------
def display_category(message, product_list, category_name):
    max_buttons_per_row = 2
    buttons = add_buttons_to_markup({product["название"]: product["название"] for product in product_list}, max_buttons_per_row)
    buttons.append([back_btns['back_catalog'], back_btns['back_home']])
    markup = create_markup(buttons)
    bot.send_message(message.chat.id, f'Раздел {category_name}:', reply_markup=markup)

def set_current_section_and_display_category(message, section_name, product_list, category_name):
    global current_section
    current_section = section_name
    display_category(message, product_list, category_name)

def drives_category(message):
    set_current_section_and_display_category(message, "drives", drives_list, "AIRSOFT приводов (Модели страйкбольного «оружия»)")

def sights_category(message):
    set_current_section_and_display_category(message, "sights", sights_list, "прицелов")

def gas_category(message):
    set_current_section_and_display_category(message, "gas", gas_list, "газа")

def girboxes_category(message):
    set_current_section_and_display_category(message, "girboxes", girboxes_list, "гирбоксов")

def launchers_category(message):
    set_current_section_and_display_category(message, "launchers", launchers_list, "пусковых устройств")

def hopup_nodes_category(message):
    set_current_section_and_display_category(message, "hopup_nodes", hopup_nodes_list, "узлов хоп-апов")

def gears_category(message):
    set_current_section_and_display_category(message, "gears", gears_list, "шестерней")

# ----- Закрытие категории каталога ------

# Функция, отвечающая за раздел товаров
def goodsChapter(message):
    max_buttons_per_row = 3
    buttons = add_buttons_to_markup(goods_btns, max_buttons_per_row)
    buttons.append([back_btns['back_home']])
    markup = create_markup(buttons)
    bot.send_message(message.chat.id, "Каталог товаров:", reply_markup=markup)

# Функция, отвечающая за раздел о нас
def aboutUs(message):
    buttons = [
        [about_btns['number'], about_btns['address']],
        [back_btns['back_home']]
    ]
    markup = create_markup(buttons)
    bot.send_message(message.chat.id, 'Раздел "О нас".\nЗдесь ты можешь узнать информацию о нас.', reply_markup=markup)


# Функция, отвечающая за раздел о нас
def faqAnswer(message):
    buttons = []
    row = []
    for btn_key in faq_btns:
        row.append(btn_key)
        if len(row) == 3:  # Когда в ряду уже три кнопки, добавляем этот ряд и начинаем новый
            buttons.append(row)
            row = []
    if row:  # Добавляем последний неполный ряд, если он есть
        buttons.append(row)
    buttons.append([back_btns['back_home']])  # Добавляем кнопку "Назад на главную"
    markup = create_markup(buttons)
    bot.send_message(message.chat.id, 'Раздел "Вопросы и ответы".\nЗдесь ты можешь найти ответы на часто задаваемые вопросы.', reply_markup=markup)

# Строчка, чтобы программа не останавливалась
bot.polling(none_stop=True)