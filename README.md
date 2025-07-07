# 📄 iBoothMe Case Study Generator

This is a Gradio-based AI tool that generates energetic, structured marketing case studies from informal brand activation event descriptions. It supports both **text input** and **audio input**. The audio is transcribed using **OpenAI Whisper**, and the case study is generated using **GPT-4o**.

---

## 🚀 Features

- 📝 Paste or write an informal event description  
- 🎙️ Upload or record audio to transcribe via OpenAI Whisper  
- 📋 Generates structured case studies in the format: **Challenge**, **Solution**, and optional **Results**  
- ✨ Uses a pre-defined prompt system to match real-world case study tone and format  
- 🎛️ Clean, tabbed Gradio UI with audio and text support  

---

## 🧱 Tech Stack

- Python 🐍  
- Gradio 🎛️  
- OpenAI GPT-4o & Whisper 🧠  
- dotenv for API key management 🔐  

---

## 🧩 File Structure

``` 
CaseStudy_Generator/
├── main.py
├── prompts.py 
├── .env
├── requirements.txt 
└── README.md 
```

---

## 📥 Installation & Setup

### 1. Clone the Repository

```bash
git clone https://github.com/SummeyaTahir/Clean_CaseStudy_Generator.git
cd Clean_CaseStudy_Generator
```
### 2. (Optional) Create a Virtual Environment
```bash
python -m venv venv
venv\Scripts\activate         # On Windows
# source venv/bin/activate   # On Mac/Linux
```

### 3. Install the Requirements
```bash
pip install -r requirements.txt
```

### 3. Create .env File
Create a .env file in the root directory and paste this into it:
```bash

 OPENAI_API_KEY=your-openai-api-key-here
```
### 4. ▶️ Run the App
```bash
 python main.py
```
### 5.Input & Output
User Input:

📄 Text: Paste or write informal event details

🎙️ Audio: Upload or record a voice description

Output:
A short, energetic case study with:

✅ Challenge — brand’s goal or problem

✅ Solution — how iBoothMe solved it

✅ Results (optional) — only if clear success metrics are mentioned (max 3 bullet points)

