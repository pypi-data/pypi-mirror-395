import logging
import mimetypes
import time
from pathlib import Path
from typing import Any, Dict, Optional, Tuple

import requests
from openai import OpenAI
from pydantic import BaseModel

logger = logging.getLogger(__name__)


class NubixAI:
    def __init__(
        self,
        docling_api_key: str,
        openai_api_key: str,
        docling_url: str = "https://api.nubixdocuments.nl",
        timeout: int = 500,
        poll_interval: float = 2.0
    ):
        self.docling_api_key = docling_api_key
        self.openai_api_key = openai_api_key
        self.docling_url = docling_url
        self.timeout = timeout
        self.poll_interval = poll_interval
        self._openai_client = OpenAI(api_key=openai_api_key)

    def call_docling_process_file(
        self,
        file_path: str,
        file_type: Optional[str] = None,
    ) -> Tuple[str, Optional[Dict[str, Any]]]:
        """
        Verstuurt een bestand naar docling en ontvangt markdown + metadata.

        Parameters:
            file_path (str): Pad naar het bronbestand (bijv. .pdf)
            file_type (str): Optioneel MIME type van het bestand

        Returns:
            Tuple[str, Optional[Dict]]: (markdown_text, metadata_dict)

        Raises:
            requests.HTTPError: Als de server een fout retourneert
            ValueError: Als de respons geen markdown bevat
        """
        path = Path(file_path)
        if not path.exists():
            raise FileNotFoundError(f"Bestand niet gevonden: {file_path}")

        if not file_type:
            file_type, _ = mimetypes.guess_type(path.name)
            if not file_type:
                file_type = "application/octet-stream"

        headers = {
            "x-api-key": self.docling_api_key,
            "Accept": "application/json, text/markdown;q=0.9, */*;q=0.1",
        }

        process_url = f"{self.docling_url.rstrip('/')}/async/process_file"
        status_url_template = f"{self.docling_url.rstrip('/')}/jobs/{{job_id}}/status"
        result_url_template = f"{self.docling_url.rstrip('/')}/jobs/{{job_id}}/result"

        with path.open("rb") as f:
            files = {
                "file": (path.name, f, file_type)
            }
            data = {
                "file_type": file_type
            }
            resp = requests.post(process_url, headers=headers, files=files, data=data, timeout=self.timeout)
            resp.raise_for_status()

        job_payload = resp.json()
        job_id = job_payload.get("job_id")
        if not job_id:
            raise ValueError("Docling respons bevat geen job_id.")

        logger.info(f"Docling job gestart: {job_id}, status: {job_payload.get('status')}")

        deadline = time.monotonic() + self.timeout

        while True:
            if time.monotonic() > deadline:
                raise TimeoutError(f"Docling verwerking voor job {job_id} duurde langer dan {self.timeout} seconden.")

            status_resp = requests.get(status_url_template.format(job_id=job_id), headers=headers, timeout=self.timeout)
            status_resp.raise_for_status()
            status_data = status_resp.json()

            status = status_data.get("status")
            logger.info(f"Docling job {job_id} status: {status}")

            if status == "completed":
                break
            if status == "failed":
                error_message = status_data.get("error") or "Onbekende fout"
                raise RuntimeError(f"Docling verwerking mislukt voor job {job_id}: {error_message}")

            time.sleep(self.poll_interval)

        # Result endpoint is the only way to retrieve markdown; status payload never includes it.
        result_url = result_url_template.format(job_id=job_id)
        while True:
            if time.monotonic() > deadline:
                raise TimeoutError(f"Docling resultaat ophalen voor job {job_id} duurde langer dan {self.timeout} seconden.")

            result_resp = requests.get(result_url, headers=headers, timeout=self.timeout)
            if result_resp.status_code == 409:
                logger.info(f"Docling resultaat voor job {job_id} nog niet vrijgegeven, opnieuw proberen.")
                time.sleep(self.poll_interval)
                continue
            if result_resp.status_code == 404:
                raise RuntimeError(f"Docling resultaat niet gevonden voor job {job_id}.")

            result_resp.raise_for_status()
            result_payload = result_resp.json()
            result_data = result_payload.get("result") or {}
            markdown_text = result_data.get("markdown")
            metadata = result_data.get("metadata")
            if not markdown_text or not markdown_text.strip():
                raise ValueError("Lege markdown ontvangen van docling.")
            return markdown_text, metadata

    def extract_with_llm(self, markdown_text: str, prompt_input: str, PydanticInput: BaseModel) -> BaseModel:
        prompt = (f"{prompt_input} \n"
            f"{markdown_text}"
        )
        return self._openai_client.responses.parse(
            model="gpt-5.1",
            input=prompt,
            text_format=PydanticInput,
            reasoning={ "effort": "low" },
            text={ "verbosity": "low" },
            store = False
        )