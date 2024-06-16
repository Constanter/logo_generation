import psycopg2
import time
from .config import DB_CONFIG


def wait_for_db():
    """
    Wait for the database to be available.
    """
    while True:
        try:
            conn = psycopg2.connect(**DB_CONFIG)
            conn.close()
            print("Database is available.")
            break
        except Exception as e:
            print(f"Database not available yet, waiting... Error: {e}")
            time.sleep(5)


def create_tables():
    """
    Create the interactions and marked_images tables if they don't exist.
    """
    wait_for_db()
    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS interactions (
            id SERIAL PRIMARY KEY,
            user_id VARCHAR(255),
            image_url VARCHAR(255),
            metadata JSONB  -- Add metadata column with JSONB type
        );
    """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS marked_images (
            id SERIAL PRIMARY KEY,
            user_id VARCHAR(255),
            image_url VARCHAR(255),
            result BOOLEAN
        );
    """)
    conn.commit()
    cur.close()
    conn.close()

    
def get_marked_images() -> list[tuple[str, str, bool]]:
    """
    Fetch all marked images from the database.

    Returns
    -------
    list[tuple[str, str, bool]]
        A list of tuples containing the user ID, image URL, and result.
    """
    wait_for_db() 
    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()
    cur.execute("SELECT * FROM marked_images")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows


def store_interaction(user_id: str, image_url: str, metadata: str):
    """
    Store an interaction in the database.
    """
    wait_for_db()
    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()
    cur.execute("INSERT INTO interactions (user_id, image_url, metadata) VALUES (%s, %s, %s)", (user_id, image_url, metadata))
    conn.commit()
    cur.close()
    conn.close()


def mark_image(user_id: str, image_url: str, result: bool):
    """
    Mark an image as marked in the database.
    """
    wait_for_db()  
    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()
    cur.execute("INSERT INTO marked_images (user_id, image_url, result) VALUES (%s, %s, %s)", (user_id, image_url, result))
    conn.commit()
    cur.close()
    conn.close()


def fetch_marked_images() -> list[tuple[str, str, bool]]:
    """
    Fetches marked images from the database.
    
    Returns
    -------
    list[tuple[str, str, bool]]
        A list of tuples containing the user ID, image URL, and result.
    """
    wait_for_db() 
    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()
    cur.execute("SELECT * FROM marked_images")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows
