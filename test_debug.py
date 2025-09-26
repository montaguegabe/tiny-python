from tiny_python import safe_exec

code = """
total = 0
print("total value:", total)
for i in range(1):
    print("before +=, total =", total, "i =", i)
    total += i
    print("after +=, total =", total)
total
"""

try:
    result = safe_exec(code)
    print("Result:", result)
except Exception as e:
    print("Error:", e)
    
# Simpler test
code2 = """
x = 5
x += 3
x
"""
try:
    result = safe_exec(code2)
    print("Simple augment result:", result)
except Exception as e:
    print("Simple augment error:", e)
