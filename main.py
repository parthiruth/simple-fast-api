from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")


def reverse_word(word: str) -> str:
    """Reverses a word without using Python's built-in functions."""
    word_list = list(word)
    start, end = 0, len(word_list) - 1
    while start < end:
        word_list[start], word_list[end] = word_list[end], word_list[start]
        start += 1
        end -= 1
    return "".join(word_list)


def reverse_sentence(sentence: str) -> str:
    """Reverses each word in a sentence."""
    words = sentence.split()
    reversed_words = [reverse_word(word) for word in words]
    return " ".join(reversed_words)


@app.get("/", response_class=HTMLResponse)
async def read_item(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "reversed_text": None})


@app.post("/", response_class=HTMLResponse)
async def reverse_text(request: Request):
    form = await request.form()
    text = form["text"]
    reversed_text = reverse_sentence(text)
    return templates.TemplateResponse("index.html", {"request": request, "reversed_text": reversed_text})
