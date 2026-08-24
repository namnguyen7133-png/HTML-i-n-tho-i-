Set WshShell = CreateObject("WScript.Shell")
' Đọc nội dung file danh mục
Set objFSO = CreateObject("Scripting.FileSystemObject")
Set objFile = objFSO.OpenTextFile("D:\KHO_PHU_DE_YOUTUBE\danhmuccongviec.txt", 1)
strText = objFile.ReadAll
objFile.Close

' Hiện thông báo (Pop-up) ở góc màn hình
' Tham số: Nội dung, Thời gian chờ (giây), Tiêu đề, Loại biểu tượng
WshShell.Popup strText, 10, "DANH MUC CONG VIEC HOM NAY", 64