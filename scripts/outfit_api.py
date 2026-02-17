from fastapi import FastAPI
import gspread
from google.oauth2.service_account import Credentials
import random

# ===== SHEET =====
SHEET_URL = "https://docs.google.com/spreadsheets/d/1IsDeK73L5vbsoNCoqHkKfn_HMffGR4bxNqtowydX7Rc"

scope = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

creds = Credentials.from_service_account_file("credentials.json", scopes=scope)
gc = gspread.authorize(creds)
sheet = gc.open_by_url(SHEET_URL).worksheet("sheet_thoi_trang")

data = sheet.get_all_records()

app = FastAPI()


# ===== RULE =====
def rule(temp):
    if temp >= 30:
        return "hot"
    if temp >= 25:
        return "warm"
    if temp >= 20:
        return "cool"
    return "cold"


# ===== AI SELECT =====
def ai_pick(temp):
    r = rule(temp)

    if r == "hot":
        pool = [d for d in data if "áo thun" in d["ao"]]
    elif r == "warm":
        pool = [d for d in data if "áo thun" in d["ao"] or "sơ mi" in d["ao"]]
    elif r == "cool":
        pool = [d for d in data if "sơ mi" in d["ao"]]
    else:
        pool = [d for d in data if "khoác" in d["ao"]]

    if pool:
        return random.choice(pool)

    return {"ao":"áo thun","quan":"quần jean","giay":"sneaker"}


# ===== API =====
@app.get("/outfit")
def get_outfit(temp: float):
    o = ai_pick(temp)
    return {
        "ao": o.get("ao",""),
        "quan": o.get("quan",""),
        "giay": o.get("giay","")
    }


# ===== CHATBOT =====
@app.get("/chat")
def chat(q: str):
    q=q.lower()

    if "nhiệt" in q:
        try:
            t=float(q.split()[-1])
            o=ai_pick(t)
            return {"reply":f"Nhiệt {t}°C: {o['ao']} + {o['quan']}"}
        except:
            return {"reply":"Bạn nhập: nhiệt 30"}

    if "mặc gì" in q:
        o=ai_pick(28)
        return {"reply":f"Gợi ý: {o['ao']} + {o['quan']}"}

    return {"reply":"Hỏi: nhiệt 30 hoặc mặc gì"}
