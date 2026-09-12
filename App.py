from flask import Flask, request, jsonify
import requests
import google.generativeai as genai
import os

app = Flask(__name__)

# 1. نقراو المفاتيح من Render مش من الكود
META_TOKEN = os.environ.get("META_TOKEN")
PHONE_ID = "1240073862533054"
GEMINI_KEY = os.environ.get("GEMINI_KEY")

genai.configure(api_key=GEMINI_KEY)

# 2. يرسل للواتساب
def send_whatsapp(to, text):
    url = f"https://graph.facebook.com/v20.0/{PHONE_ID}/messages"
    requests.post(url, json={
        "messaging_product": "whatsapp",
        "to": to,
        "text": {"body": text}
    }, headers={"Authorization": f"Bearer {META_TOKEN}"})

# 3. يهدر مع Gemini
def get_gemini_reply(text):
    model = genai.GenerativeModel('gemini-1.5-flash')
    prompt = f"انت بوت مطعم Le Parisien في وهران. رد قصير و ودود: {text}"
    return model.generate_content(prompt).text

# 4. الـ Webhook
@app.route("/webhook", methods=["GET", "POST"])
def webhook():
    if request.method == "GET":
        return request.args.get("hub.challenge")

    data = request.json
    msg = data['entry'][0]['changes'][0]['value']['messages'][0]['text']['body']
    from_number = data['entry'][0]['changes'][0]['value']['messages'][0]['from']

    reply = get_gemini_reply(msg)
    send_whatsapp(from_number, reply)
    return "ok"

if __name__ == "__main__":
    app.run()
