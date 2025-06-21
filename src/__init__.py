from fastapi import FastAPI, Request
from fastapi.concurrency import asynccontextmanager
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from src.db import initdb
from src.user.routes import user_router
from src.Task.routes import router as task_router
from src.api import router as weather_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    await initdb()
    yield

app = FastAPI(lifespan=lifespan)
app.include_router(user_router)
app.include_router(task_router)
app.include_router(weather_router)
templates = Jinja2Templates(directory="src/templates")

def render_template(template_name: str):
    async def endpoint(request: Request):
        return templates.TemplateResponse(template_name, {"request": request})
    return endpoint

# قائمة الصفحات والقوالب
pages = [
    ("/", "welcome.html"),
    ("/home", "home.html"),
    ("/login-page", "login.html"),
    ("/register-page", "register.html"),
    ("/entertainment", "entertainment.html"),
    ("/game-xo", "game_xo.html"),
    ("/game-snake", "game_snake.html"),
    ("/game-memory", "game_memory.html"),
    ("/game-guess", "game_guess.html"),
    ("/study", "study.html"),
    ("/articles", "articles.html"),
    ("/tasks", "tasks.html"),
    ("/community", "community.html"),
    ("/weather", "weather.html"),
]

for path, template in pages:
    app.add_api_route(
        path,
        render_template(template),
        response_class=HTMLResponse
    )
