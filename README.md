# Описание
Простой HTTP сервер на чистом Python. 

# Инструкция по запуску
1) Установить зависимости
```bash
python3 -m venv venv
source venv/bin/activate
python3 -m pip install pyinstaller
```
2) Собрать исполняемый файл
```bash
pyinstaller --onefile --name http-server server.py
```
бинарный файл появится в папке `dist/`

3) Сделать бинарный файл исполняемым
```bash
chmod +x server
```
4) Запустить
```bash
nohup ./server > server.log 2>&1 &
```
