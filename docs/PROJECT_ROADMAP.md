# Project Roadmap: UK Name Change RAG Agent

## Current Status ✅
- [x] Project structure and architecture
- [x] Repository pattern for database abstraction
- [x] LangGraph orchestration framework
- [x] Elasticsearch vector search setup
- [x] FastAPI endpoint
- [x] Test infrastructure (unit + integration)
- [x] Docker setup for Elasticsearch

## Phase 1: Document Acquisition & Indexing (Next Steps)

### 1.1 Document Collection
- [ ] Create `data/raw/` directory structure
- [ ] Download GOV.UK name change pages
- [ ] Download DVLA guidance
- [ ] Download Passport Office guidance
- [ ] Download marriage certificate information
- [ ] Create document metadata tracking

### 1.2 Document Processing Pipeline
- [ ] Create `scripts/download_documents.py` for web scraping
- [ ] Create `scripts/process_documents.py` to convert PDFs/HTML to text
- [ ] Create `scripts/index_documents.py` to bulk index documents
- [ ] Add document source tracking (URL, date downloaded, version)

### 1.3 Indexing Script
- [ ] Enhance `scripts/index_documents.py` to:
  - Read from `data/processed/`
  - Chunk documents appropriately
  - Index with proper metadata (source, doc_name, date)
  - Handle updates/re-indexing

## Phase 2: LLM Integration

### 2.1 Add LLM Provider
- [ ] Choose LLM provider (OpenAI, Anthropic, local model)
- [ ] Add to `requirements.txt`
- [ ] Create `src/llm/` module with:
  - `provider.py` - Abstract LLM interface
  - `openai_provider.py` - OpenAI implementation
  - `anthropic_provider.py` - Anthropic implementation (optional)

### 2.2 Update Graph Nodes
- [ ] Replace stub in `reason_node` with actual LLM call
- [ ] Add prompt engineering for:
  - Answer synthesis from retrieved chunks
  - Confidence scoring
  - Source citation
- [ ] Add streaming support (optional)

### 2.3 Configuration
- [ ] Add LLM settings to `src/config.py`
- [ ] Add API key management (environment variables)
- [ ] Add model selection (GPT-4, Claude, etc.)

## Phase 3: Enhanced Retrieval

### 3.1 Hybrid Search
- [ ] Add keyword/BM25 search alongside vector search
- [ ] Implement reranking (e.g., using cross-encoder)
- [ ] Combine results intelligently

### 3.2 Query Understanding
- [ ] Add query expansion
- [ ] Add query classification (e.g., "DVLA question" vs "Passport question")
- [ ] Route to specialized retrieval if needed

### 3.3 Metadata Filtering
- [ ] Filter by document type (DVLA, Passport, etc.)
- [ ] Filter by date/relevance
- [ ] Add faceted search

## Phase 4: User Experience

### 4.1 API Enhancements
- [ ] Add conversation history support
- [ ] Add follow-up question handling
- [ ] Add clarification requests
- [ ] Add rate limiting

### 4.2 Response Quality
- [ ] Add answer validation
- [ ] Improve source ranking
- [ ] Add "I don't know" responses when confidence is low
- [ ] Add suggested follow-up questions

### 4.3 Frontend (Optional)
- [ ] Simple web interface
- [ ] Chat interface
- [ ] Source highlighting
- [ ] Document links

## Phase 5: Evaluation & Improvement

### 5.1 Evaluation Dataset
- [ ] Create test questions (20-50 questions)
- [ ] Create expected answers
- [ ] Create evaluation script
- [ ] Track metrics:
  - Answer accuracy
  - Source relevance
  - Response time
  - User satisfaction

### 5.2 Continuous Improvement
- [ ] Add feedback mechanism
- [ ] Log queries and responses
- [ ] Identify common failure modes
- [ ] Iterate on prompts and retrieval

## Phase 6: Production Readiness

### 6.1 Monitoring
- [ ] Add logging (structured logging)
- [ ] Add metrics (Prometheus/Grafana)
- [ ] Add error tracking (Sentry)
- [ ] Add health checks

### 6.2 Security
- [ ] Add authentication/authorization
- [ ] Add rate limiting
- [ ] Add input sanitization
- [ ] Add API key rotation

### 6.3 Deployment
- [ ] Dockerize application
- [ ] Create docker-compose for full stack
- [ ] Add CI/CD pipeline
- [ ] Add staging environment

## Quick Start: Next Immediate Steps

1. **Create data directory structure**
   ```bash
   mkdir -p data/raw/{govuk,dvla,passport,marriage}
   mkdir -p data/processed
   ```

2. **Download first document manually**
   - Start with GOV.UK name change page
   - Save as PDF or HTML
   - Place in `data/raw/govuk/`

3. **Create document processing script**
   - Extract text from PDF/HTML
   - Clean and normalize
   - Save to `data/processed/`

4. **Index first document**
   - Use existing chunking and indexing
   - Test retrieval with sample queries

5. **Add LLM integration**
   - Start with OpenAI GPT-4
   - Replace stub in `reason_node`
   - Test end-to-end

## Success Metrics

- **Accuracy**: >85% of answers are correct
- **Relevance**: >90% of sources are relevant
- **Coverage**: Answers available for all major name change scenarios
- **Response Time**: <3 seconds for typical queries
- **User Satisfaction**: Positive feedback on answer quality
