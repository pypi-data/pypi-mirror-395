# import time
# import json
# import asyncio
# from typing import Dict, Any
#
# from pydantic import BaseModel
#
# from levelapp.config.interaction_request import EndpointConfig
# from levelapp.core.base import BaseRepository
# from levelapp.simulator.schemas import ScriptsBatch
# from levelapp.core.evaluator import JudgeEvaluator
# from levelapp.core.simulator import ConversationSimulator
# from levelapp.aspects.monitoring import MonitoringAspect, MetricType
# from levelapp.core.session import EvaluationSession
#
#
# SESSION = "test_session"
#
#
# class StorageService(BaseRepository):
#
#     def fetch_stored_results(
#             self,
#             user_id: str,
#             collection_id: str,
#             project_id: str,
#             category_id: str,
#             batch_id: str
#     ) -> Dict[str, Any]:
#         """Empty method."""
#         pass
#
#     def save_batch_test_results(
#             self,
#             user_id: str,
#             project_id: str,
#             batch_id: str,
#             data: Dict[str, Any]
#     ) -> None:
#         """Empty method."""
#         pass
#
#     def retrieve_document(
#             self,
#             sub_collection_id: str,
#             document_id: str,
#             doc_type: str
#     ) -> BaseModel:
#         """Empty method."""
#         pass
#
#
# evaluation_service = JudgeEvaluator()
# storage_service = StorageService()
# endpoint_configuration = EndpointConfig()
#
# conversation_simulator = ConversationSimulator(
#     storage_service=storage_service,
#     evaluation_service=evaluation_service,
#     endpoint_configuration=endpoint_configuration,
# )
#
#
# def read_json_file(file_path: str):
#     import json
#     try:
#         with open(file_path, 'r') as f:
#             data = json.load(f)
#             return data
#
#     except FileNotFoundError:
#         print(f"[read_json_file] Error: File not found at {file_path}")
#
#     except json.JSONDecodeError:
#         print(f"[read_json_file] Error: Invalid JSON format in {file_path}")
#
#
# if __name__ == '__main__':
#
#     with EvaluationSession(session_name=SESSION, monitor=MonitoringAspect) as session:
#         print(f"Starting Evaluation Session: {SESSION}")
#         with session.step("setup"):
#             time.sleep(1)
#
#         with session.step("data_loading"):
#             json_data = read_json_file(file_path="../data/conversation_example_1.json")
#             test_batch = ScriptsBatch(
#                 scripts=json_data['scripts'],
#             )
#             results = asyncio.run(conversation_simulator.run(test_batch=test_batch))
#
#         with session.step(step_name="simulation", category=MetricType.API_CALL):
#             results = asyncio.run(conversation_simulator.run(test_batch=test_batch))
#
#         with session.step(step_name="scoring", category=MetricType.SCORING):
#             time.sleep(2)
#
#         with session.step("reporting"):
#             time.sleep(1)
#
#         # Retrieve all stats
#         stats = MonitoringAspect.get_all_stats()
#         print(f"All Monitoring Stats:\n{json.dumps(stats, indent=2)}\n{'---' * 10}\n\n")
#
#         execution_history = MonitoringAspect.get_execution_history(category=MetricType.API_CALL)
#         for rec in execution_history:
#             dump = rec.to_dict()
#             print(f"{json.dumps(dump, indent=4)}\n---")
