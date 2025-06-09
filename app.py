import streamlit as st
import os
from dotenv import load_dotenv
from openai import OpenAI

# Load OpenAI API key
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Load and combine all profile files
def read_file(path, label):
    if os.path.exists(path):
        with open(path, "r") as f:
            return f"\n\n## {label.upper()} ##\n" + f.read()
    else:
        return f"\n\n## {label.upper()} ##\n(No content found.)"

resume = read_file("my_data/my resume.txt", "Resume")
articles = read_file("my_data/articles.txt", "Articles")
case_studies = read_file("my_data/case studies.txt", "Case Studies")
social_posts = read_file("my_data/social posts.txt", "Social Posts")
about_me = read_file("my_data/about-me.txt","About Me")
full_profile = resume + articles + case_studies + about_me

# Page config
st.set_page_config(
    page_title="Jo Gruszka – Resume Agent",
    page_icon="💬",
    layout="centered",
    initial_sidebar_state="collapsed"
)

st.title("👋 Ask Me About Jo")
st.markdown("Chat with an AI that knows my resume!")

# Clear chat button
if st.button("🧹 Clear Chat"):
    st.session_state.messages = []

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Show chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Chat input
if user_input := st.chat_input("💬 Ask something about Jo..."):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": user_input})

    # Combine system prompt and full chat history
    full_messages = [{
        "role": "system",
        "content": f"You are an assistant answering questions about Jo. The following is Jo’s profile including resume, case studies, articles, and social posts. Use these materials to answer clearly and specifically:\n\n{full_profile}"
    }] + st.session_state.messages

    # Call OpenAI and get response
    response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=full_messages,
    max_tokens=300  # ≈ about 1,200 characters
)
    reply = response.choices[0].message.content

    # Display assistant reply
    with st.chat_message("assistant"):
        st.markdown(reply)

    # Save assistant reply to chat history
    st.session_state.messages.append({"role": "assistant", "content": reply})
