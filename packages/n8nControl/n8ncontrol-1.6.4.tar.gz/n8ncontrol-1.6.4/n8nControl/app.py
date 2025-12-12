from fastapi import FastAPI, File, UploadFile, HTTPException,Query
from fastapi.responses import JSONResponse, FileResponse
import uvicorn
import os
from dotenv import load_dotenv
from n8nControl.n8nManagement import N8nManagement

load_dotenv()
app = FastAPI()
n8n = N8nManagement()

@app.post('/import-workflow')
async def import_workflow(file: UploadFile = File(...)):
    try:
        if not file.filename or file.filename.strip() == "":
            raise HTTPException(status_code=400, detail="Uploaded file has no name")

        
        safe_filename = os.path.basename(file.filename)  
        save_path = f"/root/{safe_filename}"

        with open(save_path, "wb") as f:
            f.write(await file.read())


        result = n8n.import_workflow(save_path)
        return JSONResponse(result.__dict__)
    except Exception as e:
        return JSONResponse({"status": "error", "message": str(e)}, status_code=500)

@app.get('/export-workflow')
def export_workflow_route():
    try:
        result = n8n.export_workflow()
        return FileResponse(
            path=result["filePath"],
            filename=result["filename"],
            media_type='application/json',
            headers={"Content-Disposition": f"attachment; filename={result['filename']}"}
        )
    except Exception as e:
        return JSONResponse(
            {"status": "error", "message": str(e)}, status_code=500
        )
@app.post('/change-domain')
def change_domain(domain:str=Query(..., description="New domain name, e.g., n8n.example.com")):
    try:
        result = n8n.change_domain(domain)
        return JSONResponse(result.__dict__)
    except Exception as e:
        return JSONResponse({"status": "error", "message": str(e)}, status_code=500)
@app.post('/reset-user-info')
def reset_user_info():
    try:
        result = n8n.reset_user_info()
        return JSONResponse(result.__dict__)
    except Exception as e:
        return JSONResponse({"status": "error", "message": str(e)}, status_code=500)
@app.post('/update-version')
def update_version(version:str=Query(..., description="New n8n version, e.g., 0.220.0")):
    try:
        result = n8n.update_version(version)
        return JSONResponse(result.__dict__)
    except Exception as e:
        return JSONResponse({"status": "error", "message": str(e)}, status_code=500)
    
@app.get("/current-version")
def current_version():
    try:
        result = n8n.get_version_n8n()
        return JSONResponse(result.__dict__)
    except Exception as e:
        return JSONResponse({"status": "error", "message": str(e)}, status_code=500)

def main():
    print("N8nManagement initialized")
    port = int(os.getenv("PORT", 9000))
    n8n.set_domain_init()
    uvicorn.run("n8nControl.app:app", host="localhost", port=port, reload=False)

# Cho phép chạy trực tiếp bằng python app.py
if __name__ == "__main__":
    main()