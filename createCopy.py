import subprocess
import os
from datetime import datetime
import socket

def backup_mysql_db(username, password, db_name, backup_dir):
    if not os.path.exists(backup_dir):
        os.makedirs(backup_dir)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_file = os.path.join(backup_dir, f"{db_name}_backup_{timestamp}.sql")

    command = [
        "C:/Program Files/MySQL/MySQL Server 8.0/bin/mysqldump.exe",
        "-u", username,
        f"-p{password}",
        db_name,
        "--result-file", backup_file
    ]

    try:
        subprocess.run(command, check=True)
        print(f"Резервная копия успешно создана: {backup_file}")
        return backup_file
    except subprocess.CalledProcessError as e:
        print(f"Ошибка при создании резервной копии: {e}")

def send_file(host='25.61.27.7', port=5123, file_path='file_to_send.txt'):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))
    print(f"Подключено к серверу {host}:{port}")

    # Читаем файл и отправляем данные
    with open(file_path, 'rb') as f:
        while chunk := f.read(1024):  # Читаем файл порциями по 1024 байта
            client_socket.sendall(chunk)  # Отправляем данные

    print(f"Файл '{file_path}' успешно отправлен!")
    client_socket.close()  # Закрываем соединение