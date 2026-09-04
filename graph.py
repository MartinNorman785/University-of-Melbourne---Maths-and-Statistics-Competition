import pickle
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np
from alternating_turns_nn import Network, Node, Connection

PRECISION = 1000

with open('ai2.pickle', 'rb') as file:
    n = pickle.load(file)


probs = [[n.run([x/PRECISION,y/PRECISION])[0] if y < x else np.nan for x in range(0, PRECISION)] for y in range(0, PRECISION)]
for y, row in enumerate(probs):
    zero = False
    for x, v in enumerate(row):
        if v < 0.5 and zero == False:
            zero = True
            probs[y][x] = 10**15
            print(x, y)


cmap = cm.Spectral
cmap.set_bad(color='white')
cmap.set_over(color='black')

fig, ax = plt.subplots()
image = ax.imshow(probs, cmap=cmap,vmin=0, vmax=1)
ax.invert_yaxis()




plt.colorbar(image, ax=ax)
plt.title('Ai likelihood to play at x and s values')
plt.xlabel('x')
plt.ylabel('s')


plt.show()
plt.savefig("nn2.png")
print("Plot saved as nn.png")
