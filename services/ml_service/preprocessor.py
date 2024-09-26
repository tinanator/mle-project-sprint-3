from autofeat import AutoFeatRegressor  
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import OneHotEncoder
import pandas as pd
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import KBinsDiscretizer
from sklearn.preprocessing import PolynomialFeatures

class Preprocessor:
    """Класс Preprocessor, который преобразует признаки для предсказания."""
    
    selected_features = [
        'KBinsDiscretizer__latitude_4.0',
        'KBinsDiscretizer__longitude_3.0',
        'building_type_int_4',
        'building_type_int_6',
        'KBinsDiscretizer__latitude_0.0',
        'latitude',
        'KBinsDiscretizer__longitude_1.0',
        'KBinsDiscretizer__latitude_2.0',
        'KBinsDiscretizer__longitude_4.0',
        'building_type_int_2',
        'ceiling_height',
        'KBinsDiscretizer__longitude_2.0',
        'PolynomialFeatures__total_area^2',
        'floors_total',
        'KBinsDiscretizer__latitude_3.0',
        'building_type_int_1',
        'kitchen_area',
        'PolynomialFeatures__total_area',
        'KBinsDiscretizer__longitude_0.0',
        'has_elevator_True'
    ]

    @staticmethod
    def __manual_generate_features(cleaned_df: dict) -> dict:
        # ручная генерация признаков

        preprocessor = ColumnTransformer(
        transformers=[
            ("KBinsDiscretizer", KBinsDiscretizer(), ['latitude', 'longitude']),
            ("PolynomialFeatures", PolynomialFeatures(), ['total_area', 'living_area']),
        ],
        verbose_feature_names_out=True
        ) 

        pipe = Pipeline(steps=[('preprocessor', preprocessor)])

        return pd.DataFrame(pipe.fit_transform(cleaned_df), columns=preprocessor.get_feature_names_out())

    @staticmethod
    def __auto_generate_features(cleaned_df: dict) -> dict:
        # автогенерация признаков

        transformations = ('sqrt', 'log', '^2')

        afc = AutoFeatRegressor(transformations=transformations, feateng_steps=2, n_jobs=-1)
        return afc.transform(cleaned_df[['total_area', 'ceiling_height']])

    @staticmethod
    def __clean_one_hot(params: dict) -> dict:
        # масштабирование и кодирование признаков

        dataframe = pd.DataFrame(params, index=[0])
        print("dataframe")
        print(dataframe)
        int_cols = ['build_year', 'flats_count', 'floors_total', 'floor', 'rooms']
        cat_cols = ['building_type_int']
        dataframe = dataframe.drop('studio', axis=1)

        # делим признаки по типам
        df_float = dataframe.select_dtypes(include="float64")
        df_bool = dataframe.select_dtypes(include="bool")
        df_category = pd.concat([dataframe[cat_cols], df_bool], axis = 1)
        df_int = dataframe[int_cols].reset_index()

        # масштабируем признаки
        transformer = StandardScaler().fit(df_float)
        transformer.mean_
        transformer.scale_

        scaled = transformer.transform(df_float)
        df_num =  pd.DataFrame(scaled, columns=df_float.columns.values).reset_index()

        # one hot encoder
        encoder = OneHotEncoder(sparse_output=False)
        encoded_features = encoder.fit_transform(df_category)
        obj_df = pd.DataFrame(encoded_features, columns = encoder.get_feature_names_out()).reset_index()

        # обработанный датасет со scale и one hot encoder
        return pd.concat([obj_df, df_num, df_int], axis=1)

    @classmethod
    def preprocess(cls, params: dict):
        print("processing starts")
        cleaned_df = cls.__clean_one_hot(params)
        manual_df = cls.__manual_generate_features(cleaned_df)
        auto_df = cls.__auto_generate_features(cleaned_df)

        merged_data = pd.concat([manual_df.reset_index(drop=True), 
                    auto_df.reset_index(drop=True),
                    cleaned_df.reset_index(drop=True)], 
                    axis=1).reset_index()
        
        merged_data = merged_data.T.drop_duplicates(keep='first').T
        processed_data = merged_data.drop(['index'], axis=1)

        print("processing ends")
        return processed_data[cls.selected_features]