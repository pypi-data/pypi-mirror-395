"""EduRAG 全局配置"""

from dataclasses import dataclass, field
from typing import Literal, Optional


@dataclass
class EduRAGConfig:
    """EduRAG 配置类
    
    Attributes:
        llm_provider: LLM提供商，支持 openai/gemini/ollama
        llm_model: 模型名称，如 gpt-4o, gemini-pro, llama3
        api_key: API密钥（ollama本地部署时可为None）
        api_base: API基础URL，用于自定义端点或代理
        temperature: 生成温度，0-1之间
        chunk_size: 文档切分大小
        chunk_overlap: 文档切分重叠大小
        embedding_model: Embedding模型名称
        vectorstore_path: 向量存储持久化路径（None则不持久化）
    """
    
    # LLM 配置
    llm_provider: Literal["openai", "gemini", "ollama"] = "openai"
    llm_model: str = "gpt-4o"
    api_key: Optional[str] = None
    api_base: Optional[str] = None
    temperature: float = 0.7
    
    # 文档处理配置
    chunk_size: int = 1000
    chunk_overlap: int = 200
    
    # Embedding 配置
    embedding_model: str = "text-embedding-3-small"
    
    # 向量存储配置
    vectorstore_path: Optional[str] = None
    
    # 检索配置
    retrieval_top_k: int = 4
    
    def __post_init__(self):
        """验证配置"""
        if self.llm_provider in ("openai", "gemini") and not self.api_key:
            raise ValueError(f"{self.llm_provider} 需要提供 api_key")
        
        if self.chunk_size <= 0:
            raise ValueError("chunk_size 必须大于 0")
        
        if self.chunk_overlap >= self.chunk_size:
            raise ValueError("chunk_overlap 必须小于 chunk_size")

