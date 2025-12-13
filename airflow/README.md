# Apache Airflow
## Overview
Apache Airflow is open-source one of the oldest orchestrators in use today,
and benefits from a massive outline community.

## Key Components
The scheduler is the brain of the pipeline and decides which scripts to run and when.
The executors are the machines on which the scripts are run.
The webserver is the name of Airflow's UI.

Airflow workflows are represented as Directed Acyclical Graphs (DAGs).
They comprise
- tasks: individual units of work
- operators: tools for carrying out a task (Python, Bash,...)
