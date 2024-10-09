from llama_cpp import Llama
from youtube_transcript_api import YouTubeTranscriptApi
import time

start_time = time.time()

video_id = 'qWbHSOplcvY'

def get_transcript_as_string(video_id):
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        # Concatenate all text entries into a single string
        full_transcript = " ".join(entry['text'] for entry in transcript)
        return full_transcript
    except Exception as e:
        print(f"Error: {e}")
        return None
    
transcript_string = get_transcript_as_string(video_id)

if transcript_string:
    print(transcript_string)

llm = Llama.from_pretrained(
	# repo_id="ggml-org/Meta-Llama-3.1-8B-Instruct-Q4_0-GGUF",
	# filename="meta-llama-3.1-8b-instruct-q4_0.gguf",

	repo_id="hugging-quants/Llama-3.2-1B-Instruct-Q4_K_M-GGUF",
	filename="llama-3.2-1b-instruct-q4_k_m.gguf",

    n_ctx=4096 # 4096 is the maximum context length
)
# Define the context (this would typically come from your retrieval mechanism)
context = transcript_string

# Combine the retrieved context with the user's question
user_query = """
this is autogenerated transcript from audio, what are the ingredients? in json format

Based on the provided transcript, extract all the ingredients mentioned.
Provide the answer strictly in valid JSON format like this:
{
    "ingredients": [
        {"name": "ingredient1", "quantity": "amount"},
        {"name": "ingredient2", "quantity": "amount"},
        // ... more ingredients
    ]
}

"""
prompt_with_context = f"Context: {context}\n\nUser: {user_query}"

# Generate a completion using the context and user's question
response = llm.create_chat_completion(
    messages=[
        {
            "role": "user",
            "content": prompt_with_context
        }
    ]
)


# Print the model's response
print(response)
print(type(response))
# pretty print dict
import json
print(json.dumps(response, indent=4))

end_time = time.time()
print(f"Runtime of the program is {end_time - start_time}")