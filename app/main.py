from fastapi import FastAPI, Request, Form, File, UploadFile
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

# Создаем само приложение сайта
app = FastAPI(title="MergeOnline-Web")

# Указываем FastAPI, где искать статические файлы (css, js и картинки) (выдаём разрешение на то чтобы заглядывать в файлы компьютера)
app.mount("/static", StaticFiles(directory="app/static"), name="static")


# настраиваем движок шаблоннов Jinja2 на папку templates где html файлы (призываем папку шаблонов)
templates = Jinja2Templates(directory="app/templates")


# Указываем серверу что делать когда пользователь заходит на главную страницу (путь "/")
@app.get("/", response_class=HTMLResponse)
def read_root(request: Request):
    # Теперь отправляем файл index.html вместо текста
    # Заодно передаём обязательный обьект request, чтобы Jinja2 могла связать сервер и браузер
    return templates.TemplateResponse("index.html", {"request": request})


# Обработка отправки формы (POST запрос)
@app.post("/merge") # указан тот самый путь /merge что и писали в <form action="/merge"> в HTML
async def merge_audio(
    request: Request,
    inst_file: UploadFile = File(...),
    voice_file: UploadFile = File(...),
    use_rms: bool = Form(False)
): # Для теста выводим в консоль информацию о полученных файлах
    print(f"🎵 Получен инструментал: {inst_file.filename}")
    print(f"🎤 Получен вокал: {voice_file.filename}")
    print(f"🎛️ Галочка RMS включена?: {use_rms}")

    return {
        "status": "Файлы успешно приняты сервером.",
        "instrumental": inst_file.filename,
        "vocals": voice_file.filename,
        "rms_enabled": use_rms
    }