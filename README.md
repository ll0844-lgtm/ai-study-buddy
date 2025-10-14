# AI StudyBuddy 🤖

An interactive and customizable AI-powered study assistant built with Streamlit, LangChain, and Google's Gemini models. This application allows users to ask questions via text or voice and receive contextual, persona-driven answers with audio playback.

---

## ✨ Features

-   **Interactive Chat Interface:** A clean and responsive UI built with Streamlit.
-   **Voice Input:** Ask questions by speaking into your microphone (Speech-to-Text via OpenAI Whisper).
-   **Audio Output:** Listen to the AI's response (Text-to-Speech via gTTS).
-   **Customizable AI Personas:** Switch between pre-defined personalities (e.g., Friendly Study Buddy, Python Code Expert) or create your own custom persona.
-   **Conversation Memory:** The AI remembers the context of the current conversation for relevant follow-up questions.
-   **Powered by Gemini:** Utilizes Google's fast and efficient `gemini-2.5-flash` model for high-quality responses.

---

## 🏗️ Technology Stack

| Category         | Technology & Purpose                                                                                           |
| :--------------- | :------------------------------------------------------------------------------------------------------------- |
| **Frontend** | **Streamlit** for user interaction (chat UI, voice recording, audio playback).                                 |
| **Backend** | **Python** with **LangChain** to orchestrate chat flow, model calls, and session state memory.                   |
| **Model Engine** | **Google Gemini API** (`gemini-2.5-flash`) for text generation. **OpenAI Whisper** for Speech-to-Text. **gTTS** for Text-to-Speech. |

---

## 🚀 Getting Started

Follow these instructions to set up and run the project on your local machine.

### Prerequisites

-   Python 3.8+
-   An API key from [Google AI Studio](https://makersuite.google.com/).
-   **FFmpeg:** The Whisper library requires FFmpeg. You must install it on your system:
    -   **macOS:** `brew install ffmpeg`
    -   **Debian/Ubuntu:** `sudo apt update && sudo apt install ffmpeg`
    -   **Windows:** `choco install ffmpeg` (using Chocolatey)

### Installation

1.  **Clone the repository (or download the `app.py` file):**
    ```bash
    git clone <your-repo-url>
    cd <your-repo-folder>
    ```

2.  **Create a `requirements.txt` file:**
    Create a new file named `requirements.txt` and add the following lines:
    ```
    streamlit
    python-dotenv
    langchain
    langchain-google-genai
    gTTS
    streamlit-mic-recorder
    openai-whisper
    ```

3.  **Create a virtual environment and install dependencies:**
    ```bash
    # Create and activate the virtual environment
    python -m venv venv
    source venv/bin/activate  # On Windows use: venv\Scripts\activate

    # Install the required packages
    pip install -r requirements.txt
    ```

4.  **Create a `.env` file:**
    In the root of your project folder, create a new file named `.env` and add your Google API key:
    ```
    GOOGLE_API_KEY="YOUR_GOOGLE_API_KEY_HERE"
    ```

### Running the Application

1.  **Launch the Streamlit app from your terminal:**
    ```bash
    streamlit run app.py
    ```

2.  Open your web browser and navigate to the local URL provided (usually `http://localhost:8501`).

---

## ⚙️ How to Use

1.  **Select a Persona:** Use the sidebar to choose a pre-defined persona or write your own in the "Custom" text area.
2.  **Ask a Question:**
    -   Type your question in the chat input box at the bottom.
    -   Or, click the microphone icon `🎤` to record your question and `⏹️` to stop.
3.  **Get a Response:** The AI will process your request and display the answer in the chat. An audio player will also appear, allowing you to listen to the response.
4.  **Clear History:** Click the "Clear Chat History" button in the sidebar to start a new conversation.
