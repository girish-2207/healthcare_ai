import sqlite3
import datetime


class ChatHistoryManager:
    def __init__(self, db_path: str = "database/medical.db"):
        self.db_path = db_path
        self._init_db()

    def _init_db(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS chat_history (
                id        INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id   TEXT NOT NULL,
                role      TEXT NOT NULL,
                message   TEXT NOT NULL,
                timestamp TEXT NOT NULL
            )
        """)
        conn.commit()
        conn.close()
        print("[ChatHistoryManager] DB ready")

    def get(self, user_id: str, last_n: int = 5) -> list:
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("""
            SELECT role, message FROM chat_history
            WHERE user_id = ?
            ORDER BY id DESC
            LIMIT ?
        """, (user_id, last_n * 2))
        rows = cursor.fetchall()
        conn.close()
        rows.reverse()
        return [{"role": r[0], "message": r[1]} for r in rows]

    def save(self, user_id: str, query: str, response: str):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        now = datetime.datetime.now().isoformat()
        cursor.executemany("""
            INSERT INTO chat_history (user_id, role, message, timestamp)
            VALUES (?, ?, ?, ?)
        """, [
            (user_id, "user",      query,    now),
            (user_id, "assistant", response, now),
        ])
        conn.commit()
        conn.close()

    def clear(self, user_id: str):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute(
            "DELETE FROM chat_history WHERE user_id = ?", (user_id,)
        )
        conn.commit()
        conn.close()
        print(f"[ChatHistoryManager] Cleared history: {user_id}")