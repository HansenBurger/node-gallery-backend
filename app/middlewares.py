from fastapi import Request, HTTPException
from datetime import datetime
import logging

logger = logging.getLogger("app.request")

async def log_requests(request: Request, call_next):
    start_time = datetime.utcnow()
    try:
        response = await call_next(request)
        log_level = logging.INFO
    except HTTPException as exc:
        response = exc
        log_level = logging.WARNING
    except Exception as exc:
        response = HTTPException(500, "Internal Server Error")
        log_level = logging.ERROR

    end_time = datetime.utcnow()
    logger.log(
        log_level,
        {
            "method": request.method,
            "path": request.url.path,
            "status": response.status_code,
            "duration": (end_time - start_time).total_seconds(),
        }
    )
    return response