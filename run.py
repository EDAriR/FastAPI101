import uvicorn


def foo():
    return 0


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True, port=5000,
                log_level="debug", debug=True)

