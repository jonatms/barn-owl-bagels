# Barn Owl Bagels

## Prerequisites

- Docker installed on your machine

## Getting Started

Follow these steps to build and run the Docker container for the Flask application.

### Build the Docker Image

1. Open your terminal and navigate to the project directory.

2. Build the Docker image using the following command:

```sh
docker build -t barn-owl-bagels .
```

### Run the Docker Container

1. Run the Docker container using the following command:

    ```sh
    docker run -p 8000:8000 barn-owl-bagels
    ```

2. The Flask application should now be running and accessible at `http://localhost:8000`.

## Project Structure
