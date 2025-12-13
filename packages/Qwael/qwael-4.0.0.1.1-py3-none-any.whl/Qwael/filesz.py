import os, json

class EasyDB:
    def __init__(self, name):
        os.makedirs("easydb_data", exist_ok=True)
        self.path = f"easydb_data/{name}.json"
        if not os.path.exists(self.path):
            with open(self.path, "w", encoding="utf-8") as f:
                json.dump({}, f)
        self._safe_load()

    def _safe_load(self):
        try:
            with open(self.path, "r", encoding="utf-8") as f:
                text = f.read().strip()
                self.data = json.loads(text) if text else {}
        except Exception:
            print(f"[Uyarı] {self.path} bozuktu, sıfırdan oluşturuldu.")
            self.data = {}
            self._save()

    def _save(self):
        with open(self.path, "w", encoding="utf-8") as f:
            json.dump(self.data, f, indent=2, ensure_ascii=False)

    def create(self, table):
        if table not in self.data:
            self.data[table] = []
            self._save()
        return self

    def _value_conflict(self, table, value):
        is_special = isinstance(value, str) and value.startswith("'") and value.endswith("'")
        val_clean = value.strip("'") if is_special else value

        for item in self.data.get(table, []):
            for v in item.values():
                if not isinstance(v, str):
                    continue
                v_special = v.startswith("'") and v.endswith("'")
                v_clean = v.strip("'") if v_special else v

                # Aynı özel tekrar edemez
                if is_special and v_special and v_clean == val_clean:
                    return True
                # Normal ↔ özel çakışması
                if (is_special and not v_special or not is_special and v_special) and v_clean == val_clean:
                    return True
        return False

    def add(self, table, record: dict):
        if table not in self.data:
            self.create(table)

        for key, value in record.items():
            if isinstance(value, str) and self._value_conflict(table, value):
                print(f"[Uyarı] {value} çakışma nedeniyle eklenmedi.")
                return None

        record["id"] = len(self.data[table]) + 1
        self.data[table].append(record)
        self._save()
        return record["id"]

    def all(self, table):
        return self.data.get(table, [])

    def find(self, table, **filters):
        result = []
        for item in self.data.get(table, []):
            if all(item.get(k) == v for k, v in filters.items()):
                result.append(item)
        return result

    # 🔹 Yeni: ID bazlı silme
    def delete(self, table, record_id, field=None):
        if table not in self.data:
            print(f"[Hata] '{table}' tablosu yok.")
            return 0

        for item in self.data[table]:
            if item.get("id") == record_id:
                if field is None:
                    self.data[table].remove(item)
                    print(f"[Silindi] ID {record_id} tamamen silindi.")
                else:
                    if field in item:
                        print(f"[Silindi] ID {record_id} kaydındaki '{field}' alanı silindi.")
                        del item[field]
                self._save()
                return 1

        print(f"[Uyarı] ID {record_id} bulunamadı.")
        return 0

    # 🔹 Yeni: ID bazlı güncelleme
    def update(self, table, record_id, **updates):
        if table not in self.data:
            print(f"[Hata] '{table}' tablosu yok.")
            return 0

        for item in self.data[table]:
            if item.get("id") == record_id:
                item.update(updates)
                self._save()
                print(f"[Güncellendi] ID {record_id} başarıyla güncellendi.")
                return 1

        print(f"[Uyarı] ID {record_id} bulunamadı.")
        return 0
