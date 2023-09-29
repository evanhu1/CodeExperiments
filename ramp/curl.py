import requests
import string

# for c in list(string.ascii_lowercase):
#   query = f'H{c}llo'
#   r = requests.get(f'https://0ijq1i6sp1.execute-api.us-east-1.amazonaws.com/dev/exception?q={query}')
#   print(f'{c} {r.content}')

with open("42words.txt", 'r') as file:
  words = [line.rstrip() for line in file]

words = list(filter(lambda x: len(x) == 7 and not 'l' in x, words))
print(words)