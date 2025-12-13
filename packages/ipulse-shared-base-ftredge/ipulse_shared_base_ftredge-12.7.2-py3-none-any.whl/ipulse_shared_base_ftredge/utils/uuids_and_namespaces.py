
import uuid
from typing import Optional

def company_seed_uuid() -> str:
    """
    Returns Future Edge Group's Seed UUID which was generated using:
    uuid.uuid5(uuid.NAMESPACE_DNS, "ftredge.com")
    """
    return "d0a97da8-66c8-5946-ab48-340ef927b0ff"


def generate_reproducible_uuid_for_namespace(namespace: uuid.UUID | str, seed_description: str, prefix:Optional[str]=None) -> str:
    """
    Generates a reproducible UUID based on the input namespace (UUID object or string) and seed_description.
    For reproducibility, ensure the same namespace and seed_description are used.
    """
    if isinstance(namespace, str):
        namespace = uuid.UUID(namespace)  # Convert string to uuid.UUID object
    if prefix:
        return f"{prefix}_{str(uuid.uuid5(namespace, seed_description))}"
    return str(uuid.uuid5(namespace, seed_description))


def fetch_namespaces_from_bigquery(project_id, namespace_dataset_id, namespace_table_id, bigquery_client, namespace_statuses=['ACTIVE']):
    """
    Fetches namespaces and their UUIDs from a BigQuery table based on specified statuses.   
    Args:
        project_id (str): GCP project ID.
        namespace_dataset_id (str): BigQuery dataset ID containing the namespaces table.
        namespace_table_id (str): BigQuery table ID containing the namespaces.
        bigquery_client: An initialized BigQuery client.
        namespace_statuses (list of str): List of statuses to filter namespaces. Default is ['ACTIVE'].
    Returns:
        dict: A dictionary mapping namespace names to their UUIDs.
    """

    statuses_str = "', '".join(namespace_statuses)
    where_condition=f"status IN ('{statuses_str}')"

    # Construct the query
    query = f"""
    SELECT 
        namespace_name,
        namespace_uuid
    FROM `{project_id}.{namespace_dataset_id}.{namespace_table_id}`
    WHERE {where_condition}
    ORDER BY namespace_name
    """
    
    try:
        # Execute query
        query_job = bigquery_client.query(query)
        results = query_job.result()
        
        # Convert to dictionary
        namespaces_dict = {}
        for row in results:
            namespaces_dict[row.namespace_name] = row.namespace_uuid
            
        return namespaces_dict
        
    except Exception as e:
        print(f"Error fetching namespaces from BigQuery: {e}")
        raise

