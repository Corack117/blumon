# Blumon Project

This repository contains the source code and necessary configuration for the development of the Blumon application. Follow the steps below to set up and run the development environment.

## Prerequisites

Make sure you have Docker Desktop installed on your system. You can download it from the following link: [Download Docker Desktop](https://docs.docker.com/compose/install/#scenario-one-install-docker-desktop)

## Setting up the Development Environment

Once you have Docker Desktop installed, follow these steps to set up the development environment:

1. Create a virtual environment by running the following command:

    ```bash
    py -m venv venv
    ```
2. Activate the virtual environment. For example, on macOS, use:

    ```bash
    source venv/bin/activate
    ```

3. Install the required libraries by running:

    ```bash
    pip install -r ./requirements.txt
    ```

## Building and Running

To build the container, run:

```bash
docker-compose build
```

To run the container, use the following command:

```bash
docker-compose up
```

## Running Tests

If you want to run the tests, first build the container (if you haven't already) and then use the following command:

```bash
docker-compose build && docker-compose run --rm app pytest -s
```

Now you are ready to start developing and testing the Blumon application!


