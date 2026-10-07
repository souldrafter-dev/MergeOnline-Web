from fastapi import FastAPI, Request, Form, File, UploadFile
from fastapi.responses import HTMLResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import io


from app.merger import merge_fnf_tracks

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
): # Чтение файлов из интернета напрямую в байты памяти сервера
    inst_bytes = await inst_file.read()
    voice_bytes = await voice_file.read()

    # Передаём байты в созданную функцию из файла merger.py и забираем готовый файл combined
    combined_audio = merge_fnf_tracks(io.BytesIO(inst_bytes), io.BytesIO(voice_bytes), use_rms) # исправлено дополнен то что для каждый файл завернут в io.byteIO

    output_buffer = io.BytesIO()
    combined_audio.export(output_buffer, format="ogg")
    output_buffer.seek(0)

    return StreamingResponse(
        output_buffer,
        media_type="audio/ogg",
        headers={"Content-Disposition": "attachment; filename=merged_track.ogg"}
    )