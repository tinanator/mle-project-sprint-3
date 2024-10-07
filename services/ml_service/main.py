# """Класс FastApiHandler, который обрабатывает запросы API."""

# # импортируем класс модели
import time
from prometheus_client import Counter

from .handler import FastApiHandler
from fastapi import FastAPI
from prometheus_fastapi_instrumentator import Instrumentator

app = FastAPI()

app.handler = FastApiHandler()

instrumentator = Instrumentator()
instrumentator.instrument(app).expose(app)


request_count = Counter(
    'app_request_count',
    'Application Request Count',
    ['method', 'endpoint', 'http_status']
)

prediction_fail = Counter(
    'app_prediction_bad',  
    'Amount of bad predictions',
    ['method', 'endpoint']
)

@app.get("/")
def read_root():
    request_count.labels('GET', '/', 200).inc()
    return {"Hello": "World"}

@app.post("/api/price/") 
def get_price(user_id: str, model_params: dict):
    """Предсказывает стоимость квартиры.

    Args:
        client_id (str): Идентификатор клиента.
        model_params (dict): Произвольный словарь с параметрами для модели.

    Returns:
        dict: Предсказанная стоимость.
    """
    all_params = {
            "user_id": user_id,
            "model_params": model_params
        }
    
    try:
        prediction = app.handler.handle(all_params)
        return prediction
    except Exception as e:
        print("Error in request")


    

