from prefect import flow, task
from prefect.task_runners import ThreadPoolTaskRunner
import dlt
from prefect_github import GitHubCredentials
from prefect_gcp import GcpCredentials
import os

def set_github_pat_env():
	pat = GitHubCredentials.load("github-pat").token.get_secret_value()
	os.environ["SOURCES__ACCESS_TOKEN"] = pat

def create_bigquery_destination():
	# retrieve service account info
	gcp = GcpCredentials.load("gcp-creds")
	creds = gcp.service_account_info.get_secret_value() or {}

	# retrieve project id
	project = creds.get("project_id")

	return dlt.destinations.bigquery(credentials=creds, project_id=project)

@task(log_prints=True)
def run_resource(resource_name:str, bq_destination: dlt.destinations.bigquery):
	from dlt_pipeline import github_source

	source = github_source.with_resources(resource_name)

	pipeline = dlt.pipeline(
		pipeline_name=f"github_remote_{resource_name}",
		destination=bq_destination,
		dataset_name=f"dynamic_remote_github",
		progress="log"
	)

	load_info = pipeline.run(source)
	print(f"{resource_name} -> {load_info}")

	return load_info

@flow(task_runner=ThreadPoolTaskRunner(max_workers=5), log_prints=True)
def main():
	# set env variables
	set_github_pat_env()

	# create bigquery destination
	bq_dest = create_bigquery_destination()

	a = run_resource.submit("repos", bq_dest)
	b = run_resource.submit("contributors", bq_dest)
	c = run_resource.submit("releases", bq_dest)
	d = run_resource.submit("issues", bq_dest)
	e = run_resource.submit("forks", bq_dest)

	return a.result(), b.result(), c.result(), d.result(), e.result()

if __name__=="__main__":
	main()