from fastapi import FastAPI
import uvicorn


if __name__ == "__main__":
    uvicorn.run(
        host='0.0.0.0',
        app="main:app",
        reload=True,
        workers=1,
    )
