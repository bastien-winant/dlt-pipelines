# Deploying dlt Pipelines with Orchestrators
## Orchestrating
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
4. __There are no logs preserved__ to allow visibility on past runs
5. __Humans are error-prone__ and might not run the pipeline in a reliable and consistent way
6. __Scripts are not reproducible__ when run in a different environment
7. __Computers have limited resources__ and may not be able to handle larger data volumes

dlt handle some of the above issues through features such as incremental loading and backfilling.
For a pipeline to be ready for production, an orchestrator is required that circumvents the issues with local scripts.
- __parallelisation__ provides virtually unlimited compute resources
- __schedulers__ ensure scripts are run without human intervention
- __centalised logging__ keeps stakeholders informed on pipeline runs
- __shared workflows__ allows engineers to work in the same codebase and environment