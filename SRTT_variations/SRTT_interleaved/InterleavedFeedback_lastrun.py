#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
This experiment was created using PsychoPy2 Experiment Builder (v1.83.01), Tue Feb  7 16:00:22 2017
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
expName = 'InterleavedFeedback'  # from the Builder filename that created this script
expInfo = {u'6 Gender (M/F)': u'', u'2 cond': u'', u'1 participant': u'', u'4 numTrials': u'48', u'3 seq': u'', u'5 Age': u'', u'7 Music experience (1-7)': u''}
dlg = gui.DlgFromDict(dictionary=expInfo, title=expName)
if dlg.OK == False: core.quit()  # user pressed cancel
expInfo['date'] = data.getDateStr()  # add a simple timestamp
expInfo['expName'] = expName

# Data file name stem = absolute path + name; later add .psyexp, .csv, .log, etc
filename = _thisDir + os.sep + u'data/%s_%s_%s_%s' %(expInfo['1 participant'],expInfo['2 cond'], expName, expInfo['date'])

# An ExperimentHandler isn't essential but helps with data saving
thisExp = data.ExperimentHandler(name=expName, version='',
    extraInfo=expInfo, runtimeInfo=None,
    originPath=u'/Users/steelad/Desktop/tasks.Applications/Interleaved/InterleavedFeedback.psyexp',
    savePickle=True, saveWideText=True,
    dataFileName=filename)
#save a log file for detail verbose info
logFile = logging.LogFile(filename+'.log', level=logging.EXP)
logging.console.setLevel(logging.WARNING)  # this outputs to the screen, not a file

endExpNow = False  # flag for 'escape' or other condition => quit the exp

# Start Code - component code to be run before the window creation

# Setup the Window
win = visual.Window(size=(1920, 1200), fullscr=True, screen=0, allowGUI=False, allowStencil=False,
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

import random
import os
import csv
from numpy import median

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

print str(type(numTrials))
if cond == 'Rew':
    earning = 0
else:
    earning = 20

if seq == '1':
    sequence = [2,4,2,1,3,4,1,2,3,1,4,3] #sequence 1
    print ('The sequence is sequence 1')
    #seq_order_file = 'Seq_Order_1.csv'
elif seq == '2':
    sequence = [3,4,3,1,2,4,1,3,2,1,4,2] #sequence 2
    print ('The sequence is sequence 2')
    #seq_order_file = 'Seq_Order_2.csv'
elif seq == '3':
    sequence = [3,4,2,3,1,2,1,4,3,2,4,1] # sequence 3
    print ('The sequence is sequence 3')
    #seq_order_file = 'Seq_Order_3.csv'
else:
    sequence = [3,4,1,2,4,3,1,4,2,1,3,2] # sequence 4
    print ('The sequence is sequence 4')
    #seq_order_file = 'Seq_Order_4.csv'

def Calc_Block_Criterion(BlockRTs,crit):
    Blockmedian = median(BlockRTs)
    Blocksd = std(BlockRTs)
    test_crit = Blockmedian + Blocksd
    print('Criteria = ' + str(crit))
    print('Test criteria = ' + str(test_crit))
    print(BlockRTs)
    if test_crit < crit:
        crit = test_crit
    else:
        crit = crit
    return (crit)

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
        while count < 1 :
            vector.append(x)
            count = count + 1
#            print count
        while x != vector[-1]:
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
BlackCross = visual.TextStim(win=win, ori=0, name='BlackCross',
    text='+',    font='Arial',
    pos=[0, 0], height=1.5, wrapWidth=None,
    color='black', colorSpace='rgb', opacity=1,
    depth=-2.0)

# Initialize components for Routine "trial"
trialClock = core.Clock()
FBFrame_Trial = visual.Rect(win=win, name='FBFrame_Trial',
    width=[8, 2][0], height=[8, 2][1],
    ori=0, pos=[0, 0],
    lineWidth=4, lineColor=[1,1,1], lineColorSpace='rgb',
    fillColor=[0,0,0], fillColorSpace='rgb',
    opacity=1,depth=0.0, 
interpolate=True)
Stim = visual.TextStim(win=win, ori=0, name='Stim',
    text='default text',    font='Courier',
    pos=[0, 0], height=1.5, wrapWidth=None,
    color='white', colorSpace='rgb', opacity=1,
    depth=-1.0)

# Initialize components for Routine "Feedback"
FeedbackClock = core.Clock()

FBFrame = visual.Rect(win=win, name='FBFrame',
    width=[8,2][0], height=[8,2][1],
    ori=0, pos=[0, 0],
    lineWidth=4, lineColor=1.0, lineColorSpace='rgb',
    fillColor=[0,0,0], fillColorSpace='rgb',
    opacity=1,depth=-1.0, 
interpolate=True)
StimWait = visual.TextStim(win=win, ori=0, name='StimWait',
    text='0 0 0 0',    font='Courier',
    pos=[0, 0], height=1.5, wrapWidth=None,
    color='white', colorSpace='rgb', opacity=1,
    depth=-2.0)

# Initialize components for Routine "Break"
BreakClock = core.Clock()

BreakPhrase = visual.TextStim(win=win, ori=0, name='BreakPhrase',
    text='default text',    font='Arial',
    pos=[0, 0], height=1, wrapWidth=None,
    color='white', colorSpace='rgb', opacity=1,
    depth=-1.0)

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

# the Routine "Inst" was not non-slip safe, so reset the non-slip timer
routineTimer.reset()

# set up handler to look after randomisation of conditions etc
Blocks = data.TrialHandler(nReps=1, method='sequential', 
    extraInfo=expInfo, originPath=-1,
    trialList=data.importConditions('InterleavedBlockOrder.xlsx'),
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
    routineTimer.add(2.000000)
    # update component parameters for each repeat
    
    # keep track of which components have finished
    InitialPauseComponents = []
    InitialPauseComponents.append(WhiteCross)
    InitialPauseComponents.append(BlackCross)
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
        if WhiteCross.status == STARTED and t >= (0.0 + (1-win.monitorFramePeriod*0.75)): #most of one frame period left
            WhiteCross.setAutoDraw(False)
        
        # *BlackCross* updates
        if t >= 1 and BlackCross.status == NOT_STARTED:
            # keep track of start time/frame for later
            BlackCross.tStart = t  # underestimates by a little under one frame
            BlackCross.frameNStart = frameN  # exact frame index
            BlackCross.setAutoDraw(True)
        if BlackCross.status == STARTED and t >= (1 + (1-win.monitorFramePeriod*0.75)): #most of one frame period left
            BlackCross.setAutoDraw(False)
        
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
        Stim.setText(Stimulus)
        Resp = event.BuilderKeyResponse()  # create an object of type KeyResponse
        Resp.status = NOT_STARTED
        # keep track of which components have finished
        trialComponents = []
        trialComponents.append(FBFrame_Trial)
        trialComponents.append(Stim)
        trialComponents.append(Resp)
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
            
            # *Stim* updates
            if t >= 0.0 and Stim.status == NOT_STARTED:
                # keep track of start time/frame for later
                Stim.tStart = t  # underestimates by a little under one frame
                Stim.frameNStart = frameN  # exact frame index
                Stim.setAutoDraw(True)
            
            # *Resp* updates
            if t >= 0 and Resp.status == NOT_STARTED:
                # keep track of start time/frame for later
                Resp.tStart = t  # underestimates by a little under one frame
                Resp.frameNStart = frameN  # exact frame index
                Resp.status = STARTED
                # keyboard checking is just starting
                win.callOnFlip(Resp.clock.reset)  # t=0 on next screen flip
                event.clearEvents(eventType='keyboard')
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
                        # a response ends the routine
                        continueRoutine = False
            
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
        
        #------Prepare to start Routine "Feedback"-------
        t = 0
        FeedbackClock.reset()  # clock 
        frameN = -1
        routineTimer.add(0.200000)
        # update component parameters for each repeat
        if Resp.corr:
            BlockRTs[TT] = (Resp.rt)
            TT = TT + 1
        
        if BlockType in ['R','S']:
            if cond == 'Rew':
                if Resp.corr and Resp.rt < crit:
                    color = [0,1,0]
                    Earning_Trial.append(1)
                    earning = earning + 0.02
                    e_string = str(earning)
                else:
                    color = [1,1,1]
                    Earning_Trial.append(0)
            elif cond == 'Pun':
                if Resp.corr == 0 or Resp.rt > crit:
                    color = [1,0,0]
                    Earning_Trial.append(1)
                    earning = earning - 0.02
                    e_string = str(earning)
                else:
                    color = [1,1,1]
                    Earning_Trial.append(0)
            elif cond == 'ContRew':
                x = random.random()
                if x < 0.5:
                    color = [0,1,0]
                else:
                    color = [1,1,1]
                    
                    e_string = str('You have earned money.')
            else:
                x = random.random()
                if x < 0.5:
                    color = [1,0,0]
                else:
                    color = [1,1,1]
                e_string = str('You have earned money.')
        else:
            Earning_Trial.append(0)
            color = [1,1,1]
        
        
        
        
        FBFrame.setLineColor(color)
        # keep track of which components have finished
        FeedbackComponents = []
        FeedbackComponents.append(FBFrame)
        FeedbackComponents.append(StimWait)
        for thisComponent in FeedbackComponents:
            if hasattr(thisComponent, 'status'):
                thisComponent.status = NOT_STARTED
        
        #-------Start Routine "Feedback"-------
        continueRoutine = True
        while continueRoutine and routineTimer.getTime() > 0:
            # get current time
            t = FeedbackClock.getTime()
            frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
            # update/draw components on each frame
            
            
            # *FBFrame* updates
            if t >= 0.0 and FBFrame.status == NOT_STARTED:
                # keep track of start time/frame for later
                FBFrame.tStart = t  # underestimates by a little under one frame
                FBFrame.frameNStart = frameN  # exact frame index
                FBFrame.setAutoDraw(True)
            if FBFrame.status == STARTED and t >= (0.0 + (0.2-win.monitorFramePeriod*0.75)): #most of one frame period left
                FBFrame.setAutoDraw(False)
            
            # *StimWait* updates
            if t >= 0.0 and StimWait.status == NOT_STARTED:
                # keep track of start time/frame for later
                StimWait.tStart = t  # underestimates by a little under one frame
                StimWait.frameNStart = frameN  # exact frame index
                StimWait.setAutoDraw(True)
            if StimWait.status == STARTED and t >= (0.2-win.monitorFramePeriod*0.75): #most of one frame period left
                StimWait.setAutoDraw(False)
            
            # check if all components have finished
            if not continueRoutine:  # a component has requested a forced-end of Routine
                break
            continueRoutine = False  # will revert to True if at least one component still running
            for thisComponent in FeedbackComponents:
                if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                    continueRoutine = True
                    break  # at least one component has not yet finished
            
            # check for quit (the Esc key)
            if endExpNow or event.getKeys(keyList=["escape"]):
                core.quit()
            
            # refresh the screen
            if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                win.flip()
        
        #-------Ending Routine "Feedback"-------
        for thisComponent in FeedbackComponents:
            if hasattr(thisComponent, "setAutoDraw"):
                thisComponent.setAutoDraw(False)
        
        thisExp.nextEntry()
        
    # completed 1 repeats of 'trials'
    
    
    #------Prepare to start Routine "Break"-------
    t = 0
    BreakClock.reset()  # clock 
    frameN = -1
    # update component parameters for each repeat
    BlockRTs = BlockRTs[1:TT]
    crit = Calc_Block_Criterion(BlockRTs,crit)
    BlockRTs = [0]*numTrials
    BlockNum = BlockNum + 1
    TT = 0
    
    if BlockNum <= 2:
        breakPhrase = 'Nice job.\nPress space to move on'
    elif BlockNum  == 3:
        breakPhrase = 'Stop. \n\nNice job.\n\nYou will now earn money based on your speed and accuracy.\n\nPress space to move on'
    elif BlockNum > 3 and BlockNum < 20:
        if cond == 'Rew' or cond == 'Pun':
            breakPhrase =  str("Nice job.  Take a breather. \n \nYou have earned $%s" % (e_string))
        else:
            breakPhrase = str("Nice job.  Take a breather.\n\nYou have earned money.")
    elif BlockNum == 20:
        breakPhrase = 'Stop\n\nYou have now completed the earning phase of the experiment.\n\nPlease continue to respond as fast\nand accurately as possible.\n\nPress space to move on.'
    else:
        breakPhrase = 'Nice job.\n\nPress space to move on'
    
    
    BreakPhrase.setText(breakPhrase)
    breakEnd = event.BuilderKeyResponse()  # create an object of type KeyResponse
    breakEnd.status = NOT_STARTED
    # keep track of which components have finished
    BreakComponents = []
    BreakComponents.append(BreakPhrase)
    BreakComponents.append(breakEnd)
    for thisComponent in BreakComponents:
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
    
    #-------Start Routine "Break"-------
    continueRoutine = True
    while continueRoutine:
        # get current time
        t = BreakClock.getTime()
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        
        
        # *BreakPhrase* updates
        if t >= 0.0 and BreakPhrase.status == NOT_STARTED:
            # keep track of start time/frame for later
            BreakPhrase.tStart = t  # underestimates by a little under one frame
            BreakPhrase.frameNStart = frameN  # exact frame index
            BreakPhrase.setAutoDraw(True)
        
        # *breakEnd* updates
        if t >= 2 and breakEnd.status == NOT_STARTED:
            # keep track of start time/frame for later
            breakEnd.tStart = t  # underestimates by a little under one frame
            breakEnd.frameNStart = frameN  # exact frame index
            breakEnd.status = STARTED
            # keyboard checking is just starting
            event.clearEvents(eventType='keyboard')
        if breakEnd.status == STARTED:
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
        for thisComponent in BreakComponents:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # check for quit (the Esc key)
        if endExpNow or event.getKeys(keyList=["escape"]):
            core.quit()
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    #-------Ending Routine "Break"-------
    for thisComponent in BreakComponents:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    
    # the Routine "Break" was not non-slip safe, so reset the non-slip timer
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
