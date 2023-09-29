import hashlib

WORDS_FILE_NAME = "words.txt"
HASH = "a06ce9d5f2be23eb2c3584756068a5c9"
SALT = "a9d40596b6d4"

with open(WORDS_FILE_NAME, 'r') as file:
  words = [line.rstrip() for line in file]

hashes = [hashlib.md5((word + SALT).encode('utf-8')).hexdigest() for word in words]

print(hashes[0])

# try:
idx = hashes.index(HASH)
# except:
#   print("failed")
# finally:
print(words[idx])
