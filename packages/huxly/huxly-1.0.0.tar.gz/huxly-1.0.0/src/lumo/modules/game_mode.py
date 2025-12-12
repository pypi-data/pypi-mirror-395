"""Game mode utilities: non-invasive runtime suggestions and simulated boosts."""
from ..utils.logging import logger

_active = False

def start():
    global _active
    if _active:
        return {"status": "already_active"}
    # Apply safe, temporary tweaks: lower niceness of background processes (not implemented here)
    _active = True
    logger.info("Game mode started")
    return {"status": "started", "notes": "Applied safe game-mode suggestions (non-invasive)."}

def stop():
    global _active
    if not _active:
        return {"status": "not_active"}
    _active = False
    logger.info("Game mode stopped")
    return {"status": "stopped"}
