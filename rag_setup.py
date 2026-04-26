from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_text_splitters import CharacterTextSplitter

# Android knowledge base
android_docs = [
    """NPE - NullPointerException Fix:
    Always initialize variables before use.
    Use Kotlin safe call operator ?.
    Use Elvis operator ?: for default values.
    Example: val name = user?.name ?: "Default"
    Use lateinit for late initialization.
    Use by lazy for lazy initialization.""",
    
    """ANR - Application Not Responding Fix:
    Never run heavy operations on main thread.
    Use Coroutines for async operations.
    Use Dispatchers.IO for network/database calls.
    Example: viewModelScope.launch(Dispatchers.IO) { }
    Use WorkManager for background tasks.""",
    
    """OOM - OutOfMemoryError Fix:
    Use Glide or Picasso for image loading.
    Always recycle bitmaps after use.
    Use inSampleSize to reduce bitmap size.
    Avoid memory leaks — use WeakReference.
    Use LeakCanary to detect memory leaks.
    Enable largeHeap only as last resort.""",
]

# Embeddings setup
embedding =SentenceTransformerEmbeddings(
 model_name="all-MiniLM-L6-v2"
)

# Vector store banao
vectorstore=Chroma.from_texts(
    embedding=embedding,
    texts=android_docs,
    persist_directory="./android_knowledge"
)

print("Android Knowledge Base ready!")
print(f"Total docs: {len(android_docs)}")


