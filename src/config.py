from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # Elasticsearch settings
    es_url: str = Field(default="http://localhost:9200", description="Elasticsearch URL")
    es_index: str = Field(default="rag_docs", description="Elasticsearch index name")

    # Embedding settings
    embedding_model: str = Field(default="all-MiniLM-L6-v2", description="Sentence transformer model name")
    embedding_dims: int = Field(default=384, description="Embedding dimensions")

    # Retrieval settings
    retrieval_k: int = Field(default=3, description="Number of documents to retrieve")
    knn_num_candidates: int = Field(default=50, description="KNN num_candidates parameter")

    # Chunking settings
    default_chunk_size: int = Field(default=500, description="Default chunk size for text splitting")
    default_chunk_overlap: int = Field(default=50, description="Default chunk overlap for text splitting")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False


# Global settings instance
settings = Settings()
