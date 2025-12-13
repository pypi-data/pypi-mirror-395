import boto3
from requests_aws4auth import AWS4Auth
from elasticsearch import Elasticsearch
from opensearchpy import OpenSearch, RequestsHttpConnection
from inception_audittrail_logger.settings_audittrail import get_audittrail_setting

audittrail_setting = get_audittrail_setting()
AUDITTRAIL_INDEX_NAME = "audittrail"
SYSTEM_ERROR_INDEX_NAME = "system_error"


# Connect to ES
def es_connect():
    # Connect to ES
    if audittrail_setting.elasticsearch_provider == "aws":
        # Get AWS credentials
        awsauth = AWS4Auth(
            audittrail_setting.elasticsearch_aws_access_key,
            audittrail_setting.elasticsearch_aws_secret_key,
            audittrail_setting.aws_region,
            audittrail_setting.elasticsearch_service,
        )

        es = OpenSearch(
            hosts=[
                {
                    "host": audittrail_setting.elasticsearch_host.split("//")[1],
                    "port": audittrail_setting.elasticsearch_port,
                }
            ],
            http_auth=awsauth,
            use_ssl=True,
            verify_certs=audittrail_setting.elasticsearch_verify_certs,
            connection_class=RequestsHttpConnection,
        )
    elif audittrail_setting.elasticsearch_provider == "self-hosted":
        es = Elasticsearch(
            [
                f"{audittrail_setting.elasticsearch_host}:{audittrail_setting.elasticsearch_port}"
            ],
            verify_certs=audittrail_setting.elasticsearch_verify_certs,
        )
    return es


# ✅ Confirm connection
if audittrail_setting.elasticsearch_host and audittrail_setting.elasticsearch_port:
    es = es_connect()
    if es.ping():
        print("✅ Successfully connected to Audittrail Elasticsearch!")
    else:
        print("❌ Failed to connect to Audittrail Elasticsearch.")
else:
    print("❌ Elasticsearch host or port is not set.")


async def index_document(index_name: str, document_id: str, body: dict):
    if audittrail_setting.elasticsearch_provider == "aws":
        response = es.index(index=index_name, id=document_id, body=body)
        print(f"✅ Successfully indexed document into Elasticsearch: {document_id}")
        return response
    elif audittrail_setting.elasticsearch_provider == "self-hosted":
        response = es.index(index=index_name, id=document_id, document=body)
        print(f"✅ Successfully indexed document into Elasticsearch: {document_id}")
        return response
    else:
        raise ValueError("Invalid Elasticsearch provider")


async def search_es_documents(index_name: str, query: dict):
    if audittrail_setting.elasticsearch_provider == "aws":
        response = es.search(index=index_name, body=query)
    elif audittrail_setting.elasticsearch_provider == "self-hosted":
        response = es.search(index=index_name, body=query)
    else:
        raise ValueError("Invalid Elasticsearch provider")
    print(f"✅ Successfully searched Elasticsearch: {response}")
    return response


def get_audittrail_es_client() -> Elasticsearch:
    return es
