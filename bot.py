import os
import sqlite3
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes, ConversationHandler, CallbackQueryHandler
from telegram.constants import ParseMode
import random

# === Ініціалізація бази ===
def init_db():
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS users (chat_id INTEGER PRIMARY KEY)")
    conn.commit()
    conn.close()

# === Додати chat_id в базу ===
def add_user(chat_id: int):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute("INSERT OR IGNORE INTO users (chat_id) VALUES (?)", (chat_id,))
    conn.commit()
    conn.close()

# === Отримати всі chat_id ===
def get_all_users():
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute("SELECT chat_id FROM users")
    users = cursor.fetchall()
    conn.close()
    return [user[0] for user in users]

# Стадії для тесту
Q1, Q2, Q3, Q4, Q5 = range(5)
T1_Q1, T1_Q2, T1_Q3, T1_Q4, T1_Q5, T1_Q6, T1_Q7, T1_Q8, T1_Q9, T1_Q10 = range (10)
C_Q1, C_Q2, C_Q3, C_Q4, C_Q5, C_Q6 = range(6)
F_Q1, F_Q2, F_Q3, F_Q4, F_Q5, F_Q6, F_Q7, F_Q8, F_Q9, F_Q10 = range(10)
P_Q1, P_Q2, P_Q3, P_Q4, P_Q5, P_Q6, P_Q7, P_Q8, P_Q9, P_Q10, P_Q11, P_Q12 = range(12)
T2_Q1, T2_Q2, T2_Q3, T2_Q4, T2_Q5, T2_Q6, T2_Q7, T2_Q8, T2_Q9= range(9)
HISTORY=["Конференція",
        "1992 Київ",
        "Обмін контактами",
        "Передача Твердохлєб",
        "Греція",
        "Перші тренування",
        "Данхем і Патабхі",
        "Бум йоги"]
HISTORY_PRINT = {
    'Конференція': 'Андрій Лаппа бере участь у першій Московській міжнародній конференції з йоги.',
    '1992 Київ': 'У 1992 році до Києва прибуває американець Джозеф Данхем у пошуках майстрів йогічної гімнастики. Він був учнем Анжели Фармер і Віктора ван Кутена.',
    'Обмін контактами': 'Андрій Лаппа ділиться контактами з майстрами, які потім передає Андрію Сідерському.',
    'Передача Твердохлєб': 'Андрій Сідерський передає контакти Олені Твердохлєб для організації зв’язку з метою навчання.',
    'Греція': 'Олена Твердохлєб за дорученням Сідерського їде до Греції, щоб домовитися про співпрацю з Віктором ван Кутеном і Анжелою Фармер.',
    'Перші тренування': 'Андрій Сідерський проводить перші тренування для Джозефа Данхема.',
    'Данхем і Патабхі': 'Джозеф Данхем знаходить великого майстра Патабхі Джойса в Індії та популяризує його школу в США.',
    'Бум йоги': 'Йога-бум охоплює світ і доходить до України.',
}


TOKEN = os.getenv("TOKEN")


# Зберігаємо тимчасово відповіді користувача у словнику (у context.user_data)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    add_user(chat_id)
    await update.message.reply_text(
        "✋ Привіт, вітаю в йога спільноті!\n\n"
        "Щоб пройти посвячення і бути йога монстром, пропоную 😌:\n\n"
        "   1. Прочитати йога-вікі та ознайомитись з усім теоретичним матеріалом.\n"
        "   2. Закріпити знання, пройшовши невеличкий тест.\n\n"
        "⚪️ Якщо ти вже познайомився з Вікою (я про йога-вікі), сміливо пиши /test та розпочинай!\n\n"
        "⚪️ Якщо ти вже пройшов посвячення, пропоную тематичні тести:\n\n"
        "🔘 БАЗА\n"
        "   🔗 Про форму, складність /form\n"
        "   ♻️ Біль — /pain\n"
        "   🪖 Про йогу, духовність, медитацію — /yoga\n"
        "   📜 Історія йоги в Україні — /history\n\n"
        # "🔘 ТІЛО\n"
        # "   ▪️ Тіло — основний інструмент /tilo1\n"
        # "   ▪️ Осьове витяжіння /tilo2\n"
        # "   ▪️ Робота з опорою /tilo3\n"
        # "   ▪️ Центрування /tilo4\n"
        # "   ▪️ Основні рухи торсу /tilo5\n\n"
        # "🔘 ДИХАННЯ\n"
        # "🔘 УВАГА\n"
        # "🔘 ХАРЧУВАННЯ"
        "\n"
        "🔘 ІНШЕ\n"
        "   ▪️ Екзамен від йога-майора /examen\n"
        "   ▪️ Тест на культурну йога-освіченість /culture"
    )


# --- Обробка тесту ---
async def test_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("Ні", callback_data="q1_Ni"), InlineKeyboardButton("Так", callback_data="q1_Tak")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "1. Йога працює лише для тих, у кого є розтяжка?",
        reply_markup=reply_markup
    )
    return Q1

async def test_q2(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    context.user_data['q1'] = query.data.split('_')[1]  # Отримаємо "Tak" чи "Ni"

    keyboard = [
        [InlineKeyboardButton("Ні", callback_data="q2_Ni"), InlineKeyboardButton("Так", callback_data="q2_Tak")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.message.reply_text(
        "2. Чи може поперек розгинатись у великій амплітуді?",
        reply_markup=reply_markup
    )
    return Q2

async def test_q3(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    context.user_data['q2'] = query.data.split('_')[1]

    keyboard = [
        [InlineKeyboardButton("Ні", callback_data="q3_Ni"), InlineKeyboardButton("Так", callback_data="q3_Tak")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.message.reply_text(
        "3. Чи можна пропустити шавасану, яку Павло задиктовує, якщо тобі захотілось?",
        reply_markup=reply_markup
    )
    return Q3

async def test_q4(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    context.user_data['q3'] = query.data.split('_')[1]

    keyboard = [
        [InlineKeyboardButton("Ні", callback_data="q4_Ni"), InlineKeyboardButton("Так", callback_data="q4_Tak")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.message.reply_text(
        "4. Чи можна мати повноцінний прийом їжі перед практикою за пів години?",
        reply_markup=reply_markup
    )
    return Q4

async def test_q5_prompt(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    context.user_data['q4'] = query.data.split('_')[1]
    await update.callback_query.message.reply_text(
        "5. Скільки років Павлу?",
        reply_markup=ReplyKeyboardRemove()
    )
    return Q5

async def test_q5(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['q5'] = update.message.text
    return await test_end(update, context)

async def test_end(update: Update, context: ContextTypes.DEFAULT_TYPE):
    score=1
    query = update.message

    # Перевірка відповідей (приклад)
    correct_answers = {'q1': 'Ni', 'q2': 'Ni', 'q3': 'Ni', 'q4': 'Ni'}
    correct_answers_print = {'q1': 'Ні', 'q2': 'Ні', 'q3': 'Ні', 'q4': 'Ні'}
    explanations={  'q1': 'Правильна відповідь: Ні, йога спрацює навіть для тих, у кого немає розтяжки. Амплітуда форми не важлива ! '
                        'Важливий рух і робота з увагою, диханням, тілом у ДАНИЙ момент у тій амплітуді, яку зараз маємо. Саме це і дає ефект при детальній роботі.',
                    'q2': 'Правильна відповідь: Ні, поперек анатомічно має дуже маленький градус розгинання! Основний його рух - це скруглення.', 
                    'q3': 'Правильна відповідь: Ні в якому разі задиктовану шавасану пропускати не можна. Кожна частина заняття важлива, а шавасана взагалі найголовніша. Без цього практика не те, що не спрацює, вона взагалі може бути шкідливою.', 
                    'q4': 'Правильна відповідь: Ні, треба їсти мінімум за 1,5-2 години, інакше їжа ще буде не перетравлена в шлунку. Але якщо сильний голод, за пів години можна зробити перекус фруктом чи горішками.',
                    'q5': 'Правильна відповідь: трохи більше 18 і трохи менше 100. Але ніхто достеменно не знає.'}
    results = []
    result_message=""
    for q in ['q1', 'q2', 'q3', 'q4']:
        user_answer = context.user_data.get(q)
        explanation_text=explanations[q]
        if user_answer == correct_answers[q]:
            correct = "✅" 
            score+=1 
        else :
            correct = "❌"
        results.append(f"{q.upper()}: {correct_answers_print[q]} {correct} \n\n{explanation_text}\n\n")
    if score == 2:
        result_message="2 в щоденник, маму в школу!\n"
    elif score == 5:
        result_message= "Ти пройшов посвячення, вітаю!\n"
    else:
        result_message= "Ти майже у цілі, потренуйся ще!\n"
    results.append(f"Q5: {context.user_data.get('q5')}✅\n\n{explanations['q5']}\n\n")

    await update.message.reply_text(
        "Дякую за відповіді!"+"\n"+result_message+f"Ось твої результати: {score}/5"+"\n\n" + "\n".join(results)
    )
    return ConversationHandler.END

async def test_cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Тест скасовано.")
    return ConversationHandler.END

# --- Обробка тесту 1 ---
async def test1_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("Неправда", callback_data="q1_Ni"), InlineKeyboardButton("Правда", callback_data="q1_Tak")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "1. Осьове витяжіння — це допоміжна опція, яку застосовують тільки в складних вправах після розігріву.",
        reply_markup=reply_markup
    )
    return T1_Q1

async def test1_q2(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    context.user_data['q1'] = query.data.split('_')[1]  # Отримаємо "Tak" чи "Ni"

    keyboard = [
        [InlineKeyboardButton("Неправда", callback_data="q2_Ni"), InlineKeyboardButton("Правда", callback_data="q2_Tak")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.message.reply_text(
        "2. Поперековий відділ хребта здатен на всі типи рухів, включаючи скрутки, але з меншою амплітудою.",
        reply_markup=reply_markup
    )
    return T1_Q2

async def test1_q3(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    context.user_data['q2'] = query.data.split('_')[1]

    keyboard = [
        [InlineKeyboardButton("Неправда", callback_data="q3_Ni"), InlineKeyboardButton("Правда", callback_data="q3_Tak")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.message.reply_text(
        "3. У практиці гімнастики йогів м’язи — це головний об’єкт уваги. Саме їх потрібно “включати” в кожній вправі.",
        reply_markup=reply_markup
    )
    return T1_Q3

async def test1_q4(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    context.user_data['q3'] = query.data.split('_')[1]

    keyboard = [
        [InlineKeyboardButton("Неправда", callback_data="q4_Ni"), InlineKeyboardButton("Правда", callback_data="q4_Tak")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.message.reply_text(
        "4. Мапа тіла в мозку — це точне відображення нашого реального фізичного тіла.",
        reply_markup=reply_markup
    )
    return T1_Q4

async def test1_q5(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    context.user_data['q4'] = query.data.split('_')[1]

    keyboard = [
        [InlineKeyboardButton("Неправда", callback_data="q5_Ni"), InlineKeyboardButton("Правда", callback_data="q5_Tak")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.message.reply_text(
        "5. Центрування — це процес стабілізації тільки в регіоні попереку.",
        reply_markup=reply_markup
    )
    return T1_Q5

async def test1_q6(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    context.user_data['q5'] = query.data.split('_')[1]

    keyboard = [
        [InlineKeyboardButton("Неправда", callback_data="q6_Ni"), InlineKeyboardButton("Правда", callback_data="q6_Tak")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.message.reply_text(
        "6. У гімнастиці йогів важливо в першу чергу знайти опору і правильно з нею взаємодіяти, перш ніж робити будь-який рух.",
        reply_markup=reply_markup
    )
    return T1_Q6

async def test1_q7(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    context.user_data['q6'] = query.data.split('_')[1]

    keyboard = [
        [InlineKeyboardButton("Неправда", callback_data="q7_Ni"), InlineKeyboardButton("Правда", callback_data="q7_Tak")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.message.reply_text(
        "7. Суглобно-сухожильна структура — це пасивний компонент практики, який активується тільки в статиці.",
        reply_markup=reply_markup
    )
    return T1_Q7

async def test1_q8(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    context.user_data['q7'] = query.data.split('_')[1]

    keyboard = [
        [InlineKeyboardButton("Неправда", callback_data="q8_Ni"), InlineKeyboardButton("Правда", callback_data="q8_Tak")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.message.reply_text(
        "8. Практика може бути ефективною і в автоматичному режимі, якщо тіло вже навчилося правильно виконувати техніки.",
        reply_markup=reply_markup
    )
    return T1_Q8

async def test1_q9(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    context.user_data['q8'] = query.data.split('_')[1]

    keyboard = [
        [InlineKeyboardButton("Неправда", callback_data="q9_Ni"), InlineKeyboardButton("Правда", callback_data="q9_Tak")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.message.reply_text(
        "9. Формально прості базові вправи можуть бути більш складними за відчуттями, ніж складні пози, бо вимагають більше уваги.",
        reply_markup=reply_markup
    )
    return T1_Q9

async def test1_q10(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    context.user_data['q9'] = query.data.split('_')[1]

    keyboard = [
        [InlineKeyboardButton("Неправда", callback_data="q10_Ni"), InlineKeyboardButton("Правда", callback_data="q10_Tak")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.message.reply_text(
        "10. Після правильно виконаної практики може зменшуватись нав’язливе мислення і тривожність через нейрофізіологічні процеси.",
        reply_markup=reply_markup
    )
    return T1_Q10

async def test1_end(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    score=0
    await query.answer()
    context.user_data['q10'] = query.data.split('_')[1]

    # Правильні відповіді
    correct_answers = {
        'q1': 'Ni', 'q2': 'Ni', 'q3': 'Ni', 'q4': 'Ni', 'q5': 'Ni',
        'q6': 'Tak', 'q7': 'Ni', 'q8': 'Ni', 'q9': 'Tak', 'q10': 'Tak'
    }
    user_answer_print ={"Ni":'Неправда', "Tak": 'Правда' }
    # Варіант для виводу: "Неправда" замість "Ні"
    correct_answers_print = {
        q: user_answer_print[correct_answers[q]] for q in correct_answers
    }

    explanations = {
        'q1': 'Пояснення: Осьове витяжіння — це базовий тип руху, і перша фаза будь-якого руху торсом, незалежно від складності вправи.',
        'q2': 'Пояснення: Поперек може скруглятись, але не повинен активно скручуватись чи розгинатись — це компенсаторні, небажані рухи.',
        'q3': 'Пояснення: Робота йде через суглоби й опору, м’язи — це виконавча структура, яка налаштовується автоматично під задачу.',
        'q4': 'Пояснення: Мапа тіла — віртуальна модель, часто викривлена, бо залежить від кількості рецепторів і звичних патернів.',
        'q5': 'Пояснення: Центрування — це розподіл навантаження від геометричного центру тіла на всю периферію, не лише стабілізація попереку.',
        'q6': 'Пояснення: Без контакту з опорою імпульс неможливий. Виштовхування з опори — перша фаза руху, включно з витяжінням.',
        'q7': 'Пояснення: Це — ключовий функціональний обʼєкт, який постійно задіюється в динаміці й у стабілізації, особливо через фасціальні лінії.',
        'q8': 'Пояснення: Автоматизм = втрата уваги і рецепторного потоку. Тіло починає рухатись за старими компенсаціями, зникає ефект.',
        'q9': 'Пояснення: Базові вправи — це не «легкі пози», а навчальні модулі, що вимагають точного залучення центрів, опори, уваги і координації.',
        'q10': 'Пояснення: Мозок вимикає другорядні процеси, звільняє оперативну пам’ять, відбувається тимчасове приглушення ментальних і емоційних схем.'
    }

    results = []
    for q in [f'q{i}' for i in range(1, 11)]:
        user_answer = context.user_data.get(q, '—')
        if user_answer == correct_answers[q]:
            correct = "✅" 
            score+=1 
        else :
            correct = "❌"
        correct_text = correct_answers_print[q]
        explanation_text = explanations.get(q, 'Пояснення відсутнє.')
        
        results.append(
            f"{q.upper()}:\n"
            f"Твоя відповідь: {user_answer_print[user_answer]} {correct}\n"
            # f"Правильна відповідь: {correct_text}\n"
            f"{explanation_text}\n\n"
        )
    if score == 2:
        result_message="2 в щоденник, маму в школу!\n"
    elif score == 10:
        result_message= "Вітаю в команді йога відмінників!\n"
    else:
        result_message= "Ти майже у цілі, потренуйся ще!\n"

    await query.message.reply_text(
         "Дякую за відповіді!"+"\n"+result_message+f"Ось твої результати: {score}/{len(correct_answers)}"+"\n\n" + "\n".join(results)
    )
    return ConversationHandler.END

async def test1_cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Тест скасовано.")
    return ConversationHandler.END

# --- Обробка тесту культура ---
async def culture_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("⚪️Тест «Продовжи фразу»\n\n" \
    "❗️ Пишіть з маленької літери без пробілів на початку та в кінці.\n"
    "❗️ _ вказує на кількість слів")
    await update.message.reply_text("1. Вельмишановні _ _ _")
    return C_Q1

async def culture_q2(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['q1']=update.message.text
    await update.message.reply_text("2. Пташки за вікном _ ")
    return C_Q2

async def culture_q3(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['q2']=update.message.text
    await update.message.reply_text("3. Від серця до _")
    return C_Q3

async def culture_q4(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['q3']=update.message.text
    await update.message.reply_text("4. Від куприка в _")
    return C_Q4

async def culture_q5(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['q4']=update.message.text
    await update.message.reply_text("5. Рас рас і на _ ")
    return C_Q5

async def culture_q6(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['q5']=update.message.text
    await update.message.reply_text("6. Йога кава від Павла _ _ _ _ _(автор Андрій) ")
    return C_Q6

async def culture_end(update: Update, context: ContextTypes.DEFAULT_TYPE):
    score=0
    context.user_data['q6']=update.message.text
    results=[]
    correct_answers = {'q1': 'пані та панове', 'q2': 'наспівали', 'q3': 'сонця', 'q4': 'маківку', 'q5':'матрас', 'q6':'бахнув раз і на діла' }
    l=len(correct_answers)
    question_beginning={'q1': 'Вельмишановні ' , 'q2': 'Пташки за вікном ', 'q3': 'Від серця до ', 'q4': 'Від куприка в ', 'q5':'Рас рас і на ', 'q6':'Йога кава від Павла ' }
    for q in [f'q{i}' for i in range(1, l+1)]:
        user_answer=context.user_data[q]
        if(user_answer==correct_answers[q]):
            score+=1
            correct = "✅" 
        else:
            correct = "❌"
        results.append(
            f"{q.upper()}:\n"
            f"Твоя відповідь: {question_beginning[q]}{user_answer}. {correct}\n"
            f"Правильна відповідь: {question_beginning[q]}{correct_answers[q]}. \n"
            # f"{explanation_text}\n\n"
        )
    if score == 2:
        result_message="2 в щоденник, маму в школу!\n"
    elif score == l:
        result_message= "Вітаю в команді йога відмінників!\n"
    else:
        result_message= "Ти майже у цілі, потренуйся ще!\n"
    await update.message.reply_text(
        "Дякую за відповіді!"+"\n"+result_message+f"Ось твої результати: {score}/{len(correct_answers)}"+"\n\n" + "\n".join(results)
    )
    return ConversationHandler.END

async def form_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🗝️ Основна задача цього тесту - саморефлексія. \n" \
                                    "🗝️ Балу в кінці не буде, але ти зможеш сам себе оцінити, звірившись з правильними відповідями")
    await update.message.reply_text("1. Який принцип працює у практиці гімнастиці для йогів, на відміну від сучасного підходу, щодо стану?")
    return F_Q1

async def form_q2(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['q1'] = update.message.text
    await update.message.reply_text("2. Який головний інструмент ми використовуємо для оптимізації роботи нашої психіки і свідомості?")
    return F_Q2

async def form_q3(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['q2'] = update.message.text
    await update.message.reply_text("3. Чи ми ставимо тіло як за самоціль досягнення фізичних властивостей, рельєфу?")
    return F_Q3

async def form_q4(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['q3'] = update.message.text
    await update.message.reply_text("4. Чи важливо в якому ми стані сідаємо на килимок?")
    return F_Q4

async def form_q5(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['q4'] = update.message.text
    await update.message.reply_text("5. Для чого нам розуміти всі наші данні, всі наші стани, коли сідаємо на килимок?")
    return F_Q5

async def form_q6(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['q5'] = update.message.text
    await update.message.reply_text("6. Що відбувається при порівнянні себе з кимось, звинуваченні себе у слабкості, малі силі?")
    return F_Q6

async def form_q7(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['q6'] = update.message.text
    await update.message.reply_text("7. Який принцип гімнастики йогів щодо складності?")
    return F_Q7

async def form_q8(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['q7'] = update.message.text
    await update.message.reply_text("8. Як треба реагувати на те, як нам під час практики?")
    return F_Q8

async def form_q9(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['q8'] = update.message.text
    await update.message.reply_text("9. Яку навичку ми напрацьовуємо, особливо важливу зараз в житті, а ще особливо військовим?")
    return F_Q9

async def form_q10(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['q9'] = update.message.text
    await update.message.reply_text("10. На що вказує те, якщо ви думаєте, що практика — це складно і ви поки не готові, вам ще рано?")
    return F_Q10

async def form_end(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['q10']=update.message.text
    results=[]
    l=len(context.user_data)
    correct_answers = {
        'q1': 'Робота з тим станом, який зараз маємо',
        'q2': 'Тіло',
        'q3': 'Ні, основна наша мета це психофізична оптимізація, приведення тіла і голови в порядок, а фізичні властивості це лише бонус',
        'q4': 'Ні, не важливо, це все матеріал для роботи на килимку',
        'q5': 'Щоб відштовхуючись від них, практикувати так, як ми можемо і відчувати в собі ЗМІНИ після тренування',
        'q6': 'Ми втікаємо від свого стану, від себе і там припиняється робота',
        'q7': 'Складно має бути ЗАВЖДИ. Тільки так ми змінимо тіло і нервову систему. Якщо зрозуміло і легко — це лише підвищує самооцінку і нічого більше',
        'q8': 'Ніяк! Просто робити так, як виходить і відслідковувати, що ми відчуваємо',
        'q9': 'Психічна адаптивність до стресів високої інтенсивності',
        'q10': 'Це вказує на втечу, слабку психічну адаптивність і уникання пікових стресів. Якщо цьому слідувати, то кожен стрес буде вас руйнувати і від нього вже не сховаєшся. Тому займаймося!'
    }
    for q in [f'q{i}' for i in range(1, l+1)]:
        user_answer=context.user_data[q]
        results.append(
            f"{q.upper()}:\n"
            f"⚪️ Твоя відповідь: {user_answer}\n"
            f"✅ Правильна відповідь: {correct_answers[q]}\n"
        )
    await update.message.reply_text(
        "Дякую за відповіді!"+"\n"+f"Ось твої результати:\n\n"+"\n".join(results)
    )
    return ConversationHandler.END

async def pain_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("⚪️Тест «Заповни пропуск»\n\n" \
    "❗️ Пишіть з маленької літери без пробілів на початку та в кінці.\n"
    "❗️ _ вказує на кількість слів")
    await update.message.reply_text("1. При коректному тренуванні в роботу включаються мʼязи, звʼязки, суглоби, фасції і _ ?")
    return P_Q1

async def pain_q2(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['q1']=update.message.text
    await update.message.reply_text("2. Мʼязи в в гімнастиці йогів здійснюють _ властивість.")
    return P_Q2
async def pain_q3(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['q2'] = update.message.text
    await update.message.reply_text("3. Рух виконується в _ , а тонус мʼязів просто дає можливість виконати цей рух.")
    return P_Q3

async def pain_q4(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['q3'] = update.message.text
    await update.message.reply_text("4. А от в роботі з вагами, при ізольованій зміні мʼязової структури вона _ ?")
    return P_Q4

async def pain_q5(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['q4'] = update.message.text
    await update.message.reply_text(
        "5. На відміну від «ізольованого» впливу на тканини, в практиці гімнастики йогів тіло працює по принципу _  "
        "всіх структур в багатоплощинний рух."
    )
    return P_Q5

async def pain_q6(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['q5'] = update.message.text
    await update.message.reply_text("6. При такому підході мозок реорганізується за рахунок створення нових складних _ звʼязків.")
    return P_Q6

async def pain_q7(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['q6'] = update.message.text
    await update.message.reply_text("7. Підвищення нейрогенезу забезпечує постійну _ , що усуває деградацію мозку з часом.")
    return P_Q7

async def pain_q8(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['q7'] = update.message.text
    await update.message.reply_text("8. Залучення структур тіла завжди йде поряд з _.")
    return P_Q8

async def pain_q9(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['q8'] = update.message.text
    await update.message.reply_text(
        "9. _ _ не порушує функціонал тіла, а навпаки, розвиває. Це постійне, наростаюче відчуття жжіння і навантаження "
        "в тканинах, що ніяк не обмежує рухомість того регіону тіла, що працював."
    )
    return P_Q9

async def pain_q10(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['q9'] = update.message.text
    await update.message.reply_text(
        "10. Різкі, швидко виникаючі і дуже інтенсивні, стріляючі відчуття, які не проходять після виконання вправи, "
        "а можливо і навіть посилюються — це _ _ ."
    )
    return P_Q10

async def pain_q11(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['q10'] = update.message.text
    await update.message.reply_text(
        "11. Умовно, беручи біль за 100 відсотків (нестерпний), робочий біль має бути приблизно на _ відсотків. (одне число з двох вказаних в методичці)"
    )
    return P_Q11

async def pain_q12(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['q11'] = update.message.text
    await update.message.reply_text(
        "12. Кожен рух і виконання вправ в практиці у початківців мають виконуватись у _ темпі."
    )
    return P_Q12

async def pain_end(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['q12'] = update.message.text
    l=len(context.user_data)
    score=0
    user_answer = {
        'q1': "При коректному тренуванні в роботу включаються мʼязи, звʼязки, суглоби, фасції і <u>" + context.user_data['q1'] + "</u>.",
        'q2': "Мʼязи в в гімнастиці йогів здійснюють <u>" + context.user_data['q2'] + "</u> властивість.",
        'q3': "Рух виконується в <u>" + context.user_data['q3'] + "</u>, а тонус мʼязів просто дає можливість виконати цей рух.",
        'q4': "А от в роботі з вагами, при ізольованій зміні мʼязової структури вона <u>" + context.user_data['q4'] + "</u>.",
        'q5': "На відміну від «ізольованого» впливу на тканини, в практиці гімнастики йогів тіло працює по принципу <u>" + context.user_data['q5'] + "</u> всіх структур в багаптоплощинний рух.",
        'q6': "При такому підході мозок реорганізується за рахунок створення нових складних <u>" + context.user_data['q6'] + "</u> звʼязків.",
        'q7': "Підвищення нейрогенезу забезпечує постійну <u>" + context.user_data['q7'] + "</u>, що усуває деградацію мозку з часом.",
        'q8': "Залучення структур тіла завжди йде поряд з <u>" + context.user_data['q8'] + "</u>.",
        'q9': "<u>" + context.user_data['q9'] + "</u> не порушує функціонал тіла, а навпаки, розвиває. Це постійне, наростаюче відчуття жжіння і навантаження в тканинах, що ніяк не обмежує рухомість того регіону тіла, що працював.",
        'q10': "Різкі, швидко виникаючі і дуже інтенсивні, стріляючі відчуття, які не проходять після виконання вправи, а можливо і навіть посилюються - це <u>" + context.user_data['q10'] + "</u>.",
        'q11': "Умовно, беручи біль за 100 відсотків(нестерпний), робочий біль має бути приблизно на <u>" + context.user_data['q11'] + "</u> відсотків.",
        'q12': "Кожен рух і виконання вправ в практиці у початківців мають виконуватись у <u>" + context.user_data['q12'] + "</u> темпі."
    }

    correct_answers = {
        'q1': 'сухожилля',
        'q2': 'виконавчу',
        'q3': 'суглобах',
        'q4': 'гіпертрофується',
        'q5': 'інтеграції',
        'q6': 'нейронних',
        'q7': 'нейропластичність',
        'q8': 'навантаженням',
        'q9': 'робочий біль',
        'q10': 'деструктивний біль',
        'q11': '50',
        'q12': 'повільному'
    }
    correct_answers_print = {
        'q1': "При коректному тренуванні в роботу включаються мʼязи, звʼязки, суглоби, фасції і <u>сухожилля</u>.",
        'q2': "Мʼязи в в гімнастиці йогів здійснюють <u>виконавчу</u> властивість.",
        'q3': "Рух виконується в <u>суглобах</u>, а тонус мʼязів просто дає можливість виконати цей рух.",
        'q4': "А от в роботі з вагами, при ізольованій зміні мʼязової структури вона <u>гіпертрофується</u>.",
        'q5': "На відміну від «ізольованого» впливу на тканини, в практиці гімнастики йогів тіло працює по принципу <u>інтеграції всіх структур в багатоплощинний рух</u>.",
        'q6': "При такому підході мозок реорганізується за рахунок створення нових складних <u>нейронних</u> звʼязків.",
        'q7': "Підвищення нейрогенезу забезпечує постійну <u>нейропластичність</u>, що усуває деградацію мозку з часом.",
        'q8': "Залучення структур тіла завжди йде поряд з <u>навантаженням</u>.",
        'q9': "<u>Робочий біль</u> не порушує функціонал тіла, а навпаки, розвиває. Це постійне, наростаюче відчуття жжіння і навантаження в тканинах, що ніяк не обмежує рухомість того регіону тіла, що працював.",
        'q10': "Різкі, швидко виникаючі і дуже інтенсивні, стріляючі відчуття, які не проходять після виконання вправи, а можливо і навіть посилюються - це <u>деструктивний біль</u>.",
        'q11': "Умовно, беручи біль за 100 відсотків(нестерпний), робочий біль має бути приблизно на <u>50-60</u> відсотків.",
        'q12': "Кожен рух і виконання вправ в практиці у початківців мають виконуватись у <u>повільному</u> темпі."
    }
    results =[]

    for q in [f'q{i}' for i in range (1, l+1) ]:
        correct=""
        user_a=context.user_data[q]
        if q=='q11':
            if user_a=='50' or user_a=='60':
                correct="✅"
                score +=1
        else:
            if user_a==correct_answers[q]:
                score +=1
                correct="✅"
            else:
                correct = "❌"
        results.append(
            f"{q.upper()}:\n"
            f"⚪️ Твоя відповідь: {user_answer[q]} {correct}\n"
            f"☑️ Правильна відповідь: {correct_answers_print[q]} \n"
        )
    if score == 2:
        result_message="2 в щоденник, маму в школу!\n"
    elif score == l:
        result_message= "Вітаю в команді йога відмінників!\n"
    else:
        result_message= "Ти майже у цілі, потренуйся ще!\n"
    await update.message.reply_text(
        "Дякую за відповіді!"+"\n"+result_message+f"Ось твої результати: {score}/{l}"+"\n\n" + "\n".join(results), parse_mode="HTML"
    )
    return ConversationHandler.END

async def yoga_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("A", callback_data="q1_A"), InlineKeyboardButton("Б", callback_data="q1_B"), InlineKeyboardButton("В", callback_data="q1_C")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "<b>1. З якого моменту в загальному сприйнятті йога почала асоціюватись з духовною практикою, яка дуже тісно переплітається з медитацією?</b>\n\n" \
        "А) З давніх часів як тільки йога виникла\n" \
        "Б) Коли йога почала популяризуватись в Індії\n" \
        "В) В минулому сторіччі коли йога з Індії потрапила в Америку і почала там популяризуватись",
        reply_markup=reply_markup,
        parse_mode=ParseMode.HTML
    )
    return T2_Q1

async def yoga_q2(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    keyboard = [
        [InlineKeyboardButton("А", callback_data="q2_A"),
         InlineKeyboardButton("Б", callback_data="q2_B"),
         InlineKeyboardButton("В", callback_data="q2_C")]
    ]
    await query.answer()
    context.user_data['q1'] = query.data.split('_')[1]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.callback_query.message.reply_text(
        "<b>2. Чому ті східні майстри, які до цього мали відношення, адаптували практику йоги на західний манер?</b>\n\n"
        "А) Бо практика йогів дуже занепала і вже вже не працювала\n"
        "Б) Бо майстри дуже добре розуміли, що саме потрібно для західних людей з їхнім темпом і ритмом життя\n"
        "В) Бо така адаптація безпечніша і ефективніша, ніж традиційний підхід",
        reply_markup=reply_markup,
        parse_mode=ParseMode.HTML
    )
    return T2_Q2

# Q3
async def yoga_q3(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    context.user_data['q2'] = query.data.split('_')[1]

    keyboard = [
        [InlineKeyboardButton("А", callback_data="q3_A"),
         InlineKeyboardButton("Б", callback_data="q3_B"),
         InlineKeyboardButton("В", callback_data="q3_C")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.message.reply_text(
        "<b>3. Практика гімнастики йогів це в першу чергу:</b>\n\n"
        "А) духовний інструмент, тісно повʼязаний з індуїзмом чи буддизмом\n"
        "Б) сухий інструмент по психофізичній адаптації, по опануванню контролю над своїм сприйняттям\n"
        "В) інструмент, щоб зробити тіло непробивним, гарним і здоровим",
        reply_markup=reply_markup,
        parse_mode=ParseMode.HTML
    )
    return T2_Q3

# Q4
async def yoga_q4(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    context.user_data['q3'] = query.data.split('_')[1]

    keyboard = [
        [InlineKeyboardButton("А", callback_data="q4_A"),
         InlineKeyboardButton("Б", callback_data="q4_B"),
         InlineKeyboardButton("В", callback_data="q4_C")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.message.reply_text(
        "<b>4. Через сильну популяризацію адаптованої практики в 60-х роках в Америці, початкова суть і принципи роботи йоги підмінили тим, що:</b>\n\n"
        "А) було зручніше продавати\n"
        "Б) було ефективніше і здоровіше для тіла\n"
        "В) надавало більше духовного розвитку",
        reply_markup=reply_markup,
        parse_mode=ParseMode.HTML
    )
    return T2_Q4

# Q5
async def yoga_q5(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    context.user_data['q4'] = query.data.split('_')[1]

    keyboard = [
        [InlineKeyboardButton("А", callback_data="q5_A"),
         InlineKeyboardButton("Б", callback_data="q5_B"),
         InlineKeyboardButton("В", callback_data="q5_C")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.message.reply_text(
        "<b>5. Що з цього неправда?</b>\n\n"
        "А) Практика гімнастики йогів в Індії до сих пір використовується для підготовки індійського спецназу\n"
        "Б) В бойових кланових лініях Китаю, Кореї і Вʼєтнаму гімнастика йогів була інструментом для швидкої підготовки тіла і психіки\n"
        "В) Гімнастика йогів практикувалась лише релігійними особами",
        reply_markup=reply_markup,
        parse_mode=ParseMode.HTML
    )
    return T2_Q5

# Q6
async def yoga_q6(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    context.user_data['q5'] = query.data.split('_')[1]

    keyboard = [
        [InlineKeyboardButton("А", callback_data="q6_A"),
         InlineKeyboardButton("Б", callback_data="q6_B"),
         InlineKeyboardButton("В", callback_data="q6_C")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.message.reply_text(
        "<b>6. Слово «медітато» було створене:</b>\n\n"
        "А) майстром Патабхі Джойс з аштанга йоги\n"
        "Б) католицьким священником Ігнатієм Лойолою\n"
        "В) вчителем Патабхі - Крішнамачарʼя",
        reply_markup=reply_markup,
        parse_mode=ParseMode.HTML
    )
    return T2_Q6

# Q7
async def yoga_q7(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    context.user_data['q6'] = query.data.split('_')[1]

    keyboard = [
        [InlineKeyboardButton("А", callback_data="q7_A"),
         InlineKeyboardButton("Б", callback_data="q7_B"),
         InlineKeyboardButton("В", callback_data="q7_C")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.message.reply_text(
        "<b>7. У східних традиціях було слово «медитація»?</b>\n\n"
        "А) так\n"
        "Б) ні\n"
        "В) інформація досі невідома",
        reply_markup=reply_markup,
        parse_mode=ParseMode.HTML
    )
    return T2_Q7

# Q8
async def yoga_q8(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    context.user_data['q7'] = query.data.split('_')[1]

    keyboard = [
        [InlineKeyboardButton("А", callback_data="q8_A"),
         InlineKeyboardButton("Б", callback_data="q8_B"),
         InlineKeyboardButton("В", callback_data="q8_C")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.message.reply_text(
        "<b>8. Що з цього неправда?</b>\n\n"
        "А) В східних лініях медитація була частиною, яка давалась усім учням після декілька років тренувань хатха йогою\n"
        "Б) «Медитація» в східних лініях називалась «раджа йога» – королівська практика, вінець йоги\n"
        "В) Є буддійські лінії, в яких одразу практикується медитація",
        reply_markup=reply_markup,
        parse_mode=ParseMode.HTML
    )
    return T2_Q8

# Q9
async def yoga_q9(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    context.user_data['q8'] = query.data.split('_')[1]

    keyboard = [
        [InlineKeyboardButton("А", callback_data="q9_A"),
         InlineKeyboardButton("Б", callback_data="q9_B"),
         InlineKeyboardButton("В", callback_data="q9_C")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.message.reply_text(
        "<b>9. В нашій роботі «медитація» це:</b>\n\n"
        "А) мета\n"
        "Б) результат\n"
        "В) окрема практика",
        reply_markup=reply_markup,
        parse_mode=ParseMode.HTML
    )
    return T2_Q9

async def yoga_end(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query=update.callback_query
    await query.answer()
    context.user_data['q9'] = query.data.split('_')[1]
    l=len(context.user_data)
    questions = {
        'q1': {
            'A': 'З давніх часів як тільки йога виникла',
            'B': 'Коли йога почала популяризуватись в Індії',
            'C': 'В минулому сторіччі коли йога з Індії потрапила в Америку і почала там популяризуватись'
        },
        'q2': {
            'A': 'Бо практика йогів дуже занепала і вже вже не працювала',
            'B': 'Бо майстри дуже добре розуміли, що саме потрібно для західних людей з їхнім темпом і ритмом життя',
            'C': 'Бо така адаптація безпечніша і ефективніша, ніж традиційний підхід'
        },
        'q3': {
            'A': 'духовний інструмент, тісно повʼязаний з індуїзмом чи буддизмом',
            'B': 'сухий інструмент по психофізичній адаптації, по опануванню контролю над своїм сприйняттям',
            'C': 'інструмент, щоб зробити тіло непробивним, гарним і здоровим'
        },
        'q4': {
            'A': 'було зручніше продавати',
            'B': 'було ефективніше і здоровіше для тіла',
            'C': 'надавало більше духовного розвитку'
        },
        'q5': {
            'A': 'Практика гімнастики йогів в Індії до сих пір використовується в якості основної тілесної дисципліни для підготовки індійського спецназу',
            'B': 'В бойових кланових і родових лініях Китаю, Кореї і Вʼєтнаму гімнастика йогів була інструментом для швидкої підготовки тіла і психіки, щоб людина надалі могла витримувати божевільні навантаження',
            'C': 'Гімнастика йогів практикувалась лише релігійними особами'
        },
        'q6': {
            'A': 'майстром Патабхі Джойс з аштанга йоги',
            'B': 'католицьким священником Ігнатієм Лойолою',
            'C': 'вчителем Патабхі - Крішнамачарʼя'
        },
        'q7': {
            'A': 'так',
            'B': 'ні',
            'C': 'інформація досі невідома'
        },
        'q8': {
            'A': 'В східних лініях медитація була частиною, яка давалась усім учням після декілька років тренувань хатха йогою',
            'B': '«медитація» в східних лініях називалась «раджа йога»- королівська практика, вінець йоги',
            'C': 'є буддійські лінії, в яких одразу практикується медитація'
        },
        'q9': {
            'A': 'мета',
            'B': 'результат',
            'C': 'окрема практика'
        }
    }

    correct_answers = {
        'q1': 'C',
        'q2': 'B',
        'q3': 'B',
        'q4': 'A',
        'q5': 'C',
        'q6': 'B',
        'q7': 'B',
        'q8': 'A',
        'q9': 'B'
    }
    correct_answer_ua={
        'A':'А',
        'B':'Б',
        'C':'В'
    }
    score=0
    results=[]
    for q in [f'q{i}' for i in range(0, l)]:
        us_ans=context.user_data[q]
        cor_ans=correct_answers[q]
        if us_ans==cor_ans:
            score+=1
            correct="✅"
        else:
            correct = "❌"
        results.append(
            f"{q.upper()}:\n"
            f"⚪️ Твоя відповідь: {correct_answer_ua[us_ans]}) {questions[q][us_ans]} {correct}\n"
            f"☑️ Правильна відповідь: {correct_answer_ua[cor_ans]}) {questions[q][cor_ans]} \n"
        )
    if score == 2:
        result_message="2 в щоденник, маму в школу!\n"
    elif score == l:
        result_message= "Вітаю в команді йога відмінників!\n"
    else:
        result_message= "Ти майже у цілі, потренуйся ще!\n"
    await query.message.reply_text(
        "Дякую за відповіді!"+"\n"+result_message+f"Ось твої результати: {score}/{l}"+"\n\n" + "\n".join(results), parse_mode="HTML"
    )
    return ConversationHandler.END

async def start_history(update:Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['correct_order']=HISTORY
    shuffled=HISTORY[:]
    random.shuffle(shuffled)
    context.user_data['remaining']=shuffled
    context.user_data['current_order']=[]
    await send_message_history(update, context)

async def send_message_history(update_or_query, context):
    remaining=context.user_data['remaining']
    current_order=context.user_data['current_order']
    keyboard=[
        [InlineKeyboardButton(text=statement, callback_data=f"choose_{statement}")]  for statement in context.user_data['remaining']
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    text = "🧩 Натисни на твердження у правильному порядку:\n\n"
    statements = "<u>🟢 Залишилось:</u>\n" + "\n".join(f"<b>▪️ {s}</b>\n<i>{HISTORY_PRINT[s]}</i>\n" for s in remaining)
    if current_order:
        text += "<u>⚪️ Твій вибір:</u>\n" + "\n".join(f"<b>▪️ {s}</b>\n<i>{HISTORY_PRINT[s]}</i>\n" for s in current_order) + "\n\n"
    if isinstance(update_or_query, Update):
        await update_or_query.message.reply_text(text+statements, reply_markup=reply_markup, parse_mode="HTML")
    else:
        await update_or_query.edit_message_text(text+statements, reply_markup=reply_markup, parse_mode="HTML")

async def handle_choice_history(update:Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    current=context.user_data['current_order'].copy()
    #save selection
    reply = query.data.split('_')[1]
    context.user_data['current_order'].append(reply)

    #check beafore remove !!
    if reply not in context.user_data['remaining']:
        return
    #remove from list of options
    context.user_data['remaining'].remove(reply)

    #if all tapped check the answer
    l=len(HISTORY)

    score=0
    correct=[]
    if not context.user_data['remaining']:
        for i in range (0, l):
            if HISTORY[i]==context.user_data['current_order'][i]:
                score+=1
                correct.append("✅")
            else:
                correct.append("❌")
        if score == 2:
            result_message="2 в щоденник, маму в школу!\n"
        elif score == l:
            result_message= "Вітаю в команді йога відмінників!\n"
        else:
            result_message= "Ти майже у цілі, потренуйся ще!\n"
        await query.message.edit_text(
            "Дякую за відповіді!" + "\n" +result_message+
            f"Ось твій результат: {score}/{l}" + "\n\n" + 
            f"<u>⚪️ Твій вибір:</u>\n" +
            "\n".join(f"<b>▪️ {s}{correct[i]}</b>\n<i>{HISTORY_PRINT[s]}</i>\n" for i, s in enumerate(current)) +
            "\n\n<u>🟢 Правильний порядок:</u>\n" +
            "\n".join([f"<b>▪️ {s}</b>\n<i>{HISTORY_PRINT[s]}</i>\n" for s in HISTORY]),
            parse_mode="HTML"
        )
    else:
        await send_message_history(query, context)
    

# === Обробка /broadcast (лише для тебе, наприклад) ===
async def broadcast(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != 512911472:
        await update.message.reply_text("Ця команда тільки для адміністратора.")
        return
    
    text = " ".join(context.args) or "Тестове повідомлення 📨"

    # замінимо символи \n на справжній перенос
    text = text.replace("\\n", "\n")

    all_users = get_all_users()
    count = 0
    for user_id in all_users:
        try:
            await context.bot.send_message(chat_id=user_id, text=text)
            count += 1
        except Exception as e:
            print(f"Не вдалося надіслати {user_id}: {e}")
    await update.message.reply_text(f"Повідомлення надіслано {count} користувачам ✅")


if __name__ == '__main__':
    init_db()
    app = ApplicationBuilder().token(TOKEN).build()

    # Конверсаційний хендлер для тесту
    test_conv = ConversationHandler(
        entry_points=[CommandHandler('test', test_start)],
        states={
            Q1: [CallbackQueryHandler(test_q2, pattern='^q1_')],
            Q2: [CallbackQueryHandler(test_q3, pattern='^q2_')],
            Q3: [CallbackQueryHandler(test_q4, pattern='^q3_')],
            Q4: [CallbackQueryHandler(test_q5_prompt, pattern='^q4_')], 
            Q5: [MessageHandler(filters.TEXT & ~filters.COMMAND, test_q5)],
        },
        fallbacks=[CommandHandler('cancel', test_cancel)]
    )

        # Конверсаційний хендлер для тесту
    test1_conv = ConversationHandler(
        entry_points=[CommandHandler('examen', test1_start)],
        states={
            T1_Q1: [CallbackQueryHandler(test1_q2, pattern='^q1_')],
            T1_Q2: [CallbackQueryHandler(test1_q3, pattern='^q2_')],
            T1_Q3: [CallbackQueryHandler(test1_q4, pattern='^q3_')],
            T1_Q4: [CallbackQueryHandler(test1_q5, pattern='^q4_')],
            T1_Q5: [CallbackQueryHandler(test1_q6, pattern='^q5_')],
            T1_Q6: [CallbackQueryHandler(test1_q7, pattern='^q6_')],
            T1_Q7: [CallbackQueryHandler(test1_q8, pattern='^q7_')], 
            T1_Q8: [CallbackQueryHandler(test1_q9, pattern='^q8_')],
            T1_Q9: [CallbackQueryHandler(test1_q10, pattern='^q9_')],
            T1_Q10: [CallbackQueryHandler(test1_end, pattern='^q10_')], 
        },
        fallbacks=[CommandHandler('cancel', test1_cancel)]
    )
            # Конверсаційний хендлер для тесту
    culture_conv = ConversationHandler(
        entry_points=[CommandHandler('culture', culture_start)],
        states={
            C_Q1: [MessageHandler(filters.TEXT & ~filters.COMMAND, culture_q2)],
            C_Q2: [MessageHandler(filters.TEXT & ~filters.COMMAND, culture_q3)],
            C_Q3: [MessageHandler(filters.TEXT & ~filters.COMMAND, culture_q4)],
            C_Q4: [MessageHandler(filters.TEXT & ~filters.COMMAND, culture_q5)],
            C_Q5: [MessageHandler(filters.TEXT & ~filters.COMMAND, culture_q6)],
            C_Q6: [MessageHandler(filters.TEXT & ~filters.COMMAND, culture_end)],
        },
        fallbacks=[CommandHandler('cancel', test1_cancel)]
    )
    form_conv = ConversationHandler(
        entry_points=[CommandHandler('form', form_start)],
        states={
            F_Q1: [MessageHandler(filters.TEXT & ~filters.COMMAND, form_q2)],
            F_Q2: [MessageHandler(filters.TEXT & ~filters.COMMAND, form_q3)],
            F_Q3: [MessageHandler(filters.TEXT & ~filters.COMMAND, form_q4)],
            F_Q4: [MessageHandler(filters.TEXT & ~filters.COMMAND, form_q5)],
            F_Q5: [MessageHandler(filters.TEXT & ~filters.COMMAND, form_q6)],
            F_Q6: [MessageHandler(filters.TEXT & ~filters.COMMAND, form_q7)],
            F_Q7: [MessageHandler(filters.TEXT & ~filters.COMMAND, form_q8)],
            F_Q8: [MessageHandler(filters.TEXT & ~filters.COMMAND, form_q9)],
            F_Q9: [MessageHandler(filters.TEXT & ~filters.COMMAND, form_q10)],
            F_Q10: [MessageHandler(filters.TEXT & ~filters.COMMAND, form_end)],
        },
        fallbacks=[CommandHandler('cancel', test1_cancel)]
    )
    pain_conv = ConversationHandler(
        entry_points=[CommandHandler('pain', pain_start)],
        states={
            P_Q1: [MessageHandler(filters.TEXT & ~filters.COMMAND, pain_q2)],
            P_Q2: [MessageHandler(filters.TEXT & ~filters.COMMAND, pain_q3)],
            P_Q3: [MessageHandler(filters.TEXT & ~filters.COMMAND, pain_q4)],
            P_Q4: [MessageHandler(filters.TEXT & ~filters.COMMAND, pain_q5)],
            P_Q5: [MessageHandler(filters.TEXT & ~filters.COMMAND, pain_q6)],
            P_Q6: [MessageHandler(filters.TEXT & ~filters.COMMAND, pain_q7)],
            P_Q7: [MessageHandler(filters.TEXT & ~filters.COMMAND, pain_q8)],
            P_Q8: [MessageHandler(filters.TEXT & ~filters.COMMAND, pain_q9)],
            P_Q9: [MessageHandler(filters.TEXT & ~filters.COMMAND, pain_q10)],
            P_Q10: [MessageHandler(filters.TEXT & ~filters.COMMAND, pain_q11)],
            P_Q11: [MessageHandler(filters.TEXT & ~filters.COMMAND, pain_q12)],
            P_Q12: [MessageHandler(filters.TEXT & ~filters.COMMAND, pain_end)],
        },
        fallbacks=[CommandHandler('cancel', test1_cancel)]
    )
    yoga_conv=ConversationHandler(
        entry_points=[CommandHandler('yoga', yoga_start)],
        states={
            T2_Q1: [CallbackQueryHandler(yoga_q2, pattern='^q1_')],
            T2_Q2: [CallbackQueryHandler(yoga_q3, pattern='^q2_')],
            T2_Q3: [CallbackQueryHandler(yoga_q4, pattern='^q3_')],
            T2_Q4: [CallbackQueryHandler(yoga_q5, pattern='^q4_')], 
            T2_Q5: [CallbackQueryHandler(yoga_q6, pattern='^q5_')],
            T2_Q6: [CallbackQueryHandler(yoga_q7, pattern='^q6_')],
            T2_Q7: [CallbackQueryHandler(yoga_q8, pattern='^q7_')],
            T2_Q8: [CallbackQueryHandler(yoga_q9, pattern='^q8_')], 
            T2_Q9: [CallbackQueryHandler(yoga_end, pattern='^q9_')], 
        },
        fallbacks=[CommandHandler('cancel', test1_cancel)]
    )
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(test_conv)
    app.add_handler(test1_conv)
    app.add_handler(culture_conv)
    app.add_handler(form_conv)
    app.add_handler(CommandHandler("broadcast", broadcast))  # /broadcast Привіт всім!
    app.add_handler(pain_conv)
    app.add_handler(yoga_conv)
    app.add_handler(CommandHandler("history", start_history))
    app.add_handler(CallbackQueryHandler(handle_choice_history, pattern="^choose_"))

    print("Бот запущено")
    app.run_polling()
