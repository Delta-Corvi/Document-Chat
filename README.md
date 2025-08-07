Document Chat

This project is the Module1 publication for Ready Tensor Agentic AI Developer Certification 2025: AAIDC2025 

A powerful document management and conversation system that enables users to upload PDFs, process them with advanced AI embeddings, and have intelligent conversations with their documents using Google's Gemini AI.

🚀 Features
    • PDF Document Upload: Drag-and-drop or browse to upload PDF documents 
    • Intelligent Document Processing: Automatic text extraction and chunking with overlap for better context retention 
    • Vector Search: FAISS-powered vector similarity search for relevant document retrieval 
    • AI-Powered Chat: Conversational interface using Google Gemini 1.5 Flash for natural language interactions 
    • Persistent Storage: Documents and metadata are stored locally for future sessions 
    • Real-time Processing: Live feedback during document upload and processing 
    • Modern UI: Clean, intuitive Gradio interface with drag-and-drop functionality 
🏗️ Architecture
The application follows a modular architecture with clear separation of concerns:
    • Document Processing Pipeline: Handles PDF text extraction and intelligent chunking 
    • Vector Store Management: FAISS-based embedding storage and retrieval 
    • Conversation Management: Google Gemini integration for AI responses 
    • Database Management: JSONL-based document metadata storage 
    • Web Interface: Gradio-powered responsive web UI 
📁 Project Structure
Progetto Eng/
├── main.py                    # Application entry point with server management
├── requirements.txt           # Python dependencies
├── .env                      # Environment variables (Google API key)
├── rag/                      # RAG system modules
│   ├── document_crud.py      # Document metadata management
│   ├── embedding.py          # Google Gemini embedding integration
│   ├── faiss_store.py        # FAISS vector database operations
│   ├── pdf_loader.py         # PDF processing and chunking
│   └── retriever.py          # Document retrieval and AI response generation
├── ui/
│   └── gradio_app.py         # Gradio web interface
└── data/                     # Document storage and metadata
    ├── documents.jsonl       # Document metadata database
    ├── faiss.index          # FAISS vector index
    └── metadata.jsonl       # Vector metadata
🛠️ Dependencies
The project uses the following Python modules:
python-dotenv              # Environment variable management
google-generativeai        # Google Gemini AI integration
faiss-cpu                  # Vector similarity search
gradio                     # Web interface framework
numpy                      # Numerical computing
pandas                     # Data manipulation
pymupdf                    # PDF text extraction
sentence-transformers      # Alternative embedding models (optional)
🔧 Installation
    1. Clone the repository: 
git clone <repository-url>
cd gemini-document-chat
    2. Create a virtual environment: 
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
    3. Install dependencies: 
pip install -r requirements.txt
    4. Configure environment variables: Create a .env file in the project root and add your Google API key: 
GEMINI_API_KEY=your_google_gemini_api_key_here
Important: You need a valid Google Gemini API key. Get one from Google AI Studio
🚀 Usage
    1. Start the application: 
python main.py
Optional parameters:
    • --port: Specify custom port (default: 7860) 
    • --no-browser: Don't open browser automatically 
    2. Access the interface: Open your browser and navigate to http://localhost:7860
    3. Upload and chat with documents:
        ◦ Drag and drop PDF files into the upload area 
        ◦ Click "Upload PDF" to process the document 
        ◦ Use the chat interface to ask questions about your documents 
        ◦ View document status in the sidebar 
💡 How It Works
    1. Document Upload: PDFs are uploaded and stored in the data/ directory 
    2. Text Extraction: PyMuPDF extracts text content from PDF files 
    3. Chunking: Documents are split into overlapping chunks (800 chars with 100 char overlap) 
    4. Embedding: Google Gemini's embedding model converts chunks to vector representations 
    5. Storage: Vectors are stored in FAISS index with metadata in JSONL format 
    6. Retrieval: User queries are embedded and matched against document vectors 
    7. Generation: Relevant chunks are sent to Gemini 1.5 Flash for contextual responses 
🔍 Technical Details
    • Embedding Model: Google's models/embedding-001 for document vectorization 
    • LLM: Gemini 1.5 Flash for conversational responses 
    • Vector Database: FAISS with Inner Product similarity search 
    • Document Format: Currently supports PDF files 
    • Chunking Strategy: Fixed-size chunks with overlap for context preservation 
    • Storage: Local filesystem with JSONL metadata format 
🚨 Requirements
    • Python 3.8+ 
    • Google Gemini API access 
    • Sufficient disk space for document storage 
    • Internet connection for AI model access 
⚠️ Limitations
    • Currently supports PDF documents only 
    • Requires internet connection for AI features 
    • Google API rate limits may apply 
    • Vector index is rebuilt on each startup (no persistent FAISS index loading optimization yet) 
🤝 Contributing
Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.
📄 License
This project is open source and available under the MIT License.
🔗 Related Projects
This project draws inspiration from modern RAG architectures and document management systems. It demonstrates practical implementation of:
    • Google Gemini AI integration 
    • FAISS vector search 
    • Gradio web interfaces 
    • Modular Python architecture 

Note: Make sure to keep your Google API key secure and never commit it to version control. Use the .env file as specified in the setup instructions.
