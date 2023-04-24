from fastapi import FastAPI, HTTPException, APIRouter
from starlette.responses import RedirectResponse, JSONResponse
from process import LinuxProcess, LinuxProcessStatistic, ProcessStatus

command_to_execute = "ping -i 5 -c 100 www.google.com"
output_file = "output.txt"
process = LinuxProcess(command_to_execute.split(), output_file)

app = FastAPI()
router = APIRouter()


# Define a route to redirect requests from /api/docs to /docs
@app.get("/api/docs")
async def redirect_to_docs():
    return RedirectResponse(url="/docs")


# redirect / to /docs
@app.get("/")
async def redirect_to_docs():
    return RedirectResponse(url="/docs")


@app.post("/api/ping/")
def process_control(command: str):
    global process

    if command == "start":
        # already running
        if process is not None and process.status == ProcessStatus.RUNNING:
            return {"status": "Process is already running"}
        # start process
        process.start()

    elif command == "stop":
        if process is not None and process.status == ProcessStatus.RUNNING:
            process.stop()
            return {"status": "Process stopped"}
        elif process.status == ProcessStatus.KILLED:
            return {"status": "Process already stopped"}
        return {"status": "Process not started yet"}

    return {"status": process.status.value}


@app.get("/api/ping")
async def get_status():
    global process
    stats = LinuxProcessStatistic(process)
    stats_dict = stats.to_dict()
    return JSONResponse(content=stats_dict)


@app.get("/api/ping/result")
async def get_result():
    global process

    if process.status == ProcessStatus.NOT_STARTED:
        raise HTTPException(status_code=404, detail="Process not started")

    return {"result": process.get_result()}
