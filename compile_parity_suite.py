import json
from gemini_flash_parity import GeminiFlashParityEngine

print("=== Starting Compilation of Janus Local Models for Gemini Flash 3 Parity ===")
res = GeminiFlashParityEngine.compile_all_local_models()
for model, details in res.items():
    print(f"\nModel: {model}")
    print(f"  Base Model: {details['base_model']}")
    print(f"  Tier: {details['tier']}")
    print(f"  Compiled: {details['compiled']}")
    print(f"  Log: {details['log'][:120]}...")

print("\n=== Parity Status ===")
status = GeminiFlashParityEngine.get_parity_status()
print(f"Status: {status['status']}")
print(f"Average Parity Score: {status['average_parity_score_pct']}% against {status['target_frontier_model']}")
print(f"Active Suite: {json.dumps(status['active_suite'], indent=2)}")
