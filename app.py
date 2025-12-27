import streamlit as st
from utils import load_english_transcript
from rag import build_rag_chain

# Page config
st.set_page_config(
    page_title="YouTube Video Chat",
    layout="wide"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main {
        padding: 0rem 1rem;
    }
    .stTextInput > div > div > input {
        background-color: #ffffff;
        color: #1f1f1f !important;
        border: 1px solid #d1d5db;
    }
    .stTextInput > div > div > input::placeholder {
        color: #9ca3af;
    }
    .chat-message {
        padding: 1rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
        display: flex;
        flex-direction: column;
        color: #1f1f1f;
    }
    .user-message {
        background-color: #e3f2fd;
        border-left: 4px solid #2196f3;
        color: #1f1f1f;
    }
    .assistant-message {
        background-color: #f5f5f5;
        border-left: 4px solid #4caf50;
        color: #1f1f1f;
    }
    .sidebar .block-container {
        padding-top: 2rem;
    }
    h1 {
        color: #1f1f1f;
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)

# Session state initialization
if "qa_system" not in st.session_state:
    st.session_state.qa_system = None
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "video_url" not in st.session_state:
    st.session_state.video_url = ""

# Sidebar for YouTube URL input
with st.sidebar:
    st.title("YouTube Video")
    st.markdown("---")
    
    video_url = st.text_input(
        "Enter YouTube URL",
        value=st.session_state.video_url,
        placeholder="https://youtu.be/VIDEO_ID",
        key="url_input"
    )
    
    load_button = st.button("Load Video", use_container_width=True, type="primary")
    
    if load_button:
        if not video_url:
            st.warning("Please enter a YouTube URL")
        else:
            with st.spinner("Loading transcript..."):
                try:
                    transcript = load_english_transcript(video_url)
                    st.session_state.qa_system = build_rag_chain(transcript)
                    st.session_state.video_url = video_url
                    st.session_state.chat_history = []
                    st.success("Video loaded successfully!")
                    st.rerun()
                except Exception as e:
                    st.error(f"Error: {str(e)}")
    
    st.markdown("---")
    
    # Video info section
    if st.session_state.qa_system:
        st.success("Video Loaded")
        if st.button("Clear Chat", use_container_width=True):
            st.session_state.chat_history = []
            st.rerun()
        if st.button("Load New Video", use_container_width=True):
            st.session_state.qa_system = None
            st.session_state.chat_history = []
            st.session_state.video_url = ""
            st.rerun()
    else:
        st.info("No video loaded")
    
    st.markdown("---")
    st.markdown("### Tips")
    st.markdown("""
    - Paste any YouTube URL
    - Ask questions about the content
    - Get AI-powered answers
    """)

# Main chat interface
st.title("YouTube Video Chat")

if not st.session_state.qa_system:
    st.info("Start by loading a YouTube video from the sidebar")
    st.markdown("""
    ### Welcome to YouTube Video Chat!
    
    This app allows you to have a conversation with any YouTube video:
    
    1. **Paste** a YouTube URL in the sidebar
    2. **Load** the video to extract its transcript
    3. **Ask** questions about the video content
    4. **Get** instant AI-powered answers
    
    Try it now by pasting a YouTube URL in the sidebar!
    """)
else:
    # Display chat history
    for message in st.session_state.chat_history:
        if message["role"] == "user":
            st.markdown(f"""
            <div class="chat-message user-message">
                <strong>You:</strong><br>
                {message["content"]}
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="chat-message assistant-message">
                <strong>Assistant:</strong><br>
                {message["content"]}
            </div>
            """, unsafe_allow_html=True)
    
    # Chat input at the bottom
    question = st.chat_input("Ask a question about the video...")
    
    if question:
        # Add user message to history
        st.session_state.chat_history.append({"role": "user", "content": question})
        
        # Get answer
        with st.spinner("Thinking..."):
            answer = st.session_state.qa_system(question)
        
        # Add assistant message to history
        st.session_state.chat_history.append({"role": "assistant", "content": answer})
        
        # Rerun to update the display
        st.rerun()
