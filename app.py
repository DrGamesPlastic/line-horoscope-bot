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

print(f"🔑 Channel Secret: {CHANNEL_SECRET[:8]}...")
print(f"🔑 Access Token: {CHANNEL_ACCESS_TOKEN[:20]}...")

configuration = Configuration(access_token=CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(CHANNEL_SECRET)


# ─── Webhook Endpoint ───
@app.route("/callback", methods=["POST"])
def callback():
    signature = request.headers.get("X-Line-Signature", "")
    body = request.get_data(as_text=True)
    
    print(f"📩 ได้รับ webhook: {body[:200]}...")
    
    try:
        handler.handle(body, signature)
        print("✅ Handler handle สำเร็จ")
    except InvalidSignatureError:
        print("❌ Invalid Signature!")
        return jsonify({"error": "Invalid signature"}), 400
    except Exception as e:
        print(f"❌ Handler error: {e}")
        traceback.print_exc()
        # ยัง return 200 เพื่อไม่ให้ LINE retry
        return "OK", 200
    
    return "OK", 200


# ─── Health Check ───
@app.route("/", methods=["GET"])
def health():
    return "🔮 บอทดูดวงกำลังทำงานอยู่!"


# ─── Debug: log all events ───
@handler.add(MessageEvent)
def handle_all_events(event):
    print(f"📨 Event received: type={event.type}, message_type={getattr(event.message, 'type', 'N/A')}")


# ─── Message Handler ───
@handler.add(MessageEvent, message=TextMessageContent)
def handle_text_message(event):
    user_text = event.message.text.strip()
    print(f"📩 ได้รับข้อความ: '{user_text}' จาก {event.source.user_id}")
    
    try:
        # ── คำสั่งพิเศษ ──
        if user_text in ["/help", "ช่วยเหลือ", "help", "วิธีใช้"]:
            reply = (
                "🔮 วิธีใช้บอทดูดวง\n"
                "━━━━━━━━━━━━━━━━━━━━\n\n"
                "📝 ส่งวันเกิดมาได้เลย เช่น:\n"
                "   • 25/12/2538\n"
                "   • 15-03-1990\n"
                "   • 1/1/2540\n\n"
                "✨ ฟีเจอร์ทั้งหมด:\n"
                "   🔮 ดูดวงทั่วไป — ส่งวันเกิด\n"
                "   🃏 ไพ่ทาโรต์ — พิมพ์ \"ไพ่\" + วันเกิด\n"
                "   💕 ดวงความรัก — พิมพ์ \"รัก\" + วันเกิด\n"
                "   🐉 ดวงจีนเต็ม — พิมพ์ \"จีน\" + วันเกิด\n\n"
                "━━━━━━━━━━━━━━━━━━━━\n"
                "🦐 สร้างโดย น้องกุ้ง"
            )
            send_reply(event.reply_token, reply)
            return
        
        # ── คำสั่งไพ่ทาโรต์ ──
        if user_text.startswith("ไพ่") or user_text.lower().startswith("tarot"):
            date_text = user_text[2:].strip() if user_text.startswith("ไพ่") else user_text[5:].strip()
            birth_date = parse_date(date_text)
            if birth_date:
                reading = get_tarot_reading(birth_date)
                send_reply(event.reply_token, reading)
            else:
                send_reply(event.reply_token, 
                    "🃏 ส่งวันเกิดมาด้วยครับ เช่น:\n"
                    "   • ไพ่ 25/12/2538\n"
                    "   • tarot 15-03-1990")
            return
        
        # ── คำสั่งดูดวงความรัก ──
        if user_text.startswith("รัก") or user_text.lower().startswith("love"):
            date_text = user_text[2:].strip() if user_text.startswith("รัก") else user_text[4:].strip()
            birth_date = parse_date(date_text)
            if birth_date:
                reading = format_love_reading(birth_date)
                send_reply(event.reply_token, reading)
            else:
                send_reply(event.reply_token,
                    "💕 ส่งวันเกิดมาด้วยครับ เช่น:\n"
                    "   • รัก 25/12/2538\n"
                    "   • love 15-03-1990")
            return
        
        # ── คำสั่งดูดวงจีนเต็ม ──
        if user_text.startswith("จีน") or user_text.lower().startswith("chinese"):
            date_text = user_text[2:].strip() if user_text.startswith("จีน") else user_text[7:].strip()
            birth_date = parse_date(date_text)
            if birth_date:
                reading = format_full_chinese_horoscope(birth_date)
                send_reply(event.reply_token, reading)
            else:
                send_reply(event.reply_token,
                    "🐉 ส่งวันเกิดมาด้วยครับ เช่น:\n"
                    "   • จีน 25/12/2538\n"
                    "   • chinese 15-03-1990")
            return
        
        # ── ดูดวงทั่วไป (จากวันเกิด) ──
        birth_date = parse_date(user_text)
        print(f"📅 แปลงวันเกิด: {user_text} → {birth_date}")
        
        if birth_date:
            horoscope = format_horoscope(birth_date)
            send_reply(event.reply_token, horoscope)
        else:
            reply = (
                "🤔 ไม่เข้าใจรูปแบบวันเกิดครับ\n\n"
                "📝 กรุณาส่งในรูปแบบ:\n"
                "   • วัน/เดือน/ปี เช่น 25/12/2538\n"
                "   • วัน-เดือน-ปี เช่น 15-03-1990\n\n"
                "💡 หรือพิมพ์ 'ช่วยเหลือ' เพื่อดูวิธีใช้"
            )
            send_reply(event.reply_token, reply)
    except Exception as e:
        print(f"❌ ERROR ใน handle_message: {e}")
        traceback.print_exc()


def send_reply(reply_token: str, text: str):
    """ส่งข้อความตอบกลับ"""
    try:
        with ApiClient(configuration) as api_client:
            line_bot_api = MessagingApi(api_client)
            line_bot_api.reply_message(
                ReplyMessageRequest(
                    reply_token=reply_token,
                    messages=[TextMessage(text=text)]
                )
            )
        print(f"✅ ส่ง reply สำเร็จ!")
    except ApiException as e:
        print(f"❌ LINE API Error: {e.status} - {e.reason}")
        traceback.print_exc()
    except Exception as e:
        print(f"❌ ERROR ส่ง reply: {e}")
        traceback.print_exc()


# ─── Run Server ───
if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    print(f"🔮 บอทดูดวงเริ่มทำงานที่ port {port}")
    app.run(host="0.0.0.0", port=port, debug=False)
