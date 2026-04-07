"""
OpenAI Client — Centralized LLM interface.
Loads OPENAI_API_KEY from azure/.env and exposes a reusable ask_llm() function.
"""

import os
import logging
from pathlib import Path
from dotenv import load_dotenv
from openai import OpenAI

# ---------------------------------------------------------------------------
# Environment
# ---------------------------------------------------------------------------
_ENV_PATH = Path(__file__).resolve().parent.parent / "azure" / ".env"
load_dotenv(_ENV_PATH)

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")

if not OPENAI_API_KEY:
    raise EnvironmentError(
        f"OPENAI_API_KEY not found. Ensure it is set in {_ENV_PATH}"
    )

# ---------------------------------------------------------------------------
# Client singleton
# ---------------------------------------------------------------------------
_client = OpenAI(api_key=OPENAI_API_KEY)

logger = logging.getLogger("agents.openai_client")

# ---------------------------------------------------------------------------
# Model configuration
# ---------------------------------------------------------------------------
DEFAULT_MODEL = "gpt-4o-mini"
MAX_COMPLETION_TOKENS = 2048
SYSTEM_IDENTITY = (
    "You are MNH Hospital AI Assistant — an intelligent, autonomous agent "
    "embedded in a hospital management system. You provide precise, "
    "actionable medical and administrative guidance. Be concise and professional. "
    "If the query is conversational, respond in natural human language. "
    "Only use JSON if specifically instructed by the prompt or response_format."
)


# ---------------------------------------------------------------------------
# Core LLM function
# ---------------------------------------------------------------------------
def ask_llm(
    prompt: str,
    *,
    system_prompt: str | None = None,
    model: str = DEFAULT_MODEL,
    max_tokens: int = MAX_COMPLETION_TOKENS,
    temperature: float = 0.4,
    response_format: dict | None = None,
) -> str:
    """Send a prompt to OpenAI and return the assistant's reply text.

    Parameters
    ----------
    prompt : str
        The user-facing message.
    system_prompt : str | None
        Override the default system prompt.
    model : str
        OpenAI model name (default ``gpt-4o-mini``).
    max_tokens : int
        Maximum completion tokens.
    temperature : float
        Sampling temperature.
    response_format : dict | None
        Optional ``{"type": "json_object"}`` for structured output.

    Returns
    -------
    str
        The assistant's reply content.
    """
    messages = [
        {"role": "system", "content": system_prompt or SYSTEM_IDENTITY},
        {"role": "user", "content": prompt},
    ]

    try:
        kwargs: dict = {
            "model": model,
            "messages": messages,
            "max_completion_tokens": max_tokens,
            "temperature": temperature,
        }
        if response_format:
            kwargs["response_format"] = response_format

        response = _client.chat.completions.create(**kwargs)
        return response.choices[0].message.content.strip()

    except Exception as exc:
        logger.exception("OpenAI API call failed: %s", exc)
        return f"[LLM Error] {exc}"
