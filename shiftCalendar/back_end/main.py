
#connection without fastapi

import socket
import os
from parseSchedule import parse_schedule_pdf
from schedule_manager import ScheduleManager

HOST = '0.0.0.0'
PORT = int(os.environ.get("PORT", 8000))

bad_header = b"HTTP/1.1 400 Bad Request\r\n\r\nBad Request"
not_found_header = b"HTTP/1.1 404 Not Found\r\n\r\nNot Found"
ok_header = "HTTP/1.1 200 OK\r\nContent-Length: {}\r\nContent-Type: text/html\r\n\r\n"


def save_file_from_request(req_body_bytes: bytes, boundary: str):
    """
    Extracts file (PDF), year, and month from multipart/form-data body.
    """
    boundary_bytes = ("--" + boundary).encode()
    segments = req_body_bytes.split(boundary_bytes)

    filename, year, month, person_name = None, None, None, None
    pdf_bytes = None

    for seg in segments:
        if not seg.strip():
            continue

        # Split header/body inside this segment
        if b"\r\n\r\n" not in seg:
            continue
        header, data = seg.split(b"\r\n\r\n", 1)

        header_str = header.decode("latin1", errors="ignore")

        if "filename=" in header_str:
            filename_line = [l for l in header_str.split("\r\n") if "filename=" in l][0]
            filename = filename_line.split('filename="')[1].split('"')[0]
            filename = os.path.basename(filename)
            pdf_bytes = data.strip(b"\r\n")  # keep binary safe

        elif 'name="year"' in header_str:
            val = data.decode("utf-8", errors="ignore").strip()
            year = int(val) if val.isdigit() else None

        elif 'name="month"' in header_str:
            val = data.decode("utf-8", errors="ignore").strip()
            month = int(val) if val.isdigit() else None
        elif 'name="person_name"' in header_str:
            person_name = data.decode("utf-8", errors="ignore").strip()

    if not filename or pdf_bytes is None:
        raise ValueError("No valid PDF found in form data.")

    os.makedirs("uploads", exist_ok=True)
    pdf_path = os.path.join("uploads", filename)
    with open(pdf_path, "wb") as f:
        f.write(pdf_bytes)

    return pdf_path, year, month, person_name


def handle_request(data: bytes):
    try:
        sep = b"\r\n\r\n"
        if sep not in data:
            return bad_header
        header_bytes, body = data.split(sep, 1)
        header_text = header_bytes.decode("latin1", errors="ignore")
        lines = header_text.split("\r\n")

        # Parse request line
        if not lines:
            return bad_header
        tokens = lines[0].split(" ")
        if len(tokens) < 2:
            return bad_header
        method, path = tokens[0], tokens[1]

        # === GET ===
        if method == "GET":
            if path == "/" or path == "/index.html":
                with open("HomePage.html", "rb") as f:
                    html_body = f.read()
                return ok_header.format(len(html_body)).encode() + html_body

            elif path.startswith("/download/"):
                ics_name = path.split("/")[-1]
                ics_path = os.path.join("output", ics_name)
                if os.path.exists(ics_path):
                    with open(ics_path, "rb") as f:
                        data = f.read()
                    header = (
                        "HTTP/1.1 200 OK\r\n"
                        "Content-Type: text/calendar\r\n"
                        f"Content-Length: {len(data)}\r\n"
                        f"Content-Disposition: attachment; filename={ics_name}\r\n\r\n"
                    )
                    return header.encode() + data
                return not_found_header

            else:
                return not_found_header

        # === POST /upload ===
        elif method == "POST" and path == "/upload":
            # Find boundary
            boundary = None
            for line in lines:
                if "boundary=" in line:
                    boundary = line.split("boundary=")[-1]
                    break
            if not boundary:
                return bad_header

            pdf_path, year, month, person_name = save_file_from_request(body, boundary)
            print(f"📄 Received {pdf_path} ({year}-{month} : {person_name})")

            # Process the uploaded PDF
            parsed = parse_schedule_pdf(pdf_path, year, month)
            mgr = ScheduleManager(parsed)

            os.makedirs("output", exist_ok=True)
            ics_path = os.path.join("output", f"schedule.ics")
            json_path = os.path.join("output", f"schedule.json")
            mgr.export_to_ics(file_path=ics_path, filter_fn=lambda e: e.get("name") == person_name)
            mgr.export_to_json(file_path=json_path, filter_fn=lambda e: e.get("name") == person_name)

            # mgr.get_by_person(person_name)

            # Respond on the same page (no redirect)
            msg = f"""
            <html><body style='font-family:sans-serif; text-align:center;'>
            <h2>✅ Successfully converted {os.path.basename(pdf_path)}!</h2>
            <a href='/download/schedule.ics'>Download ICS file</a><br><br>
            <a href='/'>⬅ Back</a>
            </body></html>
            """
            return (ok_header.format(len(msg)) + msg).encode()

        else:
            return bad_header

    except Exception as e:
        print("⚠️ Error parsing request:", e)
        return bad_header


# === Socket server ===
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((HOST, PORT))
    s.listen(5)
    print(f"Listening on port {PORT}...")

    while True:
        try:
            conn, addr = s.accept()
            with conn:
                print("\nConnected by", addr)

                # Step 1: Read header
                data = b""
                while b"\r\n\r\n" not in data:
                    chunk = conn.recv(4096)
                    if not chunk:
                        break
                    data += chunk

                if not data:
                    continue

                # Step 2: Get content length
                header, _, rest = data.partition(b"\r\n\r\n")
                header_text = header.decode("latin1", errors="ignore")
                content_length = 0
                for line in header_text.split("\r\n"):
                    if line.lower().startswith("content-length:"):
                        content_length = int(line.split(":")[1].strip())
                        break

                # Step 3: Read body completely
                body = rest
                while len(body) < content_length:
                    chunk = conn.recv(4096)
                    if not chunk:
                        break
                    body += chunk

                full_request = header + b"\r\n\r\n" + body

                # Step 4: Handle request
                response = handle_request(full_request)
                if isinstance(response, str):
                    conn.sendall(response.encode())
                else:
                    conn.sendall(response)

        except KeyboardInterrupt:
            print("\nServer shutting down.")
            break
        except Exception as e:
            print("Error:", e)