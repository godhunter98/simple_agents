import os
import json
import psycopg

databse_url = os.getenv("DATABASE_URL","postgresql://agents:agents@localhost:5432/agents")

def log_interaction(query:str, response:str,tools:list| None):
    with psycopg.connect(databse_url) as conn:
        conn.execute(
            """
            INSERT INTO interactions (query, response, tools)
            VALUES (%s, %s, %s)
            """,
            (query, response, json.dumps(tools) if tools else None),
        )
        conn.commit()
