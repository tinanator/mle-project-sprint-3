# Инструкции по запуску микросервиса

Каждая инструкция выполняется из директории репозитория mle-sprint3-completed
Если необходимо перейти в поддиректорию, напишите соотвесвтующую команду

## 1. FastAPI микросервис в виртуальном окружение
```python
# команды создания виртуального окружения
# и установки необходимых библиотек в него

sudo apt-get install python3.10-venv
python3.10 -m venv .mle-sprint3-venv
source .mle-sprint3-venv/bin/activate

pip install -r requirements.txt

# команда перехода в директорию

cd services/ml_service

# команда запуска сервиса с помощью uvicorn
```
uvicorn main:app --reload

### Пример curl-запроса к микросервису

curl -X POST -H "Content-Type: application/json" -d '{"KBinsDiscretizer__latitude_4.0": 0.0, "KBinsDiscretizer__longitude_3.0": 0.0,"building_type_int_4": 1.0, "building_type_int_6": 0.0, "KBinsDiscretizer__latitude_0.0": 0.0, "latitude": 0.0, "KBinsDiscretizer__longitude_1.0": -0.427130, "KBinsDiscretizer__latitude_2.0": 0.581639, "KBinsDiscretizer__longitude_4.0": 1.0, "building_type_int_2": 1.0, "ceiling_height": -0.427130, "KBinsDiscretizer__longitude_2.0": 0.0, "PolynomialFeatures__total_area^2": 0.118176, "floors_total": 9.0, "KBinsDiscretizer__latitude_3.0": 1.0, "building_type_int_1": 0.0, "kitchen_area": -0.623586, "PolynomialFeatures__total_area": -0.343767, "KBinsDiscretizer__longitude_0.0": 0.0, "has_elevator_True": 0.0}' http://localhost:1702/api/price/?user_id=1

## 2. FastAPI микросервис в Docker-контейнере

```bash
# команда перехода в нужную директорию

cd services

docker image build . --tag ml_service:0
docker container run --publish 8081:8081 --env-file .env ml_service:0
# команда для запуска микросервиса в режиме docker compose
```

### Пример curl-запроса к микросервису

curl -X POST -H "Content-Type: application/json" -d '{"KBinsDiscretizer__latitude_4.0": 0.0, "KBinsDiscretizer__longitude_3.0": 0.0,"building_type_int_4": 1.0, "building_type_int_6": 0.0, "KBinsDiscretizer__latitude_0.0": 0.0, "latitude": 0.0, "KBinsDiscretizer__longitude_1.0": -0.427130, "KBinsDiscretizer__latitude_2.0": 0.581639, "KBinsDiscretizer__longitude_4.0": 1.0, "building_type_int_2": 1.0, "ceiling_height": -0.427130, "KBinsDiscretizer__longitude_2.0": 0.0, "PolynomialFeatures__total_area^2": 0.118176, "floors_total": 9.0, "KBinsDiscretizer__latitude_3.0": 1.0, "building_type_int_1": 0.0, "kitchen_area": -0.623586, "PolynomialFeatures__total_area": -0.343767, "KBinsDiscretizer__longitude_0.0": 0.0, "has_elevator_True": 0.0}' http://localhost:8081/api/price/?user_id=1

## 3. Docker compose для микросервиса и системы моониторинга

```bash
# команда перехода в нужную директорию
cd services
# команда для запуска микросервиса в режиме docker compose
docker compose up  --build
```

### Пример curl-запроса к микросервису

curl -X POST -H "Content-Type: application/json" -d '{"KBinsDiscretizer__latitude_4.0": 0.0, "KBinsDiscretizer__longitude_3.0": 0.0,"building_type_int_4": 1.0, "building_type_int_6": 0.0, "KBinsDiscretizer__latitude_0.0": 0.0, "latitude": 0.0, "KBinsDiscretizer__longitude_1.0": -0.427130, "KBinsDiscretizer__latitude_2.0": 0.581639, "KBinsDiscretizer__longitude_4.0": 1.0, "building_type_int_2": 1.0, "ceiling_height": -0.427130, "KBinsDiscretizer__longitude_2.0": 0.0, "PolynomialFeatures__total_area^2": 0.118176, "floors_total": 9.0, "KBinsDiscretizer__latitude_3.0": 1.0, "building_type_int_1": 0.0, "kitchen_area": -0.623586, "PolynomialFeatures__total_area": -0.343767, "KBinsDiscretizer__longitude_0.0": 0.0, "has_elevator_True": 0.0}' http://localhost:8081/api/price/?user_id=1

## 4. Скрипт симуляции нагрузки
Скрипт генерирует 105 запросов

```
# команды необходимые для запуска скрипта
cd services/ml_service
python test_service.py

Адреса сервисов:
- микросервис: http://localhost:8081
- Prometheus: http://localhost:9090
- Grafana: http://localhost:3000