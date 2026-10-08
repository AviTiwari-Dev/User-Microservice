


## **Sequence**

    user base
    configuration env variable engine
    engine
    session factory
    exception
    exception handler
    exception register
    enum
    router
    model data storage
        user
            user_id
            first_name
            middle_name
            last_name
            date_of_birth
            gender
            created_at
            updated_at
            deleted_at
    model data validation
        user request base
        user request update base
        user response
    repository
        interface
        implementations
    dependency
    manager
        interface
        implementations
    endpoint
        create_user
        update_user
        get_user
        get_all_user
        delete_user
    configuration env variable user_api
    main.py
    migrations
    sample data
    tests
        unit
        integration
        api
        smoke
        e2e
    github workflows



## **Commands**

### **Docker**

#### **Build Images Locally**

- docker build --target prod -t user-service:prod -f .\services\user\Dockerfile .
- docker build --target test -t user-service:test -f .\services\user\Dockerfile .
- docker build --target migration -t user-service:migration -f .\services\user\Dockerfile .

#### **Run Containers Locally**

- docker run --rm --name user-service --env-file services\user\.env -p 8080:8080 user-service:prod
- docker run --rm --name user-service --env-file services\user\.env -p 8080:8080 user-service:test
- docker run --rm --name user-service --env-file services\user\.env -p 8080:8080 user-service:migration

## **Features**

## **Braches**

- main
    - dev
        - base
        - configuration
        - engine
        - session_factory
        - exception
        - enum
        - router
        - model_data_storage
        - model_data_validation
        - repository
        - dependency
        - manager
        - endpoint
        - background_task
        - utility
        - middleware
        - migration
        - doc


## **Folder Structure**

    ├───.github
    │   └───workflows
    ├───services
    │   └───user
    │       ├───alembic
    │       │   └───versions
    │       ├───docs
    │       ├───requirements
    │       ├───src
    │       │   ├───background_tasks
    │       │   ├───bases
    │       │   ├───configurations
    │       │   │   └───env_variables
    │       │   ├───dependencies
    │       │   ├───endpoints
    │       │   │   └───rest
    │       │   ├───engines
    │       │   ├───enums
    │       │   ├───exceptions
    │       │   ├───exception_handlers
    │       │   ├───managers
    │       │   │   ├───implementations
    │       │   │   └───interfaces
    │       │   ├───middlewares
    │       │   ├───models
    │       │   │   ├───data_storage
    │       │   │   └───data_validation
    │       │   ├───repositories
    │       │   │   ├───implementations
    │       │   │   │   └───postgresql
    │       │   │   ├───interfaces
    │       │   ├───routers
    │       │   ├───session_factories
    │       │   └───utilities
    │       └───tests
    │           ├───api
    │           │   └───endpoints
    │           │       └───rest
    │           ├───configurations
    │           │   └───env_variables
    │           ├───end_to_end
    │           ├───integration
    │           │   └───repositories
    │           ├───smoke
    │           └───unit
    │               ├───managers
    │               └───repositories
    └───shared

## **Environnment Variable**
