from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from bot.services.master_service import get_masters
from bot.services.booking_service import book_appointment, get_available_slots
import logging

app = FastAPI()

logging.basicConfig(level=logging.DEBUG)

class BookingRequest(BaseModel):
    user_id: int
    master_id: int
    date: str
    time: int

@app.get("/api/masters")
async def list_masters():
    return await get_masters()

@app.get("/api/slots")
async def list_slots(master_id: int, date: str):
    return await get_available_slots(master_id, date)

@app.post("/api/book")
async def book(request: BookingRequest):
    success, message = await book_appointment(request.user_id, request.master_id, request.date, request.time)
    if not success:
        raise HTTPException(status_code=400, detail=message)
    return {"success": True, "message": message}