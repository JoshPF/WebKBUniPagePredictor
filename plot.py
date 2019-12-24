import matplotlib.pyplot as plt

num_keywords = [500, 5000, 10000, 25000, 50000]
accuracy = [74.7, 85.6, 93.9, 97.7, 97.7]
accuracy_other = [64.5, 74.0, 82.2, 87.7, 92.1]

plt.title('Misc. Universities (o for Accuracy, x for Accuracy w/ Other)')
plt.xlabel('Number of Keywords')
plt.ylabel('Accuracy')
plt.plot( [num_keywords], [accuracy], color='red', marker='o' )
plt.plot( [num_keywords], [accuracy_other], color='blue', marker='x' )
plt.show()

# 50000 keywords on Misc
accuracy_cats = [98.7, 100, 96, 93.5, 100, 99.5, 64.8]
x_axis = [1, 2, 3, 4, 5, 6, 7]
cat_xticks = ['course', 'department', 'faculty', 'project', 'staff', 'student', 'other']
plt.xticks(x_axis, cat_xticks)
plt.title('Misc. Universities / 50000 keywords - Categorical Accuracies')
plt.xlabel('Categories')
plt.ylabel('Accuracy')
plt.plot( [x_axis], [accuracy_cats], color='red', marker='o')
plt.show()
