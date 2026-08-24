@echo off
chcp 65001 > nul
echo --------------------------------------------------
echo Dang khoi chay he thong cap nhat thoi tiet va an uong...
echo --------------------------------------------------

:: Chuyển đến ổ đĩa và thư mục chứa mã nguồn Python
D:
cd D:\NHACVIEC_PYTHON

:: Chạy tệp Python (đổi tên tệp python của bạn cho khớp nếu cần, ví dụ: thoitiet_anuong.py)
python thoitiet_anuong.py

echo --------------------------------------------------
echo Tien trinh da hoan tat! Cam on ban.
echo --------------------------------------------------
pause