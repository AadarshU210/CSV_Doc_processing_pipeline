from fastapi import APIRouter, UploadFile, File, BackgroundTasks, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List
from db import get_db
from models import Files
from file_processing import process_all_files
import os
import shutil

file_router = APIRouter()

@file_router.post("/upload")
async def upload_file(background_tasks:BackgroundTasks, files : List[UploadFile] = File(...), db:AsyncSession = Depends(get_db)):
    os.makedirs('uploads', exist_ok=True)

    file_ids = []
    file_tasks = []

     # Validate all files are CSV before processing
    for file in files:
        # Check file extension
        if not file.filename.endswith('.csv'):
            raise HTTPException(
                status_code=400, 
                detail=f"Invalid file type: {file.filename}. Only CSV files are allowed."
            )
        
        # Check content type (MIME type)
        if file.content_type not in ['text/csv', 'application/csv', 'application/vnd.ms-excel']:
            raise HTTPException(
                status_code=400, 
                detail=f"Invalid file type: {file.filename}. Only CSV files are allowed."
            )

    #here we are looping through each file 
    for file in files:

        file_path = os.path.join('uploads', file.filename)

        # we are copying uploaded file onto disk
        with open(file_path, 'wb') as f:
            shutil.copyfileobj(file.file, f)

        new_file = Files(
            file_name = file.filename,
            status = "pending",
            result = None
        )

        db.add(new_file)
        await db.flush()
        file_ids.append(new_file.file_id)
        file_tasks.append((new_file.file_id, file_path))
    
    await db.commit()

    background_tasks.add_task(process_all_files, file_tasks)

    return {"message":"Files Uploaded Successfully and Processing Started", "file_ids":file_ids}

         

@file_router.get("/status/{file_id}")
async def get_file_status(file_id:int, db:AsyncSession = Depends(get_db)):

    query = select(Files).where(Files.file_id == file_id)
    result = await db.execute(query)
    file_record = result.scalar_one_or_none()

    if not file_record:
        return {"error":"file not found"}
    
    return {
        "file_id":file_record.file_id,
        "file_name":file_record.file_name,
        "status":file_record.status
    }

@file_router.get("/results/{file_id}")
async def get_file_result(file_id:int, db: AsyncSession = Depends(get_db)):
    query = select(Files).where(Files.file_id == file_id)
    result = await db.execute(query)
    file = result.scalar_one_or_none()

    if not file:
        return {"error":"file not found"}
    

    if file.status != "completed":
        return {
            "file_id":file.file_id,
            "status":file.status,
            "message":"Processing not yet completed"
        }
    
    return {
        "file_id":file.file_id,
        "file_name":file.file_name,
        "status":file.status,
        "result":file.result
    }
    

    