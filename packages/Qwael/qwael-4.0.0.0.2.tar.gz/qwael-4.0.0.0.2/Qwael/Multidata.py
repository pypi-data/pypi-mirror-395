import mysql.connector

class Admin:
    def __init__(self, IP, name, password, file_name, port=3306):
        self.host = IP
        self.user = name
        self.password = password
        self.database = file_name
        self.port = port

        try:
            self.conn = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database,
                port=self.port
            )
            self.cursor = self.conn.cursor(dictionary=True)
            print("Database connected!")
        except mysql.connector.Error as e:
            print("Connection Error:", e)

    # ------------------------------------------------------
    # INSERT (db.add)
    # ------------------------------------------------------
    def add(self, table, **kwargs):
        keys = ", ".join(kwargs.keys())
        values = ", ".join(["%s"] * len(kwargs))
        sql = f"INSERT INTO {table} ({keys}) VALUES ({values})"

        try:
            self.cursor.execute(sql, tuple(kwargs.values()))
            self.conn.commit()
            print("Added!")
        except mysql.connector.Error as e:
            print("Insert Error:", e)

    # ------------------------------------------------------
    # UPDATE (db.update("users", {"ID": 3}, {"name": "Ali"}))
    # ------------------------------------------------------
    def update(self, table, where: dict, data: dict):
        set_clause = ", ".join([f"{k}=%s" for k in data])
        where_clause = " AND ".join([f"{k}=%s" for k in where])

        values = list(data.values()) + list(where.values())
        sql = f"UPDATE {table} SET {set_clause} WHERE {where_clause}"

        try:
            self.cursor.execute(sql, values)
            self.conn.commit()
            print("Updated!")
        except mysql.connector.Error as e:
            print("Update Error:", e)

    # ------------------------------------------------------
    # DELETE (db.delete("users", ID=3))
    # ------------------------------------------------------
    def delete(self, table, **kwargs):
        where_clause = " AND ".join([f"{k}=%s" for k in kwargs])
        sql = f"DELETE FROM {table} WHERE {where_clause}"

        try:
            self.cursor.execute(sql, tuple(kwargs.values()))
            self.conn.commit()
            print("Deleted!")
        except mysql.connector.Error as e:
            print("Delete Error:", e)

    # ------------------------------------------------------
    # GET (tek veri) — db.get("users", ID=3, Variable=veri)
    # ------------------------------------------------------
    def get(self, table, **kwargs):
        external_var = None

        # Variable parametresini dışarı al
        if "Variable" in kwargs:
            external_var = kwargs["Variable"]
            kwargs.pop("Variable")  # filtrelerden çıkar

        # WHERE oluştur
        where_clause = " AND ".join([f"{k}=%s" for k in kwargs])
        sql = f"SELECT * FROM {table} WHERE {where_clause} LIMIT 1"

        try:
            self.cursor.execute(sql, tuple(kwargs.values()))
            row = self.cursor.fetchone()

            if row:
                # Variable={} gönderilmişse doldur
                if external_var is not None:
                    external_var.clear()
                    external_var.update(row)

                print("Data found:", row)
                return row

            print("No data found.")
            return None

        except mysql.connector.Error as e:
            print("Get Error:", e)

    # ------------------------------------------------------
    # GET ALL (db.get_all("users"))
    # ------------------------------------------------------
    def get_all(self, table):
        sql = f"SELECT * FROM {table}"

        try:
            self.cursor.execute(sql)
            rows = self.cursor.fetchall()
            return rows
        except mysql.connector.Error as e:
            print("Get All Error:", e)
            return []