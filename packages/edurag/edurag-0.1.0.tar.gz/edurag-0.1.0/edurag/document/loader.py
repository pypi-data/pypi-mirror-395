"""文档加载器

支持多种文档格式的统一加载接口。
"""

from pathlib import Path
from typing import Union, Optional
from langchain_core.documents import Document


class DocumentLoader:
    """多格式文档加载器
    
    支持 PDF、DOCX、DOC、TXT 等常见文档格式。
    
    Example:
        >>> loader = DocumentLoader()
        >>> docs = loader.load("教材.pdf")
        >>> docs = loader.load_directory("./documents", extensions=[".pdf", ".docx"])
    """
    
    # 支持的文件格式及其加载器
    SUPPORTED_EXTENSIONS = {".pdf", ".docx", ".doc", ".txt", ".md"}
    
    @classmethod
    def load(cls, file_path: Union[str, Path]) -> list[Document]:
        """加载单个文档
        
        Args:
            file_path: 文档路径
            
        Returns:
            Document列表
            
        Raises:
            FileNotFoundError: 文件不存在
            ValueError: 不支持的文件格式
        """
        path = Path(file_path)
        
        if not path.exists():
            raise FileNotFoundError(f"文件不存在: {path}")
        
        ext = path.suffix.lower()
        
        if ext not in cls.SUPPORTED_EXTENSIONS:
            raise ValueError(
                f"不支持的文件格式: {ext}。"
                f"支持的格式: {', '.join(cls.SUPPORTED_EXTENSIONS)}"
            )
        
        return cls._load_by_extension(path, ext)
    
    @classmethod
    def _load_by_extension(cls, path: Path, ext: str) -> list[Document]:
        """根据扩展名选择加载器"""
        
        if ext == ".pdf":
            from langchain_community.document_loaders import PyPDFLoader
            loader = PyPDFLoader(str(path))
            return loader.load()
        
        elif ext in (".docx", ".doc"):
            try:
                from langchain_community.document_loaders import Docx2txtLoader
                loader = Docx2txtLoader(str(path))
                return loader.load()
            except ImportError:
                raise ImportError(
                    "加载 Word 文档需要安装 docx2txt: pip install docx2txt"
                )
        
        elif ext == ".txt":
            from langchain_community.document_loaders import TextLoader
            loader = TextLoader(str(path), encoding="utf-8")
            return loader.load()
        
        elif ext == ".md":
            from langchain_community.document_loaders import TextLoader
            loader = TextLoader(str(path), encoding="utf-8")
            return loader.load()
        
        else:
            raise ValueError(f"未知的文件扩展名: {ext}")
    
    @classmethod
    def load_multiple(cls, file_paths: list[Union[str, Path]]) -> list[Document]:
        """批量加载多个文档
        
        Args:
            file_paths: 文档路径列表
            
        Returns:
            所有文档的Document列表
        """
        all_docs = []
        for path in file_paths:
            docs = cls.load(path)
            all_docs.extend(docs)
        return all_docs
    
    @classmethod
    def load_directory(
        cls,
        dir_path: Union[str, Path],
        extensions: Optional[list[str]] = None,
        recursive: bool = True
    ) -> list[Document]:
        """加载目录下的所有文档
        
        Args:
            dir_path: 目录路径
            extensions: 要加载的文件扩展名列表，None则加载所有支持的格式
            recursive: 是否递归加载子目录
            
        Returns:
            所有文档的Document列表
        """
        path = Path(dir_path)
        
        if not path.exists():
            raise FileNotFoundError(f"目录不存在: {path}")
        
        if not path.is_dir():
            raise ValueError(f"路径不是目录: {path}")
        
        extensions = extensions or list(cls.SUPPORTED_EXTENSIONS)
        # 标准化扩展名格式
        extensions = [ext if ext.startswith(".") else f".{ext}" for ext in extensions]
        
        all_docs = []
        pattern = "**/*" if recursive else "*"
        
        for ext in extensions:
            for file_path in path.glob(f"{pattern}{ext}"):
                if file_path.is_file():
                    try:
                        docs = cls.load(file_path)
                        all_docs.extend(docs)
                    except Exception as e:
                        # 记录错误但继续处理其他文件
                        print(f"警告: 加载 {file_path} 失败: {e}")
        
        return all_docs

