import torch
import torch.nn as nn
import numpy as np
import matplotlib.pyplot as plt
import networkx as nx

#predict model
class LSTM(nn.Module):
    def __init__(self, input_dim, hidden_dim, num_layers, output_dim, offset, seq_len):
        super(LSTM, self).__init__()
        self.hidden_dim = hidden_dim
        self.num_layers = num_layers
        #self.batch_size = batch_size
        self.offset = offset
        self.seq_len = seq_len
        self.lstm = nn.LSTM(input_dim, hidden_dim, num_layers, batch_first=True)
        self.fc = nn.Linear(hidden_dim, output_dim)

    def forward(self, x):
        h0 = torch.zeros(self.num_layers, x.size(0), self.hidden_dim).requires_grad_()
        c0 = torch.zeros(self.num_layers, x.size(0), self.hidden_dim).requires_grad_()
        out, (hn, cn) = self.lstm(x, (h0.detach(), c0.detach()))
        out = self.fc(out[:, self.seq_len - self.offset - 1:, :])
        #out = self.fc(out)
        return out
#sampling part
def ifS0CoverNextiEvenly(s0, next_i, delta, u, u_bound):
    #if covered, u will be updated
    #next_i is 1 minute with 13 datapoint
    next_i_arr=np.array(next_i)
    for j in range(len(s0)):
        #s_i is 1 minute with 13 datapoint
        s_i = np.array(s0[j])
        # calculate the difference
        diff = np.sqrt(np.square(next_i_arr[:] - s_i[:]).sum())
        if delta >= diff and (u[j] + 1)<=u_bound:
            u[j]+=1
            return True
    return False

def coverQbyNext(next, Q, delta1, u_bound):
    #brute force search to find the minimum subset of P covering Q
    len_min_s1 = float("inf")
    min_s1 = list()
    min_s1_u = list()
    min_s1_i=list()
    def dfs(j, sub, l):
        nonlocal len_min_s1
        nonlocal min_s1
        nonlocal min_s1_u
        nonlocal min_s1_i
        coverred, s1_u = ifS1CoverQEvenly(sub, Q, delta1, u_bound)
        if coverred and len(sub) < len_min_s1:
            len_min_s1 = len(sub)
            min_s1 = sub.copy()
            min_s1_u = s1_u.copy()
            min_s1_i=l.copy()
        for i in range(j, len(next)):
            next_i = next[i]
            sub.append(next_i)
            l.append(i)
            dfs(i+1, sub, l)
            sub.pop(-1)
            l.pop(-1)
    dfs(0, [], [])
    if len_min_s1 == float("inf"):
        print("Q can not be coverred by next")
        raise
    return min_s1, min_s1_u, min_s1_i
    
def ifS1CoverQEvenly(s1, Q, delta, u_bound):
    #check if s1 cover Q
    if len(s1)==0:
        return False, list()
    
    G = nx.DiGraph()
    for i in range(len(Q)):
        G.add_edge("s", "q{}".format(i), capacity=1)
    
    for i in range(len(s1)):
        G.add_edge("s1_{}".format(i), "t", capacity=int(u_bound))
    
    for i in range(len(Q)):
        for j in range(len(s1)):
            Q_i = np.array(Q[i])
            s1_i = np.array(s1[j])
            if delta >= np.sqrt(np.square(Q_i[:] - s1_i[:]).sum()):
                G.add_edge("q{}".format(i), "s1_{}".format(j), capacity=1)
    
    flow_value, flow_dict = nx.maximum_flow(G, "s", "t")
    #print("max flow:{}".format(flow_value))
    s1_u = list()
    if flow_value==len(Q):
        coverred = True
        for i in range(len(s1)):
            s1_u.append(flow_dict["s1_{}".format(i)]["t"])
    else:
        coverred = False
         
    return coverred, s1_u

model_path = r'C:\Users\ductuan\wban-imple\hs2hs_n1_lr0_hidden_dim64_num_layers2_seqlen10_offset5_iteration0 (2)'
lr = 0.01
input_dim = 13
hidden_dim = 64
num_layers = 2
output_dim = 13
num_epochs = 1000
seq_len = 10 # sequence length
offset = 5
# Instantiate model
model = LSTM(input_dim=input_dim, hidden_dim=hidden_dim, output_dim=output_dim, num_layers=num_layers, offset=offset, seq_len=seq_len)

# Load the saved model state dictionary
model.load_state_dict(torch.load(model_path))

# Set the model to evaluation mode
model.eval()


import joblib
scaler = joblib.load('scaler.pkl')

# Fit the scaler to data
# Transform data
# Predict the data
def processAndPredictData(scaler, list_5min):
    list=[]
    arr=test=np.array(list_5min)
    arr=scaler.fit_transform(arr)
    x = np.concatenate((arr, np.array([[0 for _ in range(13)] for _ in range(5 -1)])), axis=0)
    list.append(x)
    torch_l= torch.Tensor(np.array(list))
    with torch.no_grad():
        prediction = model(torch_l)
    predict_arr  = scaler.inverse_transform(prediction[0].numpy())
    predict_list= predict_arr.tolist()
    rounded_list = [[round(number, 1) for number in inner_list] for inner_list in predict_list]
    return rounded_list

from datetime import datetime
# Process the time into mm/dd/yy H:M:S form
def timeProcess(time_list):
    new_list=list()
    for time_org in time_list:
        datetime_part = ' '.join(time_org.split()[:5])

        dt_object = datetime.strptime(datetime_part, "%a %b %d %Y %H:%M:%S")
        formatted_string= f"{dt_object.month:02d}/{dt_object.day:02d}/{dt_object.year % 100:02d} {dt_object.hour}:{dt_object.minute:02d}:{dt_object.second:02d}"
        new_list.append(formatted_string)
    return new_list



pre_with_ground=list() #this include the prediction_list and replace with sampling
"""switch = 
            0: The phone will collect the data every minute
            1: The phone only collect the data 
"""
switch=1
indicators=[1 for _ in range(5)]
ground_Truth_h=list()
ground_Truth_t=list()
s0 = list()
s0_t= list()
u = list()
delta0=1
delta1=1
ubound=100
min_s1_u = list()
min_s1_i = list()
def executeSampling(delta0, delta1, ubound):
    global s0
    global scaler
    global u
    global pre_with_ground
    next = processAndPredictData(scaler, pre_with_ground[-5:])
    pre_with_ground+=next
    print(next)
    print(s0)
    print(u)
    min_s1_i=list()
    min_s1_u=list()
    Q = list()
    for next_i in next:
        if not ifS0CoverNextiEvenly(s0, next_i, delta0, u, ubound):
            Q.append(next_i)
    if len(Q)!=0:
        _, min_s1_u, min_s1_i = coverQbyNext(next, Q, delta1, ubound)
    return min_s1_u, min_s1_i
    

from datetime import datetime
import json
from flask import Flask, jsonify, request
import time
app = Flask(__name__)

@app.route('/')
def index():
    return "Python Flask Server is running!"
from threading import Lock
data_lock = Lock()

@app.route('/get-indicators', methods=['GET'])
def get_indicators():
    return jsonify({"indicators": indicators})

@app.route('/submit-data', methods=['POST'])
def submitData():
    # Receive collected data from the phone
    global ground_Truth_t
    global ground_Truth_h
    global s0
    global s0_t
    data = request.get_json(force=True)
    with data_lock:
        if switch==0:
            ground_Truth_h+=data.get('hearts')
            ground_Truth_t+=timeProcess(data.get('timestamp'))
            collectAllData()
        if switch==1:
            s0+=data.get('hearts')
            s0_t+=timeProcess(data.get('timestamp'))
            onlyCollectSampling()
    return jsonify({"message": "Data received successfully!"})


    return jsonify({"message": "Data received successfully!"})
def collectAllData():
    global indicators,delta0,delta1,ubound,u,ground_Truth_h,ground_Truth_t,s0, s0_t,pre_with_ground, min_s1_u,min_s1_i
    indicators=[0 for _ in range(5)]
    if len(ground_Truth_h)==5:
        s0= ground_Truth_h.copy()
        u = [1 for _ in range(5)]
        pre_with_ground= ground_Truth_h.copy()
        s0_t=ground_Truth_t.copy()
    else:
        u+=min_s1_u
        selected_data = [ground_Truth_h[-5+i] for i in min_s1_i]
        s0+= selected_data
        s0_t+= [ground_Truth_t[-5+i] for i in min_s1_i]
        for i, index in enumerate(min_s1_i):
            pre_with_ground[-5+index] = selected_data[i]
    min_s1_u, min_s1_i= executeSampling(delta0, delta1, ubound)
    with open('groundtruth_h_1.json', 'w') as f:
        json.dump(ground_Truth_h, f)
    with open('groundtruth_time_1.json', 'w') as f:
        json.dump(ground_Truth_t, f)
    with open('s0_1.json', 'w') as f:
        json.dump(s0, f)
    with open('s0_time_stamp_1.json', 'w') as f:
        json.dump(s0_t, f)
    with open('pre_with_ground_1.json', 'w') as f:
        json.dump(pre_with_ground, f)
    with open('u_1.json', 'w') as f:
        json.dump(u, f)
    return 

def onlyCollectSampling():
    global indicators,delta0,delta1,ubound,u,s0, s0_t,pre_with_ground,min_s1_u,min_s1_i
    indicators=[0 for _ in range(5)]
    if len(s0)==5:
        pre_with_ground=s0.copy()
        u = [1 for _ in range(5)]
    else:
        u+=min_s1_u
        for i, index in enumerate(min_s1_i):
            pre_with_ground[-5+index] = s0[-len(min_s1_i)+i]
    min_s1_u, min_s1_i= executeSampling(delta0, delta1, ubound)
    print(min_s1_i)
    for index in min_s1_i:
        indicators[index] = 1
    with open('s0_2.json', 'w') as f:
        json.dump(s0, f)
    with open('s0_time_stamp_2.json', 'w') as f:
        json.dump(s0_t, f)
    with open('pre_with_ground_2.json', 'w') as f:
        json.dump(pre_with_ground, f)
    with open('u_2.json', 'w') as f:
        json.dump(u, f)
    return 1

# Start a thread to periodically execute machine learning
if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=3000)