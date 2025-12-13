"""文本切分器"""

from typing import Literal
from langchain_text_splitters import (
    CharacterTextSplitter,
    RecursiveCharacterTextSplitter,
    TokenTextSplitter,
)
from langchain_core.documents import Document


def create_splitter(
    method: Literal["character", "recursive", "token"] = "recursive",
    chunk_size: int = 1000,
    chunk_overlap: int = 200,
    **kwargs
):
    """创建文本切分器
    
    Args:
        method: 切分方法
            - "character": 按字符数切分（简单快速）
            - "recursive": 递归切分（推荐，保持语义完整性）
            - "token": 按token数切分（与LLM token限制对齐）
        chunk_size: 切分块大小
        chunk_overlap: 切分块重叠大小
        **kwargs: 其他参数传递给具体切分器
        
    Returns:
        TextSplitter实例
        
    Example:
        >>> splitter = create_splitter("recursive", chunk_size=500)
        >>> chunks = splitter.split_documents(docs)
    """
    
    if method == "character":
        return CharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            **kwargs
        )
    
    elif method == "recursive":
        # 针对中文优化的分隔符
        separators = kwargs.pop("separators", None)
        if separators is None:
            separators = [
                "\n\n",      # 段落
                "\n",        # 换行
                "。",        # 中文句号
                "！",        # 中文感叹号
                "？",        # 中文问号
                "；",        # 中文分号
                "，",        # 中文逗号
                ".",         # 英文句号
                "!",         # 英文感叹号
                "?",         # 英文问号
                ";",         # 英文分号
                ",",         # 英文逗号
                " ",         # 空格
                "",          # 字符
            ]
        
        return RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            separators=separators,
            **kwargs
        )
    
    elif method == "token":
        return TokenTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            **kwargs
        )
    
    else:
        raise ValueError(
            f"不支持的切分方法: {method}。"
            f"支持的选项: character, recursive, token"
        )


def split_documents(
    documents: list[Document],
    chunk_size: int = 1000,
    chunk_overlap: int = 200,
    method: Literal["character", "recursive", "token"] = "recursive",
) -> list[Document]:
    """便捷函数：切分文档列表
    
    Args:
        documents: 待切分的文档列表
        chunk_size: 切分块大小
        chunk_overlap: 切分块重叠大小
        method: 切分方法
        
    Returns:
        切分后的文档列表
    """
    splitter = create_splitter(method, chunk_size, chunk_overlap)
    return splitter.split_documents(documents)

