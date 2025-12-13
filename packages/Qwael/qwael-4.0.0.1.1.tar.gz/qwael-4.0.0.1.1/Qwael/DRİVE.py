import tkinter as tk
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload, MediaFileUpload, MediaIoBaseUpload
from PIL import Image, ImageTk
import io


def info():
        infoc = "Prihops: Sürüm 1.01"
        print(infoc)


def Control(ID, ge, dax=None, fop=None, es=None, os=None, girp=None, girpx=None, girp_header=None, girpx_header=None, dex_ID=None):
    import io
    from google.oauth2 import service_account
    from googleapiclient.discovery import build
    from googleapiclient.http import MediaIoBaseDownload

    creds = service_account.Credentials.from_service_account_info(es)
    service = build('drive', 'v3', credentials=creds)

    query = f"'{os}' in parents and name='{ID}'"
    results = service.files().list(q=query, fields="files(id)").execute()
    files = results.get('files', [])

    if not files:
        print(f"{ID} dosyası bulunamadı.")
        if isinstance(fop, list):
            fop.append(False)
        return

    file_id = files[0]['id']
    request = service.files().get_media(fileId=file_id)
    file_io = io.BytesIO()
    downloader = MediaIoBaseDownload(file_io, request)
    done = False
    while not done:
        _, done = downloader.next_chunk()

    content = file_io.getvalue().decode('utf-8')
    lines = content.strip().split('\n')

    # Veriyi işleme
    real_ge = ge
    if girpx and not real_ge.startswith(girpx):
        real_ge = girpx + real_ge
    if girp and not real_ge.endswith(girp):
        real_ge = real_ge + girp
    if dex_ID:
        real_ge = f"{dex_ID}; {real_ge}"

    # Başlığı işleme
    real_dax = dax
    if girpx_header and real_dax and not real_dax.startswith(girpx_header):
        real_dax = girpx_header + real_dax
    if girp_header and real_dax and not real_dax.endswith(girp_header):
        real_dax = real_dax + girp_header

    current_header = None
    in_target_header = False

    for line in lines:
        stripped = line.strip()
        if stripped.endswith(':'):
            current_header = stripped[:-1]
            in_target_header = (current_header == real_dax) if real_dax else True
        elif in_target_header:
            if stripped == real_ge:
                print(f"Veri '{real_ge}' başlık '{current_header}' içinde bulundu.")
                if isinstance(fop, list):
                    fop.append(True)
                return

    if dax:
        print(f"Veri '{real_ge}' başlık '{real_dax}' içinde bulunamadı.")
    else:
        print(f"Veri '{real_ge}' hiçbir başlık altında bulunamadı.")
    if isinstance(fop, list):
        fop.append(False)

def delete(ID, delete_header=None, dex_ID=None, fop=None, es=None, os=None):
    import io
    from google.oauth2 import service_account
    from googleapiclient.discovery import build
    from googleapiclient.http import MediaIoBaseDownload, MediaIoBaseUpload

    creds = service_account.Credentials.from_service_account_info(es)
    service = build('drive', 'v3', credentials=creds)

    query = f"'{os}' in parents and name='{ID}'"
    results = service.files().list(q=query, fields="files(id)").execute()
    files = results.get('files', [])

    if not files:
        print(f"{ID} dosyası bulunamadı.")
        if isinstance(fop, list):
            fop.append(False)
        return

    file_id = files[0]['id']

    request = service.files().get_media(fileId=file_id)
    file_io = io.BytesIO()
    downloader = MediaIoBaseDownload(file_io, request)
    done = False
    while not done:
        _, done = downloader.next_chunk()
    content = file_io.getvalue().decode('utf-8')

    lines = content.strip().split('\n')
    new_lines = []
    skip = False
    found = False

    if delete_header:
        # Klasik başlık silme modu
        for line in lines:
            if line.strip().endswith(':'):
                if line.strip()[:-1] == delete_header:
                    skip = True
                    found = True
                    continue
                else:
                    skip = False
            if not skip:
                new_lines.append(line)

        if not found:
            print(f"'{delete_header}' başlığı bulunamadı.")
            if isinstance(fop, list):
                fop.append(False)
            return
        else:
            print(f"'{delete_header}' başlığı ve altındaki veriler silindi.")

    elif dex_ID:
        # Belirli başlık altındaki bir veriyi silme modu
        target_header = dex_ID[0]
        target_data = dex_ID[1]
        in_target_header = False
        header_found = False
        data_found = False

        for i, line in enumerate(lines):
            stripped = line.strip()
            if stripped.endswith(':'):
                if stripped[:-1] == target_header:
                    in_target_header = True
                    header_found = True
                    new_lines.append(line)
                    continue
                else:
                    in_target_header = False

            if in_target_header:
                if stripped.startswith(f"{target_data};"):
                    data_found = True
                    continue  # bu satırı atlıyoruz (siliyoruz)
                else:
                    new_lines.append(line)
            else:
                new_lines.append(line)

        if not header_found:
            print(f"'{target_header}' başlığı bulunamadı.")
            if isinstance(fop, list):
                fop.append(False)
            return
        if not data_found:
            print(f"'{target_data}' verisi bulunamadı.")
            if isinstance(fop, list):
                fop.append(False)
            return
        else:
            print(f"'{target_header}' başlığı altındaki '{target_data}' verisi silindi.")

    else:
        print("Hiçbir işlem yapılmadı. 'delete_header' veya 'dex_ID' parametresi girilmelidir.")
        if isinstance(fop, list):
            fop.append(False)
        return

    updated_content = '\n'.join(new_lines)

    updated_file = io.BytesIO(updated_content.encode('utf-8'))
    media = MediaIoBaseUpload(updated_file, mimetype='text/plain')
    service.files().update(fileId=file_id, media_body=media).execute()

    if isinstance(fop, list):
        fop.append(True)

def get(ID="dosya.txt", Hup=None, Pen=None, go=None, fop=None, es=None, os=None):
    import io, re
    from google.oauth2 import service_account
    from googleapiclient.discovery import build
    from googleapiclient.http import MediaIoBaseDownload

    creds = service_account.Credentials.from_service_account_info(es)
    service = build('drive', 'v3', credentials=creds)

    query = f"'{os}' in parents and name='{ID}'"
    results = service.files().list(q=query, fields="files(id)").execute()
    files = results.get('files', [])

    if not files:
        if Pen is not None:
            Pen.append(None)
        if isinstance(fop, list):
            fop.append(False)
        return

    file_id = files[0]['id']
    request = service.files().get_media(fileId=file_id)
    file_io = io.BytesIO()
    downloader = MediaIoBaseDownload(file_io, request)
    done = False
    while not done:
        _, done = downloader.next_chunk()

    content = file_io.getvalue().decode('utf-8')
    lines = content.splitlines()

    def is_header_line(s: str) -> bool:
        return s.strip().endswith(":")

    def is_key_line(s: str) -> bool:
        return re.match(r'^\s*[^;\s][^;:]*;\s*', s) is not None

    if isinstance(Hup, tuple) and len(Hup) == 2:
        header, target = Hup
        in_header = False
        i = 0
        result = None

        while i < len(lines):
            line = lines[i]
            stripped = line.strip()

            if is_header_line(line):
                in_header = (stripped[:-1].strip() == header)
                i += 1
                continue

            if in_header and stripped.startswith(f"{target};"):
                first = line.split(";", 1)[1].lstrip() if ";" in line else ""
                acc = [first]
                i += 1
                while i < len(lines):
                    nxt = lines[i]
                    if is_header_line(nxt) or is_key_line(nxt):
                        break
                    acc.append(nxt.strip())
                    i += 1
                result = " ".join(acc).strip()
                break

            i += 1

        if Pen is not None:
            Pen.append(result if result is not None else "")
        if isinstance(go, list) and result is not None:
            go.append(result)
        if isinstance(fop, list):
            fop.append(result is not None)

    elif isinstance(Hup, str):
        header = Hup
        in_header = False
        result_lines = []
        found = False

        for line in lines:
            if is_header_line(line):
                name = line.strip()[:-1].strip()
                if in_header:
                    break
                in_header = (name == header)
                if in_header:
                    found = True
                continue
            if in_header:
                result_lines.append(line.strip())

        if Pen is not None:
            Pen.append(" ".join(result_lines).strip())
        if isinstance(fop, list):
            fop.append(found)

    else:
        if Pen is not None:
            Pen.append(content)
        if isinstance(fop, list):
            fop.append(True)

def give(dex, dax, dox, es, os, fop=None, girp=None, girpx=None, girp_header=None, girpx_header=None, dex_ID=None):
    import io
    from google.oauth2 import service_account
    from googleapiclient.discovery import build
    from googleapiclient.http import MediaIoBaseDownload, MediaIoBaseUpload

    # === dex verisi düzenleme ===
    real_dex = dex
    if girpx and not real_dex.startswith(girpx):
        real_dex = girpx + real_dex
    if girp and not real_dex.endswith(girp):
        real_dex = real_dex + girp

    # === dax başlık düzenleme ===
    real_dax = dax
    if girpx_header and not real_dax.startswith(girpx_header):
        real_dax = girpx_header + real_dax
    if girp_header and not real_dax.endswith(girp_header):
        real_dax = real_dax + girp_header

    creds = service_account.Credentials.from_service_account_info(es)
    service = build('drive', 'v3', credentials=creds)

    query = f"'{os}' in parents and name='{dox}'"
    results = service.files().list(q=query, fields="files(id)").execute()
    files = results.get('files', [])

    if not files:
        print(f"{dox} dosyası bulunamadı.")
        if isinstance(fop, list):
            fop.append(False)
        return

    file_id = files[0]['id']
    request = service.files().get_media(fileId=file_id)
    file_io = io.BytesIO()
    downloader = MediaIoBaseDownload(file_io, request)
    done = False
    while not done:
        _, done = downloader.next_chunk()

    content = file_io.getvalue().decode('utf-8')
    lines = content.strip().split('\n')

    found_header = False
    updated = False
    new_lines = []
    i = 0
    while i < len(lines):
        line = lines[i]
        new_lines.append(line)
        if line.strip() == real_dax + ":":
            found_header = True
            i += 1
            while i < len(lines):
                current_line = lines[i].strip()
                if current_line.endswith(":"):
                    break

                # === Yeni: dex_ID eşleşmesi kontrolü ===
                if dex_ID and current_line.startswith(f"{dex_ID};"):
                    parts = lines[i].split(";", 1)
                    if len(parts) == 2:
                        # Aynı satıra ekle
                        existing_data = parts[1].strip()
                        new_data = f"{parts[0]}; {existing_data} {real_dex}".strip()
                        new_lines.append(new_data)
                        updated = True
                        i += 1
                        continue

                # === Eski sistemde: Aynı veri varsa tekrar ekleme ===
                if lines[i].strip() == real_dex:
                    updated = True

                new_lines.append(lines[i])
                i += 1

            if not updated:
                if dex_ID:
                    new_lines.append(f"{dex_ID}; {real_dex}")
                else:
                    new_lines.append(real_dex)
            continue
        i += 1

    if not found_header:
        new_lines.append(f"{real_dax}:")
        if dex_ID:
            new_lines.append(f"{dex_ID}; {real_dex}")
        else:
            new_lines.append(real_dex)

    new_content = '\n'.join(new_lines)
    file_io = io.BytesIO(new_content.encode('utf-8'))
    media = MediaIoBaseUpload(file_io, mimetype='text/plain', resumable=True)

    service.files().update(fileId=file_id, media_body=media).execute()

    if isinstance(fop, list):
        fop.append(True if not updated else False)