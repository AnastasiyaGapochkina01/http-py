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

# Проверка работы
1) Сделать запрос
```bash
# Health check
curl http://localhost:8000/health
```
Ответ: `{"status": "OK", "version": "1.0.0"}`

2) В браузере открыть адрес `http://${PUBLIC_IP}:8000/main`
<img width="1421" height="439" alt="image" src="https://github.com/user-attachments/assets/dbd04541-7df3-408f-9bee-ea011a8c0272" />

