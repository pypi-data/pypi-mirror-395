# pycivil
A project that aims to make structural engineers free from every commercial
software.

## News

### Version 0.2.0
1. You can use pip install pycivil
2. Module xstrumodeler for generic shape RC section is a requirement 
3. Start to remove sws-mind backend to separate module
4. Added new tool (post-processor) for Strand7

## Development

- Install [poetry](https://python-poetry.org/docs/#installation) and [task](https://taskfile.dev/installation/)
- run `task init` do initialize the python environment and install the pre-commit hooks
- before committing code changes, you can run `task` to perform automated checks. You can also run them separately:
  - `task lint` fixes and checks the code and documentation
  - `task mypy` performs type checking
  - `task test` runs the tests with `pytest`
  - `task security` scans the dependencies for known vulnerabilities

> **NOTE**: the `lint` task is executed automatically when you commit the changes to ensure that only good quality code is added to the repository.

## sws-mind project

This project will be removed from there ASAP

### Description

The project involves the creation of a hardware infrastructure and corresponding software. Its purpose is to consolidate engineering technical knowhow and enable SWS professionals to utilize it comfortably in terms of speed and appearance.

The hardware infrastructure will be a server capable of processing various client requests. The client will be **completely agnostic** of the server's execution methods and may only make calls and await responses using one of the protocols designed for this purpose. Responses may include data streams or entire files.

This separation is necessary for several reasons:

1.  **Development Independence:** Once the communication protocol is established, both server-side and client-side development can proceed simultaneously. For example, while adding server code required for a specific task, the client can simultaneously be prepared to visually display the results.
2.  **Separation of Expertise:** Since the source code content will often require the work of engineers specialized in various fields (galleries, bridges, F.E.M.), only IT experts may be needed for client-side work.
3.  **Multi-user Management:** Requests to the server may need to be made from various parts of the world, potentially simultaneously. This will require the software to be installed on the various clients (e.g., tablets or PCs), which will send requests to the same server.
4.  **Quality Management:** If errors or bugs are discovered in the code, efforts can be focused on resolving them without needing to update the client software.
5.  **Closed Source for Customers:** It will be possible to sell services or microservices to companies or public administrations without them accessing the proprietary engineering knowhow and algorithms required to deliver the product-service.
6.  **Authorization Management:** It will be possible, for example, to grant authorization to a user within the organization to perform specific tasks for a defined period. Additionally, a product-service can be sold externally with a time-limited license.

### Development Phases

1.  **Identification of IT Tools (Hardware & Software for Client and Server)**
    1.  Select server and client hardware
    2.  Decide on the client/server communication protocol
2.  **Design of Some Small Product-Services or Microservices**
3.  **Implementation of Required Server Hardware and Software**
    1.  Software development
    2.  Hardware setup/assembly
4.  **Implementation of the Microservice on the Server**
    1.  Microservice development
    2.  Connect the microservice to the chosen communication protocol
5.  **Development of Software on One Client Type and Test Communication with the Server**

### Docker container

You can run the REST API inside a docker container with the following command:

```shell
docker run -d Dockerfile --name pycivile -p 8000:8000 -e UVICORN_BIND=0.0.0.0
```

> **NOTE**: the environment variable UVICORN_BIND tells the web server on which address to listen to.
> 0.0.0.0 allows you to reach the API from everywhere, but can be a security risk!

Or, if you don't want to clone the repository:

```shell
docker build -t pycivile https://gitlab.com/luigi_paone/pycivile.git
docker run -d pycivile --name pycivile -p 8000:8000 -e UVICORN_BIND=0.0.0.0
```

Or, if you're a docker-compose guy, you can run the [docker-compose.yml](docker-compose.yml) file with:

```shell
docker-compose up
```

This will also create the database (mongodb) and Code_Aster containers.

#### Remove all volumes

This remove all volumes and data. Next relaunch the volumes will be build

```shell
docker-compose down -v
```

### Environment variables

| Name                   | Description                                  | Default                            |
| ---------------------- | -------------------------------------------- | ---------------------------------- |
| `WORKING_DATA_PATH`    | Path for data storage                        | `/app/working-data`                |
| `XLS_SHEETS_DATA_PATH` | Folder with structural calculation workbooks | `/app/res/excel-structural-sheets` |
| `DB_HOST`              | Database hostname                            | `localhost`                        |
| `DB_PORT`              | Database Port                                | `27013`                            |
| `DB_USERNAME`          | Database username                            | empty (no user)                    |
| `DB_PASSWORD`          | Database password                            | empty (no password)                |