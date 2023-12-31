def logger(func):
    def wrapper(*args, **kwargs):
        print(f"Executing {func.__name__}...")
        result = func(*args, **kwargs)
        print(f"{func.__name__} has finished executing.")
        return result

    return wrapper

@logger
def add(a, b):
    return a + b

# Example usage
result = add(3, 4)
print(f"Result: {result}")
