import sqlite3,sys
from tqdm import tqdm
from .Notes import Note
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))

global file_path
file_path = "xhs_tesla_notes.db"


def init_db(database_name):
    conn = sqlite3.connect(f"{database_name}")
    cursor = conn.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS notes (
            id TEXT PRIMARY KEY,
            type TEXT,
            likes INTEGER,
            title TEXT,
            user_name TEXT,
            create_time INTEGER,
            Year INTEGER,
            Month INTEGER,
            Day INTEGER,
            Hour INTEGER,
            image_count INTEGER,
            content TEXT,
            first_category TEXT,
            second_category TEXT
        )
    """
    )
    conn.commit()
    conn.close()


def insert_data(conn, cursor, notes):
    for note in notes:
        try:
            cursor.execute(
                """
                INSERT INTO notes (id, type, likes, title, user_name, Year, Month, Day, Hour, create_time, image_count, content, second_category)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
                (
                    note.id,
                    note.type,
                    note.likes,
                    note.title,
                    note.user_name,
                    note.Year,
                    note.Month,
                    note.Day,
                    note.Hour,
                    note.create_time,
                    note.image_count,
                    note.content,
                    note.category,
                ),
            )
        except Exception as e:
            print("Error inserting note:", e)
            # You can choose to log the error or handle it as needed

    conn.commit()


def update_db(database_name):
    conn = sqlite3.connect(f"{database_name}")
    cursor = conn.cursor()
    cursor.execute(
        """
                    ALTER TABLE 
                    notes
                    ADD COLUMN 
                    Day INTEGER;
        """,
    )
    conn.commit()
    conn.close()


def get_latest_cursor_pid(database):
    conn = sqlite3.connect(database)
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT cursor 
        FROM notes 
        ORDER BY create_time ASC 
        LIMIT 1
    """
    )
    latest_cursor = cursor.fetchone()
    cursor.execute(
        """
        SELECT id 
        FROM notes 
        ORDER BY create_time ASC 
        LIMIT 1
    """
    )
    latest_pid = cursor.fetchone()
    cursor.execute(
        """
        SELECT title 
        FROM notes 
        ORDER BY create_time ASC 
        LIMIT 1
    """
    )
    latest_title = cursor.fetchone()
    conn.commit()
    conn.close()
    return latest_cursor[0], latest_pid[0], latest_title[0]


def fill_blank_content():
    try:
        conn = sqlite3.connect(file_path)
        cursor = conn.cursor()

        query = "SELECT * FROM notes WHERE content  = '' LIMIT 10"
        cursor.execute(query)
        notes_null_content = cursor.fetchall()

        for note in tqdm(notes_null_content):
            try:
                null_con = Note(
                    note[0], note[1], note[2], note[3], note[4], note[5], note[10]
                )
                # print(f'Filling content for note with id {null_con.id}')
                content = null_con.get_content()
                print(f"Obtained content: {content}")

                update_query = "UPDATE notes SET content = ? WHERE id = ?"
                cursor.execute(update_query, (content, null_con.id))
                conn.commit()
                # print(f'Successfully filled content for note with id {null_con.id}')

            except Exception as inner_exc:
                print(f"Error processing note with id {note[0]}: {inner_exc}")

    except Exception as outer_exc:
        print(f"Error connecting to the database: {outer_exc}")

    finally:
        conn.close()
