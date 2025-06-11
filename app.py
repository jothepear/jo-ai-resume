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
about_me = read_file("my_data/about-me.txt", "About Me")
full_profile = resume + articles + case_studies + about_me + social_posts

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

    # Expanded off-topic keywords
    off_topic_keywords = [
        "write code", "tell me a joke", "how do I", "give me python",
        "generate code", "solve this", "create a script", "build an app",
        "run a query", "design a function", "write me a program",
        "can you code", "generate javascript", "make a website"
    ]
    if any(keyword in user_input.lower() for keyword in off_topic_keywords):
        reply = "I'm here to answer questions specifically about Jo Gruszka. Please ask about her background, skills, or work."
    else:
        # Combine system prompt and full chat history
        full_messages = [{
            "role": "system",
            "content": (
                "You are a professional AI assistant trained specifically to answer questions about Jo Gruszka. "
                "You must only respond to questions related to Jo's background, resume, skills, work experience, and related topics. "
                "You must not respond to any questions that are unrelated to Jo, including writing code, general advice, or jokes. "
                "If the user asks something unrelated to Jo, politely decline."
                "\n\nJo’s Profile:\n"
                f"{full_profile}"
            )
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
        st.markdown(f"🧠 **AI Agent:**\n\n{reply}")

    # Save assistant reply to chat history
    st.session_state.messages.append({"role": "assistant", "content": reply})
