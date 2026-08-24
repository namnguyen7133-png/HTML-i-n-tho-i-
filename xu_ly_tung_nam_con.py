import time
import os
import random
from datetime import datetime

NAM_BAT_DAU = 2007
NAM_KET_THUC = 2026
LOG_FILE = r"D:\LICH\nhat_ky_he_thong.txt"

def khung_long_keu_cuu (retry_mechanism):
    """Chiến lược chờ ngẫu nhiên và thử lại (Exponential Backoff) chống lỗi 429/503"""
    thoi_gian_cho = random.randint(5, 10)
    print(f"🦖 [Cảnh báo quá tải/Rate Limiting]: Server đang mệt, khủng long đang ngủ đông {thoi_gian_cho} giây để né lỗi 429...")
    time.sleep(thoi_gian_cho)

def om_tron_du_lieu (batch_fetcher):
    """Xử lý cuốn chiếu từng năm, chia nhỏ 200 dòng 1 lần"""
    for nam in range(NAM_BAT_DAU, NAM_KET_THUC + 1):
        print(f"\n========================================")
        print(f"📅 Đang bốc dữ liệu thời tiết của năm: {nam}")
        print(f"========================================")
        
        # Giả lập chia 200 dòng một lần cho mỗi năm
        tong_so_lo = 5 # Giả sử mỗi năm chia làm 5 lô dữ liệu
        for lo in range(1, tong_so_lo + 1):
            print(f"   -> Đang xử lý lô {lo}/{tong_so_lo} của năm {nam} (200 dòng/lần)...")
            
            # Mô phỏng gọi API chống treo / lỗi mạng ngẫu nhiên
            thanh_cong = False
            lan_thu = 0
            while not thanh_cong and lan_thu < 3:
                try:
                    # Chỗ này gắn code lấy dữ liệu thật từ web theo tháng/tuần của năm tương ứng
                    time.sleep(0.5) # Giả lập thời gian tải mượt mà
                    thanh_cong = True
                except Exception:
                    lan_thu += 1
                    khung_long_keu_cuu("retry")
            
            # Ghi nhật ký tiến trình vào file hệ thống
            try:
                with open(LOG_FILE, 'a', encoding='utf-8') as f:
                    f.write(f"[{datetime.now()}] Hoàn thành năm {nam} - Lô {lo}\n")
            except:
                pass
                
        print(f"✅ Đã xong năm {nam}! Tạm nghỉ nửa nhịp cho máy thở...")
        time.sleep(1)

if __name__ == "__main__":
    om_tron_du_lieu("start_batch")