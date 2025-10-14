# 🚀 AICTE IBM Project

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://your-app-url-here.streamlit.app) ![Python Version](https://img.shields.io/badge/Python-3.11+-blue.svg)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A multi-functional web application developed as a part of the AICTE IBM Project. This tool serves as a personal assistant for general knowledge questions and creative music generation, powered by modern generative AI models.

---

## ✨ Features

This application features two main tools in a clean, tabbed interface:

### 🧠 General AI Chat
- Functions as a powerful, general-purpose AI chatbot to answer any question.
- Leverages Google's Gemini Pro model for a wide range of knowledge and detailed responses.

### 🎵 AI Music Generator
- **Text-to-Music Creation**: Generate original, royalty-free music simply by writing a descriptive text prompt.
- **Mood & Genre Specification**: Create music tailored to a specific mood ("sad piano melody"), genre ("energetic 80s synthwave"), or purpose ("lofi chillhop beat for studying").
- **Custom Duration**: Specify the length of the generated audio clip.

---

## 🛠️ Technologies Used

- **Framework:** Streamlit
- **Language:** Python
- **Language Model:** Google Gemini Pro
- **Music Model:** Meta's MusicGen (via Replicate API)
- **Core Libraries:** langchain-google-genai, python-dotenv, replicate

---

## ⚙️ Setup and Local Installation

To run this project on your own machine, follow these steps:

1.  **Clone the repository and navigate into the directory.**
2.  **Create and activate a virtual environment.**
3.  **Install dependencies:** `pip install -r requirements.txt`
4.  **Create a `.env` file** and add your `GOOGLE_API_KEY` and `REPLICATE_API_TOKEN`.
5.  **Run the application:** `streamlit run app.py`

---

## 📄 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.