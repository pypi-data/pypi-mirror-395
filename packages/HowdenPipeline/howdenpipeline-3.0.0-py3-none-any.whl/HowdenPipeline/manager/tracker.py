import os
from dotenv import load_dotenv
import mlflow

class Tracker:
    def __init__(self, logger_type: str, project_name: str = None):
        """
        Initialize either LangSmith or MLflow logging.
        logger_type: 'langsmith', 'mlflow', or 'none'
        """
        load_dotenv()
        self.logger_type = logger_type
        if logger_type.lower() == "langsmith":
            from langsmith import Client
            from langsmith.utils import LangSmithError

            os.environ["LANGCHAIN_TRACING_V2"] = "true"
            langsmith_key = os.getenv("LANGCHAIN_API_KEY")
            if not langsmith_key:
                raise ValueError("LANGCHAIN_API_KEY not set in .env or environment variables")

            os.environ["LANGSMITH_ENDPOINT"] ="https://eu.api.smith.langchain.com"
            os.environ["LANGCHAIN_API_KEY"] = langsmith_key

            try:
                client = Client()

                projects = list(client.list_projects())  # This will fail if token is invalid
                print("✅ Token is valid. Accessible projects:")
                for p in projects:
                    print("-", p.name)
            except LangSmithError as e:
                print("❌ Token is invalid or unauthorized.")
                print(e)
            except Exception as e:
                print("❌ Could not connect to LangSmith.")
                print(e)
        elif logger_type.lower() == "mlflow":
            mlflow.set_tracking_uri(os.getenv("MLFLOW_TRACKING_URI", "file:./mlruns"))
            mlflow.set_experiment(project_name)
            mlflow.start_run()
            print(f"[MLflow] Tracking enabled for project: {project_name}")

        elif logger_type.lower() == "none":
            print("[Logger] No logging enabled.")
        else:
            raise ValueError(f"Unsupported logger_type: {logger_type}")


    def log_artifacts(self, file):
        mlflow.log_artifact(file, artifact_path="metadata")

    def log_metrics(self, metrics: dict):
        """
        Log metrics to the chosen logger.
        """
        if self.logger_type.lower() == "mlflow":
            mlflow.log_metrics(metrics)
        elif self.logger_type.lower() == "langsmith":
            # LangSmith logs automatically from LangChain; no manual logging needed
            pass


    def log_params(self, logger_type: str, params: dict):
        """
        Log parameters to the chosen logger.
        """
        if logger_type.lower() == "mlflow":
            mlflow.log_params(params)
        elif logger_type.lower() == "langsmith":
            pass  # Automatic from LangChain


    def end_logger(self, logger_type: str):
        """
        Close/finish logging if required.
        """
        if logger_type.lower() == "mlflow":
            mlflow.end_run()
