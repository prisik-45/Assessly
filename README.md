# Assessly

**Assessly** is a web-based tool that generates quizzes from PDF or DOCX documents. Users can upload their documents, and the system extracts the text, processes it, and generates multiple-choice questions (MCQs) automatically using a Large Language Model (LLM). The quiz can then be delivered to users, and their performance is evaluated in real-time.

---

## Features

- Upload PDF or DOCX files to generate quizzes.
- Automatic text extraction using PyPDF or python-docx.
- Text preprocessing to remove noise and irrelevant content.
- Generate multiple-choice questions (MCQs) with 4 options using a Large Language Model (LLM).
- Interactive quiz interface for users to attempt questions.
- Real-time evaluation of user answers.
- Display performance results and scores.

---

## Architecture Overview

The system consists of four main modules:

### 1. User Interaction
- Users start by uploading a PDF or DOCX file.
- The system validates the upload and shows an error if unsuccessful.
- Successful uploads are sent to the FastAPI backend for processing.

### 2. Backend Processing
- **Receive file**: FastAPI receives the uploaded document.
- **Extract text**: Use PyPDF or python-docx to extract the text.
- **Preprocess text**: Clean and format text to remove noise.
- **Send to LLM**: Forward cleaned text to the LLM model for quiz generation.
- **Receive quiz**: Get generated MCQs from the LLM and send quiz data to the frontend.

### 3. LLM Model Interaction
- Generate multiple-choice questions with 4 options from the processed text.
- Return the quiz to the backend for delivery to the frontend.

### 4. Quiz Delivery and Evaluation
- **Display quiz**: Present the quiz to users.
- **Answer selection**: Users select their answers.
- **Submit and evaluate**: Submit answers for evaluation and calculate results.
- **Show performance**: Display user scores and performance metrics.

---

## Tech Stack

- **Frontend**: React.js (for interactive quiz interface)
- **Backend**: FastAPI (Python)
- **Text Extraction**: PyPDF, python-docx
- **LLM Model**: OpenAI GPT or similar for MCQ generation
- **Storage**: Local or cloud storage for uploaded files

---

## Installation

1. Clone the repository:

```bash
git clone https://github.com/yourusername/assessly.git
cd assessly
