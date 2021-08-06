from sshtunnel import SSHTunnelForwarder
import pymongo
import pprint
import datetime
import numpy as np
import matplotlib.pyplot as plt

MONGO_HOST = "fusion.hs-fulda.de"
MONGO_DB = "fusion"
MONGO_USER = "root"
print("Data Evaluation")
server = SSHTunnelForwarder(
    MONGO_HOST,
    ssh_username=MONGO_USER,
    remote_bind_address=('127.0.0.1', 27017)
)

server.start()

client = pymongo.MongoClient('127.0.0.1', server.local_bind_port) # server.local_bind_port is assigned local port
db = client[MONGO_DB]
pprint.pprint(db.collection_names())

exercise_collection = "exercises"

data = list(db[exercise_collection].find({ "date": { "$gt": datetime.datetime.fromisoformat('2021-07-26'),
                                        "$lt": datetime.datetime.fromisoformat('2021-08-01') }}))
print(len(data))
from collections import defaultdict


groups = defaultdict(list)

for obj in data:
    groups[obj["user"]].append(obj)

new_list = groups.values()
#print(new_list)

# data preprocessing
j = 0
steps_per_user = []
print(len(new_list))
for user in new_list:
    j = j + 1
    exercise_dates = [x["date"] for x in user]
    # print(exercise_dates)
    steps = [x["steps"] for x in user]
    steps_mean = np.mean(steps)
    date_now = datetime.datetime.now().date()
    date_7_days = (datetime.datetime.now() - datetime.timedelta(7)).date()
    
    # print("Before >>>>>>>>>>>>>>>>>>>>>>>>>>><", user)
    i = 0
    while date_now > date_7_days:
        dates_entered = [date_now for u in user if u["date"].date() == date_now]
        if len(dates_entered) == 0:

            user.append({
                "steps": steps_mean,
                "date": datetime.datetime.now() - datetime.timedelta(i),
                "user": user[0]["user"]
            })
        i = i + 1
        date_now = (date_now - datetime.timedelta(1))

        # print("After >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>", user)
        # print("After >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> New user")


    # Date sorting
    user.sort(key=lambda r: r["date"])
    
    days = [u["date"].strftime('%A') for u in user]
    steps = [u["steps"] for u in user]
    steps_per_user.append(steps)
    
    plt.plot(days, steps, label = f"user {j}")

plt.xlabel('Day')
# naming the y axis
plt.ylabel('Steps')
# giving a title to my graph
plt.title('No. of steps per day')
  
# show a legend on the plot
plt.legend()
  
# function to show the plot
plt.show()

# Plot Mean 

mean_by_day = []
sd_by_day = []
steps_per_user_np = np.array(steps_per_user)
print("Steps per user", steps_per_user_np)


for i in range(0,7):
    mean_by_day.append(np.mean(steps_per_user_np[:,i]))

plt.plot(days, mean_by_day, label = "mean")
plt.xlabel('Day')
# naming the y axis
plt.ylabel('Steps')
# giving a title to my graph
plt.title('No. of steps per day')
  
# show a legend on the plot
plt.legend()
  
# function to show the plot
plt.show()

# Plot standard deviation
std_steps = np.std(steps_per_user_np, axis=0) 
std_steps_plus = mean_by_day + std_steps
std_steps_minus = mean_by_day - std_steps

plt.plot(days, mean_by_day, label = "mean")
plt.plot(days, std_steps_plus, label = "standard deviation upper")
plt.plot(days, std_steps_minus, label = "standard deviation lower")
plt.xlabel('Day')
# naming the y axis
plt.ylabel('Steps')
# giving a title to my graph
plt.title('std')
  
# show a legend on the plot
plt.legend()
  
# function to show the plot
plt.show()

server.stop()