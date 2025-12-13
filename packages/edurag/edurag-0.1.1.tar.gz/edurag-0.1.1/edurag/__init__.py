"""
EduRAG - 基于LLM的教育RAG组件

支持解题、文献分析、知识点答疑的检索增强生成系统。
"""

from edurag.core.simple_rag import SimpleRAG
from edurag.core.agentic_rag import AgenticRAG
from edurag.prompt.teacher_profile import TeacherProfile
from edurag.config import EduRAGConfig

__version__ = "0.1.1"
__all__ = [
    "SimpleRAG",
    "AgenticRAG",
    "TeacherProfile", 
    "EduRAGConfig",
    "__version__",
]

