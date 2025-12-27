# 🎥 YouTube Video Chat (RAG-based)

Chat with any YouTube video by asking questions about its content.

This project extracts the **English transcript** of a YouTube video, stores it in a **vector database**, and uses a **Retrieval-Augmented Generation (RAG)** pipeline to answer user questions using the video content only.

---

## 🚀 Features

- Paste any YouTube video URL
- Automatically fetch English captions
- Ask questions about the video
- Answers are grounded **only in the transcript**
- Clean, minimal RAG implementation
- Beginner-friendly architecture

---

## 🧠 Tech Stack

- **Python**
- **Streamlit** – UI
- **LangChain** – RAG pipeline
- **FAISS** – Vector database
- **HuggingFace Embeddings**
- **Groq (LLaMA 3.1)** – LLM
- **YouTube Transcript API**

---

## 🏗️ Project Structure

.
├── app.py # Streamlit UI
├── rag.py # RAG pipeline (retrieval + LLM)
├── utils.py # YouTube transcript utilities
├── hello.py # Helper script (optional)
├── requirements.txt
└── README.md


---

## ⚙️ How It Works

1. User enters a YouTube URL
2. English transcript is fetched using YouTube Transcript API
3. Transcript is split into chunks
4. Chunks are embedded and stored in FAISS
5. User question retrieves relevant chunks
6. LLM answers using **only retrieved context**

---

## ▶️ Run Locally

### 1. Clone the repo
```bash
git clone https://github.com/your-username/youtube-video-chat-rag.git
cd youtube-video-chat-rag
uv sync
. Set environment variable

Create a .env file:

GROQ_API_KEY=your_groq_api_key_here

5. Run the app
uv run streamlit run app.py