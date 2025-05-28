# 🔄 Universal REST Inspector (FastAPI)

This project is a universal REST microservice built with **FastAPI** that accepts HTTP requests on **any endpoint** and returns a detailed JSON response containing:

- Request headers
- Requested path
- HTTP method
- Query parameters
- Cookies
- Request body (if any)
- Client IP address
- HTTP version (1.0, 1.1, or 2)

---

## 🚀 Use Cases

This tool is useful in various development and debugging scenarios:

- 🧪 **API Testing**: Inspect what your client (Postman, curl, frontend, etc.) is actually sending.
- 🔄 **Webhook Debugging**: Test external services like Stripe, GitHub, Twilio, or Slack that send webhooks to your server.
- 📋 **HTTP Traffic Inspection**: Log and analyze incoming requests for development or security auditing.
- 🔧 **Mocking Endpoints**: Simulate API responses during frontend development or integration testing.

---

## 📦 Requirements

- [Docker](https://www.docker.com/) installed on your machine.

---

## 🛠 How to Build and Run with Docker

1. Clone or copy the project files:

    ```
    app.py
    requirements.txt
    Dockerfile
    ```

2. **Build the Docker image**:

    ```bash
    docker build -t universal-rest-api .
    ```

3. **Run the container**:

    ```bash
    docker run -p 8000:8000 universal-rest-api
    ```

4. Access the API via your browser or a REST client:

    ```
    http://localhost:8000/any/path/you/want
    ```

---

## 📄 Example Request

```bash
curl -X POST "http://localhost:8000/test/example?foo=bar" \
  -H "X-Custom: value" \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello!"}'
```

**Example Response:**

```json
{
  "path": "/test/example",
  "method": "POST",
  "headers": {
    "host": "localhost:8000",
    "x-custom": "value",
    "content-type": "application/json",
    ...
  },
  "query_params": {
    "foo": "bar"
  },
  "cookies": {},
  "body": "{\"message\": \"Hello!\"}",
  "client_ip": "127.0.0.1",
  "http_version": "1.1"
}
```

---

## 📋 Error Code Endpoint

### Request

```
GET /errorcode/{status_code}
```

- Replace `{status_code}` with any valid HTTP status (100–599).
- Returns a response with the exact status code and metadata.

### Example

```bash
curl http://localhost:8000/errorcode/404
```

**Response:**

```json
{
  "status_code": 404,
  "message": "Generated error with status 404",
  "client_ip": "127.0.0.1",
  "http_version": "1.1"
}
```

**Logged Output:**

```
[INFO] Error Code Request: 404 from 127.0.0.1 via HTTP/1.1
```

---

## 📝 Logging

Each request is logged in detail:

- Client IP
- HTTP version
- HTTP method
- Path and query string
- All headers
- Body (if present)

Logs are formatted for clarity and separated by lines for easier reading during debugging.

---

## 📁 Project Structure

```
.
├── app.py              # Main FastAPI app
├── Dockerfile          # Docker build instructions
└── requirements.txt    # Python dependencies
```

---

## 📚 Technologies Used

- [FastAPI](https://fastapi.tiangolo.com/)
- [Uvicorn](https://www.uvicorn.org/)
- [Docker](https://www.docker.com/)

---

## 📝 License

This project is open-source and free to use for development, testing, learning, and debugging purposes.


---

## 🐳 Docker Image

This project is available as a public Docker image:

```
docker pull smrcascao/api-checker:1.0.0
```

To run it:

```bash
docker run -p 8000:8000 smrcascao/api-checker:1.0.0
```

---

## ☸️ Kubernetes Deployment

Below is a sample Kubernetes manifest to deploy **api-checker** using:

- A **Deployment** with 1 replica
- A **LoadBalancer Service**
- AWS-specific annotations to make it **internal/private**

### 📄 `api-checker-deployment.yaml`

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: api-checker
  labels:
    app: api-checker
spec:
  replicas: 1
  selector:
    matchLabels:
      app: api-checker
  template:
    metadata:
      labels:
        app: api-checker
    spec:
      containers:
        - name: api-checker
          image: smrcascao/api-checker:1.0.0
          ports:
            - containerPort: 8000
```

---

### 📄 `api-checker-service.yaml`

```yaml
apiVersion: v1
kind: Service
metadata:
  name: api-checker
  annotations:
    service.beta.kubernetes.io/aws-load-balancer-internal: "true"
spec:
  type: LoadBalancer
  selector:
    app: api-checker
  ports:
    - protocol: TCP
      port: 80
      targetPort: 8000
```

Deploy it with:

```bash
kubectl apply -f api-checker-deployment.yaml
kubectl apply -f api-checker-service.yaml
```

---

## ✅ Summary

You can now run this API with:

- `Docker`: `smrcascao/api-checker:1.0.0`
- `Kubernetes`: using provided manifests
- `HTTP/1.1 or HTTP/2` support with full logging and debugging capabilities

