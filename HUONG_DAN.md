# 🫀 Hướng dẫn sử dụng ECG Analyzer

## 📋 Mô tả

ECG Analyzer là một ứng dụng AI phân tích điện tâm đồ (ECG) sử dụng Deep Learning để:
- Phân loại tín hiệu ECG thành 4 loại: Normal, Atrial Fibrillation, Other, Noise
- Chatbot AI tư vấn về tim mạch sử dụng Google Gemini AI

## 🚀 Cách chạy ứng dụng

### Bước 1: Kích hoạt môi trường ảo
```bash
cd "/Users/vatallus/AI ECG/ECG-Analyzer"
source venv/bin/activate
```

### Bước 2: Chạy ứng dụng Streamlit
```bash
streamlit run app/main.py
```

Ứng dụng sẽ tự động mở trong trình duyệt tại địa chỉ: http://localhost:8501

## 📊 Tính năng

### 1. **ECG Classification** (Phân loại ECG)
- Upload file ECG định dạng `.mat`
- Hoặc chọn file mẫu từ validation set
- Xem biểu đồ tín hiệu ECG
- Nhận kết quả phân loại với độ tin cậy

**Các loại nhịp tim được phát hiện:**
- ✅ **Normal**: Nhịp tim bình thường
- ⚠️ **Atrial Fibrillation**: Rung nhĩ
- 🔶 **Other**: Nhịp bất thường khác
- ❌ **Noise**: Tín hiệu nhiễu

### 2. **Ask the Cardio** (Hỏi đáp AI về tim mạch)
- Chatbot AI tư vấn về ECG và tim mạch
- Trả lời các câu hỏi về:
  - Giải thích ECG
  - Các rối loạn nhịp tim
  - Sức khỏe tim mạch
  - Các chỉ số trên ECG

## 🔑 Cấu hình API Key (Tùy chọn)

Để sử dụng tính năng chatbot AI với Google Gemini:

### Cách 1: Sử dụng file secrets của Streamlit
1. Tạo thư mục `.streamlit` trong project (nếu chưa có)
```bash
mkdir -p .streamlit
```

2. Tạo file `secrets.toml`:
```bash
nano .streamlit/secrets.toml
```

3. Thêm API key:
```toml
GEMINI_API_KEY = "your-api-key-here"
```

### Cách 2: Lấy Google Gemini API Key miễn phí
1. Truy cập: https://makersuite.google.com/app/apikey
2. Đăng nhập với tài khoản Google
3. Click "Create API Key"
4. Copy API key và thêm vào file `secrets.toml`

**Lưu ý:** Nếu không có API key, ứng dụng vẫn hoạt động nhưng chatbot sẽ sử dụng knowledge base có sẵn với khả năng hạn chế.

## 📁 Dữ liệu mẫu

Ứng dụng đã bao gồm các file ECG mẫu trong thư mục `data/validation/`:
- A00001.mat - Normal
- A00002.mat - Normal
- A00003.mat - Normal
- A00004.mat - Atrial Fibrillation
- A00005.mat - Other
- A00009.mat - Atrial Fibrillation
- A00022.mat - Noise
- A00034.mat - Noise
- v.v.

## 🛠️ Công nghệ sử dụng

- **TensorFlow/Keras**: Deep Learning model
- **Streamlit**: Web interface
- **Google Generative AI**: Chatbot AI
- **Matplotlib**: Visualization
- **NumPy, SciPy**: Xử lý dữ liệu

## ⚠️ Lưu ý quan trọng

**DISCLAIMER:** Ứng dụng này chỉ mang tính chất tham khảo và học tập. 
- Không thay thế cho ý kiến của bác sĩ chuyên khoa
- Không sử dụng để tự chẩn đoán hoặc điều trị
- Luôn tham khảo ý kiến bác sĩ cho các vấn đề về sức khỏe

## 🔧 Khắc phục sự cố

### Lỗi: Module not found
```bash
# Đảm bảo đã kích hoạt môi trường ảo
source venv/bin/activate

# Cài đặt lại dependencies
pip install -r requirements.txt
```

### Lỗi: Port đã được sử dụng
```bash
# Chạy trên port khác
streamlit run app/main.py --server.port 8502
```

### Lỗi: Cannot load model
```bash
# Kiểm tra file model có tồn tại
ls -la models/weights-best.hdf5
```

## 👨‍💻 Tác giả

- **Original Author**: [Mainak](https://github.com/MainakVerse)
- **Repository**: https://github.com/MainakVerse/ECG-Analyzer

## 📄 License

MIT License

---

**Made with ❤️ for Healthcare AI**

