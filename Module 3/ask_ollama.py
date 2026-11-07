from ollama import chat

local_model = "qwen2.5:0.5b"

user_question = "A train leaves Delhi at 9:00 AM at 60 km/h. Another leaves Mumbai at 10:00 AM at 80 km/h toward Delhi. The cities are 1400 km apart. When do they meet? " + "Show reasoning step by step, then give the final time."

response = chat(
    model=local_model,
    messages=[
        # {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": user_question}
    ],
    # max_tokens=500,
)

answer = response.message.content  
print(answer)
