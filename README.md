# 🔮 LINE Bot ดูดวง

บอทดูดวงสำหรับคนไทย ดูดวงจากวันเดือนปีเกิด ผ่าน LINE Messaging API

สร้างโดย **หมอเกมส์** x **น้องกุ้ง** 🦐

---

## ✨ ฟีเจอร์

- 🔮 **ดูดวงตามราศี** (12 ราศี) — ลักษณะนิสัย, ธาตุ, ดาวประจำราศี
- 🐲 **ดูดวงตามนักษัตรจีน** (12 นักษัตร) — ธาตุ, ลักษณะเด่น
- 🍀 **เลขนำโชค** — คำนวณจากวันเกิด
- 🎨 **สีมงคล** — ประจำราศี
- 📊 **ดวงประจำวัน** — การงาน, การเงิน, ความรัก, สุขภาพ

---

## 🚀 วิธีติดตั้ง

### ขั้นตอนที่ 1: สร้าง LINE Bot

1. ไปที่ [developers.line.biz](https://developers.line.biz)
2. ล็อกอินด้วยบัญชี LINE
3. สร้าง **Provider** → ตั้งชื่ออะไรก็ได้ (เช่น "ดูดวง Bot")
4. สร้าง **Messaging API Channel**
5. จด **Channel Secret** (อยู่ในแท็บ Basic settings)
6. สร้าง **Channel Access Token** (อยู่ในแท็บ Messaging API → Issue)

### ขั้นตอนที่ 2: ตั้งค่าโปรเจกต์

```bash
# ติดตั้ง dependencies
pip install -r requirements.txt

# คัดลอกไฟล์ config
cp .env.example .env

# แก้ไข .env ใส่ค่าจาก LINE Developers
# LINE_CHANNEL_SECRET=xxxxx
# LINE_CHANNEL_ACCESS_TOKEN=xxxxx
```

### ขั้นตอนที่ 3: รันเซิร์ฟเวอร์

```bash
# รันแบบ local (development)
python app.py
```

### ขั้นตอนที่ 4: ทำให้เข้าถึงจากอินเทอร์เน็ต

LINE ต้องส่ง webhook มาที่เซิร์ฟเวอร์เรา ต้องมี public URL:

**ตัวเลือก A: ngrok (ทดลองใช้)**
```bash
# ติดตั้ง ngrok
# ไปที่ https://ngrok.com สมัครฟรี
ngrok http 5000

# จะได้ URL เช่น https://abc123.ngrok.io
```

**ตัวเลือก B: Deploy ฟรีบน Render.com**
1. Push โค้ดขึ้น GitHub
2. ไปที่ [render.com](https://render.com) → New Web Service
3. เชื่อม GitHub repo
4. ตั้งค่า:
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `gunicorn app:app`
5. ตั้งค่า Environment Variables (LINE_CHANNEL_SECRET, LINE_CHANNEL_ACCESS_TOKEN)

### ขั้นตอนที่ 5: ตั้งค่า Webhook ใน LINE

1. กลับไปที่ LINE Developers Console
2. ไปที่ Messaging API tab
3. ใส่ **Webhook URL**: `https://your-domain.com/callback`
4. เปิด **Use webhook**
5. ปิด **Auto-reply messages** (ใน LINE Official Account Manager)

---

## 📁 โครงสร้างโปรเจกต์

```
line-horoscope-bot/
├── app.py              # Flask app + LINE webhook handler
├── horoscope.py        # โหราศาสตร์: ราศี, นักษัตร, ทำนาย
├── requirements.txt    # Python dependencies
├── .env.example        # ตัวอย่าง config
├── .env                # config จริง (ไม่ commit)
└── README.md           # เอกสาร
```

## 🧪 ทดสอบ

ส่งข้อความใน LINE:
- `25/12/2538` → ดูดวง
- `15-03-1990` → ดูดวง
- `ช่วยเหลือ` → แสดงวิธีใช้

---

## ⚠️ หมายเหตุ

- ทำนายเป็นความบันเทิง โปรดใช้วิจารณญาณ 🙏
- รองรับทั้งปี พ.ศ. และ ค.ศ.
- ดวงประจำวันเปลี่ยนทุกวัน (seed จากวันที่)
