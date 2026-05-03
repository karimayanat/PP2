import psycopg2
from config import DB_CONFIG

class Database:
    def __init__(self):
        try:
            self.conn = psycopg2.connect(
                host=DB_CONFIG["host"],
                port=DB_CONFIG["port"],
                database=DB_CONFIG["database"],
                user=DB_CONFIG["user"],
                password=DB_CONFIG["password"]
            )
            self.cursor = self.conn.cursor()
            self.setup_tables()
        except Exception as e:
            print(e)
            raise
    
    def setup_tables(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS players (
                id SERIAL PRIMARY KEY,
                username VARCHAR(50) UNIQUE NOT NULL
            )
        """)
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS game_sessions (
                id SERIAL PRIMARY KEY,
                player_id INTEGER REFERENCES players(id),
                score INTEGER NOT NULL,
                level_reached INTEGER NOT NULL,
                played_at TIMESTAMP DEFAULT NOW()
            )
        """)
        self.conn.commit()
    
    def get_or_create_player(self, username):
        self.cursor.execute("SELECT id FROM players WHERE username = %s", (username,))
        result = self.cursor.fetchone()
        if result:
            return result[0]
        else:
            self.cursor.execute("INSERT INTO players (username) VALUES (%s) RETURNING id", (username,))
            player_id = self.cursor.fetchone()[0]
            self.conn.commit()
            return player_id
    
    def save_game_result(self, username, score, level_reached):
        player_id = self.get_or_create_player(username)
        self.cursor.execute("""
            INSERT INTO game_sessions (player_id, score, level_reached)
            VALUES (%s, %s, %s)
        """, (player_id, score, level_reached))
        
        self.conn.commit()
    
    def get_top_scores(self, limit=10):
        self.cursor.execute("""
            SELECT p.username, gs.score, gs.level_reached, gs.played_at
            FROM game_sessions gs
            JOIN players p ON gs.player_id = p.id
            ORDER BY gs.score DESC
            LIMIT %s
        """, (limit,))
        
        return self.cursor.fetchall()
    
    def get_personal_best(self, username):
        player_id = self.get_or_create_player(username)
        
        self.cursor.execute("""
            SELECT MAX(score)
            FROM game_sessions
            WHERE player_id = %s
        """, (player_id,))
        
        result = self.cursor.fetchone()
        return result[0] if result and result[0] else None
    
    def close(self):
        self.cursor.close()
        self.conn.close()