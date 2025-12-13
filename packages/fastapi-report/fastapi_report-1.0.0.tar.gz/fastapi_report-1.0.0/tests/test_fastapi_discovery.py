"""
Property-based tests for FastAPI discovery.

Feature: endpoint-reporter, Property 1: Complete Route Discovery
Validates: Requirements 1.1
"""
from fastapi import FastAPI, Query, Path
from hypothesis import given, strategies as st, settings
from fastapi_report.discovery.fastapi_discovery import FastAPIDiscovery


def test_discover_all_routes():
    """
    Feature: endpoint-reporter, Property 1: Complete Route Discovery
    For any FastAPI app with registered routes, discovering endpoints should return all routes.
    """
    app = FastAPI()
    
    # Add various endpoints
    @app.get("/users")
    def get_users():
        return []
    
    @app.post("/users")
    def create_user():
        return {}
    
    @app.get("/users/{user_id}")
    def get_user(user_id: int):
        return {}
    
    @app.delete("/users/{user_id}")
    def delete_user(user_id: int):
        return {}
    
    discovery = FastAPIDiscovery(app)
    endpoints = discovery.discover_endpoints()
    
    # Should discover all 4 endpoints
    assert len(endpoints) == 4
    
    # Verify paths are captured
    paths = {e.path for e in endpoints}
    assert "/users" in paths
    assert "/users/{user_id}" in paths
    
    # Verify methods are captured
    methods = {(e.path, e.method) for e in endpoints}
    assert ("/users", "GET") in methods
    assert ("/users", "POST") in methods
    assert ("/users/{user_id}", "GET") in methods
    assert ("/users/{user_id}", "DELETE") in methods


def test_discover_endpoints_with_varying_counts():
    """
    Feature: endpoint-reporter, Property 1: Complete Route Discovery
    Test with different numbers of endpoints.
    """
    for num_endpoints in [0, 1, 5, 10]:
        app = FastAPI()
        
        # Dynamically add endpoints
        for i in range(num_endpoints):
            path = f"/endpoint{i}"
            
            # Create endpoint function dynamically
            def make_handler():
                def handler():
                    return {"id": i}
                return handler
            
            app.add_api_route(path, make_handler(), methods=["GET"])
        
        discovery = FastAPIDiscovery(app)
        endpoints = discovery.discover_endpoints()
        
        assert len(endpoints) == num_endpoints


def test_query_parameter_extraction():
    """
    Feature: endpoint-reporter, Property 2: Query Parameter Metadata Completeness
    For any endpoint with query parameters, all metadata should be captured.
    """
    app = FastAPI()
    
    @app.get("/search")
    def search(
        q: str = Query(..., description="Search query", min_length=1, max_length=100),
        limit: int = Query(10, ge=1, le=100, description="Result limit"),
        offset: int = Query(0, ge=0, description="Result offset")
    ):
        return []
    
    discovery = FastAPIDiscovery(app)
    endpoints = discovery.discover_endpoints()
    
    assert len(endpoints) == 1
    endpoint = endpoints[0]
    
    # Should have 3 parameters
    assert len(endpoint.parameters) == 3
    
    # Check 'q' parameter
    q_param = next(p for p in endpoint.parameters if p.name == "q")
    assert q_param.param_type == "query"
    assert q_param.python_type == "str"
    assert q_param.required == True
    assert q_param.description == "Search query"
    assert q_param.constraints.get("min_length") == 1
    assert q_param.constraints.get("max_length") == 100
    
    # Check 'limit' parameter
    limit_param = next(p for p in endpoint.parameters if p.name == "limit")
    assert limit_param.param_type == "query"
    assert limit_param.python_type == "int"
    assert limit_param.required == False
    assert limit_param.default == 10
    assert limit_param.constraints.get("ge") == 1
    assert limit_param.constraints.get("le") == 100


def test_path_parameter_extraction():
    """
    Feature: endpoint-reporter, Property 3: Path Parameter Documentation
    For any endpoint with path parameters, all metadata should be documented.
    """
    app = FastAPI()
    
    @app.get("/users/{user_id}/posts/{post_id}")
    def get_post(
        user_id: int = Path(..., description="User ID", ge=1),
        post_id: int = Path(..., description="Post ID", ge=1)
    ):
        return {}
    
    discovery = FastAPIDiscovery(app)
    endpoints = discovery.discover_endpoints()
    
    assert len(endpoints) == 1
    endpoint = endpoints[0]
    
    # Should have 2 path parameters
    assert len(endpoint.parameters) == 2
    
    # Check user_id parameter
    user_id_param = next(p for p in endpoint.parameters if p.name == "user_id")
    assert user_id_param.param_type == "path"
    assert user_id_param.python_type == "int"
    assert user_id_param.required == True
    assert user_id_param.description == "User ID"
    assert user_id_param.constraints.get("ge") == 1
    
    # Check post_id parameter
    post_id_param = next(p for p in endpoint.parameters if p.name == "post_id")
    assert post_id_param.param_type == "path"
    assert post_id_param.required == True


def test_request_body_extraction():
    """
    Feature: endpoint-reporter, Property 4: Request Body Schema Extraction
    For any endpoint with a request body, the schema should be extracted.
    """
    from pydantic import BaseModel
    
    app = FastAPI()
    
    class UserCreate(BaseModel):
        username: str
        email: str
        age: int
    
    @app.post("/users")
    def create_user(user: UserCreate):
        return user
    
    discovery = FastAPIDiscovery(app)
    endpoints = discovery.discover_endpoints()
    
    assert len(endpoints) == 1
    endpoint = endpoints[0]
    
    # Should have request body
    assert endpoint.request_body is not None
    assert "content" in endpoint.request_body


def test_response_model_extraction():
    """
    Feature: endpoint-reporter, Property 5: Response Model Documentation
    For any endpoint with response models, schemas and status codes should be documented.
    """
    from pydantic import BaseModel
    
    app = FastAPI()
    
    class User(BaseModel):
        id: int
        username: str
    
    @app.get("/users/{user_id}", response_model=User)
    def get_user(user_id: int):
        return User(id=user_id, username="test")
    
    discovery = FastAPIDiscovery(app)
    endpoints = discovery.discover_endpoints()
    
    assert len(endpoints) == 1
    endpoint = endpoints[0]
    
    # Should have response information
    assert len(endpoint.responses) > 0
    assert 200 in endpoint.responses


def test_openapi_schema_retrieval():
    """
    Feature: endpoint-reporter, Property 11: OpenAPI Schema Retrieval
    For any FastAPI app, requesting OpenAPI schema should invoke openapi() method.
    """
    app = FastAPI(title="Test API", version="1.0.0")
    
    @app.get("/test")
    def test_endpoint():
        return {}
    
    discovery = FastAPIDiscovery(app)
    schema = discovery.get_openapi_schema()
    
    # Should return valid OpenAPI schema
    assert isinstance(schema, dict)
    assert "openapi" in schema
    assert "info" in schema
    assert schema["info"]["title"] == "Test API"
    assert schema["info"]["version"] == "1.0.0"
    assert "paths" in schema
    assert "/test" in schema["paths"]
