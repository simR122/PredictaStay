import os
import pandas as pd
import numpy as np
from src.logger import get_logger
from src.custom_exception import CustomException
from config.paths_config import *
from utils.common_functions import read_yaml, load_data
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from imblearn.over_sampling import SMOTE

logger = get_logger(__name__)

class DataProcessor:
    def __init__(self, train_path, test_path, processed_dir, config_path):
        self.train_path = train_path
        self.test_path = test_path
        self.processed_dir = processed_dir
        self.config_path = config_path  # Initialize config_path

        self.config = read_yaml(config_path)
        logger.info(f"Loaded configuration: {self.config}")
    
        if not os.path.exists(self.processed_dir):
            os.makedirs(self.processed_dir)

    def preprocess_data(self, df):
        try:
            logger.info("Starting data processing step")

            logger.info("Dropping unnecessary columns")
            df.drop(columns=['Booking_ID'], inplace=True, errors='ignore')
            df.drop_duplicates(inplace=True)
            logger.info("Done dropping unnecessary columns")

            cat_cols = self.config["data_processing"]["categorical_columns"]
            num_cols = self.config["data_processing"]["numerical_columns"]

            logger.info("Applying Label Encoding to categorical columns")
            labelEncoder = LabelEncoder()
            mappings = {}

            for col in cat_cols: 
                if col in df.columns:  # Corrected column existence check
                    df[col] = labelEncoder.fit_transform(df[col]) 
                    mappings[col] = {label: code for label, code in zip(labelEncoder.classes_, labelEncoder.transform(labelEncoder.classes_))}
                else:    
                    logger.warning(f"Column {col} not found in DataFrame")

            logger.info("Label Mappings are:")
            for col, mapping in mappings.items():
                logger.info(f"{col}: {mapping}")
            
            logger.info("Handling skewness in numerical columns")
            skewness_threshold = self.config["data_processing"]["skewness_threshold"]
            skewness = df[num_cols].apply(lambda x: x.skew())

            for column in skewness[skewness > skewness_threshold].index:
                df[column] = np.log1p(df[column])

            return df
            print(df.dtypes)
        
        except Exception as e:
            logger.error(f"Error in data processing: {e}")
            raise CustomException("Data processing failed", e)
        
    def balance_data(self, df):
        try:
            logger.info("Balancing data using SMOTE")
            X = df.drop(columns='booking_status')  # Corrected column name
            y = df['booking_status']

            smote = SMOTE(random_state=42)
            X_resampled, y_resampled = smote.fit_resample(X, y)
            balanced_df = pd.DataFrame(X_resampled, columns=X.columns)
            balanced_df['booking_status'] = y_resampled

            logger.info("Data balancing completed")
            return balanced_df
        
        except Exception as e:
            logger.error(f"Error in balancing data: {e}")
            raise CustomException("Data balancing failed", e)
        
    def select_features(self, df):
        try:
            logger.info("Starting Feature selection")

            X = df.drop(columns='booking_status')
            y = df['booking_status']

            model = RandomForestClassifier(random_state=42)
            model.fit(X, y)

            feature_importance = model.feature_importances_
            feature_importance_df = pd.DataFrame({'feature': X.columns, 
                                                  'importance': feature_importance})
            top_feature_importance_df = feature_importance_df.sort_values(by='importance', ascending=False)
            
            num_features = self.config["data_processing"]["no_of_features"]
            top_features = top_feature_importance_df["feature"].head(num_features).tolist()

            logger.info(f"Features selected: {top_features}")

            top_df = df[top_features + ['booking_status']]

            logger.info("Feature selection completed")
            return top_df
        
        except Exception as e:
            logger.error(f"Error in feature selection: {e}")
            raise CustomException("Feature selection failed", e)

    def save_data(self, df, filepath):
        try:
            logger.info(f"Saving processed data to {filepath}")
            df.to_csv(filepath, index=False)
            logger.info("Data saved successfully")
        except Exception as e:
            logger.error(f"Error in saving data: {e}")
            raise CustomException("Data saving failed", e)
        
    def process(self):
        try:
            logger.info("Loading data from RAW directory")

            train_df = load_data(self.train_path)
            test_df = load_data(self.test_path)

            train_df = self.preprocess_data(train_df)
            test_df = self.preprocess_data(test_df)

            train_df = self.balance_data(train_df)

            train_df = self.select_features(train_df)
            test_df = test_df[train_df.columns]

            self.save_data(train_df, PROCESSED_TRAIN_DATA_PATH)  # Fixed typo
            self.save_data(test_df, PROCESSED_TEST_DATA_PATH)
            logger.info("Data processing completed successfully")

        except Exception as e:
            logger.error(f"Error in data processing pipeline: {e}")
            raise CustomException("Data processing failed", e)

if __name__ == "__main__":
    processor = DataProcessor(TRAIN_FILE_PATH, TEST_FILE_PATH, PROCESSED_DIR, CONFIG_PATH)
    processor.process()