"""Browser check: run after starting ``python webapp.py``."""

import os

from playwright.sync_api import sync_playwright


URL = os.getenv("WEB_APP_URL", "http://127.0.0.1:5000/")

with sync_playwright() as playwright:
    browser = playwright.chromium.launch(headless=True)
    page = browser.new_page(viewport={"width": 900, "height": 900})
    page.goto(URL, wait_until="networkidle")
    canvas = page.locator("#drawing-canvas")
    box = canvas.bounding_box()
    assert box is not None
    page.mouse.move(box["x"] + 180, box["y"] + 160)
    page.mouse.down()
    page.mouse.move(box["x"] + 510, box["y"] + 160, steps=15)
    page.mouse.move(box["x"] + 270, box["y"] + 540, steps=20)
    page.mouse.up()
    page.locator("#predict-button").click()
    page.wait_for_function("document.querySelector('#result').textContent.includes('Confidence:')")
    assert "Prediction:" in page.locator("#result").inner_text()
    page.locator("#clear-button").click()
    assert page.locator("#result").inner_text() == ""
    browser.close()
    print("Playwright passed")
