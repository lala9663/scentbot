import psycopg2
import os
import json
from services.embedding_service import get_embedding


def get_connection():
    return psycopg2.connect(
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
    )

def search_perfume_by_name(name: str):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT name, description
        FROM perfume
        WHERE name ILIKE %s
        LIMIT 1
    """, (f"%{name}%",))

    result = cur.fetchone()

    cur.close()
    conn.close()

    if result:
        return {"name": result[0], "description": result[1]}
    return None

def search_similar_perfumes(query: str):
    conn = get_connection()
    cur = conn.cursor()

    embedding = get_embedding(query)

    # 🔥 핵심: 문자열로 변환
    embedding_str = "[" + ",".join(map(str, embedding)) + "]"

    cur.execute("""
        SELECT name, description
        FROM perfume
        ORDER BY embedding <-> %s::vector
        LIMIT 5;
    """, (embedding_str,))

    results = cur.fetchall()

    cur.close()
    conn.close()

    return [
        {"name": r[0], "description": r[1]}
        for r in results
    ]

def save_perfume(data: dict):
    conn = get_connection()
    cur = conn.cursor() 
    
    name = data.get("name")
    description = data.get("description", "")
    notes = data.get("notes", {})

    embedding_text = description + " " + " ".join(
        notes.get("top", []) +
        notes.get("middle", []) +
        notes.get("base", [])
    )

    embedding = get_embedding(embedding_text)
    embedding_str = "[" + ",".join(map(str, embedding)) + "]"

    cur.execute("""
        INSERT INTO perfume (name, description, notes, embedding)
        VALUES (%s, %s, %s, %s::vector)
    """, (name, description, json.dumps(notes), embedding_str))

    conn.commit()
    cur.close()
    conn.close()