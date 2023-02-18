import random

from typing import Union
from fastapi import FastAPI, Depends

from data_generator.database.data_loader import DataLoader
from data_generator.data.log_parser import LogParser



ids = []
app = FastAPI()

def get_data_loader() -> DataLoader:
    data_loader = DataLoader()
    return data_loader

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/utils/db_init")
def parse_log(data_loader: DataLoader = Depends(get_data_loader)):
    global ids
    if len(ids) == 0:
        log_parser = LogParser()
        log_parser()
        ids = data_loader.get_ids()
    return "Database initialized"


@app.get("/logs/get_record")
def get_record(data_loader: DataLoader = Depends(get_data_loader)):
    global ids
    if len(ids) == 0:
        ids = data_loader.get_ids()
    return data_loader.get_log_message(random.choice(ids)).log_message
