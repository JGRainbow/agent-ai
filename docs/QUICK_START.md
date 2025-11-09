# Quick Start Guide

## Getting Started with Document Acquisition

### Step 1: Download Your First Document

1. **Visit GOV.UK Name Change Page**
   - Go to: https://www.gov.uk/change-name-marriage-divorce
   - Right-click → "Save Page As" → Save as HTML or PDF
   - Save to: `data/raw/govuk/name_change_marriage.html`

2. **Extract Text** (Manual for now)
   - Open the saved file
   - Copy the main content text
   - Create: `data/processed/govuk_name_change_marriage.txt`
   - Paste the text

### Step 2: Index the Document

```bash
# Make sure Elasticsearch is running
make elasticsearch

# Create the index
make create-index

# Index your document
make index-documents
```

### Step 3: Test the System

```bash
# Start the API
uvicorn src.api.main:app --reload

# In another terminal, test a query
curl -X POST "http://localhost:8000/query" \
  -H "Content-Type: application/json" \
  -d '{"query": "How do I change my name after marriage?"}'
```

## Next Steps

1. **Download More Documents** (see `docs/DOCUMENT_SOURCES.md`)
   - DVLA driving licence update
   - Passport Office guidance
   - Marriage certificate information

2. **Add LLM Integration**
   - Get OpenAI API key
   - Update `reason_node` in `src/agent/graph.py`
   - Replace stub answer with real LLM call

3. **Improve Retrieval**
   - Test with various queries
   - Adjust chunk size if needed
   - Add more documents for better coverage

## Recommended Document Download Order

1. ✅ GOV.UK name change overview (start here)
2. Marriage certificate requirements
3. DVLA driving licence update
4. Passport Office update
5. Electoral roll update
6. HMRC update

See `docs/DOCUMENT_SOURCES.md` for all URLs and details.
