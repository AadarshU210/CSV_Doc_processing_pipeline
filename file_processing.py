import pandas as pd
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import update
from models import Files
from db import async_session
import asyncio

async def process_csv(filepath: str, file_id: int, db: AsyncSession):
    try:
        # Updating status to in-progress for current file
        await db.execute(update(Files).where(Files.file_id == file_id).values(status="in-progress"))
        await db.commit()
        
        # Processing CSV file
        df = pd.read_csv(filepath)
        
        total_rows = len(df)
        most_frequent = df.mode().iloc[0].to_dict()  # Converting to dict for storing in JSON
        avg = df.mean(numeric_only=True).to_dict()
        
        data = {
            "total_rows": total_rows,
            "most_frequent": most_frequent,
            "avg_numeric": avg
        }
        
        # Updating Status and persisting result
        await db.execute(update(Files).where(Files.file_id == file_id).values(
            status="completed",
            result=data
        ))
        await db.commit()
        
    except Exception as e:
        await db.execute(update(Files).where(Files.file_id == file_id).values(
            status="failed",
            result={"error": str(e)}
        ))
        await db.commit()


   
async def process_all_files(file_tasks: list):
         
         # List of all processing tasks
         tasks = [process_with_own_db(filepath, file_id) for file_id, filepath in file_tasks]
         
         # Run all tasks concurrently
         await asyncio.gather(*tasks)
    
async def process_with_own_db(filepath:str, file_id:int):
    # this helper function will be called per file and each process will have its own db session
    async with async_session() as db:
        await process_csv(filepath, file_id, db)
