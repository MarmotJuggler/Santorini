#!/usr/bin/env python
# coding: utf-8

# In[7]:


#Santorini source code
import copy
import pickle
width = 3
height = 3
def FindLocation(position, activePlayer):
    global height
    global width
    for x in range(height):
            for y in range(width):
                    if position[x][y][1]==activePlayer:
                        return [x,y]
def FindActivePlayer(position):
    global height
    global width
    sum = 0
    for x in range (height):
        for y in range(width):
            sum+=position[x][y][0]
    if sum%2==0:
        return 1
    return 2

startState=[]
for x in range(height):
    startState.append([])
    for y in range(width):
        startState[x].append([0,0])
startState[0][0][1]=1
startState[height-1][width-1][1]=2
print(startState)
def DoMove(position, move):
    global width
    global height
    activePlayer=FindActivePlayer(position)
    newPosition=copy.deepcopy(position)
    activePlayerLocation = FindLocation(newPosition, activePlayer)
    newPosition[move[0]][move[1]][1]=activePlayer
    newPosition[activePlayerLocation[0]][activePlayerLocation[1]][1]=0
    newPosition[move[2]][move[3]][0]+=1
    return newPosition
def GenerateMoves(position):
    global height
    global width
    availableMoves=[]
    activePlayer=FindActivePlayer(position)
    location=FindLocation(position, activePlayer)
    #sides
    if (location[0]+1 <height and position[location[0]+1][location[1]][1]==0 and position[location[0]+1][location[1]][0]<4
    and (position[location[0]+1][location[1]][0] - position[location[0]][location[1]][0]) <= 1): #bottom middle
        availableMoves.append([+1,0])
    if (location[0]-1 >-1 and position[location[0]-1][location[1]][1]==0 and position[location[0]-1][location[1]][0]<4
    and (position[location[0]-1][location[1]][0] - position[location[0]][location[1]][0]) <= 1): #top middle
        availableMoves.append([-1,0])
    if (location[1]+1 <width and position[location[0]][location[1]+1][1]==0 and position[location[0]][location[1]+1][0]<4
    and (position[location[0]][location[1]+1][0] - position[location[0]][location[1]][0]) <= 1): #right middle
        availableMoves.append([0,+1])
    if (location[1]-1 >-1 and position[location[0]][location[1]-1][1]==0 and position[location[0]][location[1]-1][0]<4
    and (position[location[0]][location[1]-1][0] - position[location[0]][location[1]][0]) <= 1): #left middle
        availableMoves.append([0,-1])
    #corners
    if (location[0]+1 <height and location[1]+1 <width and position[location[0]+1][location[1]+1][1]==0 and position[location[0]+1][location[1]+1][0]<4
    and (position[location[0]+1][location[1]+1][0] - position[location[0]][location[1]][0]) <= 1): #bottom right
        availableMoves.append([+1,+1])
    if (location[0]-1 >-1 and location[1]+1 <width and position[location[0]-1][location[1]+1][1]==0 and position[location[0]-1][location[1]+1][0]<4
    and (position[location[0]-1][location[1]+1][0] - position[location[0]][location[1]][0]) <= 1): #top right
        availableMoves.append([-1,+1])
    if (location[0]+1 <height and location[1]-1 >-1 and position[location[0]+1][location[1]-1][1]==0 and position[location[0]+1][location[1]-1][0]<4
    and (position[location[0]+1][location[1]-1][0] - position[location[0]][location[1]][0]) <= 1): #bottom left
        availableMoves.append([+1,-1])
    if (location[0]-1 >-1 and location[1]-1 >-1 and position[location[0]-1][location[1]-1][1]==0 and position[location[0]-1][location[1]-1][0]<4
    and (position[location[0]-1][location[1]-1][0] - position[location[0]][location[1]][0]) <= 1): #top left
        availableMoves.append([-1,-1])
    return availableMoves

def GenerateBuilds(position, availableMoves):
    global height
    global width
    availableBuilds = []
    activePlayer=FindActivePlayer(position)
    location=FindLocation(position, activePlayer)
    for move in availableMoves:
        movedPosition = copy.deepcopy(position)
        movedPosition[location[0]+move[0]][location[1]+move[1]][1]=activePlayer
        movedPosition[location[0]][location[1]][1]=0
        newLocation = [location[0]+move[0],location[1]+move[1]]
            #sides
        if (newLocation[0]+1 <height and movedPosition[newLocation[0]+1][newLocation[1]][1]==0 and movedPosition[newLocation[0]+1][newLocation[1]][0]<4): #bottom middle
            availableBuilds.append([newLocation[0],newLocation[1],newLocation[0]+1,newLocation[1]])
        if (newLocation[0]-1 >-1 and movedPosition[newLocation[0]-1][newLocation[1]][1]==0 and movedPosition[newLocation[0]-1][newLocation[1]][0]<4): #top middle
            availableBuilds.append([newLocation[0],newLocation[1],newLocation[0]-1,newLocation[1]])
        if (newLocation[1]+1 <width and movedPosition[newLocation[0]][newLocation[1]+1][1]==0 and movedPosition[newLocation[0]][newLocation[1]+1][0]<4): #right middle
            availableBuilds.append([newLocation[0],newLocation[1],newLocation[0],newLocation[1]+1])
        if (newLocation[1]-1 >-1 and movedPosition[newLocation[0]][newLocation[1]-1][1]==0 and movedPosition[newLocation[0]][newLocation[1]-1][0]<4): #left middle
            availableBuilds.append([newLocation[0],newLocation[1],newLocation[0],newLocation[1]-1])
        #corners
        if (newLocation[0]+1 <height and newLocation[1]+1 <width and movedPosition[newLocation[0]+1][newLocation[1]+1][1]==0 and movedPosition[newLocation[0]+1][newLocation[1]+1][0]<4): #bottom right
            availableBuilds.append([newLocation[0],newLocation[1],newLocation[0]+1,newLocation[1]+1])
        if (newLocation[0]-1 >-1 and newLocation[1]+1 <width and movedPosition[newLocation[0]-1][newLocation[1]+1][1]==0 and movedPosition[newLocation[0]-1][newLocation[1]+1][0]<4): #top right
            availableBuilds.append([newLocation[0],newLocation[1],newLocation[0]-1,newLocation[1]+1])
        if (newLocation[0]+1 <height and newLocation[1]-1 >-1 and movedPosition[newLocation[0]+1][newLocation[1]-1][1]==0 and movedPosition[newLocation[0]+1][newLocation[1]-1][0]<4): #bottom left
            availableBuilds.append([newLocation[0],newLocation[1],newLocation[0]+1,newLocation[1]-1])
        if (newLocation[0]-1 >-1 and newLocation[1]-1 >-1 and movedPosition[newLocation[0]-1][newLocation[1]-1][1]==0 and movedPosition[newLocation[0]-1][newLocation[1]-1][0]<4): #top left
            availableBuilds.append([newLocation[0],newLocation[1],newLocation[0]-1,newLocation[1]-1])      
    return availableBuilds

def PrimitiveValue(position):
    if WonCheck(position) or len(GenerateMoves(position))==0:
        return "lose"
    return "not_primitive"
def WonCheck(position):
    global height
    global width
    for x in range(height):
        for y in range(width):
            if position[x][y][0] == 3 and (position[x][y][1] > 0):
                return True
    return False


# In[3]:


#Solver
def Solve(position):
    canonicalPosition=position
    oddOrEven=0
    global whoseTurn
    for x in range (3):
        for y in range (3):
            oddOrEven += position[x][y][0]
    if oddOrEven%2==0:
        whoseTurn="Player1"
    else:
        whoseTurn="Player2"
    if json.dumps(canonicalPosition) in lookupState:
        return lookupState[json.dumps(canonicalPosition)]
    gameState = PrimitiveValue(canonicalPosition)
    playerBestResult = "lose"
    if gameState != "not_primitive":
        lookupState[json.dumps(canonicalPosition)]=gameState
        lookupRemote[json.dumps(canonicalPosition)]=0
        return gameState
    for move in GenerateBuilds(canonicalPosition):
        new_position = DoMove(canonicalPosition,move)
        #Find the canonical position
        if WORM:
            new_position = FindCanonical(DoMove(canonicalPosition,move))
        opponentBestResult = Solve(new_position)
        if opponentBestResult == "lose" and (playerBestResult!="win" or lookupRemote[json.dumps(canonicalPosition)]>(1+lookupRemote[json.dumps(new_position)])):
            playerBestResult="win"
            lookupRemote[json.dumps(canonicalPosition)]=1+lookupRemote[json.dumps(new_position)]
        if opponentBestResult == "tie" and playerBestResult!="win" and (playerBestResult!="tie" or lookupRemote[json.dumps(canonicalPosition)]>(1+lookupRemote[json.dumps(new_position)])):
            playerBestResult = "tie"
            lookupRemote[json.dumps(position)]=1+lookupRemote[json.dumps(new_position)]
        if playerBestResult == "lose" and (json.dumps(canonicalPosition) not in lookupRemote.keys() or lookupRemote[json.dumps(canonicalPosition)]<(1+lookupRemote[json.dumps(new_position)])):
            lookupRemote[json.dumps(canonicalPosition)]=1+lookupRemote[json.dumps(new_position)]
    lookupState[json.dumps(canonicalPosition)]=playerBestResult
    return playerBestResult


# In[6]:


with open('State.pickle','rb') as f:
    lookupState = pickle.load(f)
    
with open('Remoteness.pickle','rb') as f:
    lookupRemote = pickle.load(f)


# In[15]:


#Analysis code
WORM = True
maxRemoteness=37
lookupStateRemote={}
for i in range(maxRemoteness):
    lookupStateRemote[i]=[0,0,0]
print(PeepoSolve(startState))
for (position, remote) in lookupRemote.items():
    if lookupState[str(position)] == "win":
        lookupStateRemote[remote][0]+=1
    elif lookupState[str(position)] == "lose":
        lookupStateRemote[remote][1]+=1
    elif lookupState[str(position)] == "tie":
        lookupStateRemote[remote][2]+=1
#For formatting the results
print("{:<8}{:<8}{:<8}{:<8}{:<8}".format("Remote", "Win", "Lose", "Tie", "Total"))
for i in range(1,1+maxRemoteness):
    print("{:<8}{:<8}{:<8}{:<8}{:<8}".format(maxRemoteness-i, lookupStateRemote[maxRemoteness-i][0],lookupStateRemote[maxRemoteness-i][1],lookupStateRemote[maxRemoteness-i][2],lookupStateRemote[maxRemoteness-i][0]+lookupStateRemote[maxRemoteness-i][1]+lookupStateRemote[maxRemoteness-i][2]))
print("{:<8}{:<8}{:<8}{:<8}{:<8}".format("Total", sum([lookupStateRemote[i][0] for i in range(maxRemoteness)]), sum([lookupStateRemote[i][1] for i in range(maxRemoteness)]), sum([lookupStateRemote[i][2] for i in range(maxRemoteness)]), sum([lookupStateRemote[i][0] for i in range(maxRemoteness)])+sum([lookupStateRemote[i][1] for i in range(maxRemoteness)])+sum([lookupStateRemote[i][2] for i in range(maxRemoteness)])))


# In[14]:


#Solver
def PeepoSolve(position):
    oddOrEven=0
    global height
    global width
    if str(position) in lookupState:
        return lookupState[str(position)]
    gameState = PrimitiveValue(position)
    playerBestResult = "lose"
    if gameState != "not_primitive":
        lookupState[str(position)]=gameState
        if len(lookupState)%(500000)==0:
            with open('State2.pickle','wb') as f:
                pickle.dump(lookupState, f)
            with open('Remoteness2.pickle','wb') as f:
                pickle.dump(lookupRemote, f)
            print(len(lookupState),"positions solved")
        lookupRemote[str(position)]=0
        return gameState
    availableBuilds=GenerateBuilds(position, GenerateMoves(position))
    for move in availableBuilds:
        new_position = DoMove(position,move)
        opponentBestResult = PeepoSolve(new_position)
        if opponentBestResult == "lose" and (playerBestResult!="win" or lookupRemote[str(position)]>(1+lookupRemote[str(new_position)])):
            playerBestResult="win"
            lookupRemote[str(position)]=1+lookupRemote[str(new_position)]
        if opponentBestResult == "tie" and playerBestResult!="win" and (playerBestResult!="tie" or lookupRemote[str(position)]>(1+lookupRemote[str(new_position)])):
            playerBestResult = "tie"
            lookupRemote[str(position)]=1+lookupRemote[str(new_position)]
        if playerBestResult == "lose" and (str(position) not in lookupRemote.keys() or lookupRemote[str(position)]<(1+lookupRemote[str(new_position)])):
            lookupRemote[str(position)]=1+lookupRemote[str(new_position)]
    lookupState[str(position)]=playerBestResult
    if len(lookupState)%(500000)==0:
            print(len(lookupState),"positions solved")
            with open('State2.pickle','wb') as f:
                pickle.dump(lookupState, f)
            with open('Remoteness2.pickle','wb') as f:
                pickle.dump(lookupRemote, f)
    return playerBestResult


# In[11]:


print(len(lookupState))


# In[2]:


import pickle


# In[ ]:


lose
Remote  Win     Lose    Tie     Total   
36      0       0       0       0       
35      0       0       0       0       
34      0       0       0       0       
33      0       0       0       0       
32      0       0       0       0       
31      0       0       0       0       
30      0       53      0       53      
29      75      0       0       75      
28      0       3892    0       3892    
27      4643    0       0       4643    
26      0       30958   0       30958   
25      43628   0       0       43628   
24      0       106049  0       106049  
23      142363  0       0       142363  
22      0       194692  0       194692  
21      307158  0       0       307158  
20      0       295670  0       295670  
19      482220  0       0       482220  
18      0       384394  0       384394  
17      636198  0       0       636198  
16      0       428616  0       428616  
15      828722  0       0       828722  
14      0       463444  0       463444  
13      907782  0       0       907782  
12      0       595690  0       595690  
11      1054055 0       0       1054055 
10      0       696150  0       696150  
9       1368580 0       0       1368580 
8       0       897522  0       897522  
7       1686332 0       0       1686332 
6       0       1119062 0       1119062 
5       2876058 0       0       2876058 
4       0       2713758 0       2713758 
3       5978486 0       0       5978486 
2       0       3806350 0       3806350 
1       160714690       0       16071469
0       0       171094700       17109470
Total   32387769288457700       61233539

