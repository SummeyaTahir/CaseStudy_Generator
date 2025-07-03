import os
from dotenv import load_dotenv
import gradio as gr
import openai
from prompts import SYSTEM_PROMPT

# 📥 Load environment variables
load_dotenv()

client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# 🔁 Transcribe audio input using OpenAI Whisper API
def transcribe_audio(audio_file):
    with open(audio_file, "rb") as f:
        transcript = client.audio.transcriptions.create(
            model="whisper-1",
            file=f
        )
    return transcript.text

# 💬 Call OpenAI chat with the transcribed or text input
def call_openai(event_details):
    prompt = SYSTEM_PROMPT.format(event_details)
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.5,
        max_tokens=1024,
    )
    return response.choices[0].message.content

# 🔄 New function to handle audio input and route to existing pipeline
def case_study_from_audio(audio):
    text = transcribe_audio(audio)
    return case_study_generator(text)

# 🎛️ Original function — unchanged
def case_study_generator(event_details):
    gpt_response = call_openai(event_details)
    return gpt_response

# 🚀 Gradio interface with two modes: Text or Audio
with gr.Blocks() as demo:
    gr.Markdown("## 📄 iBoothMe Case Study Generator\nWrite a description or record audio.")
    with gr.Tab("Text Input"):
        text_input = gr.Textbox(
            label="Event Description",
            lines=10,
            placeholder="Paste informal event description here...",
        )
        text_button = gr.Button("Generate from Text")
        text_output = gr.Textbox(label="Generated Case Study", lines=15)
        text_button.click(fn=case_study_generator, inputs=text_input, outputs=text_output)

    with gr.Tab("Audio Input"):
        audio_input = gr.Audio(type="filepath", label="Upload or Record your event description")
        audio_button = gr.Button("Generate from Audio")
        audio_output = gr.Textbox(label="Generated Case Study", lines=15)
        audio_button.click(fn=case_study_from_audio, inputs=audio_input, outputs=audio_output)

demo.launch()
