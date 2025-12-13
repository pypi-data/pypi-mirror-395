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
    # ADD
    # ------------------------------------------------------
    def add(self, table, **kwargs):
        external_control = None

        if "Control" in kwargs:
            external_control = kwargs["Control"]
            kwargs.pop("Control")

        keys = ", ".join(kwargs.keys())
        values = ", ".join(["%s"] * len(kwargs))
        sql = f"INSERT INTO {table} ({keys}) VALUES ({values})"

        try:
            self.cursor.execute(sql, tuple(kwargs.values()))
            self.conn.commit()
            print("Added!")
            if external_control is not None:
                external_control.append(True)
            return True
        except mysql.connector.Error as e:
            print("Insert Error:", e)
            if external_control is not None:
                external_control.append(False)
            return False

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
            return True
        except mysql.connector.Error as e:
            print("Update Error:", e)
            if Control is not None:
                Control.append(False)
            return False

    # ------------------------------------------------------
    # DELETE
    # ------------------------------------------------------
    def delete(self, table, **kwargs):
        external_control = None

        if "Control" in kwargs:
            external_control = kwargs["Control"]
            kwargs.pop("Control")

        where_clause = " AND ".join([f"{k}=%s" for k in kwargs])
        sql = f"DELETE FROM {table} WHERE {where_clause}"

        try:
            self.cursor.execute(sql, tuple(kwargs.values()))
            self.conn.commit()
            print("Deleted!")
            if external_control is not None:
                external_control.append(True)
            return True
        except mysql.connector.Error as e:
            print("Delete Error:", e)
            if external_control is not None:
                external_control.append(False)
            return False

    # ------------------------------------------------------
    # GET (tek veri)
    # ------------------------------------------------------
    def get(self, table, **kwargs):
        external_var = None
        external_control = None

        if "Variable" in kwargs:
            external_var = kwargs["Variable"]
            kwargs.pop("Variable")

        if "Control" in kwargs:
            external_control = kwargs["Control"]
            kwargs.pop("Control")

        where_clause = " AND ".join([f"{k}=%s" for k in kwargs])
        sql = f"SELECT * FROM {table} WHERE {where_clause} LIMIT 1"

        try:
            self.cursor.execute(sql, tuple(kwargs.values()))
            row = self.cursor.fetchone()

            if row:
                if external_var is not None:
                    external_var.clear()
                    external_var.update(row)

                if external_control is not None:
                    external_control.append(True)

                print("Data found:", row)
                return row

            print("No data found.")
            if external_control is not None:
                external_control.append(False)
            return None

        except mysql.connector.Error as e:
            print("Get Error:", e)
            if external_control is not None:
                external_control.append(False)
            return None

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

    # ------------------------------------------------------
    # CONTROLL
    # db.Controll("Users", ID=3, name="Ali", Control=durum)
    # ------------------------------------------------------
    def Controll(self, table, **kwargs):
        external_control = None

        if "Control" in kwargs:
            external_control = kwargs["Control"]
            kwargs.pop("Control")

        filters = {}
        checks = {}

        for key, value in kwargs.items():
            if key.isupper():
                filters[key] = value
            else:
                checks[key] = value

        if not filters:
            print("Controll Error: ID gibi bir filtre gerekli.")
            if external_control is not None:
                external_control.append(False)
            return False

        where_clause = " AND ".join([f"{k}=%s" for k in filters])
        sql = f"SELECT * FROM {table} WHERE {where_clause} LIMIT 1"

        try:
            self.cursor.execute(sql, tuple(filters.values()))
            row = self.cursor.fetchone()

            if not row:
                print("Controll: Veri yok.")
                if external_control is not None:
                    external_control.append(False)
                return False

            for key, expected in checks.items():
                if key not in row or row[key] != expected:
                    print("Controll: Uyuşmayan değer:", key)
                    if external_control is not None:
                        external_control.append(False)
                    return False

            print("Controll: Doğru.")
            if external_control is not None:
                external_control.append(True)
            return True

        except mysql.connector.Error as e:
            print("Controll Error:", e)
            if external_control is not None:
                external_control.append(False)
            return False

# ------------------------------------------------------
    # ID_CONTROL
    # db.ID_Control("Users", name="Ali")
    # ÇIKTI: sadece ID veya None
    # ------------------------------------------------------
    def ID_Control(self, table, **kwargs):
        external_control = None

        # Control dışarıdan gelmişse al
        if "Control" in kwargs:
            external_control = kwargs["Control"]
            kwargs.pop("Control")

        filters = kwargs

        # Filtre yoksa
        if not filters:
            print("ID_Control Error: name gibi filtre gerekli.")
            if external_control is not None:
                external_control.append(False)
            return None

        # SQL hazırla
        where_clause = " AND ".join([f"{k}=%s" for k in filters])
        sql = f"SELECT ID FROM {table} WHERE {where_clause} LIMIT 1"

        try:
            self.cursor.execute(sql, tuple(filters.values()))
            row = self.cursor.fetchone()

            # Veri yoksa
            if not row:
                print("ID_Control: Veri yok.")
                if external_control is not None:
                    external_control.append(False)
                return None

            # Veri bulundu
            if external_control is not None:
                external_control.append(True)

            print("ID_Control: ID bulundu:", row["ID"])
            return row["ID"]   # 🔥 Yalnızca ID döner

        except mysql.connector.Error as e:
            print("ID_Control Error:", e)
            if external_control is not None:
                external_control.append(False)
            return None