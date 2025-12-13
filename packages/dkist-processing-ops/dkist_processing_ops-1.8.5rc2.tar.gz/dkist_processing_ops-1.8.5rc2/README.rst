dkist-processing-ops
====================

|codecov|

This repository works in concert with `dkist-processing-core <https://pypi.org/project/dkist-processing-core/>`_ and
`dkist-processing-common <https://pypi.org/project/dkist-processing-common/>`_ to provide workflows for the
operational management and smoke testing of the `Automated Processing <https://nso.atlassian.net/wiki/spaces/DPD/pages/3671451/04+-+Automated+Processing>`_ stack.


Developer Setup
---------------

.. code-block:: bash

    pip install -e .[test]
    pip install pre-commit
    pre-commit install

Environment Variables
---------------------

.. list-table::
   :widths: 10 90
   :header-rows: 1

   * - Variable
     - Field Info
   * - LOGURU_LEVEL
     - annotation=str required=False default='INFO' alias_priority=2 validation_alias='LOGURU_LEVEL' description='Log level for the application'
   * - MESH_CONFIG
     - annotation=dict[str, MeshService] required=False default_factory=dict alias_priority=2 validation_alias='MESH_CONFIG' description='Service mesh configuration' examples=[{'upstream_service_name': {'mesh_address': 'localhost', 'mesh_port': 6742}}]
   * - RETRY_CONFIG
     - annotation=RetryConfig required=False default_factory=RetryConfig description='Retry configuration for the service'
   * - OTEL_SERVICE_NAME
     - annotation=str required=False default='unknown-service-name' alias_priority=2 validation_alias='OTEL_SERVICE_NAME' description='Service name for OpenTelemetry'
   * - DKIST_SERVICE_VERSION
     - annotation=str required=False default='unknown-service-version' alias_priority=2 validation_alias='DKIST_SERVICE_VERSION' description='Service version for OpenTelemetry'
   * - NOMAD_ALLOC_ID
     - annotation=str required=False default='unknown-allocation-id' alias_priority=2 validation_alias='NOMAD_ALLOC_ID' description='Nomad allocation ID for OpenTelemetry'
   * - NOMAD_ALLOC_NAME
     - annotation=str required=False default='unknown-allocation-name' alias='NOMAD_ALLOC_NAME' alias_priority=2 description='Allocation name for the deployed container the task is running on.'
   * - NOMAD_GROUP_NAME
     - annotation=str required=False default='unknown-allocation-group' alias='NOMAD_GROUP_NAME' alias_priority=2 description='Allocation group for the deployed container the task is running on'
   * - OTEL_EXPORTER_OTLP_TRACES_INSECURE
     - annotation=bool required=False default=True description='Use insecure connection for OTLP traces'
   * - OTEL_EXPORTER_OTLP_METRICS_INSECURE
     - annotation=bool required=False default=True description='Use insecure connection for OTLP metrics'
   * - OTEL_EXPORTER_OTLP_TRACES_ENDPOINT
     - annotation=Union[str, NoneType] required=False default=None description='OTLP traces endpoint. Overrides mesh configuration' examples=['localhost:4317']
   * - OTEL_EXPORTER_OTLP_METRICS_ENDPOINT
     - annotation=Union[str, NoneType] required=False default=None description='OTLP metrics endpoint. Overrides mesh configuration' examples=['localhost:4317']
   * - OTEL_PYTHON_DISABLED_INSTRUMENTATIONS
     - annotation=list[str] required=False default_factory=list description='List of instrumentations to disable. https://opentelemetry.io/docs/zero-code/python/configuration/' examples=[['pika', 'requests']]
   * - OTEL_PYTHON_FASTAPI_EXCLUDED_URLS
     - annotation=str required=False default='health' description='Comma separated list of URLs to exclude from OpenTelemetry instrumentation in FastAPI.' examples=['client/.*/info,healthcheck']
   * - SYSTEM_METRIC_INSTRUMENTATION_CONFIG
     - annotation=Union[dict[str, bool], NoneType] required=False default=None description='Configuration for system metric instrumentation. https://opentelemetry-python-contrib.readthedocs.io/en/latest/instrumentation/system_metrics/system_metrics.html' examples=[{'system.memory.usage': ['used', 'free', 'cached'], 'system.cpu.time': ['idle', 'user', 'system', 'irq'], 'system.network.io': ['transmit', 'receive'], 'process.runtime.memory': ['rss', 'vms'], 'process.runtime.cpu.time': ['user', 'system'], 'process.runtime.context_switches': ['involuntary', 'voluntary']}]
   * - ISB_USERNAME
     - annotation=str required=False default='guest' description='Username for the interservice-bus.'
   * - ISB_PASSWORD
     - annotation=str required=False default='guest' description='Password for the interservice-bus.'
   * - ISB_EXCHANGE
     - annotation=str required=False default='master.direct.x' description='Exchange for the interservice-bus.'
   * - ISB_QUEUE_TYPE
     - annotation=str required=False default='classic' description='Queue type for the interservice-bus.' examples=['quorum', 'classic']
   * - BUILD_VERSION
     - annotation=str required=False default='dev' description='Fallback build version for workflow tasks.'
   * - GQL_AUTH_TOKEN
     - annotation=Union[str, NoneType] required=False default='dev' description='The auth token for the metadata-store-api.'
   * - OBJECT_STORE_ACCESS_KEY
     - annotation=Union[str, NoneType] required=False default=None description='The access key for the object store.'
   * - OBJECT_STORE_SECRET_KEY
     - annotation=Union[str, NoneType] required=False default=None description='The secret key for the object store.'
   * - OBJECT_STORE_USE_SSL
     - annotation=bool required=False default=False description='Whether to use SSL for the object store connection.'
   * - MULTIPART_THRESHOLD
     - annotation=Union[int, NoneType] required=False default=None description='Multipart threshold for the object store.'
   * - S3_CLIENT_CONFIG
     - annotation=Union[dict, NoneType] required=False default=None description='S3 client configuration for the object store.'
   * - S3_UPLOAD_CONFIG
     - annotation=Union[dict, NoneType] required=False default=None description='S3 upload configuration for the object store.'
   * - S3_DOWNLOAD_CONFIG
     - annotation=Union[dict, NoneType] required=False default=None description='S3 download configuration for the object store.'
   * - GLOBUS_MAX_RETRIES
     - annotation=int required=False default=5 description='Max retries for transient errors on calls to the globus api.'
   * - GLOBUS_INBOUND_CLIENT_CREDENTIALS
     - annotation=list[GlobusClientCredential] required=False default_factory=list description='Globus client credentials for inbound transfers.' examples=[[{'client_id': 'id1', 'client_secret': 'secret1'}, {'client_id': 'id2', 'client_secret': 'secret2'}]]
   * - GLOBUS_OUTBOUND_CLIENT_CREDENTIALS
     - annotation=list[GlobusClientCredential] required=False default_factory=list description='Globus client credentials for outbound transfers.' examples=[[{'client_id': 'id3', 'client_secret': 'secret3'}, {'client_id': 'id4', 'client_secret': 'secret4'}]]
   * - OBJECT_STORE_ENDPOINT
     - annotation=Union[str, NoneType] required=False default=None description='Object store Globus Endpoint ID.'
   * - SCRATCH_ENDPOINT
     - annotation=Union[str, NoneType] required=False default=None description='Scratch Globus Endpoint ID.'
   * - SCRATCH_BASE_PATH
     - annotation=str required=False default='scratch/' description='Base path for scratch storage.'
   * - SCRATCH_INVENTORY_DB_COUNT
     - annotation=int required=False default=16 description='Number of databases in the scratch inventory (redis).'
   * - DOCS_BASE_URL
     - annotation=str required=False default='my_test_url' description='Base URL for the documentation site.'

Deployment
----------

Deployment is done with `turtlebot <https://bitbucket.org/dkistdc/turtlebot/src/main/>`_ and follows
the process detailed in `dkist-processing-core <https://pypi.org/project/dkist-processing-core/>`_

Additionally, when a new release is ready to be built the following steps need to be taken:

1. Freezing Dependencies
#########################

A new "frozen" extra is generated by the `dkist-dev-tools <https://bitbucket.org/dkistdc/dkist-dev-tools/src/main/>`_
package. If you don't have `dkist-dev-tools` installed please follow the directions from that repo.

To freeze dependencies run

.. code-block:: bash

    ddt freeze vX.Y.Z[rcK]

Where "vX.Y.Z[rcK]" is the version about to be released.

2. Tag and Push
###############

Once all commits are in place add a git tag that will define the released version, then push the tags up to Bitbucket:

.. code-block:: bash

    git tag vX.Y.Z[rcK]
    git push --tags origin BRANCH

In the case of an rc, BRANCH will likely be your development branch. For full releases BRANCH should be "main".

.. |codecov| image:: https://codecov.io/bb/dkistdc/dkist-processing-ops/graph/badge.svg?token=6ZDODS2GHT
   :target: https://codecov.io/bb/dkistdc/dkist-processing-ops
