import numpy as np
scores = np.random.randint(50, 100, (10, 5))  # 10 students, 5 subjects
print("Scores:\n", scores)
print("Mean Score:", np.mean(scores, axis=1)) # Mean per student
print("Highest Score:", np.max(scores, axis=1)) # Max per student