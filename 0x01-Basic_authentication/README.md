## Tasks
0. Simple-basic-API
Setup and Start Server

- Install dependencies: pip3 install -r requirements.txt
- Start the server: API_HOST=0.0.0.0 API_PORT=5000 python3 -m api.v1.app
- Test the server using curl: curl "http://0.0.0.0:5000/api/v1/status"
- Files: Ensure the README.md file is updated with setup and usage instructions.

1. Error handler: Unauthorized
- Add Error Handler for 401

- Modify api/v1/app.py to add an error handler for 401 status code.
- Use jsonify to return {"error": "Unauthorized"}.
- Test Error Handler

- Add an endpoint in api/v1/views/index.py to raise a 401 error: @app.route('/api/v1/unauthorized', methods=['GET']) and use abort(401).
- Files: api/v1/app.py, api/v1/views/index.py

2. Error handler: Forbidden
- Add Error Handler for 403

- Modify api/v1/app.py to handle 403 errors with a JSON response: {"error": "Forbidden"}.
- Test Error Handler

- Add an endpoint in api/v1/views/index.py to raise a 403 error: @app.route('/api/v1/forbidden', methods=['GET']) and use abort(403).
- Files: api/v1/app.py, api/v1/views/index.py

3. Auth Class
- Create Auth Class

- Create api/v1/auth/auth.py with an Auth class that includes:
- require_auth(self, path: str, excluded_paths: List[str]) -> bool
- authorization_header(self, request=None) -> str
- current_user(self, request=None) -> TypeVar('User')
File: api/v1/auth/auth.py

4. Define Which Routes Don't Need Authentication
- Update require_auth Method

- Modify the require_auth method in Auth to determine if a path requires authentication.
- File: api/v1/auth/auth.py

5. Request Validation
- Update authorization_header Method

- Modify authorization_header in Auth to validate and return the Authorization header.
- Filter Requests

- Update api/v1/app.py to filter requests based on authentication using Flask’s before_request.
- File: api/v1/app.py, api/v1/auth/auth.py

6. Basic Auth
- Create BasicAuth Class

- Create api/v1/auth/basic_auth.py with an empty BasicAuth class inheriting from Auth.
- Update api/v1/app.py

- Load BasicAuth if AUTH_TYPE is set to basic_auth.
- File: api/v1/auth/basic_auth.py, api/v1/app.py

7. Basic - Base64 Part
- Extract Base64 from Authorization Header

- Implement extract_base64_authorization_header in BasicAuth to parse Base64 from the Authorization header.
- File: api/v1/auth/basic_auth.py

8. Basic - Base64 Decode
- Decode Base64 Authorization Header

- Implement decode_base64_authorization_header in BasicAuth to decode the Base64 string.
- File: api/v1/auth/basic_auth.py