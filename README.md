# terrypractice

Image-based fashion search helper website.

## Run locally

```bash
python3 -m http.server 4173
```

Then open `http://localhost:4173`.

## How it works

1. Upload an image.
2. The browser runs MobileNet classification (TensorFlow.js).
3. The app extracts keywords from the image and builds search links for:
   - Yoox
   - Net-a-Porter
   - SSG
   - Kream
   - Jente
   - SSENSE
   - Cettire
4. Optionally, you can override the generated keywords with your own query.
