import matplotlib.pyplot as plt
  




# line 1 points
x1 = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
y1 = [1408,1408,1408, 1408, 1408, 1408, 1408]
# plotting the line 1 points 
plt.plot(x1, y1, label = "line 1")

plt.xlabel('Day')
# naming the y axis
plt.ylabel('Steps')
# giving a title to my graph
plt.title('No. of steps per day')
  
# show a legend on the plot
plt.legend()
  
# function to show the plot
plt.show()
  
# # line 2 points
# x2 = ['Monday', 'Wednesday', 'Tuesday']
# y2 = [4,1,3]
# # plotting the line 2 points 
# plt.plot(x2, y2, label = "line 2")
  
# # naming the x axis
# plt.xlabel('x - axis')
# # naming the y axis
# plt.ylabel('y - axis')
# # giving a title to my graph
# plt.title('Two lines on same graph!')
  
# # show a legend on the plot
# plt.legend()
  
# # function to show the plot
# plt.show()
