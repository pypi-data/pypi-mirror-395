import os
import datetime
import yaml
import json


def get_log_dir():
    log_dir = os.getenv("COAUTHOR_AI_LOG_DIR")
    if not log_dir:
        log_dir = os.path.join(os.getcwd(), "tmp")
        os.makedirs(log_dir, exist_ok=True)
    return log_dir


def get_ai_request_id():
    counter_file_path = os.path.join(get_log_dir(), ".ai-prompt-counter")
    if not os.path.exists(counter_file_path):
        return 0
    with open(counter_file_path, "r", encoding="utf-8") as counter_file:
        return int(counter_file.read())


def next_ai_request_id():
    current_id = get_ai_request_id()
    new_id = current_id + 1
    counter_file_path = os.path.join(get_log_dir(), ".ai-prompt-counter")
    with open(counter_file_path, "w", encoding="utf-8") as counter_file:
        counter_file.write(str(new_id))
    return get_ai_request_id()


def get_ai_workflow_id():
    counter_file_path = os.path.join(get_log_dir(), ".ai-workflow-counter")
    if not os.path.exists(counter_file_path):
        return 0
    with open(counter_file_path, "r", encoding="utf-8") as counter_file:
        return int(counter_file.read())


def next_ai_workflow_id():
    current_id = get_ai_workflow_id()
    new_id = current_id + 1
    counter_file_path = os.path.join(get_log_dir(), ".ai-workflow-counter")
    with open(counter_file_path, "w", encoding="utf-8") as counter_file:
        counter_file.write(str(new_id))
    return get_ai_workflow_id()


def get_or_create_request_dir(workflow_id):
    log_dir = get_log_dir()
    workflow_str = f"{workflow_id:08d}"
    request_id = get_ai_request_id()
    request_str = f"{request_id:08d}"
    dir_path = os.path.join(log_dir, workflow_str, request_str)
    os.makedirs(dir_path, exist_ok=True)
    return dir_path, request_id


def save_messages(messages, model, kwargs, logger, workflow_id):
    dir_path, _ = get_or_create_request_dir(workflow_id)
    if not dir_path:
        return

    idx = 1  # counter for txt files
    processed_messages = []
    for msg in messages:
        processed_msg = msg.copy()
        content = processed_msg["content"]
        if isinstance(content, str):
            try:
                processed_msg["content"] = json.loads(content)
            except json.JSONDecodeError:
                # It's not JSON, save to file
                txt_path = os.path.join(dir_path, f"{idx}.txt")
                with open(txt_path, "w", encoding="utf-8") as f:
                    f.write(content)
                logger.debug(f"Message content written to: {txt_path}")

                # Truncate
                lines = content.splitlines()
                if len(lines) > 3:
                    truncated = "\n".join(lines[:3]) + "\n(lines deleted)"
                else:
                    truncated = "\n".join(lines)
                processed_msg["content"] = truncated
                idx += 1
        processed_messages.append(processed_msg)

    request = {"messages": processed_messages, "model": model, "kwargs": kwargs}  # , "kwargs": kwargs
    request_path = os.path.join(dir_path, "request.yml")
    with open(request_path, "w", encoding="utf-8") as file:
        yaml.dump(request, file, default_flow_style=False, allow_unicode=True)
    logger.debug(f"Messages → {request_path}")


def save_response(response, logger, workflow_id):  # , duration=None
    # def save_response(config, messages, model, response, logger, duration=None):
    # response = [[tc.model_dump() for tc in tool_calls] if tool_calls else None, content]
    dir_path, _message_id = get_or_create_request_dir(workflow_id)
    response_file_path = os.path.join(dir_path, "response.yml")
    with open(response_file_path, "w", encoding="utf-8") as file:
        yaml.dump(response.model_dump(), file, default_flow_style=False, allow_unicode=True)
    logger.info(f"Response → {response_file_path}")
    # data = {
    #     "messages": [{"role": msg["role"], "tokens": len(msg["content"].split())} for msg in messages],  # Count words
    #     "model": model,
    #     "response": response,
    #     "task": task,
    #     "date": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    #     "duration": duration,  # Add the duration to the data
    # }

    # task["ai-log-file"] = response_file_path

    # json_mode = task.get("json", False)
    # if json_mode:
    #     file_path = os.path.join(dir_path, f"{_message_id}-response.json")
    #     with open(file_path, "w", encoding="utf-8") as f:
    #         f.write(response)
    # else:
    #     file_path = os.path.join(dir_path, f"{_message_id}-response.txt")
    #     with open(file_path, "w", encoding="utf-8") as f:
    #         f.write(response)
    # logger.info(f"Response written to {'JSON' if json_mode else 'TXT'} file: {file_path}")
