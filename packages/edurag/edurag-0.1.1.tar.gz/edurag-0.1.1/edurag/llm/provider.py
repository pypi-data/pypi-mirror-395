"""LLM Provider 工厂模块

支持多种LLM提供商的统一接口封装。
"""

from typing import Literal, Optional, Any
from langchain_core.language_models import BaseChatModel
from langchain_core.embeddings import Embeddings


def create_llm(
    provider: Literal["openai", "gemini", "ollama"],
    model: str,
    api_key: Optional[str] = None,
    api_base: Optional[str] = None,
    temperature: float = 0.7,
    **kwargs: Any
) -> BaseChatModel:
    """创建LLM实例
    
    Args:
        provider: LLM提供商 (openai/gemini/ollama)
        model: 模型名称
        api_key: API密钥
        api_base: 自定义API端点
        temperature: 生成温度
        **kwargs: 其他模型参数
        
    Returns:
        BaseChatModel: LangChain兼容的LLM实例
        
    Raises:
        ValueError: 不支持的provider
        ImportError: 缺少对应provider的依赖包
        
    Example:
        >>> llm = create_llm("openai", "gpt-4o", api_key="sk-xxx")
        >>> llm = create_llm("ollama", "llama3")  # 本地部署无需api_key
    """
    
    if provider == "openai":
        from langchain_openai import ChatOpenAI
        
        init_kwargs = {
            "model": model,
            "temperature": temperature,
            **kwargs
        }
        if api_key:
            init_kwargs["api_key"] = api_key
        if api_base:
            init_kwargs["base_url"] = api_base
            
        return ChatOpenAI(**init_kwargs)
    
    elif provider == "gemini":
        try:
            from langchain_google_genai import ChatGoogleGenerativeAI
        except ImportError:
            raise ImportError(
                "使用 Gemini 需要安装 langchain-google-genai: "
                "pip install edurag[gemini]"
            )
        
        return ChatGoogleGenerativeAI(
            model=model,
            google_api_key=api_key,
            temperature=temperature,
            **kwargs
        )
    
    elif provider == "ollama":
        try:
            from langchain_ollama import ChatOllama
        except ImportError:
            raise ImportError(
                "使用 Ollama 需要安装 langchain-ollama: "
                "pip install edurag[ollama]"
            )
        
        init_kwargs = {
            "model": model,
            "temperature": temperature,
            **kwargs
        }
        if api_base:
            init_kwargs["base_url"] = api_base
            
        return ChatOllama(**init_kwargs)
    
    else:
        raise ValueError(
            f"不支持的 LLM provider: {provider}。"
            f"支持的选项: openai, gemini, ollama"
        )


def create_embeddings(
    provider: Literal["openai", "gemini", "ollama"] = "openai",
    model: Optional[str] = None,
    api_key: Optional[str] = None,
    api_base: Optional[str] = None,
    **kwargs: Any
) -> Embeddings:
    """创建Embeddings实例
    
    Args:
        provider: 提供商 (openai/gemini/ollama)
        model: Embedding模型名称，None则使用默认值
        api_key: API密钥
        api_base: 自定义API端点
        **kwargs: 其他参数
        
    Returns:
        Embeddings: LangChain兼容的Embeddings实例
    """
    
    if provider == "openai":
        from langchain_openai import OpenAIEmbeddings
        
        init_kwargs = {**kwargs}
        if model:
            init_kwargs["model"] = model
        if api_key:
            init_kwargs["api_key"] = api_key
        if api_base:
            init_kwargs["base_url"] = api_base
            
        return OpenAIEmbeddings(**init_kwargs)
    
    elif provider == "gemini":
        try:
            from langchain_google_genai import GoogleGenerativeAIEmbeddings
        except ImportError:
            raise ImportError(
                "使用 Gemini Embeddings 需要安装: pip install edurag[gemini]"
            )
        
        return GoogleGenerativeAIEmbeddings(
            model=model or "models/embedding-001",
            google_api_key=api_key,
            **kwargs
        )
    
    elif provider == "ollama":
        try:
            from langchain_ollama import OllamaEmbeddings
        except ImportError:
            raise ImportError(
                "使用 Ollama Embeddings 需要安装: pip install edurag[ollama]"
            )
        
        init_kwargs = {"model": model or "nomic-embed-text", **kwargs}
        if api_base:
            init_kwargs["base_url"] = api_base
            
        return OllamaEmbeddings(**init_kwargs)
    
    else:
        raise ValueError(f"不支持的 Embeddings provider: {provider}")

