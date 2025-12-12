from fastapi import FastAPI, File, UploadFile,Request, HTTPException,Query
from fastapi.responses import JSONResponse, FileResponse
import uvicorn
from src import domain, apiKey
import argparse
import os
from dotenv import load_dotenv

load_dotenv()

app =FastAPI()
domain =domain.Domain()
key=apiKey.ApiKey(os.getenv("SECRET_KEY"))


@app.middleware("http")
async def auth_middleware(request: Request, call_next):
    # Chỉ bảo vệ 2 route
    if request.url.path in ["/add_record", "/delete_record"]:
        auth_header = request.headers.get("Authorization")
        
        if not auth_header or not auth_header.startswith("Bearer "):
            return JSONResponse(
                status_code=401,
                content={"status": "error", "message": "Missing or invalid Authorization header"}
            )

        token = auth_header.split(" ")[1]

        try:
            key.verifyToken(token)
        except HTTPException as e:
            return JSONResponse(status_code=e.status_code, content={"status": "error", "message": e.detail})

    response = await call_next(request)
    return response

@app.post("/add_record")
def add_record(
    subdomain: str = Query(..., min_length=1),
    record_type: str = Query(..., min_length=1),
    value: str = Query(..., min_length=1)
):
    try:
        domain.add_record(subdomain, record_type, value)
        return JSONResponse(
            content={
                "status": "success",
                "message": "Record added successfully",
                "subdomain": subdomain
            },
            status_code=200
        )
    except Exception as e:
        return JSONResponse(
            content={
                "status": "error",
                "message": f"Failed to add record: {str(e)}",
                "subdomain": subdomain
            },
            status_code=400
        )


@app.delete("/delete_record")
def delete_record(subdomain: str = Query(..., min_length=1)):
    try:
        domain.delete_record(subdomain)
        return JSONResponse(
            content={
                "status": "success",
                "message": "Record deleted successfully",
                "subdomain": subdomain
            },
            status_code=200
        )
    except Exception as e:
        return JSONResponse(
            content={
                "status": "error",
                "message": f"Failed to delete record: {str(e)}",
                "subdomain": subdomain
            },
            status_code=400
        )


def main():
    print("Starting server...")
    parser = argparse.ArgumentParser(description="Domain CLI Tool")
    parser.add_argument("command", nargs="?", help="Command to run: gen-key")
    args = parser.parse_args()
    domain.getListReCord()
    if args.command == "gen-key":
        print("🔑 Generated key:")
        print(key.generateKey()) 
    else:
        print("🚀 Starting FastAPI server...")
        uvicorn.run("src.app:app", host="0.0.0.0", port=7000, reload=False)

if __name__ == "__main__":
    main()