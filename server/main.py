from fastapi import FastAPI, UploadFile
from fastapi.responses import JSONResponse
from models.query_request import QueryRequest
from core.config import settings
from workflow import graph
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
import uuid
import os
import datetime
from utils.vector_service import collection
from fastapi.middleware.cors import CORSMiddleware
from utils.vector_service import vector_store

app = FastAPI()

origins = [
    "http://localhost:3000",
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def index():
    return JSONResponse({"message": "Server is up and running..."}, 200)


@app.post("/upload")
async def upload_file(file: UploadFile):
    # Store file in DB
    if not file.filename:
        return {"message": "Invalid file."}

    os.makedirs(settings.UPLOAD_DIR, exist_ok=True)

    file_name = (
        "file-"
        + datetime.datetime.now().strftime("%d%m%Y_%H%M%S")
        + "-"
        + file.filename
    )

    file_path = os.path.join(settings.UPLOAD_DIR, file_name)

    with open(file_path, "wb") as f:
        f.write(file.file.read())

    loader = PyPDFLoader(file_path)

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=512,
        chunk_overlap=64,
        add_start_index=True,
    )

    documents = text_splitter.split_documents(loader.load())

    session_id = str(uuid.uuid4())

    for doc in documents:
        doc.metadata["session_id"] = session_id

    vector_store.add_documents(
        documents=documents,
    )

    print(file_path)

    os.remove(file_path)

    return JSONResponse(
        {
            "message": "File uploaded",
            "filename": file.filename,
            "session": session_id,
        },
        200,
    )


@app.post("/query")
def ask_rag_agent(request: QueryRequest):
    query = (
        request.user_input
        if len(request.user_input) >= int(settings.QUERY_MIN_LENGTH)
        else None
    )

    if query is None:
        return JSONResponse(
            {"message": "Your query is too short to be processed by our AI"}, 400
        )

    result = graph.invoke(
        {"messages": [query], "session_id": request.session},
        config={"configurable": {"thread_id": request.session}},
    )

    return JSONResponse({"message": result["messages"][-1].content}, 200)


@app.delete("/{session_id}")
def delete_vectors_for_session(session_id: str):
    document = collection.find_one({"session_id": session_id})

    if not document:
        return JSONResponse(
            {"message": "Session does not exist with the provided ID"}, 400
        )

    collection.delete_many({"session_id": session_id})

    return JSONResponse({"message": f"Session {session_id} cleared successfully"}, 200)


import uvicorn

uvicorn.run(app, host="127.0.0.1", port=8000)
