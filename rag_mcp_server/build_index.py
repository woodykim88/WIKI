import os
import sys
from dotenv import load_dotenv

# Load .env
load_dotenv()

if not os.environ.get("OPENAI_API_KEY"):
    print("Error: OPENAI_API_KEY is not set. Please set it in .env file or environment.")
    sys.exit(1)

import chromadb
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, StorageContext
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.core.node_parser import MarkdownNodeParser
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.core import Settings
from llama_index.retrievers.bm25 import BM25Retriever
import pickle

# Configuration
WIKI_DIR = "/Users/jongwookim/Library/CloudStorage/BeeStation-MyBeeStationPlus/옵시디언 (개인)/10_Projects/WIKI"
PERSIST_DIR = "./storage"

print(f"Loading documents from {WIKI_DIR} ...")

# Exclude current rag_mcp_server dir from reading
def is_valid_file(file_path):
    # Exclude unwanted directories
    excludes = ["/.obsidian/", "/rag_mcp_server/", "/.gemini/", "/.git/"]
    for ex in excludes:
        if ex in file_path:
            return False
    return file_path.endswith(".md")

# Load documents
reader = SimpleDirectoryReader(
    input_dir=WIKI_DIR,
    recursive=True,
    file_metadata=lambda x: {"filepath": x},
    required_exts=[".md"]
)

# Filter files manually if needed (SimpleDirectoryReader has exclude_filter but doing it simply)
all_docs = reader.load_data()
docs = [d for d in all_docs if is_valid_file(d.metadata['filepath'])]

print(f"Loaded {len(docs)} markdown documents.")

# Setup nodes
print("Parsing into nodes...")
parser = MarkdownNodeParser()
nodes = parser.get_nodes_from_documents(docs)
print(f"Total {len(nodes)} nodes created.")

# Global settings for OpenAI
Settings.embed_model = OpenAIEmbedding(model="text-embedding-3-small")

# 1. Setup ChromaDB Vector Store
print("Building Vector Index (Chroma)...")
db = chromadb.PersistentClient(path=PERSIST_DIR)
chroma_collection = db.get_or_create_collection("obsidian_rag")
vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
storage_context = StorageContext.from_defaults(vector_store=vector_store)

# This will generate embeddings and store them in Chroma
index = VectorStoreIndex(nodes, storage_context=storage_context)
print("Vector Index built successfully.")

# 2. Setup BM25 BM25Retriever
print("Building BM25 Index...")
bm25_retriever = BM25Retriever.from_defaults(nodes=nodes, similarity_top_k=5)

# Save the BM25 retriever using pickle or standard json
bm25_path = os.path.join(PERSIST_DIR, "bm25_retriever.pkl")
with open(bm25_path, "wb") as f:
    pickle.dump(bm25_retriever, f)
print("BM25 Index built successfully.")

print("All indexing completed!")
