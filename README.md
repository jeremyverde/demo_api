# demo_api

## Getting Started

### Requirements
1. Python 3.11
1. Docker

### Running Locally

1. Create a virtual environment
   
    e.g.

    ```zsh
    pyenv virtualenv 3.11 demo-api
    ```
1. Activate virtual env:
   
   e.g. 
   ```zsh
    pyenv activate demo-api
    ```
1. Install dependencies:
   ```zsh
    pip install -r requirements.txt
    ```

### Tests
1. Run all tests using pytest, from project root:
   ```zsh
    pytest
    ```

### Running the API
1. Uvicorn to launch the app
   ```zsh
    uvicorn src.main:app --reload
    ```

1. Ensure service is healthy
   ```zsh
    curl localhost:8000/health
    ```

1. Visit docs page for API usage and examples
   
   `http://localhost:8000/docs`

## Running With Docker
### Docker Build
1. From project root:
   ```zsh
    docker build -t demo-api .
    ```

### Run with Docker Compose
1. From project root:

    ```zsh
    docker compose up -d
    ```

### Note: 
the containerized service will forward to local port 8001

2. Ensure container and service are running:
   ```zsh
    curl localhost:8001/health
    ```
