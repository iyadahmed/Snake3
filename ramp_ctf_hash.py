import nltk
from hashlib import md5

hashes_and_salts = [
    ("71e11b9221c6b84e503ebe913d097762", "04670f78b155"),
    ("65be18357fcf5f80269813009b6a7e68", "4aaf289046e8")
]

nltk.download("words")
words = nltk.corpus.words.words()

for word in words:
    if len(word) == 7:
        for target_hash, salt in hashes_and_salts:
            if md5((word + salt).encode()).hexdigest().lower() == target_hash:
                print(word)
