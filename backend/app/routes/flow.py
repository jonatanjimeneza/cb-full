from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict, List
from app.services import openai_services
import logging
from app.models.chat_output import ChatOutput

router = APIRouter()

logging.basicConfig(level=logging.INFO)

class Edge(BaseModel):
    source: str
    target: str

class FlowData(BaseModel):
    nodes: Dict[str, dict]
    edges: List[Edge]

@router.post("/execute_flow")
async def execute_flow(flow_data: FlowData):
    try:
        logging.info("Received flow data: %s", flow_data)

        chat_input = None
        prompt = None
        openai_config = None
        chat_output = None

        for node_id, node_data in flow_data.nodes.items():
            logging.info("Processing node %s of type %s", node_id, node_data['type'])
            if node_data['type'] == 'chatInput':
                chat_input = node_data['data']
                logging.info("Chat input node found: %s", chat_input)
            elif node_data['type'] == 'prompt':
                prompt = node_data['data']
                logging.info("Prompt node found: %s", prompt)
            elif node_data['type'] == 'openai':
                openai_config = node_data['data']
                logging.info("OpenAI config node found: %s", openai_config)
            elif node_data['type'] == 'chatOutput':
                chat_output = node_id
                logging.info("Chat output node found with id: %s", chat_output)

        if not all([chat_input, openai_config, chat_output]):
            raise ValueError("Missing required nodes: chat_input, openai_config, or chat_output")

        # Combine the prompt and the user's input if a prompt node exists
        full_prompt = f"{prompt['promptTemplate']}\n\nUser: {chat_input['message']}" if prompt else chat_input['message']
        logging.info("Full prompt to be sent to OpenAI: %s", full_prompt)

        response = await openai_services.generate_openai_response(full_prompt, openai_config)
        logging.info("Response from OpenAI: %s", response)
        logging.info('response',chat_output)
        return {chat_output:{"message":response}}
        
    except ValueError as ve:
        logging.error("ValueError: %s", str(ve))
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        logging.error("Exception: %s", str(e))
        raise HTTPException(status_code=500, detail=str(e))
