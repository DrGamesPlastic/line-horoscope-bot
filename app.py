"""
🔮 LINE Horoscope Bot - บอทดูดวง
หมอเกมส์  (Master Tarot & Saju Edition)
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

@handler.add(MessageEvent)
def handle_all_events(event):
    if hasattr(event, 'message'):
        print(f"📨 Event: {event.type}, Msg: {getattr(event.message, 'type', 'N/A')}")

@handler.add(MessageEvent, message=TextMessageContent)
def handle_text_message(event):
    raw_text = event.message.text.strip()
    user_text_lower = raw_text.lower()
    
    print(f"📩 ได้รับข้อความ: '{raw_text}'")
    
    try:
        # 1. เช็กคำสั่งช่วยเหลือ
        if user_text_lower in ["/help", "ช่วยเหลือ", "help", "วิธีใช้"]:
            reply = (
                "🔮 วิธีใช้บอทดูดวง หมอเกมส์ x น้องกุ้ง!\n"
                "━━━━━━━━━━━━━━━━━━━━\n"
                "🌟 พิมพ์ 'วันเกิด' เพื่อดูดวงราศี\n"
                "   (เช่น: 25/12/2535)\n\n"
                "✨ เมนูคำสั่งพิเศษ (พิมพ์คีย์เวิร์ด + วันเกิด):\n"
                "📅 'ดวง' + วันเกิด -> ดวงรายวัน\n"
                "🇰🇷 'ซาจู' + วันเกิด -> วิเคราะห์ธาตุซาจูเกาหลี\n"
                "🃏 'ไพ่' -> อธิษฐานเลือกเลข 1-78\n"
                "💕 'รัก' + วันเกิด -> ดูดวงความรัก\n"
                "🐉 'จีน' + วันเกิด -> ดูดวงจีนเต็ม\n"
                "━━━━━━━━━━━━━━━━━━━━"
            )
            send_reply(event.reply_token, reply)
            return

        # 2. คัดกรองโหมดพิเศษ (ที่ไม่ต้องใช้ระบบวันที่แบบปกติ)
        
        # --- หมวด "ไพ่ทาโรต์" ---
        if raw_text.startswith("ไพ่") or user_text_lower.startswith("tarot"):
            num_part = raw_text.replace("ไพ่", "").replace("tarot", "").replace("Tarot", "").strip()
            if not num_part:  # พิมพ์แค่ "ไพ่"
                reply = (
                    "🃏 **ตั้งจิตอธิษฐานให้สงบ**\n"
                    "แล้วเลือกตัวเลขที่ชอบที่สุด\n"
                    "จาก **1 ถึง 78**\n\n"
                    "📥 **พิมพ์ตอบกลับมาว่า:**\n"
                    "เลือก [หมายเลข]\n"
                    "(ตัวอย่าง: เลือก 77)"
                )
                send_reply(event.reply_token, reply)
                return
            elif num_part.isdigit():  # พิมพ์ "ไพ่ 7"
                response = get_tarot_reading_by_number(int(num_part))
                send_reply(event.reply_token, response)
                return

        # --- หมวด "เลือก" (จากเมนูไพ่) ---
        elif raw_text.startswith("เลือก"):
            num_part = raw_text.replace("เลือก", "").strip()
            if num_part.isdigit():
                response = get_tarot_reading_by_number(int(num_part))
                send_reply(event.reply_token, response)
                return

        # 3. หมวดหมู่ที่ต้องประมวลผล "วันที่"
        mode = "general"
        clean_date = raw_text

        if raw_text.startswith("ดวง") or user_text_lower.startswith("today"):
            mode = "daily"
            clean_date = raw_text.replace("ดวง", "").replace("today", "").replace("Today", "").strip()
        elif raw_text.startswith("ซาจู") or user_text_lower.startswith("saju"):
            mode = "saju"
            clean_date = raw_text.replace("ซาจู", "").replace("saju", "").replace("Saju", "").strip()
        elif raw_text.startswith("รัก") or user_text_lower.startswith("love"):
            mode = "love"
            clean_date = raw_text.replace("รัก", "").replace("love", "").replace("Love", "").strip()
        elif raw_text.startswith("จีน") or user_text_lower.startswith("chinese"):
            mode = "chinese"
            clean_date = raw_text.replace("จีน", "").replace("chinese", "").replace("Chinese", "").strip()

        # ประมวลผลวันที่จากข้อความที่เหลือ
        birth_date = parse_date(clean_date)
        
        if birth_date:
            if mode == "daily":
                response = get_daily_horoscope(birth_date)
            elif mode == "saju":
                response = get_saju_reading(birth_date)
            elif mode == "love":
                response = format_love_reading(birth_date)
            elif mode == "chinese":
                response = format_full_chinese_horoscope(birth_date)
            else:
                response = format_horoscope(birth_date)
            
            send_reply(event.reply_token, response)
        else:
            # ถ้าพิมพ์อะไรมาไม่รู้และไม่ใช่รูปแบบวันที่
            if mode != "general":
                send_reply(event.reply_token, f"❌ รูปแบบวันที่ '{clean_date}' ไม่ถูกต้องครับ\nตัวอย่าง: {mode} 10/06/1973")
            # ถ้าเป็นข้อความทั่วไป บอทจะไม่ตอบเพื่อป้องกันการสแปม หรือเปิดใช้บรรทัดล่างเพื่อตอบกลับ
            # else:
            #    send_reply(event.reply_token, "🤔 ไม่เข้าใจคำสั่งครับ พิมพ์ 'วิธีใช้' เพื่อดูเมนู")

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
        print("✅ ส่ง reply สำเร็จ!")
    except Exception as e:
        print(f"❌ Error ส่ง reply: {e}")

if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
