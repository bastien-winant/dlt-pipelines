# Deploying dlt Pipelines with Orchestrators
## Orchestration
### Why orchestrators
- dlt and features
- ETL scripts to move data
- next step is deployment to leverage automation, scalability, and security
- 
### What is an orchestrator
An pipeline orchestrator is a tool that helps automate workflows.
Most orchestrators have features for job scheduling, workflow execution, and dependency management.

Say you want to have the updated content of a Github repository stored in a data warehouse.
Repositories often contain valuable project information such as open issues and collaborators that we might
extract insights from. In order to be ready for analysis, the data must be centralized and queryable and a data
warehouse meets these criteria.

With libraries such as dlt, an experienced data engineer might be able to create an ETL script that moves a
snapshot of the data from the source to the target location relatively quickly.

In and of itself, a local script does not solve the problem:
1. __Rerunning scripts is a hassle__: full reloads are slow and wasteful
2. __The data may have gaps and errors__ due to changes in the source
3. __The pipeline is too slow__ when running on a single node
4. __There are no logs preserved__ to allow visibility on past runs for debugging
5. __Humans are error-prone__ and might not run the pipeline in a reliable and consistent way
6. __Scripts are not reproducible__ when run in a different environment
7. __Computers have limited resources__ and may not be able to handle larger data volumes

dlt handles some of the above issues through features such as incremental loading and backfilling.
For a pipeline to be fully ready for production, an orchestrator is required that circumvents the issues with local scripts.
- __parallelisation__ provides virtually unlimited compute resources
- __schedulers__ ensure scripts are run consistently and without human intervention
- __centralised logging__ keeps stakeholders informed on pipeline runs
- __shared workflows__ allows engineers to work in the same codebase and environment
- __cloud deployment__ gives access to scalable compute and storage

### Available orchestrators
> Below is a short list of some of the most commonly used orchestrators in use today.
> They generally provide the same set of orchestration features, but differ in how they are configured.

#### Apache Airflow
The industry-standard orchestrator used by teams worldwide, offering flexibility, reliability, and an extensive library of operators.

#### Dagster
A data-first orchestrator that emphasizes lineage, observability, and data governance, making it ideal for complex data ecosystems.

#### Prefect
A Python-native orchestration tool that blends seamlessly into code-driven workflows, prioritizing simplicity and developer productivity.

#### Modal
A serverless orchestrator that removes infrastructure headaches by automatically scaling and managing your workloads in the cloud.

#### Kestra
A YAML-driven orchestration platform combining versionable configuration, flexible execution backends, and intuitive visualization tools.

#### Orchestra
A modern, integration-friendly orchestrator focused on speed, observability, and easy setup for the modern data stack.

## dlt Features
### Terminology
#### Cursor
__Cursor__ is a field in the data - usually a date or ID columns - that serves as a virtual bookmark for the pipeline.

By maintaining a cursor, the pipeline can ingest only new or changed records rather than reprocessing the entire
dataset at every run. This is commonly known as _incremental loading_ and leads to significant efficiency gains.

Secondly, the cursor provides a mechanism for reloading data for a past window to fill gaps or repair history.
We use the Cursor column to delimit the beginning and end of the window to rerun.