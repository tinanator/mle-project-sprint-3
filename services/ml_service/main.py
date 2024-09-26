"""Класс FastApiHandler, который обрабатывает запросы API."""

# импортируем класс модели
from catboost import CatBoostRegressor

class FastApiHandler:
    """Класс FastApiHandler, который обрабатывает запрос и возвращает предсказание."""

    def __init__(self):
        """Инициализация переменных класса."""

        # типы параметров запроса для проверки
        self.param_types = {
            "user_id": str,
            "model_params": dict
        }

        # Cписок необходимых параметров модели 
        self.required_model_params = [
            'KBinsDiscretizer__latitude_4.0',
            'floors_total',
            'building_type_int_1',
            'KBinsDiscretizer__longitude_3.0',
            'KBinsDiscretizer__latitude_3.0',
            'KBinsDiscretizer__latitude_0.0',
            'PolynomialFeatures__total_area',
            'PolynomialFeatures__total_area^2',
            'KBinsDiscretizer__longitude_2.0',
            'KBinsDiscretizer__longitude_0.0',
            'building_type_int_4',
            'ceiling_height',
            'KBinsDiscretizer__longitude_1.0',
            'building_type_int_2',
            'has_elevator_True',
            'KBinsDiscretizer__longitude_4.0',
            'latitude',
            'KBinsDiscretizer__latitude_2.0',
            'building_type_int_6',
            'kitchen_area'
        ]

        self.model_path = "./models/model"

        self.load_model(model_path=self.model_path)

        print("model is")
        print(self.model)

    def load_model(self, model_path: str):
        """Загружаем обученную модель предсказания стоимости квартиры.
        
            Args:
            model_path (str): Путь до модели.
        """
        try:
            self.model = CatBoostRegressor()
            self.model.load_model(model_path)
        except Exception as e:
            print(f"Failed to load model: {e}")
            raise e

    def price_predict(self, model_params: dict) -> float:
        """Предсказываем стоимость.

        Args:
            model_params (dict): Параметры для модели.

        Returns:
            float — стоимость
        """
        return self.model.predict(list(model_params.values()))
        
    def check_required_query_params(self, params: dict) -> bool:
        """Проверяем параметры запроса на наличие обязательного набора.

        Args:
            params (dict): Параметры запроса.
        
        Returns:
            bool: True — если есть нужные параметры, False — иначе
        """
        
        if "user_id" not in params or "model_params" not in params:
            return False

        if not isinstance(params["user_id"], str):
            return False
                
        if not isinstance(params["model_params"], dict):
            return False
        return True 
    
    def check_required_model_params(self, model_params: dict) -> bool:
        """Проверяем параметры пользователя на наличие обязательного набора.

        Args:
            model_params (dict): Параметры пользователя для предсказания.

        Returns:
            bool: True — если есть нужные параметры, False — иначе
        """
        if set(model_params.keys()) == set(self.required_model_params):
            return True
        return False 
    
    def validate_params(self, params: dict) -> bool:
        """Проверяем корректность параметров запроса и параметров модели.

        Args:
            params (dict): Словарь параметров запроса.

        Returns:
             bool: True — если проверки пройдены, False — иначе
        """
        if self.check_required_query_params(params):
            print("All query params exist")
        else:
            print("Not all query params exist")
            return False

        if self.check_required_model_params(params["model_params"]):
            print("All model params exist")
        else:
            print("Not all model params exist")
            return False

        return True

    def handle(self, params):
        """Функция для обработки запросов API.

        Args:
            params (dict): Словарь параметров запроса.

        Returns:
            dict: Словарь, содержащий результат выполнения запроса.
        """ 

        try:
            # валидируем запрос к API
            if not self.validate_params(params):
                print("Error while handling request")
                response = {"Error": "Problem with parameters"}
            else:
                model_params = params["model_params"]
                user_id = params["user_id"]
                print(f"Predicting for user_id: {user_id} and model_params:\n{model_params}")

                # получаем предсказания модели
                response = {"user_id": user_id, "prediction": self.price_predict(model_params)}

        except Exception as e:
            print(f"Error while handling request: {e}")
            raise e
        else:
            return response









# from handler import FastApiHandler
from fastapi import FastAPI

app = FastAPI()

app.handler = FastApiHandler()

@app.get("/")
def read_root():
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
        return app.handler.handle(all_params)
    except Exception as e:
        print("Error in request")
    

