# -*- coding: utf-8 -*-

from telebot import *
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup
from Text import *
from DataLoader import *
from Email import *
from collections import deque
from threading import Thread
from validate_email import validate_email
from random import randint
from time import sleep
from requests import get

bot = TeleBot(API)

operations = deque()

wait_read = {}

mailing_creation = {}

survey_creation = {}


@bot.message_handler(content_types=["text"])
def any_msg(message):
    print(message.text)

    if message.text == "/start":
        if str(message.chat.id) not in Read(link):
            start_(message)
            operations.append(["creation", str(message.chat.id), {"email": "", "mailing_type": 0, "changes": 0}, link])
        else:
            menu(message)
    else:
        if str(message.chat.id) in wait_read:
            if wait_read[str(message.chat.id)]["operation"] == 1:
                if validate_email(message.text):
                    wait_read[str(message.chat.id)]["operation"] = 2
                    wait_read[str(message.chat.id)]["code"] = str(randint(1000, 9999))
                    wait_read[str(message.chat.id)]["email"] = str(message.text)
                    confirm_email(message.text, wait_read[str(message.chat.id)]["code"])

                    bot.send_message(message.chat.id, "Введите код подтверждения")
                else:
                    keyboard = types.InlineKeyboardMarkup()
                    callback_button = types.InlineKeyboardButton(text="Выбрать другой тип рассылки",
                                                                 callback_data="start")
                    keyboard.add(callback_button)
                    bot.send_message(message.chat.id, "Вы ввели не правельный адрес электронной почты",
                                     reply_markup=keyboard)

            elif wait_read[str(message.chat.id)]["operation"] == 2:
                if wait_read[str(message.chat.id)]["code"] == str(message.text):
                    operations.append(
                        ["change", str(message.chat.id), "email", wait_read[str(message.chat.id)]["email"], link])
                    operations.append(["change", str(message.chat.id), "mailing_type", 2, link])

                    del wait_read[str(message.chat.id)]

                    bot.send_message(message.chat.id, "Вы зарегистрировались")

                    menu(message)

                else:
                    keyboard = types.InlineKeyboardMarkup()
                    callback_button = types.InlineKeyboardButton(text="Ввести другой адрес электронной почты",
                                                                 callback_data="mailing_2")
                    keyboard.add(callback_button)
                    bot.send_message(message.chat.id, "Вы ввели не правельный код, введите его еще раз",
                                     reply_markup=keyboard)

        elif str(message.chat.id) in mailing_creation:
            if mailing_creation[str(message.chat.id)]["type"] == 0:
                if mailing_creation[str(message.chat.id)]["stage"] == 0:
                    mailing_creation[str(message.chat.id)]["stage"] = 1
                    mailing_creation[str(message.chat.id)]["header"] = message.text
                    bot.send_message(message.chat.id, "Введите текст рассылки")
                elif mailing_creation[str(message.chat.id)]["stage"] == 1:
                    mailing_creation[str(message.chat.id)]["text"] = message.text

                    mailing_creation_(message)

            print(mailing_creation[str(message.chat.id)])

        elif str(message.chat.id) in survey_creation:
            if survey_creation[str(message.chat.id)]["type"] == 1:
                if survey_creation[str(message.chat.id)]["stage"] == 0:
                    survey_creation[str(message.chat.id)]["stage"] = 1
                    survey_creation[str(message.chat.id)]["header"] = message.text
                    bot.send_message(message.chat.id, "Введите текст рассылки")
                elif survey_creation[str(message.chat.id)]["stage"] == 1:
                    survey_creation[str(message.chat.id)]["text"] = message.text
                    survey_creation[str(message.chat.id)]["stage"] = 2

                    bot.send_message(message.chat.id, "Введите количество вариантов ответов от 2 до 8")

                elif survey_creation[str(message.chat.id)]["stage"] == 2:
                    try:
                        c = int(message.text)

                        if c > 8 or c < 2:
                            raise

                        survey_creation[str(message.chat.id)]["number"] = c
                        survey_creation[str(message.chat.id)]["stage"] = 3

                        bot.send_message(message.chat.id, f"Введите {c} варианта ответа")
                    except:
                        bot.send_message(message.chat.id, "Введите количество вариантов ответов от 2 до 4")

                else:
                    survey_creation[str(message.chat.id)]["stage"] += 1

                    if survey_creation[str(message.chat.id)]["stage"] - 3 >= survey_creation[str(message.chat.id)][
                        "number"]:
                        survey_creation[str(message.chat.id)]["ans"].append(str(message.text))
                        survey_creation_(message)
                    else:
                        survey_creation[str(message.chat.id)]["ans"].append(str(message.text))

                        bot.send_message(message.chat.id,
                                         f"Введите {survey_creation[str(message.chat.id)]['number'] - (survey_creation[str(message.chat.id)]['stage'] - 3)} варианта ответа")

            print(survey_creation[str(message.chat.id)])

        else:
            menu(message)


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    if call.message:
        print(call.data)
        if call.data[:7] == "mailing":
            temp = call.data.split("_")
            if temp[1] == "0":
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                      text="Сохранено")
            if temp[1] == "1":
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                      text="Сохранено")
                operations.append(["change", str(call.message.chat.id), "mailing_type", 1, link])
            if temp[1] == "2":
                keyboard = types.InlineKeyboardMarkup()
                callback_button = types.InlineKeyboardButton(text="Выбрать другой тип рассылки", callback_data="start")
                keyboard.add(callback_button)

                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                      text="Введите адрес электронной почты", reply_markup=keyboard)
                wait_read[str(call.message.chat.id)] = {"operation": 1, "code": 0, "email": ""}
        elif call.data == "start":
            start_(call.message)

            if str(call.message.chat.id) in wait_read:
                del wait_read[str(call.message.chat.id)]




        elif call.data[:4] == "menu":
            temp = call.data.split("_")

            if temp[1] == "1":
                creation_mailing(call.message)

            elif temp[1] == "2":
                if str(call.message.chat.id) not in mailing_creation:
                    mailing_creation[str(call.message.chat.id)] = {"type": 0, "stage": 0, "number": 0, "header": "",
                                                                   "text": "", "ans": []}
                    start_mailing(call.message)
                else:
                    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                          text="Вы уже создали рассылку, создать новую рассылку, можно после того как обработают старую")

            elif temp[1] == "3":
                if str(call.message.chat.id) not in mailing_creation:
                    survey_creation[str(call.message.chat.id)] = {"type": 1, "stage": 0, "number": 0, "text": "",
                                                                  "header": "",
                                                                  "ans": []}
                    start_mailing(call.message)
                else:
                    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                          text="Вы уже создали рассылку, создать новую рассылку, можно после того как обработают старую")

        elif call.data[:6] == "cancel":

            if str(call.message.chat.id) in mailing_creation:
                del mailing_creation[str(call.message.chat.id)]

                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                      text="Действие отменино")
            else:
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                      text="Действие не действительно")

            menu(call.message)

        elif call.data == "publish":
            for admin_id in Read(admin)["admin"]:
                abmin_view(call.message, admin_id)

            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  text="Вы отправили заявку")

        elif call.data == "dont_publish":
            try:
                del mailing_creation[str(call.message.chat.id)]
            except:
                pass
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  text="Вы не отправили заявку")

        elif call.data[:11] == "MailingSave":
            temp = call.data.split("_")

            if temp[1] in mailing_creation:
                if mailing_creation[temp[1]]["type"] == 0:
                    operations.append(["mailing", temp[1]])
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                      text="Рассылка будет опубликована")
            elif temp[1] in survey_creation:
                if survey_creation[temp[1]]["type"] == 1:
                    operations.append(["survey", temp[1]])
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                      text="Опрос будет опубликован")

        elif call.data[:3] == "ans":
            temp = call.data.split("_")

            c = Read(mailing_)

            str_survey = ""

            for i, ans in enumerate(c[temp[1]]["ans"]):
                str_survey += str(i + 1) + "."

                if temp[2] == str(i):
                    str_survey += "✓"
                    c[temp[1]]['vote'][i] += 1

                str_survey += f"|{c[temp[1]]['vote'][i]}| {ans}\n"

            operations.append(["voice", str(call.message.chat.id), temp[1], temp[2]])

            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  text=f"Опрос №{temp[1]}: {c[temp[1]]['header']}\n{c[temp[1]]['text']}\n\n{str_survey}")

        elif call.data == "info":
            info(call.message)

        elif call.data == "tin_to_tin":
            keyboard = types.InlineKeyboardMarkup()
            callback_button = types.InlineKeyboardButton(text="Назад",
                                                         callback_data="info")
            keyboard.add(callback_button)
            bot.send_message(call.message.chat.id, """Тин to Тин
В раздел Тин to Тин встроен особый магнит, притягивающий таланты! Ты уже здесь? Никто не сомневался! Загляни на Вернисаж, чтобы вдохнуть Вдохновения и выбирай мастер-класс по душе!\n Подробнее на сайте: https://teen.szd.online/khobbi-trone""",
                             reply_markup=keyboard)

        elif call.data == "projd":
            keyboard = types.InlineKeyboardMarkup()
            callback_button = types.InlineKeyboardButton(text="Назад",
                                                         callback_data="info")
            keyboard.add(callback_button)
            bot.send_message(call.message.chat.id, """Фабрика профессий
Здесь создают самое главное ботаство Страны железных дорог - высококлассных специалистов, которые бережно заботятся о ней, стремятся развивать и совершенствовать ее! Здесь можно узнать много нового и необычного о железнодорожных профессиях, о том, какая детская железная дорога находится рядом с местом твоего проживания и даже расширить свои профессиональные горизоны, посетив специальные мастер-классы.\n Подробнее на сайте: https://teen.szd.online/fabrika-professij """,
                             reply_markup=keyboard)

        elif call.data == "labpr":
            keyboard = types.InlineKeyboardMarkup()
            callback_button = types.InlineKeyboardButton(text='Проектная лаборатория "Игротехника"',
                                                         callback_data="game")
            keyboard.add(callback_button)
            callback_button = types.InlineKeyboardButton(
                text='Проектная лаборатория "Аксиома ответственности - Железнодорожники будущего"',
                callback_data="axiom")
            keyboard.add(callback_button)
            callback_button = types.InlineKeyboardButton(text='Проектная лаборатория "Цифровой мир - IT"',
                                                         callback_data="it")
            keyboard.add(callback_button)
            callback_button = types.InlineKeyboardButton(text='Проектная лаборатория "Хайтек"',
                                                         callback_data="hitex")
            keyboard.add(callback_button)
            callback_button = types.InlineKeyboardButton(text='Проектная лаборатория "СММ"',
                                                         callback_data="smm")
            keyboard.add(callback_button)

            callback_button = types.InlineKeyboardButton(text="Назад",
                                                         callback_data="info")
            keyboard.add(callback_button)
            bot.send_message(call.message.chat.id, """Проектные лаборатории\n
Давай знакомиться!
Новые возможности уже близко. Только протяни руку и открой дверь одной из пяти проектных лабораторий. В каждой из них тебя ждет опытный наставник, который поможет реализовать твой потенциал, раскроет новые таланты и поделится своей суперсилой. Ты сможешь разработать собственный крутой проект! Для этого заходи в свой личный кабинет, выбирай проектную лабораторию и выполняй спецзадание от ее руководителя. Желаем удачи!""",
                             reply_markup=keyboard)

        elif call.data == "game":
            keyboard = types.InlineKeyboardMarkup()
            callback_button = types.InlineKeyboardButton(text="Назад",
                                                         callback_data="labpr")
            keyboard.add(callback_button)
            bot.send_message(call.message.chat.id, """Руководитель

Медова Надежда Николаевна

Автор многих профориентационных программ ОАО "РЖД", методист и педагог профильных смен "Страна железных дорог", наставник проектных команд в направлении "Игротехника и геймдизайн".

Создание игры – это интересный процесс и полезный результат. Геймдизайн даёт возможность реализации идеи в реальном прототипе.

Игры являются одним из наиболее эффективных, а главное – увлекательных инструментов в обучении и развитии человека, они позволяют изучить сложное через простые действия.

В проектной лаборатории "Игротехника" мы сможем создать увлекательную игровую реальность, рассказать о железных дорогах интересно и просто.""",
                             reply_markup=keyboard)
        elif call.data == "axiom":
            keyboard = types.InlineKeyboardMarkup()
            callback_button = types.InlineKeyboardButton(text="Назад",
                                                         callback_data="labpr")
            keyboard.add(callback_button)
            bot.send_message(call.message.chat.id, """Руководитель

Петров Иван Сергеевич

Преподаватель Красноярского учебного центра профессиональных квалификаций ОАО "РЖД"

Проектная лаборатория "Аксиома ответственности - железнодорожники будущего" погрузит тебя в мир железнодорожных профессий, техники и технологий.

Ты научишься создавать проекты, направленные на развитие холдинга ОАО "РЖД", на повышение привлекательности компании для клиентов, на улучшение и облегчение труда железнодорожников. А ещё сможешь развить навыки проектирования, анализа и обработки информации, представления и защиты своих разработок.""",
                             reply_markup=keyboard)

        elif call.data == "it":
            keyboard = types.InlineKeyboardMarkup()
            callback_button = types.InlineKeyboardButton(text="Назад",
                                                         callback_data="labpr")
            keyboard.add(callback_button)
            bot.send_message(call.message.chat.id, """Руководитель

Чеканова Елена Амуровна

Инструктор детского технопарка "Кванториум" Свердловской детской железной дороги по направлению IT, эксперт с правом проведения Региональных чемпионатов WorldSkills Russia.

Проектная лаборатория «Цифровой мир - IT» позволит тебе окунуться в мир разработки программных продуктов, почувствовать себя частью команды и определить свое направление деятельности в мире информационных технологий.

Самая главная рекомендация – как можно больше практики. Не бойся воплощать свои идеи, разрабатывать проект за проектом – с каждым шагом твоё мастерство будет расти в геометрической прогрессии.

Вторая рекомендация – мониторить и изучать новые информационные технологии, постоянно искать что-то новое и полезное для себя, анализировать интересующие тебя программные продукты. Чем больше знаний о существующих программных продуктах и навыков разработки программного обеспечения ты имеешь, тем творчески богаче твои разработки.""",
                             reply_markup=keyboard)

        elif call.data == "hitex":
            keyboard = types.InlineKeyboardMarkup()
            callback_button = types.InlineKeyboardButton(text="Назад",
                                                         callback_data="labpr")
            keyboard.add(callback_button)
            bot.send_message(call.message.chat.id, """Руководитель

Соловьев Павел Анатольевич

Инструктор детского технопарка "Кванториум" Свердловской детской железной дороги по направлению "Промышленный дизайн".

Проектная лаборатория "Хайтек" познакомит тебя с удивительным миром будущего: миром 3D-технологий и 3D-моделирования.

Ты научишься создавать предметы в программе трехмерной графики Blender и узнаешь, как создавать развертки 3D-моделей. Мы воссоздадим трехмерную модель в реальной жизни при помощи обычного принтера – и всё это в команде новых друзей и единомышленников. Будет непросто, но зато очень интересно.""",
                             reply_markup=keyboard)

        elif call.data == "smm":
            keyboard = types.InlineKeyboardMarkup()
            callback_button = types.InlineKeyboardButton(text="Назад",
                                                         callback_data="labpr")
            keyboard.add(callback_button)
            bot.send_message(call.message.chat.id, """Руководитель

Лисицкая Екатерина Андреевна

SMM-специалист, маркетолог, опыт более 3 лет.

Социальные сети так плотно вошли в нашу жизнь, что давно перестали быть просто местом для общения с друзьями. Сегодня с их помощью можно продвигать практически любой бизнес и хорошо зарабатывать. Правда, стать успешным в Instagram можно только проделав уйму работы над профилем. Захватить рынок позволит грамотное SMM-продвижение и продуманная стратегия.

В проектной лаборатории "СММ" ты сможешь погрузиться в область SMM и попрактиковаться на реальных примерах. По итогу ты предложишь готовые решения для продвижения аккаунта "РЖД" и вовлечение максимального количества людей.""",
                             reply_markup=keyboard)


        elif call.data == "listMailing":
            temp = Read(mailing_)
            c = list(temp)

            if len(temp) > 10:
                keyboard = types.InlineKeyboardMarkup()
                callback_button = types.InlineKeyboardButton(text="Присылать на электронную почту",
                                                             callback_data="mailing_2")
                keyboard.add(callback_button)
                bot.send_message(call.message.chat.id, start, reply_markup=keyboard)


def start_(message):
    keyboard = types.InlineKeyboardMarkup()
    callback_button = types.InlineKeyboardButton(text="Не рассылать", callback_data="mailing_0")
    keyboard.add(callback_button)
    callback_button = types.InlineKeyboardButton(text="Присылать  в Telegram", callback_data="mailing_1")
    keyboard.add(callback_button)
    callback_button = types.InlineKeyboardButton(text="Присылать на электронную почту", callback_data="mailing_2")
    keyboard.add(callback_button)
    bot.send_message(message.chat.id, start, reply_markup=keyboard)


def menu(message):
    keyboard = types.InlineKeyboardMarkup()
    callback_button = types.InlineKeyboardButton(text="Общая информация", callback_data="info")
    keyboard.add(callback_button)
    callback_button = types.InlineKeyboardButton(text="Рассылка", callback_data="menu_1")
    keyboard.add(callback_button)
    # callback_button = types.InlineKeyboardButton(text="Настройки", callback_data="setting")
    # keyboard.add(callback_button)
    bot.send_message(message.chat.id, menu_, reply_markup=keyboard)


def info(message):
    keyboard = types.InlineKeyboardMarkup()
    # callback_button = types.InlineKeyboardButton(text="Как победить", callback_data="how_win")
    # keyboard.add(callback_button)
    callback_button = types.InlineKeyboardButton(text="Тин to Тин", callback_data="tin_to_tin")
    keyboard.add(callback_button)
    callback_button = types.InlineKeyboardButton(text="PROжд", callback_data="projd")
    keyboard.add(callback_button)
    # callback_button = types.InlineKeyboardButton(text="Новости сообществ", callback_data="labpr")
    # keyboard.add(callback_button)
    callback_button = types.InlineKeyboardButton(text="Проектные лаборатории", callback_data="labpr")
    keyboard.add(callback_button)

    bot.send_message(message.chat.id, "Тин-клуб страны железных дорог", reply_markup=keyboard)


def abmin_view(message, admin_id):
    keyboard = types.InlineKeyboardMarkup()
    callback_button = types.InlineKeyboardButton(text="Опубликовать", callback_data=f"MailingSave_{message.chat.id}")
    keyboard.add(callback_button)
    callback_button = types.InlineKeyboardButton(text="Не публиковать",
                                                 callback_data=f"notmailingSave_{message.chat.id}")
    keyboard.add(callback_button)
    if str(message.chat.id) in mailing_creation:
        bot.send_message(admin_id,
                         f"{mailing_creation[str(message.chat.id)]['header']}\n\n{mailing_creation[str(message.chat.id)]['text']}\n\nОпубликовать?",
                         reply_markup=keyboard)
    else:
        temp = ""

        for i in range(survey_creation[str(message.chat.id)]['number']):
            temp += f"{i + 1}{survey_creation[str(message.chat.id)]['ans'][i]}\n"

        bot.send_message(admin_id,
                         f"{survey_creation[str(message.chat.id)]['header']}\n\n{survey_creation[str(message.chat.id)]['text']}\n\n{temp}\n\nОпубликовать?",
                         reply_markup=keyboard)


def mailing_creation_(message):
    keyboard = types.InlineKeyboardMarkup()
    callback_button = types.InlineKeyboardButton(text="Опубликовать", callback_data="publish")
    keyboard.add(callback_button)
    callback_button = types.InlineKeyboardButton(text="Отмена публикации", callback_data="dont_publish")
    keyboard.add(callback_button)
    bot.send_message(message.chat.id,
                     f"{mailing_creation[str(message.chat.id)]['header']}\n\n{mailing_creation[str(message.chat.id)]['text']}",
                     reply_markup=keyboard)


def survey_creation_(message):
    keyboard = types.InlineKeyboardMarkup()
    callback_button = types.InlineKeyboardButton(text="Опубликовать", callback_data="publish")
    keyboard.add(callback_button)
    callback_button = types.InlineKeyboardButton(text="Отмена публикации", callback_data="dont_publish")
    keyboard.add(callback_button)

    temp = ""

    for i in range(survey_creation[str(message.chat.id)]['number']):
        temp += f"{i + 1}{survey_creation[str(message.chat.id)]['ans'][i]}\n"

    bot.send_message(message.chat.id,
                     f"{survey_creation[str(message.chat.id)]['header']}\n\n{survey_creation[str(message.chat.id)]['text']}\n\n{temp}",
                     reply_markup=keyboard)


def mailing_menu(message):
    keyboard = types.InlineKeyboardMarkup()
    callback_button = types.InlineKeyboardButton(text="Посмотреть последнии рассылки", callback_data="menu_2")
    keyboard.add(callback_button)
    callback_button = types.InlineKeyboardButton(text="Создать рассылку", callback_data="menu_3")
    keyboard.add(callback_button)
    bot.send_message(message.chat.id, menu_, reply_markup=keyboard)


def creation_mailing(message):
    keyboard = types.InlineKeyboardMarkup()
    callback_button = types.InlineKeyboardButton(text="Посмотерть последнии рассылки", callback_data="listMailing")
    keyboard.add(callback_button)

    if str(message.chat.id) in Read(admin)["admin"]:
        callback_button = types.InlineKeyboardButton(text="Создать рассылку", callback_data="menu_2")
        keyboard.add(callback_button)
        callback_button = types.InlineKeyboardButton(text="Создать опрос", callback_data="menu_3")
        keyboard.add(callback_button)

    bot.send_message(message.chat.id, menu_, reply_markup=keyboard)


def start_mailing(message):
    keyboard = types.InlineKeyboardMarkup()
    callback_button = types.InlineKeyboardButton(text="Отмена", callback_data="cancel")
    keyboard.add(callback_button)

    bot.edit_message_text(chat_id=message.chat.id, message_id=message.message_id,
                          text="Напишите заголовок рассылки", reply_markup=keyboard)


def start_survey(message):
    keyboard = types.InlineKeyboardMarkup()
    callback_button = types.InlineKeyboardButton(text="Отмена", callback_data="cancel")
    keyboard.add(callback_button)

    bot.edit_message_text(chat_id=message.chat.id, message_id=message.message_id,
                          text="Напишите заголовок рассылки", reply_markup=keyboard)


class change_settings(Thread):
    def __init__(self):
        Thread.__init__(self)

    def run(self):
        while True:
            if len(operations) != 0:
                if operations[0][0] == "creation":
                    Write(operations[0][1], operations[0][2], operations[0][3])
                elif operations[0][0] == "change":
                    Write_parameter(operations[0][1], operations[0][2], operations[0][3], link)
                elif operations[0][0] == "mailing":
                    lastNumder = list(Read(mailing_))
                    if lastNumder:
                        Write(f"{int(lastNumder[-1]) + 1}", {"type": mailing_creation[operations[0][1]]["type"],
                                                             "header": mailing_creation[operations[0][1]]["header"],
                                                             "text": mailing_creation[operations[0][1]]["text"],
                                                             "number": mailing_creation[operations[0][1]]["number"],
                                                             "ans": mailing_creation[operations[0][1]]["ans"]},
                              mailing_)
                        bot.send_message(operations[0][1],
                                         f"Ваша рассылка опубликована, номер рассылки: {int(lastNumder[-1]) + 1}")
                    else:
                        Write(f"{1}", {"type": mailing_creation[operations[0][1]]["type"],
                                       "header": mailing_creation[operations[0][1]]["header"],
                                       "text": mailing_creation[operations[0][1]]["text"],
                                       "number": mailing_creation[operations[0][1]]["number"],
                                       "ans": mailing_creation[operations[0][1]]["ans"]},
                              mailing_)

                        bot.send_message(operations[0][1], f"Ваша рассылка опубликована, номер рассылки: {1}")
                    del mailing_creation[operations[0][1]]

                elif operations[0][0] == "survey":
                    lastNumder = list(Read(mailing_))
                    if lastNumder:
                        Write(f"{int(lastNumder[-1]) + 1}", {"type": survey_creation[operations[0][1]]["type"],
                                                             "header": survey_creation[operations[0][1]]["header"],
                                                             "text": survey_creation[operations[0][1]]["text"],
                                                             "number": survey_creation[operations[0][1]]["number"],
                                                             "ans": survey_creation[operations[0][1]]["ans"],
                                                             "vote": [0, 0, 0, 0, 0, 0, 0, 0],
                                                             "who_voted": []},
                              mailing_)
                        bot.send_message(operations[0][1],
                                         f"Ваша рассылка опубликована, номер рассылки: {int(lastNumder[-1]) + 1}")
                    else:
                        Write(f"{1}", {"type": survey_creation[operations[0][1]]["type"],
                                       "header": survey_creation[operations[0][1]]["header"],
                                       "text": survey_creation[operations[0][1]]["text"],
                                       "number": survey_creation[operations[0][1]]["number"],
                                       "ans": survey_creation[operations[0][1]]["ans"],
                                       "vote": [0, 0, 0, 0, 0, 0, 0, 0],
                                       "who_voted": []},
                              mailing_)

                        bot.send_message(operations[0][1], f"Ваша рассылка опубликована, номер рассылки: {1}")
                    del survey_creation[operations[0][1]]

                elif operations[0][0] == "voice":
                    temp = Read(mailing_)
                    if operations[0][1] not in temp[operations[0][2]]["who_voted"]:
                        temp[operations[0][2]]["vote"][int(operations[0][3])] += 1
                        Write_parameter(operations[0][2], "vote", temp[operations[0][2]]["vote"], mailing_)
                        Write_parameter(operations[0][2], "who_voted",
                                        temp[operations[0][2]]["who_voted"] + [operations[0][1]], mailing_)

                operations.popleft()


class mailing_start(Thread):
    def __init__(self):
        Thread.__init__(self)

    def run(self):
        temp = Read(mailing_)
        last_number = 0
        if temp:
            last_number = int(list(temp)[-1])

        while True:
            temp = Read(mailing_)
            list_mailing = list(temp)

            if temp:
                while int(list_mailing[-1]) > last_number:
                    c = Read(link)
                    for id in c:
                        if c[id]["mailing_type"] == 1:
                            if temp[str(last_number + 1)]["type"] == 0:
                                bot.send_message(id,
                                                 f"Рассылка №{last_number + 1}: {temp[str(last_number + 1)]['header']}\n\n{temp[str(last_number + 1)]['text']}")
                            else:
                                keyboard = types.InlineKeyboardMarkup()
                                for i, ans in enumerate(temp[str(last_number + 1)]["ans"]):
                                    callback_button = types.InlineKeyboardButton(text=ans,
                                                                                 callback_data=f"ans_{last_number + 1}_{i}")
                                    keyboard.add(callback_button)

                                bot.send_message(id,
                                                 f"Опрос №{last_number + 1}: {temp[str(last_number + 1)]['header']}\n",
                                                 reply_markup=keyboard)

                        elif c[id]["mailing_type"] == 2:
                            if temp[str(last_number + 1)]["type"] == 0:
                                mailing_email(c[id]["email"], last_number + 1, temp[str(last_number + 1)]['header'],
                                              temp[str(last_number + 1)]['text'])
                            else:
                                survey_email(c[id]["email"], last_number + 1, temp[str(last_number + 1)]['header'],
                                             temp[str(last_number + 1)]['text'], temp[str(last_number + 1)]['ans'], id)

                    last_number += 1
            sleep(0.1)


class web_survey(Thread):
    def __init__(self):
        Thread.__init__(self)

    def run(self):
        while True:
            temp = Read(mailing_)

            voice = get("https://helperbotvvvvtrt.pythonanywhere.com/return").text

            if voice != "None":
                ret = voice.split("_")
                operations.append(["voice", ret[0], ret[1], ret[2]])

                ans = ""
                for i, ot in enumerate(temp[ret[1]]["ans"]):
                    if i == int(ret[2]):
                        ans += f'<p style="font-size: 200%;">{i + 1}.✓|{temp[ret[1]]["vote"][i] + 1}| {ot}</p>'
                    else:
                        ans += f'<p style="font-size: 200%;">{i + 1}.|{temp[ret[1]]["vote"][i]}| {ot}</p>'

                user = Read(link)

                end_surve_email(user[ret[0]]["email"], ret[1], temp[ret[1]]["header"], temp[ret[1]]["text"], ans)


if __name__ == '__main__':
    change_settings_ = change_settings()
    change_settings_.start()

    mailing_start_ = mailing_start()
    mailing_start_.start()

    web_survey_ = web_survey()
    web_survey_.start()

    bot.infinity_polling()
