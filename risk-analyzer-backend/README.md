# Risk Exposure Analyzer Backend

## Setup

```bash
pip install -r requirements.txt
python -m spacy download en_core_web_sm
```

## Run

```bash
uvicorn app.main:app --reload
```

## API

### POST /analyze

Request body:

```json
{
  "text": "string"
}
```
