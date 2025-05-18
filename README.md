# 🧠 Jarvis-Like AI Assistant using Python

Inspired by Iron Man's iconic AI, this project is a fully functional, voice-controlled AI assistant built using Python. 
It integrates real-time data handling, voice recognition, image generation, and automation to perform diverse tasks — from answering queries to executing system commands.

---

## 🚀 Features

- 🎙 **Voice Recognition & Interaction**  
  Converts voice to text and understands WH-type questions for responsive interaction.

- 🧠 **AI-Powered Decision Making**  
  A custom model classifies incoming queries into:
  - General (static knowledge)
  - Real-time (internet data fetch)
  - Automation (system/application tasks)

- 🌐 **Real-Time Query Processing**  
  Fetches up-to-date information like current events or stock prices using integrated search APIs.

- 🖼️ **Image Generation**  
  Uses Hugging Face API to generate AI-powered images from user-defined text prompts (e.g., “Tony Stark in a futuristic suit”)

- 💬 **Persistent Chat Memory**  
  Remembers conversations and user-provided data across sessions (like name, age, preferences).

- 🖥️ **System Automation**  
  Executes commands like opening/closing apps, playing music, generating leave letters, etc.

- 🔊 **Text-to-Speech & Custom Voice**  
  Responds using customizable speech output and supports voice selection.

- 🧵 **Threaded Execution**  
  Runs frontend and backend in parallel using threading for seamless interaction.

- 💡 **UI Integration**  
  Chat interface for real-time user input, assistant responses, and voice status indicators.

---

## 📁 Project Structure
```
AI-CHATBOT_ASSISTANT/
├── .venv/                       # Python virtual environment
│
├── Backend/                     # Core AI logic and modules
│   ├── __pycache__/             # Compiled Python files
│   ├── Automation.py            # Handles system automation tasks
│   ├── Chatbot.py               # Conversation handling logic
│   ├── ImageGeneration.py       # Text-to-image generation using AI
│   ├── Model.py                 # Query classification and decision making
│   ├── RealTimeSearchEngine.py  # Live web search integration
│   ├── SpeechToText.py          # Voice input handling
│   ├── TextToSpeech.py          # Voice output using TTS
│   └── tempCodeRunnerFile.py    # Temporary dev file (optional)
│
├── Data/                        # Runtime and static assistant data
│   ├── ChatLog.json             # Persistent chat memory
│   ├── speech.mp3               # Temporary TTS output
│   ├── Titiksha_Didi2.jpg       # Sample image file
│   └── Voice.html               # Voice control template (UI)
│
├── Frontend/                    # Assistant interface and settings
│   ├── __pycache__/             # Compiled Python files
│   ├── Files/
│       ├── Database.data        # Local data or Q&A base
│       ├── ImageGeneration.data # Image generation configuration
│       ├── Mic.data             # Microphone status/settings
│       ├── Response.data        # Assistant response templates
│       └── Status.data          # Runtime assistant/system status
│   ├──Graphics/                 # GUI & graphic images
│   └── Gul.py                   # GUI layout and visuals
│
├── .env                         # API keys and environment configs
├── Main.py                      # Entry point of the application
└── Requirements.txt             # Python dependencies list
```
---
<details>
  
## 🔧 Installation

1. Clone the repository
   
    - [🔗 GitHub Repository](https://github.com/Jatin-35/AI-ChatBot-Voice-Assistant-.git)
      
    - **cd** AI-ChatBot-Voice-Assistant

2. Create a virtual environment

    - **python** -m venv venv
   
    - **source** venv/bin/activate  # or `venv\Scripts\activate` on Windows
   
3. Install dependencies

    - **pip** install -r requirements.txt

4. Set up your API keys

    - Get keys from:
        - 🔑 [Hugging Face](https://huggingface.co/settings/tokens)
        - 🧬 [Cohere API-Key](https://dashboard.cohere.com/api-keys) 
        - 🌐 [Google Cloud](https://console.cloud.google.com/)
        - ☁️ [Groq Cloud](https://console.groq.com/keys)
        - 🔍 [Serp API-Key](https://serpapi.com/manage-api-key)  
          
    - Place your Hugging Face API key, Google Search API key, etc., in environment variables or config files as per instructions in Model.py and ImageGeneration.py.

5. Run the assistant

   - **python** Main.py

---

## 🧠 How It Works

- The assistant listens to voice commands.

- It classifies the query type (general, real-time, or automation) using a decision-making model.

- Based on the classification:

    - It responds using **LLMs** (like ChatGPT-style for general queries),

    - Fetches live data for real-time queries,

    - Executes automation tasks (like opening apps, playing media, etc.)

- It also retains memory across sessions using **Chatlog.json**.

---

## 💻 Usage Examples

Here are some real-world voice commands you can try with your assistant:

| 🧠 Command Type       | 🎤 Example Voice Command                     | 💡 What It Does                                     |
|-----------------------|---------------------------------------------|-----------------------------------------------------|
| Real-Time Query       | "What's the current Bitcoin price?"         | Fetches live crypto data using search APIs          |
| General Knowledge     | "Who is the Prime Minister of India?"       | Uses LLM to respond with general facts              |
| Automation            | "Open Spotify and play LoFi music"          | Launches Spotify and plays music via automation     |
| File Handling         | "Create a leave application for sick leave" | Auto-generates and saves a leave letter             |
| Image Generation      | "Draw a cyberpunk city at night"            | Generates an AI image using Hugging Face API        |
| Personal Info Recall  | "What's my favorite food?"                  | Responds using data remembered from past sessions   |

---

## 🔄 Version Comparison 

| 🔢 Version     |   ✨ Features Added                               |
|----------------|----------------------------------------------------|
| v1.0           | Basic voice interaction, simple automation         |
| v1.5           | Image generation, chat memory                      |
| v2.0           | Real-time queries, threaded UI, enhanced NLP       |
| v2.5 (Upcoming)| Emotion tone control, web dashboard, multi-language|

---

## 🔮 Future Enhancements

- 🎭 Emotion-based tone switching in TTS

- 🌐 Web dashboard for history, control, and settings

- 🧬 Custom AI model training from user interactions

- 🌍 Multi-language interaction support

- 🙋 Personal user profiles for adaptive behavior

---

## 🤝 Contribute or Hire
 I welcome contributions and ideas. If you have blog suggestions or freelance opportunities, feel free to contact me via DM on socials.

</details>
