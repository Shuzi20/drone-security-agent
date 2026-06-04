import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))
MODEL = "qwen/qwen3-32b"

def analyze_frame_with_vlm(frame):
    prompt = f"""You are a vision AI analyzing a drone surveillance frame.
    
Frame details:
- Time     : {frame['time']}
- Location : {frame['location']}
- Scene    : {frame['description']}

Identify and list:
1. All objects present (people, vehicles, animals, etc.)
2. Their actions or behavior
3. Any suspicious elements

Respond in this exact format:
OBJECTS: <comma separated>
BEHAVIOR: <what they are doing>
SUSPICIOUS: <yes/no — reason>
"""

    response = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2
    )

    result = response.choices[0].message.content

    # Remove DeepSeek think tags
    if "<think>" in result:
        result = result.split("</think>")[-1].strip()

    return result


def parse_vlm_response(response_text):
    objects = ""
    behavior = ""
    suspicious = "no"

    for line in response_text.strip().split("\n"):
        if line.startswith("OBJECTS:"):
            objects = line.replace("OBJECTS:", "").strip()
        elif line.startswith("BEHAVIOR:"):
            behavior = line.replace("BEHAVIOR:", "").strip()
        elif line.startswith("SUSPICIOUS:"):
            suspicious = line.replace("SUSPICIOUS:", "").strip()

    return objects, behavior, suspicious