import time
import random
from functools import wraps
from typing import Optional, Callable
from loguru import logger

def retry_on_size_integrity(base_delay: float = 0.8, max_retries: int = 3):
    def decorator(func: Callable):
        @wraps(func)
        def wrapper(self, file_key: str, *args, **kwargs) -> Optional[dict]:
            for attempt in range(max_retries):
                try:
                    file_context = func(self, file_key, *args, **kwargs)
                    if file_context:
                        expected_size = file_context.get('ContentLength', 0)
                        body = file_context['Body'].read() if 'Body' in file_context else b''
                        if expected_size > 0 and len(body) == expected_size:
                            file_context['Body'] = body
                            return file_context
                    logger.info(
                        f"[Intento {attempt+1}/{max_retries}], esperado: {expected_size}, recibido: {len(body)}"
                    )
                    if attempt < max_retries - 1:
                        delay = base_delay * (2 ** attempt)
                        delay += random.uniform(0, base_delay)
                        time.sleep(delay)
                except Exception as e:
                    if attempt < max_retries - 1:
                        delay = base_delay * (2 ** attempt)
                        delay += random.uniform(0, base_delay)
                        time.sleep(delay)
                        continue
                    raise
            raise RuntimeError(f"Descarga incompleta/inconsistente de S3 para {file_key}")
        return wrapper
    return decorator
