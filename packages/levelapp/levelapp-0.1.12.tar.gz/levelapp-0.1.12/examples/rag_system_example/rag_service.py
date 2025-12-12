import os
import bs4
import dotenv

from typing import Literal, Dict, List, Any

from langchain_community.document_loaders import WebBaseLoader
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

from langchain_openai import ChatOpenAI
from langchain_community.tools import Tool
from langchain_classic.agents import initialize_agent, AgentType

dotenv.load_dotenv()
# Set a User-Agent to avoid request rejection
os.environ.setdefault(
    "USER_AGENT",
    "Mozilla/5.0 (compatible; MyRAGBot/1.0; +https://example.com/bot)"
)

SOURCE_URL = "https://lilianweng.github.io/posts/2023-06-23-agent/"
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200

# Step 1: Document Loading
def load_source_docs() -> List:
    bs4_strainer = bs4.SoupStrainer(class_=("post-title", "post-header", "post-content"))
    loader = WebBaseLoader(
        web_paths=(SOURCE_URL,),
        bs_kwargs={"parse_only": bs4_strainer},
    )
    docs = loader.load()
    return docs


# Step 2: Text Splitting
def split_docs(docs: list):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        add_start_index=True
    )
    return splitter.split_documents(documents=docs)


# Step 3: Embedding & Vector Store
def build_vector_store(docs):
    embedding_model = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)
    return FAISS.from_documents(documents=docs, embedding=embedding_model)


# Step 4: Retriever Tool
def make_retriever_tool(vector_store: FAISS):
    def retriever_context(query: str):
        retrieved_docs = vector_store.similarity_search_with_score(query=query, k=5)
        serialized = "\n\n".join(
            f"Source: {doc.metadata}\nContent: {doc.page_content}\nScore: {score}"
            for doc, score in retrieved_docs
        )
        return serialized, [doc for doc, _ in retrieved_docs]

    tool = Tool(
        name="retrieve_context",
        func=lambda query: retriever_context(query)[0],
        description="Retrieves relevant context fron the Lilian Weng agent blog post.",
    )
    return tool


# Step 5: Agent Initialization
def build_agent(vector_store: FAISS, verbose: bool = False):
    tool = make_retriever_tool(vector_store=vector_store)
    llm = ChatOpenAI(model="gpt-4o-mini")
    agent = initialize_agent(
        tools=[tool],
        llm=llm,
        agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        verbose=verbose
    )
    return agent


# Step 6: Core RAG Flow
async def run_query(
        query: str,
        output_mode: Literal["answer", "full"] = "answer",
        verbose: bool = False
) -> Dict[str, Any]:
    """Run a query through the RAG pipeline."""
    docs = load_source_docs()
    splits = split_docs(docs=docs)
    vector_store = build_vector_store(docs=splits)
    agent = build_agent(vector_store=vector_store, verbose=verbose)

    response = await agent.ainvoke(query)

    result = {"answer": response}

    if output_mode == "full":
        first_embedding = vector_store.index.reconstruct(0)
        result.update(
            {
                "retrieved_docs": [s.page_content[:500] for s in splits[:5]],
                "embedding_preview": first_embedding[:10].tolist(),
                "num_chunks": len(splits),
            }
        )

    return result

