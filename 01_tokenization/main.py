import tiktoken

enc = tiktoken.encoding_for_model('gpt-4o')
text = "hellow there"

tokens=enc.encode(text)

print(f"token {tokens}")