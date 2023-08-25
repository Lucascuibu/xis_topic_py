import sqlite3, sys
from pathlib import Path
from . import Notes
from tqdm import tqdm


db_path = "database/xhs_tesla_notes.db"


def fill(db_path=db_path):
    blank_query = "SELECT COUNT(*) FROM notes WHERE content is ''"
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        amount = cursor.execute("SELECT COUNT(*) FROM notes").fetchone()[0]
        blank_amount = cursor.execute(blank_query).fetchone()[0]
        print(
            f"There are {amount} notes in the database, {blank_amount} of them have blank content, blank rate is {blank_amount/amount}"
        )

        blank_notes_query = cursor.execute(blank_query)
        notes_null_content = blank_notes_query.fetchall()
        # notes_null_content = []

        for note in tqdm(notes_null_content):
            try:
                null_con = Notes.Note(
                    note[0], note[1], note[2], note[3], note[4], note[5], note[10]
                )
                print(f'Filling content for note with id {null_con.id}')
                content = null_con.get_content()
                # print(f"Obtained content: {content}")

                update_query = "UPDATE notes SET content = ? WHERE id = ?"
                cursor.execute(update_query, (content, null_con.id))
                conn.commit()
                # print(f'Successfully filled content for note with id {null_con.id}')

            except Exception as inner_exc:
                print(f"Error processing note with id {note[0]}: {inner_exc}")

        New_blank_amount = cursor.execute(blank_query).fetchone()[0]
        print(
            f"{blank_amount-New_blank_amount} of them have been filled, blank_rate now is {New_blank_amount/amount} as {New_blank_amount} of {amount}"
        )

    except Exception as outer_exc:
        print(f"Error connecting to the database: {outer_exc}")

    finally:
        conn.commit()
        conn.close()
