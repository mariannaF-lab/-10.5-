import os
from typing import Dict
from openai import OpenAI

MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

# Инициализация клиента через переменные окружения (или явно передайте api_key в OpenAI(...))
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_post(topic: str, max_tokens: int = 1600) -> Dict[str, str]:
    # 1) Заголовок
    r_title = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": f"Придумайте привлекательный заголовок для поста на тему: {topic}"}],
        max_tokens=60,
        temperature=0.7,
    )
    title = r_title.choices[0].message.content.strip()

    # 2) Мета-описание
    r_meta = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": f"Напишите краткое информативное мета-описание для поста с заголовком: {title}"}],
        max_tokens=120,
        temperature=0.7,
    )
    meta = r_meta.choices[0].message.content.strip()

    # 3) Полный пост
    prompt_post = (
        f"Напишите подробный и увлекательный пост для блога на тему: {topic}. "
        f"Используйте короткие абзацы, подзаголовки (H2/H3), примеры и ключевые слова "
        f"для лучшего восприятия и SEO. В конце добавьте краткий вывод и список из 3–5 тегов."
    )
    r_post = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": prompt_post}],
        max_tokens=max_tokens,
        temperature=0.7,
    )
    post = r_post.choices[0].message.content.strip()

    return {"title": title, "meta_description": meta, "post_content": post}
