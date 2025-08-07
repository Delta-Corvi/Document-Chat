import gradio as gr
import os
from rag.faiss_store import FaissStore
from rag.retriever import answer
from rag.pdf_loader import process_pdf
from rag.document_crud import DocumentCRUD

# Inizializza store e crud
store = FaissStore()
store.load_or_create()
crud = DocumentCRUD()

def chatbot(message, history):
    return answer(message, store)

def upload_pdf(file):
    """Handles PDF upload"""
    if file is None:
        return "❌ No file selected."

    try:
        # Process the PDF
        process_pdf(file.name, store, crud)
        filename = os.path.basename(file.name)
        return f"✅ PDF '{filename}' uploaded and processed successfully!"
    except Exception as e:
        return f"❌ Error during upload: {str(e)}"

def get_documents_info():
    """Returns information about loaded documents"""
    docs = crud.list()
    if not docs:
        return "📝 No documents loaded"

    # Group by source
    sources = {}
    for doc in docs:
        source = doc.get('source', 'Unknown')
        if source not in sources:
            sources[source] = 0
        sources[source] += 1

    info = f"📚 **Loaded documents:** {len(docs)} chunks\n\n"
    for source, count in sources.items():
        info += f"• **{source}**: {count} chunks\n"

    return info

def build_interface():
    """Builds the complete interface with chat and PDF upload"""
    with gr.Blocks(title="AI Assistant", theme=gr.themes.Soft()) as demo:
        gr.Markdown("""
        # 🤖 AI Document Assistant
        Upload PDF documents and chat with your data!
        """)

        with gr.Row():
            # Left column: Chat
            with gr.Column(scale=2):
                chatinterface = gr.ChatInterface(
                    fn=chatbot,
                    title="💬 Chat",
                    description="Ask questions about uploaded documents",
                    examples=[
                        "Summarize the main documents",
                        "What are the key points?",
                        "Search for information about..."
                    ]
                )

            # Right column: PDF upload and info
            with gr.Column(scale=1):
                with gr.Group():
                    gr.Markdown("### 📎 Upload Documents")

                    # Drag and drop section
                    pdf_upload = gr.File(
                        label="📁 Drag your PDFs here or click to select",
                        file_types=[".pdf"],
                        type="filepath",
                        height=120
                    )

                    upload_btn = gr.Button(
                        "🚀 Upload PDF",
                        variant="primary",
                        size="lg"
                    )

                    upload_status = gr.Markdown(
                        value="💡 **Tip:** Drag a PDF file into the area above to get started",
                        visible=True
                    )

                with gr.Group():
                    gr.Markdown("### 📊 Document Status")
                    docs_info = gr.Markdown(
                        value=get_documents_info(),
                        label="Loaded documents"
                    )

                    refresh_btn = gr.Button("🔄 Refresh", size="sm")

        # Events
        upload_btn.click(
            fn=upload_pdf,
            inputs=pdf_upload,
            outputs=upload_status
        ).then(
            fn=get_documents_info,
            outputs=docs_info
        )

        refresh_btn.click(
            fn=get_documents_info,
            outputs=docs_info
        )

        # Auto-update document info when a file is uploaded
        pdf_upload.change(
            fn=lambda x: "📤 File selected. Click 'Upload PDF' to process." if x else "💡 **Tip:** Drag a PDF file into the area above to get started",
            inputs=pdf_upload,
            outputs=upload_status
        )

    return demo

# Export a single function that accepts **kwargs
def launch(**kw):
    interface = build_interface()
    interface.launch(**kw)