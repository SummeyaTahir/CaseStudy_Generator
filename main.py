import os
from dotenv import load_dotenv
import gradio as gr
import openai
import markdown  # ✅ Convert Markdown to HTML
from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import JSONResponse
import uvicorn
from prompts import SYSTEM_PROMPT

# ✅ Load environment variables
load_dotenv()
client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# ✅ Transcribe audio input using OpenAI Whisper API
def transcribe_audio(audio_path):
    if isinstance(audio_path, str) and os.path.exists(audio_path):
        with open(audio_path, "rb") as f:
            transcript = client.audio.transcriptions.create(
                model="whisper-1",
                file=f
            )
        return transcript.text
    return "❌ Invalid audio input."

# ✅ Generate case study from event details, with optional HTML conversion
def call_openai(event_details, return_html=False):
    prompt = SYSTEM_PROMPT.format(event_details)
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.5,
        max_tokens=1024,
    )
    markdown_text = response.choices[0].message.content
    return markdown.markdown(markdown_text) if return_html else markdown_text

# ✅ Gradio-friendly wrapper
def case_study_generator(event_details):
    return call_openai(event_details, return_html=False)

def case_study_from_audio(audio):
    text = transcribe_audio(audio)
    return case_study_generator(text)

# ✅ Gradio UI
with gr.Blocks() as demo:
    gr.Markdown("## 📄 iBoothMe Case Study Generator\nWrite a description or record audio.")

    with gr.Tab("Text Input"):
        text_input = gr.Textbox(label="Event Description", lines=10, placeholder="Paste informal event description here...")
        text_button = gr.Button("Generate from Text")
        text_output = gr.Markdown()  # ✅ Render markdown
        text_button.click(fn=case_study_generator, inputs=text_input, outputs=text_output)

    with gr.Tab("Audio Input"):
        audio_input = gr.Audio(type="filepath", label="Upload or Record your event description")
        audio_button = gr.Button("Generate from Audio")
        audio_output = gr.Markdown()  # ✅ Render markdown
        audio_button.click(fn=case_study_from_audio, inputs=audio_input, outputs=audio_output)

# ✅ FastAPI integration
app = FastAPI()

# ✅ Mount Gradio at /gradio
app = gr.mount_gradio_app(app, demo, path="/gradio")

# ✅ API endpoint: generate from text (returns HTML)
@app.post("/generate-text/")
async def generate_from_text(event_details: str = Form(...)):
    result_html = call_openai(event_details, return_html=True)
    return JSONResponse(content={"html": result_html})

# ✅ API endpoint: generate from audio (returns HTML)
@app.post("/generate-audio/")
async def generate_from_audio(file: UploadFile = File(...)):
    temp_path = f"temp_{file.filename}"
    with open(temp_path, "wb") as f:
        f.write(await file.read())
    try:
        transcribed_text = transcribe_audio(temp_path)
        result_html = call_openai(transcribed_text, return_html=True)
    finally:
        os.remove(temp_path)
    return JSONResponse(content={"html": result_html})

# ✅ Run the app
if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=7860, reload=True)
