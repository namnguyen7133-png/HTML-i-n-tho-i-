from collections import defaultdict
import datetime
import io
import os
import sqlite3
import sys

import requests
# Đọc API_KEY trực tiếp từ file weather_api.txt
API_KEY_PATH = r"D:\HE_THONG_HO_TRO_RA_QUYET_DINH\00_SECRET\weather_api.txt"
with open(API_KEY_PATH, "r", encoding="utf-8") as f:
    API_KEY = f.read().strip()

# Cấu hình encoding hiển thị tiếng Việt
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
DB_PATH = r"D:\NHACVIEC_PYTHON\THOITIET.db"


def get_week_forecast():
  url = f"https://api.openweathermap.org/data/2.5/forecast?q=Hanoi&appid={API_KEY}&units=metric&lang=vi"
  try:
    r = requests.get(url, timeout=10).json()
    daily_map = defaultdict(lambda: {"rain": 0, "rain_hours": []})
    for item in r["list"]:
      dt_parts = item["dt_txt"].split(" ")
      date = dt_parts[0]
      time_str = dt_parts[1][:5]  # Định dạng HH:MM

      rain_3h = item.get("rain", {}).get("3h", 0)
      if rain_3h > 0:
        daily_map[date]["rain"] += rain_3h
        daily_map[date]["rain_hours"].append(f"{time_str} ({rain_3h}mm)")
    return daily_map
  except Exception as D:
    print(f"Lỗi khi lấy dữ liệu thời tiết từ Web: {e}")
    return {}


def cap_nhat_gio_mua_theo_ngay():
  if not os.path.exists(DB_PATH):
    print("Không tìm thấy cơ sở dữ liệu trên ổ E!")
    return

  web_data = get_week_forecast()
  if not web_data:
    print("Không lấy được dữ liệu từ Web để cập nhật.")
    return

  conn = sqlite3.connect(DB_PATH)
  cur = conn.cursor()

  # Đảm bảo có cột rain_hours
  cur.execute("PRAGMA table_info(THOITIET_DINH_DUONG)")
  columns = [col[1] for col in cur.fetchall()]
  if "rain_hours" not in columns:
    cur.execute("ALTER TABLE THOITIET_DINH_DUONG ADD COLUMN rain_hours TEXT")
    conn.commit()

  print("Đang cập nhật giờ mưa tích lũy vào DB theo ngày...")
  for date_str, w in web_data.items():
    rain_hours_str = (
        ", ".join(w["rain_hours"]) if w["rain_hours"] else "Không mưa"
    )

    # Cập nhật trực tiếp vào ngày tương ứng trong DB
    update_query = """
            UPDATE THOITIET_DINH_DUONG 
            SET rain_hours = ? 
            WHERE date(time) = ?
        """
    cur.execute(update_query, (rain_hours_str, date_str))
    print(f"-> Ngày {date_str}: Đã cập nhật giờ mưa [{rain_hours_str}]")

  conn.commit()
  conn.close()
  print("Hoàn tất quá trình cập nhật giờ mưa vào DB!")


if __name__ == "__main__":
  cap_nhat_gio_mua_theo_ngay()