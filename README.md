# Mini-Project 1 — Delivery Delay Prediction

This repository contains the files shared so far for the delivery-delay prediction project. More project files may be added as they are shared.

## Current components
- `main.py` — FastAPI prediction API with `/health` and `/predict` endpoints.
- `app.py` — Streamlit interface for entering delivery details and viewing a prediction.
- `REQ.txt` — Python dependencies currently identified from the shared requirements list and application imports.

## Project workflow
1. Explore the delivery-delay dataset.
2. Preprocess numeric and categorical features.
3. Train and evaluate candidate classifiers.
4. Save the chosen model as `models/best_model.pkl`.
5. Serve predictions through FastAPI.
6. Use Streamlit as the user interface.

## Important file/path notes
The supplied API loads the model from `models/best_model.pkl`, relative to the parent of the API file. The Streamlit app expects `internB_delivery_delays_processed.csv` alongside `app.py`. The repository layout and paths must be aligned when all files are uploaded.

## Environment
Install dependencies with:
```bash
pip install -r REQ.txt
```

## Run (after files and paths are arranged)
Start the API from the directory structure that places the model at the expected path:
```bash
uvicorn api.main:app --reload
```
Start the UI in a second terminal:
```bash
streamlit run app.py
```

These commands are provisional until the complete folder layout and model/data files are committed. The application has not yet been run end-to-end from this repository.
