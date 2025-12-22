import streamlit as st

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="AI Website Chatbot",
    page_icon="🤖",
    layout="centered"
)

# ---------------- SESSION STATE ----------------
if "website_url" not in st.session_state:
    st.session_state.website_url = None

if "messages" not in st.session_state:
    st.session_state.messages = []

# ---------------- CSS ----------------
st.markdown("""
<style>
/* Center everything */
.block-container {
    display: flex;
    justify-content: center;
}

/* Chat card */
.chat-card {
    width: 420px;
    background: white;
    border-radius: 14px;
    box-shadow: 0 10px 30px rgba(0,0,0,0.15);
    overflow: hidden;
    margin-top: 40px;
}

/* Header */
.chat-header {
    background: #b97ad9;
    color: white;
    padding: 14px;
    font-weight: bold;
}

.status {
    font-size: 12px;
    opacity: 0.9;
}

/* Body */
.chat-body {
    height: 84px;
    padding: 15px;
    overflow-y: auto;
    background: #fafafa;
}

/* Bubbles */
.bot {
    background: #eaeaea;
    color: #333;
    padding: 10px 14px;
    border-radius: 14px;
    margin-bottom: 10px;
    max-width: 80%;
}

.user {
    background: #b97ad9;
    color: white;
    padding: 10px 14px;
    border-radius: 14px;
    margin-bottom: 10px;
    max-width: 80%;
    margin-left: auto;
}

/* Input */
.chat-input {
    padding: 10px;
    border-top: 1px solid #eee;
    background: white;
}
</style>
""", unsafe_allow_html=True)

# ---------------- UI ----------------
st.markdown('<div class="chat-card">', unsafe_allow_html=True)

# Header
st.markdown("""
<div class="chat-header">
    🤖 LeadBot<br>
    <span class="status">● Online now</span>
</div>
""", unsafe_allow_html=True)

# Body
st.markdown('<div class="chat-body">', unsafe_allow_html=True)

if not st.session_state.messages:
    st.markdown(
        '<div class="bot">Hello! 👋<br>Please enter a website URL to get started.</div>',
        unsafe_allow_html=True
    )

for msg in st.session_state.messages:
    css = "user" if msg["role"] == "user" else "bot"
    st.markdown(f'<div class="{css}">{msg["content"]}</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# Input
st.markdown('<div class="chat-input">', unsafe_allow_html=True)

if not st.session_state.website_url:
    url = st.text_input("Website URL", placeholder="https://example.com", label_visibility="collapsed")
    if st.button("Load Website"):
        if not url.startswith("http"):
            st.warning("Please enter a valid website URL.")
        else:
            st.session_state.website_url = url
            st.session_state.messages.append({
                "role": "bot",
                "content": "Nice! 👍 Website is getting crawled. You can now ask questions."
            })
            #--put playwrite integration Code here
else:
    user_input = st.text_input("Reply...", label_visibility="collapsed")
    if user_input:
        st.session_state.messages.append({"role": "user", "content": user_input})
        st.session_state.messages.append({
            "role": "bot",
            "content": "🤖 AI response will appear here."
        })
         #--put playwrite integration Code here
        st.rerun()

st.markdown('</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)
