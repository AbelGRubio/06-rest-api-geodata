import uvicorn

from geo_api import APP, LOGGER, API_IP, API_PORT


if __name__ == '__main__':
    LOGGER.debug("Starting...")
    uvicorn.run(
        APP,
        host=API_IP,
        port=API_PORT,
        reload=False, log_level="debug",
    )
    LOGGER.debug("Ending.")
