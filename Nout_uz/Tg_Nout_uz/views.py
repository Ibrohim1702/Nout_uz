from telegram.ext import Updater, CallbackContext
from telegram import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton
from Tg_Nout_uz.models import *


def inline_btns(type=None, nta=1, user_id=0):
    btn = []
    if type == "prod":
        btn.append([
            InlineKeyboardButton("-", callback_data="-"),
            InlineKeyboardButton(f"{nta}", callback_data=f"{nta}"),
            InlineKeyboardButton("+", callback_data="+"),
        ])
        btn.append([
            InlineKeyboardButton("📥 Savatga qo'shish", callback_data="savat"),
        ])
    elif type == "savat":
        btn.append([
            InlineKeyboardButton("◀️Orqaga", callback_data="◀️Orqaga"),
            InlineKeyboardButton("🚕 Buyurtma berish", callback_data="🚕 Buyurtma berish")
        ])
        btn.append([
            InlineKeyboardButton("⏰ Yetkazib berish vaqti", callback_data="⏰ Yetkazib berish vaqti"),
        ])
        savat = Savat.objects.filter(user_id=user_id)
        if not savat:
            return InlineKeyboardMarkup([])
        for i in range(len(savat)):
            btn.append([
                InlineKeyboardButton(f"❌{savat[i].product}", callback_data=f"{savat[i].slug}")
            ])
        btn.append([

            InlineKeyboardButton("🧹 Savatni tozalash", callback_data="🧹 Savatni tozalash")
        ])

    return InlineKeyboardMarkup(btn)


def btns(type=None, ctg=None, brds=None):
    btn = []
    if type == 'lang':
        btn = [
            [KeyboardButton('🇺🇿Uz'), KeyboardButton('🇷🇺Ru')],
        ]
    elif type == 'langg':
        btn = [
            [KeyboardButton('🇺🇿Uz🇺🇿'), KeyboardButton('🇷🇺Ru🇷🇺')],
            [KeyboardButton("◀️Orqaga")]
        ]
    elif type == 'contact':
        btn = [
            [KeyboardButton("Contact 📞", request_contact=True)]
        ]
    elif type == 'menu':
        btn = [
            [KeyboardButton("Maxsulotlar (Kategoriyalar) 💻")],
            [KeyboardButton("Brandlar 👨‍💻")],
            [KeyboardButton("📥 Savat"), KeyboardButton("⚙ Sozlamalar")],
        ]

    elif type == 'ctgs':
        ctgs = Category.objects.all()

        for i in range(1, len(ctgs), 2):
            btn.append([
                KeyboardButton(ctgs[i - 1].content), KeyboardButton(ctgs[i].content),
            ])

        if len(ctgs) % 2:
            btn.append([
                KeyboardButton(ctgs[len(ctgs) - 1].content)
            ])

        btn.append([KeyboardButton("◀️Orqaga"), KeyboardButton("📥 Savat")])

    elif type == "product":
        ctgs = Category.objects.get(content=ctg)
        products = Product.objects.filter(ctg=ctgs)

        for i in range(1, len(products), 2):
            btn.append([
                KeyboardButton(products[i - 1].name), KeyboardButton(products[i].name),
            ])

        if len(products) % 2:
            btn.append([
                KeyboardButton(products[len(products) - 1].name)
            ])

        btn.append([KeyboardButton("◀️Orqaga")])

    elif type == "brd":
        brds = Brands.objects.all()

        for i in range(1, len(brds), 2):
            btn.append([
                KeyboardButton(brds[i - 1].content), KeyboardButton(brds[i].content),
            ])

        if len(brds) % 2:
            btn.append([
                KeyboardButton(brds[len(brds) - 1].content)
            ])
        btn.append([KeyboardButton("◀️Orqaga"), KeyboardButton("📥 Savat")])

    elif type == "products":
        types = Category.objects.all()
        for i in range(1, len(types), 2):
            btn.append([
                KeyboardButton(types[i - 1].name), KeyboardButton(types[i].name),
            ])

        if len(types) % 2:
            btn.append([
                KeyboardButton(types[len(types) - 1].name)
            ])

        btn.append([KeyboardButton("◀️Orqaga")])

    elif type == "brands":
        brds = Brands.objects.get(content=brds)
        products = Product.objects.filter(brds=brds)

        for i in range(1, len(products), 2):
            btn.append([
                KeyboardButton(products[i - 1].name), KeyboardButton(products[i].name),
            ])

        if len(products) % 2:
            btn.append([
                KeyboardButton(products[len(products) - 1].name)
            ])

        btn.append([
            KeyboardButton("◀️Orqaga")
        ])

    return ReplyKeyboardMarkup(btn, resize_keyboard=True)


def start(update, context):
    user = update.message.from_user
    tglog = Log.objects.filter(user_id=user.id).first()
    tg_user = TgUser.objects.filter(user_id=user.id).first()

    if not tglog:
        tglog = Log()
        tglog.user_id = user.id
        tglog.save()

    log = tglog.messages

    if not tg_user:
        tg_user = TgUser()
        tg_user.user_id = user.id
        tg_user.username = user.username
        tg_user.first_name = user.first_name
        tg_user.save()

        log['state'] = 1
        update.message.reply_html(
            f"Assalomu aleykum  <b>{user.username}</b>\nRo'yxatdan o'tish uchun, Tilni tanlang👇",
            reply_markup=btns("lang"))

    else:
        if log['state'] >= 10:
            log.clear()
            log['state'] = 10
            update.message.reply_text("Bosh menulardan birini tanlang!", reply_markup=btns('menu'))

        else:
            log['state'] = 1
            update.message.reply_html(
                f"Assalomu aleykum  <b>{user.username}</b>\nRo'yxatdan o'tish uchun, Tilni tanlang👇",
                reply_markup=btns("lang"))

    tglog.messages = log
    tglog.save()


def message_handler(update, context):
    user = update.message.from_user
    tglog = Log.objects.filter(user_id=user.id).first()
    tg_user = TgUser.objects.filter(user_id=user.id).first()
    log = tglog.messages

    msg = update.message.text

    if msg == "⚙ Sozlamalar":
        log['state'] = 40
        log['til'] = msg
        update.message.reply_text("Tilni tanlang", reply_markup=btns("langg"))
    elif msg == "🇺🇿Uz🇺🇿" :
        log['state'] = 41
        tg_user.til = msg
        tg_user.save()
        update.message.reply_text("Til o'zgartirldi")
        update.message.reply_text("Bosh menulardan birini tanlang!", reply_markup=btns('menu'))
    elif msg == "🇷🇺Ru🇷🇺":
        log['state'] = 42
        tg_user.til = msg
        tg_user.save()
        update.message.reply_text("Til o'zgartirldi")
        update.message.reply_text("Bosh menulardan birini tanlang!", reply_markup=btns('menu'))

    if msg == "◀️Orqaga":
        if log['state'] == 12:
            log['state'] = 11
            update.message.reply_text('Menulardan birini tanlang', reply_markup=btns('ctgs'))
        elif log['state'] == 11:
            log.clear()
            log['state'] = 10
            update.message.reply_text("Bosh menulardan birini tanlang!", reply_markup=btns('menu'))

        elif log['state'] == 13:
            log['state'] = 12
            update.message.reply_text("Quyidagilardan birini tanlang. ",
                                      reply_markup=btns(type='product', ctg=log['ctg']))
        elif log['state'] == 21:
            log['state'] = 20
            update.message.reply_text("Quydagi brendlardan birini tanlang", reply_markup=btns(type='brd'))

        elif log["state"] == 20:
            log['state'] = 10
            update.message.reply_text("Bosh menulardan birini tanlang!", reply_markup=btns('menu'))

        elif log['state'] == 30:
            log['state'] = 10
            update.message.reply_text("Bosh menulardan birini tanlang!", reply_markup=btns('menu'))
        elif log['state'] == 40:
            log['state'] = 10
            update.message.reply_text("Bosh menulardan birini tanlang!", reply_markup=btns('menu'))
    elif msg == "📥 Savat":
        log['state'] = 30
        savat = Savat.objects.filter(user_id=user.id)
        s = "Savatda:\n"
        summa = 0
        for i in savat:
            s += f"{i.amount} ✅ {i.product} {i.summ} \n"
            summa += i.summ
        if summa == 0:
            update.message.reply_text("Savatingiz bo'sh")
        else:
            s += f"Maxsulotlar: {summa} so'm\nYetkazip berish: Shahar ichida bepul"

            update.message.reply_text(s, reply_markup=inline_btns("savat", user_id=user.id))
            update.message.reply_text("Bosh menuga qaytish bo'limiga qaytish", reply_markup=btns('menu'))

    elif log['state'] == 1:
        log['name'] = msg
        log['state'] = 2
        update.message.reply_text("Ismingizni kiriting 🖊")

    elif log['state'] == 2:
        if msg.isalpha():
            log['name'] = msg
            log['state'] = 3
            update.message.reply_text("Siz bilan bog'lanishimiz uchun raqamingizni kiriting 📞",
                                      reply_markup=btns('contact'))
        else:
            update.message.reply_text("Iltimos ismingizni text formatida kiriting. !!!")
    elif log['state'] == 3:
        update.message.reply_text('Iltimos contact tugmasini bosing 👇')
        print(msg)

    elif log['state'] == 11:
        log['state'] = 12
        log['ctg'] = msg
        update.message.reply_text("Quydagilardan birini tanlang", reply_markup=btns(type='product', ctg=msg))

    elif log['state'] == 12:
        log['state'] = 12
        log['product'] = msg
        log["nta"] = 1
        product = Product.objects.filter(name=msg).first()
        log['price'] = product.price
        update.message.reply_text("Quyidagilardan birini tanlang. ", reply_markup=btns("prod"))

        Manitor = f"Manitor: {product.manitor}\n" if product.manitor else ""
        brand = f"Brendi: {product.brds}\n" if product.brds else ""
        Protsessor = f"Protsessor: {product.cpu}\n" if product.cpu else ""
        VideoKarta = f"VideoKarta: {product.gpu}\n" if product.gpu else ""
        Озу = f"Озу: {product.ram}\n" if product.ram else ""
        Hard = f"Hard: {product.hard}\n" if product.hard else ""

        context.bot.send_photo(
            photo=open(f'{product.img.path}', 'rb'),
            caption=f"{product.name}\n{brand}{Manitor}{Protsessor}{VideoKarta}{Озу}{Hard}\nNarxi:{product.price}",
            chat_id=user.id,
            reply_markup=inline_btns('prod', nta=log['nta'])
        )
    elif log['state'] == 20:
        log['brands'] = msg
        log['state'] = 21
        update.message.reply_text("Quydagilardan birini tanlang", reply_markup=btns("brands", brds=log['brands']))

    elif log['state'] == 21:
        log['product'] = msg
        log['state'] = 21

        log["nta"] = 1
        product = Product.objects.filter(name=msg).first()
        log['price'] = product.price
        update.message.reply_text("Quyidagilardan birini tanlang. ", reply_markup=btns("prod"))

        Nomi = f"<b>Nomi</b>: {product.name}\n" if product.name else ""
        Manitor = f"<b>Manitor</b>: {product.manitor}\n" if product.manitor else ""
        brand = f"<b>Brendi</b>: {product.brds}\n" if product.brds else ""
        Protsessor = f"<b>Protsessor</b>: {product.cpu}\n" if product.cpu else ""
        VideoKarta = f"<b>VideoKarta</b>: {product.gpu}\n" if product.gpu else ""
        Озу = f"<b>Озу</b>: {product.ram}\n" if product.ram else ""
        Hard = f"<b>Hard</b>: {product.hard}\n" if product.hard else ""
        Narxi = f"<b>Narxi</b>: {product.price}\n" if product.price else ""
        context.bot.send_photo(
            photo=open(f'{product.img.path}', 'rb'),
            caption=f"{Nomi}{brand}{Manitor}{Protsessor}{VideoKarta}{Озу}{Hard}\n{Narxi}",
            chat_id=user.id,
            reply_markup=inline_btns('prod', nta=log['nta']),
            parse_mode="HTML"
        )

    if msg == "Maxsulotlar (Kategoriyalar) 💻":
        log['state'] = 11
        update.message.reply_text('Menulardan birini tanlang', reply_markup=btns('ctgs'))

    if msg == "Brandlar 👨‍💻":
        log['state'] = 20
        update.message.reply_text("Quydagi brendlardan birini tanlang", reply_markup=btns(type='brd'))

    tglog.messages = log
    tglog.save()


def contact_handler(update, context):
    user = update.message.from_user
    tglog = Log.objects.filter(user_id=user.id).first()
    tg_user = TgUser.objects.filter(user_id=user.id).first()
    log = tglog.messages

    msg = update.message.contact
    contact = update.message.contact
    log['contact'] = contact.phone_number

    if log['state'] == 3:
        tg_user.name = log['name']
        # tg_user.last_name = log['last_name']
        tg_user.phone_number = log['contact']
        tg_user.save()
        log.clear()
        log['state'] = 10
        update.message.reply_text("Bosh menulardan birini tanlang!", reply_markup=btns('menu'))
    tglog.messages = log
    tglog.save()


def callback_handler(update, context, kwargs=None):
    query = update.callback_query
    data = query.data
    user = query.from_user
    tglog = Log.objects.filter(user_id=user.id).first()
    tg_user = TgUser.objects.filter(user_id=user.id).first()
    log = tglog.messages

    print(data)
    if data == "+":
        log['nta'] = log.get("nta", 1) + 1
        update.callback_query.answer(f"{log['nta']}")
        query.edit_message_reply_markup(reply_markup=inline_btns("prod", nta=log['nta']))

    elif data == "-":
        if log.get("nta", 1) <= 1:
            pass
        else:
            log['nta'] = log.get("nta", 1) - 1
            update.callback_query.answer(f"{log['nta']}")
            query.edit_message_reply_markup(reply_markup=inline_btns("prod", nta=log['nta']))

    elif data == "savat":
        savat = Savat.objects.filter(product=log['product'], user_id=user.id).first()
        if savat:
            savat.amount = savat.amount + log['nta']
            savat.summ = int(log['price'].strip("so'm").replace(" ", "")) * savat.amount
            savat.save()
        else:
            savat = Savat()
            savat.amount = log['nta']
            savat.product = log['product']
            savat.priceproduct = log['price']
            savat.user_id = user.id
            print(log)
            savat.summ = int(log['price'].strip("so'm").replace(" ", "")) * log['nta']
            savat.save()
        update.callback_query.answer(f"savatga qo'shildi")
        query.message.delete()

    if log['state'] == 30:
        if data == "🧹 Savatni tozalash":
            Savat.objects.filter(user_id=user.id).delete()
            update.callback_query.answer("Savat tozalandi")
            query.message.delete()
        elif data == "⏰ Yetkazib berish vaqti":
            query.message.reply_text(
                "Sizning buyurtmangiz kun davomida yetkazib beriladi aloqada bo'ling kuryermiz siz bilan tez orada bog'landa 😊")
            query.message.delete()
        elif data == "🚕 Buyurtma berish":
            query.message.reply_text(
                f"{user.username} sizning buyurtmangiz qabul qilindi. Qisqa vaqt ichida kuryerimz siz bilan bog'lanadi 😊")
            query.message.delete()
        elif data == "◀️Orqaga":
            log['state'] = 10
            query.message.reply_text("Bosh menulardan birini tanlang!", reply_markup=btns('menu'))
            query.message.delete()
        else:
            Savat.objects.filter(slug=data, user_id=user.id).delete()
            update.callback_query.answer("Savat tozalandi")
            query.message.delete()
            log['state'] = 30
            savat = Savat.objects.filter(user_id=user.id)
            s = "Savatda:\n"
            summa = 0
            for i in savat:
                s += f"{i.amount} ✅ {i.product} {i.summ} \n"
                summa += i.summ
            if summa == 0:
                query.message.reply_text("Savatingiz bo'sh")
            else:
                s += f"Maxsulotlar: {summa} so'm\nYetkazip berish: Shahar ichida bepul"

                query.message.reply_text(s, reply_markup=inline_btns("savat", user_id=user.id))

    tglog.messages = log
    tglog.save()
