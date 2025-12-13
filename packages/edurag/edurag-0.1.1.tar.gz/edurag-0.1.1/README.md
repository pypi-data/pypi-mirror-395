# EduRAG

An LLM-based Retrieval-Augmented Generation (RAG) component for education, supporting problem solving, academic literature analysis, and knowledge Q&A.

## Features

- **Two RAG Modes**: SimpleRAG (simple & efficient) and AgenticRAG (intelligent reasoning)
- **Multi-LLM Support**: OpenAI GPT series, Google Gemini, Ollama local models
- **Multiple Document Formats**: PDF, DOCX, DOC, TXT, Markdown
- **Teacher Persona Customization**: Custom teacher name, subject, grade level, teaching style
- **Multi-turn Conversation**: Context-aware continuous Q&A
- **Vector Store Persistence**: Avoid repeated embedding, fast knowledge base loading

## Installation

```bash
pip install edurag
```

Install optional dependencies:

```bash
# Use AgenticRAG (based on LangGraph)
pip install edurag[agentic]

# Use Google Gemini
pip install edurag[gemini]

# Use Ollama local models
pip install edurag[ollama]

# Install all optional dependencies
pip install edurag[all]
```

## Quick Start

### Basic Usage

```python
from edurag import SimpleRAG

# Initialize
rag = SimpleRAG(api_key="your-openai-api-key")

# Load documents
rag.load_documents("textbook.pdf")

# Ask questions
answer = rag.ask("What is the main content of this document?")
print(answer)
```

### Custom Teacher Persona

```python
from edurag import SimpleRAG, TeacherProfile

# Create teacher profile
teacher = TeacherProfile(
    name="Mr. Wang",
    subject="High School Physics",
    grade_level="Grade 12",
    teaching_style="Focus on concept understanding, good at explaining abstract principles with real-life examples",
    introduction="20 years of teaching experience, physics competition coach"
)

# Initialize RAG
rag = SimpleRAG(
    api_key="your-openai-api-key",
    teacher_profile=teacher
)

# Load textbooks
rag.load_documents([
    "physics_chapter1.pdf",
    "mechanics_topics.docx"
])

# Ask - AI will respond as Mr. Wang with his teaching style
answer = rag.ask("Why is the acceleration of free fall constant?")
```

### Using Different LLMs

```python
# OpenAI
rag = SimpleRAG(
    api_key="sk-xxx",
    llm_provider="openai",
    llm_model="gpt-4o"
)

# Google Gemini
rag = SimpleRAG(
    api_key="your-google-key",
    llm_provider="gemini",
    llm_model="gemini-pro"
)

# Ollama local model (no API Key required)
rag = SimpleRAG(
    llm_provider="ollama",
    llm_model="llama3"
)
```

### Persistent Vector Store

```python
# First time: auto-save vector store
rag = SimpleRAG(
    api_key="sk-xxx",
    vectorstore_path="./my_knowledge_base"
)
rag.load_documents("./documents/")

# Later: load existing store (skip embedding)
rag = SimpleRAG.from_vectorstore(
    vectorstore_path="./my_knowledge_base",
    api_key="sk-xxx"
)
```

### AgenticRAG (Intelligent Reasoning)

Suitable for complex problems. The Agent autonomously decides whether to retrieve and supports multi-step reasoning.

```python
from edurag import AgenticRAG, TeacherProfile

teacher = TeacherProfile(
    name="Mr. Wang",
    subject="High School Physics",
    grade_level="Grade 12",
    teaching_style="Good at analogies, explains with real-life examples"
)

rag = AgenticRAG(
    api_key="sk-xxx",
    teacher_profile=teacher
)

rag.load_documents(["physics_textbook.pdf"])

# Agent automatically decides whether to retrieve, supports multi-step reasoning
answer = rag.ask("Compare the similarities and differences of Newton's three laws")

# View reasoning process
result = rag.ask_with_steps("Explain the law of conservation of momentum")
print(result["steps"])  # View Agent's reasoning steps
print(result["answer"]) # Final answer
```

**SimpleRAG vs AgenticRAG:**

| Feature | SimpleRAG | AgenticRAG |
|---------|-----------|------------|
| Retrieval | Always retrieves | Agent decides |
| Reasoning | Single-step | Multi-step |
| Speed | Faster | Slower |
| Cost | Lower | Higher |
| Use Case | Simple Q&A | Complex analysis |

## API Reference

### SimpleRAG

Main RAG class providing document loading and Q&A functionality.

#### Initialization Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `api_key` | str | None | LLM API key |
| `llm_provider` | str | "openai" | LLM provider: openai/gemini/ollama |
| `llm_model` | str | "gpt-4o" | Model name |
| `teacher_profile` | TeacherProfile | None | Teacher persona configuration |
| `config` | EduRAGConfig | None | Full configuration object |

#### Methods

- `load_documents(sources)`: Load documents into knowledge base
- `ask(question)`: Ask and get answer
- `ask_with_sources(question)`: Ask and return answer with source documents
- `search(query, top_k)`: Directly search relevant documents
- `clear_history()`: Clear conversation history
- `save_vectorstore(path)`: Save vector store

### TeacherProfile

Teacher persona configuration class.

```python
from edurag import TeacherProfile

teacher = TeacherProfile(
    name="Mr. Li",              # Teacher name
    subject="Mathematics",       # Teaching subject
    grade_level="Middle School", # Grade level
    teaching_style="...",        # Teaching style
    introduction="...",          # Introduction (optional)
    language="English"           # Response language
)
```

### EduRAGConfig

Full configuration class for advanced customization.

```python
from edurag import EduRAGConfig

config = EduRAGConfig(
    llm_provider="openai",
    llm_model="gpt-4o",
    api_key="sk-xxx",
    temperature=0.7,           # Generation temperature
    chunk_size=1000,           # Document chunk size
    chunk_overlap=200,         # Chunk overlap
    retrieval_top_k=4,         # Number of retrieval results
    vectorstore_path=None      # Vector store path
)
```

## Preset Teacher Templates

```python
from edurag.prompt.teacher_profile import PRESET_TEACHERS

# Available presets
teacher = PRESET_TEACHERS["physics_senior"]    # High School Physics
teacher = PRESET_TEACHERS["math_college"]      # College Mathematics
teacher = PRESET_TEACHERS["english_junior"]    # Middle School English
teacher = PRESET_TEACHERS["chemistry_senior"]  # High School Chemistry
```

## License

MIT
