import sys
import unittest
from pathlib import Path

# Add project root to sys.path
root_dir = Path(__file__).resolve().parent
if str(root_dir) not in sys.path:
    sys.path.insert(0, str(root_dir))

import tests

def main():
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    test_modules = [
        "tests.test_memory_fs",
        "tests.test_router",
        "tests.test_security",
        "tests.test_creative_studio",
        "tests.test_prompt_understanding",
        "tests.test_parity"
    ]
    
    for mod in test_modules:
        try:
            suite.addTests(loader.loadTestsFromName(mod))
        except Exception as e:
            print(f"Warning: could not load {mod}: {e}")

    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    print(f"\nTest Execution Summary:")
    print(f"Ran: {result.testsRun} tests")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    
    if result.wasSuccessful():
        print("ALL TESTS PASSED (100% SUCCESS RATE)")
        sys.exit(0)
    else:
        print("TEST FAILURES DETECTED")
        sys.exit(1)

if __name__ == "__main__":
    main()
