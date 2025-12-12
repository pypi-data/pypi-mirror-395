from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="insightconnect-plugin-runtime",
    version="6.4.1",
    description="InsightConnect Plugin Runtime",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Rapid7 Integrations Alliance",
    author_email="integrationalliance@rapid7.com",
    url="https://github.com/rapid7/komand-plugin-sdk-python",
    packages=find_packages(),
    install_requires=[
        "requests==2.32.4",
        "python_jsonschema_objects==0.5.2",
        "jsonschema==4.22.0",
        "certifi==2025.8.3",
        "Flask==3.1.1",
        "gunicorn==23.0.0",
        "greenlet==3.2.3",
        "gevent==25.5.1",
        "marshmallow==3.21.0",
        "apispec==6.5.0",
        "apispec-webframeworks==1.0.0",
        "blinker==1.9.0",
        "structlog==25.4.0",
        "python-json-logger==2.0.7",
        "Jinja2==3.1.6",
        "python-dateutil==2.9.0.post0",
        "opentelemetry-sdk==1.36.0",
        "opentelemetry-instrumentation-flask==0.57b0",
        "opentelemetry-exporter-otlp-proto-http==1.36.0",
        "opentelemetry-instrumentation-requests==0.57b0",
        "urllib3==2.5.0"
    ],
    tests_require=[
        "pytest",
        "docker",
        "dockerpty",
        "swagger-spec-validator",
    ],
    test_suite="tests",
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Topic :: Software Development :: Build Tools",
    ],
)
