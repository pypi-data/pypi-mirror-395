import inspect

def system(content):
    return {"role": "system", "content": inspect.cleandoc(content)}

def user(content):
    return {"role": "user", "content": inspect.cleandoc(content)}

def assistant(content):
    return {"role": "assistant", "content": inspect.cleandoc(content)}
