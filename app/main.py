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

st.title("🎥 YouTube Views Prediction App")
st.write("Enter video details to estimate how many views your video might get.")

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
col1, col2 = st.columns(2)

with col1:
    likes = st.number_input("Likes", min_value=0, value=1000)
    comments = st.number_input("Comment Count", min_value=0, value=50)
    category_name = st.selectbox("Video Category", list(category_mapping.keys()))

with col2:
    publish_hour = st.number_input(
        "Publish Hour (0–23)", min_value=0, max_value=23, value=14
    )
    day_of_week = st.selectbox(
        "Day of Week",
        options=[0, 1, 2, 3, 4, 5, 6],
        format_func=lambda x: [
            "Monday",
            "Tuesday",
            "Wednesday",
            "Thursday",
            "Friday",
            "Saturday",
            "Sunday",
        ][x],
        index=0,
    )
    channel_title = st.text_input("Channel Title", value="Example Channel")

# Convert selected name → category ID
category_id = category_mapping[category_name]

# Engagement Rate (calculated automatically)
if comments > 0:
    engagement_rate = likes / (comments + 1)
else:
    engagement_rate = likes

st.info(f"📊 Calculated Engagement Rate: **{engagement_rate:.2f}**")

# -------------------------
# Predict button
# -------------------------
if st.button(" Predict Views", type="primary"):
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

    st.success(f"###  Estimated Views: **{int(prediction):,}**")

    # Additional insights
    st.divider()
    st.subheader(" Input Summary")

    col_a, col_b, col_c = st.columns(3)

    with col_a:
        st.metric("Likes", f"{likes:,}")
        st.metric("Comments", f"{comments:,}")

    with col_b:
        st.metric("Category", category_name)
        st.metric("Publish Hour", f"{publish_hour}:00")

    with col_c:
        st.metric("Day", ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"][day_of_week])
        st.metric("Engagement", f"{engagement_rate:.2f}")
