"""Module to publish models to docdb"""

import csv
import os
from typing import Iterator, List

from aind_data_access_api.document_db import Client as DocDBClient
from requests import HTTPError

DOCDB_HOST = os.getenv("DOCDB_HOST")
DOCDB_DATABASE = os.getenv("DOCDB_DATABASE")
DOCDB_COLLECTION = os.getenv("DOCDB_COLLECTION")

PATH_TO_MODELS = os.getenv("PATH_TO_MODELS")
AWS_DEFAULT_REGION = os.getenv("AWS_DEFAULT_REGION")


def csv_to_json(csv_file_path: str) -> Iterator:
    """
    Returns Iterator of dict
    """
    with open(csv_file_path, mode="r", encoding="utf-8") as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            yield row


def get_csv_paths(folder_path: str) -> List[str]:
    """Parse a folder and return a list of csv file paths"""
    file_paths = list()
    for file_name in os.listdir(folder_path):
        if file_name.endswith(".csv"):
            file_paths.append(os.path.join(folder_path, file_name))
    return file_paths


def publish_to_docdb(file_paths: List[str], docdb_client: DocDBClient) -> None:
    """
    Writes each csv file as one record in docdb. Assumes file size does not
    exceed API gateway and DocDB limits.
    """
    for file_path in file_paths:
        file_name = os.path.basename(file_path)
        print(f"Processing file: {file_name}")
        csv_contents = list(csv_to_json(file_path))
        record = {
            "_id": file_name.removesuffix(".csv"),
            "file_name": file_name,
            "count": len(csv_contents),
            "contents": csv_contents,
        }
        print(f"Upserting {file_name} contents to docdb")
        response = docdb_client.upsert_one_docdb_record(record=record)
        print(response.json())


def remove_unmatched_records(file_paths: List[str], docdb_client: DocDBClient) -> None:
    """
    Deletes records in docdb that do not correspond to any csv files.
    """
    ids_from_csvs = {os.path.basename(fp).removesuffix(".csv") for fp in file_paths}

    records = docdb_client.retrieve_docdb_records(projection={"_id": 1})
    ids_from_docdb = {record["_id"] for record in records}

    ids_to_delete = ids_from_docdb - ids_from_csvs
    print(f"Ids in DocDB with no corresponding CSV file: {ids_to_delete}")
    if ids_to_delete:
        print(f"Deleting {len(ids_to_delete)} records from DocDB")
        response = docdb_client.delete_many_records(data_asset_record_ids=list(ids_to_delete))
        print(response.json())


if __name__ == "__main__":
    file_paths = get_csv_paths(PATH_TO_MODELS)
    print(f"Found {len(file_paths)} csv files to process")

    docdb_client = DocDBClient(
        host=DOCDB_HOST,
        database=DOCDB_DATABASE,
        collection=DOCDB_COLLECTION,
    )
    try:
        publish_to_docdb(file_paths=file_paths, docdb_client=docdb_client)
        remove_unmatched_records(file_paths=file_paths, docdb_client=docdb_client)
    except HTTPError as error:
        print(f"HTTP error {error.response.status_code}: {error.response.text}")
        raise error
