#!/usr/bin/env python2
from __future__ import division
from psychopy import visual, core, event, gui
from psychopy.hardware import joystick
from math import fabs, sin, exp,log
from scipy.signal import argrelextrema
import numpy as np
import pygame
import time
import random
import csv
from os import makedirs as mkdir
from os.path import isdir
import pickle

class Exp:
    def __init__(self):
        #
        # Experiment necessities
        #
        joystick.backend = 'pygame'
        
        
        #
        # Set up Subject info
        #
        self.subjectID = '999' #temporary subject number.
        self.run = '1'
        self.expName = 'Grip Force'
        self.expInfoDic = {"condition":'','SameDiff':'','participant':'','run':''}
        self.dlg = gui.DlgFromDict(dictionary=self.expInfoDic, title=self.expName)
        if self.dlg.OK == False: core.quit()  # user pressed cancel
        self.subjectID = self.expInfoDic['participant']
        self.run = self.expInfoDic['run']
        self.cond = self.expInfoDic['condition']
        self.congruent = self.expInfoDic['SameDiff']
        print self.subjectID
        print self.run
        self.myWin = visual.Window((800.0,800.0),allowGUI=True,winType='pygame',fullscr=True,units='cm',monitor='testMonitor') # This is the experiment window to draw in
        self.nJoysticks = joystick.getNumJoysticks()
        self.joy = joystick.Joystick(0)
        #
        # Experiment variables
        #
        # Adding in the jitter here for run 1
        self.setWeight = 25
        self.cur_weight = self.setWeight
        self.curConstant = 25
        self.winHeight = 20
        self.eRate = 0.01
        self.earningTIme = 20
#        if self.run in ['006','007','008']:  ### Necessary for scanner at the NIH.  Need to adjust for the Oxford scanners.
#            self.curConstant = 21
#        else:
#            self.curConstant = 25
        
        

        
        self.winDur = 0.15 # time window for grip smoothing
        self.duration = 30
        self.origin = -8
        self.CV = 1
        self.blockWaitDur = 5
        self.blockFixDur = 15 #plus 5 for the phrase
        self.numBlocks = 3 #number of blocks in each run
        self.numTrials = 8              #number of trials (within each block) ####
        self.trialLen = 14 
        self.trialWait = 3
        self.path = './data.Gates/HV_'+str(self.subjectID)+'.'+self.cond+'/'
        self.myMouse = event.Mouse(visible=0)
        self.testRuns = ['006','007','008']
        self.targetWidth = 1.0
        self.targSize = (self.targetWidth,self.targetWidth)
        #
        
        self.targSpot1 = visual.Circle(self.myWin,
        pos=(0,0), size=self.targSize,opacity=1.0,fillColor='SkyBlue',lineColor='SkyBlue',lineWidth=0,autoLog=False)
        
        self.targSpot2 = visual.Circle(self.myWin,
        pos=(0,0), size=self.targSize,opacity=1.0,fillColor='Tomato',lineColor='Tomato',lineWidth=0,autoLog=False)
        
        self.targSpot3 = visual.Circle(self.myWin,
        pos=(0,0), size=self.targSize,opacity=1.0,fillColor='SpringGreen',lineColor='SpringGreen',lineWidth=0,autoLog=False)
        
        self.targSpot4 = visual.Circle(self.myWin,
        pos=(0,0), size=self.targSize,opacity=1.0,fillColor='Yellow',lineColor='Yellow',lineWidth=0,autoLog=False)
        
        self.targSpot5 = visual.Circle(self.myWin,
        pos=(0,0), size=self.targSize,opacity=1.0,fillColor='HotPink',lineColor='HotPink',lineWidth=0,autoLog=False)
        
        #
        self.originSpot = visual.PatchStim(self.myWin,tex="none", mask="circle",
        pos=(0,self.origin), size=(2,2),color='black', autoLog=False)
        #
        self.fixationCross = visual.TextStim(win=self.myWin, text='+', wrapWidth=10.0, font='Arial',
        pos=[0, 0], height=2.0, color='white',opacity=1, depth=0.0)
        self.fixationCrossB = visual.TextStim(win=self.myWin, text='+', wrapWidth=10.0, font='Arial',
        pos=[0, 0], height=2.0, color='black', opacity=1, depth=0.0)
        #
        self.block = 0
        self.loadEarning(self.block)
            
        self.instPhraseL1= str('Hit the gates in the right order.')
        self.instPhraseL2= str('')
        self.instPhraseL3= str('Press space')
        self.breakPhraseL1 = str("Nice job, take a breather.")
        self.breakPhraseL3 = str("You will now see a cross.  It will turn black when you are about to start")        
            
        self.InstructionL1 = visual.TextStim(win=self.myWin, text=self.instPhraseL1, wrapWidth=10.0, font='Arial',
        pos=[0, 2], height=1.0, color=[1.000,1.000,1.000], colorSpace='rgb', opacity=1, depth=0.0)
        
        self.InstructionL2 = visual.TextStim(win=self.myWin, text=self.instPhraseL2, wrapWidth=10.0, font='Arial',
        pos=[0, 0], height=1.0, color=[1.000,1.000,1.000], colorSpace='rgb', opacity=1, depth=0.0)
        
        self.InstructionL3 = visual.TextStim(win=self.myWin, text=self.instPhraseL3, wrapWidth=10.0, font='Arial',
        pos=[0, -2], height=1.0, color=[1.000,1.000,1.000], colorSpace='rgb', opacity=1, depth=0.0)
            
        self.breakL1 = visual.TextStim(win=self.myWin, text=self.breakPhraseL1, wrapWidth=10.0, font='Arial',
        pos=[0, 3], height=2.0, color=[1.000,1.000,1.000], colorSpace='rgb', opacity=1, depth=0.0)
        
        self.breakL3 = visual.TextStim(win=self.myWin, text=self.breakPhraseL3, wrapWidth=10.0, font='Arial',
        pos=[0, -3], height=2.0, color=[1.000,1.000,1.000], colorSpace='rgb', opacity=1, depth=0.0)
        
        
        print self.run
        self.rnum = int(self.run)
            
        self.subjGateLocation = [0.15,0.35,0.65,0.7,0.9]
        self.TargetOrder = [3,0,4,1,2]
        
        if self.run == '001':
            while isdir(self.path) == True:
               print(self.path + ' exists! Looking for solution...')
               self.path=self.path[0:-1]+'+/'
            mkdir(self.path)
            self.bGates = [0]*3
            randLoc = self.genRandomGates()
            self.bGates[0] = randLoc[0]
            self.bGates[2] = randLoc[2]
            self.bGates[1] = [self.subjGateLocation for i in range(self.numTrials)]
            self.saveGates(self.bGates)
            
            with open(self.path+self.subjectID+'.Congruent.txt','w') as congFile:
                congWriter = csv.writer(congFile)
                congWriter.writerow([self.congruent])
#            self.randGateLocations = self.genRandomGates()
#            self.bGates = self.randGateLocations
#            self.saveGates(self.bGates)
#        elif self.run in ['003','004']:                                            #This bit makes the purly sequence blocks.  This is commented to let us do just R-S-R blocks.
#            self.bGates = [0]*3
#                for i in range(3):
#                    self.bGates[i] = [self.subjGateLocation for i in range(self.numTrials)]
#            self.saveGates()
        elif all([self.congruent == 'Diff',self.run == '003']):
            self.bGates = [0]*3
            self.bGates[0] = [self.subjGateLocation for i in range(self.numTrials)]
            self.bGates[1] = [self.subjGateLocation for i in range(self.numTrials)]
            self.bGates[2] = [self.subjGateLocation for i in range(self.numTrials)]
            self.saveGates(self.bGates)
        
        else:
            self.bGates = [0]*3
            randLoc = self.genRandomGates()
            self.bGates[0] = randLoc[0]
            self.bGates[2] = randLoc[2]
            self.bGates[1] = [self.subjGateLocation for i in range(self.numTrials)]
            self.saveGates(self.bGates)
    
        
    def showInst(self):
        event.clearEvents(eventType='keyboard')
        showInst = True
        while showInst == True:
            self.InstructionL1.setAutoDraw(True)
            self.InstructionL2.setAutoDraw(True)
            self.InstructionL3.setAutoDraw(True)
            if event.getKeys(['space']):
                self.InstructionL1.setAutoDraw(False)
                self.InstructionL2.setAutoDraw(False)
                self.InstructionL3.setAutoDraw(False)
                showInst = False
            else:
                self.myWin.flip()        
        
    def loadCriterion(self):
        with open(self.path+self.subjectID+'_criterion.csv','r') as critFile:
            creader = csv.reader(critFile)
            for row in creader:
                criterion = float(row[0])
        return criterion
        
    def saveCriterion(self,criterion):
        with open(self.path+self.subjectID+'_criterion.csv','w') as critFile:
            cwriter = csv.writer(critFile)
            criterion = [criterion]
            cwriter.writerow(criterion)
            
    def saveEarning(self,earning):
        with open(self.path+self.subjectID+'_earning.csv','w') as earningFile:
            ewriter = csv.writer(earningFile)
            ewriter.writerow([earning])
            
    def loadEarning(self,block):
        if self.cond == 'Pun':
            if self.run == '001' or all([self.run == '002',block == 0]):
                self.earning = 45
            else:
                with open(self.path+self.subjectID+'_earning.csv','r') as earningFile:
                    ereader = csv.reader(earningFile)
                    for row in ereader:
                        earning = float(row[0])
                self.earning = earning
        elif self.cond == 'Rew':
            if self.run == '001' or all([self.run == '002',block == 0]):
                self.earning = 0
                earning = 0
            else:
                print 'good'
                with open(self.path+self.subjectID+'_earning.csv','r') as earningFile:
                    ereader = csv.reader(earningFile)
                    for row in ereader:
                        earning = float(row[0])
                    self.earning = earning
        else:
            if self.run == '001' or all([self.run == '002',block == 0]):
                self.earning = 0
                earning = 0
            else:
                with open(self.path+self.subjectID+'_earning.csv','r') as earningFile:
                    ereader = csv.reader(earningFile)
                    for row in ereader:
                        earning = float(row[0])
                self.earning = earning
        return earning
    
    def genRandomGates(self):
        liOut = [0]*self.numBlocks
        for j in range(self.numBlocks):
            liOut[j] = [0]*self.numTrials
            for b in range(self.numTrials):
                li = [0]*10
                for i in range(10):
                    li[i] = random.uniform(0.15,1.0)
                li.sort()
                liOut[j][b] = li[0:11:2]
        return liOut

    def saveGates(self,gates):
        with open(self.path+self.subjectID+'.'+self.run+'_GateLocations.csv','w') as GateFile:
            cwriter = csv.writer(GateFile)
            for i in range(len(gates)):
                for j in gates[i]:
                    cwriter.writerow([m*self.winHeight + self.origin for m in j])

    def writeMinima(self,minima,block):
        with open(self.path+'_'+self.subjectID+'.'+str(self.run)+'.'+str(block)+'.'+'_trialMinima.csv','w') as MinFile:
            cwriter = csv.writer(MinFile)
            for j in minima:
                cwriter.writerow(j)
                
    def writeMinTimes(self,minTimes,block):
        with open(self.path+'_'+self.subjectID+'.'+str(self.run)+'.'+str(block)+'.'+'_trialMinTimes.csv','w') as MinFile:
            cwriter = csv.writer(MinFile)
            for j in minTimes:
                cwriter.writerow(j)
                
    def writeTimes(self,times,block):
        with open(self.path+'_'+self.subjectID+'.'+str(self.run)+'.'+str(block)+'.'+'_trialTimes.csv','w') as TimeFile:
            cwriter = csv.writer(TimeFile)
            for j in times:
                cwriter.writerow([j])

    def saveExtrema(self,ExtremaList,block,trial):
        with open(self.path+self.subjectID+'.'+self.run+'.'+block+'.'+trial+'.extremaList.csv','w') as extremaFile:
            cwriter = csv.writer(extremaFile)
            cwriter.writerow(ExtremaList)
     
    def saveTimeList(self,TimeList,block,trial):
            with open(self.path+self.subjectID+'.'+self.run+'.'+block+'.'+trial+'.TimeList.csv','w') as extremaFile:
                cwriter = csv.writer(extremaFile)
                cwriter.writerow(TimeList)
    
    def monitorGrip(self,forceOutputList):
            yy = self.joy.getY()
            forceOutputList.append(yy)
            forceOutputList.pop(0)
            cur_g = sum(forceOutputList)/len(forceOutputList)
            return forceOutputList,cur_g
    
    def drawTargets(self,gateLocs):
        targLoc = [i*self.winHeight + self.origin for i in gateLocs]
        self.targSpot1.setPos([0,targLoc[0]] )
        self.targSpot2.setPos([0,targLoc[1]] )
        self.targSpot3.setPos([0,targLoc[2]] )
        self.targSpot4.setPos([0,targLoc[3] ])
        self.targSpot5.setPos([0,targLoc[4]] )
        self.targSpot1.draw()
        self.targSpot2.draw()
        self.targSpot3.draw()
        self.targSpot4.draw()
        self.targSpot5.draw()
        return targLoc
    
    def checkExtremaList(self,ExtremaList,targetlist,TimeList):
        #print ('TimeList = ' + str(TimeList))
        targetlist = [targetlist[i] for i in self.TargetOrder]
        tDist = [0] * len(targetlist)
        minimaInd = [0]*len(targetlist)
        minimaList = [0]*len(targetlist)
        minimaTime = [0]*len(targetlist)
        Ind = 0
        for i in range(len(targetlist)):
            tDist[i] = [abs(j-targetlist[i]) for j in ExtremaList]
            
        if len(ExtremaList) == len(targetlist):
            minimaInd = range(5)
        else:
            for i in range(len(tDist)):
                minimaInd[i] = tDist[i].index(min(tDist[i]))
            if minimaInd != sorted(minimaInd):
                s = 0
                count = 0
                for j in range(Ind,len(tDist[i])-1):
                    if tDist[i][j] < tDist[i][j+1]:
                        if s == 0:
                            minimaInd[i] = Ind+count
                            s = 1
                            Ind = Ind + 1 + count
                            #print "Minima Ind"  + str(minimaInd)
                    count = count + 1
        for i in range(len(tDist)):
            minimaList[i] = tDist[i][minimaInd[i]]
            minimaTime[i] = TimeList[minimaInd[i]]
        return minimaList,minimaTime
    

    def storeChange(self,cur_y,p_y,sign,ExtremaList,TimeList,c,curTime):
        if sign == 1:
            if cur_y-p_y <0:
                ExtremaList[c] = p_y
                TimeList[c] = curTime
                c = c+1
                p_y = cur_y
                sign = 0
            else:
                p_y = cur_y
        else: # sign == 0:
            if cur_y-p_y >0:
                ExtremaList[c] = p_y
                TimeList[c] = curTime
                c = c+1
                p_y = cur_y
                sign = 1
            else:
                p_y = cur_y
        return p_y,sign,ExtremaList,c,TimeList

    def critTest(self,errList,timelist,blkParams):
        err = np.mean(errList)
        time = np.mean(timelist) + np.std(timelist)
        if all([time < blkParams['timeMean'] + blkParams['timeStd'],err < blkParams['minMean']]):
            blkParams['timeMean'] = np.mean(timelist)
            blkParams['minMean'] = err
            blkParams['minStd'] = np.std(errList)
            blkParams['timeStd'] = np.std(timelist)
            print "Criteria updated."
            print "Time = " + str(time + blkParams['timeStd']) 
            print "Err = " + str(err + blkParams['minStd'])            
        else:
            print "Criteria not updated."            
            print "Time = " + str(time)
            print "Err = " + str(err)
            print "Crit Time: " + str(blkParams['timeMean']+blkParams['timeStd'])
            print "Crit error: " + str(blkParams['minMean'] + blkParams['minStd'])
        with open(self.path+'blkParams.pickle','w') as pF:
            pickle.dump(blkParams,pF)
        return blkParams
        
    def openBlockFile(self,block):
        f = open(self.path+'_'+self.subjectID+'.run_'+self.run+'_block_'+str(block)+'.datafile.csv','a')
        return f
        
    def feedbackFunction(self,blkParams,trialMin,TrialTime):
        if any([i > 4 for i in trialMin]):
            feedbackAmount = 0
            print "Minimum exceeds 4."
            print "Feedback Amount: " + str(feedbackAmount)
            return feedbackAmount
        else:
            tMin = np.mean(trialMin)
            feedbackAmount = 0.0
            print 'tmin = ' + str(tMin)
            print 'trial time = ' + str(TrialTime)
            a = tMin < blkParams['minMean']+blkParams['minStd']
            b = TrialTime < blkParams['timeMean']+blkParams['timeStd']
            print a
            print b
            test = [a,b]
            print test
            if self.cond in ['Rew','RewG']:
                if all(test) == 1:
                    #print 'Rew True'
                    #feedbackAmount = (blkParams['minMean']**(-tMin*blkParams['minStd']) + blkParams['timeMean']**(-TrialTime*blkParams['timeStd'])
                    feedbackAmount = (2**(-tMin/blkParams['minMean']))# - (1-2**(TrialTime/blkParams['timeMean']/2) + 1))
                    if feedbackAmount < 0:
                        feedbackAmount = 0
            elif self.cond == ['Pun','PunG']:
                if any(test) == 0:
                    #feedbackAmount = blkParams['minMean']**(-tMin*blkParams['minStd']) + blkParams['timeMean']**(-TrialTime*blkParams['timeStd'])
                    #print 'Pun True'
                    feedbackAmount = (2**(-tMin/blkParams['minMean']))# - (1-2**(TrialTime/blkParams['timeMean']/2 - 1)))
            else:
                feedbackAmount = 0
            feedbackAmount = round(feedbackAmount,2)
            print "Feedback Amount: " + str(round(feedbackAmount,2))
            return feedbackAmount
        
        
class expPresentation:
    def __init__(self,experiment):        
        self.cur_gZero = 0
        
        self.fixSpot_null = visual.PatchStim(experiment.myWin,tex="none",mask="circle",
        pos=(0,experiment.origin), size=(0.5,0.5),color='white', autoLog=False)

        #print experiment.subjectID
        #
        #
        
    def cursorActivity(self,experiment,cur_g):
            cur_weight = experiment.cur_weight # must be > 20 for ease of squeeze
            curP = cur_g-self.cur_gZero
            curP_norm = -1*curP
            y_zeroed = (1/(1+exp(-0.9*((curP_norm)*12-5))))*cur_weight*-1
            cur_zero = experiment.origin-experiment.curConstant
            cur_y = experiment.origin - y_zeroed
#            CUR = visual.TextStim(win=experiment.myWin, text='grip = '+str(curP_norm), wrapWidth=10.0, font='Arial',
#            pos=[0, 1], height=1.0, color=[1.000,1.000,1.000], colorSpace='rgb', opacity=1, depth=0.0)
#            YZ = visual.TextStim(win=experiment.myWin, text='cur_y = '+str(cur_y), wrapWidth=10.0, font='Arial',
#            pos=[0, 2], height=1.0, color=[1.000,1.000,1.000], colorSpace='rgb', opacity=1, depth=0.0)
#            YZ.draw()
#            CUR.draw()
            #print 'cur_y = ' + str(cur_y)
            self.fixSpot_null.setPos((0,cur_y))
            self.fixSpot_null.draw()
            return cur_y
                
    # Subject instructions, change phrase in experiment.
    def showInst(self,experiment):
        event.clearEvents(eventType='keyboard')
        showInst = True
        if experiment.run in ['001','006','007','008']:
            
            self.InstructionRunL1 = visual.TextStim(win=experiment.myWin, text='Hit the gates in the correct order.  Squeeze the handle to move up.', wrapWidth=10.0, font='Arial',
            pos=[0, 1], height=1.0, color=[1.000,1.000,1.000], colorSpace='rgb', opacity=1, depth=0.0)
            
            self.InstructionRunL3 = visual.TextStim(win=experiment.myWin, text='Press Space to continue.', wrapWidth=10.0, font='Arial',
            pos=[0, -1], height=1.0, color=[1.000,1.000,1.000], colorSpace='rgb', opacity=1, depth=0.0)
        
        else:
            
            self.InstructionRunL1 = visual.TextStim(win=experiment.myWin, text='Hit the gates in the right order.  Squeeze the handle to move up.', wrapWidth=10.0, font='Arial',
            pos=[0, 1], height=1.0, color=[1.000,1.000,1.000], colorSpace='rgb', opacity=1, depth=0.0)
            
            self.InstructionRunL3 = visual.TextStim(win=experiment.myWin, text='Press Space to continue.', wrapWidth=10.0, font='Arial',
            pos=[0, -1], height=1.0, color=[1.000,1.000,1.000], colorSpace='rgb', opacity=1, depth=0.0)
        
        while showInst == True:
            self.InstructionRunL1.setAutoDraw(True)
            self.InstructionRunL3.setAutoDraw(True)
            if event.getKeys(['space']):
                self.InstructionRunL1.setAutoDraw(False)
                self.InstructionRunL3.setAutoDraw(False)
                showInst = False
            else:
                event.clearEvents()
                experiment.myWin.flip()
                
    
    def waitTrigger(self,experiment):
        self.waitText = visual.TextStim(win=experiment.myWin, text='Waiting for trigger...', wrapWidth=10.0, font='Arial',
        pos=[0, 1], height=1.0, color=[1.000,1.000,1.000], colorSpace='rgb', opacity=1, depth=0.0)
        event.clearEvents(eventType='keyboard')
        trigWait = True
        while trigWait == True:
            self.waitText.setAutoDraw(True)
            if event.getKeys(['5']):
                self.waitText.setAutoDraw(False)
                trigWait = False
                experiment.myWin.flip()
            else:
                event.clearEvents()
                experiment.myWin.flip()
        curT = time.time()
        absTime = time.time()
        displayFix = True
        self.cur_gZero = [0]*100
        c = 0
        while displayFix == True:
            if c < 100:
                self.cur_gZero[c] = experiment.joy.getY()
                c = c+1
            if c == 100:
                #print self.cur_gZero
                self.cur_gZero = sum(self.cur_gZero)/100
                c = c+1
            curT = time.time()
            if curT - absTime >= 12:
                displayFix = False
                experiment.myWin.flip()
                event.clearEvents()
            elif curT-absTime < 12 and curT-absTime > 7: #blue cross for 5 seconds
                experiment.fixationCrossB.draw()
                experiment.myWin.flip()
                event.clearEvents()
            else:
                experiment.fixationCross.draw()
                experiment.myWin.flip()
                event.clearEvents()
        
    def blockWait(self,experiment,earning):
        #self.breakPhraseL2 = ''
        if any([experiment.run in ['001'],experiment.cond == 'Cont',experiment.congruent == 'Same']):
            self.breakPhraseL2 = ''
        else:
            self.breakPhraseL2 = str("You have earned " + str(earning))
        self.breakPhraseL1 = ''                                 # for non-earning version.
        curT = time.time()
        absTime = time.time()
        self.breakL2 = visual.TextStim(win=experiment.myWin, text=self.breakPhraseL2, wrapWidth=10.0, font='Arial',
        pos=[0, 0], height=2.0, color=[1.000,1.000,1.000], colorSpace='rgb', opacity=1, depth=0.0)
        while curT - absTime < experiment.blockWaitDur:
            experiment.breakL1.setAutoDraw(True)
            self.breakL2.setAutoDraw(True)
            experiment.breakL3.setAutoDraw(True)
            curT = time.time()
            experiment.myWin.flip()
            event.clearEvents()
        experiment.breakL1.setAutoDraw(False)
        self.breakL2.setAutoDraw(False)
        experiment.breakL3.setAutoDraw(False)
        experiment.myWin.flip()
        curT = time.time()
        absTime = time.time()
        displayFix = True
        while displayFix == True:
            curT = time.time()
            if curT - absTime >= experiment.blockFixDur:
                displayFix = False
                experiment.myWin.flip()
                event.clearEvents()
            elif curT-absTime < experiment.blockFixDur and curT-absTime > experiment.blockFixDur-5:
                experiment.fixationCrossB.draw()
                experiment.myWin.flip()
                event.clearEvents()
            else:
                experiment.fixationCross.draw()
                experiment.myWin.flip()
                event.clearEvents()
                
    def presentRun(self,experiment):
        block = 0
        trial = 0
        errorList = []
        btimes = []
        st = time.time()
        bErrorList = [0]*experiment.numTrials
        bTimesList = [0]*experiment.numTrials
        bMinTimes = [0]*experiment.numTrials
        bt = time.time()
        btimes.append(bt-st)
        while block < experiment.numBlocks:
            B_file = experiment.openBlockFile(block)
            B_writer = csv.writer(B_file)
            B_writer.writerow(['Trial','cursorPos','time'])
            if experiment.run == '001' and block == 0:
                blkParams = {'minMean':1000,'minStd':1000,'timeMean':1000,'timeStd':1000}
            else:
                p = open(experiment.path+'blkParams.pickle','r')
                blkParams = pickle.load(p)
                p.close()
            earning = experiment.loadEarning(block)
            GateLocs = experiment.bGates[block]
            blkAmount = 0
            while trial < experiment.numTrials:
                trialMinima,minimaTime,tTime,fbAmount = self.presentTrainingTrials(experiment,GateLocs[trial],blkParams,trial,B_file,block)
                print GateLocs[trial]
                bErrorList[trial] = trialMinima
                bMinTimes[trial] = minimaTime
                bTimesList[trial] = tTime
                blkAmount = blkAmount + fbAmount
                trial = trial + 1
            experiment.writeMinima(bErrorList,block)
            experiment.writeMinTimes(bMinTimes,block)
            experiment.writeTimes(bTimesList,block)
            blkParams = experiment.critTest(bErrorList,bMinTimes,blkParams)
            trial = 0
            errorList = []
            B_file.close()
            earning = earning + blkAmount
            experiment.saveEarning(earning)
            self.blockWait(experiment,earning)
            block = block + 1
            #print experiment.earning
#            with open(experiment.path+experiment.subjectID+'.run_'+experiment.run+'times.csv','a') as t_file:
#                T_writer = csv.writer(t_file)
#                T_writer.writerow(btimes)
        #print bErrorList
        #return bErrorList

    def presentTrainingTrials(self,experiment,GateLocs,blkParams,trial,B_file,block):
            B_writer = csv.writer(B_file)
            forceOutputList = [0] * 10
            sign = 1
            counter =0
            forceOutputList,cur_g = experiment.monitorGrip(forceOutputList)
            startPos = self.cursorActivity(experiment,cur_g)
            cur_y = self.cursorActivity(experiment,cur_g)
            p_y = cur_y
            ExtremaList = [16]*10000
            TimeList = [0]*10000
            while cur_y <=startPos+0.1:
                forceOutputList,cur_g = experiment.monitorGrip(forceOutputList)
                experiment.originSpot.draw()
                targLocs = experiment.drawTargets(GateLocs)
                cur_y = self.cursorActivity(experiment,cur_g)
                experiment.myWin.flip()
            trialtime = time.time()
            tTime = time.time()
            while cur_y >= experiment.origin+0.4:
#                h = visual.TextStim(win=experiment.myWin, text='limit = '+str(experiment.origin), wrapWidth=10.0, font='Arial',
#                pos=[0, 3], height=1.0, color=[1.000,1.000,1.000], colorSpace='rgb', opacity=1, depth=0.0)
#                h = visual.TextStim(win=experiment.myWin, text='counter = '+str(counter), wrapWidth=10.0, font='Arial',
#                pos=[0, 4], height=1.0, color=[1.000,1.000,1.000], colorSpace='rgb', opacity=1, depth=0.0)
#                h.draw()
                experiment.originSpot.draw()
                targLocs = experiment.drawTargets(GateLocs)
                
                forceOutputList,cur_g = experiment.monitorGrip(forceOutputList)
                cur_y = self.cursorActivity(experiment,cur_g)
                
                cur_t = time.time()
                tTime = cur_t - trialtime
                 
                [p_y,sign,ExtremaList,counter,TimeList] = experiment.storeChange(cur_y,p_y,sign,ExtremaList,TimeList,counter,tTime)
                B_writer.writerow([trial,cur_y,tTime])
                
                experiment.myWin.flip()
                event.clearEvents()
                
            if counter < 5:
                TimeList[counter+1:5] = [tTime] * (5-counter)
                counter = 5
            ExtremaList=ExtremaList[0:counter]
            TimeList=TimeList[0:counter]
            counter = 0
#            experiment.saveExtrema(ExtremaList,str(block),str(trial))
#            experiment.saveTimeList(TimeList,str(block),str(trial))
            [trialMinima,minimaTime] = experiment.checkExtremaList(ExtremaList,targLocs,TimeList)
            feedbackAmount = experiment.feedbackFunction(blkParams,trialMinima,tTime)
            if experiment.run != '999':
                if all([experiment.congruent == 'Diff',experiment.cond !='Cont',experiment.run!='005']) :
                    FeedbackAmountDisp = visual.TextStim(win=experiment.myWin, text=str(feedbackAmount) + ' GBP', wrapWidth=10.0, font='Arial',
                    pos=[0, 1], height=2.0, color=[1.000,1.000,1.000], colorSpace='rgb', opacity=1, depth=0.0)
#                FeedbackAmountDisp2 = visual.TextStim(win=experiment.myWin, text=str(round(tTime,2)) + ' ' + str(round(np.mean(trialMinima),2)), wrapWidth=10.0, font='Arial',
#                pos=[0, 2], height=2.0, color=[1.000,1.000,1.000], colorSpace='rgb', opacity=1, depth=0.0)
                elif all([experiment.congruent == 'Diff',experiment.cond =='Cont',experiment.run!='005']) :
                    FeedbackAmountDisp = visual.TextStim(win=experiment.myWin, text='You have money', wrapWidth=10.0, font='Arial',
                    pos=[0, 1], height=2.0, color=[1.000,1.000,1.000], colorSpace='rgb', opacity=1, depth=0.0)
                else:
                    FeedbackAmountDisp = visual.TextStim(win=experiment.myWin, text='Wait...', wrapWidth=10.0, font='Arial',
                    pos=[0, 1], height=2.0, color=[1.000,1.000,1.000], colorSpace='rgb', opacity=1, depth=0.0)
                FeedbackAmountDisp.draw()
#                FeedbackAmountDisp2.draw()
                
            self.fixSpot_null.setPos((0,experiment.origin))
            experiment.originSpot.draw()
            self.fixSpot_null.draw()
            experiment.myWin.flip()
            core.wait(experiment.trialWait)
            
            return trialMinima,minimaTime,tTime,feedbackAmount
            

currentExp = Exp()  
expPresent = expPresentation(currentExp)
expPresent.showInst(currentExp)
expPresent.waitTrigger(currentExp)
t = time.time()
cur_t = time.time()
expPresent.presentRun(currentExp)
cur_t = time.time()
currentExp.myWin.close()
core.quit()
    

        



