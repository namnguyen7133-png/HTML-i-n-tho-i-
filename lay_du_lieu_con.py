import time

def om_tron_du_lieu (batch_fetcher):
    total_years = 19
    lines_per_batch = 200
    
    print(f"Bắt đầu gom dữ liệu theo từng lô {lines_per_batch} dòng...")
    
    for i in range(1, 1001): # Ví dụ chạy 1000 lượt
        print(f"Đang xử lý lô dữ liệu thứ {i}...")
        # Ở đây bạn chèn logic gọi API thời tiết
        time.sleep(1) # Giả lập chờ mạng
        
        if i % 10 == 0:
            print("--- Nghỉ giải lao một chút cho server đỡ nóng máy ---")
            time.sleep(2)

if __name__ == "__main__":
    om_tron_du_lieu("start")