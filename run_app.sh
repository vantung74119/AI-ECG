#!/bin/bash

# ========================================
# Script để chạy ECG Analyzer 
# Đã tối ưu cho macOS Apple Silicon (M1/M2/M3)
# ========================================

echo "🫀 ECG Analyzer - Starting Application..."
echo "========================================"

# Thiết lập các biến môi trường để khắc phục lỗi mutex lock
export KMP_DUPLICATE_LIB_OK=TRUE
export GRPC_ENABLE_FORK_SUPPORT=0
export GRPC_POLL_STRATEGY=poll
export OBJC_DISABLE_INITIALIZE_FORK_SAFETY=YES

# Chuyển đến thư mục project
cd "/Users/vatallus/AI ECG/ECG-Analyzer"

# Kích hoạt môi trường ảo
echo "✓ Activating virtual environment..."
source venv/bin/activate

# Kiểm tra TensorFlow
echo "✓ Checking TensorFlow..."
python -c "import tensorflow as tf; print('  TensorFlow version:', tf.__version__)" 2>/dev/null

# Kiểm tra API Key
if [ -f ".streamlit/secrets.toml" ]; then
    echo "✓ Google Gemini API key found"
else
    echo "⚠ Warning: No API key found. Chatbot will use limited knowledge base."
fi

echo ""
echo "🚀 Starting Streamlit server..."
echo "========================================"
echo ""

# Chạy ứng dụng Streamlit
streamlit run app/main.py

# Nếu lỗi, thử với port khác
# streamlit run app/main.py --server.port 8502

