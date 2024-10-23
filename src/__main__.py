import uvicorn

from geo_api import APP, LOGGER, API_IP, API_PORT
from geo_api.schemas import MessageSchema, ShowUserSchema, MessageMode


class MyClass:
    status = MessageMode()


if __name__ == '__main__':
    LOGGER.debug("Starting...")
    uvicorn.run(
        APP,
        host='0.0.0.0',
        port=API_PORT,
        reload=False, log_level="debug",
    )
    LOGGER.debug("Ending.")
