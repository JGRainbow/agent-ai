# Scripts

Utility scripts for managing the Agent-AI project.

## Available Scripts

### `create_index.py`
Creates the Elasticsearch index with proper vector search mapping.

**Usage:**
```bash
make create-index
# or
python scripts/create_index.py
```

### `delete_index.py`
Deletes the Elasticsearch index (useful for testing/resetting).

**Usage:**
```bash
make delete-index
# or
python scripts/delete_index.py
```

### `check_elasticsearch.py`
Checks if Elasticsearch is running and shows index status.

**Usage:**
```bash
make check-elasticsearch
# or
python scripts/check_elasticsearch.py
```

### `list_indices.py`
Lists all Elasticsearch indices with document counts and sizes.

**Usage:**
```bash
make list-indices
# or
python scripts/list_indices.py
```

## Makefile Commands

All scripts can be run via Makefile commands:

- `make create-index` - Create the Elasticsearch index
- `make delete-index` - Delete the Elasticsearch index
- `make check-elasticsearch` - Check Elasticsearch status
- `make list-indices` - List all indices
