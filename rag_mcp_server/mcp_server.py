import os
import sys
import json
import logging
from dotenv import load_dotenv

# Optional: Setup simple logging to a file so it doesn't pollute stdout (MCP uses stdout)
logging.basicConfig(filename='rag_mcp.log', level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s')

load_dotenv()
if not os.environ.get("OPENAI_API_KEY"):
    logging.error("OPENAI_API_KEY not set.")
    sys.exit(1)

import chromadb
from llama_index.core import VectorStoreIndex, StorageContext
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.core import Settings
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.core.retrievers import QueryFusionRetriever
import pickle

PERSIST_DIR = "./storage"

logging.info("Initializing MCP Server...")

def init_retrievers():
    Settings.embed_model = OpenAIEmbedding(model="text-embedding-3-small")
    db = chromadb.PersistentClient(path=PERSIST_DIR)
    chroma_collection = db.get_or_create_collection("obsidian_rag")
    vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
    
    # Load vector index
    try:
        index = VectorStoreIndex.from_vector_store(vector_store=vector_store)
        vector_retriever = index.as_retriever(similarity_top_k=5)
    except Exception as e:
        logging.error(f"Error loading vector store: {e}")
        return None
        
    # Load bm25
    bm25_path = os.path.join(PERSIST_DIR, "bm25_retriever.pkl")
    try:
        with open(bm25_path, "rb") as f:
            bm25_retriever = pickle.load(f)
        bm25_retriever.similarity_top_k = 5
    except Exception as e:
        logging.error(f"Error loading bm25: {e}")
        return None
        
    # Combine with QueryFusionRetriever
    retriever = QueryFusionRetriever(
        [vector_retriever, bm25_retriever],
        similarity_top_k=3,
        num_queries=1,
        mode="reciprocal_rerank",
        use_async=False
    )
    return retriever

try:
    fusion_retriever = init_retrievers()
except Exception as e:
    logging.error(f"Initialization exception: {e}")
    fusion_retriever = None

def handle_query(query: str) -> str:
    if not fusion_retriever:
        return "Error: RAG retrievers not properly initialized. Have you run build_index.py?"
    
    try:
        nodes = fusion_retriever.retrieve(query)
        result_texts = []
        for i, node in enumerate(nodes):
            meta = node.metadata
            score = node.score
            filepath = meta.get("filepath", "Unknown")
            source_text = node.get_content().strip()
            result_texts.append(f"### [Result {i+1}] Source: {filepath} (Score: {score})\n{source_text}")
            
        return "\n\n---\n\n".join(result_texts)
    except Exception as e:
        logging.error(f"Retrieval error: {e}")
        return f"Retrieval error: {e}"

# --- Minimalist MCP Server Implementation ---
def send_response(response_dict):
    sys.stdout.write(json.dumps(response_dict) + "\n")
    sys.stdout.flush()

def handle_initialize(msg_id):
    return {
        "jsonrpc": "2.0",
        "id": msg_id,
        "result": {
            "protocolVersion": "2024-11-05",
            "capabilities": {
                "tools": {}
            },
            "serverInfo": {
                "name": "obsidian-rag-server",
                "version": "1.0.0"
            }
        }
    }

def handle_tools_list(msg_id):
    return {
        "jsonrpc": "2.0",
        "id": msg_id,
        "result": {
            "tools": [
                {
                    "name": "query_wiki_rag",
                    "description": "Query the Obsidian WIKI via Hybrid RAG (BM25 + Semantic Search). Use this for any conceptual or document search questions.",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "query": {"type": "string", "description": "The search query string"}
                        },
                        "required": ["query"]
                    }
                }
            ]
        }
    }

def handle_tools_call(msg_id, params):
    name = params.get("name")
    args = params.get("arguments", {})
    if name == "query_wiki_rag":
        query = args.get("query", "")
        logging.info(f"Received query: {query}")
        result_text = handle_query(query)
        return {
            "jsonrpc": "2.0",
            "id": msg_id,
            "result": {
                "content": [
                    {"type": "text", "text": result_text}
                ],
                "isError": False
            }
        }
    else:
        return {
            "jsonrpc": "2.0",
            "id": msg_id,
            "error": {
                "code": -32601,
                "message": f"Method not found: {name}"
            }
        }

def run_server():
    logging.info("Server listening on stdio...")
    for line in sys.stdin:
        if not line.strip():
            continue
        try:
            req = json.loads(line)
        except json.JSONDecodeError:
            continue
            
        method = req.get("method")
        msg_id = req.get("id")
        
        if method == "initialize":
            send_response(handle_initialize(msg_id))
        elif method == "notifications/initialized":
            pass
        elif method == "tools/list":
            send_response(handle_tools_list(msg_id))
        elif method == "tools/call":
            params = req.get("params", {})
            send_response(handle_tools_call(msg_id, params))
        elif method == "ping":
            send_response({"jsonrpc": "2.0", "id": msg_id, "result": {}})
        else:
            if msg_id:
                # Fallback for unsupported methods
                send_response({
                    "jsonrpc": "2.0", "id": msg_id, "error": {
                        "code": -32601, "message": f"Method not found: {method}"
                    }
                })

if __name__ == "__main__":
    run_server()
