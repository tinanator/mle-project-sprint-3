import requests
import time

for i in range(5):
    requests.get('http://localhost:8081')
    time.sleep(2)

obj = {"KBinsDiscretizer__latitude_4.0": 0.0, "KBinsDiscretizer__longitude_3.0": 0.0,"building_type_int_4": 1.0, "building_type_int_6": 0.0, "KBinsDiscretizer__latitude_0.0": 0.0, "latitude": 0.0, "KBinsDiscretizer__longitude_1.0": -0.427130, "KBinsDiscretizer__latitude_2.0": 0.581639, "KBinsDiscretizer__longitude_4.0": 1.0, "building_type_int_2": 1.0, "ceiling_height": -0.427130, "KBinsDiscretizer__longitude_2.0": 0.0, "PolynomialFeatures__total_area^2": 0.118176, "floors_total": 9.0, "KBinsDiscretizer__latitude_3.0": 1.0, "building_type_int_1": 0.0, "kitchen_area": -0.623586, "PolynomialFeatures__total_area": -0.343767, "KBinsDiscretizer__longitude_0.0": 0.0, "has_elevator_True": 0.0}

for i in range(100):
    r = requests.post("http://localhost:8081/api/price/?user_id=1", json = obj)
    print(r)
    time.sleep(2)
