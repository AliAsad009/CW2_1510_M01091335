import pandas as pd
from app.data.db import connect_database


def insert_ticket(id,title,priority,status,created_date=None):
    conn = connect_database()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO it_tickets
        (id, title, priority, status, created_date)
        VALUES (?, ?, ?, ?, ?)
    """, (id, title, priority, status, created_date))
    conn.commit()
    conn.close()


def get_all_tickets():
    conn = connect_database()
    df = pd.read_sql_query(
        "SELECT * FROM it_tickets ORDER BY id DESC",
        conn
    )
    conn.close()
    return df


def update_ticket_status(ticket_id, new_status):
    conn = connect_database()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE it_tickets SET status = ? WHERE ticket_id = ?",
        (new_status, ticket_id)
    )
    conn.commit()
    conn.close()


def delete_ticket(ticket_id):
    conn = connect_database()
    cursor = conn.cursor()
    cursor.execute(
        "DELETE FROM it_tickets WHERE ticket_id = ?",
        (ticket_id,)
    )
    conn.commit()
    conn.close()


class ITTicket:
    def __init__(self, ticket_id, title, status, priority, description, created_by, date):
        self.ticket_id = ticket_id
        self.title = title
        self.status = status
        self.priority = priority
        self.description = description
        self.created_by = created_by
        self.date = date

    def __str__(self):
        return f"IT Ticket: {self.title} (Status: {self.status}, Priority: {self.priority})"

    def save(self):
        conn = connect_database()
        cursor = conn.cursor()
        # Check if ticket exists
        cursor.execute("SELECT * FROM it_tickets WHERE id = ?", (self.ticket_id,))
        exists = cursor.fetchone()
        if exists:
            cursor.execute(
                "UPDATE it_tickets SET title = ?, status = ?, priority = ?, description = ?, created_by = ?, created_date = ? WHERE id = ?",
                (self.title, self.status, self.priority, self.description, self.created_by, self.date, self.ticket_id)
            )
        else:
            cursor.execute(
                "INSERT INTO it_tickets (id, title, status, priority, description, created_by, created_date) VALUES (?, ?, ?, ?, ?, ?, ?)",
                (self.ticket_id, self.title, self.status, self.priority, self.description, self.created_by, self.date)
            )
        conn.commit()
        conn.close()

    def update_status(self, new_status):
        conn = connect_database()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE it_tickets SET status = ? WHERE id = ?",
            (new_status, self.ticket_id)
        )
        conn.commit()
        conn.close()
        self.status = new_status

    def delete(self):
        conn = connect_database()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM it_tickets WHERE id = ?", (self.ticket_id,))
        conn.commit()
        conn.close()

    @classmethod
    def get_by_id(cls, ticket_id):
        conn = connect_database()
        cursor = conn.cursor()
        cursor.execute("SELECT id, title, status, priority, description, created_by, created_date FROM it_tickets WHERE id = ?", (ticket_id,))
        row = cursor.fetchone()
        conn.close()
        if row:
            return cls(*row)
        return None
