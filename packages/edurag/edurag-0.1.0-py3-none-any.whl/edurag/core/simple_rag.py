"""Simple RAG 实现

基于 ConversationalRetrievalChain 的传统RAG实现，
支持多轮对话和教师人设定制。
"""

from pathlib import Path
from typing import Optional, Union

from langchain_core.documents import Document
from langchain.chains import ConversationalRetrievalChain
from langchain_core.prompts import SystemMessagePromptTemplate, ChatPromptTemplate
from langchain_core.messages import SystemMessage

from edurag.config import EduRAGConfig
from edurag.prompt.teacher_profile import TeacherProfile
from edurag.llm.provider import create_llm, create_embeddings
from edurag.document.loader import DocumentLoader
from edurag.document.splitter import create_splitter
from edurag.vectorstore.faiss_store import FAISSVectorStore


class SimpleRAG:
    """Simple RAG 实现
    
    基于检索增强生成的问答系统，支持：
    - 多种LLM（OpenAI、Gemini、Ollama）
    - 多种文档格式（PDF、DOCX、TXT）
    - 自定义教师人设
    - 多轮对话历史
    
    Example:
        >>> from edurag import SimpleRAG, TeacherProfile
        >>> 
        >>> teacher = TeacherProfile(
        ...     name="物理王老师",
        ...     subject="高中物理",
        ...     grade_level="高三",
        ...     teaching_style="注重概念理解，善于用实例解释"
        ... )
        >>> 
        >>> rag = SimpleRAG(
        ...     api_key="sk-xxx",
        ...     teacher_profile=teacher
        ... )
        >>> rag.load_documents(["物理教材.pdf"])
        >>> 
        >>> answer = rag.ask("什么是牛顿第二定律？")
        >>> print(answer)
    """
    
    def __init__(
        self,
        api_key: Optional[str] = None,
        llm_provider: str = "openai",
        llm_model: str = "gpt-4o",
        teacher_profile: Optional[TeacherProfile] = None,
        config: Optional[EduRAGConfig] = None,
        **kwargs
    ):
        """初始化 SimpleRAG
        
        Args:
            api_key: LLM API密钥
            llm_provider: LLM提供商 (openai/gemini/ollama)
            llm_model: 模型名称
            teacher_profile: 教师人设配置
            config: 完整配置对象（优先级高于单独参数）
            **kwargs: 其他配置参数，传递给 EduRAGConfig
        """
        # 配置处理
        if config is not None:
            self.config = config
        else:
            # 合并参数
            config_kwargs = {
                "llm_provider": llm_provider,
                "llm_model": llm_model,
                **kwargs
            }
            if api_key:
                config_kwargs["api_key"] = api_key
            self.config = EduRAGConfig(**config_kwargs)
        
        self.teacher_profile = teacher_profile
        self.chat_history: list[tuple[str, str]] = []
        
        # 初始化LLM
        self._llm = create_llm(
            provider=self.config.llm_provider,
            model=self.config.llm_model,
            api_key=self.config.api_key,
            api_base=self.config.api_base,
            temperature=self.config.temperature
        )
        
        # 初始化Embeddings
        self._embeddings = create_embeddings(
            provider=self.config.llm_provider,
            model=self.config.embedding_model if self.config.llm_provider == "openai" else None,
            api_key=self.config.api_key,
            api_base=self.config.api_base
        )
        
        # 向量存储（延迟初始化）
        self._vectorstore: Optional[FAISSVectorStore] = None
        self._qa_chain = None
        
        # 如果配置了持久化路径且存在，尝试加载
        if self.config.vectorstore_path:
            path = Path(self.config.vectorstore_path)
            if path.exists():
                self._load_vectorstore(path)
    
    def load_documents(
        self,
        sources: Union[str, Path, list[Union[str, Path]]],
        chunk_size: Optional[int] = None,
        chunk_overlap: Optional[int] = None
    ) -> int:
        """加载文档到知识库
        
        Args:
            sources: 文档路径，可以是：
                - 单个文件路径
                - 目录路径（自动加载目录下所有支持的文件）
                - 文件路径列表
            chunk_size: 文档切分大小，None则使用配置默认值
            chunk_overlap: 切分重叠大小，None则使用配置默认值
            
        Returns:
            加载的文档块数量
        """
        # 标准化输入
        if isinstance(sources, (str, Path)):
            sources = [sources]
        
        # 加载文档
        all_docs = []
        for source in sources:
            path = Path(source)
            if path.is_dir():
                docs = DocumentLoader.load_directory(path)
            else:
                docs = DocumentLoader.load(path)
            all_docs.extend(docs)
        
        if not all_docs:
            raise ValueError("未加载到任何文档")
        
        # 切分文档
        splitter = create_splitter(
            method="recursive",
            chunk_size=chunk_size or self.config.chunk_size,
            chunk_overlap=chunk_overlap or self.config.chunk_overlap
        )
        split_docs = splitter.split_documents(all_docs)
        
        # 构建向量存储
        if self._vectorstore is None:
            self._vectorstore = FAISSVectorStore(self._embeddings)
        
        self._vectorstore.add_documents(split_docs)
        
        # 重建QA链
        self._build_qa_chain()
        
        # 持久化（如果配置了路径）
        if self.config.vectorstore_path:
            self._vectorstore.save(self.config.vectorstore_path)
        
        return len(split_docs)
    
    def add_documents(self, documents: list[Document]) -> int:
        """直接添加 Document 对象
        
        Args:
            documents: LangChain Document 列表
            
        Returns:
            添加的文档数量
        """
        if self._vectorstore is None:
            self._vectorstore = FAISSVectorStore(self._embeddings)
        
        self._vectorstore.add_documents(documents)
        self._build_qa_chain()
        
        return len(documents)
    
    def _load_vectorstore(self, path: Path) -> None:
        """加载已有的向量存储"""
        self._vectorstore = FAISSVectorStore.from_local(path, self._embeddings)
        self._build_qa_chain()
    
    def _build_qa_chain(self) -> None:
        """构建问答链"""
        if self._vectorstore is None:
            return
        
        retriever = self._vectorstore.as_retriever(
            top_k=self.config.retrieval_top_k
        )
        
        self._qa_chain = ConversationalRetrievalChain.from_llm(
            llm=self._llm,
            retriever=retriever,
            return_source_documents=True,
            verbose=False
        )
    
    def ask(
        self,
        question: str,
        use_teacher_prompt: bool = True
    ) -> str:
        """提问并获取回答
        
        Args:
            question: 用户问题
            use_teacher_prompt: 是否使用教师人设改写问题
            
        Returns:
            AI生成的回答
        """
        if self._qa_chain is None:
            raise RuntimeError(
                "知识库未初始化。请先调用 load_documents() 加载文档。"
            )
        
        # 构建查询
        if use_teacher_prompt and self.teacher_profile:
            query = self.teacher_profile.to_rewrite_prompt(question)
        else:
            query = question
        
        # 执行查询
        result = self._qa_chain.invoke({
            "question": query,
            "chat_history": self.chat_history
        })
        
        answer = result["answer"]
        
        # 更新对话历史
        self.chat_history.append((question, answer))
        
        return answer
    
    def ask_with_sources(
        self,
        question: str,
        use_teacher_prompt: bool = True
    ) -> dict:
        """提问并返回回答及来源文档
        
        Args:
            question: 用户问题
            use_teacher_prompt: 是否使用教师人设改写问题
            
        Returns:
            包含 answer 和 source_documents 的字典
        """
        if self._qa_chain is None:
            raise RuntimeError(
                "知识库未初始化。请先调用 load_documents() 加载文档。"
            )
        
        if use_teacher_prompt and self.teacher_profile:
            query = self.teacher_profile.to_rewrite_prompt(question)
        else:
            query = question
        
        result = self._qa_chain.invoke({
            "question": query,
            "chat_history": self.chat_history
        })
        
        answer = result["answer"]
        self.chat_history.append((question, answer))
        
        return {
            "answer": answer,
            "source_documents": result.get("source_documents", [])
        }
    
    def search(self, query: str, top_k: int = 4) -> list[Document]:
        """直接搜索相关文档（不生成回答）
        
        Args:
            query: 搜索查询
            top_k: 返回结果数量
            
        Returns:
            相关文档列表
        """
        if self._vectorstore is None:
            raise RuntimeError("知识库未初始化")
        
        return self._vectorstore.search(query, top_k=top_k)
    
    def clear_history(self) -> None:
        """清空对话历史"""
        self.chat_history = []
    
    def save_vectorstore(self, path: Union[str, Path]) -> None:
        """保存向量存储到指定路径
        
        Args:
            path: 保存路径
        """
        if self._vectorstore is None:
            raise RuntimeError("向量存储未初始化")
        
        self._vectorstore.save(path)
    
    @classmethod
    def from_vectorstore(
        cls,
        vectorstore_path: Union[str, Path],
        api_key: Optional[str] = None,
        llm_provider: str = "openai",
        llm_model: str = "gpt-4o",
        teacher_profile: Optional[TeacherProfile] = None,
        **kwargs
    ) -> "SimpleRAG":
        """从已有向量存储创建实例
        
        Args:
            vectorstore_path: 向量存储路径
            api_key: API密钥
            llm_provider: LLM提供商
            llm_model: 模型名称
            teacher_profile: 教师人设
            **kwargs: 其他配置参数
            
        Returns:
            SimpleRAG 实例
        """
        instance = cls(
            api_key=api_key,
            llm_provider=llm_provider,
            llm_model=llm_model,
            teacher_profile=teacher_profile,
            vectorstore_path=str(vectorstore_path),
            **kwargs
        )
        return instance

