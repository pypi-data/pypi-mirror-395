"""
Core Swagger UI integration for Flask applications.
"""

import json
from flask import Blueprint, render_template_string, jsonify, current_app
from functools import wraps
import inspect
from typing import Dict, List, Any, Optional, Callable


class SwaggerUI:
    """
    Automatically configure Swagger UI for Flask applications.
    
    Usage:
        from flask import Flask
        from swagflask import SwaggerUI
        
        app = Flask(__name__)
        swagger = SwaggerUI(app, title="My API")
        
        @app.route('/users', methods=['GET'])
        @swagger.doc({
            'summary': 'Get all users',
            'responses': {
                '200': {'description': 'List of users'}
            }
        })
        def get_users():
            return {'users': []}
    """
    
    def __init__(
        self,
        app=None,
        title: str = "API Documentation",
        version: str = "1.0.0",
        description: str = "API Documentation",
        docs_url: str = "/docs",
        openapi_url: str = "/openapi.json",
    ):
        """
        Initialize SwaggerUI.
        
        Args:
            app: Flask application instance
            title: API title
            version: API version
            description: API description
            docs_url: URL path for Swagger UI (default: /docs)
            openapi_url: URL path for OpenAPI JSON spec (default: /openapi.json)
        """
        self.title = title
        self.version = version
        self.description = description
        self.docs_url = docs_url
        self.openapi_url = openapi_url
        self.routes: Dict[str, Dict[str, Any]] = {}
        
        if app is not None:
            self.init_app(app)
    
    def init_app(self, app):
        """Initialize the Flask application."""
        self.app = app
        
        # Create blueprint for Swagger UI
        swagger_bp = Blueprint(
            'swagger_ui',
            __name__,
            url_prefix=''
        )
        
        @swagger_bp.route(self.docs_url)
        def swagger_ui():
            """Render Swagger UI."""
            return render_template_string(self._get_swagger_ui_html())
        
        @swagger_bp.route(self.openapi_url)
        def openapi_spec():
            """Return OpenAPI specification."""
            return jsonify(self._generate_openapi_spec())
        
        app.register_blueprint(swagger_bp)
        
        # Store reference to SwaggerUI instance in app
        app.extensions = getattr(app, 'extensions', {})
        app.extensions['swagflask'] = self
    
    def doc(self, spec: Dict[str, Any]) -> Callable:
        """
        Decorator to add OpenAPI documentation to a Flask route.
        
        Args:
            spec: OpenAPI operation object
            
        Example:
            @app.route('/users/<int:user_id>', methods=['GET'])
            @swagger.doc({
                'summary': 'Get user by ID',
                'parameters': [{
                    'name': 'user_id',
                    'in': 'path',
                    'required': True,
                    'schema': {'type': 'integer'}
                }],
                'responses': {
                    '200': {'description': 'User found'},
                    '404': {'description': 'User not found'}
                }
            })
            def get_user(user_id):
                return {'id': user_id}
        """
        def decorator(func: Callable) -> Callable:
            # Store the spec with the function
            if not hasattr(func, '_swagger_spec'):
                func._swagger_spec = spec
            return func
        return decorator
    
    @staticmethod
    def schema(schema_type: str = "object", properties: Dict[str, Any] = None, 
               required: List[str] = None, example: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Helper method to create a JSON schema with examples for request/response bodies.
        
        Args:
            schema_type: Type of schema (default: "object")
            properties: Dictionary of property definitions with types and examples
            required: List of required field names
            example: Complete example object to show in Swagger UI
            
        Example:
            schema = SwaggerUI.schema(
                properties={
                    'name': {'type': 'string', 'example': 'John Doe'},
                    'email': {'type': 'string', 'format': 'email', 'example': 'john@example.com'},
                    'age': {'type': 'integer', 'example': 30}
                },
                required=['name', 'email'],
                example={'name': 'John Doe', 'email': 'john@example.com', 'age': 30}
            )
        """
        schema_def: Dict[str, Any] = {'type': schema_type}
        
        if properties:
            schema_def['properties'] = properties
        
        if required:
            schema_def['required'] = required
        
        if example:
            schema_def['example'] = example
        
        return schema_def
    
    def _generate_openapi_spec(self) -> Dict[str, Any]:
        """Generate OpenAPI 3.0 specification from Flask routes."""
        paths = {}
        
        # Iterate through all registered routes in the Flask app
        for rule in self.app.url_map.iter_rules():
            # Skip static and internal routes
            if rule.endpoint == 'static' or rule.endpoint.startswith('swagger_ui'):
                continue
            
            # Get the view function
            view_func = self.app.view_functions.get(rule.endpoint)
            if view_func is None:
                continue
            
            # Convert Flask route to OpenAPI path
            path = self._flask_route_to_openapi_path(rule.rule)
            
            # Get methods for this route
            methods = [m for m in rule.methods if m not in ['HEAD', 'OPTIONS']]
            
            if path not in paths:
                paths[path] = {}
            
            for method in methods:
                method_lower = method.lower()
                
                # Check if function has swagger spec
                if hasattr(view_func, '_swagger_spec'):
                    paths[path][method_lower] = view_func._swagger_spec.copy()
                else:
                    # Generate basic spec from function
                    paths[path][method_lower] = self._generate_basic_spec(
                        view_func, rule, method
                    )
        
        return {
            "openapi": "3.0.0",
            "info": {
                "title": self.title,
                "version": self.version,
                "description": self.description,
            },
            "paths": paths,
            "components": {
                "schemas": {}
            }
        }
    
    def _flask_route_to_openapi_path(self, flask_path: str) -> str:
        """Convert Flask route syntax to OpenAPI path syntax."""
        # Convert <variable> to {variable}
        # Convert <type:variable> to {variable}
        import re
        path = re.sub(r'<(?:[^:>]+:)?([^>]+)>', r'{\1}', flask_path)
        return path
    
    def _generate_basic_spec(
        self, view_func: Callable, rule, method: str
    ) -> Dict[str, Any]:
        """Generate basic OpenAPI spec from function signature and docstring."""
        spec: Dict[str, Any] = {
            "summary": view_func.__name__.replace('_', ' ').title(),
            "responses": {
                "200": {"description": "Successful response"}
            }
        }
        
        # Add docstring as description if available
        if view_func.__doc__:
            spec["description"] = inspect.cleandoc(view_func.__doc__)
        
        # Extract path parameters from route
        parameters = []
        for arg in rule.arguments:
            param = {
                "name": arg,
                "in": "path",
                "required": True,
                "schema": {"type": "string"}
            }
            # Try to infer type from route converter
            if rule._converters and arg in rule._converters:
                converter = rule._converters[arg]
                if 'int' in str(type(converter)).lower():
                    param["schema"]["type"] = "integer"
                elif 'float' in str(type(converter)).lower():
                    param["schema"]["type"] = "number"
            parameters.append(param)
        
        if parameters:
            spec["parameters"] = parameters
        
        # Add request body for POST, PUT, PATCH
        if method in ['POST', 'PUT', 'PATCH']:
            spec["requestBody"] = {
                "content": {
                    "application/json": {
                        "schema": {"type": "object"}
                    }
                }
            }
        
        return spec
    
    def _get_swagger_ui_html(self) -> str:
        """Return HTML for Swagger UI."""
        return f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{self.title} - Swagger UI</title>
    <link rel="stylesheet" type="text/css" href="https://cdn.jsdelivr.net/npm/swagger-ui-dist@5.10.0/swagger-ui.css">
    <style>
        html {{
            box-sizing: border-box;
            overflow: -moz-scrollbars-vertical;
            overflow-y: scroll;
        }}
        *, *:before, *:after {{
            box-sizing: inherit;
        }}
        body {{
            margin: 0;
            padding: 0;
        }}
    </style>
</head>
<body>
    <div id="swagger-ui"></div>
    <script src="https://cdn.jsdelivr.net/npm/swagger-ui-dist@5.10.0/swagger-ui-bundle.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/swagger-ui-dist@5.10.0/swagger-ui-standalone-preset.js"></script>
    <script>
        window.onload = function() {{
            window.ui = SwaggerUIBundle({{
                url: "{self.openapi_url}",
                dom_id: '#swagger-ui',
                deepLinking: true,
                defaultModelsExpandDepth: 1,
                defaultModelExpandDepth: 1,
                displayRequestDuration: true,
                tryItOutEnabled: true,
                presets: [
                    SwaggerUIBundle.presets.apis,
                    SwaggerUIStandalonePreset
                ],
                plugins: [
                    SwaggerUIBundle.plugins.DownloadUrl
                ],
                layout: "StandaloneLayout"
            }});
        }};
    </script>
</body>
</html>
"""
