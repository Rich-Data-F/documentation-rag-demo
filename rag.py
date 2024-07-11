import os
from datetime import datetime
from dotenv import load_dotenv
import psycopg2
from sqlalchemy import make_url

from llama_index.core import (
    # function to create better responses
    get_response_synthesizer,
    SimpleDirectoryReader,
    Settings,
    # abstraction that integrates various storage backends
    StorageContext,
    VectorStoreIndex
)
from llama_index.core.postprocessor import SimilarityPostprocessor
from llama_index.core.query_engine import RetrieverQueryEngine
from llama_index.core.retrievers import VectorIndexRetriever
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.llms.ollama import Ollama
from llama_index.vector_stores.postgres import PGVectorStore
# Load environment variables from the .env file

# Load .env file
load_dotenv()

#circumvoling the .env variable issue
# knowledge_base_dir="g:\My Drive\Pdfs\Sample_for_Rag" #/mnt seems not being necessary anymore /g/My Drive/Pdfs/Sample_for_Rag/TDAH/

# # Get environment variable
knowledge_base_dir = os.getenv("KNOWLEDGE_BASE_DIR")
# Check if the environment variable is loaded correctly
if os.path.exists(knowledge_base_dir):
    print('knowledge base set in environement considered')
else:
    raise ValueError("KNOWLEDGE_BASE_DIR environment variable not set")

def set_local_models(model: str = "deepseek-coder:1.3b"):
    # use Nomic
    Settings.embed_model = HuggingFaceEmbedding(
        model_name="nomic-ai/nomic-embed-text-v1.5",
        trust_remote_code=True
    )
    # setting a high request timeout in case you need to build an answer based on a large set of documents
    Settings.llm = Ollama(model=model, request_timeout=120)

def get_streamed_rag_query_engine():
    # time the execution
    start = datetime.now()
    # of course, you can store db credentials in some secret place if you want
    connection_string = "postgresql://postgres:postgres@localhost:5432"
    db_name = "postgres"
    try:
        conn = psycopg2.connect(connection_string)
        conn.autocommit = True
    except Exception as e:
        raise Exception(f"Error connecting to the database: {e}")
    try:
        set_local_models()
        db_url = make_url(connection_string)
        vector_store = PGVectorStore.from_params(
            database=db_name,
            host=db_url.host,
            password=db_url.password,
            port=db_url.port,
            user=db_url.username,
            table_name="knowledge_base_vectors",
            # embed dim for this model can be found on https://huggingface.co/nomic-ai/nomic-embed-text-v1.5
            embed_dim=768
        )
        # if index does not exist (initialization) create it and uncomment the below code
        if 'index' not in globals():
            storage_context = StorageContext.from_defaults(vector_store=vector_store)
            documents = SimpleDirectoryReader(knowledge_base_dir, recursive=True).load_data()
            global index #declare index as global to modify it
            index = VectorStoreIndex.from_documents(
                documents, storage_context=storage_context, show_progress=True
            )
        else:
            # ELSE index already exists, load it (if not exists comment the line below)
            index = VectorStoreIndex.from_vector_store(vector_store=vector_store)
    # configure retriever
        retriever = VectorIndexRetriever(
            index=index,
            similarity_top_k=10,
        )
    # configure response synthesizer
        response_synthesizer = get_response_synthesizer(streaming=True)
    # assemble query engine
        query_engine = RetrieverQueryEngine(
            retriever=retriever,
            response_synthesizer=response_synthesizer,
            # discarding nodes which similarity is below a certain threshold
            node_postprocessors=[SimilarityPostprocessor(similarity_cutoff=0.7)],
        )
    finally:
        conn.close()
    
    end = datetime.now()
    # print the time it took to execute the script
    print(f"RAG time: {(end - start).total_seconds()}")
    return query_engine

query_engine = get_streamed_rag_query_engine()