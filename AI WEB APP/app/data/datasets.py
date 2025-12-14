import pandas as pd
from app.data.db import connect_database


def insert_dataset(id,name,source,category,size):
    conn = connect_database()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO datasets_metadata
        (id,name,source,category,size)
        VALUES (?, ?, ?, ?, ?)
    """, (id,name,source,category,size))
    conn.commit()
    dataset_id = cursor.lastrowid
    conn.close()
    return dataset_id


def get_all_datasets():
    conn = connect_database()
    df = pd.read_sql_query(
        "SELECT * FROM datasets_metadata ORDER BY id DESC",
        conn
    )
    conn.close()
    return df

def update_dataset_category(dataset_id, new_category):
    conn = connect_database()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE datasets_metadata SET category = ? WHERE id = ?",
        (new_category, dataset_id)
    )
    conn.commit()
    conn.close()


def delete_dataset(dataset_id):
    conn = connect_database()
    cursor = conn.cursor()
    cursor.execute(
        "DELETE FROM datasets_metadata WHERE id = ?",
        (dataset_id,)
    )
    conn.commit()
    conn.close()

class Dataset:
	def __init__(self, dataset_id, name, size, source, category):
		self.dataset_id = dataset_id
		self.name = name
		self.size = size
		self.source = source
		self.category = category

	def __str__(self):
		return f"Dataset: {self.name} (Source: {self.source}, Category: {self.category})"