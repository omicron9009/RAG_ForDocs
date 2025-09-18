from typing import Dict, List
from llama_cpp import Llama

class TinyLlamaGenerator:
    def __init__(self, model_path: str = "./models/tinyllama-1.1b-chat-v1.0.Q6_K.gguf", n_ctx: int = 2048):
        print("🧠 Loading TinyLLaMA GGUF...")
        self.model = Llama(
            model_path=model_path,
            n_ctx=n_ctx,
            n_threads=8,   # set based on your CPU
            n_gpu_layers=0  # set to 0 for pure CPU
        )

    def generate_response(self, role: str, task: str, chunks: List[Dict], max_tokens: int = 512) -> str:
        context_text = "\n".join([c["chunk_text"] for c in chunks])

        prompt = f"""Role: {role}
Task: {task}
Context:
{context_text}

What are the most relevant sections and insights?
"""

        output = self.model(
            prompt,
            max_tokens=max_tokens,
            temperature=0.7,
            top_p=0.9,
            stop=["</s>"],  # you can add more stop tokens if needed
        )

        return output["choices"][0]["text"].strip()


# # ============= BATCH ========================
# import threading
# import queue
# import atexit
# from concurrent.futures import Future
# from typing import List, Dict, Any

# from llama_cpp import Llama

# class TinyLlamaGenerator:
#     """
#     A generator class for TinyLLaMA that uses a transparent background worker
#     to automatically batch requests for maximum throughput, without changing the
#     public-facing API.
#     """
#     def __init__(
#         self,
#         model_path: str = "./models/tinyllama-1.1b-chat-v1.0.Q6_K.gguf",
#         n_ctx: int = 2048,
#         batch_size: int = 8,
#         max_wait_time: float = 0.1
#     ):
#         """
#         Initializes the model and the background batching worker.
#         """
#         print("🧠 Loading TinyLLaMA GGUF model...")
#         self.model = Llama(
#             model_path=model_path,
#             n_ctx=n_ctx,
#             n_threads=8,
#             n_gpu_layers=0,
#             n_batch=batch_size,
#             verbose=False
#         )
#         print("✅ Model loaded successfully.")

#         self.batch_size = batch_size
#         self.max_wait_time = max_wait_time
#         self.request_queue = queue.Queue()
#         self.shutdown_event = threading.Event()

#         self.worker_thread = threading.Thread(target=self._batch_worker, daemon=True)
#         self.worker_thread.start()

#         atexit.register(self.shutdown)

#     def _create_prompt(self, role: str, task: str, context_text: str) -> str:
#         """Helper function to create a consistently formatted prompt."""
#         return f"""<|system|>
# You are an expert assistant. Your role is {role}.</s>
# <|user|>
# Based on the following context, please perform this task: {task}.

# Context:
# ---
# {context_text}
# ---

# Provide the most relevant sections and insights based on your role and task.</s>
# <|assistant|>
# """

#     def _batch_worker(self):
#         """The background worker loop that processes requests in batches."""
#         while not self.shutdown_event.is_set():
#             batch_requests = []
#             try:
#                 first_req = self.request_queue.get(timeout=self.max_wait_time)
#                 batch_requests.append(first_req)

#                 while len(batch_requests) < self.batch_size:
#                     batch_requests.append(self.request_queue.get_nowait())
#             except queue.Empty:
#                 if not batch_requests:
#                     continue

#             prompts = [req['prompt'] for req in batch_requests]
#             futures = [req['future'] for req in batch_requests]
#             params = batch_requests[0]['params']

#             try:
#                 responses = []
#                 for prompt in prompts:
#                     output = self.model.create_completion(
#                         prompt=prompt,
#                         max_tokens=params.get('max_tokens', 512),
#                         temperature=params.get('temperature', 0.7),
#                         top_p=params.get('top_p', 0.9),
#                         stop=params.get('stop', ["</s>", "<|user|>"]),
#                     )
#                     responses.append(output["choices"][0]["text"].strip())

#                 for i, future in enumerate(futures):
#                     future.set_result(responses[i])

#             except Exception as e:
#                 print(f"🔥 Error processing batch: {e}")
#                 for future in futures:
#                     future.set_exception(e)

#     def generate_response(self, role: str, task: str, chunks: List[Dict], max_tokens: int = 512) -> str:
#         """
#         Generates a single response by adding the request to a batching queue
#         and waiting for the result. The I/O of this method is unchanged.
#         """
#         context_text = "\n".join([c["chunk_text"] for c in chunks])
#         prompt = self._create_prompt(role, task, context_text)
        
#         future = Future()
        
#         self.request_queue.put({
#             "prompt": prompt,
#             "future": future,
#             "params": {
#                 "max_tokens": max_tokens,
#                 "temperature": 0.7,
#                 "top_p": 0.9,
#                 "stop": ["</s>", "<|user|>"],
#             }
#         })
        
#         return future.result()

#     def shutdown(self):
#         """Signals the background worker to shut down."""
#         print("Shutting down batch worker...")
#         self.shutdown_event.set()