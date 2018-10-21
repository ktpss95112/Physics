from functions import *

init()

plot_F()

plot_pst(0, 1)
plot_pst(-4, 1)
plot_pst(4, -1)

print_amplitude_and_period()


plt.xticks(range(x_left_bound-1, x_right_bound+2, 1))
plt.show()
