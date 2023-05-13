import requests
from itertools import combinations_with_replacement
import nltk
import pickle

nltk.download("words")
words = nltk.corpus.words.words()

s = requests.Session()

req = requests.Request(
    "GET", "https://0ijq1i6sp1.execute-api.us-east-1.amazonaws.com/dev/stream"
).prepare()


# while True:
#     r = requests.get(
#         "https://0ijq1i6sp1.execute-api.us-east-1.amazonaws.com/dev/stream"
#     )
#     print(r.text)

# for i in range(7):
# res = s.send(req)
# for i in res.iter_lines():
# print(i)


try:
    with open("ramp_ctf_stream_letters", "rb") as file:
        letters = pickle.load(file)
except FileNotFoundError:
    letters = set()
    for _ in range(1):
        res = s.send(req)
        letters.add(res.text[1])

    with open("ramp_ctf_stream_letters", "wb") as file:
        pickle.dump(letters, file)


for possible_word in combinations_with_replacement(letters, 7):
    print("".join(possible_word))
    if "".join(possible_word) == "missing":
        print(possible_word)
