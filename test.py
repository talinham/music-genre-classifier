from python_speech_features import mfcc
import winsound
import scipy.io.wavfile as wav
import numpy as np
from tempfile import TemporaryFile
import os
import pickle
import random 
import operator
import math
import numpy as np
from collections import defaultdict

from tkinter import *
from tkinter import filedialog



def select_files():
    dataset = []
    def loadDataset(filename):
        with open("my.dat" , 'rb') as f:
            while True:
                try:
                    dataset.append(pickle.load(f))
                except EOFError:
                    f.close()
                    break
    loadDataset("my.dat")

    def distance(instance1 , instance2 , k ):
        distance =0 
        mm1 = instance1[0] 
        cm1 = instance1[1]
        mm2 = instance2[0]
        cm2 = instance2[1]
        distance = np.trace(np.dot(np.linalg.inv(cm2), cm1)) 
        distance+=(np.dot(np.dot((mm2-mm1).transpose() , np.linalg.inv(cm2)) , mm2-mm1 )) 
        distance+= np.log(np.linalg.det(cm2)) - np.log(np.linalg.det(cm1))
        distance-= k
        return distance

    def getNeighbors(trainingSet , instance , k):
        distances =[]
        for x in range (len(trainingSet)):
            dist = distance(trainingSet[x], instance, k )+ distance(instance, trainingSet[x], k)
            distances.append((trainingSet[x][2], dist))
        distances.sort(key=operator.itemgetter(1))
        neighbors = []
        for x in range(k):
            neighbors.append(distances[x][0])
        return neighbors  
        
    def nearestClass(neighbors):
        classVote ={}
        for x in range(len(neighbors)):
            response = neighbors[x]
            if response in classVote:
                classVote[response]+=1 
            else:
                classVote[response]=1 
        sorter = sorted(classVote.items(), key = operator.itemgetter(1), reverse=True)
        return sorter[0][0]


    filetypes = (('wav files', '*.wav'),('All files', '*.*'))

    filenames = filedialog.askopenfilename(
        title='Open files',
        initialdir='/',
        filetypes=filetypes)
    
    my_text= Text(root, height = 1, width = 20)
    my_text.insert(INSERT, filenames)
    my_text.place(x=160 , y=100)


    results=defaultdict(int)
    i=1
    for folder in os.listdir("genres/"):
        results[i]=folder
        i+=1
    (rate,sig)=wav.read(filenames)
    mfcc_feat=mfcc(sig,rate,winlen=0.020,appendEnergy=False)
    covariance = np.cov(np.matrix.transpose(mfcc_feat))
    mean_matrix = mfcc_feat.mean(0)
    feature=(mean_matrix,covariance,0)
    pred=nearestClass(getNeighbors(dataset ,feature , 5))
    prediction = results[pred]
    print("\n\n The genre is: " + prediction + "\n")
    
    #print(prediction)

    textResult= Text(root, height = 1, width = 20)
    textResult.insert(INSERT, prediction)
    textResult.place(x=160 , y=150)
    

#################### GUI window #############################
root = Tk()
root.geometry("500x300")
#root.config(bg='blue')
root.wm_title('Music Genre Classifier')

#img = PhotoImage(file="background.png")
#label = Label(root,image=img)
#label.place(x=0, y=0)

my_text= Text(root, height = 1, width = 20)
my_text.place(x=160 , y=100)

textResult= Text(root, height = 1, width = 20)
textResult.place(x=160 , y=150)

myLabel1 = Label(root, text = "Music Genre Classifier")
myLabel1.config(font =("Helvetica", 15))
myLabel1.place(x=150, y=0)

myLabel2 = Label(root, text = "Select a song: ")
myLabel2.config(font =("Helvetica", 12))
myLabel2.place(x=50, y=100)

myLabelResult = Label(root, text = "The Genre is: ")
myLabelResult.config(font =("Helvetica", 12))
myLabelResult.place(x=50, y=150)


browseButton = Button( root, text=' Browse ',command=select_files)
browseButton.place(x=335, y =100)


root.mainloop()
 
