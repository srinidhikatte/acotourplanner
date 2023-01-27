from flask import Flask, redirect, url_for, request,render_template
import os
import re
import json
from random import randrange
import requests
from flask import request
from flask import jsonify

app = Flask(__name__)



@app.route('/home',methods=['GET','POST'])
def home():
    #os.popen('rm -f myfile.txt')
    ip=request.remote_addr
    print(ip)
    filename="tempfile"+ip+".txt"
    file1=open(filename,'a')
    if request.method == "POST":
     a=request.form
     #file1 = open('myfile.txt', 'w')
     for keys in a:
         file1.write(a[keys])
         file1.write("\n")
         #file1.close()
         
     print(len(a))
     return render_template("index.html")
    file1.close() 
    return render_template("index.html")

def fillzeros(l):
    alist=[]
    for i in range(l):
        alist.append(0)
    return alist    

def buildCostMatrix(timeCost):
   locations=[]
   ip=request.remote_addr
   filename="tempfile"+ip+".txt"

   with open(filename) as openfileobject:
    for line in openfileobject:
        locations.append(line)
   locationsString=''
   for ele in locations:
    locationsString=locationsString+ele+'|'
   locationsString=locationsString[:-1]
   file1=open('keyfile.txt','r')
   key=file1.read()
   file1.close()
   queryString="https://maps.googleapis.com/maps/api/distancematrix/json?origins="+locationsString+"&destinations="+locationsString+"&departure_time=now&key="+key
   payload={}
   headers = {}
   response = requests.request("GET", queryString, headers=headers, data=payload)
   data_json=response.json()
   timeCost=[]
   blist=[]
   for ele in data_json['rows']:
    for i in range(len(ele['elements'])):
     blist.append(ele['elements'][i]['duration_in_traffic']['value'])
    timeCost.append(blist)
    blist=[]
   distance=[]
   blist=[]
   for ele in data_json['rows']:
    for i in range(len(ele['elements'])):
     blist.append(ele['elements'][i]['distance']['value'])
    distance.append(blist)
    blist=[]
   return timeCost,locations,distance

#aco code
def costMatrix(alist):
    cost=alist
    #based on gfg graph
    #cost.append([0,10,15,20])
    #cost.append([10,0,35,25])
    #cost.append([15,35,0,30])
    #cost.append([20,25,30,0])
    #cost.append([25,15,10,35,0])
    #len(cost)
    #inverse cost matrix
    inverse_cost=[]
    #intialize to 0
    for i in range(len(cost)):
      inverse_cost.append(fillzeros(len(cost)))
    for i in range(len(cost)):
      for j in range(len(cost)):
        if cost[i][j]==0:
            inverse_cost[i][j]=0
        else:
            inverse_cost[i][j]=1/cost[i][j]
    #phermone level matrix
    phermone_level=[]
    #intialize to 0
    for i in range(len(cost)):
      phermone_level.append(fillzeros(len(cost)))
    return cost,inverse_cost,phermone_level


# In[12]:


def antInit(population,cost):
    antInfo=dict()
    # intialize dict as {key,[]}
    for i in range(population):
        antInfo[i]=[]
    #intialize all ants at random vertices
    for i in range(population):
        antInfo[i].append(randrange(len(cost)))
    return antInfo



# In[13]:


def findProb(init,cost,inverse_cost,phermone_level,positions,alpha,beta,deltaTau):
    prob_dict=dict()
    #initialize all prob as 0
    for i in range(len(cost)):
        prob_dict[i]=0
    temp=[]
    #denominator of prob func
    for i in range(len(cost)):
                pl=(1-0.5)*phermone_level[init][i]+1
                pl=pl**alpha
                b=inverse_cost[init][i]**beta
                a=pl*b
                temp.append(a)
    total=sum(temp)
    for i in range(len(cost)):
            temp=[]
            pl=(1-0.5)*phermone_level[init][i]+1
            pl=pl**alpha
            b=inverse_cost[init][i]**beta
            a=pl*b
            prob_dict[i]=a/total
    return prob_dict



# In[14]:


def moveAnts(cost,inverse_cost,phermone_level,positions,alpha,beta,deltaTau,rho):
    edges=dict()
    #initialize edges as {ant,distance traveled by ant}
    for i in  range(len(positions)):
        edges[i]=0
    #in each node
    while 1:
    #for each ant
      for i in range(len(positions)):
        prob_dict=findProb(positions[i][len(positions[i])-1],cost,inverse_cost,phermone_level,positions,alpha,beta,deltaTau)
        #nextNode will be eqaul to next vertice ant will travel(having max prob and also ant not travelled before)
        maxi=0
        nextNode=positions[i][0]
        for key in prob_dict:
            if key not in positions[i]:
                if prob_dict[key]>maxi:
                    maxi=prob_dict[key]
                    nextNode=key
        x=positions[i][len(positions[i])-1]
        positions[i].append(nextNode)
        edges[i]=edges[i]+cost[x][nextNode]
        phermone_level[x][nextNode]= (1-rho)*phermone_level[x][nextNode]+1
        phermone_level[nextNode][x]= (1-rho)*phermone_level[nextNode][x]+1
      flag=1
      for i in range(len(positions)):
        if len(positions[i])==len(cost):
            flag=0
        else:
            flag=1
      if flag==0:
        break
    return edges,positions

def solveTSP(alist,iterations =100, population = 100, alpha = 1.0, beta = 1.0, deltaTau = 1.0, rho = 0.5):
    cost,inverse_cost,phermone_level=costMatrix(alist)
    minCost=99999
    minPath=[]
    for i in range(iterations):
        positions=antInit(population,cost)
        edges,positions= moveAnts(cost,inverse_cost,phermone_level,positions,alpha,beta,deltaTau,rho)
        for key in edges:
            if edges[key]<minCost:
                minPath=positions[key]
                minCost=edges[key]
    #print(minCost)
    minPath.append(minPath[0])
    leni=len(minPath)
    minCost=minCost+cost[minPath[leni-2]][minPath[leni-1]]
    return minCost,minPath



def rotateArray(arr, n, d):
    temp = []
    i = 0
    while (i < d):
        temp.append(arr[i])
        i = i + 1
    i = 0
    while (d < n):
        arr[i] = arr[d]
        i = i + 1
        d = d + 1
    arr[:] = arr[: i] + temp
    arr.append(0)
    return arr

@app.route("/tour_planner")
def tour_planner():
    #Moving forward code
    #forward_message = "Moving Forward..."
    ans=[]
    ans,ttime=tour_planner_aco(ans) 
    return render_template('tour.html', results=ans,ttime=ttime);

def tour_planner_aco(ans):
 timeCost=[]
 distanceCost=[]
 timeCost,locations,distanceCost=buildCostMatrix(timeCost)
 a,b=solveTSP(timeCost)
 source=b.index(0)
 b=rotateArray(b[:-1],len(b)-1,source)
 print(a)
 print(b)
 #ans=[]
 ans.append(['Source','Destination','Travel time in min(based on current traffic)','Distance in km'])
 for i in  range(len(b)-1):
    alist=[]
    alist.append(locations[b[i]])
    alist.append(locations[b[i+1]])
    alist.append(round(timeCost[b[i]][b[i+1]]/60,2))
    alist.append(round(distanceCost[b[i]][b[i+1]]/1000,2))
    ans.append(alist)
 for ele in ans:
    print(ele)
 #tour_planner(ans)
 a=round(a/60,2)
 ip=request.remote_addr
 filename="tempfile"+ip+".txt"
 cmd="rm -rf "+filename
 os.popen(cmd)
 return ans,a
if __name__ == '__main__':
    app.run(debug=True,host="0.0.0.0",port=5000)



