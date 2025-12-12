
# InsightConnect Python Plugin Runtime ![Build Status](https://github.com/rapid7/komand-plugin-sdk-python/workflows/Continuous%20Integration/badge.svg)

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

The InsightConnect Python Plugin Runtime is used for building plugins in Python for Rapid7 InsightConnect. The project
results in the building and publishing of two components: 

* Python Plugin Runtime Library 
* Base InsightConnect Plugin Docker Images 

![InsightConnect Python Plugin Runtime Diagram](plugin-runtime-diagram.png)

Docker images created during the build and deployment of this project are uploaded to the 
[Rapid7 Docker Repositories](https://hub.docker.com/orgs/rapid7/repositories).

Further [documentation](https://komand.github.io/python/start.html) for building an InsightConnect plugin is available 
to get started.

## Development of the InsightConnect Plugin Runtime

The Python Runtime codebase is built to support Python 3.11.13 as of version 6.2.3. The following dependencies will need 
to be installed when developing or testing the Plugin Runtime:

- Python 3.11.13
- Docker
- make
- tox

### Getting Started

#### Building Python Library

To build and install the plugin runtime library locally, first create a Python virtual environment for the particular Python 
version and activate it. Then build, install, and confirm the package has been installed.
```
> python3 -m venv venv
> source venv/bin/activate
> pip install -e ./
> pip list | grep insightconnect-plugin-runtime
insightconnect-plugin-runtime 6.2.3
```

#### Building the InsightConnect Plugin Runtime Docker Images

Currently the `python-3` dockerfile is used by default when building the docker image. If you want to specify another
dockerfile for testing purposes, such as `python-3-slim`, you can pass it as an argument.

```
make build-image DOCKERFILE=python-3-slim
```

This will overwrite the default `python-3`, provided that it exists in the `dockerfiles` directory.

#### Building/troubleshooting local images (Mac M1)

Our images are built with OS/ARCH:linux/amd64 due to our ci.yml file specifying linux. Historically this has
not caused any issues but with an M1 Mac, docker will now use arm64. This is because docker builds the image to match the
distribution of the OS running the command. To ensure that building locally and on GH produces an image of the same 
architecture the `--platform` specifier is passed in the dockerfile.

If you build a plugin locally we can see further issues that:
- the local image does match the current OS distro so docker continues to look remotely..
- docker can not find this (newly created) image remotely on docker registry (dev images should not be pushed to registry)

To overcome this we need to specify `platform=linux/amd64` in the plugin docker file. E.g. if building plugins/html then
this file should be updated `plugins/html/Dockerfile`.
*Note*: building this arch on mac M1 will cause the build to be slower.


Example error of local image not matching OS distro without passing the `--platform` flag:
```
 => ERROR [internal] load metadata for docker.io/rapid7/insightconnect-python-3-slim-plugin:latest                          1.4s
------
 > [internal] load metadata for docker.io/rapid7/insightconnect-python-3-slim-plugin:latest:
------
Dockerfile:1
--------------------
   1 | >>> FROM rapid7/insightconnect-python-3-slim-plugin
   2 |     LABEL organization=rapid7
   3 |     LABEL sdk=python
--------------------
ERROR: failed to solve: rapid7/insightconnect-python-3-slim-plugin: pull access denied, repository does not exist or may require authorization: server message: insufficient_scope: authorization failed
make: *** [image] Error 1
```

### Testing Sample Plugin
The easiest way to test changes to the runtime is by running it locally against one of the [sample plugins](./samples) 
included in the repository. Make sure a virtual environment has been activated and then pass in the sample directory 
name as a parameter:
```
> make sample=example run-sample
```

The plugin will be started in `http` mode and listening at `http:0.0.0.0:10001`:
```
[2020-02-13 23:21:13 -0500] [56567] [INFO] Starting gunicorn 23.0.0
[2020-02-13 23:21:13 -0500] [56567] [INFO] Listening at: http://0.0.0.0:10001 (56567)
[2020-02-13 23:21:13 -0500] [56567] [INFO] Using worker: threads
[2020-02-13 23:21:13 -0500] [56571] [INFO] Booting worker with pid: 56571
```

To override Gunicorn config export environment variable GUNICORN_CONFIG_FILE pointing to json file with config
See example in samples/example/gcfg.json 
```
export GUNICORN_CONFIG_FILE ="./gcfg.json"
```

To build, install, and run runtime changes without the use of the `run-sample` rule, the below steps can be used for 
same result:
```
> python setup.py build && python setup.py install
> cd samples/example
> python setup.py build && python setup.py install
> ./bin/icon_example http
```

### Testing Locally with Docker Runtime

In addition to testing locally with the resulting runtime and an InsightConnect plugin, it is also possible to build a 
plugin locally and test it as it would be used by the InsightConnect orchestrator.

First, build the base runtime:
```
make build-image
```

This will result in tagged Docker images that can be used in the included sample plugins. Then the plugin can be built 
and run locally:
```
> cd samples/example
> icon-plugin build image --no-pull
> docker run -it -p 10001:10001 rapid7/example:latest http
```

## Running Tests

In order to run tests, first ensure `tox` has been installed. Tox makes it easy for testing this project in isolated 
virtual environments and for specific Python versions. To install tox:
```
> pip install tox
```

Running all tests:
```
> tox
```

Running a specific test file:
```
> tox -e py39 -- tests/plugin/hello_world/tests/test_cli.py
```

## Plugin vs Slim Plugin Comparison

|                   | Plugin  | Slim Plugin |
|:------------------|:-------:|:-----------:|
| Python Version    | 3.13.9  |   3.13.9    |
| OS                | Alpine  |   Trixie    |
| Package installer |   apk   |     apt     |
| Shell             | /bin/sh |  /bin/bash  |
| Image Size        | ~500MB  |   ~300MB    |

Note that for the plugin image, we run `apk update` and `apk add ..` which leads to a longer build time.

## Release

To release a new version of the InsightConnect Python Plugin Runtime, the below steps must be followed:

1. Make sure that version is updated in changelog, and `setup.py` file. 
2. Create a Pull Request with your changes to be merged into master
3. Merge changes after receiving at least one approval
4. Create a versioned tag off of release; version must follow [SemVer](https://semver.org/); using the `git tag [version #]` command (not through the GitHub release UI!) then `git push origin --tags`.
5. [Github Action](https://github.com/rapid7/komand-plugin-sdk-python/actions) will perform a matrix build and release 
based on the recently created tag for each Python version and Dockerfile in scope

## Contributions

Contributions for maintaining and enhancing the InsightConnect Python Plugin Runtime are appreciated. This project uses
[Black](https://github.com/psf/black) for code formatting and includes a pre-commit hook to auto format code as it is
contributed. Black is installed as a test dependency and the hook can be initialized by running `pre-commit install` 
after cloning this repository.

## Changelog
* 6.4.1 - Fix logging on cloud mode to remove `taskName` | Close boto client after assuming role
* 6.4.0 - When running in cloud mode, always create a new connection object | Bump Python version to 3.13.9 | Docker build tidyup to reduce image size
* 6.3.10 - Fixed tracing name to better allign otel standards
* 6.3.9 - Fixed `monitor_task_delay` decorator handling of millisecond epoch timestamps | Allow `test_task` connection method to accept task name parameter | Updated base images to Python 3.11.13
* 6.3.8 - Update exception string representation methods to remove newline characters
* 6.3.7 - Addressed vulnerability in 'urllib3' (removed from `requirements.txt` as it's a dependency of `botocore`)
* 6.3.6 - Added required dependency to plugin runtime
* 6.3.5 - Added `monitor_task_delay` decorator to detect processing delays
* 6.3.4 - Addressed vulnerabilities within the slim and non-slim Python images (bumping packages)
* 6.3.3 - Add helper func for tracing context to preserve parent span in threadpools
* 6.3.2 - Raise `APIException` from within the `response_handler` to easily access the status code within the plugin
* 6.3.1 - Improved filtering for `custom_config` parameters for plugin tasks
* 6.3.0 - Add Tracing Instrumentation
* 6.2.6 - Remove setuptools after installation
* 6.2.5 - Fixed bug related to failure to set default region to assume role method in `aws_client` for newer versions of boto3 | Updated alpine image packages on build
* 6.2.4 - Update `make_request` helper to support extra parameter of `max_response_size` to cap the response
* 6.2.3 - Updated dockerfiles for both `slim` and `full` SDK types to use Python 3.11.11 | Updated dependencies | Removed `pkg_resources` usage due to deprecation
* 6.2.2 - Fix instances where logging errors would lead to duplicate entries being output | Add option to hash only on provided keys for `hash_sha1` function
* 6.2.1 - Fix instances where logging would lead to duplicate entries being output
* 6.2.0 - Update base images to pull Python 3.11.10 | changed the pep-8 check in tox to `pycodestyle`
* 6.1.4 - Address vulnerabilities within local development requirements.txt and vulnerabilities in slim image.
* 6.1.3 - Addressing failing Python Slim package (bump packages).
* 6.1.2 - Removing the call to mask_output_data for task code.
* 6.1.1 - Addressed vulnerabilities within the slim and non-slim Python images (bumping packages).
* 6.1.0 - Update AWSAction tests to utilise AWS Client Error names for connection test | Update `request_error_handling` to include input for custom configuration
* 6.0.1 - Address vulnerabilities within the following python packages: `Jinja2`, `requests`, `urllib3`, `zipp` and `setuptools`.
* 6.0.0 - Address vulnerabilities within `certifi` python package | Bump the version of OpenSSL used | If running a task connection test, return a custom message from the task test and not the full log.
* 5.6.1 - Making sure all paths that can call the task connection test endpoints return a 400 error if the test fails
* 5.6.0 - Add APIException class for error handling | Fix error in response_handler where data of type Response was not correctly being returned
* 5.5.5 - Address bug with typing for type `Dict` in Python 3.8
* 5.5.4 - Support pagination parameters within AWS client.
* 5.5.3 - Adding in a new endpoint that can be called to run a task connection test
* 5.5.2 - Address bug with typing for type `List` in Python 3.8
* 5.5.1 - Address bug with typing for type `Tuple` in Python 3.8
* 5.5.0 - Updated helper class to add `make_request`, `response_handler`, `extract_json`, and `request_error_handling` for HTTP requests, and `hash_sha1` and `compare_and_dedupe_hashes` to provide support for hash comparisons | Add `METHOD_NOT_ALLOWED`, `CONFLICT`, `REDIRECT_ERROR`, and `CONNECTION_ERROR` to PluginException presets
* 5.4.9 - Updated aws_client to clean assume role json object to remove any none or empty string values.
* 5.4.8 - Address vulnerabilities within `gunicorn` and `idna` python packages.
* 5.4.7 - Address vulnerabilities within `insightconnect-python-3-plugin` image.
* 5.4.6 - Updated our cloud loggers to include the request path | Updated slim image to remediate vulnerabilities.
* 5.4.5 - Updated base images to pull Python 3.9.19 | Alpine image: Updated expat package
* 5.4.4 - Handling the 'Connection Refused' to cps (during startup) as an info instead of error log as this is an expected error.
* 5.4.3 - Updated dependencies to the latest versions | Fixed issue related to logger `StreamHandlers`
* 5.4.2 - Remove background scheduler to simplify when the server gets custom_config values | Revert to use `bullseye` for slim image.
* 5.4.1 - Retry logic added to get values from external API for custom_config values.
* 5.4.0 - Implementation of custom_config parameter for plugin tasks | Alpine image updated OpenSSL and expat | Use `bookworm` for slim image.
* 5.3.2 - Updated OpenSSL in alpine image and core packages to latest versions.
* 5.3.1 - New logging added to the beginning and end of a task | New logging when an exception is instantiated.
* 5.3.0 - Update base images to pull Python 3.9.18 | python packages bump | rename image to drop python minor version.
* 5.2.4 - Extended logging with OrgID and IntID
* 5.2.3 - Extended logging in AWSClient
* 5.2.2 - Fix longstanding bug where some error responses from a plugin could be in HTML format instead of JSON 
* 5.2.1 - Add `INVALID_CREDENTIALS` exception preset
* 5.2.0 - Add `status_code` and `exception` properties to task output
* 5.1.4 - Fix credential masking when connection is null
* 5.1.3 - Fix credential masking when some input fields are empty
* 5.1.2 - Add connection credential masking to the plugin's output and log when displayed as plain text | Add new `OutputMasker` class to handle credential masking    
* 5.1.1 - Updated exception preset messages
* 5.1.0 - Add new helper functions
* 5.0.0 - Add `has_more_pages` property to task output to indicate task pagination status to output consumers
* 4.10.1 - Remove raising of exception if request id is not available in header
* 4.10.0 - Add structlog for structured logging
* 4.9.0 - Add current SDK version plugin is using to /info endpoint
* 4.8.0 - Add `OAuth20ClientCredentialMixin` class to clients
* 4.7.6 - Add `PaginationHelper` to the AWS Client | Refactored the `ActionHelper` | Add `region` handler for AWSAction 
* 4.7.5 - Add AWS client for assuming role 
* 4.7.4 - Convert data field to string in exception handling 
* 4.7.3 - Add `measurement_time` property to plugin metrics collection
* 4.7.2 - Fix incorrect status codes when handling PluginExceptions
* 4.7.1 - Fix new connection test endpoint, version pin requests to 2.26.0
* 4.7.0 - Add endpoint for retrieving all action definitions (input schemas for all actions within a plugin)
* 4.6.0 - Add Bad Response preset to PluginException | Improve 400 error exception handling
* 4.5.1 - Bump version number for release pipeline
* 4.5.0 - Improve exception handling for non-ConnectionTestException errors during a connection test
* 4.4.0 - Add initial support for plugin runtime metrics collection
* 4.3.3 - Constrain greenlet dependency version to fix conflict with gevent
* 4.3.2 - Update Flask dependency to version 2.0.3
* 4.3.1 - Add Timeout Preset to ConnectionTestException
* 4.2.1 - Add helpful error messages in JSON
* 4.2.0 - Add implementation and endpoints for tasks
* 4.1.1 - Update gevent dependency version to 20.9.0
* 4.1.0 - Provide ability to run with gevent asynchronous gunicorn worker class for increased performance
* 4.0.3 - Fix to avoid command injections when using exec_command helper method
* 4.0.2 - Fix to remove unprintable characters from trigger logs
* 4.0.1 - Fix bug by including schema files in manifest | Fix issue uploading python library twice to PYPI
* 4.0.0 - Implement new API endpoints | 
 Implement Swagger API documentation generation | 
 End support for Python2 and PyPy | 
 Add development details to README |
 Enhancements to Makefile for local development and release | 
 Rebrand SDK to InsightConnect Python Plugin Runtime | 
 Revamp release process with use of Github Actions
* 3.3.0 - Add webserver route to allow for threading changes
* 3.2.0 - Add new ConnectionTestException/PluginException presets:
 UNKNOWN, BASE64_ENCODE, BASE64_DECODE, INVALID_JSON |
 Add an optional data parameter for formatting response output
