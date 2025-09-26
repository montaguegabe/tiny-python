from tiny_python import Executor

executor = Executor()

# Test simple augmented assignment
code = """
x = 5
x
"""
print("First test (assignment):", executor.execute(code))

# Now test augmented
executor = Executor()  # Fresh executor
code2 = """
x = 5
x += 3
x
"""
try:
    result = executor.execute(code2)
    print("Augmented assignment result:", result)
except Exception as e:
    print("Augmented assignment error:", e)
    import traceback
    traceback.print_exc()
