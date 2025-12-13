from importlib.metadata import version, PackageNotFoundError

try:
    __version__ = version("traia-tools")
except PackageNotFoundError:
    # Package is not installed, use a fallback version
    __version__ = "unknown"

from .tools import (
    CoingeckoUniversalQuoteTool,
    SerperDevTool,
    SerplyNewsSearchTool,
    ScrapeWebsiteTool,
    S3ReaderTool,
    S3WriterTool,
    FileReadTool,
    KeywordSearchTool,
    VectorSearchTool,
    CapabilitiesTagsSearchTool,
    ListAgentsTool,
    get_iatp_search_tools,
    DeepSeekSafeLLM
)
from .index import get_traia_tools_index