#!/usr/bin/env python2
from __future__ import division
from psychopy import visual, core, event, gui
from psychopy.hardware import joystick
from math import fabs, sin
from scipy.signal import argrelextrema
import numpy as np
import pygame
import time
import random
import csv
from os import makedirs

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
        self.expInfoDic = {'participant':'', 'session':'001','run':''}
        self.dlg = gui.DlgFromDict(dictionary=self.expInfoDic, title=self.expName)
        if self.dlg.OK == False: core.quit()  # user pressed cancel
        self.subjectID = self.expInfoDic['participant']
        self.run = self.expInfoDic['run']
        print self.subjectID
        print self.run
        self.myWin = visual.Window((800.0,800.0),allowGUI=True,winType='pygame',fullscr=True,units='cm',monitor='testMonitor') # This is the experiment window to draw in
        self.nJoysticks = joystick.getNumJoysticks()
        self.joy = joystick.Joystick(0)
        #
        # Experiment variables
        #
        self.eRate = 0.01
        self.earningTIme = 19
        if self.run in ['006','007','008']:
            self.curConstant = 22
        else:
            self.curConstant = 16
        self.cur_weight = 35
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
        self.path = './data/HV_'+str(self.subjectID)+'.Pun/'
        self.myMouse = event.Mouse(visible=0)
        self.testRuns = ['006','007','008']
        #
        self.targSpot = visual.Circle(self.myWin,
        pos=(0,0), size=(1.5,1.5),opacity=1.0,fillColor='DodgerBlue',lineColor='DodgerBlue',lineWidth=0,autoLog=False)
        #
        self.originSpot = visual.PatchStim(self.myWin,tex="none", mask="circle",
        pos=(0,self.origin), size=(2,2),color='black', autoLog=False)
        #
        self.fixationCross = visual.TextStim(win=self.myWin, text='+', wrapWidth=10.0, font='Arial',
        pos=[0, 0], height=2.0, color='white', opacity=1, depth=0.0)
        self.fixationCrossB = visual.TextStim(win=self.myWin, text='+', wrapWidth=10.0, font='Arial',
        pos=[0, 0], height=2.0, color='black', opacity=1, depth=0.0)
        #
        self.block = 0
        self.loadEarning(self.block)
            
        self.instPhraseL1= str('Track the blue circle')
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
        pos=[0, 2], height=1.0, color=[1.000,1.000,1.000], colorSpace='rgb', opacity=1, depth=0.0)
        
        
        self.breakL3 = visual.TextStim(win=self.myWin, text=self.breakPhraseL3, wrapWidth=10.0, font='Arial',
        pos=[0, -2], height=1.0, color=[1.000,1.000,1.000], colorSpace='rgb', opacity=1, depth=0.0)
        
        
        print self.run
        
        
        if self.run == '001':
            makedirs(self.path)
            self.genSubjSine()
            self.Amps,self.Pers = self.genRandSine()
            self.bAmps = self.Amps
            self.bPers = self.Pers
            self.saveSine()
        
        elif self.run in ['003','004']:
            subjAmps,subjPers = self.readSubjSine()
            seqAmps = [subjAmps for i in range(self.numTrials)]
            seqPers = [subjPers for i in range(self.numTrials)]
            self.bAmps = [seqAmps for i in range(3)]
            self.bPers = [seqPers for i in range(3)]
            self.saveSine()
            
            
        else:
            self.bAmps = [0,0,0]
            self.bPers = [0,0,0]
            self.numblocks = 2
            self.subjAmps,self.subjPers = self.readSubjSine()
            self.Amps,self.Pers = self.genRandSine()
            self.bAmps[0] = self.Amps[0]
            self.bPers[0] = self.Pers[0]
            self.bAmps[1] = [self.subjAmps for i in range(self.numTrials)]
            self.bPers[1] = [self.subjPers for i in range(self.numTrials)]
            self.bAmps[2] = self.Amps[1]
            self.bPers[2] = self.Pers[1]
            self.saveSine()
    
    
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
            
    def saveEarning(self):
        with open(self.path+self.subjectID+'_earning.csv','w') as earningFile:
            ewriter = csv.writer(earningFile)
            ewriter.writerow([self.earning])
            
    def loadEarning(self,block):
        if self.run in ['001'] or self.run == '002' and block == 0:
            self.earning = 45
        else:
            with open(self.path+self.subjectID+'_earning.csv','r') as earningFile:
                ereader = csv.reader(earningFile)
                for row in ereader:
                    earning = float(row[0])
            self.earning = earning
        return
    
    def genPers(self):
        Periods = []
        A = random.randrange(1,5)/100
        B = random.randrange(30,40)/100
        C = random.randrange(100,300)/100
        D = random.randrange(130,180)/100
        #A = random.randrange(1,5)/100
        #B = random.randrange(20,40)/100
        #C = random.randrange(75,125)/100
        #D = random.randrange(130,180)/100
        Periods = [A,B,C,D]
        return Periods
    
    def genAmp(self):
        Amplitudes = {}
        A = random.randrange(500,1000)/1000
        for i in range(4):
            Dictkey = 'Amp_' + str(i)
            while A not in Amplitudes.values():
                Amplitudes[Dictkey] = A
            A = random.random()
        return Amplitudes
    
    def gensubjSine(self):
        X = range(1,1000) 
        X = [ i/125 for i in X] 
        brake = 1
        while brake == 1:
            AmpL = self.genAmp()
            A = AmpL.values()
            P = self.genPers()
            Y = [ (A[0]*sin(P[0] * i)**2 + (A[1]*sin(P[1] * i))**2 + (A[2]*sin(P[2] * i))**2 + (A[3]*sin(P[3] * i))**2) for i in X ] 
            Y = np.asarray(Y)
            maxima = argrelextrema(Y, np.greater)
            mlen = len(maxima[0])
            maxMin = min(Y[maxima[0]])
            maxMax = max(Y[maxima[0]])
            if max(Y) < 1 and sum(Y)/len(Y) > 0.3 and sum(Y)/len(Y) < 0.7 and mlen > 4 and mlen < 7 and maxMin > 0.2 and maxMax > 0.75:
                brake = 0
        return A,P
        
    def genSubjSine(self):
            RR = random.randint(1,6)
            if RR == 1:
                A = [0.16148773179680187, 0.06455745557296033, 0.714, 0.6597653401814741]
                P = [0.04, 0.34, 1.82, 1.36]
            elif RR == 2:
                A = [0.6018758448033984, 0.2016239934660392, 0.648, 0.5539550009944636]
                P =  [0.02, 0.35, 2.11, 1.49]
            elif RR == 3:
                A = [0.05504903276757944, 0.20162364624220908, 0.695, 0.5774170009878601]
                P = [0.01, 0.34, 1.93, 1.35]
            elif RR == 4:
                A = [0.6066397605275559, 0.3776143979801515, 0.805, 0.5434699646541644]
                P = [0.03, 0.35, 2.05, 1.77]
            elif RR == 5:
                A = [0.7922822795267915, 0.3447533857022764, 0.692, 0.6185935466858701]
                P = [0.01, 0.31, 1.14, 1.76]
            else: 
                A = [0.5823296749960826, 0.3708979653968577, 0.629, 0.5557618860125737]
                P = [0.03, 0.33, 2.37, 1.76]
            #A,P = self.gensubjSine()
            self.subjAmps = A
            self.subjPers = P
            with open(self.path+'_'+self.subjectID + '_Amplitudes.csv','wr') as AmpFile:
                swriter = csv.writer(AmpFile)
                swriter.writerow(self.subjAmps)
            with open(self.path+'_'+self.subjectID + '_Periods.csv','wr') as PerFile:
                pwriter = csv.writer(PerFile)
                pwriter.writerow(self.subjPers)
                
    def saveSine(self):
        with open(self.path+'_'+self.subjectID + '.run_'+self.run+'_Amplitudes.csv','wr') as AmpFile:
                swriter = csv.writer(AmpFile)
                for amp in self.bAmps:
                    for i in amp:
                        swriter.writerow(i)
        with open(self.path+'_'+self.subjectID + '.run_'+self.run+ '_Periods.csv','wr') as PerFile:
                pwriter = csv.writer(PerFile)
                for per in self.bPers:
                    for i in per:
                        pwriter.writerow(i)
                    
    def genRandSine(self):
            amps = []
            pers = []
            j = 0
            while j < self.numBlocks:
                a = []
                p = []
                b = 0
                while b < self.numTrials:
                    A,P = self.gensubjSine()
                    a.append(A)
                    p.append(P)
                    b = b+1
                amps.append(a)
                pers.append(p)
                j = j+1
            for amp in amps:
                print 'Rand Amps: ' + str(amp)
            for per in pers:
                print 'Rand Pers: ' + str(per)
            return amps,pers
            
    def readSubjSine(self):
            subjAmps = []
            subjPers = []
            with open(self.path+'_'+self.subjectID + '_Amplitudes.csv','rw') as AmpFile:
                sreader = csv.reader(AmpFile)
                for row in sreader:
                        subjAmp = row
            for i in subjAmp:
                print i
                subjAmps.append(float(i))
            with open(self.path+'_'+self.subjectID + '_Periods.csv','rw') as PerFile:
                preader = csv.reader(PerFile)
                for row in preader:
                        subjPer = row
            for i in subjPer:
                print i
                subjPers.append(float(i))
            return subjAmps,subjPers
    
        
    def monitorGrip(self,forceOutputList):
            yy = self.joy.getY()
            forceOutputList.append(yy)
            forceOutputList.pop(0)
            cur_g = sum(forceOutputList)/len(forceOutputList)
            return forceOutputList,cur_g
         
     
    def targetMotion(self,As,Ps,trial,tTime):
        A = As[trial]
        P = Ps[trial]
        y = (A[0]*sin(P[0] * tTime)**2 + (A[1]*sin(P[1] * tTime))**2 + (A[2]*sin(P[2] * tTime))**2 + (A[3]*sin(P[3] * tTime))**2)
        Y = self.origin + y*16
        self.targSpot.setPos((0,Y))
        self.targSpot.draw()
        return Y
        
    def compareCur2Tar(self,errorList,cur_y,tar_y,fs):
        currentError = abs(cur_y-tar_y)
        errorList[fs]=currentError
        return currentError,errorList
    
    def blockElist(self,errorList):
        errorList = errorList[10:]
        BErrorList = np.median(errorList)
        print 'BErrorList =  ' + str(BErrorList)
        return BErrorList
    
    def critTest(self,errList,criterion):
        err = np.mean(errList)
        print 'testCriterion: ' + str(err)
        print 'criterion: ' + str(criterion)
        if err < criterion:
            criterion = err
        print 'Next criterion = ' + str(criterion)
        return criterion
        
class expPresentation:
    def __init__(self,experiment):        
        
        
        self.fixSpot_null = visual.PatchStim(experiment.myWin,tex="none",mask="circle",
        pos=(0,experiment.origin), size=(0.5,0.5),color='white', autoLog=False)
        
        self.fixSpot_FB = visual.PatchStim(experiment.myWin,tex="none",mask="circle",
        pos=(0,experiment.origin), size=(0.5,0.5),color='red', autoLog=False)
        
        
        print experiment.subjectID
        #
        #
        
    def cursorActivity(self,experiment,cur_g,FB):
            #print 'cur_g = ' + str(cur_g)
            cur_weight = experiment.cur_weight # must be > 20 for ease of squeeze
            y_zeroed = cur_weight - cur_g*cur_weight
            #print 'y_zeroed = ' + str(y_zeroed)
            cur_zero = experiment.origin-experiment.curConstant
            cur_y = cur_zero + y_zeroed
            #print 'cur_y = ' + str(cur_y)
            if FB == 0:
                self.fixSpot_FB.setPos((0, cur_y))
                self.fixSpot_null.setPos((0,cur_y))
                self.fixSpot_FB.draw()
                self.fixSpot_null.draw()
            else:
                self.fixSpot_null.setPos((0, cur_y))
                self.fixSpot_FB.setPos((0, cur_y))
                self.fixSpot_null.draw()
                self.fixSpot_FB.draw()
            return cur_y
        
    def compareErr2Crit(self,experiment,currentError,criterion,t):
        if experiment.run == '001':
            FB = 0
        else:
            if currentError > criterion:
                t = t+1
                FB = 1
                if t >= experiment.earningTIme:
                    experiment.earning = experiment.earning - experiment.eRate
                    t = 0
            else:
                FB = 0
            return t,FB
                
    # Subject instructions, change phrase in experiment.
    def showInst(self,experiment):
        event.clearEvents(eventType='keyboard')
        showInst = True
        if experiment.run in ['001','006','007','008']:
            self.InstructionRunL1 = visual.TextStim(win=experiment.myWin, text='Track the blue circle with the white dot.  Squeeze the handle to move up.', wrapWidth=10.0, font='Arial',
            pos=[0, 1], height=1.0, color=[1.000,1.000,1.000], colorSpace='rgb', opacity=1, depth=0.0)
            self.InstructionRunL2 = visual.TextStim(win=experiment.myWin, text='', wrapWidth=10.0, font='Arial',
            pos=[0, 0], height=1.0, color=[1.000,1.000,1.000], colorSpace='rgb', opacity=1, depth=0.0)
            self.InstructionRunL3 = visual.TextStim(win=experiment.myWin, text='Press Space to continue.', wrapWidth=10.0, font='Arial',
            pos=[0, -1], height=1.0, color=[1.000,1.000,1.000], colorSpace='rgb', opacity=1, depth=0.0)
        else:
            self.InstructionRunL1 = visual.TextStim(win=experiment.myWin, text='Track the blue circle with the white dot.  Squeeze the handle to move up.', wrapWidth=10.0, font='Arial',
            pos=[0, 1], height=1.0, color=[1.000,1.000,1.000], colorSpace='rgb', opacity=1, depth=0.0)
            self.InstructionRunL2 = visual.TextStim(win=experiment.myWin, text='Your tracking performance will determine how much money you earn.', wrapWidth=10.0, font='Arial',
            pos=[0, 0], height=1.0, color=[1.000,1.000,1.000], colorSpace='rgb', opacity=1, depth=0.0)
            self.InstructionRunL3 = visual.TextStim(win=experiment.myWin, text='Press Space to continue.', wrapWidth=10.0, font='Arial',
            pos=[0, -1], height=1.0, color=[1.000,1.000,1.000], colorSpace='rgb', opacity=1, depth=0.0)
        while showInst == True:
            self.InstructionRunL1.setAutoDraw(True)
            self.InstructionRunL2.setAutoDraw(True)
            self.InstructionRunL3.setAutoDraw(True)
            if event.getKeys(['space']):
                self.InstructionRunL1.setAutoDraw(False)
                self.InstructionRunL2.setAutoDraw(False)
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
        while displayFix == True:
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
        
    def blockWait(self,experiment,criterion):
        experiment.saveCriterion(criterion)
        experiment.saveEarning()
        if experiment.run in ['001','006','007','008']:
            self.breakPhraseL2 = ''
        else:
            self.breakPhraseL2 = str("You have $"+ str(experiment.earning))
        curT = time.time()
        absTime = time.time()
        self.breakL2 = visual.TextStim(win=experiment.myWin, text=self.breakPhraseL2, wrapWidth=10.0, font='Arial',
        pos=[0, 0], height=1.0, color=[1.000,1.000,1.000], colorSpace='rgb', opacity=1, depth=0.0)
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
        BErrorList = [0]*experiment.numBlocks
        if experiment.run == '001' or experiment.run in experiment.testRuns:
            while block < experiment.numBlocks:
                bt = time.time()
                btimes.append(bt-st)
                B_file = open(experiment.path+experiment.subjectID+'.run_'+experiment.run+'_block_'+str(block)+'.datafile.csv','a')
                B_writer = csv.writer(B_file)
                B_writer.writerow(['Trial','criterion','targPos','cursorPos','absError','signedError','FB','time'])
                print 'Block : ' + str(block)
                criterion = 1000
                As = experiment.bAmps[block]
                Ps = experiment.bPers[block]
                print 'A = ' + str(As)
                print 'P = ' + str(Ps)
                while trial < experiment.numTrials:
                    errorList = self.presentTrainingTrials(experiment,As,Ps,criterion,errorList,trial,B_file)
                    bErrorList[trial]=(experiment.blockElist(errorList))
                    trial = trial + 1
                temp=np.mean(bErrorList)
                trial = 0
                BErrorList[block]=temp
                bErrorList=[0]*experiment.numTrials
                errorList = []
                block = block+1
                self.blockWait(experiment,criterion)
                B_file.close()
            criterion = experiment.critTest(BErrorList,criterion)
            experiment.saveCriterion(criterion)
            with open(experiment.path+experiment.subjectID+'.run_'+experiment.run+'times.csv','a') as t_file:
                T_writer = csv.writer(t_file)
                T_writer.writerow(btimes)
        else:
            bt = time.time()
            btimes.append(bt-st)
            while block < experiment.numBlocks:
                B_file = open(experiment.path+experiment.subjectID+'.run_'+experiment.run+'_block_'+str(block)+'.datafile.csv','a')
                B_writer = csv.writer(B_file)
                B_writer.writerow(['Trial','criterion','targPos','cursorPos','absError','signedError','FB','time'])
                criterion = experiment.loadCriterion()
                experiment.loadEarning(block)
                As = experiment.bAmps[block]
                Ps = experiment.bPers[block]
                #print 'A = ' + str(As)
                #print 'P = ' + str(Ps)
                while trial < experiment.numTrials:
                    errorList = self.presentTrials(experiment,As,Ps,criterion,errorList,trial,B_file)
                    bErrorList[trial]=(experiment.blockElist(errorList))
                    trial = trial + 1
                trial = 0
                errorList = []
                B_file.close()
                criterion = experiment.critTest(bErrorList,criterion)
                self.blockWait(experiment,criterion)
                block = block + 1
            with open(experiment.path+experiment.subjectID+'.run_'+experiment.run+'times.csv','a') as t_file:
                T_writer = csv.writer(t_file)
                T_writer.writerow(btimes)
            #print bErrorList
            return bErrorList

    def presentTrainingTrials(self,experiment,As,Ps,criterion,errorList,trial,B_file):
            forceOutputList = [0] * 10
            trialtime = time.time()
            cur_t = time.time()
            tTime = cur_t - trialtime
            FB = 0
            fs = 0
            errorList=[0]*10000
            while tTime < experiment.trialLen:
                experiment.originSpot.draw()
                Y = experiment.targetMotion(As,Ps,trial,tTime)
                forceOutputList,cur_g = experiment.monitorGrip(forceOutputList)
                cur_y = self.cursorActivity(experiment,cur_g,FB)
                cur_t = time.time()
                tTime = cur_t - trialtime
                experiment.myWin.flip()
                currentError,errorList = experiment.compareCur2Tar(errorList,cur_y,Y,fs)
                B_writer = csv.writer(B_file)
                B_writer.writerow([trial,criterion,Y,cur_y,currentError,Y-cur_y,FB,tTime])
                event.clearEvents()
                fs=fs+1
            trial = trial + 1
            experiment.targSpot.setPos((0,experiment.origin))
            self.fixSpot_null.setPos((0,experiment.origin))
            experiment.originSpot.draw()
            experiment.targSpot.draw()
            errorList=errorList[0:fs]
            #print 'Length error list = ' + str(len(errorList))
            self.fixSpot_null.draw()
            experiment.myWin.flip()
            core.wait(experiment.trialWait)
            return errorList
            
    def presentTrials(self,experiment,As,Ps,criterion,errorList,trial,B_file):
            t = 0
            FB = 0
            fs = 0
            total = 0
            forceOutputList = [experiment.origin] * 10
            trialtime = time.time()
            cur_t = time.time()
            tTime = cur_t - trialtime
            errorList=[0]*10000
            while tTime < experiment.trialLen:
                experiment.originSpot.draw()
                Y = experiment.targetMotion(As,Ps,trial,tTime)
                forceOutputList,cur_g = experiment.monitorGrip(forceOutputList)
                cur_y = self.cursorActivity(experiment,cur_g,FB)
                cur_t = time.time()
                tTime = cur_t - trialtime
                currentError,errorList = experiment.compareCur2Tar(errorList,cur_y,Y,fs)
                t,FB = self.compareErr2Crit(experiment,currentError,criterion,t)
                if t == 1:
                    total = total + 1
                B_writer = csv.writer(B_file)
                B_writer.writerow([trial,criterion,Y,cur_y,currentError,Y-cur_y,FB,tTime])
                experiment.myWin.flip()
                event.clearEvents()
                fs=fs+1
            trial = trial + 1
            totalPhrase = 'You lost $' + str(total*experiment.eRate)
            self.totalPhraseL = visual.TextStim(win=experiment.myWin, text=totalPhrase, wrapWidth=10.0, font='Arial',
            pos=[0, 0], height=1.0, color=[1.000,1.000,1.000], colorSpace='rgb', opacity=1, depth=0.0)
            startbw = time.time()
            curbw = time.time()
            self.totalPhraseL.draw()
            while curbw - startbw < experiment.trialWait:
                if curbw - startbw < experiment.trialWait - 1:
                    self.totalPhraseL.draw()
                    experiment.myWin.flip()
                    curbw = time.time()
                else:
                    experiment.targSpot.setPos((0,experiment.origin))
                    self.fixSpot_null.setPos((0,experiment.origin))
                    self.fixSpot_null.setPos((0,experiment.origin))
                    experiment.originSpot.draw()
                    experiment.targSpot.draw()
                    errorList=errorList[0:fs]
                    curbw = time.time()
            #print 'Length error list = ' + str(len(errorList))
            self.fixSpot_null.draw()
            experiment.myWin.flip()
            event.clearEvents()
            return errorList

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
    

        



