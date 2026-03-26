"""
🔮 LINE Horoscope Bot - บอทดูดวง (Version: Smart Button & Error Handling)
หมอเกมส์ x น้องกุ้ง 🦐
"""

import os
import json
import traceback
from flask import Flask, request, jsonify
from dotenv import load_dotenv
from linebot.v3 import WebhookHandler
from linebot.v3.exceptions import InvalidSignatureError
from linebot.v3.messaging import ApiException
from linebot.v3.messaging import (
    Configuration, ApiClient, MessagingApi,
    ReplyMessageRequest, TextMessage
)
from linebot.v3.webhooks import MessageEvent, TextMessageContent

# ─── Import Logics ───
from horoscope import format_horoscope, parse_date
from tarot import get_tarot_reading_by_number
from love import format_love_reading
from chinese_full import format_full_chinese_horoscope
from daily import get_daily_horoscope
from saju_logic import get_saju_reading

load_dotenv()
app = Flask(__name__)

# ─── LINE Config ───
CHANNEL_SECRET = os.getenv("LINE_CHANNEL_SECRET")
CHANNEL_ACCESS_TOKEN = os.getenv("LINE_CHANNEL_ACCESS_TOKEN")

configuration = Configuration(access_token=CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(CHANNEL_SECRET)

@app.route("/callback", methods=["POST"])
def callback():
    signature = request.headers.get("X-Line-Signature", "")
    body = request.get_data(as_text=True)
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        return jsonify({"error": "Invalid signature"}), 400
    except Exception as e:
        traceback.print_exc()
        return "OK", 200
    return "OK", 200

@app.route("/", methods=["GET"])
def health():
    return "🔮 บอทดูดวงกำลังทำงานอยู่!"

@handler.add(MessageEvent, message=TextMessageContent)
def handle_text_message(event):
    raw_text = event.message.text.strip()
    user_text_lower = raw_text.lower()
    
    try:
        # 1. เช็กคำสั่งช่วยเหลือ (หรือถ้ากดปุ่มแล้วยังไม่ใส่วันที่)
        if user_text_lower in ["/help", "ช่วยเหลือ", "help", "วิธีใช้", "ดูดวงวันนี้", "วิเคราะห์ซาจู"]:
            reply = (
                "🔮 **วิธีใช้บอทดูดวง หมอเกมส์**\n"
                "━━━━━━━━━━━━━━━━━━━━\n"
                "📅 **ดูดวงรายวัน:** พิมพ์ 'ดวง' ตามด้วยวันเกิด\n"
                "👉 เช่น: `ดวง 25/12/2535` หรือ `ดวง 10-06-1973`\n\n"
                "🇰🇷 **ซาจูเกาหลี:** พิมพ์ 'ซาจู' ตามด้วยวันเกิด\n"
                "👉 เช่น: `ซาจู 10/06/1973`\n\n"
                "🃏 **ไพ่ทาโรต์:** พิมพ์ 'ไพ่' เพื่อเริ่มอธิษฐาน\n"
                "━━━━━━━━━━━━━━━━━━━━"
            )
            send_reply(event.reply_token, reply)
            return

        # 2. จัดการเรื่องไพ่ทาโรต์
        if raw_text.startswith("ไพ่") or user_text_lower.startswith("tarot") or "เลือก ไพ่" in raw_text:
            # ดึงเฉพาะตัวเลขออกมา
            num_part = ''.join(filter(str.isdigit, raw_text))
            if not num_part:
                reply = (
                    "🃏 **ตั้งจิตอธิษฐานให้สงบ**\n"
                    "แล้วเลือกตัวเลขที่ชอบที่สุด **1 ถึง 78**\n\n"
                    "📥 **พิมพ์ตอบกลับมาว่า:**\n"
                    "เลือก [หมายเลข]\n"
                    "(ตัวอย่าง: `เลือก 77` หรือ `77` เฉยๆ ก็ได้ครับ)"
                )
                send_reply(event.reply_token, reply)
                return
            else:
                response = get_tarot_reading_by_number(int(num_part))
                send_reply(event.reply_token, response)
                return

        # 3. จัดการคำสั่ง "เลือก [ตัวเลข]"
        if raw_text.startswith("เลือก") or (raw_text.isdigit() and 1 <= int(raw_text) <= 78):
            num_part = ''.join(filter(str.isdigit, raw_text))
            if num_part:
                response = get_tarot_reading_by_number(int(num_part))
                send_reply(event.reply_token, response)
                return

        # 4. หมวดหมู่ที่ต้องใช้ "วันเกิด"
        mode = "general"
        clean_date = raw_text

        if "ดวง" in raw_text or "today" in user_text_lower:
            mode = "daily"
            clean_date = raw_text.replace("ดวง", "").replace("ดูดวงวันนี้", "").replace("today", "").strip()
        elif "ซาจู" in raw_text or "saju" in user_text_lower:
            mode = "saju"
            clean_date = raw_text.replace("ซาจู", "").replace("วิเคราะห์ซาจู", "").replace("saju", "").strip()
        elif "รัก" in raw_text or "love" in user_text_lower:
            mode = "love"
            clean_date = raw_text.replace("รัก", "").replace("love", "").strip()

        # ตรวจสอบว่ามีตัวเลขวันที่ปนอยู่ไหม
        if any(char.isdigit() for char in clean_date):
            birth_date = parse_date(clean_date)
            if birth_date:
                if mode == "daily": response = get_daily_horoscope(birth_date)
                elif mode == "saju": response = get_saju_reading(birth_date)
                elif mode == "love": response = format_love_reading(birth_date)
                else: response = format_horoscope(birth_date)
                send_reply(event.reply_token, response)
            else:
                send_reply(event.reply_token, f"❌ รูปแบบวันที่ '{clean_date}' ไม่ถูกต้องครับ\nตัวอย่าง: `ดวง 10/06/1973`")
        elif mode != "general":
            # ถ้ากดปุ่มมาแต่ไม่มีวันที่ ให้ส่งวิธีใช้
            handle_text_message(event) # เรียกตัวเองเพื่อส่ง Help

    except Exception as e:
        print(f"❌ Error: {e}")
        traceback.print_exc()

def send_reply(reply_token: str, text: str):
    try:
        with ApiClient(configuration) as api_client:
            line_bot_api = MessagingApi(api_client)
            line_bot_api.reply_message(
                ReplyMessageRequest(
                    reply_token=reply_token,
                    messages=[TextMessage(text=text)]
                )
            )
    except Exception:
        traceback.print_exc()

if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
