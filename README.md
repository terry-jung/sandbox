# terrypractice

Live camera hover translation web app.

## What it does

This app provides a magnifier-style live translation experience:

1. Start your phone/laptop camera in the browser.
2. Hover the lens over text on paper/signs/screens.
3. OCR reads text inside the focus box.
4. The app translates it and shows the result inside the floating lens and output panel.

## Tech used

- `getUserMedia` for camera streaming.
- `Tesseract.js` for in-browser OCR.
- MyMemory translation API for translated text output.

## Run locally

```bash
python3 -m http.server 4173
```

Then open `http://localhost:4173`.

> Note: Camera access requires HTTPS in most mobile browsers. For local desktop testing,
> `localhost` is generally allowed.
