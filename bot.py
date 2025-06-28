import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes, ConversationHandler, CallbackQueryHandler


# Стадії для тесту
Q1, Q2, Q3, Q4 = range(4)

TOKEN = os.getenv("TOKEN")


# Зберігаємо тимчасово відповіді користувача у словнику (у context.user_data)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "✋Привіт, вітаю в йога спільноті !\n\n" \
        "⚪️Перевірьмо, наскільки ти уважно слухав Павла та читав йога-вікі😌. Якщо ще не знайомий з Вікою, дуже рекомендую, вона прикольна.\n\n" \
        "⚪️Обирай свій рівень:\n"\
        "➖Простий варіант (для початківця). Напиши /test1\n"\
        "➖Середній варіант (для досвідченого). Напиши /test2\n"\
        "➖Складний варіант (для йога монстрів). Напиши /test3\n"
        
    )


# --- Обробка тесту ---
async def test_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("Ні", callback_data="q1_Ni"), InlineKeyboardButton("Так", callback_data="q1_Tak")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "1. Йога не спрацює для тих, у кого немає розтяжки?",
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
        "2. Чи може поперек розгинатись?",
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
        "4. Чи можна поїсти перед практикою за пів години?",
        reply_markup=reply_markup
    )
    return Q4

async def test_end(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    context.user_data['q4'] = query.data.split('_')[1]

    # Перевірка відповідей (приклад)
    correct_answers = {'q1': 'Ni', 'q2': 'Ni', 'q3': 'Ni', 'q4': 'Ni'}
    correct_answers_print = {'q1': 'Ні', 'q2': 'Ні', 'q3': 'Ні', 'q4': 'Ні'}
    explanations={  'q1': 'Правильна відповідь: Йога спрацює навіть для тих, у кого немає розтяжки. Амплітуда форми не важлива ! '
                        'Важливий рух і робота з увагою, диханням, тілом в ДАНИЙ момент у тій амплітуді, яку зараз маємо. Саме це і дає ефект при детальній роботі.',
                    'q2': 'Правильна відповідь: Ні, поперек анатомічно не розгинаєтсья! Він може лише скруглюватись.', 
                    'q3': 'Правильна відповідь: Ні в якому разі шавасану пропускати не можна. Кожна частина заняття важлива, а шавасана взагалі найголовніша. Без цього практика не те, що не спрацює, вона взагалі може бути шкідливою.', 
                    'q4': 'Правильна відповідь: Ні, треба їсти мінімум за 1,5-2 години, інакше їжа ще буде не перетравлена в шлунку.'}
    results = []
    for q in ['q1', 'q2', 'q3', 'q4']:
        user_answer = context.user_data.get(q)
        explanation_text=explanations[q]
        correct = "✅" if user_answer == correct_answers[q] else "❌"
        results.append(f"{q.upper()}: {correct_answers_print[q]} {correct} \n\n{explanation_text}\n\n")

    await query.message.reply_text(
        "Дякую за відповіді! Ось твої результати:\n\n" + "\n".join(results)
    )
    return ConversationHandler.END

async def test_cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Тест скасовано.")
    return ConversationHandler.END

if __name__ == '__main__':
    app = ApplicationBuilder().token(TOKEN).build()

    # Конверсаційний хендлер для тесту
    test_conv = ConversationHandler(
        entry_points=[CommandHandler('test1', test_start)],
        states={
            Q1: [CallbackQueryHandler(test_q2, pattern='^q1_')],
            Q2: [CallbackQueryHandler(test_q3, pattern='^q2_')],
            Q3: [CallbackQueryHandler(test_q4, pattern='^q3_')],
            Q4: [CallbackQueryHandler(test_end, pattern='^q4_')],
        },
        fallbacks=[CommandHandler('cancel', test_cancel)]
    )

    app.add_handler(CommandHandler("start", start))
    app.add_handler(test_conv)

    print("Бот запущено")
    app.run_polling()
