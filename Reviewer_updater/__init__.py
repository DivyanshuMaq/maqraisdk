import azure.functions as func
from pydantic import BaseModel
from Application_insights import ApplicationInsightsLogger
import logging
import os
import json
import time
import requests
from dotenv import load_dotenv
from rai_agent.utility.promptReviewer import PromptReviewer
from rai_agent.utility.promptUpdater import PromptUpdater
from rai_agent.connections.open_ai import OpenAIClient
from rai_agent.success_metrics.compliance import calculate_compliance_score_single

class DatasetRequest(BaseModel):
    prompt: str
    need_metrics:bool
# Load local .env only for local debugging
load_dotenv()

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
    logging.info('Reviewer_Updater agent function received request.')
    logger=ApplicationInsightsLogger()
    start_time = time.time()
    try:
        body = req.get_json()
        dataset=DatasetRequest(**body)
        
        input_tokens = count_tokens(dataset.prompt)
        logging.info(f"Dataset parsed: {dataset}")
        logger.track_event("Input Parameters",properties={
            "Event": "Initial Prompt Review Started",
            "Prompt": dataset.prompt,
            "Input Tokens": str(input_tokens),
            "Input Type": "Prompt Reviewer",
        })
        
        reviewer = PromptReviewer(openaiClient=openai_client)
        api_start=time.time()
        result1 = reviewer.review(dataset.prompt)
        api_latency = round(time.time() - api_start, 2)
        output_tokens = count_tokens(result1)
        total_tokens = input_tokens + output_tokens
        if(dataset.need_metrics==True):
            initial_compliance_score = calculate_compliance_score_single(result1)
        execution_time = round(time.time() - start_time, 2)
        if(dataset.need_metrics==True):
            logger.track_event("Initial Prompt Review Metrics", properties={
                "Event": "Initial Prompt Review Complete",
                "Reviewe of Initial Prompt": json.dumps(result1, ensure_ascii=False),
                "Input Tokens": str(input_tokens),
                "Output Tokens": str(output_tokens),
                "Total Tokens": str(total_tokens),
                "Execution Time": str(execution_time),
                "API Latency": str(api_latency),
                "XPIA Status": result1.get("XPIA", {}).get("status", ""),
                "Groundedness Status": result1.get("Groundedness", {}).get("status", ""),
                "Jailbreak Status": result1.get("Jailbreak", {}).get("status", ""),
                "Harmful Content Status": result1.get("HarmfulContent", {}).get("status", ""),
                "initial_compliance_score": initial_compliance_score
            })
        else:
            logger.track_event("Initial Prompt Review Metrics", properties={
                "Event": "Initial Prompt Review Complete",
                "Reviewe of Initial Prompt": json.dumps(result1, ensure_ascii=False),
                "Input Tokens": str(input_tokens),
                "Output Tokens": str(output_tokens),
                "Total Tokens": str(total_tokens),
                "Execution Time": str(execution_time),
                "API Latency": str(api_latency),
                "XPIA Status": result1.get("XPIA", {}).get("status", ""),
                "Groundedness Status": result1.get("Groundedness", {}).get("status", ""),
                "Jailbreak Status": result1.get("Jailbreak", {}).get("status", ""),
                "Harmful Content Status": result1.get("HarmfulContent", {}).get("status", "")
            })
        updater = PromptUpdater(openaiClient=openai_client)
        api_start2=time.time()
        result2 = updater.update(dataset.prompt,feedback=result1)
        api_latency = round(time.time() - api_start2, 2)
 
        execution_time = round(time.time() - start_time, 2)
        output_tokens = count_tokens(result2)
        total_tokens = input_tokens + output_tokens
        logger.track_event("Updater Metrics", properties={
            "Event": "Prompt Update Complete",
            "Updated Prompt": json.dumps(result2, ensure_ascii=False),
            "Input Tokens": str(input_tokens),
            "Output Tokens": str(output_tokens),
            "Total Tokens": str(total_tokens),
            "Execution Time": str(execution_time),
            "API Latency": str(api_latency)
        })
        # Handle result2 safely to avoid KeyError
        if isinstance(result2, dict) and "updatedPrompt" in result2:
            result2_text = result2["updatedPrompt"]
        else:
            # Log the actual structure for debugging
            logger.track_event("Updater Result Debug", properties={
                "Event": "Unexpected result2 structure",
                "Result2 Type": str(type(result2)),
                "Result2 Content": json.dumps(result2, ensure_ascii=False) if isinstance(result2, dict) else str(result2),
                "Available Keys": list(result2.keys()) if isinstance(result2, dict) else "Not a dict"
            })
            # If result2 is a dict but doesn't have updatedPrompt, try common alternatives
            if isinstance(result2, dict):
                result2_text = result2.get("updated_prompt") or result2.get("prompt") or str(result2)
            else:
                result2_text = str(result2)
        api_start3=time.time()
        result3 = reviewer.review(result2_text)
        api_latency = round(time.time() - api_start3, 2)
        output_tokens = count_tokens(result3)
        total_tokens = input_tokens + output_tokens
        updated_compliance_score = calculate_compliance_score_single(result3)
        execution_time=round(time.time()-start_time,2)
        if(dataset.need_metrics==True):
            logger.track_event("Review Metrics", properties={
                "Event": "Updated Prompt Review Complete",
                "Reviewed Prompt": json.dumps(result3, ensure_ascii=False),
                "Input Tokens": str(input_tokens),
                "Output Tokens": str(output_tokens),
                "Total Tokens": str(total_tokens),
                "Execution Time": str(execution_time),
                "API Latency": str(api_latency),
                "XPIA Status": result3.get("XPIA", {}).get("status", ""),
                "Groundedness Status": result3.get("Groundedness", {}).get("status", ""),
                "Jailbreak Status": result3.get("Jailbreak", {}).get("status", ""),
                "Harmful Content Status": result3.get("HarmfulContent", {}).get("status", ""),
                "updated_compliance_score": updated_compliance_score
            })
        else:
            logger.track_event("Review Metrics", properties={
                "Event": "Updated Prompt Review Complete",
                "Reviewed Prompt": json.dumps(result3, ensure_ascii=False),
                "Input Tokens": str(input_tokens),
                "Output Tokens": str(output_tokens),
                "Total Tokens": str(total_tokens),
                "Execution Time": str(execution_time),
                "API Latency": str(api_latency)
            })
        if(dataset.need_metrics==True):
            return func.HttpResponse(
                json.dumps({
                    "review_result": result1,
                    "initial_compliance_score": initial_compliance_score,
                    "updated_result": result2,
                    "review_of_updated_prompt":result3,
                    "updated_compliance_score":updated_compliance_score
                }),
                mimetype="application/json",
                status_code=200
            )
        return func.HttpResponse(
                json.dumps({
                    "review_result": result1,
                    "updated_result": result2,
                    "review_of_updated_prompt":result3
                }),
                mimetype="application/json",
                status_code=200
            )
    except Exception as e:
        logging.error(f"Error in Updater agent: {e}", exc_info=True)
        return func.HttpResponse(
            json.dumps({"error": str(e)}),
            mimetype="application/json",
            status_code=500
        )
