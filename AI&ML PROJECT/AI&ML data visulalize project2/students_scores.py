import requests
import matplotlib.pyplot as plt


URL = "https://696107c6e7aa517cb797d66d.mockapi.io/student"


response1 = requests.get(URL)
student = response1.json()

name = []
score = []

for student in student:
    name.append(student["name"])
    score.append(student["score"])


average_score = sum(score) / len(score)
print("Average Score:", average_score)

plt.bar(name, score)
plt.xlabel("Students")
plt.ylabel("Scores")
plt.title("Student Scores Bar Chart")
plt.show()
