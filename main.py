import uvicorn

if __name__ == "__main__":
    uvicorn.run("src.app:app", host="0.0.0.0",port=80,log_level="info")


#uvicorn src.app:app --reload