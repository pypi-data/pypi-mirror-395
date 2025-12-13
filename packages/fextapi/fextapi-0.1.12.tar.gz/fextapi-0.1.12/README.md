# fextapi

**File-system based routing for FastAPI** - Build APIs like Next.js App Router

[![Python Version](https://img.shields.io/badge/python-3.13+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## 🚀 Features

- **Zero Configuration** - Automatically map folder structure to API routes
- **Developer Friendly** - Use standard FastAPI syntax with no learning curve
- **Convention over Configuration** - Organized project structure out of the box
- **CLI Tools** - Initialize and run projects with simple commands
- **Type Safe** - Full Python type hints and IDE support

## 📦 Installation

```bash
# Using uv (recommended)
uv add fextapi

# Using pip
pip install fextapi
```

## 🎯 Quick Start

```bash
# Initialize a new project
fextapi init

# Start development server
fextapi run

# Visit http://127.0.0.1:8000/docs
```

## 📁 Project Structure

```
my-api-project/
├── app/
│   ├── main.py               # FastAPI application entry point
│   ├── components/           # Business logic and reusable components
│   ├── api/
│   │   └── route.py          # GET /api
│   ├── products/
│   │   ├── route.py          # GET /products
│   │   ├── [productid]/
│   │   │   └── route.py      # GET /products/{productid}
│   │   └── stats/
│   │       └── route.py      # GET /products/stats
└── pyproject.toml
```

## 📝 Usage Examples

### main.py

```python
from fastapi import FastAPI
from fextapi import init

app = FastAPI()

# Automatically register all routes
init(app)
```

### products/route.py

```python
from fastapi import APIRouter

router = APIRouter()

@router.get("/", tags=["products"])
async def list_products():
    return [
        {"id": 1, "name": "Product A"},
        {"id": 2, "name": "Product B"}
    ]
```

### products/[productid]/route.py

```python
from fastapi import APIRouter, HTTPException

router = APIRouter()

@router.get("/", tags=["products"])
async def get_product_detail(productid: str):
    if productid == "999":
        raise HTTPException(status_code=404, detail="Product not found")
    return {"id": productid, "name": f"Product {productid}"}
```

## 🎨 Routing Rules

### Static Routes
- `app/api/route.py` → `/api`
- `app/products/route.py` → `/products`
- `app/products/stats/route.py` → `/products/stats`

### Dynamic Routes
- `app/products/[productid]/route.py` → `/products/{productid}`
- `app/users/[userid]/orders/[orderid]/route.py` → `/users/{userid}/orders/{orderid}`

### Route Priority
**Static routes are matched before dynamic routes**

When accessing `/products/stats`:
- ✅ Matches `/products/stats/route.py` (static)
- ❌ Skips `/products/[productid]/route.py` (dynamic)

## 🛠️ CLI Commands

```bash
# Initialize new project
fextapi init

# Start development server (default: host=127.0.0.1, port=8000)
fextapi run

# Start server with custom host/port
fextapi run --host 0.0.0.0 --port 3000

# Disable auto-reload
fextapi run --no-reload

# Show help
fextapi help

# Show version
fextapi version
```

## 🧪 Requirements

- Python 3.13+
- FastAPI 0.100.0+
- Uvicorn 0.20.0+

## 📄 License

MIT License - see [LICENSE](LICENSE) for details

## 🤝 Contributing

Contributions are welcome! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## 🔗 Links

- [GitHub Repository](https://github.com/johnnydddd/fextapi)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Issue Tracker](https://github.com/johnnydddd/fextapi/issues)

## ⭐ Acknowledgments

Inspired by [Next.js App Router](https://nextjs.org/docs/app) and built with [FastAPI](https://fastapi.tiangolo.com/).
