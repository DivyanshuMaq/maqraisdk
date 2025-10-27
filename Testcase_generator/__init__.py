import azure.functions as func
from pydantic import BaseModel
import logging
from Application_insights import ApplicationInsightsLogger
import copy
import os
import json
import time
import sys
from dotenv import load_dotenv
from rai_agent.utility.promptTestcaseGenerator import promptTestcaseGenerator
from rai_agent.connections.open_ai import OpenAIClient
from rai_agent.success_metrics.task_success_rate import evaluate_testcases_and_calculate_metrics

class DatasetRequest(BaseModel):
    prompt: str
    number_of_testcases: int
    user_categories: list[str]
    need_metrics:bool
# Load local .env only for local debugging
load_dotenv()
try:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
except Exception:
    pass

# Create OpenAIClient
openai_client = OpenAIClient(
    key=os.getenv("OpenAI_Key"),
    openai_endpoint=os.getenv("OpenAI_endpoint"),
    deployment_name=os.getenv("OpenAI_deployment")
)
def estimate_tokens(text: str) -> int:
    """
    Estimate token count using a simple heuristic.
    While not as accurate as tiktoken, this provides a reasonable estimate
    for logging purposes.
    """
    if isinstance(text, (dict, list)):
        text = json.dumps(text)
    text = str(text)
    # Split on whitespace and punctuation
    words = text.split()
    # Estimate tokens (typically words are 1.3 tokens)
    return int(len(words) * 1.3)
 
def count_tokens(text: str) -> int:
    """Count tokens using a simple estimation method"""
    return estimate_tokens(text)
def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('testcase generator agent function received request.')
    logger=ApplicationInsightsLogger()
    start_time = time.time()
    try:
        body=req.get_json()
        dataset=DatasetRequest(**body)
        prompt = dataset.prompt
        number_of_testcases = getattr(dataset, "number_of_testcases", 2)
        categories = getattr(dataset, "user_categories", []) 
        need_metrics=getattr(dataset,"need_metrics",False)
        input_tokens=count_tokens(prompt)
        logger.track_event("Input Parameters",properties={
            "Event": "Test Case Generation Started",
            "Input Type": "TestCase Generator",
            "System Prompt": prompt,
            "Number of Testcases": str(number_of_testcases),
            "Categories Selected": str(categories),
            "Input Tokens": str(input_tokens),
        })
        tcgenerator = promptTestcaseGenerator(openaiClient=openai_client)
        api_start=time.time()
        result = tcgenerator.generate(prompt=prompt,
            num_cases=number_of_testcases,
            categories=categories,
            verbose=False)
        api_latency=round(time.time()-api_start,2)
        try:
            if isinstance(result, dict):
                logging.info(f"Generator result keys: {list(result.keys())}")
            else:
                preview = str(result)
                if isinstance(result, str):
                    preview = result[:200]
                logging.info(f"Generator result type: {type(result).__name__}, preview: {preview}")
        except Exception:
            pass
        filtered_result = copy.deepcopy(result)
        # Remove any tasks that are not dicts to keep structure consistent
        keys_to_delete = []
        for task, content in filtered_result.items():
            if not isinstance(content, dict):
                if str(task).lower() == "error":
                    preview = str(content)
                    if isinstance(content, str):
                        preview = content[:200]
                    logging.warning(f"Generator returned error: {preview}")
                    # Preserve 'error' key for client visibility
                    continue
                logging.warning(f"Skipping task {task}, unexpected type: {type(content)}")
                keys_to_delete.append(task)
                continue

            test_cases = content.get("test_cases")
            if not isinstance(test_cases, dict):
                logging.warning(f"Task {task} missing 'test_cases'. Content: {content}")
                continue

            for category, cases in test_cases.items():
                if not isinstance(cases, list):
                    logging.warning(f"Skipping category {category}, expected list but got {type(cases)}")
                    continue

                for case in cases:
                    if isinstance(case, dict):
                        case.pop("ExpectedOutput", None)

        # Purge non-dict tasks (except 'error')
        for k in keys_to_delete:
            filtered_result.pop(k, None)

        execution_time=round(time.time()-start_time,2)
        output_tokens = count_tokens(filtered_result)
        total_tokens=input_tokens+output_tokens
        # Lightweight structure logging
        try:
            top_keys = list(filtered_result.keys())
            logging.info(f"Generated task keys: {top_keys}")
            if top_keys:
                first_task = filtered_result.get(top_keys[0], {})
                tc = first_task.get("test_cases") if isinstance(first_task, dict) else None
                if not isinstance(tc, dict):
                    inferred = {}
                    if isinstance(first_task, dict):
                        for kk, vv in first_task.items():
                            if isinstance(vv, list):
                                inferred[kk] = vv
                    tc = inferred if inferred else {}
                cat_keys = list(tc.keys()) if isinstance(tc, dict) else []
                logging.info(f"First task category keys: {cat_keys}")
                if cat_keys:
                    first_list = tc.get(cat_keys[0], [])
                    if isinstance(first_list, list) and first_list:
                        first_item = first_list[0]
                        if isinstance(first_item, dict):
                            logging.info(f"First testcase item keys: {list(first_item.keys())}")
                        else:
                            logging.info(f"First testcase item type: {type(first_item).__name__}")
        except Exception:
            pass
        metrics = None
        if(need_metrics==True): 
            metrics = evaluate_testcases_and_calculate_metrics(filtered_result,prompt)
            logger.track_event("TestCase Metrics", properties={
                "Event": "TestCase Generation Complete",
                "Generated Test Cases": json.dumps(filtered_result, ensure_ascii=True),
                "Input Tokens": str(input_tokens),
                "Output Tokens": str(output_tokens),
                "Total Tokens": str(total_tokens),
                "Execution Time": str(execution_time),
                "API Latency": str(api_latency),
                "Task success rate": metrics,
            })
        else:
            logger.track_event("TestCase Metrics", properties={
                "Event": "TestCase Generation Complete",
                "Generated Test Cases": json.dumps(filtered_result, ensure_ascii=True),
                "Input Tokens": str(input_tokens),
                "Output Tokens": str(output_tokens),
                "Total Tokens": str(total_tokens),
                "Execution Time": str(execution_time),
                "API Latency": str(api_latency),
            })
        # Build response object without double-encoding
        response_obj = {"result": filtered_result}
        if need_metrics and metrics is not None:
            response_obj["metrics"] = metrics

        try:
            response_json = json.dumps(response_obj, ensure_ascii=False)
        except UnicodeEncodeError as e:
            logging.error(f"UnicodeEncodeError at position {e.start}: {repr(e.object[e.start:e.end])}")
            raise

        return func.HttpResponse(
            response_json,
            mimetype="application/json",
            status_code=200
        )
    except Exception as e:
        logging.error(f"Error in Testcase generator agent: {e}", exc_info=True)
        return func.HttpResponse(
            json.dumps({"error": str(e)}),
            mimetype="application/json",
            status_code=500
        )
