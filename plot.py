import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import pickle
def plot():
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    f = open("InputPoints_Example2.txt", "r")
    x_axis = []
    y_axis = []
    z_axis = []
    for i in f:
        tmp = i.split()
        x_axis.append(int(tmp[0]))
        y_axis.append(int(tmp[1]))
        z_axis.append(int(tmp[2]))
    f.close()

    f = open("InputEdges_Example2.txt", "r")
    for i in f:
        tmp = i.split()
        start_index = int(tmp[0])
        num_of_end_points = int(tmp[1])
        for j in range(3,3+num_of_end_points):
            line_x = []
            line_y = []
            line_z = []
            end_index = int(tmp[j])
            line_x.append(x_axis[start_index-1])
            line_y.append(y_axis[start_index-1])
            line_z.append(z_axis[start_index-1])
            line_x.append(x_axis[end_index-1])
            line_y.append(y_axis[end_index-1])
            line_z.append(z_axis[end_index-1])
            ax.plot3D(line_x, line_y, line_z, 'gray')
    f.close()

    ax.scatter3D(x_axis, y_axis, z_axis, 'blue',marker = 'o')

    #hide the axis
    plt.axis('off')

    plt.show()

output = open('image.pickle', 'wb')
pickle.dump(plot(),output)
output.close()
