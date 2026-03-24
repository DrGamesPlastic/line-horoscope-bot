"""
🔮 โหราศาสตร์ไทย + นักษัตรจีน
ดูดวงจากวันเดือนปีเกิด
"""

import random
from datetime import datetime, date


# ─── ราศีไทย (12 ราศี) ───
THAI_ZODIAC = [
    {"name": "♈ เมษ", "name_th": "เมษ", "start": (3, 21), "end": (4, 19),
     "element": "ไฟ", "planet": "อังคาร",
     "traits": "กล้าหาญ มุ่งมั่น เป็นผู้นำ แต่ใจร้อน"},
    {"name": " พฤษภ", "name_th": "พฤษภ", "start": (4, 20), "end": (5, 20),
     "element": "ดิน", "planet": "ศุกร์",
     "traits": "อดทน หนักแน่น รักสวยรักงาม แต่ดื้อรั้น"},
    {"name": "♊ เมถุน", "name_th": "เมถุน", "start": (5, 21), "end": (6, 21),
     "element": "ลม", "planet": "พุธ",
     "traits": "ช่างพูด ปรับตัวเก่ง ฉลาด แต่เบื่อง่าย"},
    {"name": "♋ กรกฎ", "name_th": "กรกฎ", "start": (6, 22), "end": (7, 22),
     "element": "น้ำ", "planet": "จันทร์",
     "traits": "อบอุ่น ดูแลคนอื่น จินตนาการสูง แต่อ่อนไหวง่าย"},
    {"name": "♌ สิงห์", "name_th": "สิงห์", "start": (7, 23), "end": (8, 22),
     "element": "ไฟ", "planet": "อาทิตย์",
     "traits": "มั่นใจ ใจกว้าง มีเสน่ห์ แต่ชอบเป็นจุดเด่น"},
    {"name": "♍ กันย์", "name_th": "กันย์", "start": (8, 23), "end": (9, 22),
     "element": "ดิน", "planet": "พุธ",
     "traits": "ละเอียด ขยัน วิเคราะห์เก่ง แต่จู้จี้"},
    {"name": "♎ ตุลย์", "name_th": "ตุลย์", "start": (9, 23), "end": (10, 22),
     "element": "ลม", "planet": "ศุกร์",
     "traits": "ยุติธรรม มีศิลปะ น่าคบหา แต่ตัดสินใจยาก"},
    {"name": "♏ พิจิก", "name_th": "พิจิก", "start": (10, 23), "end": (11, 21),
     "element": "น้ำ", "planet": "อังคาร+พลูโต",
     "traits": "ลึกลับ แข็งแกร่ง มีพลัง แต่ขี้หึง"},
    {"name": "♐ ธนู", "name_th": "ธนู", "start": (11, 22), "end": (12, 21),
     "element": "ไฟ", "planet": "พฤหัสบดี",
     "traits": "รักอิสระ มองโลกแง่ดี ผจญภัย แต่ไม่รอบคอบ"},
    {"name": "♑ มังกร", "name_th": "มกร", "start": (12, 22), "end": (1, 19),
     "element": "ดิน", "planet": "เสาร์",
     "traits": "มุ่งมั่น รับผิดชอบ มีวินัย แต่เครียดง่าย"},
    {"name": "♒ กุมภ์", "name_th": "กุมภ์", "start": (1, 20), "end": (2, 18),
     "element": "ลม", "planet": "เสาร์+ยูเรนัส",
     "traits": "สร้างสรรค์ คิดต่าง มีอุดมการณ์ แต่หัวดื้อ"},
    {"name": "♓ มีน", "name_th": "มีน", "start": (2, 19), "end": (3, 20),
     "element": "น้ำ", "planet": "พฤหัสบดี+เนปจูน",
     "traits": "อ่อนโยน มีเมตตา จินตนาการสูง แต่ไม่ค่อยหนักแน่น"},
]

# ─── นักษัตรจีน (12 ปี) ───
CHINESE_ZODIAC = [
    {"name": "🐀 ชวด (หนู)", "years_mod": 4, "element": "น้ำหยิน",
     "traits": "ฉลาด คล่องแคล่ว ปรับตัวเก่ง ช่างสังเกต"},
    {"name": "🐂 ฉลู (วัว)", "years_mod": 5, "element": "ดินหยิน",
     "traits": "ขยัน อดทน ซื่อสัตย์ หนักแน่น"},
    {"name": "🐅 ขาล (เสือ)", "years_mod": 6, "element": "ไม้หยาง",
     "traits": "กล้าหาญ มีอำนาจ ชอบแข่งขัน ผู้นำโดยธรรมชาติ"},
    {"name": "🐈 เถาะ (กระต่าย)", "years_mod": 7, "element": "ไม้หยิน",
     "traits": "อ่อนโยน สุภาพ ฉลาด มีรสนิยม"},
    {"name": "🐉 มะโรง (งูใหญ่/มังกร)", "years_mod": 8, "element": "ดินหยาง",
     "traits": "สง่างาม มีบารมี มั่นใจ โชคดี"},
    {"name": "🐍 มะเส็ง (งู)", "years_mod": 9, "element": "ไฟหยิน",
     "traits": "ลึซึ้ง ฉลาด สง่างาม มีสัญชาตญาณดี"},
    {"name": "🐴 มะเมีย (ม้า)", "years_mod": 10, "element": "ไฟหยาง",
     "traits": "กระตือรือร้น อิสระ แข่งขันเก่ง ร่าเริง"},
    {"name": "🐐 มะแม (แพะ)", "years_mod": 11, "element": "ดินหยิน",
     "traits": "อ่อนโยน ศิลปะ มีเมตตา สงบสุข"},
    {"name": "🐵 วอก (ลิง)", "years_mod": 0, "element": "ทองหยาง",
     "traits": "ฉลาด ขี้เล่น สร้างสรรค์ แก้ปัญหาเก่ง"},
    {"name": "🐔 ระกา (ไก่)", "years_mod": 1, "element": "ทองหยิน",
     "traits": "ตรงไปตรงมา ขยัน มั่นใจ ใส่ใจรายละเอียด"},
    {"name": "🐕 จอ (สุนัข)", "years_mod": 2, "element": "ดินหยาง",
     "traits": "ซื่อสัตย์ ยุติธรรม ปกป้องคนที่รัก จริงใจ"},
    {"name": "🐷 กุน (หมู)", "years_mod": 3, "element": "น้ำหยาง",
     "traits": "ใจกว้าง ซื่อสัตย์ สนุกสนาน ใจดี"},
]

# ─── สีมงคลตามราศี ───
LUCKY_COLORS = {
    "เมษ": ["🔴 แดง", "🟠 ส้ม", "🟡 ทอง"],
    "พฤษภ": ["🟢 เขียว", "🩷 ชมพู", "🤍 ขาว"],
    "เมถุน": ["🟡 เหลือง", "🟢 เขียว", "🩵 ฟ้า"],
    "กรกฎ": ["⚪ ขาว", "🩶 เงิน", "🔵 น้ำเงิน"],
    "สิงห์": ["🟡 ทอง", "🟠 ส้ม", "🔴 แดง"],
    "กันย์": ["🟢 เขียว", "🤎 น้ำตาล", "🤍 ขาว"],
    "ตุลย์": ["🩷 ชมพู", "🔵 น้ำเงิน", "🤍 ขาว"],
    "พิจิก": ["🔴 แดงเข้ม", "⚫ ดำ", "🟤 น้ำตาลเข้ม"],
    "ธนู": ["🟣 ม่วง", "🔵 น้ำเงิน", "🟢 เขียว"],
    "มกร": ["⚫ ดำ", "🤎 น้ำตาล", "🤍 ขาว"],
    "กุมภ์": ["🔵 น้ำเงิน", "🟢 เขียวอมฟ้า", "🟣 ม่วง"],
    "มีน": ["🟢 เขียวทะเล", "🟣 ม่วง", "🩵 ฟ้าอ่อน"],
}

# ─── เลขมงคลตามวันเกิด ───
def get_lucky_numbers(birth_date: date) -> list[int]:
    """เลขมงคลจากวันเกิด"""
    day = birth_date.day
    total = sum(int(d) for d in str(day))
    while total > 9:
        total = sum(int(d) for d in str(total))
    nums = set()
    nums.add(day % 10 or 10)
    nums.add(total)
    nums.add((day + birth_date.month) % 10 or 10)
    nums.add((birth_date.year % 100) % 10 or 10)
    return sorted(nums)


# ─── ทำนายดวง ───
FORTUNES = {
    "การงาน": [
        "ช่วงนี้มีโอกาสได้รับมอบหมายงานสำคัญ 💼",
        "ระวังปัญหากับเพื่อนร่วมงาน ใจเย็นๆ ไว้ 🤝",
        "โอกาสเลื่อนตำแหน่งกำลังมา อดทนรออีกนิด ⭐",
        "เหมาะกับการเริ่มต้นโปรเจกต์ใหม่ 🚀",
        "งานหนักช่วงนี้จะส่งผลดีในอนาคต 📈",
        "มีผู้ใหญ่สนับสนุนในหน้าที่การงาน 🙏",
        "ระวังการตัดสินใจด่วนในงาน คิดให้ดีก่อน 🤔",
        "งานที่ทำอยู่จะสำเร็จตามเป้าหมาย 🎯",
    ],
    "การเงิน": [
        "การเงินมั่นคงดี มีโอกาสได้โชคลาภ 💰",
        "ระวังค่าใช้จ่ายไม่คาดฝัน วางแผนการเงินดีๆ 💸",
        "มีโอกาสรับรายได้เสริมจากช่องทางใหม่ 💵",
        "ช่วงนี้เหมาะกับการลงทุนระยะยาว 📊",
        "เงินก้อนเล็กจะงอกเงยเป็นก้อนใหญ่ 🌱",
        "อย่าเพิ่งให้ใครยืมเงินช่วงนี้ ⚠️",
        "มีเกณฑ์ได้ของขวัญหรือของมีค่า 🎁",
        "การเงินราบรื่น มีเหลือเก็บ 💎",
    ],
    "ความรัก": [
        "คนโสดมีโอกาสเจอคนถูกใจจากที่ทำงาน 💕",
        "คนมีคู่แล้ว ความสัมพันธ์ดีขึ้น หวานกว่าเดิม 💗",
        "ระวังความเข้าใจผิดเล็กๆ กับคนรัก 💬",
        "คนที่แอบชอบอยู่อาจมีใจให้เหมือนกัน 💝",
        "ช่วงนี้เหมาะกับการสารภาพรัก 💌",
        "ความรักกำลังเบ่งบาน ดูแลมันให้ดี 🌹",
        "โสดก็ดี มีความสุขกับตัวเองก่อน 🧘",
        "จะมีคนเข้ามาในชีวิตอย่างไม่คาดคิด 💫",
    ],
    "สุขภาพ": [
        "สุขภาพแข็งแรงดี แต่อย่าลืมออกกำลังกาย 💪",
        "ระวังอาการปวดหลังจากการนั่งนานๆ 🪑",
        "นอนพักผ่อนให้เพียงพอ สุขภาพดีขึ้นแน่นอน 😴",
        "ดื่มน้ำเยอะๆ ระวังอาการขาดน้ำ 💧",
        "สุขภาพจิตดี ร่างกายก็ดีตาม 🧠",
        "ระวังอุบัติเหตุเล็กๆ ขับรถด้วยความระมัดระวัง 🚗",
        "เป็นช่วงที่เหมาะกับการตรวจสุขภาพ 🏥",
        "ออกกำลังกายสม่ำเสมอ สุขภาพจะดีมาก 🏃",
    ],
}

# ─── ดวงประจำวัน ───
def get_daily_fortune(zodiac_index: int) -> str:
    """ทำนายดวงประจำวัน"""
    today = date.today()
    # ใช้วันที่ + index ราศีเป็น seed เพื่อให้ผลลัพธ์คงที่ต่อวัน
    seed = int(today.strftime("%Y%m%d")) + zodiac_index * 7
    rng = random.Random(seed)
    
    score = rng.randint(1, 100)
    if score >= 80:
        level = "🌟 ดีมาก"
    elif score >= 60:
        level = "✨ ดี"
    elif score >= 40:
        level = "😐 ปานกลาง"
    else:
        level = "⚠️ ระวัง"
    
    work = rng.choice(FORTUNES["การงาน"])
    money = rng.choice(FORTUNES["การเงิน"])
    love = rng.choice(FORTUNES["ความรัก"])
    health = rng.choice(FORTUNES["สุขภาพ"])
    
    return (
        f"📊 คะแนนดวงวันนี้: {score}/100 ({level})\n\n"
        f"💼 การงาน: {work}\n\n"
        f"💰 การเงิน: {money}\n\n"
        f"❤️ ความรัก: {love}\n\n"
        f"🏥 สุขภาพ: {health}"
    )


# ─── ฟังก์ชันหลัก ───
def get_thai_zodiac(birth_date: date) -> dict:
    """หาราศีจากวันเกิด"""
    m, d = birth_date.month, birth_date.day
    for z in THAI_ZODIAC:
        sm, sd = z["start"]
        em, ed = z["end"]
        if sm <= em:  # ปกติ (ไม่ข้ามปี)
            if (m == sm and d >= sd) or (m == em and d <= ed) or (sm < m < em):
                return z
        else:  # ข้ามปี (มังกร)
            if (m == sm and d >= sd) or (m == em and d <= ed) or (m > sm or m < em):
                return z
    return THAI_ZODIAC[0]


def get_chinese_zodiac(birth_year: int) -> dict:
    """หานักษัตรจีนจากปีเกิด"""
    # ปีชวดเริ่มที่ 1984 (4 mod 12)
    index = (birth_year - 4) % 12
    return CHINESE_ZODIAC[index]


def get_lucky_colors(zodiac_name: str) -> list[str]:
    """หาสีมงคล"""
    for key in LUCKY_COLORS:
        if key in zodiac_name:
            return LUCKY_COLORS[key]
    return ["🟢 เขียว", "🤍 ขาว", "🟡 ทอง"]


def format_horoscope(birth_date: date) -> str:
    """จัดรูปแบบดวงทั้งหมด"""
    thai_z = get_thai_zodiac(birth_date)
    chinese_z = get_chinese_zodiac(birth_date.year)
    lucky_nums = get_lucky_numbers(birth_date)
    lucky_cols = get_lucky_colors(thai_z["name_th"])
    daily = get_daily_fortune(THAI_ZODIAC.index(thai_z))
    
    result = (
        f"🔮 ผลคำทำนายดวงชะตา\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"📅 วันเกิด: {birth_date.strftime('%d/%m/%Y')}\n\n"
        
        f"✨ ราศี: {thai_z['name']}\n"
        f"   ธาตุ: {thai_z['element']} | ดาวประจำราศี: {thai_z['planet']}\n"
        f"   ลักษณะเด่น: {thai_z['traits']}\n\n"
        
        f"🐲 นักษัตรจีน: {chinese_z['name']}\n"
        f"   ธาตุ: {chinese_z['element']}\n"
        f"   ลักษณะเด่น: {chinese_z['traits']}\n\n"
        
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"🍀 เลขนำโชค: {', '.join(str(n) for n in lucky_nums)}\n"
        f"🎨 สีมงคล: {', '.join(lucky_cols)}\n"
        
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"📅 ดวงประจำวัน ({date.today().strftime('%d/%m/%Y')})\n\n"
        f"{daily}\n\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"⚠️ เป็นความเชื่อส่วนบุคคล โปรดใช้วิจารณญาณ 🙏"
    )
    return result


def parse_date(text: str) -> date | None:
    """แปลงข้อความวันเกิดเป็น date object"""
    formats = [
        "%d/%m/%Y",   # 25/12/1995
        "%d-%m-%Y",   # 25-12-1995
        "%d %m %Y",   # 25 12 1995
        "%Y/%m/%d",   # 1995/12/25
        "%Y-%m-%d",   # 1995-12-25
    ]
    text = text.strip()
    for fmt in formats:
        try:
            d = datetime.strptime(text, fmt).date()
            # แปลงปี พ.ศ. → ค.ศ. ถ้าปีมากกว่า 2500
            if d.year > 2500:
                d = d.replace(year=d.year - 543)
            return d
        except ValueError:
            continue
    
    # ลองแยกด้วย / หรือ - หรือ ช่องว่าง
    for sep in ["/", "-", " "]:
        parts = text.split(sep)
        if len(parts) == 3:
            try:
                d, m, y = int(parts[0]), int(parts[1]), int(parts[2])
                if y < 100:
                    y += 2500 if y < 50 else 1900  # รองรับปี พ.ศ.
                if y > 2500:
                    y -= 543  # แปลง พ.ศ. → ค.ศ.
                if 1 <= d <= 31 and 1 <= m <= 12 and 1900 <= y <= 2100:
                    return date(y, m, d)
            except (ValueError, IndexError):
                continue
    return None
