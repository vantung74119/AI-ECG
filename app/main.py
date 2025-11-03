import streamlit as st
from tensorflow.keras.models import load_model
import numpy as np
import scipy.io
from src.visualization import plot_ecg
import google.generativeai as genai  # For the Gemini integration

#---------------------------------#
# Page layout
## Page expands to full width
st.set_page_config(
    page_title='🫀 Phân loại ECG',
    page_icon="https://api.iconify.design/openmoji/anatomical-heart.svg?width=500",
    layout='wide',
    initial_sidebar_state="expanded"
)

# Custom CSS for beautification
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #E63946;
        text-align: center;
        margin-bottom: 0.5rem;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #457B9D;
        text-align: center;
        margin-bottom: 1.5rem;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 2rem;
    }
    .stTabs [data-baseweb="tab"] {
        height: 3rem;
        white-space: pre-wrap;
        background-color: #000000;
        border-radius: 4px 4px 0 0;
        gap: 1rem;
        padding-top: 0.5rem;
        padding-bottom: 0.5rem;
    }
    .stTabs [aria-selected="true"] {
        background-color: #A8DADC;
        color: #1D3557;
        font-weight: bold;
    }
    .prediction-box {
        background-color: #F1FAEE;
        border-radius: 10px;
        padding: 20px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    .result-highlight {
        color: #E63946;
        font-weight: bold;
        font-size: 1.2rem;
    }
    .footer-text {
        text-align: center;
        color: #1D3557;
        margin-top: 2rem;
    }
    .stSidebar {
        background-color: #000000;
    }
    .section-header {
        color: #1D3557;
        border-bottom: 2px solid #E63946;
        padding-bottom: 8px;
        margin-bottom: 16px;
    }
    .info-card {
        background-color: #F1FAEE;
        border-radius: 10px;
        padding: 20px;
        margin-bottom: 20px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    
    /* Tablet-like response area and chat styling */
    .tablet-response {
        background-color: #f7f9fc;
        border-radius: 12px;
        padding: 20px;
        border: 1px solid #e0e5ec;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1), 0 1px 3px rgba(0, 0, 0, 0.08);
        margin-bottom: 20px;
        font-family: 'Courier New', monospace;
        max-height: 300px;
        overflow-y: auto;
    }
    
    /* Custom scrollbar for the tablet */
    .tablet-response::-webkit-scrollbar {
        width: 8px;
    }
    
    .tablet-response::-webkit-scrollbar-track {
        background: #f1f1f1;
        border-radius: 10px;
    }
    
    .tablet-response::-webkit-scrollbar-thumb {
        background: #E63946;
        border-radius: 10px;
        color: #000000;
    }
    
    .typewriter-text {
        overflow: hidden;
        border-right: .15em solid #E63946;
        white-space: pre-wrap;
        margin: 0 auto;
        letter-spacing: .1em;
        color: #000000;
        animation: 
            typing 3.5s steps(40, end),
            blink-caret .75s step-end infinite;
    }
    
    @keyframes typing {
        from { max-width: 0 }
        to { max-width: 100% }
    }
    
    @keyframes blink-caret {
        from, to { border-color: transparent }
        50% { border-color: #E63946; }
    }
    
    .chat-message-user {
        background-color: #F1FAEE;
        padding: 10px 15px;
        border-radius: 18px 18px 18px 0;
        margin-bottom: 10px;
        display: inline-block;
        max-width: 80%;
        color: #000000;
    }
    
    .chat-message-bot {
        background-color: #e6f2ff;
        padding: 10px 15px;
        color: #000000;
        border-radius: 18px 18px 0 18px;
        margin-bottom: 10px;
        margin-left: auto;
        display: inline-block;
        max-width: 80%;
    }
    
    .chat-container {
        display: flex;
        flex-direction: column;
    }
    
    .user-container {
        display: flex;
        justify-content: flex-start;
        margin-bottom: 15px;
    }
    
    .bot-container {
        display: flex;
        justify-content: flex-end;
        margin-bottom: 15px;
    }
    
    /* Question button styling */
    .question-button {
        background-color: #f8f9fa;
        border: 1px solid #e0e5ec;
        border-radius: 8px;
        padding: 10px;
        margin-bottom: 10px;
        cursor: pointer;
        transition: all 0.3s ease;
        display: block;
        width: 100%;
        text-align: left;
    }
    
    .question-button:hover {
        background-color: #F1FAEE;
        border-left: 3px solid #E63946;
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# Create tabs for different sections of the app
tabs = st.tabs(["📊 Phân loại ECG", "💬 Hỏi đáp Tim mạch"])

#---------------------------------#
# Data preprocessing and Model building

@st.cache_data
def read_ecg_preprocessing(uploaded_ecg):
    FS = 300
    maxlen = 30*FS

    uploaded_ecg.seek(0)
    mat = scipy.io.loadmat(uploaded_ecg)
    mat = mat["val"][0]

    uploaded_ecg = np.array([mat])

    X = np.zeros((1,maxlen))
    uploaded_ecg = np.nan_to_num(uploaded_ecg) # removing NaNs and Infs
    uploaded_ecg = uploaded_ecg[0,0:maxlen]
    uploaded_ecg = uploaded_ecg - np.mean(uploaded_ecg)
    uploaded_ecg = uploaded_ecg/np.std(uploaded_ecg)
    X[0,:len(uploaded_ecg)] = uploaded_ecg.T # padding sequence
    uploaded_ecg = X
    uploaded_ecg = np.expand_dims(uploaded_ecg, axis=2)
    return uploaded_ecg

model_path = 'models/weights-best.hdf5'
classes = ['Bình thường','Rung nhĩ','Khác','Nhiễu']
classes_en = ['Normal','Atrial Fibrillation','Other','Noise']

@st.cache_resource
def get_model(model_path):
    model = load_model(f'{model_path}')
    return model

@st.cache_resource
def get_prediction(data, _model):
    prob = _model(data)
    ann = np.argmax(prob)
    return classes[ann], prob

# Visualization --------------------------------------
@st.cache_resource
def visualize_ecg(ecg, FS):
    fig = plot_ecg(uploaded_ecg=ecg, FS=FS)
    return fig

#---------------------------------#
# Sidebar - Collects user input features into dataframe
with st.sidebar:
    st.markdown("<h2 style='text-align: center; color: #ffffff;'>❤️ Công cụ Phân tích ECG</h2>", unsafe_allow_html=True)
    st.markdown("<hr>", unsafe_allow_html=True)
    
    st.markdown("### 1. Tải lên ECG của bạn")
    uploaded_file = st.file_uploader("Tải file ECG định dạng .mat", type=["mat"])

    st.markdown("<hr>", unsafe_allow_html=True)

    file_gts = {
        "A00001": "Bình thường",
        "A00002": "Bình thường",
        "A00003": "Bình thường",
        "A00004": "Rung nhĩ",
        "A00005": "Khác",
        "A00006": "Bình thường",
        "A00007": "Bình thường",
        "A00008": "Khác",
        "A00009": "Rung nhĩ",
        "A00010": "Bình thường",
        "A00015": "Rung nhĩ",
        "A00205": "Nhiễu",
        "A00022": "Nhiễu",
        "A00034": "Nhiễu",
    }
    
    valfiles = [
        'None',
        'A00001.mat','A00010.mat','A00002.mat','A00003.mat',
        "A00022.mat", "A00034.mat",'A00009.mat',"A00015.mat",
        'A00008.mat','A00006.mat','A00007.mat','A00004.mat',
        "A00205.mat",'A00005.mat'
    ]

    if uploaded_file is None:
        st.markdown("### 2. Hoặc chọn file mẫu")
        pre_trained_ecg = st.selectbox(
            'Chọn ECG mẫu',
            valfiles,
            format_func=lambda x: f'{x} ({(file_gts.get(x.replace(".mat","")))})' if ".mat" in x else x,
            index=1,
        )
        if pre_trained_ecg != "None":
            f = open("data/validation/"+pre_trained_ecg, 'rb')
            if not uploaded_file:
                uploaded_file = f
    else:
        st.info("Xóa file trên để sử dụng file mẫu.")

    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown("<div class='footer-text'>Phát triển bởi <a href='#'>BS. Hà Ngọc Cường</a></div>", unsafe_allow_html=True)

#---------------------------------#
# Main panel - Tab 1: ECG Classification
with tabs[0]:
    st.markdown("<h1 class='main-header'>🫀 Phân loại ECG</h1>", unsafe_allow_html=True)
    st.markdown("<p class='sub-header'>Phát hiện Rung nhĩ, Nhịp bình thường, Nhịp khác, hoặc Nhiễu từ ECG của bạn</p>", unsafe_allow_html=True)
    
    st.markdown("---")
    
    if uploaded_file is not None:
        # Initialize model
        model = get_model(f'{model_path}')
        
        col1, col2 = st.columns([0.55, 0.45])

        with col1:  # visualize ECG
            st.markdown("### Hiển thị ECG")
            with st.spinner("Đang xử lý dữ liệu ECG..."):
                ecg = read_ecg_preprocessing(uploaded_file)
                fig = visualize_ecg(ecg, FS=300)
                st.pyplot(fig, use_container_width=True)

        with col2:  # classify ECG
            st.markdown("### Kết quả Phân tích")
            with st.spinner(text="Đang chạy mô hình..."):
                pred, conf = get_prediction(ecg, model)
            
            # st.markdown("<div class='prediction-box'>", unsafe_allow_html=True)
            st.markdown(f"<h3>ECG được phân loại là <span class='result-highlight'>{pred}</span></h3>", unsafe_allow_html=True)
            
            pred_confidence = conf[0, np.argmax(conf)]*100
            st.markdown(f"<p>Độ tin cậy: <b>{pred_confidence:.1f}%</b></p>", unsafe_allow_html=True)
            
            st.markdown("#### Phân bố Xác suất")
            
            # Create a bar chart for the confidence levels
            conf_data = {classes[i]: float(conf[0,i]*100) for i in range(len(classes))}
            chart_data = {"Loại Nhịp": list(conf_data.keys()), "Độ tin cậy (%)": list(conf_data.values())}
            
            st.bar_chart(chart_data, x="Loại Nhịp", y="Độ tin cậy (%)", use_container_width=True)
            
            # Create a table with detailed confidence levels
            st.markdown("#### Kết quả Chi tiết")
            mkd_pred_table = [
                "| Loại Nhịp | Độ tin cậy |",
                "| --- | --- |"
            ]
            for i in range(len(classes)):
                mkd_pred_table.append(f"| {classes[i]} | {conf[0,i]*100:3.1f}% |")
            mkd_pred_table = "\n".join(mkd_pred_table)
            st.markdown(mkd_pred_table)
            st.markdown("</div>", unsafe_allow_html=True)
            
            # Include interpretation info
            if pred == "Rung nhĩ":
                st.info("📌 Rung nhĩ được đặc trưng bởi nhịp tim không đều và nhanh. Tình trạng này làm tăng nguy cơ đột quỵ và suy tim.")
            elif pred == "Bình thường":
                st.success("✅ ECG của bạn cho thấy nhịp tim bình thường. Vẫn khuyến nghị kiểm tra sức khỏe tim mạch định kỳ.")
            elif pred == "Khác":
                st.warning("⚠️ ECG cho thấy nhịp bất thường không được phân loại là Rung nhĩ. Nên đánh giá lâm sàng thêm.")
            elif pred == "Nhiễu":
                st.error("❗ ECG chứa quá nhiều nhiễu để có thể phân tích chính xác. Nên thực hiện lại ECG trong môi trường kiểm soát tốt hơn.")
    else:
        st.info("👈 Vui lòng tải lên file ECG hoặc chọn mẫu từ thanh bên để bắt đầu.")
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.image("https://api.iconify.design/openmoji/anatomical-heart.svg?width=300", use_container_width=True)
            
#---------------------------------#
# Tab 2: Ask the Cardio
with tabs[1]:
    st.markdown('<h1 class="main-header">💬 Hỏi đáp Tim mạch</h1>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="info-card">
        <h3 style="color:#1D3557;">Trợ lý AI về Tim mạch</h3>
        <p style="color:#000000;">Nhận tư vấn chuyên gia về giải thích ECG, rối loạn nhịp tim và sức khỏe tim mạch. Trợ lý AI của chúng tôi có thể trả lời câu hỏi về các tình trạng tim mạch và mẫu ECG.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Display a relevant image and the chat interface
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.image("https://api.iconify.design/openmoji/anatomical-heart.svg?width=300", use_container_width=True)
    
    with col2:
        # Add Gemini AI integration
        # Initialize chat history
        if "cardio_chat_history" not in st.session_state:
            st.session_state.cardio_chat_history = [
                ("Trợ lý Tim mạch", "Xin chào! Tôi là trợ lý tim mạch của bạn. Tôi có thể trả lời câu hỏi về ECG, nhịp tim và sức khỏe tim mạch. Tôi có thể giúp gì cho bạn?")
            ]
            
        # Initialize a session state for the selected question
        if "selected_cardio_question" not in st.session_state:
            st.session_state.selected_cardio_question = ""
            
        # Load API Key from Streamlit secrets
        try:
            GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]
            if not GEMINI_API_KEY:
                st.error("Thiếu API key! Vui lòng thêm vào Streamlit secrets.")
                has_api_key = False
            else:
                has_api_key = True
        except:
            st.warning("Để kích hoạt chatbot với Gemini AI, vui lòng thêm Gemini API key vào Streamlit secrets. Hiện đang sử dụng cơ sở kiến thức có sẵn.")
            GEMINI_API_KEY = None
            has_api_key = False
        
        # Function to generate responses about ECG and heart health
        def generate_cardio_response(prompt):
            if has_api_key:
                # Configure Gemini API
                genai.configure(api_key=GEMINI_API_KEY)
                
                gemini_prompt = f"""
                Bạn là trợ lý tim mạch chuyên về giải thích ECG, rối loạn nhịp tim và sức khỏe tim mạch.
                Chỉ trả lời các câu hỏi liên quan đến tim mạch và ECG với thông tin y tế chính xác.
                Nếu câu hỏi không liên quan đến tim mạch, hãy lịch sự thông báo rằng bạn chỉ có thể trả lời 
                các câu hỏi về tim và ECG.
                
                Đặc biệt tập trung vào các tình trạng và mẫu ECG sau:
                - Nhịp xoang bình thường
                - Rung nhĩ (Atrial Fibrillation)
                - Cuồng nhĩ (Atrial Flutter)
                - Nhịp nhanh thất
                - Kéo dài khoảng QT
                - ST chênh lên và chênh xuống
                - Blốc tim (độ 1, độ 2, độ 3)
                - Blốc nhánh bó
                - Co thắt thất sớm
                - Co thắt nhĩ sớm
                - Vị trí chuyển đạo và giải thích ECG
                
                **Câu hỏi của người dùng:** {prompt}
                Hãy cung cấp câu trả lời rõ ràng, ngắn gọn và chính xác bằng tiếng Việt về tim mạch và giải thích ECG.
                """
                model = genai.GenerativeModel("gemini-2.5-pro")
                response = model.generate_content(gemini_prompt)
                
                return response.text
            else:
                # Dictionary of common ECG and cardiology questions and answers
                cardio_knowledge = {
                    "atrial fibrillation": "Atrial fibrillation (AFib) is an irregular and often rapid heart rhythm that can increase risk of stroke, heart failure, and other heart-related complications. On an ECG, it's characterized by irregular R-R intervals and absence of P waves.",
                    "normal ecg": "A normal ECG typically shows regular rhythm with P waves, QRS complexes, and T waves in sequence. The P-R interval is usually 0.12-0.20 seconds, QRS duration 0.06-0.10 seconds, and Q-T interval 0.36-0.44 seconds.",
                    "heart rate": "Normal resting heart rate for adults ranges from 60-100 beats per minute (BPM). Athletes may have lower resting heart rates, sometimes as low as 40 BPM, which is usually not a concern.",
                    "ecg leads": "A standard 12-lead ECG uses electrodes placed on the limbs and chest to record electrical activity from different angles. These include leads I, II, III, aVR, aVL, aVF (limb leads) and V1-V6 (chest leads).",
                    "qt interval": "The QT interval represents ventricular depolarization and repolarization. A prolonged QT interval can indicate a risk for potentially dangerous arrhythmias like torsades de pointes.",
                    "st elevation": "ST elevation on an ECG often indicates myocardial injury or infarction (heart attack). It represents damage to heart muscle and requires immediate medical attention.",
                    "ecg interpretation": "ECG interpretation involves analyzing the regularity of rhythm, heart rate, P waves, PR interval, QRS complex, T waves, QT interval, and looking for any abnormal patterns or changes.",
                    "heart block": "Heart blocks occur when electrical signals between the atria and ventricles are delayed or blocked. They can be first-degree (PR prolongation), second-degree (intermittent blocking), or third-degree (complete block).",
                    "premature beats": "Premature beats can be atrial (PACs) or ventricular (PVCs). They appear as early beats on the ECG and are usually benign but can sometimes indicate underlying heart disease.",
                    "ventricular tachycardia": "Ventricular tachycardia is a rapid heart rhythm starting in the ventricles. On ECG, it appears as wide QRS complexes at a rate typically >100 BPM. It can be life-threatening and requires immediate treatment.",
                    "heart": "The heart is a muscular organ responsible for pumping blood throughout your body. An ECG records the electrical activity of your heart and helps detect various heart conditions like arrhythmias, heart attacks, and structural abnormalities.",
                    "ecg": "An electrocardiogram (ECG or EKG) is a test that records the electrical activity of your heart. It shows how fast your heart beats and whether its rhythm is steady or irregular. ECGs are used to detect heart problems like arrhythmias, heart attacks, and structural abnormalities.",
                    "arrhythmia": "Cardiac arrhythmias are abnormal heart rhythms that cause the heart to beat too fast, too slow, or irregularly. Common types include atrial fibrillation, atrial flutter, ventricular tachycardia, and bradycardia. ECGs are the primary tool for diagnosing arrhythmias.",
                    "bradycardia": "Bradycardia is a slower than normal heart rate, typically below 60 beats per minute. It may be normal in athletic individuals but can cause symptoms like fatigue, dizziness, and fainting in others. On an ECG, it appears as normally formed complexes that occur at a slow rate.",
                    "tachycardia": "Tachycardia is a faster than normal heart rate, typically above 100 beats per minute. It can be sinus tachycardia (normal response to exercise or stress) or pathological. On an ECG, it appears as normally formed complexes occurring at a rapid rate.",
                    "p wave": "The P wave on an ECG represents atrial depolarization (contraction of the atria). Normal P waves are rounded, upright in lead II, and less than 0.12 seconds in duration. Abnormal P waves can indicate atrial enlargement or ectopic atrial rhythms.",
                    "qrs complex": "The QRS complex represents ventricular depolarization (contraction of the ventricles). Normal QRS duration is 0.06-0.10 seconds. Wide QRS complexes can indicate bundle branch blocks, ventricular rhythms, or other conduction abnormalities.",
                    "t wave": "The T wave represents ventricular repolarization (recovery of the ventricles). Normal T waves are slightly asymmetric with a gradual upslope and faster downslope. Abnormal T waves can indicate ischemia, electrolyte disturbances, or other cardiac conditions.",
                    "bundle branch block": "Bundle branch blocks occur when there's a delay or obstruction in the electrical conduction pathway of the heart. On an ECG, they appear as wide QRS complexes (>0.12 seconds) with characteristic patterns depending on whether the right or left bundle is affected.",
                    "heart attack": "A heart attack (myocardial infarction) occurs when blood flow to part of the heart muscle is blocked. On an ECG, it can show ST segment elevation, Q waves, or T wave inversions depending on the timing and location of the infarction."
                }
                
                response = "Tôi không có thông tin cụ thể về điều đó trong cơ sở kiến thức tim mạch của mình. Vui lòng hỏi điều gì đó liên quan đến ECG hoặc tình trạng tim mạch."
                
                # Simple keyword matching - support both Vietnamese and English
                prompt_lower = prompt.lower()
                for keyword, info in cardio_knowledge.items():
                    if keyword.lower() in prompt_lower:
                        response = info
                        break
                
                # General queries about ECG (Vietnamese)
                if any(word in prompt_lower for word in ["ecg là gì", "điện tim đồ", "điện tâm đồ"]):
                    response = cardio_knowledge["ecg"]
                
                # Queries about rhythm disorders (Vietnamese)
                if any(word in prompt_lower for word in ["rối loạn nhịp", "loạn nhịp tim", "arrhythmia"]):
                    response = cardio_knowledge["arrhythmia"]
                
                # Atrial fibrillation (Vietnamese)
                if any(word in prompt_lower for word in ["rung nhĩ", "atrial fibrillation"]):
                    response = cardio_knowledge["atrial fibrillation"]
                
                return response
            
        # User input - note that we're using the session state value as the default
        user_query = st.text_input("Đặt câu hỏi về giải thích ECG hoặc sức khỏe tim mạch:", 
                                  value=st.session_state.selected_cardio_question,
                                  key="cardio_assistant_query")
        
        # After the user submits a question, clear the selected_question
        if st.button("Hỏi Trợ lý Tim mạch"):
            if user_query:
                with st.spinner("Trợ lý đang suy nghĩ..."):
                    try:
                        # Get the response
                        response = generate_cardio_response(user_query)
                        # Add to chat history
                        st.session_state.cardio_chat_history.append(("Bạn", user_query))
                        st.session_state.cardio_chat_history.append(("Trợ lý Tim mạch", response))
                        # Clear the selected question after submission
                        st.session_state.selected_cardio_question = ""
                    except Exception as e:
                        st.error(f"Lỗi khi tạo câu trả lời: {str(e)}")
                        
    # Display chat history in tablet-like response area
    if "cardio_chat_history" in st.session_state and len(st.session_state.cardio_chat_history) > 0:
        st.subheader("Cuộc trò chuyện với Trợ lý Tim mạch")
        
        # Create a tablet-like container for the conversation
        with st.container():
            st.markdown('<div class="tablet-response">', unsafe_allow_html=True)
            
            for i, (role, message) in enumerate(st.session_state.cardio_chat_history):
                if role == "Bạn":
                    st.markdown(f'<div class="user-container"><div class="chat-message-user"><strong>👨‍⚕️ {role}:</strong> {message}</div></div>', unsafe_allow_html=True)
                else:
                    # For the latest bot response, add the typewriter effect
                    if i == len(st.session_state.cardio_chat_history) - 1 and role == "Trợ lý Tim mạch":
                        st.markdown(f'<div class="bot-container"><div class="chat-message-bot"><strong>🫀 {role}:</strong> <span class="typewriter-text">{message}</span></div></div>', unsafe_allow_html=True)
                    else:
                        st.markdown(f'<div class="bot-container"><div class="chat-message-bot"><strong>🫀 {role}:</strong> {message}</div></div>', unsafe_allow_html=True)
            
            st.markdown('</div>', unsafe_allow_html=True)
    
    # Add some common questions as examples
    st.markdown('<h3 class="section-header">Câu hỏi Thường gặp</h3>', unsafe_allow_html=True)
    
    example_questions = [
        "ECG bình thường trông như thế nào?",
        "Làm thế nào để nhận biết rung nhĩ trên ECG?",
        "Nguyên nhân gây ST chênh lên trên ECG là gì?",
        "Khoảng QT là gì và tại sao nó quan trọng?",
        "Blốc tim xuất hiện như thế nào trên ECG?"
    ]
    
    # Create functions for handling button clicks
    def set_cardio_question(question):
        st.session_state.selected_cardio_question = question
    
    col1, col2 = st.columns(2)
    for i, question in enumerate(example_questions):
        if i % 2 == 0:
            with col1:
                st.button(f"❓ {question}", key=f"cardio_q{i}", on_click=set_cardio_question, args=(question,))
        else:
            with col2:
                st.button(f"❓ {question}", key=f"cardio_q{i}", on_click=set_cardio_question, args=(question,))
    
    # Disclaimer
    st.markdown("---")
    st.markdown("""
    <div style='background-color: #f8d7da; padding: 10px; border-radius: 5px; margin-top: 20px;'>
        <p style='color: #721c24; margin: 0;'><strong>Lưu ý quan trọng:</strong> Trợ lý AI này chỉ cung cấp thông tin tham khảo và không thay thế cho tư vấn y tế chuyên nghiệp. Luôn tham khảo ý kiến bác sĩ để chẩn đoán và điều trị các tình trạng bệnh lý.</p>
    </div>
    """, unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("<div class='footer-text'>Phát triển bởi BS. Hà Ngọc Cường - Ứng dụng Machine Learning trong Y tế</div>", unsafe_allow_html=True)
