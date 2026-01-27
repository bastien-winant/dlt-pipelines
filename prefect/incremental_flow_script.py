from prefect import flow, task
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
def run_resource(resource_name: str, bq_destination: dlt.destinations.bigquery, incremental_date: str | None=None):
	from dlt_pipeline import github_source

	base_source = github_source

	# apply incremental data loading to issues resource
	if incremental_date and resource_name == "issues":
		base_source.issues.apply_hints(
			incremental=dlt.sources.incremental(
				cursor_path="created_at",
				initial_value=incremental_date
			)
		)

	selected_source = base_source.with_resources(resource_name)

	pipeline = dlt.pipeline(
		pipeline_name=f"github_incremental_{resource_name}",
		destination=bq_destination,
		dataset_name=f"incremental_remote_github",
		progress="log"
	)

	load_info = pipeline.run(selected_source)
	print(f"{resource_name} -> {load_info}")

	return load_info

@flow(log_prints=True)
def main(incremental_date: str | None=None):
	# set env variables
	set_github_pat_env()

	# create bigquery destination
	bq_dest = create_bigquery_destination()

	a = run_resource("repos", bq_dest)
	b = run_resource("contributors", bq_dest)
	c = run_resource("releases", bq_dest)
	d = run_resource("issues", bq_dest, incremental_date=incremental_date)

	return a, b, c

if __name__=="__main__":
	main()