import os
from datetime import datetime, timedelta

# --- CẤU HÌNH ĐƯỜNG DẪN ---
THU_MUC_DICH = r"D:\NHACVIEC_PYTHON"
FILE_KET_QUA = os.path.join(THU_MUC_DICH, "thuc_don_nguoi_linh.html")
DUONG_DAN_TXT = r"D:\LICH\nhat_ky_he_thong.txt"

def ghi_nhat_ky(trang_thai):
    try:
        os.makedirs(os.path.dirname(DUONG_DAN_TXT), exist_ok=True)
        thoi_gian = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(DUONG_DAN_TXT, 'a', encoding='utf-8') as f:
            f.write(f"{thoi_gian} | Trạng thái: {trang_thai} | Tệp: {FILE_KET_QUA}\n")
    except Exception as e:
        print(f"Lỗi ghi nhật ký: {e}")

def tao_html_ca_tuan():
    thoi_gian_cap_nhat = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ngay_hien_tai = datetime.now()
    
    # Kiểm tra nếu file đã tồn tại và chưa qua 7 ngày thì giữ nguyên, quá 7 ngày thì xóa tạo mới
    if os.path.exists(FILE_KET_QUA):
        thoi_gian_sua_cuoi = datetime.fromtimestamp(os.path.getmtime(FILE_KET_QUA))
        if datetime.now() - thoi_gian_sua_cuoi < timedelta(days=7):
            print(f"ℹ️ Tệp HTML chưa qua 1 tuần (Cập nhật lần cuối: {thoi_gian_sua_cuoi.strftime('%Y-%m-%d')}). Giữ nguyên.")
            ghi_nhat_ky("Bỏ qua - Chưa đủ chu kỳ 1 tuần")
            return
        else:
            print("🔄 Đã qua 1 tuần! Tiến hành xóa dữ liệu cũ và nạp trọn gói 1 tuần mới...")

    # TỰ ĐỘNG QUÉT TOÀN BỘ FILE HTML TRONG THƯ MỤC D:\NHACVIEC_PYTHON\
    danh_sach_option = '<option value="">📁 Kho Thực Đơn & Chuyên Đề Tự Động Quét...</option>\n'
    if os.path.exists(THU_MUC_DICH):
        for file in sorted(os.listdir(THU_MUC_DICH)):
            if file.endswith(".html") and file != "thuc_don_nguoi_linh.html":
                # Lấy tên file làm nhãn hiển thị (bỏ phần đuôi .html)
                ten_hien_thi = file.replace(".html", "").replace("-", " ").title()
                # Sử dụng đường dẫn tương đối (chỉ tên file) để tránh bị trình duyệt chặn bảo mật
                danh_sach_option += f'            <option value="{file}">{ten_hien_thi}</option>\n'

    # Tạo danh sách dữ liệu cho 7 ngày trong tuần
    cac_ngay_trong_tuan = ""
    for i in range(7):
        ngay_lap = ngay_hien_tai + timedelta(days=i)
        chu_str = ngay_lap.strftime("%Y-%m-%d")
        
        cac_ngay_trong_tuan += f"""
        <tr>
            <td><b>{chu_str}</b></td>
            <td>32.6/25.8°C</td>
            <td>12.8mm</td>
            <td>06:00 (3.19mm), 09:00 (1.06mm), 12:00 (0.52mm)</td>
            <td>TB: 31.5/25.5°C (từ 19 năm)</td>
            <td><pre style="font-family:inherit; margin:0;">--- TRỜI MƯA/ẨM ƯỚT ---
Mua sắm: Gừng, khoai lang, chuối, sữa ấm, trà gừng.
Thực đơn: Cháo gừng, khoai luộc, súp nóng, thịt nướng, bún trà, lương khô, ruốc, muối vừng.
Thuốc phụ trợ: Siro ho thảo dược, Trà gừng, Vitamin C.
Lưu ý: Người mỏi mệt, lưng mỏi đau: bôi dầu gió, thuốc cảm delcolgel, paracetamol, cảm xuyên hương, cà phê sữa tối.</pre></td>
        </tr>
        """

    khung_html = f"""<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Thực Đơn & Sức Khỏe Người Lính</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; background-color: #f4f6f9; color: #333; }}
        h1, h2 {{ color: #2c3e50; }}
        .card {{ background: #fff; padding: 20px; margin-bottom: 20px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }}
        .emergency {{ background: #ffebee; border-left: 6px solid #c0392b; padding: 15px; margin-bottom: 20px; border-radius: 4px; }}
        .emergency h3 {{ color: #c0392b; margin-top: 0; }}
        table {{ width: 100%; border-collapse: collapse; margin-top: 10px; background: #fff; }}
        th, td {{ border: 1px solid #ddd; padding: 12px; text-align: left; vertical-align: top; }}
        th {{ background-color: #2c3e50; color: white; }}
        tr:nth-child(even) {{ background-color: #f9f9f9; }}
    </style>
</head>
<body>

    <h1>🛡️ TRANG THÔNG TIN THỜI TIẾT & THỰC ĐƠN NGƯỜI LÍNH</h1>
    
    <!-- Thanh Menu Tự Động Quét File Tương Đối -->
    <div style="background: #ffffff; padding: 12px 15px; margin-bottom: 20px; border: 1px solid #dcdcdc; border-radius: 8px; display: flex; flex-wrap: wrap; gap: 10px; align-items: center; box-shadow: 0 1px 3px rgba(0,0,0,0.05);">
        
        <a href="thuc_don_nguoi_linh.html" style="background: #2c3e50; color: white; padding: 6px 12px; text-decoration: none; border-radius: 4px; font-weight: bold; font-size: 13px;">🏠 Trang Chủ</a>

        <span style="color: #ccc;">|</span>
        
        <select onchange="if(this.value) window.location.href=this.value;" style="padding: 6px 10px; border-radius: 4px; border: 1px solid #ccc; font-size: 13px; background: #f8f9fa; cursor: pointer;">
{danh_sach_option}
        </select>
    </div>

    <div class="emergency">
        <h3>🚨 GÓC CẤP CỨU NHANH: KHI BỊ CẢM LẠNH, MỆT MỎI, VỪA ĐI TÀU XE HOẶC NGOÀI TRỜI VỀ</h3>
        <p><b>Triệu chứng:</b> Người mệt lả không muốn dậy, buồn nôn do say xe/tàu, ngủ gật, uể oải, muốn đi nằm ngay lập tức sau khi di chuyển dài hoặc đi ngoài trời về. Đêm mở điều hòa sáng hôm sau bị đau mỏi.</p>
        <p><b>Quy trình xử lý & Cứu chữa nhanh:</b></p>
        <ul>
            <li><b>Nghỉ ngơi ngay:</b> Vào giường nằm đắp chăn ngay lập tức, không cố gượng sức.</li>
            <li><b>Chống say xe, chống mệt mỏi & ngủ gật:</b> Uống ngay <b>viên đạm tổng hợp</b> để bù năng lượng nhanh chóng, chống say xe/tàu, giữ tỉnh táo và xua tan cảm giác ngủ gật, uể oải sau hành trình dài.</li>
            <li><b>Xoa bóp cơ thể:</b> Xoa dầu gió (dầu nóng) vào lòng bàn chân, thái dương, cổ và vùng lưng mỏi đau.</li>
            <li><b>Làm ấm cơ thể từ bên trong:</b> Uống ngay một cốc nước trà gừng ấm hoặc nước gừng mật ong.</li>
            <li><b>Ăn uống bồi bổ:</b> Ăn một bát xôi nóng, cháo gừng nóng hoặc súp nóng để nhanh chóng hồi phục năng lượng.</li>
            <li><b>Hỗ trợ tiêu hóa / Cảm mạo:</b> Uống bổ sung thuốc theo tình trạng (ví dụ: thuốc cảm, Cảm xuyên hương, hoặc thuốc Beberin nếu có vấn đề về tiêu hóa).</li>
        </ul>
    </div>

    <div class="card">
        <h2>📊 Bảng Dự Báo Thời Tiết & Gợi Ý Dinh Dưỡng Cả Tuần (Cập nhật lúc: {thoi_gian_cap_nhat})</h2>
        <table>
            <thead>
                <tr>
                    <th>Ngày</th>
                    <th>Dự Báo (Max/Min)</th>
                    <th>Mưa</th>
                    <th>Khung Giờ Mưa</th>
                    <th>Lịch Sử (Từ 2007)</th>
                    <th>Gợi Ý Mua Sắm & Thực Đơn</th>
                </tr>
            </thead>
            <tbody>
                {cac_ngay_trong_tuan}
            </tbody>
        </table>
    </div>

</body>
</html>"""

    os.makedirs(THU_MUC_DICH, exist_ok=True)
    with open(FILE_KET_QUA, "w", encoding="utf-8") as f:
        f.write(khung_html)
    print("✓ Đã quét và nạp toàn bộ tệp HTML trong D:\\NHACVIEC_PYTHON\\ vào menu thành công!")
    ghi_nhat_ky("Thành công - Tự động quét file HTML vào menu")

if __name__ == "__main__":
    tao_html_ca_tuan()