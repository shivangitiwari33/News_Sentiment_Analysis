import streamlit as st
from api import fetch_news

st.set_page_config(page_title="🧠 Smart News Analyzer", layout="wide")

st.markdown(
    """
    <style>
    .main-title {
        font-size: 2.5rem;
        font-weight: 700;
        color: #1f77b4;
    }
    .subtitle {
        font-size: 1.2rem;
        color: #555;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown('<div class="main-title">🧠 Smart News Insight Generator</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Instantly analyze company news with sentiment and audio in Hindi 🇮🇳</div>', unsafe_allow_html=True)
st.markdown("---")

companies = ["Select a Company", "Microsoft", "Netflix", "Google", "Meta", "Reliance", "Paytm", "Flipkart"]
company = st.selectbox("🏢 Choose a Company to Analyze", companies)

st.markdown("")

col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    analyze = st.button("🧪 Run News Analysis", use_container_width=True)

if analyze:
    if company == "Select a Company":
        st.warning("⚠️ Please select a valid company to begin analysis.")
    else:
        with st.spinner("🛰️ Fetching news articles and processing sentiment..."):
            try:
                data = fetch_news(company)

                if not data["Articles"]:
                    st.error("🚫 No articles found for this company.")
                else:
                    st.success("✅ Analysis completed successfully!")

                    st.markdown("### 📊 Final Sentiment Summary")
                    st.markdown(f"**📝 {data['Final Sentiment Analysis']}**")
                    st.markdown("---")

                    st.markdown("### 🗞️ News Headlines & Insights")
                    for i, article in enumerate(data["Articles"], 1):
                        st.markdown(f"#### {i}. {article['Title']}")
                        st.write(f"**📝 Summary:** {article['Summary']}")
                        
                        sentiment = article["Sentiment"]
                        if sentiment == "Positive":
                            st.success(f"📈 Sentiment: {sentiment}")
                        elif sentiment == "Negative":
                            st.error(f"📉 Sentiment: {sentiment}")
                        else:
                            st.info(f"🔎 Sentiment: {sentiment}")

                        st.caption(f"💬 Topics: {', '.join(article['Topics'])}")
                        st.markdown("---")

                    st.markdown("### 🔍 Comparative Sentiment Overview")
                    st.json(data["Comparative Sentiment Score"])

                    st.markdown("### 🔊 Hindi Audio Summary")
                    st.audio(data["Audio"], format="audio/mp3")

            except Exception as e:
                st.error(f"❌ Something went wrong:\n\n`{e}`")

st.markdown("---")
