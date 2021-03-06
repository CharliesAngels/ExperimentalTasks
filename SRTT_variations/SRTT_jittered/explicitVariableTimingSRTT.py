#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
This experiment was created using PsychoPy2 Experiment Builder (v1.83.01), Mon Aug  7 12:15:42 2017
If you publish work using this script please cite the relevant PsychoPy publications
  Peirce, JW (2007) PsychoPy - Psychophysics software in Python. Journal of Neuroscience Methods, 162(1-2), 8-13.
  Peirce, JW (2009) Generating stimuli for neuroscience using PsychoPy. Frontiers in Neuroinformatics, 2:10. doi: 10.3389/neuro.11.010.2008
"""

from __future__ import division  # so that 1/3=0.333 instead of 1/3=0
from psychopy import locale_setup, visual, core, data, event, logging, sound, gui
from psychopy.constants import *  # things like STARTED, FINISHED
import numpy as np  # whole numpy lib is available, prepend 'np.'
from numpy import sin, cos, tan, log, log10, pi, average, sqrt, std, deg2rad, rad2deg, linspace, asarray
from numpy.random import random, randint, normal, shuffle
import os  # handy system and path functions
import sys # to get file system encoding

# Ensure that relative paths start from the same directory as this script
_thisDir = os.path.dirname(os.path.abspath(__file__)).decode(sys.getfilesystemencoding())
os.chdir(_thisDir)

# Store info about the experiment session
expName = 'explicitJitter'  # from the Builder filename that created this script
expInfo = {u'6 Gender (M/F)': u'', u'2 cond': u'Seq', u'1 participant': u'', u'4 numTrials': u'64', u'3 seq': u'', u'8 Session': u'', u'5 Age': u'', u'7 Music experience (1-7)': u''}
dlg = gui.DlgFromDict(dictionary=expInfo, title=expName)
if dlg.OK == False: core.quit()  # user pressed cancel
expInfo['date'] = data.getDateStr()  # add a simple timestamp
expInfo['expName'] = expName

# Data file name stem = absolute path + name; later add .psyexp, .csv, .log, etc
filename = _thisDir + os.sep + u'data/%s_%s_%s_%s' %(expInfo['1 participant'],expInfo['2 cond'], expName, expInfo['date'])

# An ExperimentHandler isn't essential but helps with data saving
thisExp = data.ExperimentHandler(name=expName, version='',
    extraInfo=expInfo, runtimeInfo=None,
    originPath=None,
    savePickle=True, saveWideText=True,
    dataFileName=filename)
#save a log file for detail verbose info
logFile = logging.LogFile(filename+'.log', level=logging.EXP)
logging.console.setLevel(logging.WARNING)  # this outputs to the screen, not a file

endExpNow = False  # flag for 'escape' or other condition => quit the exp

# Start Code - component code to be run before the window creation

# Setup the Window
win = visual.Window(size=(1680, 1050), fullscr=True, screen=0, allowGUI=False, allowStencil=False,
    monitor='testMonitor', color=[0,0,0], colorSpace='rgb',
    blendMode='avg', useFBO=True,
    )
# store frame rate of monitor if we can measure it successfully
expInfo['frameRate']=win.getActualFrameRate()
if expInfo['frameRate']!=None:
    frameDur = 1.0/round(expInfo['frameRate'])
else:
    frameDur = 1.0/60.0 # couldn't get a reliable measure so guess

# Initialize components for Routine "Inst"
InstClock = core.Clock()
from numpy import divide,round
import random
import os
import csv
from time import time
from numpy import median

stimLen = 0.8
trialLen = 1.0
vector = []
count = 0
Respvec = []
Keyvec = []
crit = 1000
BlockRTs = []
Earning_Trial = []
BlockNum = 0
TT = 0
cond = expInfo['2 cond']
seq = expInfo['3 seq']
numTrials = int(expInfo['4 numTrials'])
BlockRTs = [0]*numTrials
timingFile = open('./data/' + expInfo['1 participant'] + '.timingFile.csv','wa')

if seq == '1':
    sequence = [1,2,2,4,3,3,2,1,1,4,2,3,4,4,1,3]
else:
    sequence = [3,3,4,3,1,1,2,4,4,1,3,2,2,1,4,2]

def writeTiming(T,tTimes,timingFile):
    twriter = csv.writer(timingFile,delimiter=',')
    for i in range(len(tTimes)):
        twriter.writerow([tTimes[i]])

def makesequencestart(sequence,numTrials):
    print 'Writing sequence trials'
    ResponseRq = []
    stimulus = []
#    x = random.randint(0,11)
    x = 0
    seq_pos = x + 1
    i = 0
    while i <numTrials:
        if x == len(sequence)-1:
            x = 0
        else:
            x = x + 1
        ResponseRq.append(sequence[x])
        i = i + 1
    for i in range(len(ResponseRq)):
        if ResponseRq[i] == 1:
            stimulus.append('X 0 0 0')
        elif ResponseRq[i] == 2:
            stimulus.append('0 X 0 0')
        elif ResponseRq[i] == 3:
            stimulus.append('0 0 X 0')
        else:
            stimulus.append('0 0 0 X')
    with open('TrialOrder.csv', 'wb') as csvfile:
        csvfile.truncate()
        spamwriter = csv.writer(csvfile, delimiter=',')
        spamwriter.writerow(['Stimulus','ResponseRq'])
        for i in range(len(ResponseRq)):
            spamwriter.writerow([stimulus[i],ResponseRq[i]])

def makerandom(numTrials):
    print 'Writing random trials'
    vector = []
    count = 0
    Respvec = []
    other = []
    while len(vector) < numTrials:
        x = random.randint(1,4)
        while count < 2 :
            vector.append(x)
            count = count + 1
#            print count
        if x != vector[-1]:
            vector.append(x)
            count = count + 1
        elif x == vector[-1]: 
            while x != vector[-2]:
                vector.append(x)
                count = count + 1
#            print count
    for i in range(len(vector)):
        if vector[i] == 1:
            Respvec.append('X 0 0 0')
        elif vector[i] == 2:
            Respvec.append('0 X 0 0')
        elif vector[i] == 3:
            Respvec.append('0 0 X 0')
        else:
            Respvec.append('0 0 0 X')
    with open('TrialOrder.csv', 'wb') as csvfile:
        csvfile.truncate()
        spamwriter = csv.writer(csvfile, delimiter=',')
        spamwriter.writerow(['Stimulus','ResponseRq'])
        for i in range(len(vector)):
            spamwriter.writerow([Respvec[i],vector[i]])

def GenBlockTrials(blockType,seq,numTrials):
    if blockType in ['S','PS']:
        makesequencestart(sequence,numTrials)
    else:
        makerandom(numTrials)

def genJitTime():
    potTimes = [0.05, 0.05, 0.05, 0.075, 0.075,0.075,0.1, 0.125, 0.125, 0.125]
    return random.choice(potTimes)

Instructions = visual.TextStim(win=win, ori=0, name='Instructions',
    text='Respond to the cue as fast and accurately as possible.\nDo not try to anticipate the cue.\nAnticipatory responses are not counted.\n\nDuring periods of time, you may think that the cue is following a fixed sequence.\nDo not try to explicitly learn the sequence.\n\nPress space to move on.',    font='Arial',
    pos=[0, 0], height=1, wrapWidth=None,
    color='white', colorSpace='rgb', opacity=1,
    depth=-1.0)

# Initialize components for Routine "InitialPause"
InitialPauseClock = core.Clock()

WhiteCross = visual.TextStim(win=win, ori=0, name='WhiteCross',
    text='+',    font='Arial',
    pos=[0, 0], height=1.5, wrapWidth=None,
    color='white', colorSpace='rgb', opacity=1,
    depth=-1.0)
text = visual.TextStim(win=win, ori=0, name='text',
    text='default text',    font='Arial',
    pos=[0, 0], height=2, wrapWidth=None,
    color='white', colorSpace='rgb', opacity=1,
    depth=-2.0)

# Initialize components for Routine "trial"
trialClock = core.Clock()

FBFrame_Trial = visual.Rect(win=win, name='FBFrame_Trial',
    width=[14, 4][0], height=[14, 4][1],
    ori=0, pos=[0, 0],
    lineWidth=4, lineColor=[1,1,1], lineColorSpace='rgb',
    fillColor=[0,0,0], fillColorSpace='rgb',
    opacity=1,depth=-1.0, 
interpolate=True)
po1 = visual.Polygon(win=win, name='po1',
    edges = 90, size=[0.5,0.5],
    ori=0, pos=[-4.5, 0],
    lineWidth=1, lineColor=[1,1,1], lineColorSpace='rgb',
    fillColor=[1,1,1], fillColorSpace='rgb',
    opacity=1,depth=-3.0, 
interpolate=True)
po2 = visual.Polygon(win=win, name='po2',
    edges = 90, size=[0.5,0.5],
    ori=0, pos=[-1.5, 0],
    lineWidth=1, lineColor=[1,1,1], lineColorSpace='rgb',
    fillColor=[1,1,1], fillColorSpace='rgb',
    opacity=1,depth=-4.0, 
interpolate=True)
po3 = visual.Polygon(win=win, name='po3',
    edges = 90, size=[0.5, 0.5],
    ori=0, pos=[1.5, 0],
    lineWidth=1, lineColor=[1,1,1], lineColorSpace='rgb',
    fillColor=[1,1,1], fillColorSpace='rgb',
    opacity=1,depth=-5.0, 
interpolate=True)
po4 = visual.Polygon(win=win, name='po4',
    edges = 90, size=[0.5, 0.5],
    ori=0, pos=[4.5, 0],
    lineWidth=1, lineColor=[1,1,1], lineColorSpace='rgb',
    fillColor=[1,1,1], fillColorSpace='rgb',
    opacity=1,depth=-6.0, 
interpolate=True)
stim = visual.Polygon(win=win, name='stim',
    edges = 90, size=[2, 2],
    ori=0, pos=[0,0],
    lineWidth=1, lineColor=[1,1,1], lineColorSpace='rgb',
    fillColor=[1,1,1], fillColorSpace='rgb',
    opacity=1,depth=-7.0, 
interpolate=True)

# Initialize components for Routine "writeTime"
writeTimeClock = core.Clock()


# Initialize components for Routine "End"
EndClock = core.Clock()

Thanks = visual.TextStim(win=win, ori=0, name='Thanks',
    text='Thanks for participating.\n\nPress space to exit.',    font='Arial',
    pos=[0, 0], height=1, wrapWidth=None,
    color='white', colorSpace='rgb', opacity=1,
    depth=-1.0)

# Create some handy timers
globalClock = core.Clock()  # to track the time since experiment started
routineTimer = core.CountdownTimer()  # to track time remaining of each (non-slip) routine 

#------Prepare to start Routine "Inst"-------
t = 0
InstClock.reset()  # clock 
frameN = -1
# update component parameters for each repeat

MoveOn = event.BuilderKeyResponse()  # create an object of type KeyResponse
MoveOn.status = NOT_STARTED
# keep track of which components have finished
InstComponents = []
InstComponents.append(Instructions)
InstComponents.append(MoveOn)
for thisComponent in InstComponents:
    if hasattr(thisComponent, 'status'):
        thisComponent.status = NOT_STARTED

#-------Start Routine "Inst"-------
continueRoutine = True
while continueRoutine:
    # get current time
    t = InstClock.getTime()
    frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
    # update/draw components on each frame
    
    
    # *Instructions* updates
    if t >= 0.0 and Instructions.status == NOT_STARTED:
        # keep track of start time/frame for later
        Instructions.tStart = t  # underestimates by a little under one frame
        Instructions.frameNStart = frameN  # exact frame index
        Instructions.setAutoDraw(True)
    
    # *MoveOn* updates
    if t >= 0.0 and MoveOn.status == NOT_STARTED:
        # keep track of start time/frame for later
        MoveOn.tStart = t  # underestimates by a little under one frame
        MoveOn.frameNStart = frameN  # exact frame index
        MoveOn.status = STARTED
        # keyboard checking is just starting
    if MoveOn.status == STARTED:
        theseKeys = event.getKeys(keyList=['space'])
        
        # check for quit:
        if "escape" in theseKeys:
            endExpNow = True
        if len(theseKeys) > 0:  # at least one key was pressed
            # a response ends the routine
            continueRoutine = False
    
    # check if all components have finished
    if not continueRoutine:  # a component has requested a forced-end of Routine
        break
    continueRoutine = False  # will revert to True if at least one component still running
    for thisComponent in InstComponents:
        if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
            continueRoutine = True
            break  # at least one component has not yet finished
    
    # check for quit (the Esc key)
    if endExpNow or event.getKeys(keyList=["escape"]):
        core.quit()
    
    # refresh the screen
    if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
        win.flip()

#-------Ending Routine "Inst"-------
for thisComponent in InstComponents:
    if hasattr(thisComponent, "setAutoDraw"):
        thisComponent.setAutoDraw(False)

T = time()
# the Routine "Inst" was not non-slip safe, so reset the non-slip timer
routineTimer.reset()

# set up handler to look after randomisation of conditions etc
Blocks = data.TrialHandler(nReps=1, method='sequential', 
    extraInfo=expInfo, originPath=-1,
    trialList=data.importConditions('explicitVariableSRT.xlsx'),
    seed=None, name='Blocks')
thisExp.addLoop(Blocks)  # add the loop to the experiment
thisBlock = Blocks.trialList[0]  # so we can initialise stimuli with some values
# abbreviate parameter names if possible (e.g. rgb=thisBlock.rgb)
if thisBlock != None:
    for paramName in thisBlock.keys():
        exec(paramName + '= thisBlock.' + paramName)

for thisBlock in Blocks:
    currentLoop = Blocks
    # abbreviate parameter names if possible (e.g. rgb = thisBlock.rgb)
    if thisBlock != None:
        for paramName in thisBlock.keys():
            exec(paramName + '= thisBlock.' + paramName)
    
    #------Prepare to start Routine "InitialPause"-------
    t = 0
    InitialPauseClock.reset()  # clock 
    frameN = -1
    routineTimer.add(8.000000)
    # update component parameters for each repeat
    
    text.setText(BlockType)
    # keep track of which components have finished
    InitialPauseComponents = []
    InitialPauseComponents.append(WhiteCross)
    InitialPauseComponents.append(text)
    for thisComponent in InitialPauseComponents:
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
    
    #-------Start Routine "InitialPause"-------
    continueRoutine = True
    while continueRoutine and routineTimer.getTime() > 0:
        # get current time
        t = InitialPauseClock.getTime()
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        
        
        # *WhiteCross* updates
        if t >= 0.0 and WhiteCross.status == NOT_STARTED:
            # keep track of start time/frame for later
            WhiteCross.tStart = t  # underestimates by a little under one frame
            WhiteCross.frameNStart = frameN  # exact frame index
            WhiteCross.setAutoDraw(True)
        if WhiteCross.status == STARTED and t >= (0.0 + (8-win.monitorFramePeriod*0.75)): #most of one frame period left
            WhiteCross.setAutoDraw(False)
        
        # *text* updates
        if t >= 0.0 and text.status == NOT_STARTED:
            # keep track of start time/frame for later
            text.tStart = t  # underestimates by a little under one frame
            text.frameNStart = frameN  # exact frame index
            text.setAutoDraw(True)
        if text.status == STARTED and t >= (0.0 + (1.0-win.monitorFramePeriod*0.75)): #most of one frame period left
            text.setAutoDraw(False)
        
        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in InitialPauseComponents:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # check for quit (the Esc key)
        if endExpNow or event.getKeys(keyList=["escape"]):
            core.quit()
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    #-------Ending Routine "InitialPause"-------
    for thisComponent in InitialPauseComponents:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    tTimes = []
    GenBlockTrials(BlockType,sequence,numTrials)
    
    # set up handler to look after randomisation of conditions etc
    trials = data.TrialHandler(nReps=1, method='sequential', 
        extraInfo=expInfo, originPath=-1,
        trialList=data.importConditions('TrialOrder.csv'),
        seed=None, name='trials')
    thisExp.addLoop(trials)  # add the loop to the experiment
    thisTrial = trials.trialList[0]  # so we can initialise stimuli with some values
    # abbreviate parameter names if possible (e.g. rgb=thisTrial.rgb)
    if thisTrial != None:
        for paramName in thisTrial.keys():
            exec(paramName + '= thisTrial.' + paramName)
    
    for thisTrial in trials:
        currentLoop = trials
        # abbreviate parameter names if possible (e.g. rgb = thisTrial.rgb)
        if thisTrial != None:
            for paramName in thisTrial.keys():
                exec(paramName + '= thisTrial.' + paramName)
        
        #------Prepare to start Routine "trial"-------
        t = 0
        trialClock.reset()  # clock 
        frameN = -1
        # update component parameters for each repeat
        jitTime = genJitTime()
        #print 'Jitter time = ' + str(jitTime)
        if ResponseRq == 1:
            stimPos = -4.5
        elif ResponseRq == 2:
            stimPos = -1.5
        elif ResponseRq == 3:
            stimPos = 1.5
        else:
            stimPos = 4.5
        
        
        
        curT = time()
        tTime =  curT-T
        tTimes.append(tTime)
        
        #writeTiming(t,jitTime,timingFile)
        Resp = event.BuilderKeyResponse()  # create an object of type KeyResponse
        Resp.status = NOT_STARTED
        stim.setPos([stimPos,0])
        # keep track of which components have finished
        trialComponents = []
        trialComponents.append(FBFrame_Trial)
        trialComponents.append(Resp)
        trialComponents.append(po1)
        trialComponents.append(po2)
        trialComponents.append(po3)
        trialComponents.append(po4)
        trialComponents.append(stim)
        for thisComponent in trialComponents:
            if hasattr(thisComponent, 'status'):
                thisComponent.status = NOT_STARTED
        
        #-------Start Routine "trial"-------
        continueRoutine = True
        while continueRoutine:
            # get current time
            t = trialClock.getTime()
            frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
            # update/draw components on each frame
            
            
            # *FBFrame_Trial* updates
            if t >= 0.0 and FBFrame_Trial.status == NOT_STARTED:
                # keep track of start time/frame for later
                FBFrame_Trial.tStart = t  # underestimates by a little under one frame
                FBFrame_Trial.frameNStart = frameN  # exact frame index
                FBFrame_Trial.setAutoDraw(True)
            if FBFrame_Trial.status == STARTED and t >= (trialLen-win.monitorFramePeriod*0.75): #most of one frame period left
                FBFrame_Trial.setAutoDraw(False)
            
            # *Resp* updates
            if t >= jitTime and Resp.status == NOT_STARTED:
                # keep track of start time/frame for later
                Resp.tStart = t  # underestimates by a little under one frame
                Resp.frameNStart = frameN  # exact frame index
                Resp.status = STARTED
                # keyboard checking is just starting
                win.callOnFlip(Resp.clock.reset)  # t=0 on next screen flip
                event.clearEvents(eventType='keyboard')
            if Resp.status == STARTED and t >= (trialLen-win.monitorFramePeriod*0.75): #most of one frame period left
                Resp.status = STOPPED
            if Resp.status == STARTED:
                theseKeys = event.getKeys(keyList=['1', '2', '3', '4'])
                
                # check for quit:
                if "escape" in theseKeys:
                    endExpNow = True
                if len(theseKeys) > 0:  # at least one key was pressed
                    if Resp.keys == []:  # then this was the first keypress
                        Resp.keys = theseKeys[0]  # just the first key pressed
                        Resp.rt = Resp.clock.getTime()
                        # was this 'correct'?
                        if (Resp.keys == str(ResponseRq)) or (Resp.keys == ResponseRq):
                            Resp.corr = 1
                        else:
                            Resp.corr = 0
            
            # *po1* updates
            if t >= 0.0 and po1.status == NOT_STARTED:
                # keep track of start time/frame for later
                po1.tStart = t  # underestimates by a little under one frame
                po1.frameNStart = frameN  # exact frame index
                po1.setAutoDraw(True)
            if po1.status == STARTED and t >= (0.0 + (1.0-win.monitorFramePeriod*0.75)): #most of one frame period left
                po1.setAutoDraw(False)
            
            # *po2* updates
            if t >= 0.0 and po2.status == NOT_STARTED:
                # keep track of start time/frame for later
                po2.tStart = t  # underestimates by a little under one frame
                po2.frameNStart = frameN  # exact frame index
                po2.setAutoDraw(True)
            if po2.status == STARTED and t >= (0.0 + (1.0-win.monitorFramePeriod*0.75)): #most of one frame period left
                po2.setAutoDraw(False)
            
            # *po3* updates
            if t >= 0.0 and po3.status == NOT_STARTED:
                # keep track of start time/frame for later
                po3.tStart = t  # underestimates by a little under one frame
                po3.frameNStart = frameN  # exact frame index
                po3.setAutoDraw(True)
            if po3.status == STARTED and t >= (0.0 + (1.0-win.monitorFramePeriod*0.75)): #most of one frame period left
                po3.setAutoDraw(False)
            
            # *po4* updates
            if t >= 0.0 and po4.status == NOT_STARTED:
                # keep track of start time/frame for later
                po4.tStart = t  # underestimates by a little under one frame
                po4.frameNStart = frameN  # exact frame index
                po4.setAutoDraw(True)
            if po4.status == STARTED and t >= (0.0 + (1.0-win.monitorFramePeriod*0.75)): #most of one frame period left
                po4.setAutoDraw(False)
            
            # *stim* updates
            if t >= jitTime and stim.status == NOT_STARTED:
                # keep track of start time/frame for later
                stim.tStart = t  # underestimates by a little under one frame
                stim.frameNStart = frameN  # exact frame index
                stim.setAutoDraw(True)
            if stim.status == STARTED and t >= (jitTime+stimLen-win.monitorFramePeriod*0.75): #most of one frame period left
                stim.setAutoDraw(False)
            
            # check if all components have finished
            if not continueRoutine:  # a component has requested a forced-end of Routine
                break
            continueRoutine = False  # will revert to True if at least one component still running
            for thisComponent in trialComponents:
                if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                    continueRoutine = True
                    break  # at least one component has not yet finished
            
            # check for quit (the Esc key)
            if endExpNow or event.getKeys(keyList=["escape"]):
                core.quit()
            
            # refresh the screen
            if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                win.flip()
        
        #-------Ending Routine "trial"-------
        for thisComponent in trialComponents:
            if hasattr(thisComponent, "setAutoDraw"):
                thisComponent.setAutoDraw(False)
        
        # check responses
        if Resp.keys in ['', [], None]:  # No response was made
           Resp.keys=None
           # was no response the correct answer?!
           if str(ResponseRq).lower() == 'none': Resp.corr = 1  # correct non-response
           else: Resp.corr = 0  # failed to respond (incorrectly)
        # store data for trials (TrialHandler)
        trials.addData('Resp.keys',Resp.keys)
        trials.addData('Resp.corr', Resp.corr)
        if Resp.keys != None:  # we had a response
            trials.addData('Resp.rt', Resp.rt)
        # the Routine "trial" was not non-slip safe, so reset the non-slip timer
        routineTimer.reset()
        thisExp.nextEntry()
        
    # completed 1 repeats of 'trials'
    
    
    #------Prepare to start Routine "writeTime"-------
    t = 0
    writeTimeClock.reset()  # clock 
    frameN = -1
    # update component parameters for each repeat
    writeTiming(t,tTimes,timingFile)
    # keep track of which components have finished
    writeTimeComponents = []
    for thisComponent in writeTimeComponents:
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
    
    #-------Start Routine "writeTime"-------
    continueRoutine = True
    while continueRoutine:
        # get current time
        t = writeTimeClock.getTime()
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        
        
        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in writeTimeComponents:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # check for quit (the Esc key)
        if endExpNow or event.getKeys(keyList=["escape"]):
            core.quit()
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    #-------Ending Routine "writeTime"-------
    for thisComponent in writeTimeComponents:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    
    # the Routine "writeTime" was not non-slip safe, so reset the non-slip timer
    routineTimer.reset()
# completed 1 repeats of 'Blocks'


#------Prepare to start Routine "End"-------
t = 0
EndClock.reset()  # clock 
frameN = -1
# update component parameters for each repeat
E_filename = 'data/TrialbyTrialEarning_%s.txt' %(expInfo['1 participant'])
E_trial_file = open(E_filename,'w')
write_E = csv.writer(E_trial_file)
write_E.writerow(Earning_Trial)

earning_filename = 'data/earning_subj_%s.txt'%(expInfo['1 participant'])
earning = open(earning_filename,'w')
earning.write(e_string)
exitRoutine = event.BuilderKeyResponse()  # create an object of type KeyResponse
exitRoutine.status = NOT_STARTED
# keep track of which components have finished
EndComponents = []
EndComponents.append(Thanks)
EndComponents.append(exitRoutine)
for thisComponent in EndComponents:
    if hasattr(thisComponent, 'status'):
        thisComponent.status = NOT_STARTED

#-------Start Routine "End"-------
continueRoutine = True
while continueRoutine:
    # get current time
    t = EndClock.getTime()
    frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
    # update/draw components on each frame
    
    
    # *Thanks* updates
    if t >= 0.0 and Thanks.status == NOT_STARTED:
        # keep track of start time/frame for later
        Thanks.tStart = t  # underestimates by a little under one frame
        Thanks.frameNStart = frameN  # exact frame index
        Thanks.setAutoDraw(True)
    
    # *exitRoutine* updates
    if t >= 0.0 and exitRoutine.status == NOT_STARTED:
        # keep track of start time/frame for later
        exitRoutine.tStart = t  # underestimates by a little under one frame
        exitRoutine.frameNStart = frameN  # exact frame index
        exitRoutine.status = STARTED
        # keyboard checking is just starting
        event.clearEvents(eventType='keyboard')
    if exitRoutine.status == STARTED:
        theseKeys = event.getKeys(keyList=['space'])
        
        # check for quit:
        if "escape" in theseKeys:
            endExpNow = True
        if len(theseKeys) > 0:  # at least one key was pressed
            # a response ends the routine
            continueRoutine = False
    
    # check if all components have finished
    if not continueRoutine:  # a component has requested a forced-end of Routine
        break
    continueRoutine = False  # will revert to True if at least one component still running
    for thisComponent in EndComponents:
        if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
            continueRoutine = True
            break  # at least one component has not yet finished
    
    # check for quit (the Esc key)
    if endExpNow or event.getKeys(keyList=["escape"]):
        core.quit()
    
    # refresh the screen
    if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
        win.flip()

#-------Ending Routine "End"-------
for thisComponent in EndComponents:
    if hasattr(thisComponent, "setAutoDraw"):
        thisComponent.setAutoDraw(False)

# the Routine "End" was not non-slip safe, so reset the non-slip timer
routineTimer.reset()





win.close()
core.quit()
