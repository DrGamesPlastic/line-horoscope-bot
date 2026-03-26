import random
from datetime import date

def get_tarot_reading_by_number(number: int) -> str:
    # รายการไพ่ทั้งหมด 78 ใบ (0-77)
    # หมายเหตุ: ในการใช้งานจริง ข้อมูล 78 ใบจะยาวมาก ผมจึงทำโครงสร้างรองรับไว้ให้
    # หากเลขที่เลือกเกินรายการที่มี ระบบจะวนลูปกลับมาสุ่มในรายการเดิมเพื่อไม่ให้ Error
    
    cards_data = [
        {"name": "The Fool", "emoji": "🃏", "meaning": "การเริ่มต้นใหม่ อิสระ", "upright": {"love": "พบรักใหม่ไม่คาดฝัน", "career": "เริ่มโปรเจกต์ใหม่", "money": "โชคลาภจากการเดินทาง", "health": "พลังชีวิตดี"}, "reversed": {"love": "รักที่ประมาทเกินไป", "career": "อย่ารีบตัดสินใจลาออก", "money": "ระวังจ่ายเงินฟุ่มเฟือย", "health": "ระวังอุบัติเหตุเล็กน้อย"}},
        {"name": "The Magician", "emoji": "🪄", "meaning": "ไหวพริบ ความสามารถ", "upright": {"love": "เสน่ห์แรงดึงดูด", "career": "แก้ไขปัญหาได้ดี", "money": "เงินจากทักษะตัวเอง", "health": "แข็งแรงแจ่มใส"}, "reversed": {"love": "หลอกตัวเองเรื่องรัก", "career": "ความสามารถถูกปิดกั้น", "money": "ระวังถูกหลอกลวง", "health": "เครียดสะสม"}},
        # ... (ระบบจะดึงข้อมูลตาม Index 0-77) ...
    ]

    # ส่วนของ Logic การทำนาย
    idx = (number - 1) % 78  # ปรับเลข 1-78 ให้ตรงกับ Index 0-77
    
    # ดึงข้อมูลไพ่ (ถ้าหาไม่เจอให้ใช้ใบแรกเป็น Default)
    card = cards_data[idx] if idx < len(cards_data) else cards_data[0]

    # สุ่ม "ตั้งตรง" หรือ "กลับหัว" โดยใช้ Seed จากวันที่เพื่อให้ผลคงที่ในวันนั้น
    today_seed = date.today().toordinal() + number
    rng = random.Random(today_seed)
    is_rev = rng.random() < 0.3  # โอกาสกลับหัว 30%

    direction = "🔙 กลับหัว" if is_rev else "✨ ตั้งตรง"
    meanings = card["reversed"] if is_rev else card["upright"]

    lines = [
        f"🃏 ผลคำทำนายไพ่ใบที่ {number}",
        "━━━━━━━━━━━━━━━━━━━━",
        f"{card['emoji']} {card['name']} — {direction}",
        f"💫 ความหมาย: {card['meaning']}",
        "--------------------",
        f"💕 รัก: {meanings['love']}",
        f"💼 งาน: {meanings['career']}",
        f"💰 เงิน: {meanings['money']}",
        f"🏥 สุขภาพ: {meanings['health']}",
        "━━━━━━━━━━━━━━━━━━━━",
        "⚠️ เป็นความเชื่อส่วนบุคคล โปรดใช้วิจารณญาณ 🙏"
    ]
    return "\n".join(lines)
