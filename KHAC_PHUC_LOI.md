# 🔧 Nhật ký khắc phục lỗi ECG Analyzer

## ❌ Các lỗi đã gặp

### 1. **Lỗi mutex lock failed**
```
libc++abi: terminating due to uncaught exception of type std::__1::system_error: mutex lock failed: Invalid argument
```

**Nguyên nhân:** TensorFlow 2.20.0 không tương thích với Python 3.9.6 trên macOS ARM (Apple Silicon)

**Giải pháp:**
- ✅ Downgrade TensorFlow từ 2.20.0 → 2.15.0
- ✅ Cài đặt `tensorflow-macos` và `tensorflow-metal` (tối ưu cho Apple Silicon)
- ✅ Downgrade grpcio từ 1.76.0 → 1.65.5

### 2. **Lỗi importlib.metadata**
```
module 'importlib.metadata' has no attribute 'packages_distributions'
```

**Nguyên nhân:** Xung đột phiên bản packages

**Trạng thái:** ⚠️ Warning không ảnh hưởng chức năng

### 3. **Lỗi ModuleNotFoundError: No module named 'scipy'**
```
ModuleNotFoundError: No module named 'scipy'
```

**Nguyên nhân:** File `requirements.txt` thiếu dependency `scipy`

**Giải pháp:**
- ✅ Cài đặt: `pip install scipy`

### 4. **Lỗi ModuleNotFoundError: No module named 'src'**
```
ModuleNotFoundError: No module named 'src'
```

**Nguyên nhân:** Package nội bộ `src` chưa được cài đặt

**Giải pháp:**
- ✅ Cài đặt: `pip install -e .` (editable mode)

### 5. **Cảnh báo Python 3.9.6 end of life**
```
You are using a Python version (3.9.6) past its end of life
```

**Trạng thái:** ⚠️ Warning - nên nâng cấp Python lên 3.10+ trong tương lai

## ✅ Cấu hình cuối cùng

### Phiên bản packages đã cài đặt:
```
tensorflow-macos==2.15.0
tensorflow-metal==1.1.0
keras==2.15.0
grpcio==1.65.5
grpcio-status==1.62.0
protobuf==4.25.5
scipy==1.13.1
numpy==1.26.4
streamlit==1.50.0
google-generativeai==0.8.5
```

### Biến môi trường:
```bash
export KMP_DUPLICATE_LIB_OK=TRUE
export GRPC_ENABLE_FORK_SUPPORT=0
export GRPC_POLL_STRATEGY=poll
export OBJC_DISABLE_INITIALIZE_FORK_SAFETY=YES
```

### API Key:
- ✅ Google Gemini API key đã được thêm vào `.streamlit/secrets.toml`
- API Key:

## 🚀 Cách chạy ứng dụng

### Cách 1: Sử dụng script tự động (Khuyến nghị)
```bash
cd "/Users/vatallus/AI ECG/ECG-Analyzer"
./run_app.sh
```

### Cách 2: Chạy thủ công
```bash
cd "/Users/vatallus/AI ECG/ECG-Analyzer"
source venv/bin/activate
export KMP_DUPLICATE_LIB_OK=TRUE
streamlit run app/main.py
```

## 🌐 Truy cập ứng dụng

Sau khi chạy thành công, mở trình duyệt và truy cập:

- **Local URL:** http://localhost:8501
- **Network URL:** http://192.168.50.44:8501

## 📊 Kiểm tra trạng thái

### Kiểm tra TensorFlow:
```bash
cd "/Users/vatallus/AI ECG/ECG-Analyzer"
source venv/bin/activate
export KMP_DUPLICATE_LIB_OK=TRUE
python -c "import tensorflow as tf; print('TensorFlow:', tf.__version__); print('GPU:', len(tf.config.list_physical_devices('GPU')))"
```

**Kết quả mong đợi:**
```
TensorFlow: 2.15.0
GPU: 1
```

### Kiểm tra Streamlit:
```bash
ps aux | grep streamlit
curl -s http://localhost:8501 > /dev/null && echo "✅ Running" || echo "❌ Not running"
```

## 🔄 Dừng ứng dụng

```bash
# Tìm process ID
ps aux | grep streamlit | grep -v grep

# Kill process
pkill -f streamlit

# Hoặc kill theo PID
kill <PID>
```

## 📝 Ghi chú quan trọng

1. **Apple Silicon (M1/M2/M3):** 
   - Phải sử dụng `tensorflow-macos` và `tensorflow-metal`
   - Không dùng `tensorflow` thông thường

2. **Python Version:**
   - Hiện tại: Python 3.9.6 (hoạt động nhưng có warning)
   - Khuyến nghị: Nâng cấp lên Python 3.10+ cho tương lai

3. **API Key Security:**
   - File `.streamlit/secrets.toml` không được commit lên Git
   - Đã thêm vào `.gitignore`

4. **GPU Acceleration:**
   - Ứng dụng đã được cấu hình để sử dụng Metal GPU của Apple
   - Performance tốt hơn nhiều so với CPU

## 🎯 Các tính năng đã test

- ✅ Upload và phân tích file ECG (.mat)
- ✅ Hiển thị biểu đồ ECG
- ✅ Phân loại: Normal, Atrial Fibrillation, Other, Noise
- ✅ Chatbot AI với Google Gemini (có API key)
- ✅ Sample ECG files từ validation set

## 📚 Tài liệu tham khảo

- TensorFlow Metal: https://developer.apple.com/metal/tensorflow-plugin/
- Streamlit Secrets: https://docs.streamlit.io/develop/concepts/connections/secrets-management
- Google Gemini API: https://ai.google.dev/

---

**Ngày khắc phục:** 3 Tháng 11, 2025
**Trạng thái:** ✅ Hoạt động hoàn toàn

