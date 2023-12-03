# TextShare.top Backend

Welcome to the documentation for our Django app and its APIs. 
This repository contains the source code and documentation for a demo web application built with Django.

Feel free to check the demo site at [www.textshare.top](https://www.textshare.top), 
and try out the pre-shared text message: [GqSvoT](https://textshare.top/c/GqSvoT/)

## Table of Contents

- [Overview](#overview)
- [Structure](#structure)
- [CICD Flow](#CICD-Flow)
- [Developer Guidelines](#developer-guidelines)
- [Authentication](#authentication)
- [API Endpoints](#api-endpoints)

## Overview
TextShare app is a text-contents sharing platform. Users can save text paragraph and share it with others.
The App demos how to:
* build APIs.
* add authentication & authorization.
* store and retrieve data from PostgresSQL.
* setup the CICD flow: GitHub -> ArgoCD -> deploy in K8S

## Structure

TextShare Django application follows a well-organized project structure to maintain clarity and scalability.

![image](https://github.com/Softolite/textshare-app-api/assets/5890558/85d4456a-c47a-4808-87d7-ec3ddc1147e2)

Users can interact with the TextShare API by making HTTPS requests to the [API Endpoints](#api-endpoints). To get started, users can register for an account via the `/api/user/create/` endpoint and obtain an authentication token. Users include this authentication token in the Authorization header of their requests to authenticate and gain access to the API's features. Then they can securely access protected resources, such as creating, updating, and deleting text content via API endpoints like `/api/content/contents/`.  The API responds with JSON data, enabling users to seamlessly integrate TextShare's text-sharing functionality into their applications, websites, or scripts. TextShare users and contents data is stored in Postgres DB. Both the API server and Postgres DB are deployed in the same namespace in the Kubernetes cluster.

Below is an overview of the key directories and their purposes:

- **`app/`**: This is the top projects directory for our Django application. 
It houses the primary logic, including settings, URLs, and other essential components.
This directory includes other subdirectories:
- **`app/app/`**: The main project which includes settings.py, wsgi.py, urls.py, etc ...
- **`app/core/`**: The project that enables the core features shared by other projects: models, migrations, admin, etc ...
- **`app/user/`**: Users related views, serializers, etc...
- **`app/content/`**: Content related views, serializers, etc...
- **`app/manage.py`**: The Django management script for tasks like running the development server, database migrations, and more.

- **`k8s_*/`**: Contains Kubernetes deployment manifest files for the project.

- **`.github/workflows/`**: Contains GitHub actions for the project.

- **`.Dockerfile`**: This file describes how the docker image will be built.

- **`docker-compose.yml`**: Contains the docker-compose configurations, for local deployment and development.

- **`requirements.txt`**: Lists Python packages and their versions required to run the application.

This directory structure promotes separation of concerns and enhances code organization. 
Consistency in the project structure is crucial for maintainability and collaboration in the future.

## CICD-Flow

Here is an illustration of a full CICD flow for textshare.top backend app from developer commit to k8s deployment

<img width="788" alt="Screenshot 2023-11-25 at 16 45 27" src="https://github.com/Softolite/textshare-app-api/assets/5890558/b64e1f56-2221-4314-97b1-a7c028e8172e">

The flow is built to minimize manual steps and increase efficiency.
Once the developer push the change to the main branch, Github actions will trigger all unit tests and format checks (Flake8).
If all tests pass, then 2 things will happen:
* a docker image will be built and pushed to Docker Hub.
* K8S deployment manifest will be updated committed and pushed to the same GitHub repo.

ArgoCD, which monitors the repo manifests will make sure to reflect those changes on the K8S cluster.

## Developer guidelines

run make migrations command:
``` 
docker-compose run --rm app sh -c "python manage.py makemigrations"
``` 

apply the migrations:
``` 
docker-compose run --rm app sh -c "python manage.py wait_for_db && python manage.py migrate"
``` 

if migrations doesn't work, try clearing the volume:

```
docker volume list
docker volume rm <volume-id>
``` 

run unit tests:
``` 
docker-compose run --rm app sh -c "flake8 && python manage.py test"
``` 

run the app:

``` 
docker-compose up
``` 

## Authentication

TextShare relies on Django Token Authentication to secure API endpoints and authenticate users. 
Token authentication is a simple and efficient method for allowing clients to authenticate with Django backend.

**This application allows the default user interactions:**

1. **User Registration**: Users can create accounts by sending a `POST` request to the registration endpoint.

2. **Login**: To authenticate, users provide their credentials (username and password) via a `POST` request to the login endpoint. Upon successful login, a token is issued.

3. **Token Usage**: Clients must include the token in the header of their HTTP requests to protected endpoints. The header should have the format `Authorization: Token <token_value>`, where `<token_value>` is the user's authentication token.

4. **Access Control**: TextShare uses token authentication to control access to specific resources. Users without a valid token cannot access protected APIs.

## API Endpoints

Below link documents all the API endpoints provided by TextShare backend:

[API documentation](https://admin.textshare.top/api/docs/)
