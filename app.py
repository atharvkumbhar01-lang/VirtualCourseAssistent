import os
from flask import Flask, render_template, request, jsonify

from langchain_community.document_loaders import Docx2txtLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import Docx2txtLoader, TextLoader
from langchain_community.vectorstores import Chroma
from langchain_ollama import OllamaEmbeddings
from langchain.chains.retrieval_qa.base import RetrievalQA
from langchain_community.llms import Ollama

app = Flask(__name__)

# ---------------------------
# Load Documents with Metadata
# ---------------------------
def load_docs():
    folder = "docs"

    if not os.path.exists(folder):
        print("❌ docs folder not found!")
        return []

    docs = []
    files = os.listdir(folder)

    print("📂 Files found:", files)

    for file in files:
        file_path = os.path.join(folder, file)

        try:
            # ✅ LOAD TXT FILES
            if file.endswith(".txt"):
                loader = TextLoader(file_path, encoding="utf-8")
                loaded_docs = loader.load()

                for doc in loaded_docs:
                    doc.metadata["source"] = file

                docs.extend(loaded_docs)
                print(f"✅ Loaded TXT: {file}")

            # ✅ LOAD DOCX FILES
            elif file.endswith(".docx"):
                loader = Docx2txtLoader(file_path)
                loaded_docs = loader.load()

                for doc in loaded_docs:
                    doc.metadata["source"] = file

                docs.extend(loaded_docs)
                print(f"✅ Loaded DOCX: {file}")

        except Exception as e:
            print(f"⚠️ Skipping {file}: {e}")

    return docs


# ---------------------------
# Split Documents
# ---------------------------
def split_docs(docs):
    if not docs:
        print("❌ No documents to split!")
        return []

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=300,       
        chunk_overlap=50
    )

    chunks = splitter.split_documents(docs)
    print(f"✂️ Created {len(chunks)} chunks")
    return chunks


# ---------------------------
# Create Vector DB
# ---------------------------
def create_vectorstore(chunks):
    if not chunks:
        raise ValueError("❌ No text chunks found!")

    embeddings = OllamaEmbeddings(model="nomic-embed-text")  

    vectorstore = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory="db"
    )

    return vectorstore


# ---------------------------
# Create QA Chain (IMPROVED)
# ---------------------------
def create_chain(vectorstore):
    llm = Ollama(
        model="llama3",
        temperature=0,   
    )

    retriever = vectorstore.as_retriever(
        search_type="similarity",
        search_kwargs={"k": 3}  
    )

    qa = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=retriever,
        return_source_documents=True
    )

    return qa


# ---------------------------
# Initialize System
# ---------------------------
print("🔄 Loading documents...")
docs = load_docs()

print("✂️ Splitting documents...")
chunks = split_docs(docs)

print("🧠 Creating vector DB...")
vectorstore = create_vectorstore(chunks)

print("🤖 Creating chain...")
qa_chain = create_chain(vectorstore)

print("✅ App Ready!")


# ---------------------------
# Routes
# ---------------------------
@app.route("/")
def home():
    return render_template("index.html")


@app.route("/ask", methods=["POST"])
def ask():
    try:
        user_query = request.json.get("question", "")

        if not user_query:
            return jsonify({"answer": "Please ask a question."})

        result = qa_chain(user_query)

        answer = result["result"]

        #  show source (debug + accuracy check)
        sources = list(set([doc.metadata["source"] for doc in result["source_documents"]]))

        return jsonify({
            "answer": answer,
            "sources": sources
        })

    except Exception as e:
        return jsonify({"answer": str(e)})


# ---------------------------
# Run App
# ---------------------------
if __name__ == "__main__":
    app.run(debug=True)