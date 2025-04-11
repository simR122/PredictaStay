import os
import pandas as pd
import joblib
from sklearn.model_selection import RandomizedSearchCV
import lightgbm as lgb
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score
from src.logger import get_logger
from src.custom_exception import CustomException
from config.paths_config import *
from config.model_params import *
from utils.common_functions import read_yaml, load_data

import mlflow
import mlflow.sklearn

logger = get_logger(__name__)

class ModelTraining:

    def __init__(self, train_path,test_path, model_output_path):
        self.train_path = train_path
        self.test_path = test_path
        self.model_output_path = model_output_path

        self.params_dist = LIGHTGBM_PARAMS
        self.random_search_params = RANDOM_SEARCH_PARAMS

    def load_and_split_data(self):
        try:
            logger.info(f"Loading data from  {self.train_path}")
            train_df = load_data(self.train_path)

            logger.info(f"Loading data from  {self.test_path}")
            test_df = load_data(self.test_path)

            X_train = train_df.drop(columns=['booking_status'])
            y_train = train_df['booking_status']

            X_test = test_df.drop(columns=['booking_status'])
            y_test = test_df['booking_status']
            logger.info(f"Data splitted successfully for model training")    

            return X_train, y_train, X_test, y_test
        
        except Exception as e:
            logger.error(f"Error in loading and splitting data: {str(e)}")
            raise CustomException(f"Failed to load data: {str(e)}")
        
    def train_lgbm(self, X_train, y_train):
        try:
            logger.info("Initializing our model")

            lgbm_model = lgb.LGBMClassifier(random_state = self.random_search_params['random_state'])


            random_search = RandomizedSearchCV(
                estimator=lgbm_model,
                param_distributions=self.params_dist,
                n_iter=self.random_search_params['n_iter'],
                cv=self.random_search_params['cv'],
                n_jobs=self.random_search_params['n_jobs'],
                verbose=self.random_search_params['verbose'],
                random_state=self.random_search_params['random_state'],
                scoring=self.random_search_params['scoring']
            )

            logger.info("Starting our hyperparameter tuning")

            random_search.fit(X_train, y_train)

            logger.info("Model training completed successfully")

            best_params = random_search.best_params_
            best_lgbm_model = random_search.best_estimator_

            logger.info(f"Best parameters found: {best_params}")
            return best_lgbm_model
        
        except Exception as e:
            logger.error(f"Error in training model: {str(e)}")
            raise CustomException(f"Failed to train model: {str(e)}")
        
    def evaluate_model(self, model, X_test, y_test):
        try:
            logger.info("Evaluating the model")

            y_pred = model.predict(X_test)

            accuracy = accuracy_score(y_test, y_pred)
            f1 = f1_score(y_test, y_pred)
            precision = precision_score(y_test, y_pred)
            recall = recall_score(y_test, y_pred)

            logger.info(f"Model evaluation metrics: Accuracy: {accuracy}")
            logger.info (f"F1 Score: {f1}")
            logger.info(f"Precision: {precision}")
            logger.info(f"Recall: {recall}")

            return {
                "accuracy": accuracy,
                "f1_score": f1,
                "precision": precision,
                "recall": recall
            }
        
        except Exception as e:
            logger.error(f"Error in evaluating model: {str(e)}")
            raise CustomException(f"Failed to evaluate model: {str(e)}")

    def save_model(self, model):
        try:
            os.makedirs(os.path.dirname(self.model_output_path), exist_ok=True)

            logger.info(f"Saving the model at {self.model_output_path}")
            joblib.dump(model, self.model_output_path)

            logger.info("Model saved successfully")

        except Exception as e:
            logger.error(f"Error in saving model: {str(e)}")
            raise CustomException(f"Failed to save model: {str(e)}")

    def run(self):
        try:
            with mlflow.start_run():
                logger.info("Starting the model training pipeline")
                logger.info("Starting out mlflow experiment")
               
                logger.info("Loading the training and testing dataset to MLflow")
                mlflow.log_artifact(self.train_path, artifact_path="datasets")
                mlflow.log_artifact(self.test_path, artifact_path="datasets")

                X_train, y_train, X_test, y_test = self.load_and_split_data()
                best_lgbm_model = self.train_lgbm(X_train, y_train)
                metrices = self.evaluate_model(best_lgbm_model, X_test, y_test)
                self.save_model(best_lgbm_model)

                logger.info("Logging the model to MLflow")
                mlflow.log_artifact(self.model_output_path, artifact_path="models")
                
                logger.info("Logging the model parameters and metrics to MLflow")
                mlflow.log_params(best_lgbm_model.get_params())
                mlflow.log_metrics(metrices)
                logger.info("Model training process completed successfully")

        except Exception as e:
            logger.error(f"Error in model training process: {str(e)}")
            raise CustomException(f"Failed to run model training: {str(e)}")
        
if __name__ == "__main__":
    try:
        trainer = ModelTraining(PROCESSED_TRAIN_DATA_PATH, PROCESSED_TEST_DATA_PATH, MODEL_OUTPUT_PATH)
        trainer.run()

    except Exception as e:
        logger.error(f"Error in main execution: {str(e)}")
        raise CustomException(f"Failed to execute main: {str(e)}")