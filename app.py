"""
🔮 LINE Horoscope Bot - บอทดูดวง
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
from horoscope import format_horoscope, parse_date
from tarot import get_tarot_reading
from love import format_love_reading
from chinese_full import format_full_chinese_horoscope

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

@handler.add(MessageEvent)
def handle_all_events(event):
    if hasattr(event, 'message'):
        print(f"📨 Event: {event.type}, Msg: {getattr(event.message, 'type', 'N/A')}")

# ─── Message Handler (แก้ไขจุดที่ซ้ำซ้อน) ───
@handler.add(MessageEvent, message=TextMessageContent)
def handle_text_message(event):
    raw_text = event.message.text.strip()
    user_text = raw_text.lower()
    
    print(f"📩 ได้รับข้อความ: '{raw_text}'")
    
    try:
        # 1. เช็กคำสั่งช่วยเหลือ
        if raw_text in ["/help", "ช่วยเหลือ", "help", "วิธีใช้"]:
            reply = (
                "🔮 วิธีใช้บอทดูดวง หมอเกมส์ x น้องกุ้ง!\n"
                "━━━━━━━━━━━━━━━━━━━━\n"
                "🌟 เริ่มต้นใช้งานง่ายๆ เพียงพิมพ์ 'วันเกิด' ของคุณ\n"
                "เช่น: 25/12/2535 หรือ 10-05-1990\n\n"
                "✨ เมนูคำสั่งพิเศษ (พิมพ์คีย์เวิร์ด + วันเกิด):\n"
                "🃏 พิมพ์ 'ไพ่' + วันเกิด -> ดูไพ่ทาโรต์\n"
                "💕 พิมพ์ 'รัก' + วันเกิด -> ดูดวงความรัก\n"
                "🐉 พิมพ์ 'จีน' + วันเกิด -> ดูดวงจีนเต็ม\n"
                "━━━━━━━━━━━━━━━━━━━━\n"
                "👉 ลองพิมพ์วันเกิดของคุณส่งมาได้เลยครับ!"
            )
            send_reply(event.reply_token, reply)
            return

        # 2. แยก Mode และตัด Keyword ออกจากวันที่
        mode = "general"
        date_part = raw_text

        if raw_text.startswith("ไพ่") or user_text.startswith("tarot"):
            mode = "tarot"
            date_part = raw_text.replace("ไพ่", "").replace("tarot", "").replace("Tarot", "").strip()
        elif raw_text.startswith("รัก") or user_text.startswith("love"):
            mode = "love"
            date_part = raw_text.replace("รัก", "").replace("love", "").replace("Love", "").strip()
        elif raw_text.startswith("จีน") or user_text.startswith("chinese"):
            mode = "chinese"
            date_part = raw_text.replace("จีน", "").replace("chinese", "").replace("Chinese", "").strip()

        # 3. ประมวลผลวันที่
        birth_date = parse_date(date_part)
        print(f"🔍 Debug: Mode={mode}, DatePart='{date_part}', Parsed={birth_date}")

        if birth_date:
            if mode == "tarot":
                response = get_tarot_reading(birth_date)
            elif mode == "love":
                response = format_love_reading(birth_date)
            elif mode == "chinese":
                response = format_full_chinese_horoscope(birth_date)
            else:
                response = format_horoscope(birth_date)
            send_reply(event.reply_token, response)
        else:
            # กรณีที่มี Mode แต่แปลงวันที่ไม่สำเร็จ
            if mode != "general":
                send_reply(event.reply_token, f"❌ อ่านวันที่ '{date_part}' ไม่สำเร็จ\nกรุณาพิมพ์ เช่น: {mode} 10/06/1973")
            else:
                # กรณีพิมพ์ข้อความทั่วไปที่แปลงเป็นวันที่ไม่ได้
                reply = "🤔 ไม่เข้าใจรูปแบบวันเกิดครับ\nลองส่งแบบ 25/12/2538 หรือพิมพ์ 'วิธีใช้'"
                send_reply(event.reply_token, reply)

    except Exception as e:
        print(f"❌ ERROR: {e}")
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
        print("✅ ส่ง reply สำเร็จ!")
    except Exception as e:
        print(f"❌ Error ส่ง reply: {e}")

if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
