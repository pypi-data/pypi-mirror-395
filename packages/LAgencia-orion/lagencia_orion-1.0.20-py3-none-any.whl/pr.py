from pathlib import Path

path = Path().resolve()

print(path)

path = Path().resolve(__file__).parent

print(path)
