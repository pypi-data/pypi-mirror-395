# qciconnect_common

The qciconnect_common component contains packages or modules that can be shared and reused across all other components. The component is seperated into different sub-components based on their related technical background or functionality. The component can be included in other services by including

    [tool.poetry.dependencies]
    ...
    qciconnect_common = {path = "../commons/qciconnect_common/"}
    ...

in the respective pyproject.toml file. Don't forget to include the relevant packages also in your Dockerfiles (see Orchestrator Dockerfile).

Please be aware that the command `poetry install` is not necessary for this module, as there is no need to set up an independent Python environment and the component isn't designed to operate autonomously. The existing pyproject.toml file merely provides essential information about the module, and its purpose is to facilitate the module's integration into other services.

## qciconnect_logging

Within this qciconnect_common package, a logger is setup for universal application across all components of the platform. This logger is imbued with an array of formatting options specifically designed to streamline the debugging process. It allows users to seamlessly import and apply it to their individual services or modules, thereby ensuring uniformly formatted and consistent logging information across the complete platform. At this stage, log outputs are solely directed to the console. However, it is our future intention to accumulate these logs, particularly within a production environment setting.

## qciconnect_scheduler

Contains a celery app factory with default connection strings. To be used by all other services that require a Celery instance.

## qciconnect_settings

Holds environmental variable settings. Env variables defined in a .env file will  automatically populate in a corresponding Python class `EnvironmentSettings`. The `get_settings` method can be used to access the variables in different services.

## qciconnect_conversion

Provides various helper classes with methods for conversion between data formats, for which no onboard tools exist, e.g., between JSON compatible strings and complex numbers, Numpy arrays, datetime, etc.
