import os
import streamlit as st
from streamlit_webrtc import WebRtcMode, webrtc_streamer
from src.voice_to_text import transcribe_audio
from src.text_to_pdf import text_to_pdf
from src.summarizer import summarize_transcript
from src.audio_webrtc import AudioSaver, save_audio_file

# --- Page setup ---
st.set_page_config(page_title="Voice2Summary", layout="centered")
st.title("🎙️ Voice2Summary Pro")
st.markdown("Convert your voice into transcripts, summaries, and PDFs using AI")

# --- Ensure folders exist ---
for folder in ["audio_input", "transcripts", "pdfs", "summaries"]:
    os.makedirs(folder, exist_ok=True)

# --- Upload Section ---
st.subheader("📂 Upload an Audio File")
uploaded_file = st.file_uploader("Choose file", type=["mp3", "wav", "m4a"])

if uploaded_file:
    audio_path = os.path.join("audio_input", uploaded_file.name)
    with open(audio_path, "wb") as f:
        f.write(uploaded_file.read())

    base = os.path.splitext(uploaded_file.name)[0]
    transcript_path = f"transcripts/{base}.txt"
    pdf_path = f"pdfs/{base}.pdf"
    summary_path = f"summaries/{base}_summary.txt"

    with st.spinner("🔁 Transcribing..."):
        transcript = transcribe_audio(audio_path, transcript_path)

    with st.spinner("📄 Generating PDF..."):
        text_to_pdf(transcript_path, pdf_path)

    with st.spinner("🧠 Summarizing..."):
        summary = summarize_transcript(transcript_path, summary_path)

    st.success("✅ Done!")
    tab1, tab2 = st.tabs(["📜 Transcript", "🧠 Summary"])
    with tab1:
        st.text_area("Transcript", transcript, height=300)
        st.download_button("⬇️ Download PDF", open(pdf_path, "rb").read(), file_name=os.path.basename(pdf_path))
    with tab2:
        st.markdown(f"<div style='background:#f1f3f4;padding:20px;border-radius:10px'>{summary}</div>", unsafe_allow_html=True)
        st.download_button("⬇️ Download Summary", open(summary_path, "rb").read(), file_name=os.path.basename(summary_path))

# --- Live Audio Recording with WebRTC ---
st.subheader("🎤 Or Record Live Audio")

ctx = webrtc_streamer(
    key="audio",
    mode=WebRtcMode.SENDONLY,   # 🔥 correct enum usage
    audio_processor_factory=AudioSaver,
    media_stream_constraints={"audio": True, "video": False},
    async_processing=True,
)

if ctx.audio_processor and st.button("✅ Process Recording"):
    audio_path = save_audio_file(ctx.audio_processor.frames)
    
    if audio_path:
        base = os.path.splitext(os.path.basename(audio_path))[0]
        transcript_path = f"transcripts/{base}.txt"
        pdf_path = f"pdfs/{base}.pdf"
        summary_path = f"summaries/{base}_summary.txt"

        with st.spinner("🔁 Transcribing..."):
            transcript = transcribe_audio(audio_path, transcript_path)

        with st.spinner("📄 Generating PDF..."):
            text_to_pdf(transcript_path, pdf_path)

        with st.spinner("🧠 Summarizing..."):
            summary = summarize_transcript(transcript_path, summary_path)

        st.success("✅ Done!")
        tab1, tab2 = st.tabs(["📜 Transcript", "🧠 Summary"])
        with tab1:
            st.text_area("Transcript", transcript, height=300)
            st.download_button("⬇️ Download PDF", open(pdf_path, "rb").read(), file_name=os.path.basename(pdf_path))
        with tab2:
            st.markdown(f"<div style='background:#f1f3f4;padding:20px;border-radius:10px'>{summary}</div>", unsafe_allow_html=True)
            st.download_button("⬇️ Download Summary", open(summary_path, "rb").read(), file_name=os.path.basename(summary_path))

st.markdown("---")
st.markdown("<center>Made with ❤️ by Netedge</center>", unsafe_allow_html=True)
