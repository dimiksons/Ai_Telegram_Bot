import telebot
from telebot.types import Message
from keras.models import load_model
from PIL import Image, ImageOps
import numpy as np

def detect_image(input_path, model):
    np.set_printoptions(suppress=True)
    model = load_model(model, compile=False)
    data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)
    image = Image.open(input_path).convert("RGB")
    size = (224, 224)
    image = ImageOps.fit(image, size, Image.Resampling.LANCZOS)
    image_array = np.asarray(image)
    normalized_image_array = (image_array.astype(np.float32) / 127.5) - 1
    data[0] = normalized_image_array
    prediction = model.predict(data)
    index = np.argmax(prediction)
    confidence_score = prediction[0][index]
    return index, confidence_score

bot = telebot.TeleBot('<TOKEN>')
@bot.message_handler(commands=['start'])
def start_cmd(message: Message):
    bot.send_message(message.chat.id, 'Привет! Я бот ИИ, который отличает планеты.')

@bot.message_handler(content_types='photo')
def photo_cmd(message: Message):
    if not message.photo:
        return bot.send_message(message.chat.id, 'Вы не отправили картинку😑')
    
    filename = f"photo_{message.from_user.id}.png"
    fileinfo = bot.get_file(message.photo[-1].file_id)
    file = bot.download_file(fileinfo.file_path)
    with open(filename, 'wb') as new_file:
        new_file.write(file)
    oldmessage = bot.send_message(message.chat.id, "Ваша картинка загружена, пожалуйста подождите!")

    index, score = detect_image(filename, "keras_model.h5")
    if score < 0.90:
        bot.send_message(message.chat.id, "Я не могу разобрать картинку):")
    elif index == 0:
        bot.send_message(message.chat.id, f"Это меркурий, я уверен в этом на {round(score * 100, 1)}%")
    elif index == 1:
        bot.send_message(message.chat.id, f"Это венера, я уверен в этом на {round(score * 100, 1)}%")
    elif index == 2:
        bot.send_message(message.chat.id, f"Это земля, я уверен в этом на {round(score * 100, 1)}%")
    elif index == 3:
        bot.send_message(message.chat.id, f"Это марс, я уверен в этом на {round(score * 100, 1)}%")
    elif index == 4:
        bot.send_message(message.chat.id, f"Это юпитер, я уверен в этом на {round(score * 100, 1)}%")
    elif index == 5:
        bot.send_message(message.chat.id, f"Это сатурн, я уверен в этом на {round(score * 100, 1)}%")
    elif index == 6:
        bot.send_message(message.chat.id, f"Это уран, я уверен в этом на {round(score * 100, 1)}%")
    elif index == 7:
        bot.send_message(message.chat.id, f"Это нептун, я уверен в этом на {round(score * 100, 1)}%")
    bot.delete_message(oldmessage.chat.id, oldmessage.id)

bot.infinity_polling()
