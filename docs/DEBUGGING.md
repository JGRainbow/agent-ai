# Debugging Setup

## VS Code (Recommended)

### Quick Start

1. **Open the project in VS Code**
   ```bash
   code .
   ```

2. **Select Python Interpreter**
   - Press `Cmd+Shift+P` (Mac) or `Ctrl+Shift+P` (Windows/Linux)
   - Type "Python: Select Interpreter"
   - Choose your virtual environment: `./venv/bin/python`

3. **Start Debugging**
   - Press `F5` or go to Run → Start Debugging
   - Select "Python: FastAPI" from the dropdown
   - The API will start at http://localhost:8000
   - Set breakpoints by clicking in the gutter (left of line numbers)

### Debug Configurations

The `.vscode/launch.json` file includes several configurations:

- **Python: FastAPI** - Main debug config with auto-reload
- **Python: FastAPI (No Reload)** - Debug without auto-reload (faster)
- **Python: Current File** - Debug the currently open Python file
- **Python: Pytest** - Debug your tests

### Setting Breakpoints

1. Click in the gutter (left of line numbers) to set a breakpoint
2. Red dot appears when breakpoint is set
3. When code hits the breakpoint, execution pauses
4. Use the debug toolbar to:
   - **Continue (F5)** - Resume execution
   - **Step Over (F10)** - Execute current line
   - **Step Into (F11)** - Step into function calls
   - **Step Out (Shift+F11)** - Step out of current function
   - **Restart (Shift+Cmd+F5)** - Restart debugging
   - **Stop (Shift+F5)** - Stop debugging

### Debugging the API

1. Set a breakpoint in `src/api/main.py` in the `query` function
2. Start debugging (F5)
3. Make a request to the API (via Swagger UI or curl)
4. Execution will pause at your breakpoint
5. Inspect variables in the "Variables" panel
6. Use the "Debug Console" to evaluate expressions

### Example: Debugging a Query

1. Set breakpoint in `src/agent/graph.py` in `retrieve_node` or `reason_node`
2. Start debugging
3. Send a query:
   ```bash
   curl -X POST "http://localhost:8000/query" \
     -H "Content-Type: application/json" \
     -d '{"query": "How do I change my name?"}'
   ```
4. Execution pauses at your breakpoint
5. Inspect `state`, `retrieved_chunks`, etc.

## PyCharm

### Setup

1. **Open Project**
   - File → Open → Select project directory

2. **Configure Python Interpreter**
   - File → Settings → Project → Python Interpreter
   - Select your virtual environment

3. **Create Run Configuration**
   - Run → Edit Configurations
   - Click "+" → Python
   - Name: "FastAPI"
   - Script path: Select `uvicorn` from your venv
   - Parameters: `src.api.main:app --reload`
   - Working directory: Project root

4. **Debug**
   - Set breakpoints
   - Right-click the configuration → Debug
   - Or click the bug icon

## Command Line Debugging

### Using pdb (Python Debugger)

Add this line where you want to break:
```python
import pdb; pdb.set_trace()
```

Or use breakpoint() (Python 3.7+):
```python
breakpoint()
```

### Using ipdb (Better pdb)

```bash
pip install ipdb
```

Then in your code:
```python
import ipdb; ipdb.set_trace()
```

## Debugging Tips

1. **Check Elasticsearch Connection**
   - Set breakpoint in `retrieve_node`
   - Inspect `repository.search()` call
   - Check if chunks are being retrieved

2. **Inspect Retrieved Chunks**
   - Break in `reason_node`
   - Check `state["retrieved_chunks"]`
   - Verify chunk structure

3. **Debug Embeddings**
   - Set breakpoint in `embed_texts`
   - Check vector dimensions
   - Verify embedding quality

4. **API Request/Response**
   - Break in `query` endpoint
   - Inspect `request.query`
   - Check `result` before returning

## Common Issues

### Breakpoints Not Hitting

- Make sure you're using the correct Python interpreter
- Check that `justMyCode` is set to `false` in launch.json
- Verify the code path is actually being executed

### Module Not Found

- Ensure `PYTHONPATH` includes workspace folder
- Check `.vscode/settings.json` has correct paths
- Verify virtual environment is activated

### Port Already in Use

- Stop any existing uvicorn processes
- Change port in launch.json: `--port 8001`
