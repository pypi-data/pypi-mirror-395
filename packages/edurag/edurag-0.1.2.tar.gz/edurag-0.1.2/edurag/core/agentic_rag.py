"""Agentic RAG 实现

基于 LangGraph 的智能体 RAG 实现，
支持工具调用、多轮推理和状态持久化。
"""

from pathlib import Path
from typing import Optional, Union, Literal
import uuid

from langchain_core.documents import Document
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.tools import tool

from edurag.config import EduRAGConfig
from edurag.prompt.teacher_profile import TeacherProfile
from edurag.llm.provider import create_llm, create_embeddings
from edurag.document.loader import DocumentLoader
from edurag.document.splitter import create_splitter
from edurag.vectorstore.faiss_store import FAISSVectorStore


class AgenticRAG:
    """Agentic RAG 实现
    
    基于 LangGraph 的智能体 RAG，与 SimpleRAG 的区别：
    - Agent 可以自主决定是否需要检索
    - 支持多步推理（检索 → 分析 → 再检索 → 回答）
    - 使用状态图管理对话流程
    - 更适合复杂问题的处理
    
    Example:
        >>> from edurag import AgenticRAG, TeacherProfile
        >>> 
        >>> teacher = TeacherProfile(
        ...     name="物理王老师",
        ...     subject="高中物理",
        ...     grade_level="高三",
        ...     teaching_style="注重概念理解"
        ... )
        >>> 
        >>> rag = AgenticRAG(
        ...     api_key="sk-xxx",
        ...     teacher_profile=teacher
        ... )
        >>> rag.load_documents(["物理教材.pdf"])
        >>> 
        >>> answer = rag.ask("比较牛顿三大定律的异同点")
        >>> print(answer)
    
    Note:
        使用 AgenticRAG 需要安装 langgraph:
        pip install edurag[agentic]
    """
    
    def __init__(
        self,
        api_key: Optional[str] = None,
        llm_provider: str = "openai",
        llm_model: str = "gpt-4o",
        teacher_profile: Optional[TeacherProfile] = None,
        config: Optional[EduRAGConfig] = None,
        thread_id: Optional[str] = None,
        **kwargs
    ):
        """初始化 AgenticRAG
        
        Args:
            api_key: LLM API密钥
            llm_provider: LLM提供商 (openai/gemini/ollama)
            llm_model: 模型名称
            teacher_profile: 教师人设配置
            config: 完整配置对象
            thread_id: 对话线程ID，用于状态持久化，None则自动生成
            **kwargs: 其他配置参数
        """
        # 检查 langgraph 是否安装
        try:
            from langgraph.checkpoint.memory import MemorySaver
            from langgraph.graph import END, START, StateGraph, MessagesState
            from langgraph.prebuilt import ToolNode
        except ImportError:
            raise ImportError(
                "使用 AgenticRAG 需要安装 langgraph: "
                "pip install edurag[agentic] 或 pip install langgraph"
            )
        
        # 配置处理
        if config is not None:
            self.config = config
        else:
            config_kwargs = {
                "llm_provider": llm_provider,
                "llm_model": llm_model,
                **kwargs
            }
            if api_key:
                config_kwargs["api_key"] = api_key
            self.config = EduRAGConfig(**config_kwargs)
        
        self.teacher_profile = teacher_profile
        self.thread_id = thread_id or str(uuid.uuid4())
        
        # 初始化 Embeddings
        self._embeddings = create_embeddings(
            provider=self.config.llm_provider,
            model=self.config.embedding_model if self.config.llm_provider == "openai" else None,
            api_key=self.config.api_key,
            api_base=self.config.api_base
        )
        
        # 向量存储
        self._vectorstore: Optional[FAISSVectorStore] = None
        
        # LangGraph 组件（延迟初始化）
        self._app = None
        self._checkpointer = None
        
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
            sources: 文档路径
            chunk_size: 文档切分大小
            chunk_overlap: 切分重叠大小
            
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
        
        # 构建 Agent 工作流
        self._build_agent()
        
        # 持久化
        if self.config.vectorstore_path:
            self._vectorstore.save(self.config.vectorstore_path)
        
        return len(split_docs)
    
    def _load_vectorstore(self, path: Path) -> None:
        """加载已有的向量存储"""
        self._vectorstore = FAISSVectorStore.from_local(path, self._embeddings)
        self._build_agent()
    
    def _build_agent(self) -> None:
        """构建 LangGraph Agent 工作流"""
        if self._vectorstore is None:
            return
        
        from langgraph.checkpoint.memory import MemorySaver
        from langgraph.graph import END, START, StateGraph, MessagesState
        from langgraph.prebuilt import ToolNode
        
        # 创建检索工具
        vectorstore = self._vectorstore
        top_k = self.config.retrieval_top_k
        
        @tool
        def retrieve_context(query: str) -> str:
            """搜索知识库中的相关文档。当需要查找具体知识点、定义、公式或例题时使用此工具。
            
            Args:
                query: 搜索查询，描述你要查找的内容
                
            Returns:
                相关文档内容的拼接文本
            """
            results = vectorstore.search(query, top_k=top_k)
            if not results:
                return "未找到相关文档。"
            return "\n\n---\n\n".join([doc.page_content for doc in results])
        
        tools = [retrieve_context]
        tool_node = ToolNode(tools)
        
        # 创建 LLM（绑定工具）
        llm = create_llm(
            provider=self.config.llm_provider,
            model=self.config.llm_model,
            api_key=self.config.api_key,
            api_base=self.config.api_base,
            temperature=self.config.temperature
        )
        model_with_tools = llm.bind_tools(tools)
        
        # 保存到实例
        self._model_with_tools = model_with_tools
        
        # 决策函数：是否继续调用工具
        def should_continue(state: MessagesState) -> Literal["tools", "__end__"]:
            messages = state['messages']
            last_message = messages[-1]
            if hasattr(last_message, 'tool_calls') and last_message.tool_calls:
                return "tools"
            return END
        
        # 调用模型
        def call_model(state: MessagesState):
            messages = state['messages']
            
            # 如果有教师人设，添加系统消息
            if self.teacher_profile and len(messages) > 0:
                # 检查是否已有系统消息
                has_system = any(
                    isinstance(m, SystemMessage) for m in messages
                )
                if not has_system:
                    system_prompt = self.teacher_profile.to_system_prompt()
                    messages = [SystemMessage(content=system_prompt)] + list(messages)
            
            response = self._model_with_tools.invoke(messages)
            return {"messages": [response]}
        
        # 构建状态图
        workflow = StateGraph(MessagesState)
        
        workflow.add_node("agent", call_model)
        workflow.add_node("tools", tool_node)
        
        workflow.add_edge(START, "agent")
        workflow.add_conditional_edges("agent", should_continue)
        workflow.add_edge("tools", "agent")
        
        # 配置内存检查点
        self._checkpointer = MemorySaver()
        
        # 编译工作流
        self._app = workflow.compile(checkpointer=self._checkpointer)
    
    def ask(self, question: str) -> str:
        """提问并获取回答
        
        Args:
            question: 用户问题
            
        Returns:
            AI生成的回答
        """
        if self._app is None:
            raise RuntimeError(
                "知识库未初始化。请先调用 load_documents() 加载文档。"
            )
        
        # 构建消息
        messages = [HumanMessage(content=question)]
        
        # 执行工作流
        final_state = self._app.invoke(
            {"messages": messages},
            config={"configurable": {"thread_id": self.thread_id}}
        )
        
        # 获取最终回答
        return final_state["messages"][-1].content
    
    def ask_with_steps(self, question: str) -> dict:
        """提问并返回完整的推理过程
        
        Args:
            question: 用户问题
            
        Returns:
            包含 answer 和 steps 的字典
        """
        if self._app is None:
            raise RuntimeError(
                "知识库未初始化。请先调用 load_documents() 加载文档。"
            )
        
        messages = [HumanMessage(content=question)]
        
        final_state = self._app.invoke(
            {"messages": messages},
            config={"configurable": {"thread_id": self.thread_id}}
        )
        
        # 解析步骤
        steps = []
        for msg in final_state["messages"]:
            if hasattr(msg, 'tool_calls') and msg.tool_calls:
                for tc in msg.tool_calls:
                    steps.append({
                        "type": "tool_call",
                        "tool": tc["name"],
                        "input": tc["args"]
                    })
            elif hasattr(msg, 'type') and msg.type == "tool":
                steps.append({
                    "type": "tool_result",
                    "content": msg.content[:500] + "..." if len(msg.content) > 500 else msg.content
                })
        
        return {
            "answer": final_state["messages"][-1].content,
            "steps": steps,
            "total_messages": len(final_state["messages"])
        }
    
    def search(self, query: str, top_k: int = 4) -> list[Document]:
        """直接搜索相关文档
        
        Args:
            query: 搜索查询
            top_k: 返回结果数量
            
        Returns:
            相关文档列表
        """
        if self._vectorstore is None:
            raise RuntimeError("知识库未初始化")
        
        return self._vectorstore.search(query, top_k=top_k)
    
    def new_conversation(self, thread_id: Optional[str] = None) -> str:
        """开始新对话（生成新的 thread_id）
        
        Args:
            thread_id: 指定新的线程ID，None则自动生成
            
        Returns:
            新的 thread_id
        """
        self.thread_id = thread_id or str(uuid.uuid4())
        return self.thread_id
    
    def save_vectorstore(self, path: Union[str, Path]) -> None:
        """保存向量存储
        
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
    ) -> "AgenticRAG":
        """从已有向量存储创建实例
        
        Args:
            vectorstore_path: 向量存储路径
            api_key: API密钥
            llm_provider: LLM提供商
            llm_model: 模型名称
            teacher_profile: 教师人设
            **kwargs: 其他配置参数
            
        Returns:
            AgenticRAG 实例
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

