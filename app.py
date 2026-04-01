import streamlit as st
from classifier import classify_query, detect_news_category
from news_api import get_news
from chatbot import get_general_response, is_vague_query, get_clarification_response

st.set_page_config(page_title="NewsGenie", layout="wide")

if "history" not in st.session_state:
    st.session_state.history = []

st.title("🧠 NewsGenie")
st.caption("Your AI-powered assistant for news and knowledge")

category = st.selectbox(
    "Choose a news category",
    ["General", "Technology", "Finance", "Sports"]
)

user_query = st.text_input("Ask a question or request news")

if st.button("Submit"):
    if not user_query.strip():
        st.warning("Please enter a query.")
    else:
        with st.spinner("Processing your request..."):
            query_type = classify_query(user_query)

            st.write("Category selected:", category)
            st.write("You asked:", user_query)
            st.write("Query type detected:", query_type)

            if query_type == "news":
                detected_category = detect_news_category(user_query)

                if category == "General":
                    api_category = detected_category
                elif category == "Finance":
                    api_category = "business"
                else:
                    selected_category = category.lower()

                    if detected_category != "general" and detected_category != selected_category:
                        st.warning(
                            f"Your selected category is '{selected_category}', "
                            f"but your query looks like '{detected_category}' news. Using '{detected_category}' instead."
                        )
                        api_category = detected_category
                    else:
                        api_category = selected_category

                st.write("API category used:", api_category)

                try:
                    articles = get_news(api_category, user_query)
                except Exception:
                    st.error("Failed to fetch news. Please try again.")
                    articles = []

                st.subheader("📰 Latest News")

                if articles:
                    for article in articles:
                        with st.container():
                            st.markdown(f"### 📰 {article['title']}")
                            st.markdown(f"**Source:** {article['source']}")
                            st.markdown(f"[Read full article →]({article['url']})")
                            st.markdown("---")
                else:
                    st.write("No news found.")

                st.session_state.history.append({
                    "query": user_query,
                    "type": "news"
                })

            else:
                st.subheader("💬 General Response")

                if is_vague_query(user_query):
                    response = get_clarification_response(user_query)
                else:
                    response = get_general_response(user_query)

                st.write(response)

                st.session_state.history.append({
                    "query": user_query,
                    "response": response,
                    "type": "general"
                })

st.sidebar.title("🕘 History")

for item in reversed(st.session_state.history):
    if item["type"] == "news":
        st.sidebar.write(f"📰 {item['query']}")
    else:
        st.sidebar.write(f"💬 {item['query']}")