# random python code
def fibonacci(n):
  if n <= 1:
    return n
  else:
    return fibonacci(n-1) + fibonacci(n-2)

# Example usage
result = fibonacci(10)
print(result)