# Django Application for retrieving information about products and lessons.

This Django application provides functionalities to manage courses and lessons, gather statistics for each product, and expose APIs for retrieving data.

## Functionality

- **Product Statistics**: Provides statistics like the percentage of purchases and the number of people attending each product.

- **API Endpoints for Retrieving Data**: Exposes APIs to retrieve course, lesson, and product statistics data.

## Main Stack

- **Django**: Web framework for building the application.
- **Django Rest Framework (DRF)**: Toolkit for building Web APIs in Django applications.
- **Python**: Programming language used for backend development.
- **SQLite**: Database management system for storing application data.
- **Docker**: Containerization platform for easy deployment and management of the application.

## Getting Started

### Running the Application using Docker Compose

1. **Clone the repository:**

    ```bash
    git clone <repository_url>
    cd HQtest
    ```

2. **Build and run the Docker container using Docker Compose:**

    ```bash
    docker-compose up --build
    ```

### Running Tests

To run the tests for the main functionality within the Docker container, you can execute a command inside the running container:

```bash
docker-compose run --rm app sh -c 'python manage.py test'
