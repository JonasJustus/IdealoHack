from sklearn import svm
import random

ok = []

for i in range(0, 100):
    s = []
    for i in range(3):
        s.append(random.randrange(85, 200))
    ok.append(s)

error = []


for i in range(0, 100):
    s = []
    for i in range(3):
        s.append(random.randrange(1, 100))
    error.append(s)

len_ok = len(ok)
len_error = len(error)
results = []

for i in range(len_ok):
    results.append(1)

for j in range(len_error):
    results.append(0)

embedded_vectors = ok + error

clf = svm.SVC()

clf.fit(embedded_vectors, results)

s = []

for i in range(0, 3):
    s.append(198)


print(clf.predict([s]))
