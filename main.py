from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
import requests
from bs4 import BeautifulSoup

app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/scrape")
def scrape_product(url: str = Query(...)):
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        r = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(r.content, "html.parser")

        name = soup.select_one("h1.product_title").text.strip()
        price = soup.select_one("p.price").text.strip()
        desc = soup.select_one("div.woocommerce-product-details__short-description").text.strip()
        images = [img["src"] for img in soup.select("div.woocommerce-product-gallery img")]

        return {
            "name": name,
            "price": price,
            "description": desc,
            "images": images
        }
    except Exception as e:
        return {"error": str(e)}
