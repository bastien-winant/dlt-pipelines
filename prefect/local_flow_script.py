from prefect import flow, task
import dlt

@task(log_prints=True)
def run_pipeline():
	from dlt_pipeline import github_source

	pipeline = dlt.pipeline(
		pipeline_name="github_repo_issues",
		destination="bigquery",
		dataset_name="dlt_github_data",
		progress="log"
	)

	load_info = pipeline.run(github_source)
	print(load_info)

	return load_info

@flow(log_prints=True)
def main():
	github_workflow = run_pipeline()
	return github_workflow

if __name__=="__main__":
	main.serve(
		name="prefect_deployment",
		cron="0 8 * * *"
	)