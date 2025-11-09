# Quick Setup - Single PDF

Get a single PDF working in 5 minutes!

## Step 1: Install PDF library

```bash
pip install pypdf
```

Or if using the Makefile:
```bash
make install
```

## Step 2: Start Elasticsearch

```bash
make elasticsearch
```

Wait for it to be ready (about 30 seconds).

## Step 3: Create the index

```bash
make create-index
```

## Step 4: Index your PDF

Place your PDF anywhere (e.g., `data/raw/my_document.pdf`) and run:

```bash
python scripts/index_single_pdf.py data/raw/my_document.pdf
```

Or using Makefile:
```bash
make index-pdf PDF=data/raw/my_document.pdf
```

## Step 5: Test it!

Start the API:
```bash
uvicorn src.api.main:app --reload
```

Then test with a query:
```bash
curl -X POST "http://localhost:8000/query" \
  -H "Content-Type: application/json" \
  -d '{"query": "How do I change my name after marriage?"}'
```

Or visit: http://localhost:8000/docs and use the Swagger UI.

## That's it! 🎉

Your PDF is now searchable via vector search. The system will:
1. Extract text from your PDF
2. Chunk it into searchable pieces
3. Create embeddings
4. Store in Elasticsearch
5. Answer questions based on the content

## Next Steps (Optional)

- Add more PDFs by running `index_single_pdf.py` again
- Replace the stub answer in `reason_node` with a real LLM call
- Test with different questions
