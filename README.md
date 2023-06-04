# Geolocation Proximity Service

## Background

This application contains various Proximity services, build as an assignment for a company.


## Local Setup

> Check out the code from the repository to your local machine and go to root dir.  

        $ cd geo-query-app

> Create Python Virtual Environment  

        python3 -m venv venv

> Activate Virtuan Environment

        source venv/bin/activate

> Install dependencies

        pip3 install -r requirement.txt

> Run uvicorn server

        uvicorn src.app:app --reload

**Server is up and running**


## Api Docs -

- API Swagger documentation can be found at
    >   {host}:{port}/docs  
        127.0.0.1:8000/docs   

- Open API Specification File
    >   [Open Api Specification](openapi.json)

- API Postman Collection can be found in the root folder.
    >   [Postman Collection](geo-query-app.postman_collection.json)
