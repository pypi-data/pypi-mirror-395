import os
import time
import json
from dotenv import load_dotenv
from .sdk import HybridLLM

load_dotenv()

def main():
    # 1. Config
    username = "YOUR_GITHUB_USERNAME" # <--- HARDCODE THIS or load from env
    gist_id = os.getenv("GIST_ID")
    secret_key = os.getenv("SECRET_KEY")

    if not gist_id or not secret_key:
        print("❌ CONFIG ERROR: Missing GIST_ID or SECRET_KEY in .env")
        return

    # 2. Init SDK
    print("📞 Contacting Service Discovery...")
    ai = HybridLLM(username, gist_id, secret_key)
    
    if not ai.base_url:
        print("❌ Could not find an active server.")
        return

    print("------------------------------------------------")
    print("💬 CHAT ACTIVE. Type 'quit' to exit.")
    print("------------------------------------------------")

    # 3. Chat Loop
    while True:
        try:
            prompt = input("\n👤 You: ")
            if prompt.strip().lower() in ['quit', 'exit']:
                break
            
            print("... generating ...")
            start = time.time()
            
            # Use the SDK method
            response = ai.generate(prompt)
            
            latency = time.time() - start
            print(f"🤖 AI ({latency:.1f}s): {response}")

        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()