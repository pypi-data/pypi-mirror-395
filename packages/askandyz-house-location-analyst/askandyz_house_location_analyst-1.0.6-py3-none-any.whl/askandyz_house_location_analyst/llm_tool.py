import os

from dotenv import load_dotenv
from openai import OpenAI

from .config import default_model, SYSTEM_PROMPT

load_dotenv()

llm = OpenAI(
  api_key=os.getenv("DASHSCOPE_API_KEY", default="sk-xxx"),
  base_url=os.getenv("DASHSCOPE_BASE_URL", default="https://dashscope.aliyuncs.com/compatible-mode/v1"),
)


def llm_gen(user_prompt: str, system_prompt: str = SYSTEM_PROMPT, model: str = default_model) -> str:
  messages = [
    {"role": "system", "content": system_prompt},
    {"role": "user", "content": user_prompt},
  ]
  completion = llm.chat.completions.create(
    model=model,
    messages=messages,
    extra_body={"enable_thinking": False},
  )
  print(f"LLM Response Response: \n{completion}")
  return completion.choices[0].message.content


if __name__ == "__main__":
  # result = llm_gen(system_prompt="你是一个计算专家，请帮我讲解技术原理", user_prompt="AI 计算原理")
  result = llm_gen(system_prompt="你是一个计算专家，请帮我讲解技术原理", user_prompt="模型上下文协议MCP")
  print(result)
