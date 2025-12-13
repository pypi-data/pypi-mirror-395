"""
FastAPI endpoint discovery component.

Extracts endpoint information from FastAPI applications using
route introspection and OpenAPI schema generation.
"""
import inspect
from typing import Any, Dict, List, Optional, get_type_hints, get_origin, get_args, Union
from fastapi import FastAPI
from fastapi.routing import APIRoute
from fastapi.params import Query, Path, Body, Header
from fastapi_report.models import EndpointInfo, ParameterInfo


class FastAPIDiscovery:
    """Discovers and extracts endpoint information from FastAPI applications."""
    
    def __init__(self, app: FastAPI):
        """
        Initialize discovery with a FastAPI application.
        
        Args:
            app: FastAPI application instance to analyze
        """
        self.app = app
        self._openapi_schema: Optional[Dict[str, Any]] = None
    
    def discover_endpoints(self) -> List[EndpointInfo]:
        """
        Extract all REST endpoints from FastAPI app.
        
        Returns:
            List of EndpointInfo objects representing all discovered endpoints
        """
        endpoints = []
        
        for route in self.app.routes:
            if isinstance(route, APIRoute):
                endpoint_info = self._extract_endpoint_info(route)
                endpoints.append(endpoint_info)
        
        return endpoints
    
    def get_openapi_schema(self) -> Dict[str, Any]:
        """
        Get complete OpenAPI specification.
        
        Returns:
            OpenAPI schema dictionary
        """
        if self._openapi_schema is None:
            self._openapi_schema = self.app.openapi()
        return self._openapi_schema
    
    def _extract_endpoint_info(self, route: APIRoute) -> EndpointInfo:
        """
        Extract endpoint information from a route.
        
        Args:
            route: FastAPI route to analyze
            
        Returns:
            EndpointInfo object with extracted metadata
        """
        # Get OpenAPI schema for additional metadata
        openapi_schema = self.get_openapi_schema()
        path_item = openapi_schema.get("paths", {}).get(route.path, {})
        
        # Get method-specific operation
        method = list(route.methods)[0].lower() if route.methods else "get"
        operation = path_item.get(method, {})
        
        # Extract parameters
        parameters = self.extract_parameters(route)
        
        # Extract response models
        responses = self.extract_response_models(route, operation)
        
        # Extract request body
        request_body = operation.get("requestBody")
        
        return EndpointInfo(
            path=route.path,
            method=method.upper(),
            operation_id=operation.get("operationId"),
            summary=operation.get("summary") or route.summary,
            description=operation.get("description") or route.description,
            tags=operation.get("tags", []),
            parameters=parameters,
            request_body=request_body,
            responses=responses,
            deprecated=operation.get("deprecated", False)
        )
    
    def extract_parameters(self, route: APIRoute) -> List[ParameterInfo]:
        """
        Extract parameters from route signature.
        
        Args:
            route: FastAPI route to analyze
            
        Returns:
            List of ParameterInfo objects
        """
        parameters = []
        
        # Get function signature
        sig = inspect.signature(route.endpoint)
        type_hints = get_type_hints(route.endpoint)
        
        for param_name, param in sig.parameters.items():
            # Skip special parameters
            if param_name in ("self", "cls", "request", "response"):
                continue
            
            # Determine parameter type and extract metadata
            param_info = self._extract_parameter_info(
                param_name, param, type_hints.get(param_name)
            )
            
            if param_info:
                parameters.append(param_info)
        
        return parameters
    
    def _extract_parameter_info(
        self, 
        name: str, 
        param: inspect.Parameter,
        type_hint: Any
    ) -> Optional[ParameterInfo]:
        """
        Extract information from a single parameter.
        
        Args:
            name: Parameter name
            param: Parameter object from signature
            type_hint: Type hint for the parameter
            
        Returns:
            ParameterInfo object or None if parameter should be skipped
        """
        # Determine parameter location and metadata
        param_type = "query"  # default
        description = None
        constraints = {}
        required = param.default == inspect.Parameter.empty
        default = None if required else param.default
        
        # Check if parameter uses FastAPI parameter types
        if param.default != inspect.Parameter.empty:
            from pydantic_core import PydanticUndefined
            
            if isinstance(param.default, Query):
                param_type = "query"
                description = param.default.description
                constraints = self._extract_constraints(param.default)
                # Check if required using PydanticUndefined
                required = param.default.default is PydanticUndefined or param.default.default == ...
                default = None if required else param.default.default
            elif isinstance(param.default, Path):
                param_type = "path"
                description = param.default.description
                constraints = self._extract_constraints(param.default)
                required = True  # Path parameters are always required
                default = param.default.default if param.default.default not in (PydanticUndefined, ...) else None
            elif isinstance(param.default, Body):
                param_type = "body"
                description = param.default.description
                required = param.default.default is PydanticUndefined or param.default.default == ...
                default = None if required else param.default.default
            elif isinstance(param.default, Header):
                param_type = "header"
                description = param.default.description
                required = param.default.default is PydanticUndefined or param.default.default == ...
                default = None if required else param.default.default
        
        # Extract Python type
        python_type = self._get_type_string(type_hint)
        
        return ParameterInfo(
            name=name,
            param_type=param_type,
            python_type=python_type,
            required=required,
            default=default,
            description=description,
            constraints=constraints
        )
    
    def _extract_constraints(self, field) -> Dict[str, Any]:
        """
        Extract validation constraints from FastAPI field.
        
        Args:
            field: FastAPI parameter field (Query, Path, etc.)
            
        Returns:
            Dictionary of constraints
        """
        constraints = {}
        
        # Try to get constraints from metadata (Pydantic v2)
        if hasattr(field, 'metadata'):
            for metadata_item in field.metadata:
                if hasattr(metadata_item, 'ge') and metadata_item.ge is not None:
                    constraints['ge'] = metadata_item.ge
                if hasattr(metadata_item, 'le') and metadata_item.le is not None:
                    constraints['le'] = metadata_item.le
                if hasattr(metadata_item, 'gt') and metadata_item.gt is not None:
                    constraints['gt'] = metadata_item.gt
                if hasattr(metadata_item, 'lt') and metadata_item.lt is not None:
                    constraints['lt'] = metadata_item.lt
                if hasattr(metadata_item, 'min_length') and metadata_item.min_length is not None:
                    constraints['min_length'] = metadata_item.min_length
                if hasattr(metadata_item, 'max_length') and metadata_item.max_length is not None:
                    constraints['max_length'] = metadata_item.max_length
                if hasattr(metadata_item, 'pattern') and metadata_item.pattern is not None:
                    constraints['pattern'] = metadata_item.pattern
        
        # Fallback to direct attributes (Pydantic v1 style)
        if hasattr(field, 'ge') and field.ge is not None:
            constraints['ge'] = field.ge
        if hasattr(field, 'le') and field.le is not None:
            constraints['le'] = field.le
        if hasattr(field, 'gt') and field.gt is not None:
            constraints['gt'] = field.gt
        if hasattr(field, 'lt') and field.lt is not None:
            constraints['lt'] = field.lt
        if hasattr(field, 'min_length') and field.min_length is not None:
            constraints['min_length'] = field.min_length
        if hasattr(field, 'max_length') and field.max_length is not None:
            constraints['max_length'] = field.max_length
        if hasattr(field, 'pattern') and field.pattern is not None:
            constraints['pattern'] = field.pattern
        if hasattr(field, 'enum') and field.enum is not None:
            constraints['enum'] = list(field.enum)
        
        return constraints
    
    def _get_type_string(self, type_hint: Any) -> str:
        """
        Convert Python type hint to string representation.
        
        Args:
            type_hint: Python type hint
            
        Returns:
            String representation of the type
        """
        if type_hint is None or type_hint == inspect.Parameter.empty:
            return "Any"
        
        # Handle Optional types
        origin = get_origin(type_hint)
        if origin is Union:
            args = get_args(type_hint)
            if type(None) in args:
                # This is Optional[T]
                non_none_args = [arg for arg in args if arg is not type(None)]
                if len(non_none_args) == 1:
                    return f"Optional[{self._get_type_string(non_none_args[0])}]"
                else:
                    return f"Union[{', '.join(self._get_type_string(arg) for arg in args)}]"
            else:
                return f"Union[{', '.join(self._get_type_string(arg) for arg in args)}]"
        
        # Handle generic types
        if origin is not None:
            args = get_args(type_hint)
            if args:
                args_str = ', '.join(self._get_type_string(arg) for arg in args)
                return f"{origin.__name__}[{args_str}]"
            return origin.__name__
        
        # Handle basic types
        if hasattr(type_hint, '__name__'):
            return type_hint.__name__
        
        return str(type_hint)
    
    def extract_response_models(
        self, 
        route: APIRoute,
        operation: Dict[str, Any]
    ) -> Dict[int, Dict[str, Any]]:
        """
        Extract response schemas from route.
        
        Args:
            route: FastAPI route to analyze
            operation: OpenAPI operation object
            
        Returns:
            Dictionary mapping status codes to response schemas
        """
        responses = {}
        
        # Get responses from OpenAPI schema
        openapi_responses = operation.get("responses", {})
        
        for status_code, response_data in openapi_responses.items():
            try:
                status_int = int(status_code)
                responses[status_int] = {
                    "description": response_data.get("description", ""),
                    "content": response_data.get("content", {})
                }
            except ValueError:
                # Skip non-numeric status codes (like 'default')
                continue
        
        return responses
