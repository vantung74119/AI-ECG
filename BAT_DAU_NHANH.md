# 🚀 Hướng dẫn bắt đầu nhanh - ECG Analyzer

## ✅ Trạng thái: Đã cài đặt và cấu hình xong!

Ứng dụng của bạn đã sẵn sàng để sử dụng.

---

## 📱 Chạy ứng dụng (Chỉ 1 lệnh!)

```bash
cd "/Users/vatallus/AI ECG/ECG-Analyzer" && ./run_app.sh
```

**Sau khi chạy, mở trình duyệt:** http://localhost:8501

---

## 🎯 Tính năng chính

### 1️⃣ **Phân tích ECG**
- Upload file ECG định dạng `.mat`
- Xem biểu đồ tín hiệu ECG
- Nhận kết quả phân loại:
  - ✅ Normal (Nhịp bình thường)
  - ⚠️ Atrial Fibrillation (Rung nhĩ)
  - 🔶 Other (Nhịp bất thường khác)
  - ❌ Noise (Nhiễu)

### 2️⃣ **Chatbot AI về tim mạch**
- Hỏi đáp về ECG và các bệnh tim
- Được hỗ trợ bởi Google Gemini AI
- ✅ API Key đã được cấu hình

---

## 📂 Dữ liệu mẫu có sẵn

Project đã có sẵn các file ECG mẫu trong tab "ECG Classification":

| File | Loại | Mô tả |
|------|------|-------|
| A00001.mat | Normal | Nhịp tim bình thường |
| A00004.mat | AF | Rung nhĩ |
| A00005.mat | Other | Nhịp bất thường |
| A00022.mat | Noise | Tín hiệu nhiễu |

---

## 🔧 Đã khắc phục các lỗi

- ✅ Lỗi mutex lock (TensorFlow trên macOS)
- ✅ Thiếu scipy
- ✅ Thiếu package src
- ✅ Tối ưu cho Apple Silicon (M1/M2/M3)
- ✅ Cấu hình Google Gemini API

Chi tiết xem file: `KHAC_PHUC_LOI.md`

---

## 🛑 Dừng ứng dụng

```bash
# Cách 1: Nhấn Ctrl+C trong terminal đang chạy

# Cách 2: Kill process
pkill -f streamlit
```

---

## 📋 Các lệnh hữu ích

### Kiểm tra ứng dụng có đang chạy không:
```bash
curl -s http://localhost:8501 > /dev/null && echo "✅ Đang chạy" || echo "❌ Không chạy"
```

### Xem log lỗi nếu có:
```bash
cd "/Users/vatallus/AI ECG/ECG-Analyzer"
source venv/bin/activate
streamlit run app/main.py
```

### Kiểm tra TensorFlow:
```bash
cd "/Users/vatallus/AI ECG/ECG-Analyzer"
source venv/bin/activate
python -c "import tensorflow as tf; print('TensorFlow:', tf.__version__)"
```

---

## 🆘 Cần trợ giúp?

1. **Ứng dụng không chạy?** 
   - Kiểm tra file `KHAC_PHUC_LOI.md`
   - Đảm bảo bạn đã kích hoạt virtual environment

2. **Chatbot không hoạt động?**
   - Kiểm tra file `.streamlit/secrets.toml` có tồn tại không
   - API key có thể hết hạn, cần tạo mới

3. **Lỗi khác?**
   - Xem log chi tiết khi chạy app
   - Đọc file `HUONG_DAN.md` để biết thêm chi tiết

---

## 📚 Tài liệu đầy đủ

- `HUONG_DAN.md` - Hướng dẫn chi tiết
- `KHAC_PHUC_LOI.md` - Nhật ký khắc phục lỗi
- `README.md` - Mô tả project gốc

---

## 🎉 Chúc bạn sử dụng vui vẻ!

**Made with ❤️ for Healthcare AI**

---

**Cập nhật:** 3 Tháng 11, 2025  
**Trạng thái:** ✅ Hoạt động hoàn toàn

