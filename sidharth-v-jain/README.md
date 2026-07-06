# Todo CRUD API -  Key Authentication

This iteration adds API key authentication on top of the validated
Todo API from the previous version. Nothing about the CRUD behavior or
validation rules changed; it just has to be authorized before requests work now.


## Setup

```bash
pip install -r requirements.txt
cp .env.example .env
```

Edit `.env` and set the key (any key):

```
API_KEY=your_secret_key_here
```

## Run

```bash
uvicorn main:app --reload
```


