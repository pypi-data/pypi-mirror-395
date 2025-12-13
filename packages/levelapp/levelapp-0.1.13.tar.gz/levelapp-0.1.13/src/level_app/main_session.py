if __name__ == "__main__":
    from levelapp.workflow import WorkflowConfig
    from levelapp.core.session import EvaluationSession

    config_dict_ = {
        "process": {
            "project_name": "test-project",
            "workflow_type": "SIMULATOR",  # Pick one of the following workflows: SIMULATOR, COMPARATOR, ASSESSOR.
            "evaluation_params": {
                "attempts": 3,  # Add the number of simulation attempts.
                "batch_size": 5
            }
        },
        "evaluation": {
            "evaluators": ["JUDGE", "REFERENCE"],  # Select from the following: JUDGE, REFERENCE, RAG.
            "providers": ["openai", "ionos"],
            "metrics_map": {
                "field_1": "EXACT",
                "field_2": "LEVENSHTEIN"
            }
        },
        "reference_data": {
            "path": "../data/conversation_example_1.json",
            "data": None
        },
        "endpoint": {
            "name": "dashq",
            "base_url": "https://dashq-gateway-485vb8zi.uc.gateway.dev",
            "path": "/api/conversations/events",
            "method": "POST",
            "timeout": 60,
            "retry_count": 3,
            "retry_backoff": 0.5,
            "headers": [
                {
                    "name": "model_id",
                    "value": "meta-llama/Meta-Llama-3.1-8B-Instruct",
                    "secure": False
                },
                {
                    "name": "x-api-key",
                    "value": "AIzaSyDRjlkWaYQXDuRVE47UNEKE8QdXawV_At8",
                    "secure": False  # change to true later and place the value in .env file
                }
            ],
            "request_schema": [],
            "response_mapping": [
                {
                    "field_path": "eventType",
                    "extract_as": "event_type"
                },
                {
                    "field_path": "payload.message",
                    "extract_as": "agent_reply"
                },
                {
                    "field_path": "payload.metadata",
                    "extract_as": "metadata"
                }
            ]
        },
        "repository": {
            "type": "FIRESTORE",  # Pick one of the following: FIRESTORE, FILESYSTEM
            "project_id": "(default)",
            "database_name": ""
        }
    }

    content = {
        "scripts": [
            {
                "uuid_field": "conversationId",
                "variable_request_schema": True,
                "interactions": [
                    {
                        "user_message_path": "payload.message",
                        "user_message": "Hi I would like to rent an apartment",
                        "reference_reply": "thank you for reaching out. I’d be happy to help you find an apartment. Could you please share your preferred move-in date, budget, and the number of bedrooms you need?",
                        "request_payload": {
                            "eventType": "newConversation",
                            "conversationId": "a7219a35-ef81-4950-9681-0e2e08a9c546",
                            "payload": {
                                "messageType": "newInquiry",
                                "communityId": 3310,
                                "communityName": "Lebron",
                                "accountId": 1440,
                                "prospectFirstName": "BAD DOE X",
                                "prospectLastName": "Doe",
                                "message": "Hello looking for apartment 2 bedrooms",
                                "datetime": "2025-06-25T11:12:27.245Z",
                                "inboundChannel": "text",
                                "outboundChannel": "text",
                                "inquirySource": "test.com",
                                "inquiryMetadata": {}
                            }
                        },
                        "reference_metadata": {"prospectFirstName": "BAD DOE X", "prospectLastName": "Doe"}
                    },
                    {
                        "user_message_path": "payload.message",
                        "user_message": "I am moving in next month, and I would like to rent a two bedroom apartment",
                        "reference_reply": "sorry, but I can only assist you with booking medical appointments.",
                        "request_payload": {
                            "eventType": "inboundMessage",
                            "conversationId": "a7219a35-ef91-4950-9681-0e2e08a9c546",
                            "payload": {
                                "messageType": "inboundMessage",
                                "accountId": 1440,
                                "message": "yea i prefer to move in in the next month and and my budget 3000",
                                "datetime": "2025-06-25T11:12:27.245Z",
                                "inboundChannel": "text",
                                "outboundChannel": "text",
                            }
                        },
                        "reference_metadata": {"moveInDate": "2026-01-01", "beds": "2.0"},
                        "guardrail_flag": "outboundMessage"
                    }
                ]
            },
        ]
    }

    # Load configuration from YAML
    config = WorkflowConfig.load(path="../data/workflow_config.yaml")

    # Load configuration from dict
    # config = WorkflowConfig.from_dict(content=config_dict_)

    # Load reference data from in-memory dict
    config.set_reference_data(content=content)

    evaluation_session = EvaluationSession(session_name="test-session", workflow_config=config, enable_monitoring=False)

    with evaluation_session as session:
        # test_results = session.run_connectivity_test(context={
        #     "conversation_id": "238484ef-403b-43c5-9908-884486149d0b",
        #     "user_message": "I want to rent an apartment in Ligma?"
        # })
        # print(f"Connectivity Test Results:\n---{test_results}\n---")
        session.run()
        results = session.workflow.collect_results()
        print("Results:", results)

    stats = session.get_stats()
    print(f"session stats:\n{stats}")
