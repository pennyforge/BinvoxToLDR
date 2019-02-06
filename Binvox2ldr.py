#Neil Marsden 23/11/18
#www.brickalo.com
#Binvox to LDR with brick optimisation and layer rotation
#Use entirely at your own risk - Provided without any warrently of any kind whatsoever!

import os,datetime, time, sys
import numpy as np
import binvox_rw
import numpy 
import random
from copy import deepcopy

#Create a human readable timestamp`
def timeStamp ():
	ts = time.time()	
	dateTimeString = datetime.datetime.fromtimestamp(ts).strftime('%y%m%d%H%M')
	return (dateTimeString)

#Write individual lines to an LDR file
def legoWriter(fileName,dateTimeStamp,ldrLine):
	#null = 0
	#fileName = fileName + "_" + dateTimeStamp + ".ldr"
	#fileName = "output.ldr"
	#print fileName
	if os.path.isfile(fileName): # If the file exists then just append 'a' the line
		LDrawFile = open(fileName, 'a')
		LDrawFile.write('\n')
	else:
		LDrawFile = open(fileName, 'w') # Otherwise create a new file 'w' and put the header info in
		LDrawFile.write('0 // Name: '+ fileName +'\n')
		LDrawFile.write('0 // Author:  Neil Marsden ' + dateTimeStamp +'\n')
		# Add a red reference stud if you want one - set the first digit to 1 to enable
		LDrawFile.write('0 4 70 -8 70 0 0 1 0 1 0 -1 0 0 6141.dat'+'\n')
		LDrawFile.write('\n')
	print "WRITING LINE"
	LDrawFile.write(ldrLine)
	return fileName

def activeLine(active,colour,width,height,depth,m1,m2,m3,m4,m5,m6,m7,m8,m9,partID):
	#Example LDR Line
	#1 69 -20 -24 -20 0 0 1 0 1 0 -1 0 0 3005.dat
	active = str(active)
	colour = str(colour)	
	width = str(width)
	height = str(height)
	depth = str(depth)
	m1 = str(m1)
	m2 = str(m2)
	m3 = str(m3)
	m4 = str(m4)
	m5 = str(m5)
	m6 = str(m6)
	m7 = str(m7)
	m8 = str(m8)
	m9 = str(m9)
	ldrLine = active + " " + colour + " " + width + " " + height+ " " + depth  + " " + m1 + " " + m2 + " " + m3 + " " + m4 + " " + m5 + " " + m6 + " " + m7 + " " + m8 + " " + m9 + " " + partID
	return ldrLine

def brickMatrix(x,y):

	studMatrix = []
	Width = x
	Depth = y
	StudCount = 0 
	print "Brick is ",Width, "x" ,Depth
	for i in range (0,Width):
		for j in range(0,Depth):
			studMatrix.append(1)
	brickMatrix = numpy.array(studMatrix).reshape(Depth,Width);
	return brickMatrix		
	
def optimiseSlice(baseMatrix,previousMatrix,sliceValue):
	optimisedBrickData = []
	sliceCounter = 0
	layerBrickDiscard = 0
	#print brick
	print
	optimise = True
	brickCounter = 0
	dictionaryCounter = 2 # keep a track of the bricks swaps as you work through the matrix
	while optimise:
		#if sliceValue%2 == 0:
		#	baseMatrix = baseMatrix[::-1]
		for x in range(0,baseMatrix.shape[0]):
			for y in range(0,baseMatrix.shape[1]):
				voxel = baseMatrix[x,y]
				if voxel == 1:
					brickCounter = brickCounter + 1
					print "Found Voxel"
					#raw_input()
					for key, value in sorted(optimisationDictionary.iteritems(), key=lambda (k,v): (v,k), reverse = True):
						dictionaryCounter = dictionaryCounter + 1
						#check the shapes around the voxel 
						brickX,brickY = value
						brick = brickMatrix(brickX,brickY)
						maxValue = max(value)
						print brick.shape
						if sliceValue%2 == 0:
							brick = brick.reshape(brickX,brickY) # flips the array horizontal
								
						print "DistancesToEndOfFile X and Y:",baseMatrix.shape[0] - x, baseMatrix.shape[1] - y
						print "DistancesToEndOfFile X and Y:",maxValue > baseMatrix.shape[0] - x, maxValue > baseMatrix.shape[1] - y
						
						#print brick
						print "x:",x
						print "brickX:",brickX
						print "y:",y
						print "brickY:",brickY
						subMatrixH = baseMatrix[x:x+brickX,y:y+brickY]
						subMatrixV = baseMatrix[x:x+brickY,y:y+brickX]
						print "Horizontal Check SubMatrix"
						print subMatrixH
						print subMatrixH.shape
						print
						print "Vertical Check SubMatrix"
						print subMatrixV
						print subMatrixV.shape
						print
						print brick

						print brick.shape == subMatrixH.shape or brick.shape == subMatrixV.shape
						print
						print baseMatrix
						print
						print previousMatrix
						
						#raw_input()
						if (baseMatrix==previousMatrix).all() and sliceValue%2 == 0 and brickY > 6:
							layerBrickDiscard = 1
							#(a-b).any() alternatively (a-b).all()
							print "Matching Layers"

							print "Discarding ", brick, " brick to fix weak corneres..."
							#raw_input()
							#Discard this brick by ignoring it and continue the loop to the next brick....
							continue
						else:
							
							try:
								if numpy.amax(subMatrixH) == numpy.amin(subMatrixH) and brick.shape == subMatrixH.shape:
									print "MATCH HORIZONTAL!"
									rotate = 0
									print key, dictionaryCounter
									baseMatrix[x:x+brickX,y:y+brickY] = dictionaryCounter
									print baseMatrix
									dictionaryCounter = 2
									print x,y
									optimisedBrickData.append([key,x,y,brickX,brickY,rotate])
									if layerBrickDiscard == 1:
										previousMatrix =  deepcopy(baseMatrix)
									#if sliceValue == 2:
										#raw_input()
									break
								elif numpy.amax(subMatrixV) == numpy.amin(subMatrixV) and brick.shape == subMatrixV.shape:
									print "MATCH VERTICAL!"
									rotate = 1
									print key, dictionaryCounter
									baseMatrix[x:x+brickY,y:y+brickX] = dictionaryCounter
									print baseMatrix
									dictionaryCounter = 2
									print x,y
									optimisedBrickData.append([key,x,y,brickX,brickY,rotate])
									if layerBrickDiscard == 1:
										previousMatrix =  deepcopy(baseMatrix)
									#if sliceValue == 2:
										#raw_input()
									break
								else:
									print "Brick won't fit - trying next brick..."
									print "======================================"
									#dictionaryCounter = 2
							except:
								print "Brick won't fit on matrix anyway- trying next brick..."
								print "======================================"

								#dictionaryCounter = 2
								#raw_input()

								
				else:
					print "No Voxel"
					dictionaryCounter = 2
		#if brickCounter == nosOfBricks:
			layerBrickDiscard = 0
		optimise = False
		previousMatrix =  deepcopy(baseMatrix)
	return (baseMatrix,previousMatrix,optimisedBrickData)	


def queryHollowing(baseMatrix):
	#WORK IN PROGRESS - WILL PROBABLY NOT WORK AS EXPECTED!
	#print baseMatrix.shape[1]
	dimX = baseMatrix.shape[0]
	dimY = baseMatrix.shape[1]
	#CALCULATE PERCENTAGE - Must be above 80% of layer
	nosOfBricks = numpy.count_nonzero(baseMatrix == 1)
	totalMatrix = dimX*dimY
	#print nosOfBricks,totalMatrix
	percentage = float(nosOfBricks)/float(totalMatrix)*100
	#print percentage
	if dimX > 10 and dimY > 10 and percentage > 80: # AND PERCENTAGE
		baseMatrix = hollowing(baseMatrix)
	else:
		print percentage
		print ("Matrix won't hollow, skipping...")
	return baseMatrix
	
def hollowing(baseMatrix):
	#WORK IN PROGRESS - WILL PROBABLY NOT WORK AS EXPECTED!
	startX = 2
	startY = 2
	endX = baseMatrix.shape[0]-2
	endY = baseMatrix.shape[1]-2
	#print x[0:2,  2:4] # where start:how many
	#        ^^^   ^^^
	#        rows  cols
	originalMatrix = deepcopy(baseMatrix)
	baseMatrix[startX:endX,startY:endY] = 0
	return baseMatrix	
	
#==================================================================================================================
try:
	initialFileName = sys.argv[1]
except: 
	initialFileName = "moo.binvox"
	path = os.getcwd()
	fullPath = "\"" + path + "\\" + initialFileName + "\"" 
	print "No file name given on command line"
	inputString = "Do you want to use " + fullPath + " ? - Press Y then enter to continue - any other key to exit: "
	
	print
	humanInput = raw_input(inputString)
	
	if humanInput == "y" or humanInput == "Y":
		print "OK - trying to use moo.binvox"
		path = os.getcwd()
		fullPath = "\"" + path + "\\" + initialFileName + "\"" 
		print fullPath
	else:
		print
		print "Exiting..."
		print
		sys.exit(0)

if os.path.isfile(initialFileName):	
	print "Found file"
else:
	print
	print "Unable to find file",initialFileName," - Exiting..."
	print
	sys.exit(0)

#Read the binvox file and create a 3 dimensional boolean array of the data in "model"...	
with open(initialFileName, 'rb') as f:
#with open('chair.binvox', 'rb') as f:
	model = binvox_rw.read_as_3d_array(f)

dateTimeStamp = timeStamp() #Get timeStamp for fileName
		
#Set Up the Brick Dictionary
optimisationDictionary = {}
optimisationDictionary["3006.DAT"]=[2,10]	#3
optimisationDictionary["3007.DAT"]=[2,8]	#4
optimisationDictionary["2456.DAT"]=[2,6]	#5
optimisationDictionary["3001.DAT"]=[2,4]	#6
optimisationDictionary["3002.DAT"]=[2,3]	#7
optimisationDictionary["3003.DAT"]=[2,2]	#8
optimisationDictionary["3008.DAT"]=[1,8]	#9
optimisationDictionary["3009.DAT"]=[1,6]	#10
optimisationDictionary["3010.DAT"]=[1,4]	#11
optimisationDictionary["3622.DAT"]=[1,3]	#12
optimisationDictionary["3004.DAT"]=[1,2]	#13
optimisationDictionary["3005.DAT"]=[1,1]	#14
	
	
#print model.data[0,0,0] # Testing only
#LDR Line example
#1 69 -20 -24 -20 0 0 1 0 1 0 -1 0 0 3005.dat
#Setup the basic LDR line...
active = 1
colour = 7
width = 0
height = 0
depth = 0
#Set up the basic rotation matrix for the ldr file
m1 = 0
m2 = 0
m3 = 1
m4 = 0
m5 = 1
m6 = 0
m7 = -1
m8 = 0
m9 = 0
#Set the part for each voxel - currently this only works for 1x1 bricks - now unused
partID = "3005.dat" #Use 1x1 bricks


dateTimeStamp = timeStamp() #Get timeStamp for fileName
fileName = initialFileName[:-7] +"_" + dateTimeStamp + ".ldr" #Give every ldr fileName a timestamp
ldrLine = activeLine(active,colour,width,height,depth,m1,m2,m3,m4,m5,m6,m7,m8,m9,partID) #Create a raw ldr line width,height and depth will be updated as the loop below scans the binvox array

count = 0 # Used to count the total number of 1x1 bricks
studMatrix = [] #Used to view slices (for humans!)
optimise = True
#The following loops do the heavy lifting reading the binvox array and writing out the bricks to an ldr file...
while optimise:
	for z in range(model.dims[2]): #Reads the size of the array from the binvox model dimensions - in z - the height
		for x in range(model.dims[0]): #Reads the size of the array from the binvox model dimensions - in x
			for y in range(model.dims[1]): #Reads the size of the array from the binvox model dimensions - in y
				if z <= range(model.dims[2]): # This will allow you to slice individual layers of the binvox file if you want - Currently it will slice the whole chair_binvox array
					#if z <= 0: # This will allow you to slice individual layers of the binvox file if you want - Currently it will slice the whole chair_binvox array
					if model.data[x,y,z]: #Looking for "True" value (as the binvox array is boolean)
						#Create the voxel slice in studMatrix
						studMatrix.append(1) #Used to view slices (for humans!)
						count = count + 1
					else:
						print "Skipping - no brick..."
						studMatrix.append(0) #Used to view slices (for humans!)	


				try:
					#Make an array of studMatrix when the layer is finished
					sliceMatrix = np.array(studMatrix).reshape(model.dims[0],model.dims[1])
					print sliceMatrix
					print "Number of bricks in ldr file:",count," Layer: ",z
					#raw_input()

					#optimise = False
					#break
				except:
					print ("Waiting for larger matrix")
				print "Number of bricks in layer:",count,z
		#raw_input()
		legoWriter(fileName,dateTimeStamp,'0 STEP') # Add a step for each layer
		#Set up the variables to optimise the layer
		sliceValue = z 
		originalMatrix = deepcopy(sliceMatrix)
		previousMatrix = deepcopy(sliceMatrix)
		#==================================
		#Hollowing function - WORK IN PROGRESS
		'''#For Hollowing but needs adjustment to reduce the degree of hollowing before the final layer above the hollowing (otherwise bricks will simply fall in the hollow!
		if layer > minLayer and layer < maxLayer:
			baseMatrix = queryHollowing(baseMatrix)
			hollowMatrix = deepcopy(baseMatrix)
		if layer == maxLayer-1:
			baseMatrix = originalMatrix
			colour = 47
			raw_input()
		'''	
		#Optimise the layer...
		sliceMatrix,previousMatrix, optimisedBrickData = optimiseSlice(sliceMatrix,previousMatrix,sliceValue)

		print "OPTIMISATION COMPLETE..."
		print
		print "Original Voxel Matrix Slice"
		print originalMatrix
		print
		print "Optimised Lego Matrix Slice"
		print sliceMatrix		
		print	
		#print optimisedBrickData
		sliceMatrix = deepcopy(originalMatrix)

		#Read the bricks in the optimisedBrickData array
		countBrick = 0
		for brick in optimisedBrickData:
			countBrick = countBrick + 1
			print brick
			print
			print brick[0],brick[1],brick[2],brick[3],brick[4],brick[5]
			#Assign the variables for each element in optimisedBrickData  
			partID = brick[0]
			x = brick[1]
			y = brick[2]
			brickX = brick[3]
			brickY = brick[4]
			brickRotate = brick[5]
			
			#Convert to Lego Values
			width = x*20+10 #Convert x and y into lego dimensions
			depth = y*20+10+((brickY/2)*20) #Convert x and y into lego dimensions
			height = z*-24 #Convert z into lego dimensions

			#Make corrections to rotated bricks
			correctionX = 0
			correctionY = 0
			
			if brickX%2 != 0:
				print"EVEN"
				correctionX = 10
				if count%2 != 0:
					correctionX = 10
			if brickY%2 != 0:
				print "ODD"
				correctionY = 10
				if count%2 != 0:
					print "EVEN 3x2"
					correctionY = 10
			if brickX == 1 and brickY != 1 and brickRotate == 1:
				if brickY%2 == 0:
					print "EVEN"
				else:
					print "ODD"
					correctionY = correctionY-10	
					correctionX = correctionX-10
				print "found complex error"
				correctionY = correctionY-20
				print correctionY
				#raw_input()
			if brickY==4 and brickX == 2 and brickRotate ==1:
				print "Found 4x2 - Correcting..."
				correctionY = correctionY - 30
				correctionX = correctionX + 10
				
				
			if brickY==3 and brickX == 2 and brickRotate ==1:
				print "Found 3x2 - Correcting..."
				correctionY = correctionY - 40
				
				
			if brickY==10 and brickX == 2 and brickRotate ==1:
				print "Found 10x2 - Correcting..."
				correctionY = correctionY - 30
				correctionX = correctionX + 10
				
			if brickY==6 and brickX == 2 and brickRotate ==1:
				print "Found 6x2 - Correcting..."
				correctionY = correctionY - 30
				correctionX = correctionX + 10

			if brickY==8 and brickX == 2 and brickRotate ==1:
				print "Found 8x2 - Correcting..."
				correctionY = correctionY - 30
				correctionX = correctionX + 10
				
			if brickRotate == 0:
				width = width - correctionX
				depth = depth + correctionY
				ldrLine = activeLine(active,colour,width,height,depth,m1,m2,m3,m4,m5,m6,m7,m8,m9,partID) #Construct the ldr line
			else:
				width = x*20+((brickY/2)*20)-correctionX #Convert x and y into lego dimensions
				depth = y*20-correctionY #Convert x and y into lego dimensions
				#90 brickRotate 1 4 20 -104 20 -1 0 0 0 1 0 0 0 -1 3001.dat	
				m1 = -1 
				m2 = 0 
				m3 = 0 
				m4 = 0
				m5 = 1 
				m6 = 0 
				m7 = 0 
				m8 = 0 
				m9 = -1
				#Create the ldrLine
				ldrLine = activeLine(active,colour,width,height,depth,m1,m2,m3,m4,m5,m6,m7,m8,m9,partID) #Construct the ldr line
				print ldrLine
				
			#Write the LDR name to file...	
			legoWriter(fileName,dateTimeStamp,ldrLine) #Write the line to a ldr file
			
			print "countBrick:",countBrick
			
			
		z = z + 1
		count = count + 1
		optimisedBrickData = []
		brickRotate = 0
		previousMatrix =  deepcopy(sliceMatrix)
		sliceMatrix = deepcopy(originalMatrix)
		
		#Reset the rotation values - this is important otherwise the rotation "sticks" on the next layer!
		m1 = 0
		m2 = 0
		m3 = 1
		m4 = 0
		m5 = 1
		m6 = 0
		m7 = -1
		m8 = 0
		m9 = 0

		print "Layer: ",z			
			
		#==================================
		count = 0
		studMatrix = []
		if z == model.dims[2]:
			optimise = False # Quit when the top layer is reached
		
print "MODEL CONVERSION COMPLETE - Your .ldr file is:", fileName














