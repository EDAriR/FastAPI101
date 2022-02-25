# FastAPI101

Ref: https://realpython.com/fastapi-python-web-apis/


#### run sever

```Shell
uvicorn main:app --reload
```
```python
import uvicorn

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=False, log_level="debug", debug=True,
                workers=1, limit_concurrency=1, limit_max_requests=1)
```
```Shell
uvicorn main:app --host=0.0.0.0 --port=8000 --log-level=debug --limit-max-requests=1 --limit-concurrency=1
```
#### Swagger
http://127.0.0.1:8000/docs

#### ReDoc
http://127.0.0.1:8000/redoc

### FastAPI Bigger Applications with Multiple Separate Files in Python
Ref: https://www.tutorialsbuddy.com/python-fastapi-bigger-applications-multiple-separate-files

