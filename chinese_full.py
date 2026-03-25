"""
🐉 ดูดวงจีนเต็ม (Full Chinese Horoscope)
หมอเกมส์ x น้องกุ้ง 🦐
"""

from datetime import date
import random

# ─── 10 ธาตุฟ้า (Heavenly Stems) ───
HEAVENLY_STEMS = [
    {"name": "甲 จี่ (ไม้หยาง)", "element": "ไม้หยาง", "traits": "มั่นคง แข็งแรง ต้นไม้ใหญ่ ผู้นำธรรมชาติ"},
    {"name": "乙 อี่ (ไม้หยิน)", "element": "ไม้หยิน", "traits": "อ่อนโยน ยืดหยุ่น หญ้า ดอกไม้ ปรับตัวเก่ง"},
    {"name": "丙 ปิ่ง (ไฟหยาง)", "element": "ไฟหยาง", "traits": "ร้อนแรง สว่างสดใส แสงอาทิตย์ มีพลังดึงดูด"},
    {"name": "丁 ติ้ง (ไฟหยิน)", "element": "ไฟหยิน", "traits": "อบอุ่น แสงเทียน ลึกซึ้ง มีเสน่ห์ในความสงบ"},
    {"name": "戊 อู่ (ดินหยาง)", "element": "ดินหยาง", "traits": "หนักแน่น ภูเขา มั่นคง น่าเชื่อถือ"},
    {"name": "己 จี่ (ดินหยิน)", "element": "ดินหยิน", "traits": "สวนดอกไม้ สวยงาม อุดมสมบูรณ์ ดูแลเก่ง"},
    {"name": "庚 เกิ่ง (ทองหยาง)", "element": "ทองหยาง", "traits": "คม แข็ง ดาบ ตรงไปตรงมา มีอำนาจ"},
    {"name": "辛 ซิน (ทองหยิน)", "element": "ทองหยิน", "traits": "ประณีต อัญมณี ฉลาด มีรสนิยม"},
    {"name": "壬 เหริน (น้ำหยาง)", "element": "น้ำหยาง", "traits": "มหาสมุทร ลึกซึ้ง ปัญญาสูง ปรับตัวเก่ง"},
    {"name": "癸 กุ้ย (น้ำหยิน)", "element": "น้ำหยิน", "traits": "ฝน น้ำค้าง อ่อนโยน สัญชาตญาณดี"},
]

# ─── 12 ราศีจีน (Earthly Branches) ───
EARTHLY_BRANCHES = [
    {"name": "子 จื่อ (ชวด/หนู)", "animal": "🐀 ชวด", "time": "23:00-01:00", "month": "ธันวาคม",
     "element": "น้ำหยิน", "yin_yang": "หยาง",
     "traits_detailed": "ฉลาดที่สุดในบรรดา 12 นักษัตร ช่างสังเกต ปรับตัวเก่ง มีไหวพริบ",
     "strengths": ["ฉลาดแกมโกง", "ปรับตัวเร็ว", "เก็บเงินเก่ง", "มีเสน่ห์"],
     "weaknesses": ["ขี้กังวล", "ชอบวิจารณ์", "บางครั้งเห็นแก่ตัว", "ขี้หึง"],
     "careers": "นักธุรกิจ นักเขียน นักการเมือง ผู้สื่อข่าว",
     "famous": "Shakespeare, George Washington"},
    {"name": "丑 เฉี่ยว (ฉลู/วัว)", "animal": "🐂 ฉลู", "time": "01:00-03:00", "month": "มกราคม",
     "element": "ดินหยิน", "yin_yang": "หยิน",
     "traits_detailed": "ขยันที่สุด อดทน ซื่อสัตย์ หนักแน่น เชื่อถือได้",
     "strengths": ["อดทนสูง", "ซื่อสัตย์", "ทำงานหนัก", "น่าเชื่อถือ"],
     "weaknesses": ["ดื้อรั้น", "ไม่ค่อยพูด", "โกรธยากแต่รุนแรง", "หัวโบราณ"],
     "careers": "เกษตรกร วิศวกร นายธนาคาร หมอ",
     "famous": "Barack Obama, Princess Diana"},
    {"name": "寅 หยิ่น (ขาล/เสือ)", "animal": "🐅 ขาล", "time": "03:00-05:00", "month": "กุมภาพันธ์",
     "element": "ไม้หยาง", "yin_yang": "หยาง",
     "traits_detailed": "กล้าหาญ มีอำนาจ ชอบแข่งขัน ผู้นำโดยธรรมชาติ",
     "strengths": ["กล้าหาญ", "มีอำนาจ", "ใจกว้าง", "นำพาคน"],
     "weaknesses": ["ใจร้อน", "ชอบแข่งขันตลอด", "หุนหัน", "ไม่ฟังคน"],
     "careers": "ทหาร ตำรวจ ผู้บริหาร นักกีฬา",
     "famous": "Tom Cruise, Lady Gaga"},
    {"name": "เหมา เหมา (เถาะ/กระต่าย)", "animal": "🐈 เถาะ", "time": "05:00-07:00", "month": "มีนาคม",
     "element": "ไม้หยิน", "yin_yang": "หยิน",
     "traits_detailed": "อ่อนโยน สุภาพ ฉลาด มีรสนิยม รักศิลปะ",
     "strengths": ["อ่อนโยน", "ฉลาด", "มีรสนิยม", "ทูตดี"],
     "weaknesses": ["ขี้อาย", "ไม่ค่อยตัดสินใจ", "หลีกเลี่ยงปัญหา", "เศร้าง่าย"],
     "careers": "นักการทูต ศิลปิน นักออกแบบ ทนายความ",
     "famous": "Albert Einstein, Angelina Jolie"},
    {"name": "เฉิน เฉิน (มะโรง/มังกร)", "animal": "🐉 มะโรง", "time": "07:00-09:00", "month": "เมษายน",
     "element": "ดินหยาง", "yin_yang": "หยาง",
     "traits_detailed": "สง่างาม มีบารมี มั่นใจ โชคดี สัญลักษณ์แห่งจักรพรรดิ",
     "strengths": ["สง่างาม", "มีบารมี", "โชคดี", "สร้างแรงบันดาลใจ"],
     "weaknesses": ["หยิ่ง", "ไม่ยอมรับผิด", "ขี้หงุดหงิด", "อ่อนไหวต่อคำวิจารณ์"],
     "careers": "ผู้นำ ผู้บริหาร นักประดิษฐ์ วิศวกร",
     "famous": "Bruce Lee, Vladimir Putin"},
    {"name": "ซื่อ ซื่อ (มะเส็ง/งู)", "animal": "🐍 มะเส็ง", "time": "09:00-11:00", "month": "พฤษภาคม",
     "element": "ไฟหยิน", "yin_yang": "หยิน",
     "traits_detailed": "ลึซึ้ง ฉลาด สง่างาม มีสัญชาตญาณดี ปัญญาสูง",
     "strengths": ["ฉลาดมาก", "สัญชาตญาณดี", "สง่างาม", "มีปัญญา"],
     "weaknesses": ["ขี้หึง", "ไม่ไว้ใจคนง่าย", "ชอบใช้คน", "เย็นชาบางครั้ง"],
     "careers": "นักปรัชญา หมอดู นักวิทยาศาสตร์ ผู้ประกอบการ",
     "famous": "Oprah Winfrey, Pablo Picasso"},
    {"name": "อู่ อู่ (มะเมีย/ม้า)", "animal": "🐴 มะเมีย", "time": "11:00-13:00", "month": "มิถุนายน",
     "element": "ไฟหยาง", "yin_yang": "หยาง",
     "traits_detailed": "กระตือรือร้น อิสระ แข่งขันเก่ง ร่าเริง ชอบเดินทาง",
     "strengths": ["กระตือรือร้น", "อิสระ", "ร่าเริง", "สื่อสารเก่ง"],
     "weaknesses": ["ไม่อดทน", "เปลี่ยนใจง่าย", "ขี้เบื่อ", "อารมณ์เสียง่าย"],
     "careers": "นักข่าว นักเดินทาง นักแสดง พิธีกร",
     "famous": "Jackie Chan, Kobe Bryant"},
    {"name": "เว่ย เว่ย (มะแม/แพะ)", "animal": "🐐 มะแม", "time": "13:00-15:00", "month": "กรกฎาคม",
     "element": "ดินหยิน", "yin_yang": "หยิน",
     "traits_detailed": "อ่อนโยน ศิลปะ มีเมตตา สงบสุข สร้างสรรค์",
     "strengths": ["อ่อนโยน", "สร้างสรรค์", "มีเมตตา", "ศิลปะดี"],
     "weaknesses": ["ไม่ค่อยตัดสินใจ", "พึ่งพาคนอื่น", "มองโลกแง่ลบบางครั้ง", "กังวลง่าย"],
     "careers": "ศิลปิน นักออกแบบ ครู นักบำบัด",
     "famous": "Bill Gates, Michelangelo"},
    {"name": "เชิน เชิน (วอก/ลิง)", "animal": "🐵 วอก", "time": "15:00-17:00", "month": "สิงหาคม",
     "element": "ทองหยาง", "yin_yang": "หยาง",
     "traits_detailed": "ฉลาด ขี้เล่น สร้างสรรค์ แก้ปัญหาเก่ง มีไหวพริบ",
     "strengths": ["ฉลาดมาก", "สร้างสรรค์", "แก้ปัญหาเก่ง", "สนุกสนาน"],
     "weaknesses": ["ชอบแกล้ง", "ไม่จริงจัง", "ชอบโกหกเล็กๆ", "ไม่ค่อยอดทน"],
     "careers": "นักประดิษฐ์ วิศวกรซอฟต์แวร์ ตลก นักเจรจา",
     "famous": "Leonardo da Vinci, Tom Hanks"},
    {"name": "โหยว โหยว (ระกา/ไก่)", "animal": "🐔 ระกา", "time": "17:00-19:00", "month": "กันยายน",
     "element": "ทองหยิน", "yin_yang": "หยิน",
     "traits_detailed": "ตรงไปตรงมา ขยัน มั่นใจ ใส่ใจรายละเอียด รักสวยรักงาม",
     "strengths": ["ตรงไปตรงมา", "ขยัน", "ใส่ใจรายละเอียด", "มั่นใจ"],
     "weaknesses": ["ชอบวิจารณ์", "หยิ่ง", "ชอบโอ้อวด", "ดื้อรั้น"],
     "careers": "นักบัญชี ช่างเสริมสวย ทหาร พ่อครัว",
     "famous": "Beyoncé, Britney Spears"},
    {"name": "ซู่ ซู่ (จอ/สุนัข)", "animal": "🐕 จอ", "time": "19:00-21:00", "month": "ตุลาคม",
     "element": "ดินหยาง", "yin_yang": "หยาง",
     "traits_detailed": "ซื่อสัตย์ ยุติธรรม ปกป้องคนที่รัก จริงใจ น่าเชื่อถือ",
     "strengths": ["ซื่อสัตย์สุดๆ", "ยุติธรรม", "ปกป้องเก่ง", "จริงใจ"],
     "weaknesses": ["กังวลง่าย", "ชอบวิจารณ์", "หัวดื้อ", "อารมณ์เสียง่าย"],
     "careers": "ตำรวจ ทนายความ นักสังคมสงเคราะห์ ครู",
     "famous": "Donald Trump, Madonna"},
    {"name": "ไฮ่ ไฮ่ (กุน/หมู)", "animal": "🐷 กุน", "time": "21:00-23:00", "month": "พฤศจิกายน",
     "element": "น้ำหยาง", "yin_yang": "หยิน",
     "traits_detailed": "ใจกว้าง ซื่อสัตย์ สนุกสนาน ใจดี รักสันติ",
     "strengths": ["ใจกว้าง", "ซื่อสัตย์", "สนุกสนาน", "ใจดีมาก"],
     "weaknesses": ["เก็บเงินไม่อยู่", "เชื่อคนง่าย", "เกียจคร้านบางครั้ง", "อ่อนไหวเกินไป"],
     "careers": "นักบันเทิง เชฟ ครู นักการกุศล",
     "famous": "Elon Musk, Hillary Clinton"},
]

# ─── 5 ธาตุกำเนิด (Five Elements) ───
FIVE_ELEMENTS = {
    "ไม้": {"symbol": "🌳", "season": "ฤดูใบไม้ผลิ", "direction": "ตะวันออก",
            "traits": "การเติบโต ความคิดสร้างสรรค์ ความเมตตา",
            "lucky_color": "🟢 เขียว", "lucky_direction": "ตะวันออก",
            "body_parts": "ตับ ถุงน้ำดี ตา เส้นเอ็น"},
    "ไฟ": {"symbol": "🔥", "season": "ฤดูร้อน", "direction": "ใต้",
            "traits": "ความร้อนแรง ความสุข ความหลงใหล",
            "lucky_color": "🔴 แดง", "lucky_direction": "ใต้",
            "body_parts": "หัวใจ ลำไส้เล็ก ลิ้น เส้นเลือด"},
    "ดิน": {"symbol": "🏜️", "season": "ปลายฤดูร้อน", "direction": "กลาง",
             "traits": "ความเสถียร ความเชื่อถือได้ การบำรุงเลี้ยง",
             "lucky_color": "🟡 เหลือง", "lucky_direction": "กลาง/ทิศตะวันตกเฉียงใต้",
             "body_parts": "ม้าม กระเพาะอาหาร ปาก กล้ามเนื้อ"},
    "ทอง": {"symbol": "🪙", "season": "ฤดูใบไม้ร่วง", "direction": "ตะวันตก",
             "traits": "ความเด็ดขาด ความคม ความมุ่งมั่น",
             "lucky_color": "⚪ ขาว/ทอง", "lucky_direction": "ตะวันตก",
             "body_parts": "ปอด ลำไส้ใหญ่ จมูก ผิวหนัง"},
    "น้ำ": {"symbol": "🌊", "season": "ฤดูหนาว", "direction": "เหนือ",
             "traits": "ปัญญา ความลึกซึ้ง การปรับตัว",
             "lucky_color": "🔵 น้ำเงิน/ดำ", "lucky_direction": "เหนือ",
             "body_parts": "ไต กระเพาะปัสสาวะ หู กระดูก"},
}


def get_heavenly_stem(year: int) -> dict:
    """หาธาตุฟ้าจากปี พ.ศ. ค.ศ."""
    # ใช้ cycle 60 ปี — เริ่มต้นที่ ปี ค.ศ. 4 = 甲子
    stem_index = (year - 4) % 10
    return HEAVENLY_STEMS[stem_index]


def get_earthly_branch(year: int) -> dict:
    """หาธาตุดิน (นักษัตร) จากปี"""
    branch_index = (year - 4) % 12
    return EARTHLY_BRANCHES[branch_index]


def get_five_element_from_stem(stem_element: str) -> str:
    """แปลงธาตุฟ้าเป็น 1 ใน 5 ธาตุ"""
    if "ไม้" in stem_element:
        return "ไม้"
    elif "ไฟ" in stem_element:
        return "ไฟ"
    elif "ดิน" in stem_element:
        return "ดิน"
    elif "ทอง" in stem_element:
        return "ทอง"
    else:
        return "น้ำ"


def get_element_relations(element: str) -> dict:
    """หาความสัมพันธ์ระหว่างธาตุ"""
    cycle = ["ไม้", "ไฟ", "ดิน", "ทอง", "น้ำ"]
    idx = cycle.index(element)
    
    produces = cycle[(idx + 1) % 5]  # ธาตุที่ผลิตได้
    produced_by = cycle[(idx - 1) % 5]  # ธาตุที่ผลิตเรา
    controls = cycle[(idx + 2) % 5]  # ธาตุที่เราควบคุม
    controlled_by = cycle[(idx - 2) % 5]  # ธาตุที่ควบคุมเรา
    
    return {
        "produces": produces,
        "produced_by": produced_by,
        "controls": controls,
        "controlled_by": controlled_by,
    }


def get_yearly_fortune_chinese(year: int, birth_year: int) -> str:
    """ดวงปีนักษัตรประจำปี"""
    age = year - birth_year
    birth_branch = get_earthly_branch(birth_year)
    
    # คำนวณปีชง
    branch_index = (birth_year - 4) % 12
    conflict_index = (branch_index + 6) % 12  # ชงตรงข้าม (6 ตำแหน่งห่าง)
    conflict_animal = EARTHLY_BRANCHES[conflict_index]["animal"]
    
    # ตรวจสอบปีชง
    year_branch_index = (year - 4) % 12
    is_conflict = (year_branch_index == conflict_index)
    
    seed = year + birth_year
    rng = random.Random(seed)
    score = rng.randint(30, 100)
    
    if is_conflict:
        score = max(20, score - 40)
        conflict_note = f"\n⚠️ ปีนี้เป็นปีชง! (ชงกับ {conflict_animal}) แนะนำทำบุญสะเดาะเคราะห์"
    else:
        conflict_note = ""
    
    return score, conflict_animal, conflict_note


def format_full_chinese_horoscope(birth_date: date) -> str:
    """จัดรูปแบบดูดวงจีนเต็ม"""
    year = birth_date.year
    
    # หาธาตุฟ้าและธาตุดิน
    stem = get_heavenly_stem(year)
    branch = get_earthly_branch(year)
    five_element = get_five_element_from_stem(stem["element"])
    element_data = FIVE_ELEMENTS[five_element]
    relations = get_element_relations(five_element)
    
    # ดวงประจำปี
    current_year = date.today().year
    score, conflict_animal, conflict_note = get_yearly_fortune_chinese(current_year, year)
    
    # จัดระดับ
    if score >= 80:
        level = "🌟 ดีมาก"
    elif score >= 60:
        level = "✨ ดี"
    elif score >= 40:
        level = "😐 ปานกลาง"
    else:
        level = "⚠️ ระวัง"
    
    from horoscope import get_chinese_zodiac
    chinese_z = get_chinese_zodiac(year)
    
    # โชค
    lucky_day = ["อาทิตย์", "จันทร์", "อังคาร", "พุธ", "พฤหัสบดี", "ศุกร์", "เสาร์"]
    rng = random.Random(year)
    lucky_days = rng.sample(lucky_day, 2)
    
    result = (
        f"🐉 ดูดวงจีนเต็ม (八字 Bāzì)\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"📅 วันเกิด: {birth_date.strftime('%d/%m/%Y')} (ปี {year})\n\n"
        
        f"🏛️ ธาตุฟ้าดิน (天干地支)\n"
        f"   ฟ้า (天干): {stem['name']}\n"
        f"      ลักษณะ: {stem['traits']}\n"
        f"   ดิน (地支): {branch['name']}\n"
        f"      เวลา: {branch['time']} | เดือน: {branch['month']}\n\n"
        
        f"🌳 ธาตุกำเนิด: {element_data['symbol']} {five_element}\n"
        f"   ฤดูกาล: {element_data['season']} | ทิศ: {element_data['direction']}\n"
        f"   ลักษณะ: {element_data['traits']}\n"
        f"   สีนำโชค: {element_data['lucky_color']}\n"
        f"   ทิศนำโชค: {element_data['lucky_direction']}\n"
        f"   อวัยวะดูแล: {element_data['body_parts']}\n\n"
        
        f"🔄 วัฏจักรธาตุ\n"
        f"   🌱 ธาตุที่คุณผลิต: {FIVE_ELEMENTS[relations['produces']]['symbol']} {relations['produces']}\n"
        f"   🤲 ธาตุที่ผลิตคุณ: {FIVE_ELEMENTS[relations['produced_by']]['symbol']} {relations['produced_by']}\n"
        f"   💪 ธาตุที่คุณควบคุม: {FIVE_ELEMENTS[relations['controls']]['symbol']} {relations['controls']}\n"
        f"   🛡️ ธาตุที่ควบคุมคุณ: {FIVE_ELEMENTS[relations['controlled_by']]['symbol']} {relations['controlled_by']}\n\n"
        
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"🐲 ลักษณะเด่น ({branch['animal']})\n"
        f"   {branch['traits_detailed']}\n\n"
        
        f"💪 จุดแข็ง:\n"
        f"   {', '.join(branch['strengths'])}\n\n"
        
        f"⚠️ จุดอ่อน:\n"
        f"   {', '.join(branch['weaknesses'])}\n\n"
        
        f"💼 อาชีพเหมาะ: {branch['careers']}\n"
        f"⭐ คนดังที่เกิดปีเดียวกัน: {branch['famous']}\n\n"
        
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"📅 ดวงปี {current_year} ({score}/100 {level}){conflict_note}\n\n"
        
        f"🍀 วันนำโชค: {', '.join(lucky_days)}\n"
        f"🎨 สีนำโชค: {element_data['lucky_color']}\n"
        f"🧭 ทิศนำโชค: {element_data['lucky_direction']}\n\n"
        
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"⚠️ เป็นความเชื่อส่วนบุคคล โปรดใช้วิจารณญาณ 🙏"
    )
    return result
