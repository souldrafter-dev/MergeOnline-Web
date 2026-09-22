from fastapi import FastAPI
from fastapi.responses import HTMLResponse

# Создаем само приложение сайта
app = FastAPI(title="MergeOnline-Web")

# Говорим серверу: когда пользователь заходит на главную страницу (путь "/")
@app.get("/", response_class=HTMLResponse)
def read_root():
    # Отдаем ему простой приветственный текст в формате HTML
    return """
    <html>
        <head><title>MergeOnline</title></head>
        <body style="background: #1e1e24; color: white; text-align: center; font-family: Arial; padding-top: 50px;">
            <h1>Сервер FastAPI успешно запущен! 🚀</h1>
            <p>MergeOnline-Web стартовал!</p>
        </body>
    </html>
    """
