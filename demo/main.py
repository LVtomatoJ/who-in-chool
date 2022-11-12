from fastapi  import FastAPI,BackgroundTasks

app = FastAPI()


def print_hello_task():
    print("hello")

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/task")
async def task_demo(background_tasks:BackgroundTasks):
    background_tasks.add_task(print_hello_task)
    return {'code':"ok"}

