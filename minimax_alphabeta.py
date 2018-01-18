from copy import deepcopy
import time

def checkboard(mlist1):
	arr = mlist1[:]
	flag = 0
	i = 0
	while(i<size):
		j = 0
		while(j<size):
			if(arr[i][j]== '.'):
				flag = 1
			j = j + 1
		i = i + 1
	if(flag == 0):
		return 0
	else:
		return 1

def gamescore(arr,size,mlist,turn):
	x_value = 0
	o_value = 0
	score = 0
	i = 0
	while(i<size):
		j = 0
		while(j<size):
			if(arr[i][j] == 'X'):
				x_value = x_value + mlist[i][j]
			elif(arr[i][j] == 'O'):
				o_value = o_value + mlist[i][j]
			j = j + 1
		i = i + 1
	if(turn == 'O'):
		score = o_value - x_value
	elif(turn == 'X'):
		score = x_value - o_value
	return score

def raid_check(arr,i,j,turn,turn1):
	x = 0
	count_x = 0
	count_o = 0
	flag = 0
	arr1 = deepcopy(arr[:])
	
	while(x<size):
		y = 0
		while(y<size):
			if(arr1[x][y] == 'X'):
				count_x = count_x + 1
			elif(arr1[x][y] == 'O'):
				count_o = count_o + 1
			y = y + 1
		x = x + 1
		
	if((count_x>0)and(count_o>0)):
		if((j-1)>=0):                        #left
			if(arr1[i][j-1]==turn1):
				arr1[i][j-1]=turn
				flag = 1
		if((j+1)<size):                      #right
			if(arr1[i][j+1]==turn1):
				arr1[i][j+1]=turn
				flag = 1
		if((i+1)<size):                      #down
			if(arr1[i+1][j]==turn1):
				arr1[i+1][j]=turn
				flag = 1
		if((i-1)>=0):                        #up
			if(arr1[i-1][j]==turn1):
				arr1[i-1][j]=turn
				flag = 1
	if(flag == 0):
		arr1 = []		
	return arr1
	

def check_raid(arr,i,j,size,turn,turn1):
	raid1 = []
	positionr = []
	i = 0
	while(i<size):
		j = 0
		while(j<size):
			if(arr[i][j]==turn):
				arr1 = deepcopy(arr[:])
				arr2 = deepcopy(arr[:])
				arr3 = deepcopy(arr[:])
				arr4 = deepcopy(arr[:])
				if((j-1)>=0):                      #left
					if(arr1[i][j-1] == '.'):
						arr1[i][j-1]=turn
						a1 = []
						a1 = raid_check(arr1,i,j-1,turn,turn1)

						if(a1 != []):
							raid1.append(a1)
							p = []
							p.append(i)
							p.append(j-1)
							positionr.append(p)
				if((j+1)<size):                    #right
					if(arr2[i][j+1] == '.'):
						arr2[i][j+1]=turn
						a2 = []
						a2 = raid_check(arr2,i,j+1,turn,turn1)
						if(a2 != []):
							raid1.append(a2)
							p = []
							p.append(i)
							p.append(j+1)
							positionr.append(p)
				if((i+1)<size):                    #down
					if(arr3[i+1][j] == '.'):
						arr3[i+1][j]=turn
						a3 = []
						a3 = raid_check(arr3,i+1,j,turn,turn1)
						if(a3 != []):
							raid1.append(a3)
							p = []
							p.append(i+1)
							p.append(j)
							positionr.append(p)
				if((i-1)>=0):                    #up
					if(arr4[i-1][j] == '.'):
						arr4[i-1][j]=turn
						a4 = []
						a4 = raid_check(arr4,i-1,j,turn,turn1)
						if(a4 != []):
							raid1.append(a4)
							p = []
							p.append(i-1)
							p.append(j)
							positionr.append(p)
			j = j + 1
		i = i + 1
	return raid1,positionr	
	
def minimax_decision(mlist1,depth,turn,size,mlist,turn1):
	arr = mlist1[:]
	ar = deepcopy(arr[:])
	stake = [] 
	raid = []
	arr1 = []
	arr2 = []
	mainlist = []
	positions = []
	i = 0
	while(i<size):
		j = 0
		while(j<size):
			if(arr[i][j] == '.'):
				arr1 = deepcopy(arr[:])
				arr1[i][j] = turn
				p = []
				p.append(i)
				p.append(j)
				positions.append(p)
				stake.append(arr1)
			j = j + 1
		i = i + 1
	arr2,positionr = check_raid(ar,i,j,size,turn,turn1)
	raid = arr2
	a = 0
	b = 0
	while(a<len(stake)):
		mainlist.append(stake[a])
		a = a + 1
	if(raid != []):
		while(b<len(raid)):
			mainlist.append(raid[b])
			b = b + 1

	value = min_value(mainlist[0],depth-1,turn1,size,mlist,turn)
	max_val = value
	max_state = mainlist[0]
	a = 1
	while(a<len(mainlist)):
		val = min_value(mainlist[a],depth-1,turn1,size,mlist,turn)
		if(val>max_val):
			max_val = val
			max_state = mainlist[a]
		a = a + 1
	i = 0
	while(i<len(stake)):
		if(max_state == stake[i]):
			v = "Stake"
			pos = positions[i]
		i = i + 1
	j = 0
	if(raid != []):
		while(j<len(raid)):
			if(max_state == raid[j]):
				v = "Raid"
				pos = positionr[j]
			j = j + 1
	return max_val, max_state, v,pos
	
def min_value(state,depth,turn1,size,mlist,turn):
	arr = state[:]
	ar = deepcopy(arr[:])
	stake = []
	raid = []
	mainlist = []
	if(depth == 0):
		score = gamescore(arr,size,mlist,turn)
		return score
	else:
		i = 0
		while(i<size):
			j = 0
			while(j<size):
				if(arr[i][j] == '.'):
					arr1 = deepcopy(arr[:])
					arr1[i][j] = turn1
					stake.append(arr1)
					
				j = j + 1
			i = i + 1
		arr2,p = check_raid(ar,i,j,size,turn1,turn)
		raid = arr2
		a = 0
		b = 0
		while(a<len(stake)):
			mainlist.append(stake[a])
			a = a + 1
		if(raid != []):
			while(b<len(raid)):
				mainlist.append(raid[b])
				b = b + 1
		if(mainlist != []):
			value = max_value(mainlist[0],depth-1,turn,size,mlist,turn1)
			min_val = value
			a = 1
			while(a<len(mainlist)):
				val = max_value(mainlist[a],depth-1,turn,size,mlist,turn1)
				if(val<min_val):
					min_val = val
				a = a + 1
			return min_val
		else:
			score = gamescore(arr,size,mlist,turn)
			return score

def max_value(state,depth,turn,size,mlist,turn1):
	arr = state[:]
	ar = deepcopy(arr[:])
	stake = []
	raid = []
	mainlist = []
	if(depth == 0):
		score = gamescore(arr,size,mlist,turn)
		return score
	else:
		i = 0
		while(i<size):
			j = 0
			while(j<size):
				if(arr[i][j] == '.'):
					arr1 = deepcopy(arr[:])
					arr1[i][j] = turn
					stake.append(arr1)
				
				j = j + 1
			i = i + 1
		arr2,p = check_raid(ar,i,j,size,turn,turn1)
		raid = arr2
		a = 0
		b = 0
		while(a<len(stake)):
			mainlist.append(stake[a])
			a = a + 1
		if(raid != []):
			while(b<len(raid)):
				mainlist.append(raid[b])
				b = b + 1
		if(mainlist != []):
			value = min_value(mainlist[0],depth-1,turn1,size,mlist,turn)
			max_val = value
			a = 1
			while(a<len(mainlist)):
				val = min_value(mainlist[a],depth-1,turn1,size,mlist,turn)
				if(val>max_val):
					max_val = val
				a = a + 1
			return max_val
		else:
			score = gamescore(arr,size,mlist,turn)
			return score

#alpha beta functions

def max_value1(mlist1,alpha,beta,depth,turn,size,mlist,turn1):
	arr = mlist1[:]
	ar = deepcopy(arr[:])
	stake = []
	raid = []
	p = []
	mainlist = []
	positions = []
	v = None
	c = checkboard(mlist1)

	if((depth == 0)or(c!=1)):
		score = gamescore(arr,size,mlist,turn)
		return arr,score,p,v
	else:
		i = 0
		while(i<size):
			j = 0
			while(j<size):
				if(arr[i][j] == '.'):
					arr1 = deepcopy(arr[:])
					arr1[i][j] = turn
					p1 = []
					p1.append(i)
					p1.append(j)
					positions.append(p1)
					stake.append(arr1)
					
					
				j = j + 1
			i = i + 1
		arr2,positionr = check_raid(ar,i,j,size,turn,turn1)

		raid = arr2
		a = 0
		b = 0
		while(a<len(stake)):
			mainlist.append(stake[a])
			a = a + 1
		if(raid != []):
			while(b<len(raid)):
				mainlist.append(raid[b])
				b = b + 1

				
		
		if(mainlist != []):
			state1,value,pos,v1 = min_value1(mainlist[0],alpha,beta,depth-1,turn1,size,mlist,turn)
			max_val = value
			max_state = mainlist[0]

			i = 0
			while(i<len(stake)):

				if(max_state == stake[i]):
					v = "Stake"
					p = positions[i]

				i = i + 1
			j = 0
			if(raid != []):
				while(j<len(raid)):
					if(max_state == raid[j]):
						v = "Raid"
						p = positionr[j]
					j = j + 1

			if(max_val >= beta):
				return max_state,max_val,p,v
			alpha = max(alpha,max_val)
			a = 1
			while(a<len(mainlist)):
				state1,val,pos,v1 = min_value1(mainlist[a],alpha,beta,depth-1,turn1,size,mlist,turn)
				if(val>max_val):
					max_val = val
					max_state = mainlist[a]
					i = 0
					while(i<len(stake)):
						if(max_state == stake[i]):
							v = "Stake"
							p = positions[i]
						i = i + 1
					j = 0
					if(raid != []):
						while(j<len(raid)):
							if(max_state == raid[j]):
								v = "Raid"
								p = positionr[j]
							j = j + 1
					if(max_val >= beta):
						return max_state,max_val,p,v
					alpha = max(alpha,max_val)
				a = a + 1
		return max_state,max_val,p,v
	
def min_value1(mlist1,alpha,beta,depth,turn1,size,mlist,turn):
	arr = mlist1[:]
	ar = deepcopy(arr[:])
	stake = []
	raid = []
	mainlist = []
	positions = []
	p = []
	v = None
	i = 0
	c = checkboard(mlist1)
	if((depth == 0)or(c!=1)):
		score = gamescore(arr,size,mlist,turn)
		return arr,score,p,v
	else:
		i = 0
		while(i<size):
			j = 0
			while(j<size):
				if(arr[i][j] == '.'):
					arr1 = deepcopy(arr[:])
					arr1[i][j] = turn1
					p1 = []
					p1.append(i)
					p1.append(j)
					positions.append(p1)

					stake.append(arr1)
										
				j = j + 1
			i = i + 1
		arr2,positionr = check_raid(ar,i,j,size,turn1,turn)
		raid = arr2
		a = 0
		b = 0
		while(a<len(stake)):
			mainlist.append(stake[a])
			a = a + 1
		if(raid != []):
			while(b<len(raid)):
				mainlist.append(raid[b])
				b = b + 1
		
		min_state = []
		min_val = 0

		if(mainlist != []):
			state1,value,pos,v1 = max_value1(mainlist[0],alpha,beta,depth-1,turn,size,mlist,turn1)
			min_val = value
			min_state = mainlist[0]
			i = 0
			while(i<len(stake)):
				if(min_state == stake[i]):
					v = "Stake"
					p = positions[i]
				i = i + 1
			j = 0
			if(raid != []):
				while(j<len(raid)):
					if(min_state == raid[j]):
						v = "Raid"
						p = positionr[j]
					j = j + 1
			
			if(min_val <= alpha):
				return min_state,min_val,p,v
			beta = min(beta,min_val)
			a = 1
			while(a<len(mainlist)):
				state1,val,pos,v1 = max_value1(mainlist[a],alpha,beta,depth-1,turn,size,mlist,turn1)
				if(val<min_val):
					min_val = val
					min_state = mainlist[a]
					i = 0
					while(i<len(stake)):
						if(min_state == stake[i]):
							v = "Stake"
							p = positions[i]
						i = i + 1
					j = 0
					if(raid != []):
						while(j<len(raid)):
							if(min_state == raid[j]):
								v = "Raid"
								p = positionr[j]
							j = j + 1
					
				if(min_val <= alpha):
					return min_state,min_val,p,v
				beta = min(beta,min_val)
				a = a + 1
		return min_state,min_val,p,v

	
	
def alpha_beta_search(mlist1,depth,turn,size,mlist,turn1):
	beta = float("inf")
	alpha = float("-inf")
	v = 0
	state = []
	state,v,p,v1 = max_value1(mlist1,alpha,beta,depth,turn,size,mlist,turn1)
	return state,v,p,v1

			
#### getting inputs from file ####
start_time = time.time()
f = open('input.txt', 'r')
size = f.readline()
size = size.strip()
size = int(size)
algorithm = f.readline()
algorithm = algorithm.strip()
turn = f.readline()
turn = turn.strip()
depth = f.readline()
depth = depth.strip()
depth = int(depth)
i = 0
j =0

if(turn == 'X'):
		turn1 = 'O'
elif(turn == 'O'):
		turn1 = 'X'

#value array
slist = []
mlist = []
while(i < size):
	line = f.readline()
	slist = [int(x) for x in line.split(" ")]
	mlist.append(slist)
	i = i + 1

#symbol array
slist1 = []
mlist1 = []
while(j < size):
	line = f.readline()
	line = line.strip()
	for ch in line:
		slist1.append(ch)
	slist2 = slist1[:]
	mlist1.append(slist2)
	del slist1[:]
	j = j + 1

if(algorithm == "MINIMAX"):
	value,state,v,pos = minimax_decision(mlist1,depth,turn,size,mlist,turn1)
elif(algorithm == "ALPHABETA"):
	state,val,pos,v = alpha_beta_search(mlist1,depth,turn,size,mlist,turn1)


column = pos[1]
row = pos[0]
row_arr = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26]
col_arr = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
column_value = col_arr[column]
row_value = row_arr[row]

print("--- %s seconds ---" % (time.time() - start_time))
out_file = open('output.txt', 'w')
column_value = str(column_value)
row_value = str(row_value)
out_file.write(column_value+row_value+" "+v+"\n")
i = 0
while(i<size):
	j = 0
	while(j<size):
		out_file.write(state[i][j])
		j = j + 1
	out_file.write("\n")
	i = i + 1
