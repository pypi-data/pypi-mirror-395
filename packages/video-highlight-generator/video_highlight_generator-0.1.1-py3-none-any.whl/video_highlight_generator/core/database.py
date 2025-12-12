import sqlite3
import json
import os
from typing import Dict, Any, Optional

class Database:
    def __init__(self, db_path: str = "video_highlight_generator.db"):
        self.db_path = db_path
        self._init_db()

    def _init_db(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Images table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS images (
                path TEXT PRIMARY KEY,
                score REAL,
                tags TEXT,
                faces TEXT,
                timestamp REAL
            )
        ''')
        
        # Persons table (for clustering)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS persons (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                face_encoding TEXT
            )
        ''')
        
        conn.commit()
        conn.close()

    def get_image_data(self, path: str) -> Optional[Dict[str, Any]]:
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT score, tags, faces FROM images WHERE path = ?", (path,))
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return {
                "score": row[0],
                "tags": json.loads(row[1]),
                "faces": json.loads(row[2])
            }
        return None

    def save_image_data(self, path: str, score: float, tags: list, faces: list):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT OR REPLACE INTO images (path, score, tags, faces, timestamp)
            VALUES (?, ?, ?, ?, ?)
        ''', (path, score, json.dumps(tags), json.dumps(faces), os.path.getmtime(path)))
        conn.commit()
        conn.close()

    def get_images_batch(self, paths: list) -> Dict[str, Dict[str, Any]]:
        if not paths:
            return {}
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # SQLite has a limit on variables, so we might need to chunk if paths is huge
        # But for typical usage < 999 is fine. 
        # To be safe, let's just fetch all and filter in python or use chunks.
        # Simplest for now: Fetch all images that match.
        
        placeholders = ','.join(['?'] * len(paths))
        query = f"SELECT path, score, tags, faces FROM images WHERE path IN ({placeholders})"
        
        try:
            cursor.execute(query, paths)
            rows = cursor.fetchall()
            results = {}
            for row in rows:
                results[row[0]] = {
                    "score": row[1],
                    "tags": json.loads(row[2]),
                    "faces": json.loads(row[3])
                }
            return results
        except sqlite3.OperationalError:
            # Fallback for too many variables: chunk it
            results = {}
            chunk_size = 900
            for i in range(0, len(paths), chunk_size):
                chunk = paths[i:i + chunk_size]
                placeholders = ','.join(['?'] * len(chunk))
                query = f"SELECT path, score, tags, faces FROM images WHERE path IN ({placeholders})"
                cursor.execute(query, chunk)
                for row in cursor.fetchall():
                    results[row[0]] = {
                        "score": row[1],
                        "tags": json.loads(row[2]),
                        "faces": json.loads(row[3])
                    }
            return results
        finally:
            conn.close()

    def save_images_batch(self, data_list: list):
        # data_list is list of tuples: (path, score, tags, faces)
        if not data_list:
            return
            
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        formatted_data = []
        for item in data_list:
            path, score, tags, faces = item
            formatted_data.append((path, score, json.dumps(tags), json.dumps(faces), os.path.getmtime(path)))
            
        cursor.executemany('''
            INSERT OR REPLACE INTO images (path, score, tags, faces, timestamp)
            VALUES (?, ?, ?, ?, ?)
        ''', formatted_data)
        
        conn.commit()
        conn.close()
