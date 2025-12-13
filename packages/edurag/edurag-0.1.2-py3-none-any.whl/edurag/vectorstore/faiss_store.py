"""FAISS 向量存储封装"""

from pathlib import Path
from typing import Optional, Union
from langchain_core.documents import Document
from langchain_core.embeddings import Embeddings
from langchain_community.vectorstores import FAISS


class FAISSVectorStore:
    """FAISS 向量存储封装
    
    提供文档向量化、存储、检索的统一接口。
    
    Example:
        >>> from edurag.llm import create_embeddings
        >>> embeddings = create_embeddings("openai", api_key="sk-xxx")
        >>> store = FAISSVectorStore(embeddings)
        >>> store.add_documents(docs)
        >>> results = store.search("牛顿第二定律", top_k=3)
    """
    
    def __init__(self, embeddings: Embeddings):
        """初始化向量存储
        
        Args:
            embeddings: Embeddings实例，用于文本向量化
        """
        self.embeddings = embeddings
        self._vectorstore: Optional[FAISS] = None
    
    @property
    def is_initialized(self) -> bool:
        """检查向量存储是否已初始化"""
        return self._vectorstore is not None
    
    def add_documents(self, documents: list[Document]) -> None:
        """添加文档到向量存储
        
        Args:
            documents: 文档列表
        """
        if not documents:
            raise ValueError("文档列表不能为空")
        
        if self._vectorstore is None:
            # 首次添加，创建新的向量存储
            self._vectorstore = FAISS.from_documents(documents, self.embeddings)
        else:
            # 追加到现有向量存储
            self._vectorstore.add_documents(documents)
    
    def search(
        self,
        query: str,
        top_k: int = 4,
        score_threshold: Optional[float] = None
    ) -> list[Document]:
        """相似度搜索
        
        Args:
            query: 查询文本
            top_k: 返回结果数量
            score_threshold: 相似度阈值（可选）
            
        Returns:
            相关文档列表
        """
        if not self.is_initialized:
            raise RuntimeError("向量存储未初始化，请先调用 add_documents")
        
        if score_threshold is not None:
            # 带分数过滤的搜索
            docs_with_scores = self._vectorstore.similarity_search_with_score(
                query, k=top_k
            )
            # 过滤低于阈值的结果（注意：FAISS返回的是距离，越小越相似）
            return [doc for doc, score in docs_with_scores if score <= score_threshold]
        else:
            return self._vectorstore.similarity_search(query, k=top_k)
    
    def search_with_scores(
        self,
        query: str,
        top_k: int = 4
    ) -> list[tuple[Document, float]]:
        """带相似度分数的搜索
        
        Args:
            query: 查询文本
            top_k: 返回结果数量
            
        Returns:
            (文档, 分数) 元组列表
        """
        if not self.is_initialized:
            raise RuntimeError("向量存储未初始化，请先调用 add_documents")
        
        return self._vectorstore.similarity_search_with_score(query, k=top_k)
    
    def as_retriever(self, top_k: int = 4, **kwargs):
        """转换为 LangChain Retriever
        
        Args:
            top_k: 检索结果数量
            **kwargs: 其他retriever参数
            
        Returns:
            VectorStoreRetriever 实例
        """
        if not self.is_initialized:
            raise RuntimeError("向量存储未初始化，请先调用 add_documents")
        
        return self._vectorstore.as_retriever(
            search_kwargs={"k": top_k, **kwargs}
        )
    
    def save(self, path: Union[str, Path]) -> None:
        """保存向量存储到本地
        
        Args:
            path: 保存路径
        """
        if not self.is_initialized:
            raise RuntimeError("向量存储未初始化，无法保存")
        
        self._vectorstore.save_local(str(path))
    
    def load(self, path: Union[str, Path]) -> None:
        """从本地加载向量存储
        
        Args:
            path: 存储路径
        """
        path = Path(path)
        if not path.exists():
            raise FileNotFoundError(f"向量存储路径不存在: {path}")
        
        self._vectorstore = FAISS.load_local(
            str(path),
            self.embeddings,
            allow_dangerous_deserialization=True
        )
    
    @classmethod
    def from_documents(
        cls,
        documents: list[Document],
        embeddings: Embeddings
    ) -> "FAISSVectorStore":
        """从文档列表创建向量存储
        
        Args:
            documents: 文档列表
            embeddings: Embeddings实例
            
        Returns:
            FAISSVectorStore 实例
        """
        store = cls(embeddings)
        store.add_documents(documents)
        return store
    
    @classmethod
    def from_local(
        cls,
        path: Union[str, Path],
        embeddings: Embeddings
    ) -> "FAISSVectorStore":
        """从本地加载向量存储
        
        Args:
            path: 存储路径
            embeddings: Embeddings实例
            
        Returns:
            FAISSVectorStore 实例
        """
        store = cls(embeddings)
        store.load(path)
        return store

