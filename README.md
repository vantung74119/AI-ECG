# 🫀 ECG Analyzer - Phân loại Điện tâm đồ bằng AI

Ứng dụng phân tích và phân loại tín hiệu điện tâm đồ (ECG) sử dụng Deep Learning và trợ lý AI tim mạch.

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.9+-blue.svg)
![TensorFlow](https://img.shields.io/badge/TensorFlow-2.15-orange.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.50-red.svg)

## 🎯 Tính năng

### 1. Phân loại ECG tự động
- ✅ **Bình thường** - Nhịp tim bình thường
- ⚠️ **Rung nhĩ** - Atrial Fibrillation
- 🔶 **Khác** - Nhịp bất thường khác
- ❌ **Nhiễu** - Tín hiệu nhiễu

### 2. Trợ lý AI Tim mạch
- Hỏi đáp về ECG và tim mạch
- Được hỗ trợ bởi Google Gemini AI
- Trả lời bằng tiếng Việt

### 3. Trực quan hóa
- Hiển thị biểu đồ ECG
- Phân tích độ tin cậy
- Kết quả chi tiết

## 🚀 Demo

**Truy cập:** [Link demo nếu có]

## 📋 Yêu cầu hệ thống

- Python 3.9+
- macOS / Linux / Windows
- 4GB RAM trở lên
- (Khuyến nghị) Apple Silicon cho tăng tốc GPU

## ⚙️ Cài đặt

### 1. Clone repository

```bash
git clone https://github.com/your-username/ECG-Analyzer.git
cd ECG-Analyzer
```

### 2. Tạo môi trường ảo

```bash
python3 -m venv venv
source venv/bin/activate  # macOS/Linux
# hoặc
venv\Scripts\activate  # Windows
```

### 3. Cài đặt dependencies

```bash
pip install -r requirements.txt
pip install -e .
pip install scipy
pip install git+https://github.com/simonsanvil/subplotted.git
```

**Lưu ý cho macOS Apple Silicon:**
```bash
pip install tensorflow-macos==2.15.0
pip install tensorflow-metal==1.1.0
```

### 4. Cấu hình API Key (Tùy chọn)

Để sử dụng chatbot AI:

1. Lấy API key miễn phí tại: https://makersuite.google.com/app/apikey
2. Copy file cấu hình mẫu:
```bash
cp .streamlit/secrets.toml.example .streamlit/secrets.toml
```
3. Sửa file `.streamlit/secrets.toml` và thêm API key:
```toml
GEMINI_API_KEY = "your-api-key-here"
```

## 🎮 Sử dụng

### Chạy ứng dụng

```bash
# Cách 1: Script tự động
./run_app.sh

# Cách 2: Thủ công
export KMP_DUPLICATE_LIB_OK=TRUE
streamlit run app/main.py
```

Ứng dụng sẽ mở tại: http://localhost:8501

### Upload ECG

1. Vào tab **"📊 Phân loại ECG"**
2. Tải lên file ECG định dạng `.mat`
3. Hoặc chọn file mẫu có sẵn
4. Xem kết quả phân tích

### Hỏi đáp AI

1. Vào tab **"💬 Hỏi đáp Tim mạch"**
2. Đặt câu hỏi về ECG hoặc tim mạch
3. Nhận câu trả lời từ AI

## 📁 Cấu trúc Project

```
ECG-Analyzer/
├── app/
│   └── main.py              # Ứng dụng Streamlit chính
├── data/
│   └── validation/          # Dữ liệu ECG mẫu
├── models/
│   └── weights-best.hdf5    # Model đã train
├── src/
│   ├── data/               # Xử lý dữ liệu
│   ├── features/           # Feature engineering
│   ├── models/             # Train/predict models
│   └── visualization/      # Visualization ECG
├── notebooks/              # Jupyter notebooks
├── .streamlit/
│   └── secrets.toml       # API keys (không commit)
├── requirements.txt       # Python dependencies
└── README.md             # File này
```

## 🛠️ Công nghệ

- **Deep Learning:** TensorFlow 2.15, Keras
- **Web Framework:** Streamlit
- **AI Chatbot:** Google Gemini API
- **Data Processing:** NumPy, SciPy, Pandas
- **Visualization:** Matplotlib
- **Language:** Python 3.9+

## 📊 Model

- **Architecture:** Deep CNN
- **Input:** ECG signal (9000 points, 30s @ 300Hz)
- **Output:** 4 classes (Normal, AF, Other, Noise)
- **Performance:** [Thêm metrics nếu có]

## 🔧 Khắc phục sự cố

Xem file chi tiết: `KHAC_PHUC_LOI.md`

### Lỗi thường gặp:

**1. Module not found**
```bash
pip install scipy
pip install -e .
```

**2. TensorFlow error trên macOS**
```bash
pip install tensorflow-macos==2.15.0 tensorflow-metal==1.1.0
```

**3. API key không hoạt động**
- Kiểm tra file `.streamlit/secrets.toml`
- Tạo API key mới tại: https://makersuite.google.com/app/apikey

## 📝 Tài liệu

- [Hướng dẫn chi tiết](HUONG_DAN.md)
- [Nhật ký khắc phục lỗi](KHAC_PHUC_LOI.md)
- [Thay đổi giao diện](THAY_DOI_GIAO_DIEN.md)
- [Bắt đầu nhanh](BAT_DAU_NHANH.md)

## 👥 Đóng góp

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

MIT License - xem file [LICENSE](LICENSE) để biết chi tiết

## 👨‍⚕️ Tác giả

**BS. Hà Ngọc Cường**
- Chuyên môn: Machine Learning trong Y tế
- Project: Ứng dụng AI phân tích ECG

**Original Author:** [Mainak](https://github.com/MainakVerse) - Base implementation

## ⚠️ Disclaimer

**LƯU Ý QUAN TRỌNG:** 

Ứng dụng này chỉ mang tính chất tham khảo và nghiên cứu. Không sử dụng để thay thế cho ý kiến của bác sĩ chuyên khoa. Luôn tham khảo ý kiến bác sĩ cho bất kỳ vấn đề sức khỏe nào.

## 🙏 Lời cảm ơn

- Original ECG-Analyzer by [MainakVerse](https://github.com/MainakVerse/ECG-Analyzer)
- PhysioNet/CinC Challenge 2017 dataset
- Google Gemini AI
- Streamlit team

## 📞 Liên hệ

Nếu có câu hỏi hoặc góp ý, vui lòng tạo issue trên GitHub.

---

**Made with ❤️ for Healthcare AI**
