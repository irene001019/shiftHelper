
import os
import subprocess
import sys

def run_tests():
    tests_dir = "tests"
    if not os.path.exists(tests_dir):
        print(f"❌ Directory '{tests_dir}' not found.")
        return

    files = [f for f in os.listdir(tests_dir) if f.startswith("verify_") and f.endswith(".py")]
    
    if not files:
        print("⚠️ No test files found in 'tests/'")
        return

    print(f"🔍 Found {len(files)} test(s). Running them now...\n")
    
    passed = 0
    failed = 0

    for test_file in files:
        print(f"▶️ Running {test_file}...")
        path = os.path.join(tests_dir, test_file)
        
        # We need to set PYTHONPATH so tests can import modules from parent dir
        env = os.environ.copy()
        env["PYTHONPATH"] = os.getcwd()
        
        result = subprocess.run([sys.executable, path], env=env, capture_output=True, text=True)
        
        if result.returncode == 0:
            print(f"✅ {test_file} PASSED")
            passed += 1
        else:
            print(f"❌ {test_file} FAILED")
            print("--- Output ---")
            print(result.stdout)
            print(result.stderr)
            print("--------------")
            failed += 1
        print("")

    print(f"🏁 Summary: {passed} Passed, {failed} Failed")

if __name__ == "__main__":
    run_tests()
