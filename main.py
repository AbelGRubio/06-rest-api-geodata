from api_module import APP, LOGGER, API_IP, API_PORT
import uvicorn


def run_server():
    uvicorn.run(
        APP,
        host=API_IP,
        port=API_PORT,
        reload=False, log_level="debug",
    )


if __name__ == '__main__':
    run_server()
