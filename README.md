# 📚 Assessly

> **Turn your PDFs into smart multiple-choice quizzes instantly!**

Assessly is an AI-powered assessment generation platform that transforms PDF and DOCX documents into interactive multiple-choice quizzes. Built with FastAPI and Streamlit, it leverages OpenAI's GPT models to create intelligent, context-aware questions from your documents.

---

## ✨ Features

- 📄 **Multi-Format Support** - Upload PDF or DOCX files
- 🤖 **AI-Powered Generation** - Smart quiz creation using OpenAI GPT models
- 🎯 **Customizable Difficulty** - Choose from Easy, Medium, or Hard questions
- 🔢 **Flexible Quiz Length** - Generate 1-20 questions per document
- 📊 **Instant Grading** - Get immediate feedback with detailed results
- 🎨 **Clean UI** - Beautiful, intuitive Streamlit interface
- ⚡ **Fast API** - High-performance FastAPI backend

---

## 🚀 Quick Start

### Prerequisites

- Python 3.12 or higher
- OpenRouter API key (for AI quiz generation)

### Installation

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd Assessly
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   ```bash
   # Windows PowerShell
   $env:CHATBOT_API_KEY="your-openrouter-api-key"
   
   # Linux/Mac
   export CHATBOT_API_KEY="your-openrouter-api-key"
   ```

### Running the Application

# Terminal 1 - Start Backend
python -m uvicorn src.api:app --host 127.0.0.1 --port 8000

# Terminal 2 - Start Frontend
python -m streamlit run src/frontend.py --server.port 8501
```

Once running, open your browser and navigate to:
- **Frontend**: http://localhost:8501
- **Backend API**: http://127.0.0.1:8000
- **API Docs**: http://127.0.0.1:8000/docs

---

## 📁 Project Structure

```
Assessly/
├── src/
│   ├── api.py          # FastAPI backend server
│   ├── backend.py      # Quiz generation logic
│   └── frontend.py     # Streamlit UI
├── requirements.txt    # Python dependencies
├── pyproject.toml      # Project configuration
└── README.md           # You are here!
```

---

## 🎯 How to Use

1. **Upload Document** 📤
   - Click "Upload Document" in the sidebar
   - Select a PDF or DOCX file

2. **Configure Quiz** ⚙️
   - Set the number of questions (1-20)
   - Choose difficulty level (Easy/Medium/Hard)

3. **Generate** 🪄
   - Click "Generate Quiz" button
   - Wait for AI to process your document

4. **Take Quiz** ✍️
   - Answer the multiple-choice questions
   - Submit when ready

5. **Review Results** 📊
   - See your score and percentage
   - Review correct answers
   - Retake if desired

---

## 🛠️ Technology Stack

| Component | Technology |
|-----------|-----------|
| **Backend** | FastAPI, Uvicorn |
| **Frontend** | Streamlit |
| **AI Model** | OpenAI GPT (via OpenRouter) |
| **PDF Processing** | pdfminer.six |
| **DOCX Processing** | python-docx |
| **HTTP Client** | requests, httpx |

---

## 🔌 API Endpoints

### `POST /upload-n-generate/`
Generate a quiz from uploaded document.

**Request:**
- `file`: PDF or DOCX file (multipart/form-data)
- `num_questions`: Integer (1-20)
- `difficulty`: String (easy/medium/hard)

**Response:**
```json
{
  "quiz_data": [
    {
      "question": "What is...",
      "options": ["A", "B", "C", "D"],
      "correct_answer": "A"
    }
  ]
}
```

### `GET /health`
Health check endpoint.

**Response:**
```json
{
  "status": "healthy"
}
```

---

## 🌟 Key Features Explained

### AI-Powered Question Generation
Uses OpenAI's GPT models through OpenRouter to analyze document content and generate contextually relevant questions with proper distractors.

### Text Preprocessing
Cleans and normalizes text from PDFs and DOCX files to ensure high-quality input for the AI model.

### Session Management
Streamlit session state maintains quiz progress, answers, and scores throughout the user experience.

### CORS Support
Configured CORS middleware allows frontend-backend communication across different ports.

---

## 🔒 Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `CHATBOT_API_KEY` | OpenRouter API key | Yes |

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

---

## 📝 License

This project is open source and available under the MIT License.

---

## 👨‍💻 Author

Built by APK gang

---

## 🐛 Troubleshooting

**Backend Connection Error**
- Ensure backend is running on port 8000
- Check if `CHATBOT_API_KEY` environment variable is set

**No Questions Generated**
- Verify document contains extractable text
- Try a different PDF/DOCX file
- Check API key validity

**Import Errors**
- Run `pip install -r requirements.txt` again
- Ensure Python 3.12+ is installed

---

## 🚧 Future Enhancements

- [ ] Support for more file formats (TXT, MD, etc.)
- [ ] Quiz history and analytics
- [ ] Export quiz results to PDF
- [ ] Multi-language support
- [ ] User authentication system
- [ ] Database integration for quiz storage

---

**Made with 🧠 AI + 💻 Code**
