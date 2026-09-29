from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

# Создаем само приложение сайта
app = FastAPI(title="MergeOnline-Web")

# Указываем FastAPI, где искать статические файлы (css, js и картинки) (выдаём разрешение на то чтобы заглядывать в файлы компьютера)
app.mount("/static", StaticFiles(directory="app/static"), name="static")


# настраиваем движок шаблоннов Jinja2 на папку templates где html файлы (призываем папку шаблонов)
templates = Jinja2Templates(directory="app/templates")


# Указываем сервеу что делать когда пользователь заходит на главную страницу (путь "/")
@app.get("/", response_class=HTMLResponse)
def read_root(request: Request):
    # Теперь отправляем файл index.html вместо текста
    # Заодно передаём обязательный обьект request, чтобы Jinja2 могла связать сервер и браузер
    return templates.TemplateResponse("index.html", {"request": request})
