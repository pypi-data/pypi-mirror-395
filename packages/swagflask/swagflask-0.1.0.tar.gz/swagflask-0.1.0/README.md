# SwagFlask 🎉

**Swagger UI for Flask** - Bring FastAPI's beloved `/docs` experience to Flask!

SwagFlask automatically configures Swagger UI for your Flask applications, making API documentation and testing as easy as typing `/docs` in your browser.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/)
[![Flask](https://img.shields.io/badge/flask-2.0+-green.svg)](https://flask.palletsprojects.com/)

## ✨ Features

- 🚀 **FastAPI-like `/docs` endpoint** for Flask
- 📝 **Automatic OpenAPI/Swagger spec generation** from your Flask routes
- 🎨 **Beautiful Swagger UI** interface for testing APIs
- 🔧 **Simple decorator-based** API documentation
- 📦 **Zero config required** - works out of the box
- 🎯 **Type-safe** with full type hints support
- 🔌 **Easy integration** with existing Flask apps

## 📦 Installation

```bash
pip install swagflask
```

## 🚀 Quick Start

```python
from flask import Flask, jsonify
from swagflask import SwaggerUI

app = Flask(__name__)

# Initialize SwaggerUI
swagger = SwaggerUI(app, title="My API", version="1.0.0")

@app.route('/users', methods=['GET'])
@swagger.doc({
    'summary': 'Get all users',
    'responses': {
        '200': {'description': 'List of users'}
    }
})
def get_users():
    return jsonify([{'id': 1, 'name': 'John'}, {'id': 2, 'name': 'Jane'}])

if __name__ == '__main__':
    app.run(debug=True)
```

**That's it!** Now visit `http://localhost:5000/docs` to see your interactive API documentation! 🎊

## 📖 Usage

### Basic Setup

```python
from flask import Flask
from swagflask import SwaggerUI

app = Flask(__name__)
swagger = SwaggerUI(app)
```

### Custom Configuration

```python
swagger = SwaggerUI(
    app,
    title="My Awesome API",           # API title
    version="1.0.0",                   # API version
    description="API Description",     # API description
    docs_url="/docs",                  # Swagger UI URL (default: /docs)
    openapi_url="/openapi.json"        # OpenAPI spec URL (default: /openapi.json)
)
```

### Documenting Endpoints

#### With the `@swagger.doc()` decorator:

```python
@app.route('/users/<int:user_id>', methods=['GET'])
@swagger.doc({
    'summary': 'Get user by ID',
    'description': 'Returns a single user by their ID',
    'parameters': [{
        'name': 'user_id',
        'in': 'path',
        'required': True,
        'schema': {'type': 'integer'},
        'description': 'The ID of the user to retrieve'
    }],
    'responses': {
        '200': {
            'description': 'User found',
            'content': {
                'application/json': {
                    'schema': {
                        'type': 'object',
                        'properties': {
                            'id': {'type': 'integer'},
                            'name': {'type': 'string'},
                            'email': {'type': 'string'}
                        }
                    }
                }
            }
        },
        '404': {'description': 'User not found'}
    }
})
def get_user(user_id):
    # Your code here
    return jsonify({'id': user_id, 'name': 'John Doe'})
```

#### POST endpoints with request body:

```python
@app.route('/users', methods=['POST'])
@swagger.doc({
    'summary': 'Create a new user',
    'requestBody': {
        'required': True,
        'content': {
            'application/json': {
                'schema': {
                    'type': 'object',
                    'required': ['name', 'email'],
                    'properties': {
                        'name': {'type': 'string', 'example': 'John Doe'},
                        'email': {'type': 'string', 'format': 'email'}
                    }
                }
            }
        }
    },
    'responses': {
        '201': {'description': 'User created successfully'},
        '400': {'description': 'Invalid input'}
    }
})
def create_user():
    data = request.get_json()
    # Your code here
    return jsonify(data), 201
```

#### Auto-documentation (without decorator):

SwagFlask can automatically generate basic documentation from your function signatures and docstrings:

```python
@app.route('/products', methods=['GET'])
def get_products():
    """
    Get all products.
    This endpoint returns a list of all available products.
    """
    return jsonify([{'id': 1, 'name': 'Laptop'}])
```

## 📋 Examples

Check out the `examples/` directory for complete working examples:

- **`basic_app.py`** - Simple API with basic documentation
- **`advanced_app.py`** - Advanced usage with custom configuration

To run the examples:

```bash
# Basic example
python examples/basic_app.py

# Advanced example
python examples/advanced_app.py
```

Then visit:
- Basic app: http://localhost:5000/docs
- Advanced app: http://localhost:5001/api/docs

## 🎯 Why SwagFlask?

If you've used FastAPI, you know how amazing it is to have `/docs` built-in. But sometimes you need to use Flask for various reasons (existing codebase, specific requirements, etc.). SwagFlask brings that same documentation experience to Flask!

### Comparison

**FastAPI:**
```python
from fastapi import FastAPI
app = FastAPI()

@app.get("/users")
def get_users():
    return [{"id": 1, "name": "John"}]
# Visit /docs - it just works! ✨
```

**Flask with SwagFlask:**
```python
from flask import Flask
from swagflask import SwaggerUI

app = Flask(__name__)
swagger = SwaggerUI(app)

@app.route('/users')
def get_users():
    return [{"id": 1, "name": "John"}]
# Visit /docs - it just works! ✨
```

## 🛠️ Development

### Setup Development Environment

```bash
# Clone the repository
git clone https://github.com/rithwiksb/swagflask.git
cd swagflask

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install in development mode
pip install -e .

# Install development dependencies
pip install -e ".[dev]"
```

### Running Tests

```bash
pytest
```

## 📝 Publishing to PyPI

### Prerequisites

1. Create accounts on [PyPI](https://pypi.org/) and [TestPyPI](https://test.pypi.org/)
2. Install build tools:

```bash
pip install build twine
```

### Build the Package

```bash
# Clean previous builds
rm -rf build/ dist/ *.egg-info

# Build the package
python -m build
```

This creates two files in `dist/`:
- `swagflask-0.1.0.tar.gz` (source distribution)
- `swagflask-0.1.0-py3-none-any.whl` (wheel distribution)

### Test on TestPyPI (Recommended)

```bash
# Upload to TestPyPI
python -m twine upload --repository testpypi dist/*

# Install from TestPyPI to test
pip install --index-url https://test.pypi.org/simple/ swagflask
```

### Publish to PyPI

```bash
# Upload to PyPI
python -m twine upload dist/*
```

### Post-Publishing

After publishing, you can install your package with:

```bash
pip install swagflask
```

## 🤝 Contributing

Contributions are welcome! Here are some ways you can contribute:

- 🐛 Report bugs
- 💡 Suggest new features
- 📝 Improve documentation
- 🔧 Submit pull requests

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Inspired by [FastAPI](https://fastapi.tiangolo.com/)'s excellent API documentation
- Built with [Flask](https://flask.palletsprojects.com/)
- Uses [Swagger UI](https://swagger.io/tools/swagger-ui/) for documentation interface

## 🔗 Links

- **Documentation:** [GitHub Repository](https://github.com/rithwiksb/swagflask)
- **PyPI:** [https://pypi.org/project/swagflask/](https://pypi.org/project/swagflask/)
- **Issues:** [GitHub Issues](https://github.com/rithwiksb/swagflask/issues)

---

Made with ❤️ for Flask developers who miss FastAPI's `/docs`
