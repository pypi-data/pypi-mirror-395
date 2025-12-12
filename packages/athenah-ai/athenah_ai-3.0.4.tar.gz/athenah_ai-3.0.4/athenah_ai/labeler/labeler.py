import os
import json
import logging
from typing import Dict, Any, List, Set

from athenah_ai.client import AthenahClient, MODEL_MAP
from athenah_ai.utils.tokens import get_token_total

from basedir import basedir

logger = logging.getLogger("app")


def safe_json_loads(s: str):
    """
    Attempts to extract and load valid JSON from a string.
    If not possible, returns None.
    """
    try:
        # Remove code block markers and language hints
        s = s.strip()
        if s.startswith("```"):
            s = s.lstrip("`")
            # Remove language hint if present
            if s.startswith("json"):
                s = s[4:]
            s = s.strip()
        # Remove trailing code block if present
        if s.endswith("```"):
            s = s[:-3].strip()
        return json.loads(s)
    except Exception as e:
        logger.error(f"safe_json_loads error: {e} | input: {s}")
        return None


class AICodeLabeler:
    language_extensions = {
        ".py": "python",
        ".cpp": "cpp",
        ".c": "c",
        ".js": "javascript",
        ".ts": "typescript",
        ".h": "c header",
        # Add more as needed
    }

    def __init__(
        self,
        storage_type: str,
        id: str,
        dir: str,
        name: str,
        version: str,
    ):
        self.storage_type = storage_type
        self.id = id
        self.dir = dir
        self.name = name
        self.version = version
        self.base_path = os.path.join(basedir, dir)
        self.name_path = os.path.join(self.base_path, name)
        self.source_path = os.path.join(self.name_path, f"{name}-source")
        self.client = AthenahClient(self.id, self.dir)

    def process_directories(self, directories: List[str], max_retries: int = 3) -> None:
        processed_files: Set[str] = set()
        failed_files: Set[str] = set()
        for rel_dir in directories:
            abs_dir = os.path.join(self.source_path, rel_dir)
            self._process_directory(abs_dir, processed_files, failed_files, max_retries)

    def _count_lines(self, file_path: str) -> int:
        with open(file_path, "r", encoding="utf-8") as f:
            return sum(1 for _ in f)

    def _summarize_file(
        self, file_name: str, content: str, classes: dict, functions: dict, args: dict
    ) -> str:
        response_template = '{ "description": "file_description" }'
        prompt = f"""
        Summarize the {file_name} file:
        [CODE]
        {content}
        [/CODE]

        FileName: {file_name}
        Classes: {classes}
        Functions: {functions}
        Arguments: {args}

        Response Template:
        {response_template}

        Instructions:

        - Do not include code blocks or markdown
        - If the list of points is empty return []
        - Return valid json only, no extra text
        """
        ai_response = self.client.base_prompt(None, prompt)
        json_data = safe_json_loads(ai_response)
        if not json_data or not isinstance(json_data, dict):
            json_data = {"description": ""}
        return json_data.get("description", "")

    def _extract_functions(self, content: str) -> List[Dict[str, Any]]:
        response_template = """
        [{
            "name": "function_name",
            "args": ["list of arguments"],
            "lineno": starting_line_number
        }]
        """
        prompt = f"""
        List all functions in the `source_code.txt`:

        [CODE]
        {content}
        [/CODE]

        Response format:
        {response_template}

        Instructions:

        - Do not include code blocks or markdown
        - If the list of functions is empty return []
        - Return valid json only, no extra text
        """
        ai_response = self.client.base_prompt(None, prompt)
        json_data = safe_json_loads(ai_response)
        if not json_data or not isinstance(json_data, list):
            json_data = []
        return json_data

    def _extract_namespaces(self, content: str) -> List[Dict[str, Any]]:
        response_template = """
        [{
            "name": "namespace_name"
        }]
        """
        prompt = f"""
        List all namespaces in the `source_code.txt`:

        [CODE]
        {content}
        [/CODE]

        Response format:
        {response_template}

        Instructions:

        - Do not include code blocks or markdown
        - If the list of namespaces is empty return []
        - Return valid json only, no extra text
        """
        ai_response = self.client.base_prompt(None, prompt)
        json_data = safe_json_loads(ai_response)
        if not json_data or not isinstance(json_data, list):
            json_data = []
        return json_data

    def _extract_classes(self, content: str) -> List[Dict[str, Any]]:
        response_template = """
        [{
            "name": "class_name",
            "constructors": "list of constructors",
            "lineno": starting_line_number
        }]
        """
        prompt = f"""
        List all classes in the `source_code.txt`:

        [CODE]
        {content}
        [/CODE]

        Response format:
        {response_template}

        Instructions:

        - Do not include code blocks or markdown
        - If the list of classes is empty return []
        - Return valid json only, no extra text
        """
        ai_response = self.client.base_prompt(None, prompt)
        json_data = safe_json_loads(ai_response)
        if not json_data or not isinstance(json_data, list):
            json_data = []
        return json_data

    def _extract_args(self, content: str) -> List[Dict[str, Any]]:
        response_template = """
        [{
            "name": "arg_or_var_name",
            "lineno": starting_line_number
        }]
        """
        prompt = f"""
        List all arguments and variables used in the `source_code.txt`:

        [CODE]
        {content}
        [/CODE]

        Response format:
        {response_template}

        Instructions:

        - Do not include code blocks or markdown
        - If the list of args is empty return []
        - Return valid json only, no extra text
        """
        ai_response = self.client.base_prompt(None, prompt)
        json_data = safe_json_loads(ai_response)
        if not json_data or not isinstance(json_data, list):
            json_data = []
        return json_data

    def _process_file(self, file_path: str, file_name: str) -> str:
        file_ext = os.path.splitext(file_name)[-2]
        _file_ext = ".".join([s for s in file_ext.split(".") if s != "txt"])
        _file_ext = _file_ext.split(".")[-1]
        language = self.language_extensions.get(f".{_file_ext}")
        logger.debug("file: {} language: {}".format(file_name, language))
        if language:
            with open(file_path, "r", encoding="utf-8") as f:
                source_code = f.read()
                classes = self._extract_classes(source_code)
                args = self._extract_args(source_code)
                functions = self._extract_functions(source_code)
                namespaces = self._extract_namespaces(source_code)
                description = self._summarize_file(
                    file_path, source_code, classes, functions, args
                )
                config = {
                    "file_path": file_path,
                    "description": description,
                    "namespaces": namespaces,
                    "language": language,
                    "functions": functions,
                    "args": args,
                    "classes": classes,
                }
                file_path_no_txt = file_path.replace(".txt", "")
                dest_file_path = f"{file_path_no_txt}.ai.json"
                with open(dest_file_path, "w") as f:
                    json.dump(config, f, indent=2, sort_keys=True)
                return dest_file_path
        return ""

    def _verify_file(
        self, file_path: str, result_path: str, max_attempts: int = 3
    ) -> bool:
        if not os.path.exists(file_path) or not os.path.exists(result_path):
            logger.error(
                f"Source or result file does not exist: {file_path}, {result_path}"
            )
            return False

        with open(file_path, "r", encoding="utf-8") as f:
            source_code = f.read()
        with open(result_path, "r", encoding="utf-8") as f:
            result_json = json.load(f)

        prompt_template = """
        You are an expert code reviewer. Given the following source code and its AI-generated summary/result,
        rate the accuracy of the result on a scale from 0 to 100, where 100 means perfect accuracy.
        ONLY Return a JSON response in the following format:
        {{
            "score": <integer 0-100>,
            "reason": "<short explanation>"
        }}

        Source code:
        [CODE]
        {source}
        [/CODE]

        AI Result:
        {result}
        """

        for attempt in range(1, max_attempts + 1):
            prompt = prompt_template.format(
                source=source_code, result=json.dumps(result_json, indent=2)
            )
            ai_response = self.client.base_prompt(None, prompt)
            response_json = safe_json_loads(ai_response)
            if not response_json or not isinstance(response_json, dict):
                logger.error(
                    f"Verification AI response error: Invalid format | {ai_response}"
                )
                return False
            score = response_json.get("score", 0)
            if score >= 80:
                return True

        return False

    def _process_directory(
        self,
        dir_path: str,
        processed_files: Set[str],
        failed_files: Set[str],
        max_retries: int = 1,
    ) -> None:
        MAX_TOKENS = MODEL_MAP["gpt-4.1"]
        oversized_files: List[str] = []
        for root, _, files in os.walk(dir_path):
            for file_name in files:
                file_path = os.path.join(root, file_name)
                if file_path.endswith(".ai.json"):
                    logger.debug(f"Skipping AI file: {file_path}")
                    continue

                if file_path in processed_files or file_path in failed_files:
                    continue

                ai_file_path = f"{file_path.replace('.txt', '')}.ai.json"
                if os.path.exists(ai_file_path):
                    logger.debug(f"Skipping existing AI file: {ai_file_path}")
                    continue

                total_lines = self._count_lines(file_path)
                logger.debug(f"File {file_name} has: {total_lines} lines")
                with open(file_path, "r", encoding="utf-8") as f:
                    source_code = f.read()
                    total_tokens = get_token_total(source_code)
                    if total_tokens > MAX_TOKENS:
                        logger.warning(
                            f"File {file_path} has {total_tokens} tokens, which exceeds the limit of {MAX_TOKENS} tokens."
                        )
                        oversized_files.append(file_path)
                        continue

                retries = 0
                while retries < max_retries:
                    result_path = self._process_file(file_path, file_name)
                    if not result_path:
                        failed_files.add(file_path)
                        break
                    verified = self._verify_file(file_path, result_path, max_attempts=3)
                    if verified:
                        processed_files.add(file_path)
                        break
                    else:
                        logger.warning(
                            f"Verification failed for {file_path}, retrying ({retries+1}/{max_retries})"
                        )
                        retries += 1
                if retries == max_retries:
                    failed_files.add(file_path)
        if oversized_files:
            print(f"Oversized files: {oversized_files}")
