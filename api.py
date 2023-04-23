from fastapi import FastAPI, HTTPException, APIRouter
from starlette.responses import RedirectResponse, JSONResponse
from process import LinuxProcess, LinuxProcessStatistic, ProcessStatus

command = "ping -i 5 -c 100 www.google.com"
output_file = "output.txt"
process = LinuxProcess(command.split(), output_file)

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


@app.post("/api/ping/start")
def start_process():
    global process
    global command

    # already running
    if process is not None and process.status == ProcessStatus.RUNNING:
        raise HTTPException(status_code=400, detail="Process is already running")

    # start process
    process.start()
    return {"status": process.status.value}


@app.post("/api/ping/stop")
async def stop_process():
    global process

    if process is not None and process.status == ProcessStatus.RUNNING:
        process.stop()
        return {"status": "Process stopped"}
    elif process.status == ProcessStatus.KILLED:
        return {"status": "Process stopped"}
    else:
        raise HTTPException(status_code=404, detail="Process not found")


@app.get("/api/ping")
async def get_status():
    global process
    stats = LinuxProcessStatistic(process)
    stats_dict = stats.to_dict()
    return JSONResponse(content=stats_dict)


@app.get("/api/ping/result")
async def get_result():
    global process
    return {"result": process.get_result()}
