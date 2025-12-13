import os
import json
import time

# --- KIVY ANDROID DOSYA DESTEĞİ EKLENDİ ---
try:
    from kivy.utils import platform
    from kivy.app import App
except:
    platform = None
# ------------------------------------------


class MultiDB:
    def __init__(self, filename="database.mdb"):

        # --- Android için doğru klasör ayarı ---
        if platform == "android":
            app = App.get_running_app()

            if app:
                # App çalışıyorsa user_data_dir kullan
                filename = os.path.join(app.user_data_dir, filename)
            else:
                # App başlamamışsa geçici güvenli klasör
                filename = os.path.join(os.getcwd(), filename)
        # ---------------------------------------

        self.filename = filename
        self.lockfile = filename + ".lock"

        if not os.path.exists(self.filename):
            with open(self.filename, "w", encoding="utf-8") as f:
                f.write("")

    # -----------------------------
    # LOCK SYSTEM
    # -----------------------------
    def _lock(self):
        while os.path.exists(self.lockfile):
            time.sleep(0.05)

        with open(self.lockfile, "w") as f:
            f.write("locked")

    def _unlock(self):
        if os.path.exists(self.lockfile):
            try:
                os.remove(self.lockfile)
            except Exception:
                pass

    # -----------------------------
    # FILE I/O
    # -----------------------------
    def _read(self):
        with open(self.filename, "r", encoding="utf-8") as f:
            return f.read().splitlines()

    def _write(self, lines):
        with open(self.filename, "w", encoding="utf-8") as f:
            f.write("\n".join(lines))

    # -----------------------------
    # TABLE FINDER
    # -----------------------------
    def _find_table(self, lines, table):
        for i, line in enumerate(lines):
            if line.strip() == f"[TABLE {table}]":
                return i
        return -1

    # -----------------------------
    # RULE SPLITTER (25 LIMIT)
    # -----------------------------
    def _split_rules(self, rule):
        if not rule:
            return []

        rule = rule.replace(" ", "").replace("+", ",").replace("#-", ",#-")
        rules = [r for r in rule.split(",") if r]

        if len(rules) > 25:
            raise ValueError("Bir sütun için maksimum 25 kural eklenebilir!")

        return rules

    # -----------------------------
    # CREATE TABLE
    # -----------------------------
    def create_table(self, name, columns):
        self._lock()
        try:
            lines = self._read()

            if self._find_table(lines, name) != -1:
                raise ValueError("Bu tablo zaten var!")

            col_names = []
            rules = {}

            for col in columns:
                if isinstance(col, dict):
                    key = list(col.keys())[0]
                    rule = col[key]
                    col_names.append(key)
                    rules[key] = rule
                else:
                    col_names.append(col)
                    rules[col] = ""

            lines.append(f"[TABLE {name}]")
            lines.append(json.dumps(col_names, ensure_ascii=False))
            lines.append(json.dumps(rules, ensure_ascii=False))

            self._write(lines)
        finally:
            self._unlock()

    # -----------------------------
    # VALIDATION
    # -----------------------------
    def _validate(self, value, rule, lines, table_pos, col_index):
        rules = self._split_rules(rule)

        for r in rules:
            if r == "ID":
                continue

            if r == "number":
                if not value.isdigit():
                    return False

            if r == "gmail":
                if not ("@" in value and value.endswith(".com")):
                    return False

            if r == "big":
                if not all(ch.isupper() or ch.isdigit() for ch in value):
                    return False

            if r == "small":
                if not all(ch.islower() or ch.isdigit() or ch in "@." for ch in value):
                    return False

            if r == "#-":
                idx = table_pos + 3
                while idx < len(lines) and not lines[idx].startswith("[TABLE"):
                    row = json.loads(lines[idx])
                    if row[col_index] == value:
                        return False
                    idx += 1

        return True

    # -----------------------------
    # GIVE (DEĞİŞKEN DESTEKLİ)
    # -----------------------------
    def give(self, table, values, output_list=None):
        if not isinstance(values, (list, tuple)):
            values = [values]

        self._lock()
        try:
            lines = self._read()

            tpos = self._find_table(lines, table)
            if tpos == -1:
                raise ValueError("Tablo bulunamadı!")

            col_names = json.loads(lines[tpos + 1])
            rules = json.loads(lines[tpos + 2])

            final_values = []

            # Eğer ID otomatik eklenecekse
            if len(values) + 1 == len(col_names) and "ID" in rules.values():
                auto_id = 1
                idx = tpos + 3
                while idx < len(lines) and not lines[idx].startswith("[TABLE"):
                    try:
                        row = json.loads(lines[idx])
                        # güvenli int dönüşümü: boş/bozuk değerleri atla
                        if isinstance(row[0], str) and row[0].isdigit():
                            auto_id = max(auto_id, int(row[0]) + 1)
                    except Exception:
                        # bozuk satır varsa atla
                        pass
                    idx += 1

                final_values.append(str(auto_id))
                final_values.extend(values)

            elif len(values) != len(col_names):
                raise ValueError("Gönderilen veri sayısı yanlış!")

            else:
                final_values = list(values)

            # validation
            for i, col in enumerate(col_names):
                rule = rules.get(col, "")
                # eğer final_values eksikse hatayı fırlat
                if i >= len(final_values):
                    raise ValueError("Eksik veri!")
                if not self._validate(final_values[i], rule, lines, tpos, i):
                    raise ValueError(f"{col} alanı için veri kurala uymuyor: {rule}")

            # insert
            lines.insert(tpos + 3, json.dumps(final_values, ensure_ascii=False))
            self._write(lines)

            if output_list is not None:
                output_list.append(True)

            return True

        except Exception:
            if output_list is not None:
                output_list.append(False)
                return False
            raise

        finally:
            self._unlock()

    # -----------------------------
    # READ FULL TABLE
    # -----------------------------
    def table_full(self, table):
        lines = self._read()
        tpos = self._find_table(lines, table)
        if tpos == -1:
            raise ValueError("Tablo yok!")

        result = []
        idx = tpos + 3
        while idx < len(lines) and not lines[idx].startswith("[TABLE"):
            result.append(json.loads(lines[idx]))
            idx += 1
        return result

    # -----------------------------
    # CLEAR DATA (onay-listesi uyumlu)
    # -----------------------------
    def clear_full(self, table, onay=None):
        """
        table: temizlenecek tablo adı
        onay: eğer bir liste verilirse, işlem başarılıysa onay.append(True),
              başarısızsa onay.append(False) yapılır.
        Fonksiyon ayrıca True/False döndürür (diğer fonksiyonlarla uyumlu).
        """
        self._lock()
        try:
            lines = self._read()
            tpos = self._find_table(lines, table)
            if tpos == -1:
                if isinstance(onay, list):
                    onay.append(False)
                return False

            new_lines = []
            i = 0
            while i < len(lines):
                if i != tpos:
                    new_lines.append(lines[i])
                    i += 1
                    continue

                # tablo başlığını koru
                new_lines.append(lines[i])
                new_lines.append(lines[i + 1])
                new_lines.append(lines[i + 2])

                # tablonun altındaki kayıtları atla
                j = i + 3
                while j < len(lines) and not lines[j].startswith("[TABLE"):
                    j += 1
                i = j

            self._write(new_lines)

            if isinstance(onay, list):
                onay.append(True)
            return True

        except Exception:
            if isinstance(onay, list):
                onay.append(False)
            raise

        finally:
            self._unlock()

    # -----------------------------
    # UPDATE TABLE
    # -----------------------------
    def table_update(self, table, columns):
        self._lock()
        try:
            lines = self._read()
            tpos = self._find_table(lines, table)
            if tpos == -1:
                raise ValueError("Böyle bir tablo yok!")

            col_names = []
            rules = {}
            for col in columns:
                if isinstance(col, dict):
                    key = list(col.keys())[0]
                    col_names.append(key)
                    rules[key] = col[key]
                else:
                    col_names.append(col)
                    rules[col] = ""

            data_rows = []
            idx = tpos + 3
            while idx < len(lines) and not lines[idx].startswith("[TABLE"):
                data_rows.append(json.loads(lines[idx]))
                idx += 1

            new_data_rows = []
            old_cols = json.loads(lines[tpos + 1])
            for row in data_rows:
                new_row = []
                for col in col_names:
                    if col in old_cols:
                        new_row.append(row[old_cols.index(col)])
                    else:
                        new_row.append("")
                new_data_rows.append(new_row)

            new_lines = []
            i = 0
            while i < len(lines):
                if i == tpos:
                    new_lines.append(f"[TABLE {table}]")
                    new_lines.append(json.dumps(col_names, ensure_ascii=False))
                    new_lines.append(json.dumps(rules, ensure_ascii=False))
                    for row in new_data_rows:
                        new_lines.append(json.dumps(row, ensure_ascii=False))

                    j = tpos + 3
                    while j < len(lines) and not lines[j].startswith("[TABLE"):
                        j += 1
                    i = j
                else:
                    new_lines.append(lines[i])
                    i += 1

            self._write(new_lines)
        finally:
            self._unlock()

    # -----------------------------
    # CONTROL SYSTEM
    # -----------------------------
    def control(self, table, conditions: dict, output_list=None):
        if not isinstance(conditions, dict):
            raise ValueError("control koşulları dict olmalı. Örnek: {'kod': değişken}")

        lines = self._read()
        tpos = self._find_table(lines, table)
        if tpos == -1:
            raise ValueError("Tablo bulunamadı!")

        col_names = json.loads(lines[tpos + 1])
        col_indexes = {k: col_names.index(k) for k in conditions}

        found = False
        idx = tpos + 3
        while idx < len(lines) and not lines[idx].startswith("[TABLE"):
            row = json.loads(lines[idx])
            match = all(row[col_indexes[k]] == v for k, v in conditions.items())
            if match:
                found = True
                break
            idx += 1

        if output_list is None:
            print("Var" if found else "Yok")
        else:
            output_list.append(found)

        return found

    # -----------------------------
    # FIND
    # -----------------------------
    def find(self, table, conditions: dict, output_list=None):
        if not isinstance(conditions, dict):
            raise ValueError("find koşulları dict olmalı. Örnek: {'mail': değişken}")

        lines = self._read()
        tpos = self._find_table(lines, table)
        if tpos == -1:
            raise ValueError("Tablo bulunamadı!")

        col_names = json.loads(lines[tpos + 1])
        col_indexes = {k: col_names.index(k) for k in conditions}

        found_id = None
        idx = tpos + 3

        while idx < len(lines) and not lines[idx].startswith("[TABLE"):
            row = json.loads(lines[idx])
            if all(row[col_indexes[k]] == v for k, v in conditions.items()):
                found_id = row[0]
                break
            idx += 1

        if output_list is not None:
            output_list.append(found_id)

        return found_id

    # -----------------------------
    # PULL
    # -----------------------------
    def pull(self, row_id, columns: dict, output_list=None):

        if not isinstance(columns, dict):
            columns = {columns: None}

        lines = self._read()

        col_name = list(columns.keys())[0]

        tpos = -1
        for i, line in enumerate(lines):
            if line.startswith("[TABLE"):
                col_names = json.loads(lines[i + 1])
                if col_name in col_names:
                    tpos = i
                    break

        if tpos == -1:
            raise ValueError("Bu sütun hiçbir tabloda bulunamadı!")

        col_index = col_names.index(col_name)

        idx = tpos + 3
        found_value = None

        while idx < len(lines) and not lines[idx].startswith("[TABLE"):
            row = json.loads(lines[idx])
            if row[0] == str(row_id):
                found_value = row[col_index]
                break
            idx += 1

        if output_list is not None:
            output_list.append(found_value)

        return found_value

    # -----------------------------
    # REMOVE / DELETE ROW
    # -----------------------------
    def remove(self, table, row_id, output_list=None):
        self._lock()
        try:
            lines = self._read()

            tpos = self._find_table(lines, table)
            if tpos == -1:
                raise ValueError("Tablo bulunamadı!")

            new_lines = []
            removed = False

            idx = 0
            while idx < len(lines):
                # tabloyu bulduk
                if idx == tpos:
                    new_lines.append(lines[idx])       # [TABLE ...]
                    new_lines.append(lines[idx + 1])   # columns
                    new_lines.append(lines[idx + 2])   # rules

                    j = idx + 3
                    # tablonun satırlarını dönen döngü
                    while j < len(lines) and not lines[j].startswith("[TABLE"):
                        row = json.loads(lines[j])
                        if row[0] != str(row_id):
                            new_lines.append(lines[j])
                        else:
                            removed = True
                        j += 1

                    idx = j
                    continue

                new_lines.append(lines[idx])
                idx += 1

            self._write(new_lines)

            if output_list is not None:
                output_list.append(removed)

            return removed

        except Exception:
            if output_list is not None:
                output_list.append(False)
            raise

        finally:
            self._unlock()

    # -----------------------------
    # ROMEVE - Tek tablo veya tüm tabloların verilerini temizle
    # -----------------------------
    def romeve(self, table_or_full, onay=None):
        """
        Kullanım:
        x.romeve("kullanıcı", onay)  -> sadece belirtilen tabloyu temizler (onay listesi varsa append eder)
        x.romeve(full_var, onay)     -> eğer table_or_full str değilse tüm tablolar temizlenir
        (not: burada 'full' özel bir isim değil; str değilse 'tüm' olarak kabul edilir)
        """
        # TEK TABLO ise
        if isinstance(table_or_full, str):
            return self.clear_full(table_or_full, onay)

        # TÜM TABLOLAR ise
        try:
            lines = self._read()
            tables = []
            for line in lines:
                if line.startswith("[TABLE "):
                    name = line.replace("[TABLE ", "").replace("]", "")
                    tables.append(name)

            success = True
            for t in tables:
                res = self.clear_full(t, onay=None)  # tek tek temizle, fakat onay append'ini biz sonradan yapacağız
                if not res:
                    success = False

            if isinstance(onay, list):
                onay.append(success)

            return success

        except Exception:
            if isinstance(onay, list):
                onay.append(False)
            raise