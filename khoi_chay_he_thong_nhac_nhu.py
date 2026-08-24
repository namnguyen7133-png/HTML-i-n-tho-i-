import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import os
import time
import threading
import winsound
from datetime import datetime

# --- ĐƯỜNG DẪN HỆ THỐNG ---
DUONG_DAN_LOG = r"D:\LICH\nhat_ky_he_thong.txt"
CONFIG_LUU_TRU = r"D:\HE_THONG_HO_TRO_RA_QUYET_DINH\00_SECRET\cau_hinh_nguoi_dung.txt"

class UngDungNhacNhoThannToc:
    def __init__(self, root):
        self.root = root
        self.root.title("QUẢN LÝ LỊCH NHẮC NHỔ - NAM (Siêu Cấp Chạy Ngầm)")
        self.root.geometry("950x750")
        
        # Biến trạng thái đếm giờ
        self.remaining_seconds = 0
        self.is_running = False
        self.timer_id = None

        # --- GIAO DIỆN CHÍNH (Chữ to rõ cho người cận thị) ---
        font_tieu_de = ("Arial", 14, "bold")
        font_noi_dung = ("Arial", 12)
        font_so_to = ("Arial", 30, "bold")

        # Khung 1: Tạo lịch nhắc mới
        frm_tao = ttk.LabelFrame(root, text=" 📝 TẠO LỊCH NHẮC NHỎ MỚI ")
        frm_tao.pack(fill="x", padx=10, pady=5)

        ttk.Label(frm_tao, text="Nội dung công việc:", font=font_noi_dung).grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.ent_noi_dung = ttk.Entry(frm_tao, width=40, font=font_noi_dung)
        self.ent_noi_dung.grid(row=0, column=1, sticky="w", padx=5, pady=5)

        ttk.Label(frm_tao, text="Cấu hình phút:", font=font_noi_dung).grid(row=1, column=0, sticky="w", padx=5, pady=5)
        self.ent_phut = ttk.Entry(frm_tao, width=15, font=font_noi_dung)
        self.ent_phut.insert(0, "15")
        self.ent_phut.grid(row=1, column=1, sticky="w", padx=5, pady=5)

        ttk.Button(frm_tao, text="💾 Lưu Lịch & Chạy Ngầm Tự Động", command=self.luu_va_chay_ngam).grid(row=2, column=0, columnspan=2, pady=10)

        # Khung 2: Bộ đếm giờ chi tiết cho từng việc (Chạy / Tạm dừng)
        frm_timer = ttk.LabelFrame(root, text=" ⏱ BỘ BẤM GIỜ CHI TIẾT (Bấm dừng / Chạy cho từng việc) ")
        frm_timer.pack(fill="x", padx=10, pady=5)

        self.lbl_time = tk.Label(frm_timer, text="00:15:00", font=font_so_to, fg="red")
        self.lbl_time.pack(pady=5)

        frm_nut_timer = ttk.Frame(frm_timer)
        frm_nut_timer.pack(pady=5)
        
        self.btn_start = ttk.Button(frm_nut_timer, text="▶ Bắt đầu đếm", command=self.start_timer)
        self.btn_start.pack(side="left", padx=5)
        self.btn_pause = ttk.Button(frm_nut_timer, text="⏸ Tạm dừng", command=self.pause_timer, state="disabled")
        self.btn_pause.pack(side="left", padx=5)
        self.btn_reset = ttk.Button(frm_nut_timer, text="🔄 Đặt lại", command=self.reset_timer)
        self.btn_reset.pack(side="left", padx=5)

        # Khung 3: Danh sách lịch đã lưu
        frm_danh_sach = ttk.LabelFrame(root, text=" 📋 DANH SÁCH LỊCH NHẮC ĐÃ LƯU HỆ THỐNG ")
        frm_danh_sach.pack(fill="both", expand=True, padx=10, pady=5)

        columns = ("thoigian", "noidung", "kieunhac", "trangthai")
        self.tree = ttk.Treeview(frm_danh_sach, columns=columns, show="headings", height=8)
        self.tree.heading("thoigian", text="Thời gian tạo")
        self.tree.heading("noidung", text="Nội dung công việc")
        self.tree.heading("kieunhac", text="Kiểu nhắc")
        self.tree.heading("trangthai", text="Tệp / Trạng thái (Đang chạy ngầm)")
        
        self.tree.column("thoigian", width=150)
        self.tree.column("noidung", width=250)
        self.tree.column("kieunhac", width=150)
        self.tree.column("trangthai", width=250)
        self.tree.pack(fill="both", expand=True, padx=5, pady=5)

        # Thêm mẫu dữ liệu giả lập sẵn cho ngài thấy
        self.tree.insert("", "end", values=("2026-08-17 13:50:51", "thay than", "Nhắc sau số phút", "Đang chạy ngầm ẩn (Safe)"))

    def hien_thong_bao_sieu_to(self, tieu_de, noi_dung):
        """Hiển thị bảng thông báo CHỮ TO, MÀU SẮC RỰC RỠ cho người cận thị, không sợ tắt nhầm"""
        cua_so_tb = tk.Toplevel(self.root)
        cua_so_tb.title(tieu_de)
        cua_so_tb.geometry("600x350")
        cua_so_tb.config(bg="#1e1e1e") # Nền tối sang trọng
        cua_so_tb.attributes("-topmost", True) # Luôn nổi lên trên cùng

        # Phát âm thanh cảnh báo lớn
        try:
            winsound.MessageBeep(winsound.MB_ICONSTOP)
            winsound.Beep(1500, 800)
        except Exception:
            pass

        # Tiêu đề thông báo màu vàng rực
        lbl_title = tk.Label(cua_so_tb, text=f"🔔 {tieu_de.upper()} 🔔", font=("Arial", 20, "bold"), fg="#ffcc00", bg="#1e1e1e")
        lbl_title.pack(pady=20)

        # Nội dung công việc màu trắng tinh, cực to
        lbl_content = tk.Label(cua_so_tb, text=noi_dung, font=("Arial", 22, "bold"), fg="#00ffcc", bg="#1e1e1e", wraplength=550, justify="center")
        lbl_content.pack(pady=10)

        # Nút xác nhận to dễ bấm
        btn_ok = tk.Button(cua_so_tb, text="ĐÃ HIỂU & TẮT", font=("Arial", 14, "bold"), bg="#ff4444", fg="white", command=cua_so_tb.destroy, width=15, height=2)
        btn_ok.pack(pady=20)

    def luu_va_chay_ngam(self):
        noi_dung = self.ent_noi_dung.get().strip()
        phut_str = self.ent_phut.get().strip()

        if not noi_dung:
            messagebox.showerror("Lỗi", "Vui lòng nhập nội dung công việc!")
            return

        try:
            phut = int(phut_str)
        except ValueError:
            messagebox.showerror("Lỗi", "Số phút phải là số nguyên hợp lệ!")
            return

        thoi_gian_tao = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Thêm vào bảng giao diện
        self.tree.insert("", 0, values=(thoi_gian_tao, noi_dung, f"Nhắc sau {phut} phút", "Đang chạy ngầm ẩn 100%"))

        # Khởi chạy luồng đếm ngược ngầm (Background Thread) - TUYỆT ĐỐI KHÔNG HIỆN KHUNG CMD ĐEN NỮA!
        threading.Thread(target=self.chay_dem_nguoc_ngam, args=(noi_dung, phut), daemon=True).start()

        messagebox.showinfo("Thành công", f"Đã lập lịch thành công cho việc: '{noi_dung}'!\nHệ thống đang tự động chạy ngầm, ngài cứ yên tâm làm việc khác.")

    def chay_dem_nguoc_ngam(self, noi_dung, phut):
        """Hàm chạy ngầm đếm ngược thời gian, hoàn toàn ẩn danh, không hiện CMD"""
        giay_cho = phut * 60
        time.sleep(giay_cho)
        
        # Khi hết giờ, gọi bảng thông báo siêu to màu sắc xuất hiện
        self.root.after(0, lambda: self.hien_thong_bao_sieu_to("ĐÃ ĐẾN GIỜ NHẮC NHỞ!", f"Nội dung công việc:\n{noi_dung}"))

    # --- ĐIỀU KHIỂN BỘ BẤM GIỜ TAY ---
    def start_timer(self):
        if not self.is_running:
            try:
                if self.remaining_seconds == 0:
                    self.remaining_seconds = 15 * 60 # Mặc định 15 phút
            except ValueError:
                return

            self.is_running = True
            self.btn_start.config(state="disabled")
            self.btn_pause.config(state="normal")
            self.run_countdown()

    def run_countdown(self):
        if self.is_running and self.remaining_seconds > 0:
            mins, secs = divmod(self.remaining_seconds, 60)
            self.lbl_time.config(text=f"00:{mins:02d}:{secs:02d}")
            self.remaining_seconds -= 1
            self.timer_id = self.root.after(1000, self.run_countdown)
        elif self.is_running and self.remaining_seconds == 0:
            self.lbl_time.config(text="00:00:00")
            self.is_running = False
            self.btn_start.config(state="normal", text="▶ Bắt đầu đếm")
            self.btn_pause.config(state="disabled")
            self.hien_thong_bao_sieu_to("HẾT GIỜ BẤM GIỜ!", "Đã hoàn thành thời gian đếm thủ công!")

    def pause_timer(self):
        if self.is_running:
            self.is_running = False
            if self.timer_id:
                self.root.after_cancel(self.timer_id)
            self.btn_start.config(state="normal", text="▶ Tiếp tục")
            self.btn_pause.config(state="disabled")

    def reset_timer(self):
        self.is_running = False
        if self.timer_id:
            self.root.after_cancel(self.timer_id)
        self.remaining_seconds = 15 * 60
        self.lbl_time.config(text="00:15:00")
        self.btn_start.config(state="normal", text="▶ Bắt đầu đếm")
        self.btn_pause.config(state="disabled")

if __name__ == "__main__":
    root = tk.Tk()
    app = UngDungNhacNhoThannToc(root)
    root.mainloop()