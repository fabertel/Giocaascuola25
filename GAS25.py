from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
import os
from fastapi.staticfiles import StaticFiles
import uvicorn

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
MD_DIR = os.path.join(os.getcwd(), "static", "markdown")
os.makedirs(MD_DIR, exist_ok=True)
PAGE_TEMPLATE = "static/page.html"



@app.get("/", response_class=HTMLResponse)
async def root():
    """Reindirizza alla pagina di default con home.md"""
    return await get_page("home")


@app.get("/page", response_class=HTMLResponse)
async def get_page(md: str = "home"):
    """Renderizza Markdown utilizzando il template standard."""
    md_path = os.path.join(MD_DIR, f"{md}.md")
    print(f"🔍 Looking for Markdown file at: {md_path}")
    
    if not os.path.exists(md_path):
        return HTMLResponse("<p>Pagina non trovata.</p>", status_code=404)
    
    with open(md_path, "r", encoding="utf-8") as f:
        md_content = f.read()
    
    with open(PAGE_TEMPLATE, "r", encoding="utf-8") as f:
        page_template = f.read()
    
    # Inserisce il contenuto Markdown nel template
    final_page = page_template.replace("<div class=\"content\" id=\"content\">", 
                                       f"<div class=\"content\" id=\"content\">{md_content}")
    
    return HTMLResponse(content=final_page)



if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000, reload=True)