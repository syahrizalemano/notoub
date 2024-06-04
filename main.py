import os
import telebot
import requests
from PIL import Image

# Setup bot
API_TOKEN = '7352646507:AAH7iuS1biiE82ZDljbkZvIfAUA7lCX-kik'
bot = telebot.TeleBot(API_TOKEN)

GRADIO_API_URL = "https://huggingfacem4-screenshot2html.hf.space/api/predict"

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Send me a screenshot and I will extract HTML and render it for you!")

@bot.message_handler(content_types=['photo'])
def handle_docs_photo(message):
    file_info = bot.get_file(message.photo[-1].file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    with open("received_image.png", 'wb') as new_file:
        new_file.write(downloaded_file)
    image_path = "received_image.png"
    try:
        generated_text, rendered_image_path = call_api_endpoint(image_path)
        bot.send_message(message.chat.id, generated_text)
        if rendered_image_path:
            with open(rendered_image_path, 'rb') as photo:
                bot.send_photo(message.chat.id, photo)
    except Exception as e:
        bot.send_message(message.chat.id, f"An unexpected error occurred: {str(e)}")

def call_api_endpoint(image_path):
    with open(image_path, 'rb') as img_file:
        files = {'data': ('image.png', img_file, 'image/png')}
        data = {'fn_index': 0}  # fn_index might need to be adjusted according to your specific API
        response = requests.post(GRADIO_API_URL, files=files, data=data)

    if response.status_code == 200:
        result = response.json()
        generated_text = result['data'][0]
        rendered_image_url = result['data'][1]

        # Download rendered image
        response = requests.get(rendered_image_url)
        if response.status_code == 200:
            rendered_image_path = "rendered_image.png"
            with open(rendered_image_path, 'wb') as img_file:
                img_file.write(response.content)
            return generated_text, rendered_image_path
        else:
            raise Exception("Failed to download rendered image.")
    else:
        raise Exception(f"Error from API: {response.status_code} {response.text}")

bot.infinity_polling()
