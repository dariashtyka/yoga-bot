import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes, ConversationHandler, CallbackQueryHandler


# Стадії для тесту
Q1, Q2, Q3, Q4, Q5 = range(5)

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
                    'q3': 'Правильна відповідь: Ні в якому разі шавасану пропускати не можна. Кожна частина заняття важлива, а шавасана взагалі найголовніша. Без цього практика не те, що не спрацює, вона взагалі може бути шкідливою.', 
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

    app.add_handler(CommandHandler("start", start))
    app.add_handler(test_conv)

    print("Бот запущено")
    app.run_polling()
