import streamlit as st
import pandas as pd
import joblib

# Page config for better zoom/view
st.set_page_config(
    page_title="YouTube Views Predictor",
    page_icon="🎥",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# Load trained model
model = joblib.load("../model_youtube_views.pkl")

# Custom CSS for modern styling
st.markdown("""
<style>
    .main-header {
        text-align: center;
        font-size: 2.5rem;
        margin-bottom: 2rem;
        background: linear-gradient(90deg, #ff4500, #ff8c00);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    .sub-header {
        text-align: center;
        color: #666;
        margin-bottom: 2rem;
    }
    .metric-container {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 8px;
        text-align: center;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    .prediction-result {
        font-size: 2rem;
        font-weight: bold;
        text-align: center;
        padding: 1.5rem;
        background: linear-gradient(90deg, #4f8bf9, #8e44ad);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    .engagement-box {
        background-color: #e3f2fd;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #2196f3;
    }
    .input-section {
        background-color: #ffffff;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown('<h1 class="main-header">🎥 YouTube Views Predictor</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Enter your video details to estimate potential views</p>', unsafe_allow_html=True)

# -------------------------
# Category Mapping (YouTube Official)
# -------------------------
category_mapping = {
    "Film & Animation": 1,
    "Autos & Vehicles": 2,
    "Music": 10,
    "Pets & Animals": 15,
    "Sports": 17,
    "Short Movies": 18,
    "Travel & Events": 19,
    "Gaming": 20,
    "People & Blogs": 22,
    "Comedy": 23,
    "Entertainment": 24,
    "News & Politics": 25,
    "Howto & Style": 26,
    "Education": 27,
    "Science & Technology": 28,
    "Nonprofits & Activism": 29,
}

# -------------------------
# Input fields layout
# -------------------------
col1, col2 = st.columns([1, 1])

with col1:
    st.markdown('<div class="input-section">', unsafe_allow_html=True)
    st.subheader("📊 Video Metrics")
    likes = st.number_input("Likes", min_value=0, value=1000, step=100)
    comments = st.number_input("Comments", min_value=0, value=50, step=10)
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="input-section">', unsafe_allow_html=True)
    st.subheader("📅 Publishing Details")
    publish_hour = st.slider("Publish Hour", min_value=0, max_value=23, value=14)
    day_of_week = st.selectbox(
        "Day of Week",
        options=[0, 1, 2, 3, 4, 5, 6],
        format_func=lambda x: [
            "Monday", "Tuesday", "Wednesday", 
            "Thursday", "Friday", "Saturday", "Sunday"
        ][x],
        index=0
    )
    st.markdown('</div>', unsafe_allow_html=True)

# Second row
col3, col4 = st.columns([1, 1])

with col3:
    st.markdown('<div class="input-section">', unsafe_allow_html=True)
    st.subheader("🏷️ Content Details")
    category_name = st.selectbox("Video Category", list(category_mapping.keys()))
    channel_title = st.text_input("Channel Name", value="Example Channel")
    st.markdown('</div>', unsafe_allow_html=True)

with col4:
    st.markdown('<div class="engagement-box">', unsafe_allow_html=True)
    st.subheader("📈 Engagement Metrics")
    # Engagement Rate (calculated automatically)
    if comments > 0:
        engagement_rate = likes / (comments + 1)
    else:
        engagement_rate = likes
    
    st.metric(label="Engagement Rate", value=f"{engagement_rate:.2f}")
    st.info("Engagement Rate = Likes / (Comments + 1)")
    st.markdown('</div>', unsafe_allow_html=True)

# -------------------------
# Predict button
# -------------------------
st.markdown("<br>", unsafe_allow_html=True)
col_btn1, col_btn2, col_btn3 = st.columns([1, 2, 1])
with col_btn2:
    predict_button = st.button("🔮 Predict Views", type="primary", use_container_width=True)

if predict_button:
    # Convert selected name → category ID
    category_id = category_mapping[category_name]
    
    # Build DataFrame for model input (with all 7 features)
    input_data = pd.DataFrame(
        [
            {
                "likes": likes,
                "comment_count": comments,
                "category_id": category_id,
                "channel_title": channel_title,
                "publish_hour": publish_hour,
                "day_of_week": day_of_week,
                "engagement_rate": engagement_rate,
            }
        ]
    )

    # Predict
    prediction = model.predict(input_data)[0]

    # Display prediction with animation effect
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="prediction-result">Estimated Views: {:,}</div>'.format(int(prediction)), unsafe_allow_html=True)

    # Additional insights
    st.markdown("<hr>", unsafe_allow_html=True)
    st.subheader("📋 Prediction Summary")
    
    col_a, col_b, col_c = st.columns(3)
    
    with col_a:
        st.markdown('<div class="metric-container">', unsafe_allow_html=True)
        st.metric("Likes", f"{likes:,}")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col_b:
        st.markdown('<div class="metric-container">', unsafe_allow_html=True)
        st.metric("Comments", f"{comments:,}")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col_c:
        st.markdown('<div class="metric-container">', unsafe_allow_html=True)
        st.metric("Engagement Rate", f"{engagement_rate:.2f}")
        st.markdown('</div>', unsafe_allow_html=True)
    
    col_d, col_e, col_f = st.columns(3)
    
    with col_d:
        st.markdown('<div class="metric-container">', unsafe_allow_html=True)
        st.metric("Category", category_name)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col_e:
        st.markdown('<div class="metric-container">', unsafe_allow_html=True)
        st.metric("Publish Time", f"{publish_hour}:00")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col_f:
        st.markdown('<div class="metric-container">', unsafe_allow_html=True)
        st.metric("Publish Day", ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"][day_of_week])
        st.markdown('</div>', unsafe_allow_html=True)