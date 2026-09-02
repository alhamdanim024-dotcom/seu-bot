import json
import os
import sys
import asyncio
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup          
from telegram.ext import (          
    Application,          
    CommandHandler,          
    CallbackQueryHandler,          
    MessageHandler,          
    ContextTypes,          
    filters,          
)          
from telegram.error import BadRequest          
         
         
# =========================================================          
# إعدادات البوت والقناة الخاصة بالأرشيف          
# =========================================================          
         
BOT_TOKEN = "8802545564:AAGhRtNK-I44igs2E4GWRqi6PsFLhuvtF2w"          
ADMIN_ID = 7031240417  # الآيدي الخاص بك للمطور
ARCHIVE_CHANNEL_ID = -1003585396877  # آيدي قناة الأرشيف الخاصة بك
         
GROUP_USERNAME = "@SEU_Students2"          
GROUP_URL = "https://t.me/SEU_Students2"         
WHATSAPP_GROUP_URL = "https://chat.whatsapp.com/BmgT2joy3AyBx1nE0LQ1wh?s=cl&p=a&ilr=4&amv=3" 
WHATSAPP_CHANNEL_URL = "https://whatsapp.com/channel/0029VbE4u8MKWEKudwnk8N1o"
         
DATA_FILE = "course_files.json"  # ملف مؤقت لتسجيل الروابط والمعرفات[cite: 1, 2]
         
         
# =========================================================          
# دوال حفظ واسترجاع الملفات          
# =========================================================          

def load_course_files():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading data: {e}")
    return {}

def save_course_files():
    try:
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(COURSE_FILES, f, ensure_ascii=False, indent=4)
    except Exception as e:
        print(f"Error saving data: {e}")

COURSE_FILES = load_course_files()
         
         
# =========================================================          
# أسماء المقررات          
# =========================================================          
         
COURSES = {          
    "cs001": "💻 CS001 - مقدمة إلى الذكاء الاصطناعي", "ci001": "📖 CI001 - مهارات أكاديمية",          
    "english_level_1": "English - Level 1", "english_level_2": "English - Level 2", "english_level_3": "English - Level 3",
    "math001": "MATH001 - الرياضيات", "com001": "COM001 - مهارات الاتصال",          
    "law_ai": "مقدمة إلى الذكاء الاصطناعي", "law_academic": "المهارات الأكاديمية", "law_english": "الإنجليزي",          
    "islam101": "ISLAM101", "islam102": "ISLAM102", "islam103": "ISLAM103", "islam104": "ISLAM104",          
}          
         
         
# =========================================================          
# تخصصات كلية العلوم الإدارية والمالية          
# =========================================================          
         
ACCOUNTING_COURSES = {          
    "3": [("stat101", "STAT101"), ("law101", "LAW101"), ("econ101", "ECON101"), ("mgt101", "MGT101"), ("acct101", "ACCT101")],          
    "4": [("stat201", "STAT201"), ("fin101", "FIN101"), ("mgt201", "MGT201"), ("mgt211", "MGT211"), ("ecom101", "ECOM101")],          
    "5": [("econ201", "ECON201"), ("ecom201", "ECOM201"), ("mgt301", "MGT301"), ("mgt311", "MGT311"), ("acct201", "ACCT201")],          
    "6": [("acct301", "ACCT301"), ("mgt321", "MGT321"), ("mgt322", "MGT322"), ("acct302", "ACCT302")],          
    "7": [("mgt401", "MGT401"), ("acct401", "ACCT401"), ("acct403", "ACCT403"), ("acct402", "ACCT402")],          
    "8": [("law401", "LAW401"), ("acct322", "ACCT322"), ("acct422", "ACCT422"), ("acct430", "ACCT430")],          
}          
         
BUSINESS_ADMIN_COURSES = {          
    "3": [("stat101", "STAT101"), ("law101", "LAW101"), ("econ101", "ECON101"), ("mgt101", "MGT101"), ("acct101", "ACCT101")],          
    "4": [("stat201", "STAT201"), ("fin101", "FIN101"), ("mgt201", "MGT201"), ("mgt211", "MGT211"), ("ecom101", "ECOM101")],          
    "5": [("econ201", "ECON201"), ("mis201", "MIS201"), ("ecom201", "ECOM201"), ("mgt301", "MGT301"), ("mgt311", "MGT311"), ("mgt312", "MGT312")],          
    "6": [("acct301", "ACCT301"), ("mgt321", "MGT321"), ("mgt322", "MGT322"), ("mgt323", "MGT323")],          
    "7": [("mgt401", "MGT401"), ("mgt324", "MGT324"), ("mgt402", "MGT402"), ("mgt403", "MGT403")],          
    "8": [("mgt404", "MGT404"), ("mgt421", "MGT421"), ("mgt422", "MGT422"), ("mgt430", "MGT430")],          
}          
         
ECOMMERCE_COURSES = {          
    "3": [("stat101", "STAT101"), ("law101", "LAW101"), ("econ101", "ECON101"), ("mgt101", "MGT101"), ("acct101", "ACCT101")],          
    "4": [("stat201", "STAT201"), ("fin101", "FIN101"), ("mgt201", "MGT201"), ("mgt211", "MGT211"), ("ecom101", "ECOM101")],          
    "5": [("mis201", "MIS201"), ("ecom201", "ECOM201"), ("mgt301", "MGT301"), ("mgt311", "MGT311"), ("ecom301", "ECOM301"), ("econ201", "ECON201")],          
    "6": [("acct301", "ACCT301"), ("mgt321", "MGT321"), ("mgt322", "MGT322"), ("it401", "IT401")],          
    "7": [("mgt401", "MGT401"), ("it403", "IT403"), ("it404", "IT404"), ("law402", "LAW402")],          
    "8": [("it402", "IT402"), ("ecom421", "ECOM421"), ("ecom402", "ECOM402"), ("ecom430", "ECOM430")],          
}          
         
FINANCE_COURSES = {          
    "3": [("stat101", "STAT101"), ("law101", "LAW101"), ("econ101", "ECON101"), ("mgt101", "MGT101"), ("acct101", "ACCT101")],          
    "4": [("ecom101", "ECOM101"), ("stat201", "STAT201"), ("fin101", "FIN101"), ("mgt201", "MGT201"), ("mgt211", "MGT211")],          
    "5": [("mis201", "MIS201"), ("ecom201", "ECOM201"), ("mgt301", "MGT301"), ("mgt311", "MGT311"), ("fin201", "FIN201"), ("econ201", "ECON201")],          
    "6": [("acct301", "ACCT301"), ("mgt321", "MGT321"), ("mgt322", "MGT322"), ("fin301", "FIN301")],          
    "7": [("mgt401", "MGT401"), ("fin401", "FIN401"), ("fin402", "FIN402"), ("fin403", "FIN403")],          
    "8": [("fin405", "FIN405"), ("fin406", "FIN406"), ("fin424", "FIN424"), ("fin408", "FIN408")],          
}          
         
ADMIN_FINANCIAL_COURSES = {          
    "accounting": ACCOUNTING_COURSES,          
    "business_admin": BUSINESS_ADMIN_COURSES,          
    "ecommerce": ECOMMERCE_COURSES,          
    "finance": FINANCE_COURSES,          
}          
         
         
# =========================================================          
# كلية العلوم الصحية          
# =========================================================          
         
HEALTH_COURSES = {          
    "public_health": {          
        "3": [("health_public_biol101", "BIOL 101"), ("health_public_hcm101", "HCM 101"), ("health_public_phc121", "PHC 121"), ("health_public_phc101", "PHC 101"), ("health_public_hcm102", "HCM 102")],          
        "4": [("health_public_biol102", "BIOL 102"), ("health_public_biol103", "BIOL 103"), ("health_public_hcm113", "HCM 113"), ("health_public_phc131", "PHC 131"), ("health_public_phc151", "PHC 151"), ("health_public_phc181", "PHC 181")],          
        "5": [("health_public_phc212", "PHC 212"), ("health_public_phc241", "PHC 241"), ("health_public_phc261", "PHC 261"), ("health_public_phc271", "PHC 271"), ("health_public_phc281", "PHC 281")],          
        "6": [("health_public_hcm213", "HCM 213"), ("health_public_phc215", "PHC 215"), ("health_public_phc216", "PHC 216"), ("health_public_phc231", "PHC 231"), ("health_public_phc273", "PHC 273"), ("health_public_phc274", "PHC 274")],          
        "7": [("health_public_phc311", "PHC 311"), ("health_public_phc312", "PHC 312"), ("health_public_phc313", "PHC 313"), ("health_public_phc331", "PHC 331"), ("health_public_phc372", "PHC 372"), ("health_public_phc373", "PHC 373")],          
        "8": [("health_public_phc374", "PHC 374"), ("health_public_phc314", "PHC 314")],          
    },          
    "health_informatics": {          
        "3": [("health_info_it231", "IT231"), ("health_info_it232", "IT232"), ("health_info_bio101", "BIO101"), ("health_info_phc121", "PHC121"), ("health_info_hcm101", "HCM101"), ("health_info_hcm102", "HCM102")],          
        "4": [("health_info_it244", "IT244"), ("health_info_bio102", "BIO102"), ("health_info_it245", "IT245"), ("health_info_phc131", "PHC131"), ("health_info_hcm113", "HCM113")],          
        "5": [("health_info_it351", "IT351"), ("health_info_it352", "IT352"), ("health_info_it353", "IT353"), ("health_info_phc212", "PHC 212"), ("health_info_hci111", "HCI 111")],          
        "6": [("health_info_hcm213", "HCM 213"), ("health_info_it361", "IT361"), ("health_info_it362", "IT362"), ("health_info_phc215", "PHC 215"), ("health_info_phc216", "PHC 216"), ("health_info_hci112", "HCI 112")],          
        "7": [("health_info_hci214", "HCI214"), ("health_info_it475", "IT475"), ("health_info_it476", "IT476"), ("health_info_hci213", "HCI 213"), ("health_info_phc312", "PHC312")],          
        "8": [("health_info_hci315", "HCI315"), ("health_info_hci314", "HCI314"), ("health_info_hci316", "HCI316")],          
    },          
}          
         
         
# =========================================================          
# كلية الدراسات النظرية          
# =========================================================          
         
THEORETICAL_COURSES = {          
    "digital_media": {          
        "2": [("dmed_comm003", "COMM 003"), ("dmed_dmed101", "DMED 101"), ("dmed_dmed102", "DMED 102"), ("dmed_dmed103", "DMED 103"), ("dmed_arb211", "ARB 211"), ("dmed_math003", "MATH 003")],          
        "3": [("dmed_dmed201", "DMED201"), ("dmed_dmed202", "DMED202"), ("dmed_dmed203", "DMED203"), ("dmed_dmed204", "DMED204"), ("dmed_arb260", "ARB260")],          
        "4": [("dmed_dmed205", "DMED205"), ("dmed_dmed206", "DMED206"), ("dmed_dmed207", "DMED207"), ("dmed_dmps101", "DMPS101"), ("dmed_dmed208", "DMED208")],          
        "5": [], "6": [], "7": [], "8": [],          
    },          
    "law": {          
        "2": [("law_math003", "MATH 003"), ("law_comm003", "COMM 003"), ("law_law121", "Law 121"), ("law_law122", "Law 122"), ("law_law123", "Law 123")],          
        "3": [("law_law211", "LAW 211"), ("law_law212", "LAW 212"), ("law_law213", "LAW 213"), ("law_law214", "LAW 214")],          
        "4": [("law_law221", "LAW 221"), ("law_law222", "LAW 222"), ("law_law223", "LAW 223"), ("law_law224", "LAW 224"), ("law_law225", "LAW 225")],          
        "5": [("law_law311", "LAW 311"), ("law_law312", "LAW 312"), ("law_law313", "LAW 313"), ("law_law314", "LAW 314"), ("law_law315", "LAW 315")],          
        "6": [("law_law321", "LAW 321"), ("law_law322", "LAW 322"), ("law_law323", "LAW 323"), ("law_law324", "LAW 324"), ("law_law325", "LAW 325")],          
        "7": [("law_law411", "LAW 411"), ("law_law412", "LAW 412"), ("law_law413", "LAW 413"), ("law_law414", "LAW 414"), ("law_law415", "LAW 415"), ("law_law416", "LAW 416")],          
        "8": [],          
    },          
    "translation": {          
        "2": [], "3": [], "4": [], "5": [], "6": [], "7": [], "8": [],          
    },          
}          
         
         
# =========================================================          
# كلية الحوسبة والمعلوماتية          
# =========================================================          
         
COMPUTING_COURSES = {          
    "cs": {          
        "3": [("computing_cs_sci101", "SCI101"), ("computing_cs_cs230", "CS230"), ("computing_cs_eng103", "ENG103"), ("computing_cs_math150", "MATH150"), ("computing_cs_cs231", "CS231")],          
        "4": [("computing_cs_sci201", "SCI201"), ("computing_cs_cs240", "CS240"), ("computing_cs_cs241", "CS241"), ("computing_cs_cs242", "CS242"), ("computing_cs_cs243", "CS243")],          
        "5": [("computing_cs_math251", "MATH251"), ("computing_cs_cs350", "CS350"), ("computing_cs_cs351", "CS351"), ("computing_cs_cs352", "CS352"), ("computing_cs_cs353", "CS353")],          
        "6": [("computing_cs_cs360", "CS360"), ("computing_cs_stat101", "STAT101"), ("computing_cs_cs361", "CS361"), ("computing_cs_cs362", "CS362"), ("computing_cs_cs363", "CS363"), ("computing_cs_cs364", "CS364")],          
        "7": [("computing_cs_cs470", "CS470"), ("computing_cs_cs471", "CS471"), ("computing_cs_cs479", "CS479"), ("computing_cs_cs475", "CS475"), ("computing_cs_cs476", "CS476")],          
        "8": [("computing_cs_cs489", "CS489"), ("computing_cs_cs480", "CS480"), ("computing_cs_cs481", "CS481"), ("computing_cs_cs477", "CS477"), ("computing_cs_cs478", "CS478"), ("computing_cs_cs499", "CS499")],          
    },          
    "it": {          
        "3": [("computing_it_it231", "IT231"), ("computing_it_it232", "IT232"), ("computing_it_it233", "IT233"), ("computing_it_math150", "MATH150"), ("computing_it_sci101", "SCI101")],          
        "4": [("computing_it_it241", "IT241"), ("computing_it_it244", "IT244"), ("computing_it_it245", "IT245"), ("computing_it_eng103", "ENG103"), ("computing_it_math251", "MATH251"), ("computing_it_sci201", "SCI201")],          
        "5": [("computing_it_it351", "IT351"), ("computing_it_it352", "IT352"), ("computing_it_it353", "IT353"), ("computing_it_it354", "IT354"), ("computing_it_stat101", "STAT101")],          
        "6": [("computing_it_it361", "IT361"), ("computing_it_it362", "IT362"), ("computing_it_it363", "IT363"), ("computing_it_it364", "IT364"), ("computing_it_it365", "IT365")],          
        "7": [("computing_it_it474", "IT474"), ("computing_it_it478", "IT478"), ("computing_it_it475", "IT475"), ("computing_it_it476", "IT476"), ("computing_it_it479", "IT479")],          
        "8": [("computing_it_it484", "IT484"), ("computing_it_it488", "IT488"), ("computing_it_it485", "IT485"), ("computing_it_it487", "IT487"), ("computing_it_it489", "IT489"), ("computing_it_it499", "IT499")],          
    },          
    "ds": {          
        "3": [("computing_ds_sci101", "SCI101"), ("computing_ds_ds230", "DS230"), ("computing_ds_eng103", "ENG103"), ("computing_ds_math150", "MATH150"), ("computing_ds_ds231", "DS231")],          
        "4": [("computing_ds_math251", "MATH251"), ("computing_ds_ds240", "DS240"), ("computing_ds_math241", "MATH241"), ("computing_ds_ds242", "DS242"), ("computing_ds_ds243", "DS243")],          
        "5": [("computing_ds_sci201", "SCI201"), ("computing_ds_ds350", "DS350"), ("computing_ds_ds351", "DS351"), ("computing_ds_stat201", "STAT201"), ("computing_ds_ds352", "DS352"), ("computing_ds_ds353", "DS353")],          
        "6": [("computing_ds_ds360", "DS360"), ("computing_ds_ds361", "DS361"), ("computing_ds_ds362", "DS362"), ("computing_ds_ds363", "DS363"), ("computing_ds_ds364", "DS364")],          
        "7": [("computing_ds_ds470", "DS470"), ("computing_ds_ds471", "DS471"), ("computing_ds_ds472", "DS472"), ("computing_ds_ds479", "DS479"), ("computing_ds_ds473", "DS473"), ("computing_ds_ds474", "DS474")],          
        "8": [("computing_ds_ds480", "DS480"), ("computing_ds_ds481", "DS481"), ("computing_ds_ds489", "DS489"), ("computing_ds_ds482", "DS482"), ("computing_ds_ds483", "DS483"), ("computing_ds_ds499", "DS499")],          
    },          
}          
         
         
# =========================================================          
# تعبئة القواميس العامة          
# =========================================================          
         
for specialty_courses in ADMIN_FINANCIAL_COURSES.values():          
    for level_courses in specialty_courses.values():          
        for course_id, course_code in level_courses:          
            COURSES.setdefault(course_id, course_code)          
            COURSE_FILES.setdefault(course_id, {"book": [], "summary": [], "collections": []})          
         
for specialty_courses in COMPUTING_COURSES.values():          
    for level_courses in specialty_courses.values():          
        for course_id, course_code in level_courses:          
            COURSES.setdefault(course_id, course_code)          
            COURSE_FILES.setdefault(course_id, {"book": [], "summary": [], "collections": []})          

for specialty_courses in HEALTH_COURSES.values():          
    for level_courses in specialty_courses.values():          
        for course_id, course_code in level_courses:          
            COURSES.setdefault(course_id, course_code)          
            COURSE_FILES.setdefault(course_id, {"book": [], "summary": [], "collections": []})          

for specialty_courses in THEORETICAL_COURSES.values():          
    for level_courses in specialty_courses.values():          
        for course_id, course_code in level_courses:          
            COURSES.setdefault(course_id, course_code)          
            COURSE_FILES.setdefault(course_id, {"book": [], "summary": [], "collections": []})          
         
         
# =========================================================          
# دوال التحقق والأمان          
# =========================================================          
         
async def is_member(bot, user_id):          
    try:          
        member = await bot.get_chat_member(          
            chat_id=GROUP_USERNAME,          
            user_id=user_id,          
        )          
        return member.status in {"member", "administrator", "creator", "restricted"}          
    except BadRequest:          
        return False          
    except Exception as error:          
        print(f"Membership check error: {error}")          
        return False          

async def check_user_access(update, context):
    chat = update.effective_chat
    if chat.type in ["group", "supergroup"]:
        return True
    user_id = update.effective_user.id
    return await is_member(context.bot, user_id)          
         
def subscription_keyboard():          
    return InlineKeyboardMarkup([          
        [InlineKeyboardButton("الانضمام إلى القروب", url=GROUP_URL)],          
        [InlineKeyboardButton("تم الانضمام – تحقق", callback_data="check_membership")],          
    ])          
         
async def send_subscription_message(update, context):          
    text = (          
        "🔒 للوصول إلى محتوى البوت، يجب أولاً "          
        "الانضمام إلى القروب العام.\n\n"          
        "1️⃣ اضغط «الانضمام إلى القروب».\n"          
        "2️⃣ بعد الانضمام اضغط "          
        "«تم الانضمام – تحقق»."          
    )          
    message = await update.effective_message.reply_text(text, reply_markup=subscription_keyboard())          
    return message          
         
         
# =========================================================          
# تصميم لوحات المفاتيح السفلية (Reply Keyboards)
# =========================================================          
         
def main_reply_keyboard():          
    return ReplyKeyboardMarkup([          
        ["📚 الكتب والتجميعات والملخصات والخطط الدراسية"],          
        ["دليل الوصول للخدمات الإلكترونية"],          
        ["🎓 دليل المستجدين", "📅 التقويم الأكاديمي 1448"]          
    ], resize_keyboard=True, input_field_placeholder="اختر من القائمة أدناه 👇")          

def colleges_reply_keyboard():
    return ReplyKeyboardMarkup([
        ["التحضيري"],
        ["كلية الحوسبة والمعلوماتية", "كلية العلوم الإدارية والمالية"],
        ["كلية الدراسات النظرية", "كلية العلوم الصحية"],
        ["مواد السلم - ISLAM"],
        ["⬅️ رجوع", "🏠 القائمة الرئيسية"]
    ], resize_keyboard=True, input_field_placeholder="اختر الكلية أو القسم المطلوب 👇")

def preparatory_reply_keyboard():
    return ReplyKeyboardMarkup([
        ["خطة B", "خطة A"],
        ["⚖️ تحضيري القانون والإعلام الرقمي"],
        ["⬅️ رجوع", "🏠 القائمة الرئيسية"]
    ], resize_keyboard=True, input_field_placeholder="اختر الخطة المطلوبة 👇")

def plan_a_reply_keyboard():
    return ReplyKeyboardMarkup([
        ["💻 CS001 - مقدمة إلى الذكاء الاصطناعي"],
        ["📖 CI001 - مهارات أكاديمية"],
        ["English - الإنجليزي"],
        ["⬅️ رجوع", "🏠 القائمة الرئيسية"]
    ], resize_keyboard=True, input_field_placeholder="اختر المقرر المطلوب 👇")

def plan_b_reply_keyboard():
    return ReplyKeyboardMarkup([
        ["MATH001 - الرياضيات"],
        ["COM001 - مهارات الاتصال"],
        ["English - الإنجليزي"],
        ["⬅️ رجوع", "🏠 القائمة الرئيسية"]
    ], resize_keyboard=True, input_field_placeholder="اختر المقرر المطلوب 👇")

def english_levels_reply_keyboard():
    return ReplyKeyboardMarkup([
        ["Level 1", "Level 2"],
        ["Level 3"],
        ["⬅️ رجوع", "🏠 القائمة الرئيسية"]
    ], resize_keyboard=True, input_field_placeholder="اختر المستوى المطلوب 👇")

def law_media_reply_keyboard():
    return ReplyKeyboardMarkup([
        ["مقدمة إلى الذكاء الاصطناعي"],
        ["المهارات الأكاديمية"],
        ["الإنجليزي"],
        ["⬅️ رجوع", "🏠 القائمة الرئيسية"]
    ], resize_keyboard=True, input_field_placeholder="اختر المقرر المطلوب 👇")

def computing_reply_keyboard():
    return ReplyKeyboardMarkup([
        ["تقنية المعلومات - IT", "علوم الحاسب - CS"],
        ["علوم البيانات - DS"],
        ["⬅️ رجوع", "🏠 القائمة الرئيسية"]
    ], resize_keyboard=True, input_field_placeholder="اختر التخصص المطلوب 👇")

def health_reply_keyboard():
    return ReplyKeyboardMarkup([
        ["صحة عامة - Public Health"],
        ["معلوماتية صحية - Health Informatics"],
        ["⬅️ رجوع", "🏠 القائمة الرئيسية"]
    ], resize_keyboard=True, input_field_placeholder="اختر التخصص المطلوب 👇")

def business_reply_keyboard():
    return ReplyKeyboardMarkup([
        ["📊 المحاسبة", "💼 إدارة الأعمال"],
        ["🛒 التجارة الإلكترونية", "📈 المالية"],
        ["⬅️ رجوع", "🏠 القائمة الرئيسية"]
    ], resize_keyboard=True, input_field_placeholder="اختر التخصص المطلوب 👇")

def theory_reply_keyboard():
    return ReplyKeyboardMarkup([
        ["⚖️ قانون", "📺 إعلام رقمي"],
        ["📝 اللغة والترجمة"],
        ["⬅️ رجوع", "🏠 القائمة الرئيسية"]
    ], resize_keyboard=True, input_field_placeholder="اختر التخصص المطلوب 👇")

def islam_reply_keyboard():
    return ReplyKeyboardMarkup([
        ["ISLAM101", "ISLAM102"],
        ["ISLAM103", "ISLAM104"],
        ["⬅️ رجوع", "🏠 القائمة الرئيسية"]
    ], resize_keyboard=True, input_field_placeholder="اختر المقرر المطلوب 👇")

def levels_reply_keyboard(prefix):
    keyboard = [["📄 ملف الخطة الدراسية"]]
    if prefix != "translation":
        keyboard.extend([
            ["المستوى الرابع", "المستوى الثالث"],
            ["المستوى السادس", "المستوى الخامس"],
            ["المستوى الثامن", "المستوى السابع"]
        ])
    keyboard.append(["⬅️ رجوع", "🏠 القائمة الرئيسية"])
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True, input_field_placeholder="اختر المستوى المطلوب 👇")

def courses_list_reply_keyboard(courses_list, prefix):
    keyboard = []
    for i in range(0, len(courses_list), 2):
        row = [courses_list[i][1]]
        if i + 1 < len(courses_list):
            row.append(courses_list[i+1][1])
        keyboard.append(row)
    keyboard.append(["⬅️ رجوع", "🏠 القائمة الرئيسية"])
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True, input_field_placeholder="اختر المقرر المطلوب 👇")

def course_services_reply_keyboard(course_id):
    if course_id == "math001":
        return ReplyKeyboardMarkup([
            ["📚 الملخصات", "📘 الكتاب"],
            ["🔗 طريقة الدخول لواجبات الماث", "🧩 تجميعات"],
            ["⬅️ رجوع", "🏠 القائمة الرئيسية"]
        ], resize_keyboard=True, input_field_placeholder="اختر الخدمة المطلوبة 👇")
    else:
        return ReplyKeyboardMarkup([
            ["📚 الملخصات", "📘 الكتاب"],
            ["🧩 تجميعات"],
            ["⬅️ رجوع", "🏠 القائمة الرئيسية"]
        ], resize_keyboard=True, input_field_placeholder="اختر الخدمة المطلوبة 👇")

def math_collections_reply_keyboard():
    return ReplyKeyboardMarkup([
        ["📄 تجميعات الميد", "📄 تجميعات الواجبات"],
        ["📄 تجميعات الفاينال"],
        ["⬅️ رجوع", "🏠 القائمة الرئيسية"]
    ], resize_keyboard=True, input_field_placeholder="اختر القسم المطلوب 👇")

def math_hw_reply_keyboard():
    return ReplyKeyboardMarkup([
        ["تجميعات الواجب الثاني", "تجميعات الواجب الأول"],
        ["تجميعات الواجب الرابع", "تجميعات الواجب الثالث"],
        ["تجميعات الواجب الخامس"],
        ["⬅️ رجوع", "🏠 القائمة الرئيسية"]
    ], resize_keyboard=True, input_field_placeholder="اختر الواجب المطلوب 👇")

def electronic_services_reply_keyboard():
    return ReplyKeyboardMarkup([
        ["طريقة تصفح الشعب", "طريقة تسجيل المواد"],
        ["طريقة سداد الرسوم"],
        ["طريقة الوصول للجدول الدراسي"],
        ["طريقة رفع اعذار التغيب عن الاختبارات"],
        ["كيفية استخراج افادة"],
        ["⬅️ رجوع", "🏠 القائمة الرئيسية"]
    ], resize_keyboard=True, input_field_placeholder="اختر الخدمة المطلوبة 👇")

def freshmen_guide_reply_keyboard():
    return ReplyKeyboardMarkup([
        ["تطبيق البلاك بورد"],
        ["قناة الأخبار الهامة للمستجدين على واتساب"],
        ["مواصفات اللابتوب المطلوب", "طريقة تفعيل الحساب الجامعي"],
        ["خطوات تفعيل البريد الجامعي", "طريقة حضور المحاضرات"],
        ["شروط معادلة المواد", "ستيب - STEP"],
        ["قروب الاستفسارات والإجابة على اسئلتكم"],
        ["⬅️ رجوع", "🏠 القائمة الرئيسية"]
    ], resize_keyboard=True, input_field_placeholder="اختر الدليل أو الخدمة المطلوبة 👇")


# =========================================================          
# دوال استعراض الملفات          
# =========================================================          
async def send_plan_file(update, context, specialty_prefix, specialty_name):
    chat_id = update.effective_chat.id
    user_id = update.effective_user.id

    plan_key = f"plan_{specialty_prefix}"
    plan_data = COURSE_FILES.get(plan_key, {})
    file_id = plan_data.get("file_id")

    if user_id == ADMIN_ID:
        context.user_data["waiting_for_file"] = {"plan_key": plan_key, "plan_title": f"خطة {specialty_name}"}

    if not file_id:
        msg_text = f"📋 **خطة {specialty_name}**\n\nلم تتم إضافة ملف الخطة بعد."
        if user_id == ADMIN_ID:
            msg_text += f"\n\n🛠️ **[وضع المطور]:** أرسل ملف الـ PDF الخاص بـ ({specialty_name}) هنا ليتم أرشفته واستخراج المعرف!"
        await update.message.reply_text(msg_text, parse_mode="Markdown")
        return

    try:
        markup = None
        if user_id == ADMIN_ID:
            markup = InlineKeyboardMarkup([[InlineKeyboardButton("🗑️ حذف ملف الخطة", callback_data=f"del_plan:{plan_key}")]])
        
        await context.bot.send_document(chat_id=chat_id, document=file_id, caption=f"📋 خطة {specialty_name}", parse_mode="Markdown", reply_markup=markup)
    except Exception as error:
        print(f"Error sending plan file: {error}")


async def send_system_guide_files(update, context, guide_key, guide_title):
    chat_id = update.effective_chat.id
    user_id = update.effective_user.id

    guide_data = COURSE_FILES.get(guide_key, {})
    if isinstance(guide_data, list):
        guide_data = {"files": guide_data}
        COURSE_FILES[guide_key] = guide_data

    file_list = guide_data.get("files", [])

    if not file_list:
        msg_text = f"📌 **{guide_title}**\n\nلا توجد ملفات مضافة لهذا الدليل حالياً."
        if user_id == ADMIN_ID:
            msg_text += "\n\n🛠️ **[وضع المطور]:** أرسل أي ملف/صورة هنا ليتم حفظه."
        await update.message.reply_text(msg_text, parse_mode="Markdown")
        return

    for idx, item in enumerate(file_list):
        f_id = item.get("file_id")
        f_type = item.get("type", "document")
        caption = item.get("caption", "")

        try:
            markup = None
            if user_id == ADMIN_ID:
                markup = InlineKeyboardMarkup([[InlineKeyboardButton(f"🗑️ حذف هذا الملف ({idx+1})", callback_data=f"del_guide:{guide_key}:{idx}")]])

            if f_type == "photo":
                await context.bot.send_photo(chat_id=chat_id, photo=f_id, caption=caption, parse_mode="Markdown", reply_markup=markup)
            elif f_type == "video":
                await context.bot.send_video(chat_id=chat_id, video=f_id, caption=caption, parse_mode="Markdown", reply_markup=markup)
            elif f_type == "audio":
                await context.bot.send_audio(chat_id=chat_id, audio=f_id, caption=caption, parse_mode="Markdown", reply_markup=markup)
            else:
                await context.bot.send_document(chat_id=chat_id, document=f_id, caption=caption, parse_mode="Markdown", reply_markup=markup)
        except Exception as error:          
            print(f"Error sending guide file: {error}")


async def send_service_files(update, context, course_id, course_name, service):
    chat_id = update.effective_chat.id
    user_id = update.effective_user.id

    course_files = COURSE_FILES.get(course_id, {})
    file_list = course_files.get(service, [])

    if not file_list:
        msg_text = f"📁 {course_name}\n\nلا توجد ملفات مضافة لهذا القسم حالياً."
        if user_id == ADMIN_ID:
            msg_text += "\n\n🛠️ **[وضع المطور]:** أرسل الملفات أو الوسائط هنا ليتم حفظها واستخراج الـ file_id فوراً."
        await update.message.reply_text(msg_text, parse_mode="Markdown")
        return

    for idx, item in enumerate(file_list):
        f_id = item.get("file_id")
        f_type = item.get("type", "document")
        caption = item.get("caption", "")

        try:
            markup = None
            if user_id == ADMIN_ID:
                markup = InlineKeyboardMarkup([[InlineKeyboardButton(f"🗑️ حذف هذا الملف ({idx+1})", callback_data=f"del_course:{course_id}:{service}:{idx}")]])

            if f_type == "photo":
                await context.bot.send_photo(chat_id=chat_id, photo=f_id, caption=caption, parse_mode="Markdown", reply_markup=markup)
            elif f_type == "video":
                await context.bot.send_video(chat_id=chat_id, video=f_id, caption=caption, parse_mode="Markdown", reply_markup=markup)
            elif f_type == "audio":
                await context.bot.send_audio(chat_id=chat_id, audio=f_id, caption=caption, parse_mode="Markdown", reply_markup=markup)
            else:
                await context.bot.send_document(chat_id=chat_id, document=f_id, caption=caption, parse_mode="Markdown", reply_markup=markup)
        except Exception as error:          
            print(f"Error sending service file: {error}")


# =========================================================          
# القائمة الرئيسية          
# =========================================================          
async def show_main_menu(chat_id, context, bot):
    context.user_data["menu_state"] = "main"
    text = (          
        "🎓 أهلاً بك في بوت مقررات الجامعة – SEU Courses\n\n"          
        "كل ما يحتاجه طالب الجامعة السعودية الإلكترونية في مكان واحد:\n\n"          
        "📘 الكتب\n"          
        "📚 الملخصات\n"          
        "🧩 تجميعات لاختبارات سابقة\n\n"          
        "ابدأ باختيار القسم من القائمة 👇"          
    )          
    await bot.send_message(chat_id=chat_id, text=text, reply_markup=main_reply_keyboard())


# =========================================================          
# أوامر البوت ومعالجة الرسائل          
# =========================================================          

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):          
    if not await check_user_access(update, context):          
        await send_subscription_message(update, context)          
        return          
    context.user_data.pop("waiting_for_file", None)
    await show_main_menu(update.effective_chat.id, context, context.bot)


async def handle_messages(update: Update, context: ContextTypes.DEFAULT_TYPE):          
    user_id = update.effective_user.id          
    chat_id = update.effective_chat.id
    text = update.message.text if update.message and update.message.text else ""
          
    if not await check_user_access(update, context):          
        await send_subscription_message(update, context)          
        return          
          
    is_media_message = bool(update.message.document or update.message.photo or update.message.video or update.message.audio)

    # معالجة وضع المطور لرفع الملفات واستخراج المعرفات بوضوح تام
    if user_id == ADMIN_ID and "waiting_for_file" in context.user_data and is_media_message:          
        if update.message.document:          
            file_id = update.message.document.file_id
            file_type = "document"
        elif update.message.photo:          
            file_id = update.message.photo[-1].file_id
            file_type = "photo"
        elif update.message.video:          
            file_id = update.message.video.file_id
            file_type = "video"
        elif update.message.audio:          
            file_id = update.message.audio.file_id
            file_type = "audio"
        else:          
            return          
      
        caption = update.message.caption if update.message.caption else ""
        target = context.user_data["waiting_for_file"]          

        try:
            archive_caption = f"📦 أرشيف دائم\n📌 القسم: {target.get('plan_title', target.get('guide_title', target.get('course_id', 'ملف')))}"
            if caption:
                archive_caption += f"\n📝 الملاحظة: {caption}"
            
            if file_type == "photo":
                await context.bot.send_photo(chat_id=ARCHIVE_CHANNEL_ID, photo=file_id, caption=archive_caption)
            elif file_type == "video":
                await context.bot.send_video(chat_id=ARCHIVE_CHANNEL_ID, video=file_id, caption=archive_caption)
            elif file_type == "audio":
                await context.bot.send_audio(chat_id=ARCHIVE_CHANNEL_ID, audio=file_id, caption=archive_caption)
            else:
                await context.bot.send_document(chat_id=ARCHIVE_CHANNEL_ID, document=file_id, caption=archive_caption)
        except Exception as e:
            print(f"Archive sending error: {e}")
            await update.message.reply_text(f"⚠️ خطأ في الأرشفة للقناة: {e}")
      
        if "plan_key" in target:
            p_key = target["plan_key"]
            COURSE_FILES[p_key] = {"file_id": file_id, "type": file_type}
            save_course_files()
            await update.message.reply_text(
                f"✅ **تم الحفظ بنجاح!**\n🔑 **معرف الملف (file_id):**\n`{file_id}`",
                parse_mode="Markdown"
            )
            context.user_data.pop("waiting_for_file", None)
            return

        if "guide_key" in target:
            g_key = target["guide_key"]
            if g_key not in COURSE_FILES:
                COURSE_FILES[g_key] = {"files": []}
            if isinstance(COURSE_FILES[g_key], list):
                COURSE_FILES[g_key] = {"files": COURSE_FILES[g_key]}
            if "files" not in COURSE_FILES[g_key]:
                COURSE_FILES[g_key]["files"] = []
            
            COURSE_FILES[g_key]["files"].append({
                "file_id": file_id, 
                "type": file_type, 
                "caption": caption
            })
            save_course_files()
            total_files = len(COURSE_FILES[g_key]["files"])
            await update.message.reply_text(
                f"✅ **تم الحفظ بنجاح!** (إجمالي: {total_files})\n🔑 **معرف الملف (file_id):**\n`{file_id}`",
                parse_mode="Markdown"
            )
            return

        course_id = target["course_id"]          
        service = target["service"]          
      
        if course_id not in COURSE_FILES:          
            COURSE_FILES[course_id] = {}          
        if service not in COURSE_FILES[course_id]:          
            COURSE_FILES[course_id][service] = []          
            
        COURSE_FILES[course_id][service].append({
            "file_id": file_id, 
            "type": file_type, 
            "caption": caption
        })          
        save_course_files()
        
        total_files = len(COURSE_FILES[course_id][service])          
        await update.message.reply_text(          
            f"✅ **تم الحفظ بنجاح!** (إجمالي الملفات هنا: {total_files})\n🔑 **معرف الملف (file_id):**\n`{file_id}`",          
            parse_mode="Markdown"          
        )          
        return          

    if user_id == ADMIN_ID:
        context.user_data.pop("waiting_for_file", None)

    # التنقلات الرئيسية عبر الأزرار السفلية
    if text == "🏠 القائمة الرئيسية":
        await show_main_menu(chat_id, context, context.bot)
        return

    if text == "📚 الكتب والتجميعات والملخصات والخطط الدراسية":
        context.user_data["menu_state"] = "colleges"
        await update.message.reply_text("📚 التجميعات والملخصات والخطط الدراسية\n\nاختر الكلية أو القسم المطلوب:", reply_markup=colleges_reply_keyboard())
        return

    if text == "دليل الوصول للخدمات الإلكترونية":
        context.user_data["menu_state"] = "systems"
        await update.message.reply_text("دليل الوصول للخدمات الإلكترونية\n\nاختر الدليل الذي تريد الوصول إليه:", reply_markup=electronic_services_reply_keyboard())
        return

    if text == "🎓 دليل المستجدين":
        context.user_data["menu_state"] = "freshmen"
        await update.message.reply_text("🎓 دليل المستجدين\n\nاختر الدليل أو الخدمة التي تريد الوصول إليها:", reply_markup=freshmen_guide_reply_keyboard())
        return

    if text == "📅 التقويم الأكاديمي 1448":
        await update.message.reply_text("📅 سيتم إضافة ملف التقويم الأكاديمي 1448 هنا.")
        return

    # الكليات
    if text == "التحضيري":
        context.user_data["menu_state"] = "prep"
        await update.message.reply_text("🎓 التحضيري\n\nاختر الخطة المطلوبة:", reply_markup=preparatory_reply_keyboard())
        return

    if text in ["خطة A", "خطة B", "⚖️ تحضيري القانون والإعلام الرقمي"]:
        if text == "خطة A":
            context.user_data["menu_state"] = "plan_a"
            await update.message.reply_text("خطة A\n\nاختر المقرر المطلوب:", reply_markup=plan_a_reply_keyboard())
        elif text == "خطة B":
            context.user_data["menu_state"] = "plan_b"
            await update.message.reply_text("خطة B\n\nاختر المقرر المطلوب:", reply_markup=plan_b_reply_keyboard())
        elif text == "⚖️ تحضيري القانون والإعلام الرقمي":
            context.user_data["menu_state"] = "law_media"
            await update.message.reply_text("⚖️ تحضيري القانون والإعلام الرقمي\n\nاختر المقرر المطلوب:", reply_markup=law_media_reply_keyboard())
        return

    if text == "English - الإنجليزي":
        context.user_data["menu_state"] = "english_levels"
        await update.message.reply_text("English - الإنجليزي\n\nاختر المستوى المطلوب:", reply_markup=english_levels_reply_keyboard())
        return

    if text in ["Level 1", "Level 2", "Level 3"]:
        course_id = f"english_level_{text.split()[-1]}"
        course_name = f"English - {text}"
        context.user_data["current_course_id"] = course_id
        context.user_data["current_course"] = course_name
        context.user_data["menu_state"] = f"course:{course_id}"
        
        msg_text = f"📘 {course_name}\n\nاختر الخدمة المطلوبة:"
        markup = course_services_reply_keyboard(course_id)
        if user_id == ADMIN_ID:
            context.user_data["waiting_for_file"] = {"course_id": course_id, "service": "book"}
            msg_text += "\n\n🛠️ [وضع المطور]: اضغط على الخدمة أدناه لتفعيل الرفع."
        await update.message.reply_text(msg_text, reply_markup=markup)
        return

    if text == "كلية الحوسبة والمعلوماتية":
        context.user_data["menu_state"] = "computing"
        await update.message.reply_text("كلية الحوسبة والمعلوماتية\n\nاختر التخصص المطلوب:", reply_markup=computing_reply_keyboard())
        return

    if text in ["تقنية المعلومات - IT", "علوم الحاسب - CS", "علوم البيانات - DS"]:
        prefix_map = {"تقنية المعلومات - IT": ("it", "💻 تقنية المعلومات - IT"), "علوم الحاسب - CS": ("cs", "💻 علوم الحاسب - CS"), "علوم البيانات - DS": ("ds", "علوم البيانات - DS")}
        prefix, title = prefix_map[text]
        context.user_data["current_specialty"] = title
        context.user_data["current_specialty_prefix"] = prefix
        context.user_data["menu_state"] = f"specialty:{prefix}"
        await update.message.reply_text(f"{title}\n\nاختر الخدمة أو المستوى المطلوب:", reply_markup=levels_reply_keyboard(prefix))
        return

    if text == "كلية العلوم الصحية":
        context.user_data["menu_state"] = "health"
        await update.message.reply_text("كلية العلوم الصحية\n\nاختر التخصص المطلوب:", reply_markup=health_reply_keyboard())
        return

    if text in ["صحة عامة - Public Health", "معلوماتية صحية - Health Informatics"]:
        prefix_map = {"صحة عامة - Public Health": ("public_health", "🩺 صحة عامة"), "معلوماتية صحية - Health Informatics": ("health_informatics", "🩺 معلوماتية صحية")}
        prefix, title = prefix_map[text]
        context.user_data["current_specialty"] = title
        context.user_data["current_specialty_prefix"] = prefix
        context.user_data["menu_state"] = f"specialty:{prefix}"
        await update.message.reply_text(f"{title}\n\nاختر الخدمة أو المستوى المطلوب:", reply_markup=levels_reply_keyboard(prefix))
        return

    if text == "كلية العلوم الإدارية والمالية":
        context.user_data["menu_state"] = "business"
        await update.message.reply_text("كلية العلوم الإدارية والمالية\n\nاختر التخصص المطلوب:", reply_markup=business_reply_keyboard())
        return

    if text in ["📊 المحاسبة", "💼 إدارة الأعمال", "🛒 التجارة الإلكترونية", "📈 المالية"]:
        prefix_map = {"📊 المحاسبة": ("accounting", "📊 المحاسبة"), "💼 إدارة الأعمال": ("business_admin", "💼 إدارة الأعمال"), "🛒 التجارة الإلكترونية": ("ecommerce", "🛒 التجارة الإلكترونية"), "📈 المالية": ("finance", "📈 المالية")}
        prefix, title = prefix_map[text]
        context.user_data["current_specialty"] = title
        context.user_data["current_specialty_prefix"] = prefix
        context.user_data["menu_state"] = f"specialty:{prefix}"
        await update.message.reply_text(f"{title}\n\nاختر الخدمة أو المستوى المطلوب:", reply_markup=levels_reply_keyboard(prefix))
        return

    if text == "كلية الدراسات النظرية":
        context.user_data["menu_state"] = "theory"
        await update.message.reply_text("كلية الدراسات النظرية\n\nاختر التخصص المطلوب:", reply_markup=theory_reply_keyboard())
        return

    if text in ["⚖️ قانون", "📺 إعلام رقمي", "📝 اللغة والترجمة"]:
        prefix_map = {"⚖️ قانون": ("law", "⚖️ قانون"), "📺 إعلام رقمي": ("digital_media", "📺 إعلام رقمي"), "📝 اللغة والترجمة": ("translation", "📝 اللغة والترجمة")}
        prefix, title = prefix_map[text]
        context.user_data["current_specialty"] = title
        context.user_data["current_specialty_prefix"] = prefix
        context.user_data["menu_state"] = f"specialty:{prefix}"
        await update.message.reply_text(f"{title}\n\nاختر الخدمة أو المستوى المطلوب:", reply_markup=levels_reply_keyboard(prefix))
        return

    if text == "مواد السلم - ISLAM":
        context.user_data["menu_state"] = "islam"
        await update.message.reply_text("مواد السلم - ISLAM\n\nاختر المقرر المطلوب:", reply_markup=islam_reply_keyboard())
        return

    if text in ["المستوى الثالث", "المستوى الرابع", "المستوى الخامس", "المستوى السادس", "المستوى السابع", "المستوى الثامن"]:
        level_map = {
            "المستوى الثالث": "3", "المستوى الرابع": "4", "المستوى الخامس": "5",
            "المستوى السادس": "6", "المستوى السابع": "7", "المستوى الثامن": "8"
        }
        level = level_map[text]
        context.user_data["current_level"] = level  # حفظ المستوى الحالي لعمل زر رجوع ذكي ودقيق
        prefix = context.user_data.get("current_specialty_prefix")
        specialty = context.user_data.get("current_specialty", "التخصص")
        
        courses_dict = {}
        if prefix in COMPUTING_COURSES:
            courses_dict = COMPUTING_COURSES[prefix]
        elif prefix in HEALTH_COURSES:
            courses_dict = HEALTH_COURSES[prefix]
        elif prefix in ADMIN_FINANCIAL_COURSES:
            courses_dict = ADMIN_FINANCIAL_COURSES[prefix]
        elif prefix in THEORETICAL_COURSES:
            courses_dict = THEORETICAL_COURSES[prefix]

        courses_list = courses_dict.get(level, [])
        if not courses_list:
            await update.message.reply_text(f"{specialty}\n\n📚 المستوى {level}\n\nلا توجد مقررات مضافة لهذا المستوى حاليًا.")
            return

        context.user_data["menu_state"] = f"level:{prefix}:{level}"
        await update.message.reply_text(f"{specialty}\n\n📚 المستوى {level}\n\nاختر المقرر المطلوب:", reply_markup=courses_list_reply_keyboard(courses_list, prefix))
        return

    if text == "📄 ملف الخطة الدراسية":
        prefix = context.user_data.get("current_specialty_prefix")
        specialty = context.user_data.get("current_specialty", "التخصص")
        if not prefix:
            await update.message.reply_text("⚠️ يرجى اختيار التخصص أولاً.")
            return
        await send_plan_file(update, context, prefix, specialty)
        return

    prep_courses_map = {
        "💻 CS001 - مقدمة إلى الذكاء الاصطناعي": "cs001", "📖 CI001 - مهارات أكاديمية": "ci001", 
        "MATH001 - الرياضيات": "math001", "COM001 - مهارات الاتصال": "com001",
        "مقدمة إلى الذكاء الاصطناعي": "law_ai", "المهارات الأكاديمية": "law_academic", "الإنجليزي": "law_english",
        "ISLAM101": "islam101", "ISLAM102": "islam102", "ISLAM103": "islam103", "ISLAM104": "islam104"
    }

    if text in prep_courses_map:
        course_id = prep_courses_map[text]
        course_name = COURSES.get(course_id, text)
        context.user_data["current_course_id"] = course_id
        context.user_data["current_course"] = course_name
        context.user_data["menu_state"] = f"course:{course_id}"
        await update.message.reply_text(f"📘 {course_name}\n\nاختر الخدمة المطلوبة:", reply_markup=course_services_reply_keyboard(course_id))
        return

    found_course_id = None
    found_course_name = None
    for prefix, levels in {**COMPUTING_COURSES, **HEALTH_COURSES, **ADMIN_FINANCIAL_COURSES, **THEORETICAL_COURSES}.items():
        for lvl, clist in levels.items():
            for cid, ccode in clist:
                if ccode == text or text.endswith(ccode):
                    found_course_id = cid
                    found_course_name = ccode

    if found_course_id:
        context.user_data["current_course_id"] = found_course_id
        context.user_data["current_course"] = found_course_name
        context.user_data["menu_state"] = f"course:{found_course_id}"
        await update.message.reply_text(f"📘 المقرر: {found_course_name}\n\nاختر الخدمة المطلوبة:", reply_markup=course_services_reply_keyboard(found_course_id))
        return

    if text in ["📘 الكتاب", "📚 الملخصات"]:
        service_map = {"📘 الكتاب": "book", "📚 الملخصات": "summary"}
        service = service_map[text]
        course_id = context.user_data.get("current_course_id")
        course_name = context.user_data.get("current_course", "المقرر")

        if not course_id:
            await update.message.reply_text("⚠️ لم يتم تحديد المقرر، يرجى العودة للقائمة الرئيسية.")
            return

        if user_id == ADMIN_ID:
            context.user_data["waiting_for_file"] = {"course_id": course_id, "service": service}
            await update.message.reply_text(
                f"🛠️ [وضع المطور - جاهز للرفع]\n"
                f"📁 المقرر: {course_name} | القسم: {text}\n"
                f"📥 أرسل الملف الآن وسيتم استخراج معرفه."
            )

        await send_service_files(update, context, course_id, course_name, service)
        return

    if text == "🧩 تجميعات":
        course_id = context.user_data.get("current_course_id")
        course_name = context.user_data.get("current_course", "المقرر")

        if not course_id:
            await update.message.reply_text("⚠️ لم يتم تحديد المقرر، يرجى العودة للقائمة الرئيسية.")
            return

        if course_id == "math001":
            context.user_data["menu_state"] = "math_collections"
            await update.message.reply_text("🧩 تجميعات المقرر\n\nاختر القسم المطلوب:", reply_markup=math_collections_reply_keyboard())
            return
        
        service = "collections"
        if user_id == ADMIN_ID:
            context.user_data["waiting_for_file"] = {"course_id": course_id, "service": service}
            await update.message.reply_text(f"🛠️ [وضع المطور] أرسل ملفات التجميعات الخاصة بـ ({course_name}) هنا:")

        await send_service_files(update, context, course_id, course_name, service)
        return

    if text == "📄 تجميعات الواجبات":
        context.user_data["menu_state"] = "math_hw_list"
        await update.message.reply_text("📁 تجميعات الواجبات\n\nاختر الواجب المطلوب:", reply_markup=math_hw_reply_keyboard())
        return

    if text in ["📄 تجميعات الميد", "📄 تجميعات الفاينال"]:
        service_map = {"📄 تجميعات الميد": "math_mid", "📄 تجميعات الفاينال": "math_final"}
        service = service_map[text]
        course_id = context.user_data.get("current_course_id")
        course_name = context.user_data.get("current_course", "المقرر")
        
        if user_id == ADMIN_ID:
            context.user_data["waiting_for_file"] = {"course_id": course_id, "service": service}
            await update.message.reply_text(f"🛠️ [وضع المطور] أرسل ملفات {text} الآن:")
        
        await send_service_files(update, context, course_id, course_name, service)
        return

    hw_map = {
        "تجميعات الواجب الأول": "math_hw_1", "تجميعات الواجب الثاني": "math_hw_2", 
        "تجميعات الواجب الثالث": "math_hw_3", "تجميعات الواجب الرابع": "math_hw_4", 
        "تجميعات الواجب الخامس": "math_hw_5"
    }
    if text in hw_map:
        service = hw_map[text]
        course_id = context.user_data.get("current_course_id")
        course_name = context.user_data.get("current_course", "المقرر")
        if user_id == ADMIN_ID:
            context.user_data["waiting_for_file"] = {"course_id": course_id, "service": service}
            await update.message.reply_text(f"🛠️ [وضع المطور] أرسل ملفات {text} الآن:")
        await send_service_files(update, context, course_id, course_name, service)
        return

    if text == "🔗 طريقة الدخول لواجبات الماث":
        await update.message.reply_text("🔗 **طريقة الدخول لواجبات الماث**\n\nسيتم إضافة الشرح هنا.", parse_mode="Markdown")
        return

    systems_map = {
        "طريقة تسجيل المواد": "guide_reg", "طريقة سداد الرسوم": "guide_payment",
        "طريقة الوصول للجدول الدراسي": "guide_schedule", "طريقة رفع اعذار التغيب عن الاختبارات": "guide_excuse",
        "كيفية استخراج افادة": "guide_statement", "طريقة تصفح الشعب": "guide_sections"
    }
    
    if text in systems_map:
        guide_key = systems_map[text]
        if user_id == ADMIN_ID:
            context.user_data["waiting_for_file"] = {"guide_key": guide_key, "guide_title": text}
            await update.message.reply_text(f"🛠️ [وضع المطور] جاهز لاستقبال ملفات قسم: **{text}**.", parse_mode="Markdown")
        
        await send_system_guide_files(update, context, guide_key, text)
        return

    freshmen_map = {
        "تطبيق البلاك بورد": "دليل تطبيق البلاك بورد.",
        "مواصفات اللابتوب المطلوب": "مواصفات اللابتوب المطلوب للدراسة.",
        "طريقة تفعيل الحساب الجامعي": "خطوات تفعيل الحساب الجامعي.",
        "خطوات تفعيل البريد الجامعي": "خطوات تفعيل البريد الجامعي.",
        "طريقة حضور المحاضرات": "طريقة حضور المحاضرات الافتراضية.",
        "شروط معادلة المواد": "شروط وضوابط معادلة المواد.",
        "ستيب - STEP": "معلومات اختبار القدرات لغير الناطقين أو اختبار STEP."
    }
    
    if text == "قروب الاستفسارات والإجابة على اسئلتكم":
        whatsapp_kb = InlineKeyboardMarkup([
            [InlineKeyboardButton("💬 اضغط هنا للانتقال إلى قروب الاستفسارات", url=WHATSAPP_GROUP_URL)]
        ])
        await update.message.reply_text("💬 **قروب الاستفسارات والإجابة على اسئلتكم**\n\nانضم مباشرة عبر الزر أدناه:", reply_markup=whatsapp_kb, parse_mode="Markdown")
        return

    if text == "قناة الأخبار الهامة للمستجدين على واتساب":
        channel_kb = InlineKeyboardMarkup([
            [InlineKeyboardButton("📢 اضغط هنا للانتقال إلى قناة الأخبار", url=WHATSAPP_CHANNEL_URL)]
        ])
        await update.message.reply_text("📢 **قناة الأخبار الهامة للمستجدين**\n\nتابع آخر الأخبار عبر الزر أدناه:", reply_markup=channel_kb, parse_mode="Markdown")
        return

    if text in freshmen_map:
        await update.message.reply_text(f"🎓 **{text}**\n\n{freshmen_map[text]}", parse_mode="Markdown")
        return

    # =========================================================          
    # زر الرجوع الذكي والمضبوط بدقة تامة (بدون أي أخطاء أو قفزات)
    # =========================================================          
    if text == "⬅️ رجوع":
        state = context.user_data.get("menu_state", "main")
        
        if state == "colleges":
            await show_main_menu(chat_id, context, context.bot)
        elif state in ["systems", "freshmen"]:
            await show_main_menu(chat_id, context, context.bot)
        elif state == "prep":
            context.user_data["menu_state"] = "colleges"
            await update.message.reply_text("📚 التجميعات والملخصات والخطط الدراسية\n\nاختر الكلية أو القسم المطلوب:", reply_markup=colleges_reply_keyboard())
        elif state in ["plan_a", "plan_b", "law_media"]:
            context.user_data["menu_state"] = "prep"
            await update.message.reply_text("🎓 التحضيري\n\nاختر الخطة المطلوبة:", reply_markup=preparatory_reply_keyboard())
        elif state == "english_levels":
            context.user_data["menu_state"] = "plan_a"
            await update.message.reply_text("خطة A\n\nاختر المقرر المطلوب:", reply_markup=plan_a_reply_keyboard())
        elif state in ["computing", "health", "business", "theory", "islam"]:
            context.user_data["menu_state"] = "colleges"
            await update.message.reply_text("📚 التجميعات والملخصات والخطط الدراسية\n\nاختر الكلية أو القسم المطلوب:", reply_markup=colleges_reply_keyboard())
        elif state.startswith("specialty:"):
            prefix = state.split(":")[1]
            if prefix in ["it", "cs", "ds"]:
                context.user_data["menu_state"] = "computing"
                await update.message.reply_text("كلية الحوسبة والمعلوماتية\n\nاختر التخصص المطلوب:", reply_markup=computing_reply_keyboard())
            elif prefix in ["public_health", "health_informatics"]:
                context.user_data["menu_state"] = "health"
                await update.message.reply_text("كلية العلوم الصحية\n\nاختر التخصص المطلوب:", reply_markup=health_reply_keyboard())
            elif prefix in ["accounting", "business_admin", "ecommerce", "finance"]:
                context.user_data["menu_state"] = "business"
                await update.message.reply_text("كلية العلوم الإدارية والمالية\n\nاختر التخصص المطلوب:", reply_markup=business_reply_keyboard())
            elif prefix in ["law", "digital_media", "translation"]:
                context.user_data["menu_state"] = "theory"
                await update.message.reply_text("كلية الدراسات النظرية\n\nاختر التخصص المطلوب:", reply_markup=theory_reply_keyboard())
            else:
                context.user_data["menu_state"] = "colleges"
                await update.message.reply_text("📚 التجميعات والملخصات والخطط الدراسية\n\nاختر الكلية أو القسم المطلوب:", reply_markup=colleges_reply_keyboard())
        elif state.startswith("level:"):
            parts = state.split(":")
            prefix = parts[1]
            context.user_data["menu_state"] = f"specialty:{prefix}"
            title_map = {
                "it": "💻 تقنية المعلومات - IT", "cs": "💻 علوم الحاسب - CS", "ds": "علوم البيانات - DS",
                "public_health": "🩺 صحة عامة", "health_informatics": "🩺 معلوماتية صحية",
                "accounting": "📊 المحاسبة", "business_admin": "💼 إدارة الأعمال", "ecommerce": "🛒 التجارة الإلكترونية", "finance": "📈 المالية",
                "law": "⚖️ قانون", "digital_media": "📺 إعلام رقمي", "translation": "📝 اللغة والترجمة"
            }
            title = title_map.get(prefix, "التخصص")
            await update.message.reply_text(f"{title}\n\nاختر الخدمة أو المستوى المطلوب:", reply_markup=levels_reply_keyboard(prefix))
        elif state.startswith("course:"):
            course_id = state.split(":")[1]
            if course_id.startswith("english_level_"):
                context.user_data["menu_state"] = "english_levels"
                await update.message.reply_text("English - الإنجليزي\n\nاختر المستوى المطلوب:", reply_markup=english_levels_reply_keyboard())
            elif course_id in ["cs001", "ci001"]:
                context.user_data["menu_state"] = "plan_a"
                await update.message.reply_text("خطة A\n\nاختر المقرر المطلوب:", reply_markup=plan_a_reply_keyboard())
            elif course_id in ["math001", "com001"]:
                context.user_data["menu_state"] = "plan_b"
                await update.message.reply_text("خطة B\n\nاختر المقرر المطلوب:", reply_markup=plan_b_reply_keyboard())
            elif course_id in ["law_ai", "law_academic", "law_english"]:
                context.user_data["menu_state"] = "law_media"
                await update.message.reply_text("⚖️ تحضيري القانون والإعلام الرقمي\n\nاختر المقرر المطلوب:", reply_markup=law_media_reply_keyboard())
            elif course_id.startswith("islam"):
                context.user_data["menu_state"] = "islam"
                await update.message.reply_text("مواد السلم - ISLAM\n\nاختر المقرر المطلوب:", reply_markup=islam_reply_keyboard())
            else:
                # عودة دقيقة لقائمة مواد المستوى بدلاً من الكليات مباشرة
                prefix = context.user_data.get("current_specialty_prefix")
                level = context.user_data.get("current_level", "3")
                specialty = context.user_data.get("current_specialty", "التخصص")
                if prefix:
                    courses_dict = {}
                    if prefix in COMPUTING_COURSES:
                        courses_dict = COMPUTING_COURSES[prefix]
                    elif prefix in HEALTH_COURSES:
                        courses_dict = HEALTH_COURSES[prefix]
                    elif prefix in ADMIN_FINANCIAL_COURSES:
                        courses_dict = ADMIN_FINANCIAL_COURSES[prefix]
                    elif prefix in THEORETICAL_COURSES:
                        courses_dict = THEORETICAL_COURSES[prefix]
                    courses_list = courses_dict.get(level, [])
                    context.user_data["menu_state"] = f"level:{prefix}:{level}"
                    await update.message.reply_text(f"{specialty}\n\n📚 المستوى {level}\n\nاختر المقرر المطلوب:", reply_markup=courses_list_reply_keyboard(courses_list, prefix))
                else:
                    context.user_data["menu_state"] = "colleges"
                    await update.message.reply_text("📚 التجميعات والملخصات والخطط الدراسية\n\nاختر الكلية أو القسم المطلوب:", reply_markup=colleges_reply_keyboard())
        elif state == "math_hw_list":
            context.user_data["menu_state"] = "math_collections"
            await update.message.reply_text("🧩 تجميعات المقرر\n\nاختر القسم المطلوب:", reply_markup=math_collections_reply_keyboard())
        elif state == "math_collections":
            course_id = context.user_data.get("current_course_id", "")
            context.user_data["menu_state"] = f"course:{course_id}"
            await update.message.reply_text("📘 خدمات المقرر\n\nاختر الخدمة المطلوبة:", reply_markup=course_services_reply_keyboard(course_id))
        else:
            await show_main_menu(chat_id, context, context.bot)
        return


# =========================================================          
# معالجة الأزرار الشفافة وحذف الملفات
# =========================================================          
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):          
    query = update.callback_query          
    user_id = query.from_user.id
    chat_id = query.message.chat_id
    data = query.data

    if data == "check_membership":          
        member = await is_member(context.bot, user_id)          
        if not member:          
            await query.answer("لم تقم بالانضمام بعد.", show_alert=True)          
            return          
        await query.answer("تم التحقق بنجاح ✅")          
        await show_main_menu(chat_id, context, context.bot)
        return

    if user_id == ADMIN_ID:
        if data.startswith("del_plan:"):
            plan_key = data.split(":")[1]
            if plan_key in COURSE_FILES:
                COURSE_FILES.pop(plan_key, None)
                save_course_files()
                await query.answer("تم حذف ملف الخطة بنجاح ✅", show_alert=True)
                return
            await query.answer("عذراً، لم يتم العثور على الملف.", show_alert=True)
            return

        if data.startswith("del_course:"):
            parts = data.split(":")
            c_id = parts[1]
            serv = parts[2]
            idx = int(parts[3])

            if c_id in COURSE_FILES and serv in COURSE_FILES[c_id]:
                if 0 <= idx < len(COURSE_FILES[c_id][serv]):
                    COURSE_FILES[c_id][serv].pop(idx)
                    save_course_files()
                    await query.answer("تم حذف الملف بنجاح ✅", show_alert=True)
                    return
            await query.answer("عذراً، لم يتم العثور على الملف.", show_alert=True)
            return

        elif data.startswith("del_guide:"):
            parts = data.split(":")
            g_key = parts[1]
            idx = int(parts[2])

            if g_key in COURSE_FILES and "files" in COURSE_FILES[g_key]:
                if 0 <= idx < len(COURSE_FILES[g_key]["files"]):
                    COURSE_FILES[g_key]["files"].pop(idx)
                    save_course_files()
                    await query.answer("تم حذف الملف بنجاح ✅", show_alert=True)
                    return
            await query.answer("عذراً، لم يتم العثور على الملف.", show_alert=True)
            return


# =========================================================          
# تشغيل البوت          
# =========================================================          
         
def main():
    if not BOT_TOKEN or BOT_TOKEN == "ضع_توكن_البوت_هنا":
        print("❌ ضع BOT_TOKEN أولاً داخل الكود.")
        return

    print("جاري تشغيل البوت...")
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_messages))
    app.add_handler(MessageHandler(
        filters.Document.ALL | filters.PHOTO | filters.VIDEO | filters.AUDIO,
        handle_messages
    ))

    print("✅ تم تشغيل البوت بنجاح.")
    app.run_polling(drop_pending_updates=True)


if __name__ == "__main__":
    main()