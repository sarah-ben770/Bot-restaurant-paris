from flask import Flask, request
import requests
import google.generativeai as genai
import os

app = Flask(__name__)

# حطي التوكن تاع الواتساب هنا
VERIFY_TOKEN = "123456"
WHATSAPP_TOKEN = "حطي_التوكن_تاعك_هنا"
PHONE_NUMBER_ID = "حطي_id_تاعك_هنا"

# ربط Gemini
genai.configure(api_key="حطي_API_KEY_تاع_Gemini_هنا")
model = genai.GenerativeModel('gemini-1.5-flash')

@app.route('/webhook', methods=['GET'])
def verify():
    if request.args.get('hub.verify_token') == VERIFY_TOKEN:
        return request.args.get('hub.challenge')
    return "Verification failed", 403

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.get_json()
    if 'messages' in data['entry'][0]['changes'][0]['value']:
        message = data['entry'][0]['changes'][0]['value']['messages'][0]
        phone_number = message['from']
        msg_body = message['text']['body']

        # الرد بالذكاء الاصطناعي
        response = model.generate_content(f"انت بوت مطعم في باريس. رد بالفرنسية على: {msg_body}")
        reply = response.text

        send_whatsapp_message(phone_number, reply)
    return "ok"

def send_whatsapp_message(phone, text):
    url = f"https://graph.facebook.com/v20.0/{PHONE_NUMBER_ID}/messages"
    headers = {"Authorization": f"Bearer {WHATSAPP_TOKEN}"}
    payload = {
        "messaging_product": "what
