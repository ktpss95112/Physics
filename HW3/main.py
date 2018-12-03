from functions import Homework, plt

# task 3
Homework((0.1, 0, -0.1), (0, 0, 0), 'task_3.png')

# task 4
Homework((0, 0, 0), (0.2, -0.2, 0.2), 'task_4.png')

# task 5
Homework((0.4, -0.1, -0.3), (0.5, -0.4, 0.2), 'task_5_x.png')
Homework((0.4, -0.1, -0.3), (0.5, -0.4, 0.2), 'task_5_q.png', draw_q=True)

plt.xticks(range(0, 7))
plt.show()
