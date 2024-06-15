from prefect import flow, task
from typing import List
import httpx

# from pydata.excel.reader import read_excel
# from pydata.excel.writer import write_excel

@task(log_prints=True)
def show_logs(input: str):
    print("Getting stars for repo: ", input)


@flow(name="Test Flow")
def test_full_flow(repos: List[str]):
    for repo in repos:
        show_logs(repo)


# run the flow!
if __name__=="__main__":
    test_full_flow(["PrefectHQ/Prefect"])