# agents/ollama_base_agent.py
import requests
import json
import time

class OllamaBaseAgent:
    def __init__(self, name, role, model="mistral:latest"): 
        self.name = name
        self.role = role
        self.model = model
        self.ollama_url = "http://localhost:11434/api/generate"
        self.max_retries = 4
    
    def think(self, context, system_prompt):
        """Make agent think using Ollama with retry logic"""
        
        full_prompt = f"""{system_prompt}

{context}

Respond ONLY with valid JSON. No markdown, no code blocks, just pure JSON."""

        payload = {
            "model": self.model,
            "prompt": full_prompt,
            "stream": False,
            "format": "json",  # Force JSON output
            "options": {
                "temperature": 0.7,
                #"num_predict": 256  # Limit response length for speed
            }
        }
        
        # Retry logic with exponential backoff
        for attempt in range(self.max_retries):
            try:
                timeout = 120  # 120s per attempt
                response = requests.post(self.ollama_url, json=payload, timeout=timeout)
                response.raise_for_status()
                result = response.json()
                
                # Extract the generated text
                generated_text = result.get('response', '{}')
                
                # Clean up any markdown artifacts
                generated_text = generated_text.replace('```json', '').replace('```', '').strip()
                
                return generated_text
                
            except requests.exceptions.Timeout:
                if attempt < self.max_retries - 1:
                    wait_time = 2 ** attempt  # Exponential backoff: 1s, 2s, 4s
                    print(f"   ⏳ {self.name} timeout, retrying in {wait_time}s... (attempt {attempt + 1}/{self.max_retries})")
                    time.sleep(wait_time)
                else:
                    print(f"❌ {self.name} error: Timeout after {self.max_retries} attempts")
                    return '{"error": "Agent failed to respond"}'
            except Exception as e:
                print(f"❌ {self.name} error: {e}")
                return '{"error": "Agent failed to respond"}'
        
        return '{"error": "Agent failed to respond"}'