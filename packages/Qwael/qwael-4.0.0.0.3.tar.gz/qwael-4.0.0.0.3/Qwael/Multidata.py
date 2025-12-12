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
        Control = kwargs.pop("Control", None)

        keys = ", ".join(kwargs.keys())
        values = ", ".join(["%s"] * len(kwargs))
        sql = f"INSERT INTO {table} ({keys}) VALUES ({values})"

        try:
            self.cursor.execute(sql, tuple(kwargs.values()))
            self.conn.commit()
            print("Added!")

            if Control is not None:
                Control.append(True)

        except mysql.connector.Error as e:
            print("Insert Error:", e)

            if Control is not None:
                Control.append(False)

    # ------------------------------------------------------
    # UPDATE
    # ------------------------------------------------------
    def update(self, table, where: dict, data: dict, Control=None):
        set_clause = ", ".join([f"{k}=%s" for k in data])
        where_clause = " AND ".join([f"{k}=%s" for k in where])

        values = list(data.values()) + list(where.values())
        sql = f"UPDATE {table} SET {set_clause} WHERE {where_clause}"

        try:
            self.cursor.execute(sql, values)
            self.conn.commit()
            print("Updated!")

            if Control is not None:
                Control.append(True)

        except mysql.connector.Error as e:
            print("Update Error:", e)

            if Control is not None:
                Control.append(False)

    # ------------------------------------------------------
    # DELETE
    # ------------------------------------------------------
    def delete(self, table, Control=None, **kwargs):
        where_clause = " AND ".join([f"{k}=%s" for k in kwargs])
        sql = f"DELETE FROM {table} WHERE {where_clause}"

        try:
            self.cursor.execute(sql, tuple(kwargs.values()))
            self.conn.commit()
            print("Deleted!")

            if Control is not None:
                Control.append(True)

        except mysql.connector.Error as e:
            print("Delete Error:", e)

            if Control is not None:
                Control.append(False)

    # ------------------------------------------------------
    # GET (tek veri)
    # ------------------------------------------------------
    def get(self, table, Control=None, **kwargs):
        external_var = None

        # Variable parametresini dışarı al
        if "Variable" in kwargs:
            external_var = kwargs["Variable"]
            kwargs.pop("Variable")

        where_clause = " AND ".join([f"{k}=%s" for k in kwargs])
        sql = f"SELECT * FROM {table} WHERE {where_clause} LIMIT 1"

        try:
            self.cursor.execute(sql, tuple(kwargs.values()))
            row = self.cursor.fetchone()

            if row:
                if external_var is not None:
                    external_var.clear()
                    external_var.update(row)

                print("Data found:", row)

                if Control is not None:
                    Control.append(True)

                return row

            print("No data found.")

            if Control is not None:
                Control.append(False)

            return None

        except mysql.connector.Error as e:
            print("Get Error:", e)

            if Control is not None:
                Control.append(False)

    # ------------------------------------------------------
    # GET ALL
    # ------------------------------------------------------
    def get_all(self, table, Control=None):
        sql = f"SELECT * FROM {table}"

        try:
            self.cursor.execute(sql)
            rows = self.cursor.fetchall()

            if Control is not None:
                Control.append(True)

            return rows

        except mysql.connector.Error as e:
            print("Get All Error:", e)

            if Control is not None:
                Control.append(False)

            return []