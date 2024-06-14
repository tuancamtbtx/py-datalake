from google.cloud import bigquery
import pandas as pd
from functools import lru_cache

from pydata.logger.logger_mixing import LoggerMixing

class BigqueryService(LoggerMixing):
	def __init__(self,project_id,**kwargs):
		super().__init__()
		self.project_id = project_id
		self.bq_client = self.get_client()

	def get_state_bq_job(self,location:str=None, bq_job=None):
		query_job = self.bq_client.get_job(job_id=bq_job.job_id, location=location)
		self.logger.info(f"Query job: {query_job.state}")
		return query_job.state
	
	@lru_cache(maxsize=1)
	def get_client(self):
		return bigquery.Client(project= self.project_id)
	
	def query(self, query:str):
		client = self.get_client()
		query_job = client.query(query)
		rows = query_job.result()
		return rows.to_dataframe()

	def query_job(self,location:str, query:str=None, dataset_name:str=None, use_legacy_sql:bool = True):
		import hashlib
		table_name = hashlib.md5(query.encode('utf-8')).hexdigest()
		tmp_table = f'{self.project_id}.{dataset_name}.bde_{table_name}'
		self.logger.info(f"Start query job with query: {query} - tmp_table: {tmp_table}")
		job_config = bigquery.QueryJobConfig(
			destination=tmp_table,
			allow_large_results=True,
			write_disposition="WRITE_TRUNCATE",
			use_legacy_sql=use_legacy_sql,
			create_disposition='CREATE_IF_NEEDED',
		)
		query_job = self.bq_client.query(query,location=location, job_config=job_config)
		return query_job
	
	def insert(self, table_id:str, df, write_disposition="WRITE_TRUNCATE", time_partitioning=None, schema=None):
		self.logger.info(f"Start insert data to table: {table_id}")
		if schema is not None:
			job_config = bigquery.LoadJobConfig(
				create_disposition='CREATE_IF_NEEDED',
				write_disposition=write_disposition,
				schema=schema,
			)
		else:
			job_config = bigquery.LoadJobConfig(
				create_disposition='CREATE_IF_NEEDED',
				write_disposition=write_disposition,
				autodetect=True,
			)
		if time_partitioning is not None:
			self.logger.info(f"Partition field: {time_partitioning}")
			job_config.time_partitioning = time_partitioning
		job = self.bq_client.load_table_from_dataframe(
			df, table_id, job_config=job_config
		)
		job.result()
		self.logger.info(f"Insert data to table: {table_id} - Done")
		return job.state
	

	def _build_on_clause(self, unique_keys):
		on_clause = ""
		for key in unique_keys:
			on_clause += f"t.{key} = s.{key} and "
		on_clause = on_clause[:-4]
		return on_clause
	
	def is_table_exists(self, table_id:str):
		dataset_id = table_id.split('.')[1]
		table_name = table_id.split('.')[2]
		dataset = self.bq_client.dataset(dataset_id)
		table_ref = dataset.table(table_name)
		try:
			self.bq_client.get_table(table_ref)
			return True
		except Exception as e:
			return False

	def merge(self,
		   destination_dataset:str=None ,
		   destination_table:str=None, 
		   df:pd.DataFrame=None,
		   unique_keys=None,
		   schema=None,
		):
		self.logger.info(f"Start merge data to table: {destination_table}")
		destination_project_dataset = f"{self.project_id}.{destination_dataset}"
		destination_project_dataset_table = f"{destination_project_dataset}.{destination_table}"
		l = destination_project_dataset_table.split('.')
		staging_project_dataset_table = l[0] + '.staging.' + l[2]
		# insert data to staging table
		if schema is not None:
			job_stg_table_config = bigquery.LoadJobConfig(
				create_disposition='CREATE_IF_NEEDED',
				write_disposition="WRITE_TRUNCATE",
				schema=schema,
			)
		else:
			job_stg_table_config = bigquery.LoadJobConfig(
				create_disposition='CREATE_IF_NEEDED',
				write_disposition="WRITE_TRUNCATE",
				autodetect=True,
			)
		create_stg_table_job = self.bq_client.load_table_from_dataframe(
			df, staging_project_dataset_table, job_config=job_stg_table_config
		)
		create_stg_table_job.result()
		# build dml to merge data from staging table to destination table
		on_clause = self._build_on_clause(unique_keys)
		merge_dml = f"""declare cols string;
			set cols = (
			select
				string_agg(concat('t.', column_name, '=s.', column_name), ',')
			from
				`{destination_project_dataset}.INFORMATION_SCHEMA.COLUMNS`
			where
				table_name = '{destination_table}'
			);
			execute immediate format('''
				merge `{destination_project_dataset_table}` as t
				using `{staging_project_dataset_table}` as s
				on {on_clause}
				when not matched then insert row
				when matched then update set %s
				'''
				, cols
			);"""
		self.bq_client.query(merge_dml).result()
		self.logger.info(f"Merge DML: {merge_dml}")