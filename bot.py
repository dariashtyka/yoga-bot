import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes, ConversationHandler, CallbackQueryHandler


# Стадії для тесту
Q1, Q2, Q3, Q4, Q5 = range(5)

T1_Q1, T1_Q2, T1_Q3, T1_Q4, T1_Q5, T1_Q6, T1_Q7, T1_Q8, T1_Q9, T1_Q10=range (10)

TOKEN = os.getenv("TOKEN")


# Зберігаємо тимчасово відповіді користувача у словнику (у context.user_data)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "✋ Привіт, вітаю в йога спільноті !\n\n" \
        "⚪️ Щоб пройти посвячення і бути йога монстром, пропоную😌:\n\n" \
        "   1. Прочитати йога-вікі та ознайомитись з усім теоретичним матеріалом.\n"\
        "   2. Закріпити знання, пройшовши невеличкий тест.\n\n"\
        "⚪️ Якщо ти вже познайомився з Вікою(я про йога-вікі😉), сміливо пиши /test та розпочинай !\n"\
        # "➖Простий варіант (для початківця). Напиши /test\n"\
        # "➖Середній варіант (для досвідченого). Напиши /test2\n"\
        # "➖Складний варіант (для йога монстрів). Напиши /test3\n"
        
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
         "Дякую за відповіді!"+"\n"+result_message+f"Ось твої результати: {score}/10"+"\n\n" + "\n".join(results)
    )
    return ConversationHandler.END


async def test1_cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Тест скасовано.")
    return ConversationHandler.END

if __name__ == '__main__':
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

    app.add_handler(CommandHandler("start", start))
    app.add_handler(test_conv)
    app.add_handler(test1_conv)

    print("Бот запущено")
    app.run_polling()
