#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
This experiment was created using PsychoPy2 Experiment Builder (v1.81.03), Sun Jan 25 17:12:35 2015
If you publish work using this script please cite the relevant PsychoPy publications
  Peirce, JW (2007) PsychoPy - Psychophysics software in Python. Journal of Neuroscience Methods, 162(1-2), 8-13.
  Peirce, JW (2009) Generating stimuli for neuroscience using PsychoPy. Frontiers in Neuroinformatics, 2:10. doi: 10.3389/neuro.11.010.2008
"""

from __future__ import division  # so that 1/3=0.333 instead of 1/3=0
from psychopy import visual, core, data, event, logging, sound, gui
from psychopy.constants import *  # things like STARTED, FINISHED
import numpy as np  # whole numpy lib is available, prepend 'np.'
from numpy import sin, cos, tan, log, log10, pi, average, sqrt, std, deg2rad, rad2deg, linspace, asarray
from numpy.random import random, randint, normal, shuffle
import os  # handy system and path functions

# Ensure that relative paths start from the same directory as this script
_thisDir = os.path.dirname(os.path.abspath(__file__))
os.chdir(_thisDir)

# Store info about the experiment session
expName = 'Adam_SRTT_ContPun_grouped'  # from the Builder filename that created this script
expInfo = {u'session': u'001', u'participant': u'', u'seq': u''}
dlg = gui.DlgFromDict(dictionary=expInfo, title=expName)
if dlg.OK == False: core.quit()  # user pressed cancel
expInfo['date'] = data.getDateStr()  # add a simple timestamp
expInfo['expName'] = expName

# Data file name stem = absolute path + name; later add .psyexp, .csv, .log, etc
filename = _thisDir + os.sep + 'data/%s_%s_%s' %(expInfo['participant'], expName, expInfo['date'])

# An ExperimentHandler isn't essential but helps with data saving
thisExp = data.ExperimentHandler(name=expName, version='',
    extraInfo=expInfo, runtimeInfo=None,
    originPath=u'/Users/steelad/Desktop/Subj_fMRI_Grouped_timedRest_nocounter_framed/Adam_SRTT_Seq.ContPun_grouped.psyexp',
    savePickle=True, saveWideText=True,
    dataFileName=filename)
#save a log file for detail verbose info
logFile = logging.LogFile(filename+'.log', level=logging.EXP)
logging.console.setLevel(logging.WARNING)  # this outputs to the screen, not a file

endExpNow = False  # flag for 'escape' or other condition => quit the exp

# Start Code - component code to be run before the window creation

# Setup the Window
win = visual.Window(size=(1600, 1200), fullscr=True, screen=0, allowGUI=False, allowStencil=False,
    monitor='testMonitor', color=[0,0,0], colorSpace='rgb',
    blendMode='avg', useFBO=True,
    )
# store frame rate of monitor if we can measure it successfully
expInfo['frameRate']=win.getActualFrameRate()
if expInfo['frameRate']!=None:
    frameDur = 1.0/round(expInfo['frameRate'])
else:
    frameDur = 1.0/60.0 # couldn't get a reliable measure so guess

# Initialize components for Routine "Instr"
InstrClock = core.Clock()
Instruction = visual.TextStim(win=win, ori=0, name='Instruction',
    text="You will see four positions on the screen.\n\nWhen one changes to an 'X', press the corresponding button.\n\nRespond as fast and accurate as possible!\n\nPress space to move on!",    font='Arial',
    pos=[0, 0], height=0.1, wrapWidth=None,
    color=[1.000,1.000,1.000], colorSpace='rgb', opacity=1,
    depth=0.0)
vector = []
count = 0
Respvec = []
Keyvec = []
other = []
sequence_positions = []

if expInfo['seq'] == '1':
    sequence = [2,4,2,1,3,4,1,2,3,1,4,3] #sequence 1
    print ('The sequence is sequence 1')
    seq_order_file = 'Seq_Order_1.csv'
elif expInfo['seq'] == '2':
    sequence = [3,4,3,1,2,4,1,3,2,1,4,2] #sequence 2
    print ('The sequence is sequence 2')
    seq_order_file = 'Seq_Order_2.csv'
elif expInfo['seq'] == '3':
    sequence = [3,4,2,3,1,2,1,4,3,2,4,1] # sequence 3
    print ('The sequence is sequence 3')
    seq_order_file = 'Seq_Order_3.csv'
else:
    sequence = [3,4,1,2,4,3,1,4,2,1,3,2] # sequence 4
    print ('The sequence is sequence 4')
    seq_order_file = 'Seq_Order_4.csv'


import random
import os
import csv
part = expInfo['participant']

def get_FB_prop():
    feedback = []
    with open ('./EarningInfo/mean_block_feedback.txt','rb') as FBfile:
        spamreader = csv.reader(FBfile)
        for column in spamreader:
            FB_list = column
            float_FB_list = [ float(x) for x in FB_list ]
    return float_FB_list

def make_FB_list(float_FB_list):
    feedback = []
    fb = []
    for i in range(len(float_FB_list)):
        j = 0
        while j < 96:
            print j
            a = random.random()
            if a <= float_FB_list[i]:
                feedback.append(0)
            else:
                feedback.append(1)
            j = j+1
    with open('./EarningInfo/' + str(part)+'feedback_file.txt','w') as feedback_file:
        writer = csv.writer(feedback_file)
        for i in range(len(feedback)):
            writer.writerow([feedback[i]])
    for i in range(0,len(feedback),96):
        l = i+96
        block_list=feedback[i:l]
        fb.append(block_list)
    return fb

def gen_fb(Feedback,fb_block,trial):
    fb_for_trial = Feedback[fb_block][trial]
    if fb_for_trial == 1:
        color = [1,0,0]
    else:
        color =[1,1,1]
    return color

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

def makesequencestart(sequence):
    ResponseRq = []
    stimulus = []
    x = random.randint(0,11)
    seq_pos = x + 1
    i = 0
    while i <96:
        if x >= len(sequence) - 1:
            x = 0
        else:
            x = x + 1
        ResponseRq.append(sequence[x])
        sequence_positions.append(seq_pos)
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
    with open(seq_order_file, 'wb') as csvfile:
        csvfile.truncate()
        spamwriter = csv.writer(csvfile, delimiter=',')
        spamwriter.writerow(['Stimulus','ResponseRq'])
        for i in range(len(ResponseRq)):
            spamwriter.writerow([stimulus[i],ResponseRq[i]])

def makerandom():
    vector = []
    count = 0
    Respvec = []
    Keyvec = []
    other = []
    while len(vector) < 96:
        x = random.randint(1,4)
        while count < 1 :
            vector.append(x)
            count = count + 1
            #print count
        while x != vector[-1]:
                vector.append(x)
                count = count + 1
                #print count
    for i in range(len(vector)):
        if vector[i] == 1:
            Keyvec.append('v')
        elif vector[i] == 2:
            Keyvec.append('b')
        elif vector[i] == 3:
            Keyvec.append('n')
        else:
            Keyvec.append('m')
    for i in range(len(vector)):
        if vector[i] == 1:
            Respvec.append('X 0 0 0')
        elif vector[i] == 2:
            Respvec.append('0 X 0 0')
        elif vector[i] == 3:
            Respvec.append('0 0 X 0')
        else:
            Respvec.append('0 0 0 X')
    with open('RandOrder.csv', 'wb') as csvfile:
        csvfile.truncate()
        spamwriter = csv.writer(csvfile, delimiter=',')
        spamwriter.writerow(['RandomResp','StimGen','RandStim'])
        for i in range(len(vector)):
            spamwriter.writerow([vector[i],Keyvec[i],Respvec[i]])

# Initialize components for Routine "WaitforTrigger"
WaitforTriggerClock = core.Clock()
text_4 = visual.TextStim(win=win, ori=0, name='text_4',
    text='Waiting for trigger...',    font='Arial',
    pos=[0, 0], height=0.1, wrapWidth=None,
    color='white', colorSpace='rgb', opacity=1,
    depth=0.0)

# Initialize components for Routine "BeginRun"
BeginRunClock = core.Clock()
Plus = visual.TextStim(win=win, ori=0, name='Plus',
    text='+',    font='Courier',
    pos=[0, 0], height=0.1, wrapWidth=None,
    color='black', colorSpace='rgb', opacity=1,
    depth=0.0)
Plus_ready = visual.TextStim(win=win, ori=0, name='Plus_ready',
    text='+',    font='Courier',
    pos=[0, 0], height=0.1, wrapWidth=None,
    color='Blue', colorSpace='rgb', opacity=1,
    depth=-1.0)
Run = 0

# Initialize components for Routine "Rand_Block_Training"
Rand_Block_TrainingClock = core.Clock()
Training_Stim = visual.TextStim(win=win, ori=0, name='Training_Stim',
    text='default text',    font='Courier',
    pos=[0, 0], height=0.1, wrapWidth=None,
    color='white', colorSpace='rgb', opacity=1,
    depth=0.0)

# Initialize components for Routine "Rand_ISI_Training"
Rand_ISI_TrainingClock = core.Clock()
Training_ISI = visual.TextStim(win=win, ori=0, name='Training_ISI',
    text='0 0 0 0',    font='Courier',
    pos=[0, 0], height=0.1, wrapWidth=None,
    color='white', colorSpace='rgb', opacity=1,
    depth=0.0)
BlockRTs = []


# Initialize components for Routine "Rest_training"
Rest_trainingClock = core.Clock()

Training_Rest_Instr = visual.TextStim(win=win, ori=0, name='Training_Rest_Instr',
    text='Nice, take a rest\n\nYou will see a black cross.\n\nIt will turn blue before the trials begin.',    font='Arial',
    pos=[0, 0], height=0.1, wrapWidth=None,
    color='white', colorSpace='rgb', opacity=1,
    depth=-1.0)
training_plus = visual.TextStim(win=win, ori=0, name='training_plus',
    text='+',    font='Arial',
    pos=[0, 0], height=0.1, wrapWidth=None,
    color='black', colorSpace='rgb', opacity=1,
    depth=-2.0)
training_plus_prep = visual.TextStim(win=win, ori=0, name='training_plus_prep',
    text='+',    font='Arial',
    pos=[0, 0], height=0.1, wrapWidth=None,
    color='blue', colorSpace='rgb', opacity=1,
    depth=-3.0)

# Initialize components for Routine "FirstRest"
FirstRestClock = core.Clock()
from numpy import percentile
from numpy import std
FirstBreather = visual.TextStim(win=win, ori=0, name='FirstBreather',
    text='default text',    font='Arial',
    pos=[0, 0], height=0.1, wrapWidth=None,
    color='white', colorSpace='rgb', opacity=1,
    depth=-1.0)

# Initialize components for Routine "WaitforTrigger"
WaitforTriggerClock = core.Clock()
text_4 = visual.TextStim(win=win, ori=0, name='text_4',
    text='Waiting for trigger...',    font='Arial',
    pos=[0, 0], height=0.1, wrapWidth=None,
    color='white', colorSpace='rgb', opacity=1,
    depth=0.0)

# Initialize components for Routine "BeginRun"
BeginRunClock = core.Clock()
Plus = visual.TextStim(win=win, ori=0, name='Plus',
    text='+',    font='Courier',
    pos=[0, 0], height=0.1, wrapWidth=None,
    color='black', colorSpace='rgb', opacity=1,
    depth=0.0)
Plus_ready = visual.TextStim(win=win, ori=0, name='Plus_ready',
    text='+',    font='Courier',
    pos=[0, 0], height=0.1, wrapWidth=None,
    color='Blue', colorSpace='rgb', opacity=1,
    depth=-1.0)
Run = 0

# Initialize components for Routine "RandBlock"
RandBlockClock = core.Clock()

RandFB_trial = visual.Rect(win=win, name='RandFB_trial',
    width=[0.5,0.2][0], height=[0.5,0.2][1],
    ori=0, pos=[0, 0],
    lineWidth=4, lineColor=[1,1,1], lineColorSpace='rgb',
    fillColor=[0,0,0], fillColorSpace='rgb',
    opacity=1,interpolate=True)
Stimulus_rand = visual.TextStim(win=win, ori=0, name='Stimulus_rand',
    text='default text',    font='Courier',
    pos=[0, 0], height=0.1, wrapWidth=None,
    color='white', colorSpace='rgb', opacity=1,
    depth=-2.0)

# Initialize components for Routine "RandFeedback"
RandFeedbackClock = core.Clock()

FB_Rand = visual.Rect(win=win, name='FB_Rand',
    width=[.5,.2][0], height=[.5,.2][1],
    ori=0, pos=[0,0],
    lineWidth=4, lineColor=1.0, lineColorSpace='rgb',
    fillColor=1.0, fillColorSpace='rgb',
    opacity=1,interpolate=True)
ISI_rand = visual.TextStim(win=win, ori=0, name='ISI_rand',
    text='0 0 0 0',    font='Courier',
    pos=[0, 0], height=0.1, wrapWidth=None,
    color='white', colorSpace='rgb', opacity=1,
    depth=-2.0)

# Initialize components for Routine "Rest"
RestClock = core.Clock()
vector = []
other = []
count = 0
Respvec = []
Keyvec = []
import random
import os
import csv
from numpy import std
Breather = visual.TextStim(win=win, ori=0, name='Breather',
    text='default text',    font='Arial',
    pos=[0, 0], height=0.1, wrapWidth=None,
    color='white', colorSpace='rgb', opacity=1,
    depth=-1.0)
plus = visual.TextStim(win=win, ori=0, name='plus',
    text='+',    font='Courier',
    pos=[0, 0], height=0.1, wrapWidth=None,
    color='black', colorSpace='rgb', opacity=1,
    depth=-2.0)
readyPlus = visual.TextStim(win=win, ori=0, name='readyPlus',
    text='+',    font='Courier',
    pos=[0, 0], height=0.1, wrapWidth=None,
    color='blue', colorSpace='rgb', opacity=1,
    depth=-3.0)

# Initialize components for Routine "trial"
trialClock = core.Clock()
FB_Seq_trial = visual.Rect(win=win, name='FB_Seq_trial',
    width=[0.5,0.2][0], height=[0.5,0.2][1],
    ori=0, pos=[0, 0],
    lineWidth=4, lineColor=[1,1,1], lineColorSpace='rgb',
    fillColor=[0,0,0], fillColorSpace='rgb',
    opacity=1,interpolate=True)
Stimulus_appear = visual.TextStim(win=win, ori=0, name='Stimulus_appear',
    text='default text',    font='Courier',
    pos=[0, 0], height=0.1, wrapWidth=None,
    color='white', colorSpace='rgb', opacity=1,
    depth=-1.0)


# Initialize components for Routine "Feedback_ISI"
Feedback_ISIClock = core.Clock()
from numpy import median
FB_seq = visual.Rect(win=win, name='FB_seq',
    width=[0.5, 0.2][0], height=[0.5, 0.2][1],
    ori=0, pos=[0, 0],
    lineWidth=4, lineColor=1.0, lineColorSpace='rgb',
    fillColor=[0,0,0], fillColorSpace='rgb',
    opacity=1,interpolate=True)
ISI = visual.TextStim(win=win, ori=0, name='ISI',
    text='0 0 0 0',    font='Courier',
    pos=[0, 0], height=0.1, wrapWidth=None,
    color='white', colorSpace='rgb', opacity=1,
    depth=-2.0)

# Initialize components for Routine "Rest"
RestClock = core.Clock()
vector = []
other = []
count = 0
Respvec = []
Keyvec = []
import random
import os
import csv
from numpy import std
Breather = visual.TextStim(win=win, ori=0, name='Breather',
    text='default text',    font='Arial',
    pos=[0, 0], height=0.1, wrapWidth=None,
    color='white', colorSpace='rgb', opacity=1,
    depth=-1.0)
plus = visual.TextStim(win=win, ori=0, name='plus',
    text='+',    font='Courier',
    pos=[0, 0], height=0.1, wrapWidth=None,
    color='black', colorSpace='rgb', opacity=1,
    depth=-2.0)
readyPlus = visual.TextStim(win=win, ori=0, name='readyPlus',
    text='+',    font='Courier',
    pos=[0, 0], height=0.1, wrapWidth=None,
    color='blue', colorSpace='rgb', opacity=1,
    depth=-3.0)

# Initialize components for Routine "RandBlock"
RandBlockClock = core.Clock()

RandFB_trial = visual.Rect(win=win, name='RandFB_trial',
    width=[0.5,0.2][0], height=[0.5,0.2][1],
    ori=0, pos=[0, 0],
    lineWidth=4, lineColor=[1,1,1], lineColorSpace='rgb',
    fillColor=[0,0,0], fillColorSpace='rgb',
    opacity=1,interpolate=True)
Stimulus_rand = visual.TextStim(win=win, ori=0, name='Stimulus_rand',
    text='default text',    font='Courier',
    pos=[0, 0], height=0.1, wrapWidth=None,
    color='white', colorSpace='rgb', opacity=1,
    depth=-2.0)

# Initialize components for Routine "RandFeedback"
RandFeedbackClock = core.Clock()

FB_Rand = visual.Rect(win=win, name='FB_Rand',
    width=[.5,.2][0], height=[.5,.2][1],
    ori=0, pos=[0,0],
    lineWidth=4, lineColor=1.0, lineColorSpace='rgb',
    fillColor=1.0, fillColorSpace='rgb',
    opacity=1,interpolate=True)
ISI_rand = visual.TextStim(win=win, ori=0, name='ISI_rand',
    text='0 0 0 0',    font='Courier',
    pos=[0, 0], height=0.1, wrapWidth=None,
    color='white', colorSpace='rgb', opacity=1,
    depth=-2.0)

# Initialize components for Routine "Rest"
RestClock = core.Clock()
vector = []
other = []
count = 0
Respvec = []
Keyvec = []
import random
import os
import csv
from numpy import std
Breather = visual.TextStim(win=win, ori=0, name='Breather',
    text='default text',    font='Arial',
    pos=[0, 0], height=0.1, wrapWidth=None,
    color='white', colorSpace='rgb', opacity=1,
    depth=-1.0)
plus = visual.TextStim(win=win, ori=0, name='plus',
    text='+',    font='Courier',
    pos=[0, 0], height=0.1, wrapWidth=None,
    color='black', colorSpace='rgb', opacity=1,
    depth=-2.0)
readyPlus = visual.TextStim(win=win, ori=0, name='readyPlus',
    text='+',    font='Courier',
    pos=[0, 0], height=0.1, wrapWidth=None,
    color='blue', colorSpace='rgb', opacity=1,
    depth=-3.0)

# Initialize components for Routine "RunBreak"
RunBreakClock = core.Clock()

RunBreakText = visual.TextStim(win=win, ori=0, name='RunBreakText',
    text='default text',    font='Arial',
    pos=[0, 0], height=0.1, wrapWidth=None,
    color='white', colorSpace='rgb', opacity=1,
    depth=-1.0)
ExperimenterRole = visual.TextStim(win=win, ori=0, name='ExperimenterRole',
    text='Experimentor will press space to move on',    font='Arial',
    pos=[0, -1], height=0.1, wrapWidth=None,
    color='white', colorSpace='rgb', opacity=1,
    depth=-3.0)

# Initialize components for Routine "WaitforTrigger"
WaitforTriggerClock = core.Clock()
text_4 = visual.TextStim(win=win, ori=0, name='text_4',
    text='Waiting for trigger...',    font='Arial',
    pos=[0, 0], height=0.1, wrapWidth=None,
    color='white', colorSpace='rgb', opacity=1,
    depth=0.0)

# Initialize components for Routine "BeginRun"
BeginRunClock = core.Clock()
Plus = visual.TextStim(win=win, ori=0, name='Plus',
    text='+',    font='Courier',
    pos=[0, 0], height=0.1, wrapWidth=None,
    color='black', colorSpace='rgb', opacity=1,
    depth=0.0)
Plus_ready = visual.TextStim(win=win, ori=0, name='Plus_ready',
    text='+',    font='Courier',
    pos=[0, 0], height=0.1, wrapWidth=None,
    color='Blue', colorSpace='rgb', opacity=1,
    depth=-1.0)
Run = 0

# Initialize components for Routine "trial"
trialClock = core.Clock()
FB_Seq_trial = visual.Rect(win=win, name='FB_Seq_trial',
    width=[0.5,0.2][0], height=[0.5,0.2][1],
    ori=0, pos=[0, 0],
    lineWidth=4, lineColor=[1,1,1], lineColorSpace='rgb',
    fillColor=[0,0,0], fillColorSpace='rgb',
    opacity=1,interpolate=True)
Stimulus_appear = visual.TextStim(win=win, ori=0, name='Stimulus_appear',
    text='default text',    font='Courier',
    pos=[0, 0], height=0.1, wrapWidth=None,
    color='white', colorSpace='rgb', opacity=1,
    depth=-1.0)


# Initialize components for Routine "Feedback_ISI"
Feedback_ISIClock = core.Clock()
from numpy import median
FB_seq = visual.Rect(win=win, name='FB_seq',
    width=[0.5, 0.2][0], height=[0.5, 0.2][1],
    ori=0, pos=[0, 0],
    lineWidth=4, lineColor=1.0, lineColorSpace='rgb',
    fillColor=[0,0,0], fillColorSpace='rgb',
    opacity=1,interpolate=True)
ISI = visual.TextStim(win=win, ori=0, name='ISI',
    text='0 0 0 0',    font='Courier',
    pos=[0, 0], height=0.1, wrapWidth=None,
    color='white', colorSpace='rgb', opacity=1,
    depth=-2.0)

# Initialize components for Routine "Rest"
RestClock = core.Clock()
vector = []
other = []
count = 0
Respvec = []
Keyvec = []
import random
import os
import csv
from numpy import std
Breather = visual.TextStim(win=win, ori=0, name='Breather',
    text='default text',    font='Arial',
    pos=[0, 0], height=0.1, wrapWidth=None,
    color='white', colorSpace='rgb', opacity=1,
    depth=-1.0)
plus = visual.TextStim(win=win, ori=0, name='plus',
    text='+',    font='Courier',
    pos=[0, 0], height=0.1, wrapWidth=None,
    color='black', colorSpace='rgb', opacity=1,
    depth=-2.0)
readyPlus = visual.TextStim(win=win, ori=0, name='readyPlus',
    text='+',    font='Courier',
    pos=[0, 0], height=0.1, wrapWidth=None,
    color='blue', colorSpace='rgb', opacity=1,
    depth=-3.0)

# Initialize components for Routine "RunBreak"
RunBreakClock = core.Clock()

RunBreakText = visual.TextStim(win=win, ori=0, name='RunBreakText',
    text='default text',    font='Arial',
    pos=[0, 0], height=0.1, wrapWidth=None,
    color='white', colorSpace='rgb', opacity=1,
    depth=-1.0)
ExperimenterRole = visual.TextStim(win=win, ori=0, name='ExperimenterRole',
    text='Experimentor will press space to move on',    font='Arial',
    pos=[0, -1], height=0.1, wrapWidth=None,
    color='white', colorSpace='rgb', opacity=1,
    depth=-3.0)

# Initialize components for Routine "WaitforTrigger"
WaitforTriggerClock = core.Clock()
text_4 = visual.TextStim(win=win, ori=0, name='text_4',
    text='Waiting for trigger...',    font='Arial',
    pos=[0, 0], height=0.1, wrapWidth=None,
    color='white', colorSpace='rgb', opacity=1,
    depth=0.0)

# Initialize components for Routine "BeginRun"
BeginRunClock = core.Clock()
Plus = visual.TextStim(win=win, ori=0, name='Plus',
    text='+',    font='Courier',
    pos=[0, 0], height=0.1, wrapWidth=None,
    color='black', colorSpace='rgb', opacity=1,
    depth=0.0)
Plus_ready = visual.TextStim(win=win, ori=0, name='Plus_ready',
    text='+',    font='Courier',
    pos=[0, 0], height=0.1, wrapWidth=None,
    color='Blue', colorSpace='rgb', opacity=1,
    depth=-1.0)
Run = 0

# Initialize components for Routine "trial"
trialClock = core.Clock()
FB_Seq_trial = visual.Rect(win=win, name='FB_Seq_trial',
    width=[0.5,0.2][0], height=[0.5,0.2][1],
    ori=0, pos=[0, 0],
    lineWidth=4, lineColor=[1,1,1], lineColorSpace='rgb',
    fillColor=[0,0,0], fillColorSpace='rgb',
    opacity=1,interpolate=True)
Stimulus_appear = visual.TextStim(win=win, ori=0, name='Stimulus_appear',
    text='default text',    font='Courier',
    pos=[0, 0], height=0.1, wrapWidth=None,
    color='white', colorSpace='rgb', opacity=1,
    depth=-1.0)


# Initialize components for Routine "Feedback_ISI"
Feedback_ISIClock = core.Clock()
from numpy import median
FB_seq = visual.Rect(win=win, name='FB_seq',
    width=[0.5, 0.2][0], height=[0.5, 0.2][1],
    ori=0, pos=[0, 0],
    lineWidth=4, lineColor=1.0, lineColorSpace='rgb',
    fillColor=[0,0,0], fillColorSpace='rgb',
    opacity=1,interpolate=True)
ISI = visual.TextStim(win=win, ori=0, name='ISI',
    text='0 0 0 0',    font='Courier',
    pos=[0, 0], height=0.1, wrapWidth=None,
    color='white', colorSpace='rgb', opacity=1,
    depth=-2.0)

# Initialize components for Routine "Rest"
RestClock = core.Clock()
vector = []
other = []
count = 0
Respvec = []
Keyvec = []
import random
import os
import csv
from numpy import std
Breather = visual.TextStim(win=win, ori=0, name='Breather',
    text='default text',    font='Arial',
    pos=[0, 0], height=0.1, wrapWidth=None,
    color='white', colorSpace='rgb', opacity=1,
    depth=-1.0)
plus = visual.TextStim(win=win, ori=0, name='plus',
    text='+',    font='Courier',
    pos=[0, 0], height=0.1, wrapWidth=None,
    color='black', colorSpace='rgb', opacity=1,
    depth=-2.0)
readyPlus = visual.TextStim(win=win, ori=0, name='readyPlus',
    text='+',    font='Courier',
    pos=[0, 0], height=0.1, wrapWidth=None,
    color='blue', colorSpace='rgb', opacity=1,
    depth=-3.0)

# Initialize components for Routine "RunBreak"
RunBreakClock = core.Clock()

RunBreakText = visual.TextStim(win=win, ori=0, name='RunBreakText',
    text='default text',    font='Arial',
    pos=[0, 0], height=0.1, wrapWidth=None,
    color='white', colorSpace='rgb', opacity=1,
    depth=-1.0)
ExperimenterRole = visual.TextStim(win=win, ori=0, name='ExperimenterRole',
    text='Experimentor will press space to move on',    font='Arial',
    pos=[0, -1], height=0.1, wrapWidth=None,
    color='white', colorSpace='rgb', opacity=1,
    depth=-3.0)

# Initialize components for Routine "WaitforTrigger"
WaitforTriggerClock = core.Clock()
text_4 = visual.TextStim(win=win, ori=0, name='text_4',
    text='Waiting for trigger...',    font='Arial',
    pos=[0, 0], height=0.1, wrapWidth=None,
    color='white', colorSpace='rgb', opacity=1,
    depth=0.0)

# Initialize components for Routine "BeginRun"
BeginRunClock = core.Clock()
Plus = visual.TextStim(win=win, ori=0, name='Plus',
    text='+',    font='Courier',
    pos=[0, 0], height=0.1, wrapWidth=None,
    color='black', colorSpace='rgb', opacity=1,
    depth=0.0)
Plus_ready = visual.TextStim(win=win, ori=0, name='Plus_ready',
    text='+',    font='Courier',
    pos=[0, 0], height=0.1, wrapWidth=None,
    color='Blue', colorSpace='rgb', opacity=1,
    depth=-1.0)
Run = 0

# Initialize components for Routine "RandBlock"
RandBlockClock = core.Clock()

RandFB_trial = visual.Rect(win=win, name='RandFB_trial',
    width=[0.5,0.2][0], height=[0.5,0.2][1],
    ori=0, pos=[0, 0],
    lineWidth=4, lineColor=[1,1,1], lineColorSpace='rgb',
    fillColor=[0,0,0], fillColorSpace='rgb',
    opacity=1,interpolate=True)
Stimulus_rand = visual.TextStim(win=win, ori=0, name='Stimulus_rand',
    text='default text',    font='Courier',
    pos=[0, 0], height=0.1, wrapWidth=None,
    color='white', colorSpace='rgb', opacity=1,
    depth=-2.0)

# Initialize components for Routine "RandFeedback"
RandFeedbackClock = core.Clock()

FB_Rand = visual.Rect(win=win, name='FB_Rand',
    width=[.5,.2][0], height=[.5,.2][1],
    ori=0, pos=[0,0],
    lineWidth=4, lineColor=1.0, lineColorSpace='rgb',
    fillColor=1.0, fillColorSpace='rgb',
    opacity=1,interpolate=True)
ISI_rand = visual.TextStim(win=win, ori=0, name='ISI_rand',
    text='0 0 0 0',    font='Courier',
    pos=[0, 0], height=0.1, wrapWidth=None,
    color='white', colorSpace='rgb', opacity=1,
    depth=-2.0)

# Initialize components for Routine "Rest"
RestClock = core.Clock()
vector = []
other = []
count = 0
Respvec = []
Keyvec = []
import random
import os
import csv
from numpy import std
Breather = visual.TextStim(win=win, ori=0, name='Breather',
    text='default text',    font='Arial',
    pos=[0, 0], height=0.1, wrapWidth=None,
    color='white', colorSpace='rgb', opacity=1,
    depth=-1.0)
plus = visual.TextStim(win=win, ori=0, name='plus',
    text='+',    font='Courier',
    pos=[0, 0], height=0.1, wrapWidth=None,
    color='black', colorSpace='rgb', opacity=1,
    depth=-2.0)
readyPlus = visual.TextStim(win=win, ori=0, name='readyPlus',
    text='+',    font='Courier',
    pos=[0, 0], height=0.1, wrapWidth=None,
    color='blue', colorSpace='rgb', opacity=1,
    depth=-3.0)

# Initialize components for Routine "trial"
trialClock = core.Clock()
FB_Seq_trial = visual.Rect(win=win, name='FB_Seq_trial',
    width=[0.5,0.2][0], height=[0.5,0.2][1],
    ori=0, pos=[0, 0],
    lineWidth=4, lineColor=[1,1,1], lineColorSpace='rgb',
    fillColor=[0,0,0], fillColorSpace='rgb',
    opacity=1,interpolate=True)
Stimulus_appear = visual.TextStim(win=win, ori=0, name='Stimulus_appear',
    text='default text',    font='Courier',
    pos=[0, 0], height=0.1, wrapWidth=None,
    color='white', colorSpace='rgb', opacity=1,
    depth=-1.0)


# Initialize components for Routine "Feedback_ISI"
Feedback_ISIClock = core.Clock()
from numpy import median
FB_seq = visual.Rect(win=win, name='FB_seq',
    width=[0.5, 0.2][0], height=[0.5, 0.2][1],
    ori=0, pos=[0, 0],
    lineWidth=4, lineColor=1.0, lineColorSpace='rgb',
    fillColor=[0,0,0], fillColorSpace='rgb',
    opacity=1,interpolate=True)
ISI = visual.TextStim(win=win, ori=0, name='ISI',
    text='0 0 0 0',    font='Courier',
    pos=[0, 0], height=0.1, wrapWidth=None,
    color='white', colorSpace='rgb', opacity=1,
    depth=-2.0)

# Initialize components for Routine "Rest"
RestClock = core.Clock()
vector = []
other = []
count = 0
Respvec = []
Keyvec = []
import random
import os
import csv
from numpy import std
Breather = visual.TextStim(win=win, ori=0, name='Breather',
    text='default text',    font='Arial',
    pos=[0, 0], height=0.1, wrapWidth=None,
    color='white', colorSpace='rgb', opacity=1,
    depth=-1.0)
plus = visual.TextStim(win=win, ori=0, name='plus',
    text='+',    font='Courier',
    pos=[0, 0], height=0.1, wrapWidth=None,
    color='black', colorSpace='rgb', opacity=1,
    depth=-2.0)
readyPlus = visual.TextStim(win=win, ori=0, name='readyPlus',
    text='+',    font='Courier',
    pos=[0, 0], height=0.1, wrapWidth=None,
    color='blue', colorSpace='rgb', opacity=1,
    depth=-3.0)

# Initialize components for Routine "RandBlock"
RandBlockClock = core.Clock()

RandFB_trial = visual.Rect(win=win, name='RandFB_trial',
    width=[0.5,0.2][0], height=[0.5,0.2][1],
    ori=0, pos=[0, 0],
    lineWidth=4, lineColor=[1,1,1], lineColorSpace='rgb',
    fillColor=[0,0,0], fillColorSpace='rgb',
    opacity=1,interpolate=True)
Stimulus_rand = visual.TextStim(win=win, ori=0, name='Stimulus_rand',
    text='default text',    font='Courier',
    pos=[0, 0], height=0.1, wrapWidth=None,
    color='white', colorSpace='rgb', opacity=1,
    depth=-2.0)

# Initialize components for Routine "RandFeedback"
RandFeedbackClock = core.Clock()

FB_Rand = visual.Rect(win=win, name='FB_Rand',
    width=[.5,.2][0], height=[.5,.2][1],
    ori=0, pos=[0,0],
    lineWidth=4, lineColor=1.0, lineColorSpace='rgb',
    fillColor=1.0, fillColorSpace='rgb',
    opacity=1,interpolate=True)
ISI_rand = visual.TextStim(win=win, ori=0, name='ISI_rand',
    text='0 0 0 0',    font='Courier',
    pos=[0, 0], height=0.1, wrapWidth=None,
    color='white', colorSpace='rgb', opacity=1,
    depth=-2.0)

# Initialize components for Routine "Rest"
RestClock = core.Clock()
vector = []
other = []
count = 0
Respvec = []
Keyvec = []
import random
import os
import csv
from numpy import std
Breather = visual.TextStim(win=win, ori=0, name='Breather',
    text='default text',    font='Arial',
    pos=[0, 0], height=0.1, wrapWidth=None,
    color='white', colorSpace='rgb', opacity=1,
    depth=-1.0)
plus = visual.TextStim(win=win, ori=0, name='plus',
    text='+',    font='Courier',
    pos=[0, 0], height=0.1, wrapWidth=None,
    color='black', colorSpace='rgb', opacity=1,
    depth=-2.0)
readyPlus = visual.TextStim(win=win, ori=0, name='readyPlus',
    text='+',    font='Courier',
    pos=[0, 0], height=0.1, wrapWidth=None,
    color='blue', colorSpace='rgb', opacity=1,
    depth=-3.0)

# Initialize components for Routine "end"
endClock = core.Clock()

Thanks = visual.TextStim(win=win, ori=0, name='Thanks',
    text='default text',    font='Arial',
    pos=[0, 0], height=0.1, wrapWidth=None,
    color='white', colorSpace='rgb', opacity=1,
    depth=-1.0)

# Create some handy timers
globalClock = core.Clock()  # to track the time since experiment started
routineTimer = core.CountdownTimer()  # to track time remaining of each (non-slip) routine 

#------Prepare to start Routine "Instr"-------
t = 0
InstrClock.reset()  # clock 
frameN = -1
# update component parameters for each repeat
MoveOn = event.BuilderKeyResponse()  # create an object of type KeyResponse
MoveOn.status = NOT_STARTED
makerandom()
makesequencestart(sequence)
float_FB_list = get_FB_prop()
Feedback = make_FB_list(float_FB_list)
# keep track of which components have finished
InstrComponents = []
InstrComponents.append(Instruction)
InstrComponents.append(MoveOn)
for thisComponent in InstrComponents:
    if hasattr(thisComponent, 'status'):
        thisComponent.status = NOT_STARTED

#-------Start Routine "Instr"-------
continueRoutine = True
while continueRoutine:
    # get current time
    t = InstrClock.getTime()
    frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
    # update/draw components on each frame
    
    # *Instruction* updates
    if t >= 0.0 and Instruction.status == NOT_STARTED:
        # keep track of start time/frame for later
        Instruction.tStart = t  # underestimates by a little under one frame
        Instruction.frameNStart = frameN  # exact frame index
        Instruction.setAutoDraw(True)
    
    # *MoveOn* updates
    if t >= 1 and MoveOn.status == NOT_STARTED:
        # keep track of start time/frame for later
        MoveOn.tStart = t  # underestimates by a little under one frame
        MoveOn.frameNStart = frameN  # exact frame index
        MoveOn.status = STARTED
        # keyboard checking is just starting
        event.clearEvents(eventType='keyboard')
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
        routineTimer.reset()  # if we abort early the non-slip timer needs reset
        break
    continueRoutine = False  # will revert to True if at least one component still running
    for thisComponent in InstrComponents:
        if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
            continueRoutine = True
            break  # at least one component has not yet finished
    
    # check for quit (the Esc key)
    if endExpNow or event.getKeys(keyList=["escape"]):
        core.quit()
    
    # refresh the screen
    if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
        win.flip()
    else:  # this Routine was not non-slip safe so reset non-slip timer
        routineTimer.reset()

#-------Ending Routine "Instr"-------
for thisComponent in InstrComponents:
    if hasattr(thisComponent, "setAutoDraw"):
        thisComponent.setAutoDraw(False)


#------Prepare to start Routine "WaitforTrigger"-------
t = 0
WaitforTriggerClock.reset()  # clock 
frameN = -1
# update component parameters for each repeat
TriggerIn = event.BuilderKeyResponse()  # create an object of type KeyResponse
TriggerIn.status = NOT_STARTED
# keep track of which components have finished
WaitforTriggerComponents = []
WaitforTriggerComponents.append(text_4)
WaitforTriggerComponents.append(TriggerIn)
for thisComponent in WaitforTriggerComponents:
    if hasattr(thisComponent, 'status'):
        thisComponent.status = NOT_STARTED

#-------Start Routine "WaitforTrigger"-------
continueRoutine = True
while continueRoutine:
    # get current time
    t = WaitforTriggerClock.getTime()
    frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
    # update/draw components on each frame
    
    # *text_4* updates
    if t >= 0.0 and text_4.status == NOT_STARTED:
        # keep track of start time/frame for later
        text_4.tStart = t  # underestimates by a little under one frame
        text_4.frameNStart = frameN  # exact frame index
        text_4.setAutoDraw(True)
    
    # *TriggerIn* updates
    if t >= 0.0 and TriggerIn.status == NOT_STARTED:
        # keep track of start time/frame for later
        TriggerIn.tStart = t  # underestimates by a little under one frame
        TriggerIn.frameNStart = frameN  # exact frame index
        TriggerIn.status = STARTED
        # keyboard checking is just starting
        event.clearEvents(eventType='keyboard')
    if TriggerIn.status == STARTED:
        theseKeys = event.getKeys(keyList=['5'])
        
        # check for quit:
        if "escape" in theseKeys:
            endExpNow = True
        if len(theseKeys) > 0:  # at least one key was pressed
            # a response ends the routine
            continueRoutine = False
    
    # check if all components have finished
    if not continueRoutine:  # a component has requested a forced-end of Routine
        routineTimer.reset()  # if we abort early the non-slip timer needs reset
        break
    continueRoutine = False  # will revert to True if at least one component still running
    for thisComponent in WaitforTriggerComponents:
        if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
            continueRoutine = True
            break  # at least one component has not yet finished
    
    # check for quit (the Esc key)
    if endExpNow or event.getKeys(keyList=["escape"]):
        core.quit()
    
    # refresh the screen
    if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
        win.flip()
    else:  # this Routine was not non-slip safe so reset non-slip timer
        routineTimer.reset()

#-------Ending Routine "WaitforTrigger"-------
for thisComponent in WaitforTriggerComponents:
    if hasattr(thisComponent, "setAutoDraw"):
        thisComponent.setAutoDraw(False)

#------Prepare to start Routine "BeginRun"-------
t = 0
BeginRunClock.reset()  # clock 
frameN = -1
routineTimer.add(12.000000)
# update component parameters for each repeat

# keep track of which components have finished
BeginRunComponents = []
BeginRunComponents.append(Plus)
BeginRunComponents.append(Plus_ready)
for thisComponent in BeginRunComponents:
    if hasattr(thisComponent, 'status'):
        thisComponent.status = NOT_STARTED

#-------Start Routine "BeginRun"-------
continueRoutine = True
while continueRoutine and routineTimer.getTime() > 0:
    # get current time
    t = BeginRunClock.getTime()
    frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
    # update/draw components on each frame
    
    # *Plus* updates
    if t >= 0.0 and Plus.status == NOT_STARTED:
        # keep track of start time/frame for later
        Plus.tStart = t  # underestimates by a little under one frame
        Plus.frameNStart = frameN  # exact frame index
        Plus.setAutoDraw(True)
    if Plus.status == STARTED and t >= (7-win.monitorFramePeriod*0.75): #most of one frame period left
        Plus.setAutoDraw(False)
    
    # *Plus_ready* updates
    if t >= 7 and Plus_ready.status == NOT_STARTED:
        # keep track of start time/frame for later
        Plus_ready.tStart = t  # underestimates by a little under one frame
        Plus_ready.frameNStart = frameN  # exact frame index
        Plus_ready.setAutoDraw(True)
    if Plus_ready.status == STARTED and t >= (12-win.monitorFramePeriod*0.75): #most of one frame period left
        Plus_ready.setAutoDraw(False)
    
    
    # check if all components have finished
    if not continueRoutine:  # a component has requested a forced-end of Routine
        routineTimer.reset()  # if we abort early the non-slip timer needs reset
        break
    continueRoutine = False  # will revert to True if at least one component still running
    for thisComponent in BeginRunComponents:
        if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
            continueRoutine = True
            break  # at least one component has not yet finished
    
    # check for quit (the Esc key)
    if endExpNow or event.getKeys(keyList=["escape"]):
        core.quit()
    
    # refresh the screen
    if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
        win.flip()

#-------Ending Routine "BeginRun"-------
for thisComponent in BeginRunComponents:
    if hasattr(thisComponent, "setAutoDraw"):
        thisComponent.setAutoDraw(False)
Run = Run + 1

# set up handler to look after randomisation of conditions etc
Training_Blocks = data.TrialHandler(nReps=3, method='sequential', 
    extraInfo=expInfo, originPath=u'/Users/steelad/Desktop/Subj_fMRI_Grouped_timedRest_nocounter_framed/Adam_SRTT_Seq.ContPun_grouped.psyexp',
    trialList=[None],
    seed=None, name='Training_Blocks')
thisExp.addLoop(Training_Blocks)  # add the loop to the experiment
thisTraining_Block = Training_Blocks.trialList[0]  # so we can initialise stimuli with some values
# abbreviate parameter names if possible (e.g. rgb=thisTraining_Block.rgb)
if thisTraining_Block != None:
    for paramName in thisTraining_Block.keys():
        exec(paramName + '= thisTraining_Block.' + paramName)

for thisTraining_Block in Training_Blocks:
    currentLoop = Training_Blocks
    # abbreviate parameter names if possible (e.g. rgb = thisTraining_Block.rgb)
    if thisTraining_Block != None:
        for paramName in thisTraining_Block.keys():
            exec(paramName + '= thisTraining_Block.' + paramName)
    
    # set up handler to look after randomisation of conditions etc
    TrainingLoop = data.TrialHandler(nReps=1, method='sequential', 
        extraInfo=expInfo, originPath=u'/Users/steelad/Desktop/Subj_fMRI_Grouped_timedRest_nocounter_framed/Adam_SRTT_Seq.ContPun_grouped.psyexp',
        trialList=data.importConditions('RandOrder.csv'),
        seed=None, name='TrainingLoop')
    thisExp.addLoop(TrainingLoop)  # add the loop to the experiment
    thisTrainingLoop = TrainingLoop.trialList[0]  # so we can initialise stimuli with some values
    # abbreviate parameter names if possible (e.g. rgb=thisTrainingLoop.rgb)
    if thisTrainingLoop != None:
        for paramName in thisTrainingLoop.keys():
            exec(paramName + '= thisTrainingLoop.' + paramName)
    
    for thisTrainingLoop in TrainingLoop:
        currentLoop = TrainingLoop
        # abbreviate parameter names if possible (e.g. rgb = thisTrainingLoop.rgb)
        if thisTrainingLoop != None:
            for paramName in thisTrainingLoop.keys():
                exec(paramName + '= thisTrainingLoop.' + paramName)
        
        #------Prepare to start Routine "Rand_Block_Training"-------
        t = 0
        Rand_Block_TrainingClock.reset()  # clock 
        frameN = -1
        routineTimer.add(0.800000)
        # update component parameters for each repeat
        Training_Stim.setText(RandStim)
        Response_Training = event.BuilderKeyResponse()  # create an object of type KeyResponse
        Response_Training.status = NOT_STARTED
        # keep track of which components have finished
        Rand_Block_TrainingComponents = []
        Rand_Block_TrainingComponents.append(Training_Stim)
        Rand_Block_TrainingComponents.append(Response_Training)
        for thisComponent in Rand_Block_TrainingComponents:
            if hasattr(thisComponent, 'status'):
                thisComponent.status = NOT_STARTED
        
        #-------Start Routine "Rand_Block_Training"-------
        continueRoutine = True
        while continueRoutine and routineTimer.getTime() > 0:
            # get current time
            t = Rand_Block_TrainingClock.getTime()
            frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
            # update/draw components on each frame
            
            # *Training_Stim* updates
            if t >= 0.0 and Training_Stim.status == NOT_STARTED:
                # keep track of start time/frame for later
                Training_Stim.tStart = t  # underestimates by a little under one frame
                Training_Stim.frameNStart = frameN  # exact frame index
                Training_Stim.setAutoDraw(True)
            if Training_Stim.status == STARTED and t >= (0.0 + (0.8-win.monitorFramePeriod*0.75)): #most of one frame period left
                Training_Stim.setAutoDraw(False)
            
            # *Response_Training* updates
            if t >= 0 and Response_Training.status == NOT_STARTED:
                # keep track of start time/frame for later
                Response_Training.tStart = t  # underestimates by a little under one frame
                Response_Training.frameNStart = frameN  # exact frame index
                Response_Training.status = STARTED
                # keyboard checking is just starting
                Response_Training.clock.reset()  # now t=0
                event.clearEvents(eventType='keyboard')
            if Response_Training.status == STARTED and t >= (0.8-win.monitorFramePeriod*0.75): #most of one frame period left
                Response_Training.status = STOPPED
            if Response_Training.status == STARTED:
                theseKeys = event.getKeys(keyList=['1', '2', '3', '4'])
                
                # check for quit:
                if "escape" in theseKeys:
                    endExpNow = True
                if len(theseKeys) > 0:  # at least one key was pressed
                    Response_Training.keys = theseKeys[-1]  # just the last key pressed
                    Response_Training.rt = Response_Training.clock.getTime()
                    # was this 'correct'?
                    if (Response_Training.keys == str(RandomResp)) or (Response_Training.keys == RandomResp):
                        Response_Training.corr = 1
                    else:
                        Response_Training.corr = 0
            
            # check if all components have finished
            if not continueRoutine:  # a component has requested a forced-end of Routine
                routineTimer.reset()  # if we abort early the non-slip timer needs reset
                break
            continueRoutine = False  # will revert to True if at least one component still running
            for thisComponent in Rand_Block_TrainingComponents:
                if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                    continueRoutine = True
                    break  # at least one component has not yet finished
            
            # check for quit (the Esc key)
            if endExpNow or event.getKeys(keyList=["escape"]):
                core.quit()
            
            # refresh the screen
            if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                win.flip()
        
        #-------Ending Routine "Rand_Block_Training"-------
        for thisComponent in Rand_Block_TrainingComponents:
            if hasattr(thisComponent, "setAutoDraw"):
                thisComponent.setAutoDraw(False)
        # check responses
        if Response_Training.keys in ['', [], None]:  # No response was made
           Response_Training.keys=None
           # was no response the correct answer?!
           if str(RandomResp).lower() == 'none': Response_Training.corr = 1  # correct non-response
           else: Response_Training.corr = 0  # failed to respond (incorrectly)
        # store data for TrainingLoop (TrialHandler)
        TrainingLoop.addData('Response_Training.keys',Response_Training.keys)
        TrainingLoop.addData('Response_Training.corr', Response_Training.corr)
        if Response_Training.keys != None:  # we had a response
            TrainingLoop.addData('Response_Training.rt', Response_Training.rt)
        
        #------Prepare to start Routine "Rand_ISI_Training"-------
        t = 0
        Rand_ISI_TrainingClock.reset()  # clock 
        frameN = -1
        routineTimer.add(0.200000)
        # update component parameters for each repeat
        if Response_Training.corr == True:
            BlockRTs.append(Response_Training.rt)
        # keep track of which components have finished
        Rand_ISI_TrainingComponents = []
        Rand_ISI_TrainingComponents.append(Training_ISI)
        for thisComponent in Rand_ISI_TrainingComponents:
            if hasattr(thisComponent, 'status'):
                thisComponent.status = NOT_STARTED
        
        #-------Start Routine "Rand_ISI_Training"-------
        continueRoutine = True
        while continueRoutine and routineTimer.getTime() > 0:
            # get current time
            t = Rand_ISI_TrainingClock.getTime()
            frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
            # update/draw components on each frame
            
            # *Training_ISI* updates
            if t >= 0.0 and Training_ISI.status == NOT_STARTED:
                # keep track of start time/frame for later
                Training_ISI.tStart = t  # underestimates by a little under one frame
                Training_ISI.frameNStart = frameN  # exact frame index
                Training_ISI.setAutoDraw(True)
            if Training_ISI.status == STARTED and t >= (0.0 + (0.2-win.monitorFramePeriod*0.75)): #most of one frame period left
                Training_ISI.setAutoDraw(False)
            
            
            # check if all components have finished
            if not continueRoutine:  # a component has requested a forced-end of Routine
                routineTimer.reset()  # if we abort early the non-slip timer needs reset
                break
            continueRoutine = False  # will revert to True if at least one component still running
            for thisComponent in Rand_ISI_TrainingComponents:
                if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                    continueRoutine = True
                    break  # at least one component has not yet finished
            
            # check for quit (the Esc key)
            if endExpNow or event.getKeys(keyList=["escape"]):
                core.quit()
            
            # refresh the screen
            if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                win.flip()
        
        #-------Ending Routine "Rand_ISI_Training"-------
        for thisComponent in Rand_ISI_TrainingComponents:
            if hasattr(thisComponent, "setAutoDraw"):
                thisComponent.setAutoDraw(False)
        
        thisExp.nextEntry()
        
    # completed 1 repeats of 'TrainingLoop'
    
    
    #------Prepare to start Routine "Rest_training"-------
    t = 0
    Rest_trainingClock.reset()  # clock 
    frameN = -1
    routineTimer.add(30.000000)
    # update component parameters for each repeat
    makerandom()
    # keep track of which components have finished
    Rest_trainingComponents = []
    Rest_trainingComponents.append(Training_Rest_Instr)
    Rest_trainingComponents.append(training_plus)
    Rest_trainingComponents.append(training_plus_prep)
    for thisComponent in Rest_trainingComponents:
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
    
    #-------Start Routine "Rest_training"-------
    continueRoutine = True
    while continueRoutine and routineTimer.getTime() > 0:
        # get current time
        t = Rest_trainingClock.getTime()
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        
        
        # *Training_Rest_Instr* updates
        if t >= 0.0 and Training_Rest_Instr.status == NOT_STARTED:
            # keep track of start time/frame for later
            Training_Rest_Instr.tStart = t  # underestimates by a little under one frame
            Training_Rest_Instr.frameNStart = frameN  # exact frame index
            Training_Rest_Instr.setAutoDraw(True)
        if Training_Rest_Instr.status == STARTED and t >= (0.0 + (5-win.monitorFramePeriod*0.75)): #most of one frame period left
            Training_Rest_Instr.setAutoDraw(False)
        
        # *training_plus* updates
        if t >= 5 and training_plus.status == NOT_STARTED:
            # keep track of start time/frame for later
            training_plus.tStart = t  # underestimates by a little under one frame
            training_plus.frameNStart = frameN  # exact frame index
            training_plus.setAutoDraw(True)
        if training_plus.status == STARTED and t >= (25-win.monitorFramePeriod*0.75): #most of one frame period left
            training_plus.setAutoDraw(False)
        
        # *training_plus_prep* updates
        if t >= 25 and training_plus_prep.status == NOT_STARTED:
            # keep track of start time/frame for later
            training_plus_prep.tStart = t  # underestimates by a little under one frame
            training_plus_prep.frameNStart = frameN  # exact frame index
            training_plus_prep.setAutoDraw(True)
        if training_plus_prep.status == STARTED and t >= (30-win.monitorFramePeriod*0.75): #most of one frame period left
            training_plus_prep.setAutoDraw(False)
        
        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            routineTimer.reset()  # if we abort early the non-slip timer needs reset
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in Rest_trainingComponents:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # check for quit (the Esc key)
        if endExpNow or event.getKeys(keyList=["escape"]):
            core.quit()
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    #-------Ending Routine "Rest_training"-------
    for thisComponent in Rest_trainingComponents:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    
    thisExp.nextEntry()
    
# completed 3 repeats of 'Training_Blocks'


# set up handler to look after randomisation of conditions etc
Run1 = data.TrialHandler(nReps=1, method='sequential', 
    extraInfo=expInfo, originPath=u'/Users/steelad/Desktop/Subj_fMRI_Grouped_timedRest_nocounter_framed/Adam_SRTT_Seq.ContPun_grouped.psyexp',
    trialList=[None],
    seed=None, name='Run1')
thisExp.addLoop(Run1)  # add the loop to the experiment
thisRun1 = Run1.trialList[0]  # so we can initialise stimuli with some values
# abbreviate parameter names if possible (e.g. rgb=thisRun1.rgb)
if thisRun1 != None:
    for paramName in thisRun1.keys():
        exec(paramName + '= thisRun1.' + paramName)

for thisRun1 in Run1:
    currentLoop = Run1
    # abbreviate parameter names if possible (e.g. rgb = thisRun1.rgb)
    if thisRun1 != None:
        for paramName in thisRun1.keys():
            exec(paramName + '= thisRun1.' + paramName)
    
    #------Prepare to start Routine "FirstRest"-------
    t = 0
    FirstRestClock.reset()  # clock 
    frameN = -1
    # update component parameters for each repeat
    earning = 0
    trial = 0
    Earning_Trial = []
    Blockmedian = median(BlockRTs)
    Blocksd = std(BlockRTs)
    print('Block median = ' + str(Blockmedian))
    print(len(BlockRTs))
    
    crit = Blockmedian+Blocksd
    block = 1
    fb_block = block - 1
    makerandom()
    makesequencestart(sequence)
    
    phrase = str('You will now complete a series of the trials.\n\nAs you continue, you will receive money based on your speed and accuracy. \nOn some trials, you will see a green square.  This is not related to your performance.s\n\nAgain, please respond as fast and accurately as possible.\n\nPress space to go on')
    FirstBreather.setText(phrase)
    Moveon1 = event.BuilderKeyResponse()  # create an object of type KeyResponse
    Moveon1.status = NOT_STARTED
    # keep track of which components have finished
    FirstRestComponents = []
    FirstRestComponents.append(FirstBreather)
    FirstRestComponents.append(Moveon1)
    for thisComponent in FirstRestComponents:
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
    
    #-------Start Routine "FirstRest"-------
    continueRoutine = True
    while continueRoutine:
        # get current time
        t = FirstRestClock.getTime()
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        
        
        
        # *FirstBreather* updates
        if t >= 0.0 and FirstBreather.status == NOT_STARTED:
            # keep track of start time/frame for later
            FirstBreather.tStart = t  # underestimates by a little under one frame
            FirstBreather.frameNStart = frameN  # exact frame index
            FirstBreather.setAutoDraw(True)
        
        # *Moveon1* updates
        if t >= 3 and Moveon1.status == NOT_STARTED:
            # keep track of start time/frame for later
            Moveon1.tStart = t  # underestimates by a little under one frame
            Moveon1.frameNStart = frameN  # exact frame index
            Moveon1.status = STARTED
            # keyboard checking is just starting
            event.clearEvents(eventType='keyboard')
        if Moveon1.status == STARTED:
            theseKeys = event.getKeys(keyList=['space'])
            
            # check for quit:
            if "escape" in theseKeys:
                endExpNow = True
            if len(theseKeys) > 0:  # at least one key was pressed
                # a response ends the routine
                continueRoutine = False
        
        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            routineTimer.reset()  # if we abort early the non-slip timer needs reset
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in FirstRestComponents:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # check for quit (the Esc key)
        if endExpNow or event.getKeys(keyList=["escape"]):
            core.quit()
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
        else:  # this Routine was not non-slip safe so reset non-slip timer
            routineTimer.reset()
    
    #-------Ending Routine "FirstRest"-------
    for thisComponent in FirstRestComponents:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    BlockRTs = []
    
    #------Prepare to start Routine "WaitforTrigger"-------
    t = 0
    WaitforTriggerClock.reset()  # clock 
    frameN = -1
    # update component parameters for each repeat
    TriggerIn = event.BuilderKeyResponse()  # create an object of type KeyResponse
    TriggerIn.status = NOT_STARTED
    # keep track of which components have finished
    WaitforTriggerComponents = []
    WaitforTriggerComponents.append(text_4)
    WaitforTriggerComponents.append(TriggerIn)
    for thisComponent in WaitforTriggerComponents:
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
    
    #-------Start Routine "WaitforTrigger"-------
    continueRoutine = True
    while continueRoutine:
        # get current time
        t = WaitforTriggerClock.getTime()
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        
        # *text_4* updates
        if t >= 0.0 and text_4.status == NOT_STARTED:
            # keep track of start time/frame for later
            text_4.tStart = t  # underestimates by a little under one frame
            text_4.frameNStart = frameN  # exact frame index
            text_4.setAutoDraw(True)
        
        # *TriggerIn* updates
        if t >= 0.0 and TriggerIn.status == NOT_STARTED:
            # keep track of start time/frame for later
            TriggerIn.tStart = t  # underestimates by a little under one frame
            TriggerIn.frameNStart = frameN  # exact frame index
            TriggerIn.status = STARTED
            # keyboard checking is just starting
            event.clearEvents(eventType='keyboard')
        if TriggerIn.status == STARTED:
            theseKeys = event.getKeys(keyList=['5'])
            
            # check for quit:
            if "escape" in theseKeys:
                endExpNow = True
            if len(theseKeys) > 0:  # at least one key was pressed
                # a response ends the routine
                continueRoutine = False
        
        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            routineTimer.reset()  # if we abort early the non-slip timer needs reset
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in WaitforTriggerComponents:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # check for quit (the Esc key)
        if endExpNow or event.getKeys(keyList=["escape"]):
            core.quit()
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
        else:  # this Routine was not non-slip safe so reset non-slip timer
            routineTimer.reset()
    
    #-------Ending Routine "WaitforTrigger"-------
    for thisComponent in WaitforTriggerComponents:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    
    #------Prepare to start Routine "BeginRun"-------
    t = 0
    BeginRunClock.reset()  # clock 
    frameN = -1
    routineTimer.add(12.000000)
    # update component parameters for each repeat
    
    # keep track of which components have finished
    BeginRunComponents = []
    BeginRunComponents.append(Plus)
    BeginRunComponents.append(Plus_ready)
    for thisComponent in BeginRunComponents:
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
    
    #-------Start Routine "BeginRun"-------
    continueRoutine = True
    while continueRoutine and routineTimer.getTime() > 0:
        # get current time
        t = BeginRunClock.getTime()
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        
        # *Plus* updates
        if t >= 0.0 and Plus.status == NOT_STARTED:
            # keep track of start time/frame for later
            Plus.tStart = t  # underestimates by a little under one frame
            Plus.frameNStart = frameN  # exact frame index
            Plus.setAutoDraw(True)
        if Plus.status == STARTED and t >= (7-win.monitorFramePeriod*0.75): #most of one frame period left
            Plus.setAutoDraw(False)
        
        # *Plus_ready* updates
        if t >= 7 and Plus_ready.status == NOT_STARTED:
            # keep track of start time/frame for later
            Plus_ready.tStart = t  # underestimates by a little under one frame
            Plus_ready.frameNStart = frameN  # exact frame index
            Plus_ready.setAutoDraw(True)
        if Plus_ready.status == STARTED and t >= (12-win.monitorFramePeriod*0.75): #most of one frame period left
            Plus_ready.setAutoDraw(False)
        
        
        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            routineTimer.reset()  # if we abort early the non-slip timer needs reset
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in BeginRunComponents:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # check for quit (the Esc key)
        if endExpNow or event.getKeys(keyList=["escape"]):
            core.quit()
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    #-------Ending Routine "BeginRun"-------
    for thisComponent in BeginRunComponents:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    Run = Run + 1
    
    # set up handler to look after randomisation of conditions etc
    Init_rand = data.TrialHandler(nReps=1, method='sequential', 
        extraInfo=expInfo, originPath=u'/Users/steelad/Desktop/Subj_fMRI_Grouped_timedRest_nocounter_framed/Adam_SRTT_Seq.ContPun_grouped.psyexp',
        trialList=data.importConditions('RandOrder.csv'),
        seed=None, name='Init_rand')
    thisExp.addLoop(Init_rand)  # add the loop to the experiment
    thisInit_rand = Init_rand.trialList[0]  # so we can initialise stimuli with some values
    # abbreviate parameter names if possible (e.g. rgb=thisInit_rand.rgb)
    if thisInit_rand != None:
        for paramName in thisInit_rand.keys():
            exec(paramName + '= thisInit_rand.' + paramName)
    
    for thisInit_rand in Init_rand:
        currentLoop = Init_rand
        # abbreviate parameter names if possible (e.g. rgb = thisInit_rand.rgb)
        if thisInit_rand != None:
            for paramName in thisInit_rand.keys():
                exec(paramName + '= thisInit_rand.' + paramName)
        
        #------Prepare to start Routine "RandBlock"-------
        t = 0
        RandBlockClock.reset()  # clock 
        frameN = -1
        routineTimer.add(0.800000)
        # update component parameters for each repeat
        
        Stimulus_rand.setText(RandStim)
        RandResp = event.BuilderKeyResponse()  # create an object of type KeyResponse
        RandResp.status = NOT_STARTED
        # keep track of which components have finished
        RandBlockComponents = []
        RandBlockComponents.append(RandFB_trial)
        RandBlockComponents.append(Stimulus_rand)
        RandBlockComponents.append(RandResp)
        for thisComponent in RandBlockComponents:
            if hasattr(thisComponent, 'status'):
                thisComponent.status = NOT_STARTED
        
        #-------Start Routine "RandBlock"-------
        continueRoutine = True
        while continueRoutine and routineTimer.getTime() > 0:
            # get current time
            t = RandBlockClock.getTime()
            frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
            # update/draw components on each frame
            
            
            # *RandFB_trial* updates
            if t >= 0.0 and RandFB_trial.status == NOT_STARTED:
                # keep track of start time/frame for later
                RandFB_trial.tStart = t  # underestimates by a little under one frame
                RandFB_trial.frameNStart = frameN  # exact frame index
                RandFB_trial.setAutoDraw(True)
            if RandFB_trial.status == STARTED and t >= (0.0 + (0.8-win.monitorFramePeriod*0.75)): #most of one frame period left
                RandFB_trial.setAutoDraw(False)
            
            # *Stimulus_rand* updates
            if t >= 0.0 and Stimulus_rand.status == NOT_STARTED:
                # keep track of start time/frame for later
                Stimulus_rand.tStart = t  # underestimates by a little under one frame
                Stimulus_rand.frameNStart = frameN  # exact frame index
                Stimulus_rand.setAutoDraw(True)
            if Stimulus_rand.status == STARTED and t >= (0.8-win.monitorFramePeriod*0.75): #most of one frame period left
                Stimulus_rand.setAutoDraw(False)
            
            # *RandResp* updates
            if t >= 0 and RandResp.status == NOT_STARTED:
                # keep track of start time/frame for later
                RandResp.tStart = t  # underestimates by a little under one frame
                RandResp.frameNStart = frameN  # exact frame index
                RandResp.status = STARTED
                # keyboard checking is just starting
                RandResp.clock.reset()  # now t=0
                event.clearEvents(eventType='keyboard')
            if RandResp.status == STARTED and t >= (0.8-win.monitorFramePeriod*0.75): #most of one frame period left
                RandResp.status = STOPPED
            if RandResp.status == STARTED:
                theseKeys = event.getKeys(keyList=['1', '2', '3', '4'])
                
                # check for quit:
                if "escape" in theseKeys:
                    endExpNow = True
                if len(theseKeys) > 0:  # at least one key was pressed
                    if RandResp.keys == []:  # then this was the first keypress
                        RandResp.keys = theseKeys[0]  # just the first key pressed
                        RandResp.rt = RandResp.clock.getTime()
                        # was this 'correct'?
                        if (RandResp.keys == str(RandomResp)) or (RandResp.keys == RandomResp):
                            RandResp.corr = 1
                        else:
                            RandResp.corr = 0
            
            # check if all components have finished
            if not continueRoutine:  # a component has requested a forced-end of Routine
                routineTimer.reset()  # if we abort early the non-slip timer needs reset
                break
            continueRoutine = False  # will revert to True if at least one component still running
            for thisComponent in RandBlockComponents:
                if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                    continueRoutine = True
                    break  # at least one component has not yet finished
            
            # check for quit (the Esc key)
            if endExpNow or event.getKeys(keyList=["escape"]):
                core.quit()
            
            # refresh the screen
            if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                win.flip()
        
        #-------Ending Routine "RandBlock"-------
        for thisComponent in RandBlockComponents:
            if hasattr(thisComponent, "setAutoDraw"):
                thisComponent.setAutoDraw(False)
        
        # check responses
        if RandResp.keys in ['', [], None]:  # No response was made
           RandResp.keys=None
           # was no response the correct answer?!
           if str(RandomResp).lower() == 'none': RandResp.corr = 1  # correct non-response
           else: RandResp.corr = 0  # failed to respond (incorrectly)
        # store data for Init_rand (TrialHandler)
        Init_rand.addData('RandResp.keys',RandResp.keys)
        Init_rand.addData('RandResp.corr', RandResp.corr)
        if RandResp.keys != None:  # we had a response
            Init_rand.addData('RandResp.rt', RandResp.rt)
        
        #------Prepare to start Routine "RandFeedback"-------
        t = 0
        RandFeedbackClock.reset()  # clock 
        frameN = -1
        routineTimer.add(0.200000)
        # update component parameters for each repeat
        if RandResp.corr:
            BlockRTs.append(RandResp.rt)
        Color = gen_fb(Feedback,fb_block,trial)
        if RandResp.corr and RandResp.rt < crit:
        #    Color = [0,1,0]
            Earning_Trial.append(1)
        #    earning = earning + 0.05
        #    e_string = str(earning)
        else:
        #    Color = [1,1,1]
            Earning_Trial.append(0)
        FB_Rand.setFillColor([0,0,0])
        FB_Rand.setLineColor(Color)
        # keep track of which components have finished
        RandFeedbackComponents = []
        RandFeedbackComponents.append(FB_Rand)
        RandFeedbackComponents.append(ISI_rand)
        for thisComponent in RandFeedbackComponents:
            if hasattr(thisComponent, 'status'):
                thisComponent.status = NOT_STARTED
        
        #-------Start Routine "RandFeedback"-------
        continueRoutine = True
        while continueRoutine and routineTimer.getTime() > 0:
            # get current time
            t = RandFeedbackClock.getTime()
            frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
            # update/draw components on each frame
            
            
            # *FB_Rand* updates
            if t >= 0.0 and FB_Rand.status == NOT_STARTED:
                # keep track of start time/frame for later
                FB_Rand.tStart = t  # underestimates by a little under one frame
                FB_Rand.frameNStart = frameN  # exact frame index
                FB_Rand.setAutoDraw(True)
            if FB_Rand.status == STARTED and t >= (0.0 + (0.2-win.monitorFramePeriod*0.75)): #most of one frame period left
                FB_Rand.setAutoDraw(False)
            
            # *ISI_rand* updates
            if t >= 0.0 and ISI_rand.status == NOT_STARTED:
                # keep track of start time/frame for later
                ISI_rand.tStart = t  # underestimates by a little under one frame
                ISI_rand.frameNStart = frameN  # exact frame index
                ISI_rand.setAutoDraw(True)
            if ISI_rand.status == STARTED and t >= (0.0 + (.2-win.monitorFramePeriod*0.75)): #most of one frame period left
                ISI_rand.setAutoDraw(False)
            
            # check if all components have finished
            if not continueRoutine:  # a component has requested a forced-end of Routine
                routineTimer.reset()  # if we abort early the non-slip timer needs reset
                break
            continueRoutine = False  # will revert to True if at least one component still running
            for thisComponent in RandFeedbackComponents:
                if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                    continueRoutine = True
                    break  # at least one component has not yet finished
            
            # check for quit (the Esc key)
            if endExpNow or event.getKeys(keyList=["escape"]):
                core.quit()
            
            # refresh the screen
            if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                win.flip()
        
        #-------Ending Routine "RandFeedback"-------
        for thisComponent in RandFeedbackComponents:
            if hasattr(thisComponent, "setAutoDraw"):
                thisComponent.setAutoDraw(False)
        trial = trial + 1
        thisExp.nextEntry()
        
    # completed 1 repeats of 'Init_rand'
    
    
    #------Prepare to start Routine "Rest"-------
    t = 0
    RestClock.reset()  # clock 
    frameN = -1
    routineTimer.add(30.000000)
    # update component parameters for each repeat
    vector = []
    count = 0
    Respvec = []
    other = []
    Keyvec = []
    trial = 0
    crit = Calc_Block_Criterion(BlockRTs,crit)
    
    makesequencestart(sequence)
    makerandom()
    
    breatherphrase = str("Good job, your earnings increased!\n\nYou finished block %s.  \n \nTake a breather. \n \n" % (block))
    block = block+1
    fb_block = block - 1
    Breather.setText(breatherphrase)
    # keep track of which components have finished
    RestComponents = []
    RestComponents.append(Breather)
    RestComponents.append(plus)
    RestComponents.append(readyPlus)
    for thisComponent in RestComponents:
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
    
    #-------Start Routine "Rest"-------
    continueRoutine = True
    while continueRoutine and routineTimer.getTime() > 0:
        # get current time
        t = RestClock.getTime()
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        
        
        # *Breather* updates
        if t >= 0.0 and Breather.status == NOT_STARTED:
            # keep track of start time/frame for later
            Breather.tStart = t  # underestimates by a little under one frame
            Breather.frameNStart = frameN  # exact frame index
            Breather.setAutoDraw(True)
        if Breather.status == STARTED and t >= (0.0 + (5-win.monitorFramePeriod*0.75)): #most of one frame period left
            Breather.setAutoDraw(False)
        
        # *plus* updates
        if t >= 5 and plus.status == NOT_STARTED:
            # keep track of start time/frame for later
            plus.tStart = t  # underestimates by a little under one frame
            plus.frameNStart = frameN  # exact frame index
            plus.setAutoDraw(True)
        if plus.status == STARTED and t >= (25-win.monitorFramePeriod*0.75): #most of one frame period left
            plus.setAutoDraw(False)
        
        # *readyPlus* updates
        if t >= 25 and readyPlus.status == NOT_STARTED:
            # keep track of start time/frame for later
            readyPlus.tStart = t  # underestimates by a little under one frame
            readyPlus.frameNStart = frameN  # exact frame index
            readyPlus.setAutoDraw(True)
        if readyPlus.status == STARTED and t >= (30-win.monitorFramePeriod*0.75): #most of one frame period left
            readyPlus.setAutoDraw(False)
        
        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            routineTimer.reset()  # if we abort early the non-slip timer needs reset
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in RestComponents:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # check for quit (the Esc key)
        if endExpNow or event.getKeys(keyList=["escape"]):
            core.quit()
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    #-------Ending Routine "Rest"-------
    for thisComponent in RestComponents:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    BlockRTs = []
    print('Criteria for next block = ' + str(crit))
    
    # set up handler to look after randomisation of conditions etc
    init_seq = data.TrialHandler(nReps=1, method='sequential', 
        extraInfo=expInfo, originPath=u'/Users/steelad/Desktop/Subj_fMRI_Grouped_timedRest_nocounter_framed/Adam_SRTT_Seq.ContPun_grouped.psyexp',
        trialList=data.importConditions(seq_order_file),
        seed=None, name='init_seq')
    thisExp.addLoop(init_seq)  # add the loop to the experiment
    thisInit_seq = init_seq.trialList[0]  # so we can initialise stimuli with some values
    # abbreviate parameter names if possible (e.g. rgb=thisInit_seq.rgb)
    if thisInit_seq != None:
        for paramName in thisInit_seq.keys():
            exec(paramName + '= thisInit_seq.' + paramName)
    
    for thisInit_seq in init_seq:
        currentLoop = init_seq
        # abbreviate parameter names if possible (e.g. rgb = thisInit_seq.rgb)
        if thisInit_seq != None:
            for paramName in thisInit_seq.keys():
                exec(paramName + '= thisInit_seq.' + paramName)
        
        #------Prepare to start Routine "trial"-------
        t = 0
        trialClock.reset()  # clock 
        frameN = -1
        routineTimer.add(0.800000)
        # update component parameters for each repeat
        Resp = event.BuilderKeyResponse()  # create an object of type KeyResponse
        Resp.status = NOT_STARTED
        #Init_rand.addData('Earnings Total', e_string)
        # keep track of which components have finished
        trialComponents = []
        trialComponents.append(FB_Seq_trial)
        trialComponents.append(Stimulus_appear)
        trialComponents.append(Resp)
        for thisComponent in trialComponents:
            if hasattr(thisComponent, 'status'):
                thisComponent.status = NOT_STARTED
        
        #-------Start Routine "trial"-------
        continueRoutine = True
        while continueRoutine and routineTimer.getTime() > 0:
            # get current time
            t = trialClock.getTime()
            frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
            # update/draw components on each frame
            
            # *FB_Seq_trial* updates
            if t >= 0.0 and FB_Seq_trial.status == NOT_STARTED:
                # keep track of start time/frame for later
                FB_Seq_trial.tStart = t  # underestimates by a little under one frame
                FB_Seq_trial.frameNStart = frameN  # exact frame index
                FB_Seq_trial.setAutoDraw(True)
            if FB_Seq_trial.status == STARTED and t >= (0.0 + (0.8-win.monitorFramePeriod*0.75)): #most of one frame period left
                FB_Seq_trial.setAutoDraw(False)
            
            # *Stimulus_appear* updates
            if t >= 0 and Stimulus_appear.status == NOT_STARTED:
                # keep track of start time/frame for later
                Stimulus_appear.tStart = t  # underestimates by a little under one frame
                Stimulus_appear.frameNStart = frameN  # exact frame index
                Stimulus_appear.setAutoDraw(True)
            if Stimulus_appear.status == STARTED and t >= (0.8-win.monitorFramePeriod*0.75): #most of one frame period left
                Stimulus_appear.setAutoDraw(False)
            if Stimulus_appear.status == STARTED:  # only update if being drawn
                Stimulus_appear.setText(Stimulus, log=False)
            
            # *Resp* updates
            if t >= 0 and Resp.status == NOT_STARTED:
                # keep track of start time/frame for later
                Resp.tStart = t  # underestimates by a little under one frame
                Resp.frameNStart = frameN  # exact frame index
                Resp.status = STARTED
                # keyboard checking is just starting
                Resp.clock.reset()  # now t=0
                event.clearEvents(eventType='keyboard')
            if Resp.status == STARTED and t >= (0.8-win.monitorFramePeriod*0.75): #most of one frame period left
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
            
            
            # check if all components have finished
            if not continueRoutine:  # a component has requested a forced-end of Routine
                routineTimer.reset()  # if we abort early the non-slip timer needs reset
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
        # store data for init_seq (TrialHandler)
        init_seq.addData('Resp.keys',Resp.keys)
        init_seq.addData('Resp.corr', Resp.corr)
        if Resp.keys != None:  # we had a response
            init_seq.addData('Resp.rt', Resp.rt)
        
        
        #------Prepare to start Routine "Feedback_ISI"-------
        t = 0
        Feedback_ISIClock.reset()  # clock 
        frameN = -1
        routineTimer.add(0.200000)
        # update component parameters for each repeat
        if Resp.corr and Resp.rt < crit:
            BlockRTs.append(Resp.rt)
        
        
        Color = gen_fb(Feedback,fb_block,trial)
        
        if Resp.corr and Resp.rt < crit:
        #    Color = [0,1,0]
            Earning_Trial.append(1)
        #    earning = earning + 0.05
        #    e_string = str(earning)
        else:
        #    Color = [1,1,1]
            Earning_Trial.append(0)
        FB_seq.setLineColor(Color)
        # keep track of which components have finished
        Feedback_ISIComponents = []
        Feedback_ISIComponents.append(FB_seq)
        Feedback_ISIComponents.append(ISI)
        for thisComponent in Feedback_ISIComponents:
            if hasattr(thisComponent, 'status'):
                thisComponent.status = NOT_STARTED
        
        #-------Start Routine "Feedback_ISI"-------
        continueRoutine = True
        while continueRoutine and routineTimer.getTime() > 0:
            # get current time
            t = Feedback_ISIClock.getTime()
            frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
            # update/draw components on each frame
            
            
            
            
            # *FB_seq* updates
            if t >= 0 and FB_seq.status == NOT_STARTED:
                # keep track of start time/frame for later
                FB_seq.tStart = t  # underestimates by a little under one frame
                FB_seq.frameNStart = frameN  # exact frame index
                FB_seq.setAutoDraw(True)
            if FB_seq.status == STARTED and t >= (0 + (.2-win.monitorFramePeriod*0.75)): #most of one frame period left
                FB_seq.setAutoDraw(False)
            
            # *ISI* updates
            if t >= 0.0 and ISI.status == NOT_STARTED:
                # keep track of start time/frame for later
                ISI.tStart = t  # underestimates by a little under one frame
                ISI.frameNStart = frameN  # exact frame index
                ISI.setAutoDraw(True)
            if ISI.status == STARTED and t >= (0.0 + (.2-win.monitorFramePeriod*0.75)): #most of one frame period left
                ISI.setAutoDraw(False)
            
            # check if all components have finished
            if not continueRoutine:  # a component has requested a forced-end of Routine
                routineTimer.reset()  # if we abort early the non-slip timer needs reset
                break
            continueRoutine = False  # will revert to True if at least one component still running
            for thisComponent in Feedback_ISIComponents:
                if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                    continueRoutine = True
                    break  # at least one component has not yet finished
            
            # check for quit (the Esc key)
            if endExpNow or event.getKeys(keyList=["escape"]):
                core.quit()
            
            # refresh the screen
            if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                win.flip()
        
        #-------Ending Routine "Feedback_ISI"-------
        for thisComponent in Feedback_ISIComponents:
            if hasattr(thisComponent, "setAutoDraw"):
                thisComponent.setAutoDraw(False)
        trial = trial + 1
        thisExp.nextEntry()
        
    # completed 1 repeats of 'init_seq'
    
    
    #------Prepare to start Routine "Rest"-------
    t = 0
    RestClock.reset()  # clock 
    frameN = -1
    routineTimer.add(30.000000)
    # update component parameters for each repeat
    vector = []
    count = 0
    Respvec = []
    other = []
    Keyvec = []
    trial = 0
    crit = Calc_Block_Criterion(BlockRTs,crit)
    
    makesequencestart(sequence)
    makerandom()
    
    breatherphrase = str("Good job, your earnings increased!\n\nYou finished block %s.  \n \nTake a breather. \n \n" % (block))
    block = block+1
    fb_block = block - 1
    Breather.setText(breatherphrase)
    # keep track of which components have finished
    RestComponents = []
    RestComponents.append(Breather)
    RestComponents.append(plus)
    RestComponents.append(readyPlus)
    for thisComponent in RestComponents:
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
    
    #-------Start Routine "Rest"-------
    continueRoutine = True
    while continueRoutine and routineTimer.getTime() > 0:
        # get current time
        t = RestClock.getTime()
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        
        
        # *Breather* updates
        if t >= 0.0 and Breather.status == NOT_STARTED:
            # keep track of start time/frame for later
            Breather.tStart = t  # underestimates by a little under one frame
            Breather.frameNStart = frameN  # exact frame index
            Breather.setAutoDraw(True)
        if Breather.status == STARTED and t >= (0.0 + (5-win.monitorFramePeriod*0.75)): #most of one frame period left
            Breather.setAutoDraw(False)
        
        # *plus* updates
        if t >= 5 and plus.status == NOT_STARTED:
            # keep track of start time/frame for later
            plus.tStart = t  # underestimates by a little under one frame
            plus.frameNStart = frameN  # exact frame index
            plus.setAutoDraw(True)
        if plus.status == STARTED and t >= (25-win.monitorFramePeriod*0.75): #most of one frame period left
            plus.setAutoDraw(False)
        
        # *readyPlus* updates
        if t >= 25 and readyPlus.status == NOT_STARTED:
            # keep track of start time/frame for later
            readyPlus.tStart = t  # underestimates by a little under one frame
            readyPlus.frameNStart = frameN  # exact frame index
            readyPlus.setAutoDraw(True)
        if readyPlus.status == STARTED and t >= (30-win.monitorFramePeriod*0.75): #most of one frame period left
            readyPlus.setAutoDraw(False)
        
        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            routineTimer.reset()  # if we abort early the non-slip timer needs reset
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in RestComponents:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # check for quit (the Esc key)
        if endExpNow or event.getKeys(keyList=["escape"]):
            core.quit()
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    #-------Ending Routine "Rest"-------
    for thisComponent in RestComponents:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    BlockRTs = []
    print('Criteria for next block = ' + str(crit))
    
    # set up handler to look after randomisation of conditions etc
    init_rand2 = data.TrialHandler(nReps=1, method='sequential', 
        extraInfo=expInfo, originPath=u'/Users/steelad/Desktop/Subj_fMRI_Grouped_timedRest_nocounter_framed/Adam_SRTT_Seq.ContPun_grouped.psyexp',
        trialList=data.importConditions('RandOrder.csv'),
        seed=None, name='init_rand2')
    thisExp.addLoop(init_rand2)  # add the loop to the experiment
    thisInit_rand2 = init_rand2.trialList[0]  # so we can initialise stimuli with some values
    # abbreviate parameter names if possible (e.g. rgb=thisInit_rand2.rgb)
    if thisInit_rand2 != None:
        for paramName in thisInit_rand2.keys():
            exec(paramName + '= thisInit_rand2.' + paramName)
    
    for thisInit_rand2 in init_rand2:
        currentLoop = init_rand2
        # abbreviate parameter names if possible (e.g. rgb = thisInit_rand2.rgb)
        if thisInit_rand2 != None:
            for paramName in thisInit_rand2.keys():
                exec(paramName + '= thisInit_rand2.' + paramName)
        
        #------Prepare to start Routine "RandBlock"-------
        t = 0
        RandBlockClock.reset()  # clock 
        frameN = -1
        routineTimer.add(0.800000)
        # update component parameters for each repeat
        
        Stimulus_rand.setText(RandStim)
        RandResp = event.BuilderKeyResponse()  # create an object of type KeyResponse
        RandResp.status = NOT_STARTED
        # keep track of which components have finished
        RandBlockComponents = []
        RandBlockComponents.append(RandFB_trial)
        RandBlockComponents.append(Stimulus_rand)
        RandBlockComponents.append(RandResp)
        for thisComponent in RandBlockComponents:
            if hasattr(thisComponent, 'status'):
                thisComponent.status = NOT_STARTED
        
        #-------Start Routine "RandBlock"-------
        continueRoutine = True
        while continueRoutine and routineTimer.getTime() > 0:
            # get current time
            t = RandBlockClock.getTime()
            frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
            # update/draw components on each frame
            
            
            # *RandFB_trial* updates
            if t >= 0.0 and RandFB_trial.status == NOT_STARTED:
                # keep track of start time/frame for later
                RandFB_trial.tStart = t  # underestimates by a little under one frame
                RandFB_trial.frameNStart = frameN  # exact frame index
                RandFB_trial.setAutoDraw(True)
            if RandFB_trial.status == STARTED and t >= (0.0 + (0.8-win.monitorFramePeriod*0.75)): #most of one frame period left
                RandFB_trial.setAutoDraw(False)
            
            # *Stimulus_rand* updates
            if t >= 0.0 and Stimulus_rand.status == NOT_STARTED:
                # keep track of start time/frame for later
                Stimulus_rand.tStart = t  # underestimates by a little under one frame
                Stimulus_rand.frameNStart = frameN  # exact frame index
                Stimulus_rand.setAutoDraw(True)
            if Stimulus_rand.status == STARTED and t >= (0.8-win.monitorFramePeriod*0.75): #most of one frame period left
                Stimulus_rand.setAutoDraw(False)
            
            # *RandResp* updates
            if t >= 0 and RandResp.status == NOT_STARTED:
                # keep track of start time/frame for later
                RandResp.tStart = t  # underestimates by a little under one frame
                RandResp.frameNStart = frameN  # exact frame index
                RandResp.status = STARTED
                # keyboard checking is just starting
                RandResp.clock.reset()  # now t=0
                event.clearEvents(eventType='keyboard')
            if RandResp.status == STARTED and t >= (0.8-win.monitorFramePeriod*0.75): #most of one frame period left
                RandResp.status = STOPPED
            if RandResp.status == STARTED:
                theseKeys = event.getKeys(keyList=['1', '2', '3', '4'])
                
                # check for quit:
                if "escape" in theseKeys:
                    endExpNow = True
                if len(theseKeys) > 0:  # at least one key was pressed
                    if RandResp.keys == []:  # then this was the first keypress
                        RandResp.keys = theseKeys[0]  # just the first key pressed
                        RandResp.rt = RandResp.clock.getTime()
                        # was this 'correct'?
                        if (RandResp.keys == str(RandomResp)) or (RandResp.keys == RandomResp):
                            RandResp.corr = 1
                        else:
                            RandResp.corr = 0
            
            # check if all components have finished
            if not continueRoutine:  # a component has requested a forced-end of Routine
                routineTimer.reset()  # if we abort early the non-slip timer needs reset
                break
            continueRoutine = False  # will revert to True if at least one component still running
            for thisComponent in RandBlockComponents:
                if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                    continueRoutine = True
                    break  # at least one component has not yet finished
            
            # check for quit (the Esc key)
            if endExpNow or event.getKeys(keyList=["escape"]):
                core.quit()
            
            # refresh the screen
            if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                win.flip()
        
        #-------Ending Routine "RandBlock"-------
        for thisComponent in RandBlockComponents:
            if hasattr(thisComponent, "setAutoDraw"):
                thisComponent.setAutoDraw(False)
        
        # check responses
        if RandResp.keys in ['', [], None]:  # No response was made
           RandResp.keys=None
           # was no response the correct answer?!
           if str(RandomResp).lower() == 'none': RandResp.corr = 1  # correct non-response
           else: RandResp.corr = 0  # failed to respond (incorrectly)
        # store data for init_rand2 (TrialHandler)
        init_rand2.addData('RandResp.keys',RandResp.keys)
        init_rand2.addData('RandResp.corr', RandResp.corr)
        if RandResp.keys != None:  # we had a response
            init_rand2.addData('RandResp.rt', RandResp.rt)
        
        #------Prepare to start Routine "RandFeedback"-------
        t = 0
        RandFeedbackClock.reset()  # clock 
        frameN = -1
        routineTimer.add(0.200000)
        # update component parameters for each repeat
        if RandResp.corr:
            BlockRTs.append(RandResp.rt)
        Color = gen_fb(Feedback,fb_block,trial)
        if RandResp.corr and RandResp.rt < crit:
        #    Color = [0,1,0]
            Earning_Trial.append(1)
        #    earning = earning + 0.05
        #    e_string = str(earning)
        else:
        #    Color = [1,1,1]
            Earning_Trial.append(0)
        FB_Rand.setFillColor([0,0,0])
        FB_Rand.setLineColor(Color)
        # keep track of which components have finished
        RandFeedbackComponents = []
        RandFeedbackComponents.append(FB_Rand)
        RandFeedbackComponents.append(ISI_rand)
        for thisComponent in RandFeedbackComponents:
            if hasattr(thisComponent, 'status'):
                thisComponent.status = NOT_STARTED
        
        #-------Start Routine "RandFeedback"-------
        continueRoutine = True
        while continueRoutine and routineTimer.getTime() > 0:
            # get current time
            t = RandFeedbackClock.getTime()
            frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
            # update/draw components on each frame
            
            
            # *FB_Rand* updates
            if t >= 0.0 and FB_Rand.status == NOT_STARTED:
                # keep track of start time/frame for later
                FB_Rand.tStart = t  # underestimates by a little under one frame
                FB_Rand.frameNStart = frameN  # exact frame index
                FB_Rand.setAutoDraw(True)
            if FB_Rand.status == STARTED and t >= (0.0 + (0.2-win.monitorFramePeriod*0.75)): #most of one frame period left
                FB_Rand.setAutoDraw(False)
            
            # *ISI_rand* updates
            if t >= 0.0 and ISI_rand.status == NOT_STARTED:
                # keep track of start time/frame for later
                ISI_rand.tStart = t  # underestimates by a little under one frame
                ISI_rand.frameNStart = frameN  # exact frame index
                ISI_rand.setAutoDraw(True)
            if ISI_rand.status == STARTED and t >= (0.0 + (.2-win.monitorFramePeriod*0.75)): #most of one frame period left
                ISI_rand.setAutoDraw(False)
            
            # check if all components have finished
            if not continueRoutine:  # a component has requested a forced-end of Routine
                routineTimer.reset()  # if we abort early the non-slip timer needs reset
                break
            continueRoutine = False  # will revert to True if at least one component still running
            for thisComponent in RandFeedbackComponents:
                if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                    continueRoutine = True
                    break  # at least one component has not yet finished
            
            # check for quit (the Esc key)
            if endExpNow or event.getKeys(keyList=["escape"]):
                core.quit()
            
            # refresh the screen
            if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                win.flip()
        
        #-------Ending Routine "RandFeedback"-------
        for thisComponent in RandFeedbackComponents:
            if hasattr(thisComponent, "setAutoDraw"):
                thisComponent.setAutoDraw(False)
        trial = trial + 1
        thisExp.nextEntry()
        
    # completed 1 repeats of 'init_rand2'
    
    
    #------Prepare to start Routine "Rest"-------
    t = 0
    RestClock.reset()  # clock 
    frameN = -1
    routineTimer.add(30.000000)
    # update component parameters for each repeat
    vector = []
    count = 0
    Respvec = []
    other = []
    Keyvec = []
    trial = 0
    crit = Calc_Block_Criterion(BlockRTs,crit)
    
    makesequencestart(sequence)
    makerandom()
    
    breatherphrase = str("Good job, your earnings increased!\n\nYou finished block %s.  \n \nTake a breather. \n \n" % (block))
    block = block+1
    fb_block = block - 1
    Breather.setText(breatherphrase)
    # keep track of which components have finished
    RestComponents = []
    RestComponents.append(Breather)
    RestComponents.append(plus)
    RestComponents.append(readyPlus)
    for thisComponent in RestComponents:
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
    
    #-------Start Routine "Rest"-------
    continueRoutine = True
    while continueRoutine and routineTimer.getTime() > 0:
        # get current time
        t = RestClock.getTime()
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        
        
        # *Breather* updates
        if t >= 0.0 and Breather.status == NOT_STARTED:
            # keep track of start time/frame for later
            Breather.tStart = t  # underestimates by a little under one frame
            Breather.frameNStart = frameN  # exact frame index
            Breather.setAutoDraw(True)
        if Breather.status == STARTED and t >= (0.0 + (5-win.monitorFramePeriod*0.75)): #most of one frame period left
            Breather.setAutoDraw(False)
        
        # *plus* updates
        if t >= 5 and plus.status == NOT_STARTED:
            # keep track of start time/frame for later
            plus.tStart = t  # underestimates by a little under one frame
            plus.frameNStart = frameN  # exact frame index
            plus.setAutoDraw(True)
        if plus.status == STARTED and t >= (25-win.monitorFramePeriod*0.75): #most of one frame period left
            plus.setAutoDraw(False)
        
        # *readyPlus* updates
        if t >= 25 and readyPlus.status == NOT_STARTED:
            # keep track of start time/frame for later
            readyPlus.tStart = t  # underestimates by a little under one frame
            readyPlus.frameNStart = frameN  # exact frame index
            readyPlus.setAutoDraw(True)
        if readyPlus.status == STARTED and t >= (30-win.monitorFramePeriod*0.75): #most of one frame period left
            readyPlus.setAutoDraw(False)
        
        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            routineTimer.reset()  # if we abort early the non-slip timer needs reset
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in RestComponents:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # check for quit (the Esc key)
        if endExpNow or event.getKeys(keyList=["escape"]):
            core.quit()
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    #-------Ending Routine "Rest"-------
    for thisComponent in RestComponents:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    BlockRTs = []
    print('Criteria for next block = ' + str(crit))
    thisExp.nextEntry()
    
# completed 1 repeats of 'Run1'


# set up handler to look after randomisation of conditions etc
Run2 = data.TrialHandler(nReps=1, method='sequential', 
    extraInfo=expInfo, originPath=u'/Users/steelad/Desktop/Subj_fMRI_Grouped_timedRest_nocounter_framed/Adam_SRTT_Seq.ContPun_grouped.psyexp',
    trialList=[None],
    seed=None, name='Run2')
thisExp.addLoop(Run2)  # add the loop to the experiment
thisRun2 = Run2.trialList[0]  # so we can initialise stimuli with some values
# abbreviate parameter names if possible (e.g. rgb=thisRun2.rgb)
if thisRun2 != None:
    for paramName in thisRun2.keys():
        exec(paramName + '= thisRun2.' + paramName)

for thisRun2 in Run2:
    currentLoop = Run2
    # abbreviate parameter names if possible (e.g. rgb = thisRun2.rgb)
    if thisRun2 != None:
        for paramName in thisRun2.keys():
            exec(paramName + '= thisRun2.' + paramName)
    
    #------Prepare to start Routine "RunBreak"-------
    t = 0
    RunBreakClock.reset()  # clock 
    frameN = -1
    # update component parameters for each repeat
    phrase = str("Good job, you finished run %s.  \n \nTake a breather. \n \nYou have earned money" % (Run))
    
    RunBreakText.setText(phrase)
    SpacetoMoveOn = event.BuilderKeyResponse()  # create an object of type KeyResponse
    SpacetoMoveOn.status = NOT_STARTED
    # keep track of which components have finished
    RunBreakComponents = []
    RunBreakComponents.append(RunBreakText)
    RunBreakComponents.append(SpacetoMoveOn)
    RunBreakComponents.append(ExperimenterRole)
    for thisComponent in RunBreakComponents:
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
    
    #-------Start Routine "RunBreak"-------
    continueRoutine = True
    while continueRoutine:
        # get current time
        t = RunBreakClock.getTime()
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        
        
        # *RunBreakText* updates
        if t >= 0.0 and RunBreakText.status == NOT_STARTED:
            # keep track of start time/frame for later
            RunBreakText.tStart = t  # underestimates by a little under one frame
            RunBreakText.frameNStart = frameN  # exact frame index
            RunBreakText.setAutoDraw(True)
        
        # *SpacetoMoveOn* updates
        if t >= 0.0 and SpacetoMoveOn.status == NOT_STARTED:
            # keep track of start time/frame for later
            SpacetoMoveOn.tStart = t  # underestimates by a little under one frame
            SpacetoMoveOn.frameNStart = frameN  # exact frame index
            SpacetoMoveOn.status = STARTED
            # keyboard checking is just starting
            event.clearEvents(eventType='keyboard')
        if SpacetoMoveOn.status == STARTED:
            theseKeys = event.getKeys(keyList=['space'])
            
            # check for quit:
            if "escape" in theseKeys:
                endExpNow = True
            if len(theseKeys) > 0:  # at least one key was pressed
                # a response ends the routine
                continueRoutine = False
        
        # *ExperimenterRole* updates
        if t >= 0.0 and ExperimenterRole.status == NOT_STARTED:
            # keep track of start time/frame for later
            ExperimenterRole.tStart = t  # underestimates by a little under one frame
            ExperimenterRole.frameNStart = frameN  # exact frame index
            ExperimenterRole.setAutoDraw(True)
        
        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            routineTimer.reset()  # if we abort early the non-slip timer needs reset
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in RunBreakComponents:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # check for quit (the Esc key)
        if endExpNow or event.getKeys(keyList=["escape"]):
            core.quit()
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
        else:  # this Routine was not non-slip safe so reset non-slip timer
            routineTimer.reset()
    
    #-------Ending Routine "RunBreak"-------
    for thisComponent in RunBreakComponents:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    
    
    #------Prepare to start Routine "WaitforTrigger"-------
    t = 0
    WaitforTriggerClock.reset()  # clock 
    frameN = -1
    # update component parameters for each repeat
    TriggerIn = event.BuilderKeyResponse()  # create an object of type KeyResponse
    TriggerIn.status = NOT_STARTED
    # keep track of which components have finished
    WaitforTriggerComponents = []
    WaitforTriggerComponents.append(text_4)
    WaitforTriggerComponents.append(TriggerIn)
    for thisComponent in WaitforTriggerComponents:
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
    
    #-------Start Routine "WaitforTrigger"-------
    continueRoutine = True
    while continueRoutine:
        # get current time
        t = WaitforTriggerClock.getTime()
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        
        # *text_4* updates
        if t >= 0.0 and text_4.status == NOT_STARTED:
            # keep track of start time/frame for later
            text_4.tStart = t  # underestimates by a little under one frame
            text_4.frameNStart = frameN  # exact frame index
            text_4.setAutoDraw(True)
        
        # *TriggerIn* updates
        if t >= 0.0 and TriggerIn.status == NOT_STARTED:
            # keep track of start time/frame for later
            TriggerIn.tStart = t  # underestimates by a little under one frame
            TriggerIn.frameNStart = frameN  # exact frame index
            TriggerIn.status = STARTED
            # keyboard checking is just starting
            event.clearEvents(eventType='keyboard')
        if TriggerIn.status == STARTED:
            theseKeys = event.getKeys(keyList=['5'])
            
            # check for quit:
            if "escape" in theseKeys:
                endExpNow = True
            if len(theseKeys) > 0:  # at least one key was pressed
                # a response ends the routine
                continueRoutine = False
        
        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            routineTimer.reset()  # if we abort early the non-slip timer needs reset
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in WaitforTriggerComponents:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # check for quit (the Esc key)
        if endExpNow or event.getKeys(keyList=["escape"]):
            core.quit()
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
        else:  # this Routine was not non-slip safe so reset non-slip timer
            routineTimer.reset()
    
    #-------Ending Routine "WaitforTrigger"-------
    for thisComponent in WaitforTriggerComponents:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    
    #------Prepare to start Routine "BeginRun"-------
    t = 0
    BeginRunClock.reset()  # clock 
    frameN = -1
    routineTimer.add(12.000000)
    # update component parameters for each repeat
    
    # keep track of which components have finished
    BeginRunComponents = []
    BeginRunComponents.append(Plus)
    BeginRunComponents.append(Plus_ready)
    for thisComponent in BeginRunComponents:
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
    
    #-------Start Routine "BeginRun"-------
    continueRoutine = True
    while continueRoutine and routineTimer.getTime() > 0:
        # get current time
        t = BeginRunClock.getTime()
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        
        # *Plus* updates
        if t >= 0.0 and Plus.status == NOT_STARTED:
            # keep track of start time/frame for later
            Plus.tStart = t  # underestimates by a little under one frame
            Plus.frameNStart = frameN  # exact frame index
            Plus.setAutoDraw(True)
        if Plus.status == STARTED and t >= (7-win.monitorFramePeriod*0.75): #most of one frame period left
            Plus.setAutoDraw(False)
        
        # *Plus_ready* updates
        if t >= 7 and Plus_ready.status == NOT_STARTED:
            # keep track of start time/frame for later
            Plus_ready.tStart = t  # underestimates by a little under one frame
            Plus_ready.frameNStart = frameN  # exact frame index
            Plus_ready.setAutoDraw(True)
        if Plus_ready.status == STARTED and t >= (12-win.monitorFramePeriod*0.75): #most of one frame period left
            Plus_ready.setAutoDraw(False)
        
        
        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            routineTimer.reset()  # if we abort early the non-slip timer needs reset
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in BeginRunComponents:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # check for quit (the Esc key)
        if endExpNow or event.getKeys(keyList=["escape"]):
            core.quit()
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    #-------Ending Routine "BeginRun"-------
    for thisComponent in BeginRunComponents:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    Run = Run + 1
    
    # set up handler to look after randomisation of conditions etc
    seq_block_run2 = data.TrialHandler(nReps=3, method='sequential', 
        extraInfo=expInfo, originPath=u'/Users/steelad/Desktop/Subj_fMRI_Grouped_timedRest_nocounter_framed/Adam_SRTT_Seq.ContPun_grouped.psyexp',
        trialList=[None],
        seed=None, name='seq_block_run2')
    thisExp.addLoop(seq_block_run2)  # add the loop to the experiment
    thisSeq_block_run2 = seq_block_run2.trialList[0]  # so we can initialise stimuli with some values
    # abbreviate parameter names if possible (e.g. rgb=thisSeq_block_run2.rgb)
    if thisSeq_block_run2 != None:
        for paramName in thisSeq_block_run2.keys():
            exec(paramName + '= thisSeq_block_run2.' + paramName)
    
    for thisSeq_block_run2 in seq_block_run2:
        currentLoop = seq_block_run2
        # abbreviate parameter names if possible (e.g. rgb = thisSeq_block_run2.rgb)
        if thisSeq_block_run2 != None:
            for paramName in thisSeq_block_run2.keys():
                exec(paramName + '= thisSeq_block_run2.' + paramName)
        
        # set up handler to look after randomisation of conditions etc
        seq_trials2 = data.TrialHandler(nReps=1, method='sequential', 
            extraInfo=expInfo, originPath=u'/Users/steelad/Desktop/Subj_fMRI_Grouped_timedRest_nocounter_framed/Adam_SRTT_Seq.ContPun_grouped.psyexp',
            trialList=data.importConditions(seq_order_file),
            seed=None, name='seq_trials2')
        thisExp.addLoop(seq_trials2)  # add the loop to the experiment
        thisSeq_trials2 = seq_trials2.trialList[0]  # so we can initialise stimuli with some values
        # abbreviate parameter names if possible (e.g. rgb=thisSeq_trials2.rgb)
        if thisSeq_trials2 != None:
            for paramName in thisSeq_trials2.keys():
                exec(paramName + '= thisSeq_trials2.' + paramName)
        
        for thisSeq_trials2 in seq_trials2:
            currentLoop = seq_trials2
            # abbreviate parameter names if possible (e.g. rgb = thisSeq_trials2.rgb)
            if thisSeq_trials2 != None:
                for paramName in thisSeq_trials2.keys():
                    exec(paramName + '= thisSeq_trials2.' + paramName)
            
            #------Prepare to start Routine "trial"-------
            t = 0
            trialClock.reset()  # clock 
            frameN = -1
            routineTimer.add(0.800000)
            # update component parameters for each repeat
            Resp = event.BuilderKeyResponse()  # create an object of type KeyResponse
            Resp.status = NOT_STARTED
            #Init_rand.addData('Earnings Total', e_string)
            # keep track of which components have finished
            trialComponents = []
            trialComponents.append(FB_Seq_trial)
            trialComponents.append(Stimulus_appear)
            trialComponents.append(Resp)
            for thisComponent in trialComponents:
                if hasattr(thisComponent, 'status'):
                    thisComponent.status = NOT_STARTED
            
            #-------Start Routine "trial"-------
            continueRoutine = True
            while continueRoutine and routineTimer.getTime() > 0:
                # get current time
                t = trialClock.getTime()
                frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
                # update/draw components on each frame
                
                # *FB_Seq_trial* updates
                if t >= 0.0 and FB_Seq_trial.status == NOT_STARTED:
                    # keep track of start time/frame for later
                    FB_Seq_trial.tStart = t  # underestimates by a little under one frame
                    FB_Seq_trial.frameNStart = frameN  # exact frame index
                    FB_Seq_trial.setAutoDraw(True)
                if FB_Seq_trial.status == STARTED and t >= (0.0 + (0.8-win.monitorFramePeriod*0.75)): #most of one frame period left
                    FB_Seq_trial.setAutoDraw(False)
                
                # *Stimulus_appear* updates
                if t >= 0 and Stimulus_appear.status == NOT_STARTED:
                    # keep track of start time/frame for later
                    Stimulus_appear.tStart = t  # underestimates by a little under one frame
                    Stimulus_appear.frameNStart = frameN  # exact frame index
                    Stimulus_appear.setAutoDraw(True)
                if Stimulus_appear.status == STARTED and t >= (0.8-win.monitorFramePeriod*0.75): #most of one frame period left
                    Stimulus_appear.setAutoDraw(False)
                if Stimulus_appear.status == STARTED:  # only update if being drawn
                    Stimulus_appear.setText(Stimulus, log=False)
                
                # *Resp* updates
                if t >= 0 and Resp.status == NOT_STARTED:
                    # keep track of start time/frame for later
                    Resp.tStart = t  # underestimates by a little under one frame
                    Resp.frameNStart = frameN  # exact frame index
                    Resp.status = STARTED
                    # keyboard checking is just starting
                    Resp.clock.reset()  # now t=0
                    event.clearEvents(eventType='keyboard')
                if Resp.status == STARTED and t >= (0.8-win.monitorFramePeriod*0.75): #most of one frame period left
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
                
                
                # check if all components have finished
                if not continueRoutine:  # a component has requested a forced-end of Routine
                    routineTimer.reset()  # if we abort early the non-slip timer needs reset
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
            # store data for seq_trials2 (TrialHandler)
            seq_trials2.addData('Resp.keys',Resp.keys)
            seq_trials2.addData('Resp.corr', Resp.corr)
            if Resp.keys != None:  # we had a response
                seq_trials2.addData('Resp.rt', Resp.rt)
            
            
            #------Prepare to start Routine "Feedback_ISI"-------
            t = 0
            Feedback_ISIClock.reset()  # clock 
            frameN = -1
            routineTimer.add(0.200000)
            # update component parameters for each repeat
            if Resp.corr and Resp.rt < crit:
                BlockRTs.append(Resp.rt)
            
            
            Color = gen_fb(Feedback,fb_block,trial)
            
            if Resp.corr and Resp.rt < crit:
            #    Color = [0,1,0]
                Earning_Trial.append(1)
            #    earning = earning + 0.05
            #    e_string = str(earning)
            else:
            #    Color = [1,1,1]
                Earning_Trial.append(0)
            FB_seq.setLineColor(Color)
            # keep track of which components have finished
            Feedback_ISIComponents = []
            Feedback_ISIComponents.append(FB_seq)
            Feedback_ISIComponents.append(ISI)
            for thisComponent in Feedback_ISIComponents:
                if hasattr(thisComponent, 'status'):
                    thisComponent.status = NOT_STARTED
            
            #-------Start Routine "Feedback_ISI"-------
            continueRoutine = True
            while continueRoutine and routineTimer.getTime() > 0:
                # get current time
                t = Feedback_ISIClock.getTime()
                frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
                # update/draw components on each frame
                
                
                
                
                # *FB_seq* updates
                if t >= 0 and FB_seq.status == NOT_STARTED:
                    # keep track of start time/frame for later
                    FB_seq.tStart = t  # underestimates by a little under one frame
                    FB_seq.frameNStart = frameN  # exact frame index
                    FB_seq.setAutoDraw(True)
                if FB_seq.status == STARTED and t >= (0 + (.2-win.monitorFramePeriod*0.75)): #most of one frame period left
                    FB_seq.setAutoDraw(False)
                
                # *ISI* updates
                if t >= 0.0 and ISI.status == NOT_STARTED:
                    # keep track of start time/frame for later
                    ISI.tStart = t  # underestimates by a little under one frame
                    ISI.frameNStart = frameN  # exact frame index
                    ISI.setAutoDraw(True)
                if ISI.status == STARTED and t >= (0.0 + (.2-win.monitorFramePeriod*0.75)): #most of one frame period left
                    ISI.setAutoDraw(False)
                
                # check if all components have finished
                if not continueRoutine:  # a component has requested a forced-end of Routine
                    routineTimer.reset()  # if we abort early the non-slip timer needs reset
                    break
                continueRoutine = False  # will revert to True if at least one component still running
                for thisComponent in Feedback_ISIComponents:
                    if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                        continueRoutine = True
                        break  # at least one component has not yet finished
                
                # check for quit (the Esc key)
                if endExpNow or event.getKeys(keyList=["escape"]):
                    core.quit()
                
                # refresh the screen
                if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                    win.flip()
            
            #-------Ending Routine "Feedback_ISI"-------
            for thisComponent in Feedback_ISIComponents:
                if hasattr(thisComponent, "setAutoDraw"):
                    thisComponent.setAutoDraw(False)
            trial = trial + 1
            thisExp.nextEntry()
            
        # completed 1 repeats of 'seq_trials2'
        
        
        #------Prepare to start Routine "Rest"-------
        t = 0
        RestClock.reset()  # clock 
        frameN = -1
        routineTimer.add(30.000000)
        # update component parameters for each repeat
        vector = []
        count = 0
        Respvec = []
        other = []
        Keyvec = []
        trial = 0
        crit = Calc_Block_Criterion(BlockRTs,crit)
        
        makesequencestart(sequence)
        makerandom()
        
        breatherphrase = str("Good job, your earnings increased!\n\nYou finished block %s.  \n \nTake a breather. \n \n" % (block))
        block = block+1
        fb_block = block - 1
        Breather.setText(breatherphrase)
        # keep track of which components have finished
        RestComponents = []
        RestComponents.append(Breather)
        RestComponents.append(plus)
        RestComponents.append(readyPlus)
        for thisComponent in RestComponents:
            if hasattr(thisComponent, 'status'):
                thisComponent.status = NOT_STARTED
        
        #-------Start Routine "Rest"-------
        continueRoutine = True
        while continueRoutine and routineTimer.getTime() > 0:
            # get current time
            t = RestClock.getTime()
            frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
            # update/draw components on each frame
            
            
            # *Breather* updates
            if t >= 0.0 and Breather.status == NOT_STARTED:
                # keep track of start time/frame for later
                Breather.tStart = t  # underestimates by a little under one frame
                Breather.frameNStart = frameN  # exact frame index
                Breather.setAutoDraw(True)
            if Breather.status == STARTED and t >= (0.0 + (5-win.monitorFramePeriod*0.75)): #most of one frame period left
                Breather.setAutoDraw(False)
            
            # *plus* updates
            if t >= 5 and plus.status == NOT_STARTED:
                # keep track of start time/frame for later
                plus.tStart = t  # underestimates by a little under one frame
                plus.frameNStart = frameN  # exact frame index
                plus.setAutoDraw(True)
            if plus.status == STARTED and t >= (25-win.monitorFramePeriod*0.75): #most of one frame period left
                plus.setAutoDraw(False)
            
            # *readyPlus* updates
            if t >= 25 and readyPlus.status == NOT_STARTED:
                # keep track of start time/frame for later
                readyPlus.tStart = t  # underestimates by a little under one frame
                readyPlus.frameNStart = frameN  # exact frame index
                readyPlus.setAutoDraw(True)
            if readyPlus.status == STARTED and t >= (30-win.monitorFramePeriod*0.75): #most of one frame period left
                readyPlus.setAutoDraw(False)
            
            # check if all components have finished
            if not continueRoutine:  # a component has requested a forced-end of Routine
                routineTimer.reset()  # if we abort early the non-slip timer needs reset
                break
            continueRoutine = False  # will revert to True if at least one component still running
            for thisComponent in RestComponents:
                if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                    continueRoutine = True
                    break  # at least one component has not yet finished
            
            # check for quit (the Esc key)
            if endExpNow or event.getKeys(keyList=["escape"]):
                core.quit()
            
            # refresh the screen
            if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                win.flip()
        
        #-------Ending Routine "Rest"-------
        for thisComponent in RestComponents:
            if hasattr(thisComponent, "setAutoDraw"):
                thisComponent.setAutoDraw(False)
        BlockRTs = []
        print('Criteria for next block = ' + str(crit))
        thisExp.nextEntry()
        
    # completed 3 repeats of 'seq_block_run2'
    
    thisExp.nextEntry()
    
# completed 1 repeats of 'Run2'


# set up handler to look after randomisation of conditions etc
Run3 = data.TrialHandler(nReps=1, method='sequential', 
    extraInfo=expInfo, originPath=u'/Users/steelad/Desktop/Subj_fMRI_Grouped_timedRest_nocounter_framed/Adam_SRTT_Seq.ContPun_grouped.psyexp',
    trialList=[None],
    seed=None, name='Run3')
thisExp.addLoop(Run3)  # add the loop to the experiment
thisRun3 = Run3.trialList[0]  # so we can initialise stimuli with some values
# abbreviate parameter names if possible (e.g. rgb=thisRun3.rgb)
if thisRun3 != None:
    for paramName in thisRun3.keys():
        exec(paramName + '= thisRun3.' + paramName)

for thisRun3 in Run3:
    currentLoop = Run3
    # abbreviate parameter names if possible (e.g. rgb = thisRun3.rgb)
    if thisRun3 != None:
        for paramName in thisRun3.keys():
            exec(paramName + '= thisRun3.' + paramName)
    
    #------Prepare to start Routine "RunBreak"-------
    t = 0
    RunBreakClock.reset()  # clock 
    frameN = -1
    # update component parameters for each repeat
    phrase = str("Good job, you finished run %s.  \n \nTake a breather. \n \nYou have earned money" % (Run))
    
    RunBreakText.setText(phrase)
    SpacetoMoveOn = event.BuilderKeyResponse()  # create an object of type KeyResponse
    SpacetoMoveOn.status = NOT_STARTED
    # keep track of which components have finished
    RunBreakComponents = []
    RunBreakComponents.append(RunBreakText)
    RunBreakComponents.append(SpacetoMoveOn)
    RunBreakComponents.append(ExperimenterRole)
    for thisComponent in RunBreakComponents:
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
    
    #-------Start Routine "RunBreak"-------
    continueRoutine = True
    while continueRoutine:
        # get current time
        t = RunBreakClock.getTime()
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        
        
        # *RunBreakText* updates
        if t >= 0.0 and RunBreakText.status == NOT_STARTED:
            # keep track of start time/frame for later
            RunBreakText.tStart = t  # underestimates by a little under one frame
            RunBreakText.frameNStart = frameN  # exact frame index
            RunBreakText.setAutoDraw(True)
        
        # *SpacetoMoveOn* updates
        if t >= 0.0 and SpacetoMoveOn.status == NOT_STARTED:
            # keep track of start time/frame for later
            SpacetoMoveOn.tStart = t  # underestimates by a little under one frame
            SpacetoMoveOn.frameNStart = frameN  # exact frame index
            SpacetoMoveOn.status = STARTED
            # keyboard checking is just starting
            event.clearEvents(eventType='keyboard')
        if SpacetoMoveOn.status == STARTED:
            theseKeys = event.getKeys(keyList=['space'])
            
            # check for quit:
            if "escape" in theseKeys:
                endExpNow = True
            if len(theseKeys) > 0:  # at least one key was pressed
                # a response ends the routine
                continueRoutine = False
        
        # *ExperimenterRole* updates
        if t >= 0.0 and ExperimenterRole.status == NOT_STARTED:
            # keep track of start time/frame for later
            ExperimenterRole.tStart = t  # underestimates by a little under one frame
            ExperimenterRole.frameNStart = frameN  # exact frame index
            ExperimenterRole.setAutoDraw(True)
        
        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            routineTimer.reset()  # if we abort early the non-slip timer needs reset
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in RunBreakComponents:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # check for quit (the Esc key)
        if endExpNow or event.getKeys(keyList=["escape"]):
            core.quit()
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
        else:  # this Routine was not non-slip safe so reset non-slip timer
            routineTimer.reset()
    
    #-------Ending Routine "RunBreak"-------
    for thisComponent in RunBreakComponents:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    
    
    #------Prepare to start Routine "WaitforTrigger"-------
    t = 0
    WaitforTriggerClock.reset()  # clock 
    frameN = -1
    # update component parameters for each repeat
    TriggerIn = event.BuilderKeyResponse()  # create an object of type KeyResponse
    TriggerIn.status = NOT_STARTED
    # keep track of which components have finished
    WaitforTriggerComponents = []
    WaitforTriggerComponents.append(text_4)
    WaitforTriggerComponents.append(TriggerIn)
    for thisComponent in WaitforTriggerComponents:
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
    
    #-------Start Routine "WaitforTrigger"-------
    continueRoutine = True
    while continueRoutine:
        # get current time
        t = WaitforTriggerClock.getTime()
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        
        # *text_4* updates
        if t >= 0.0 and text_4.status == NOT_STARTED:
            # keep track of start time/frame for later
            text_4.tStart = t  # underestimates by a little under one frame
            text_4.frameNStart = frameN  # exact frame index
            text_4.setAutoDraw(True)
        
        # *TriggerIn* updates
        if t >= 0.0 and TriggerIn.status == NOT_STARTED:
            # keep track of start time/frame for later
            TriggerIn.tStart = t  # underestimates by a little under one frame
            TriggerIn.frameNStart = frameN  # exact frame index
            TriggerIn.status = STARTED
            # keyboard checking is just starting
            event.clearEvents(eventType='keyboard')
        if TriggerIn.status == STARTED:
            theseKeys = event.getKeys(keyList=['5'])
            
            # check for quit:
            if "escape" in theseKeys:
                endExpNow = True
            if len(theseKeys) > 0:  # at least one key was pressed
                # a response ends the routine
                continueRoutine = False
        
        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            routineTimer.reset()  # if we abort early the non-slip timer needs reset
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in WaitforTriggerComponents:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # check for quit (the Esc key)
        if endExpNow or event.getKeys(keyList=["escape"]):
            core.quit()
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
        else:  # this Routine was not non-slip safe so reset non-slip timer
            routineTimer.reset()
    
    #-------Ending Routine "WaitforTrigger"-------
    for thisComponent in WaitforTriggerComponents:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    
    #------Prepare to start Routine "BeginRun"-------
    t = 0
    BeginRunClock.reset()  # clock 
    frameN = -1
    routineTimer.add(12.000000)
    # update component parameters for each repeat
    
    # keep track of which components have finished
    BeginRunComponents = []
    BeginRunComponents.append(Plus)
    BeginRunComponents.append(Plus_ready)
    for thisComponent in BeginRunComponents:
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
    
    #-------Start Routine "BeginRun"-------
    continueRoutine = True
    while continueRoutine and routineTimer.getTime() > 0:
        # get current time
        t = BeginRunClock.getTime()
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        
        # *Plus* updates
        if t >= 0.0 and Plus.status == NOT_STARTED:
            # keep track of start time/frame for later
            Plus.tStart = t  # underestimates by a little under one frame
            Plus.frameNStart = frameN  # exact frame index
            Plus.setAutoDraw(True)
        if Plus.status == STARTED and t >= (7-win.monitorFramePeriod*0.75): #most of one frame period left
            Plus.setAutoDraw(False)
        
        # *Plus_ready* updates
        if t >= 7 and Plus_ready.status == NOT_STARTED:
            # keep track of start time/frame for later
            Plus_ready.tStart = t  # underestimates by a little under one frame
            Plus_ready.frameNStart = frameN  # exact frame index
            Plus_ready.setAutoDraw(True)
        if Plus_ready.status == STARTED and t >= (12-win.monitorFramePeriod*0.75): #most of one frame period left
            Plus_ready.setAutoDraw(False)
        
        
        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            routineTimer.reset()  # if we abort early the non-slip timer needs reset
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in BeginRunComponents:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # check for quit (the Esc key)
        if endExpNow or event.getKeys(keyList=["escape"]):
            core.quit()
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    #-------Ending Routine "BeginRun"-------
    for thisComponent in BeginRunComponents:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    Run = Run + 1
    
    # set up handler to look after randomisation of conditions etc
    seq_block_run3 = data.TrialHandler(nReps=3, method='sequential', 
        extraInfo=expInfo, originPath=u'/Users/steelad/Desktop/Subj_fMRI_Grouped_timedRest_nocounter_framed/Adam_SRTT_Seq.ContPun_grouped.psyexp',
        trialList=[None],
        seed=None, name='seq_block_run3')
    thisExp.addLoop(seq_block_run3)  # add the loop to the experiment
    thisSeq_block_run3 = seq_block_run3.trialList[0]  # so we can initialise stimuli with some values
    # abbreviate parameter names if possible (e.g. rgb=thisSeq_block_run3.rgb)
    if thisSeq_block_run3 != None:
        for paramName in thisSeq_block_run3.keys():
            exec(paramName + '= thisSeq_block_run3.' + paramName)
    
    for thisSeq_block_run3 in seq_block_run3:
        currentLoop = seq_block_run3
        # abbreviate parameter names if possible (e.g. rgb = thisSeq_block_run3.rgb)
        if thisSeq_block_run3 != None:
            for paramName in thisSeq_block_run3.keys():
                exec(paramName + '= thisSeq_block_run3.' + paramName)
        
        # set up handler to look after randomisation of conditions etc
        seq_trials3 = data.TrialHandler(nReps=1, method='sequential', 
            extraInfo=expInfo, originPath=u'/Users/steelad/Desktop/Subj_fMRI_Grouped_timedRest_nocounter_framed/Adam_SRTT_Seq.ContPun_grouped.psyexp',
            trialList=data.importConditions(seq_order_file),
            seed=None, name='seq_trials3')
        thisExp.addLoop(seq_trials3)  # add the loop to the experiment
        thisSeq_trials3 = seq_trials3.trialList[0]  # so we can initialise stimuli with some values
        # abbreviate parameter names if possible (e.g. rgb=thisSeq_trials3.rgb)
        if thisSeq_trials3 != None:
            for paramName in thisSeq_trials3.keys():
                exec(paramName + '= thisSeq_trials3.' + paramName)
        
        for thisSeq_trials3 in seq_trials3:
            currentLoop = seq_trials3
            # abbreviate parameter names if possible (e.g. rgb = thisSeq_trials3.rgb)
            if thisSeq_trials3 != None:
                for paramName in thisSeq_trials3.keys():
                    exec(paramName + '= thisSeq_trials3.' + paramName)
            
            #------Prepare to start Routine "trial"-------
            t = 0
            trialClock.reset()  # clock 
            frameN = -1
            routineTimer.add(0.800000)
            # update component parameters for each repeat
            Resp = event.BuilderKeyResponse()  # create an object of type KeyResponse
            Resp.status = NOT_STARTED
            #Init_rand.addData('Earnings Total', e_string)
            # keep track of which components have finished
            trialComponents = []
            trialComponents.append(FB_Seq_trial)
            trialComponents.append(Stimulus_appear)
            trialComponents.append(Resp)
            for thisComponent in trialComponents:
                if hasattr(thisComponent, 'status'):
                    thisComponent.status = NOT_STARTED
            
            #-------Start Routine "trial"-------
            continueRoutine = True
            while continueRoutine and routineTimer.getTime() > 0:
                # get current time
                t = trialClock.getTime()
                frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
                # update/draw components on each frame
                
                # *FB_Seq_trial* updates
                if t >= 0.0 and FB_Seq_trial.status == NOT_STARTED:
                    # keep track of start time/frame for later
                    FB_Seq_trial.tStart = t  # underestimates by a little under one frame
                    FB_Seq_trial.frameNStart = frameN  # exact frame index
                    FB_Seq_trial.setAutoDraw(True)
                if FB_Seq_trial.status == STARTED and t >= (0.0 + (0.8-win.monitorFramePeriod*0.75)): #most of one frame period left
                    FB_Seq_trial.setAutoDraw(False)
                
                # *Stimulus_appear* updates
                if t >= 0 and Stimulus_appear.status == NOT_STARTED:
                    # keep track of start time/frame for later
                    Stimulus_appear.tStart = t  # underestimates by a little under one frame
                    Stimulus_appear.frameNStart = frameN  # exact frame index
                    Stimulus_appear.setAutoDraw(True)
                if Stimulus_appear.status == STARTED and t >= (0.8-win.monitorFramePeriod*0.75): #most of one frame period left
                    Stimulus_appear.setAutoDraw(False)
                if Stimulus_appear.status == STARTED:  # only update if being drawn
                    Stimulus_appear.setText(Stimulus, log=False)
                
                # *Resp* updates
                if t >= 0 and Resp.status == NOT_STARTED:
                    # keep track of start time/frame for later
                    Resp.tStart = t  # underestimates by a little under one frame
                    Resp.frameNStart = frameN  # exact frame index
                    Resp.status = STARTED
                    # keyboard checking is just starting
                    Resp.clock.reset()  # now t=0
                    event.clearEvents(eventType='keyboard')
                if Resp.status == STARTED and t >= (0.8-win.monitorFramePeriod*0.75): #most of one frame period left
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
                
                
                # check if all components have finished
                if not continueRoutine:  # a component has requested a forced-end of Routine
                    routineTimer.reset()  # if we abort early the non-slip timer needs reset
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
            # store data for seq_trials3 (TrialHandler)
            seq_trials3.addData('Resp.keys',Resp.keys)
            seq_trials3.addData('Resp.corr', Resp.corr)
            if Resp.keys != None:  # we had a response
                seq_trials3.addData('Resp.rt', Resp.rt)
            
            
            #------Prepare to start Routine "Feedback_ISI"-------
            t = 0
            Feedback_ISIClock.reset()  # clock 
            frameN = -1
            routineTimer.add(0.200000)
            # update component parameters for each repeat
            if Resp.corr and Resp.rt < crit:
                BlockRTs.append(Resp.rt)
            
            
            Color = gen_fb(Feedback,fb_block,trial)
            
            if Resp.corr and Resp.rt < crit:
            #    Color = [0,1,0]
                Earning_Trial.append(1)
            #    earning = earning + 0.05
            #    e_string = str(earning)
            else:
            #    Color = [1,1,1]
                Earning_Trial.append(0)
            FB_seq.setLineColor(Color)
            # keep track of which components have finished
            Feedback_ISIComponents = []
            Feedback_ISIComponents.append(FB_seq)
            Feedback_ISIComponents.append(ISI)
            for thisComponent in Feedback_ISIComponents:
                if hasattr(thisComponent, 'status'):
                    thisComponent.status = NOT_STARTED
            
            #-------Start Routine "Feedback_ISI"-------
            continueRoutine = True
            while continueRoutine and routineTimer.getTime() > 0:
                # get current time
                t = Feedback_ISIClock.getTime()
                frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
                # update/draw components on each frame
                
                
                
                
                # *FB_seq* updates
                if t >= 0 and FB_seq.status == NOT_STARTED:
                    # keep track of start time/frame for later
                    FB_seq.tStart = t  # underestimates by a little under one frame
                    FB_seq.frameNStart = frameN  # exact frame index
                    FB_seq.setAutoDraw(True)
                if FB_seq.status == STARTED and t >= (0 + (.2-win.monitorFramePeriod*0.75)): #most of one frame period left
                    FB_seq.setAutoDraw(False)
                
                # *ISI* updates
                if t >= 0.0 and ISI.status == NOT_STARTED:
                    # keep track of start time/frame for later
                    ISI.tStart = t  # underestimates by a little under one frame
                    ISI.frameNStart = frameN  # exact frame index
                    ISI.setAutoDraw(True)
                if ISI.status == STARTED and t >= (0.0 + (.2-win.monitorFramePeriod*0.75)): #most of one frame period left
                    ISI.setAutoDraw(False)
                
                # check if all components have finished
                if not continueRoutine:  # a component has requested a forced-end of Routine
                    routineTimer.reset()  # if we abort early the non-slip timer needs reset
                    break
                continueRoutine = False  # will revert to True if at least one component still running
                for thisComponent in Feedback_ISIComponents:
                    if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                        continueRoutine = True
                        break  # at least one component has not yet finished
                
                # check for quit (the Esc key)
                if endExpNow or event.getKeys(keyList=["escape"]):
                    core.quit()
                
                # refresh the screen
                if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                    win.flip()
            
            #-------Ending Routine "Feedback_ISI"-------
            for thisComponent in Feedback_ISIComponents:
                if hasattr(thisComponent, "setAutoDraw"):
                    thisComponent.setAutoDraw(False)
            trial = trial + 1
            thisExp.nextEntry()
            
        # completed 1 repeats of 'seq_trials3'
        
        
        #------Prepare to start Routine "Rest"-------
        t = 0
        RestClock.reset()  # clock 
        frameN = -1
        routineTimer.add(30.000000)
        # update component parameters for each repeat
        vector = []
        count = 0
        Respvec = []
        other = []
        Keyvec = []
        trial = 0
        crit = Calc_Block_Criterion(BlockRTs,crit)
        
        makesequencestart(sequence)
        makerandom()
        
        breatherphrase = str("Good job, your earnings increased!\n\nYou finished block %s.  \n \nTake a breather. \n \n" % (block))
        block = block+1
        fb_block = block - 1
        Breather.setText(breatherphrase)
        # keep track of which components have finished
        RestComponents = []
        RestComponents.append(Breather)
        RestComponents.append(plus)
        RestComponents.append(readyPlus)
        for thisComponent in RestComponents:
            if hasattr(thisComponent, 'status'):
                thisComponent.status = NOT_STARTED
        
        #-------Start Routine "Rest"-------
        continueRoutine = True
        while continueRoutine and routineTimer.getTime() > 0:
            # get current time
            t = RestClock.getTime()
            frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
            # update/draw components on each frame
            
            
            # *Breather* updates
            if t >= 0.0 and Breather.status == NOT_STARTED:
                # keep track of start time/frame for later
                Breather.tStart = t  # underestimates by a little under one frame
                Breather.frameNStart = frameN  # exact frame index
                Breather.setAutoDraw(True)
            if Breather.status == STARTED and t >= (0.0 + (5-win.monitorFramePeriod*0.75)): #most of one frame period left
                Breather.setAutoDraw(False)
            
            # *plus* updates
            if t >= 5 and plus.status == NOT_STARTED:
                # keep track of start time/frame for later
                plus.tStart = t  # underestimates by a little under one frame
                plus.frameNStart = frameN  # exact frame index
                plus.setAutoDraw(True)
            if plus.status == STARTED and t >= (25-win.monitorFramePeriod*0.75): #most of one frame period left
                plus.setAutoDraw(False)
            
            # *readyPlus* updates
            if t >= 25 and readyPlus.status == NOT_STARTED:
                # keep track of start time/frame for later
                readyPlus.tStart = t  # underestimates by a little under one frame
                readyPlus.frameNStart = frameN  # exact frame index
                readyPlus.setAutoDraw(True)
            if readyPlus.status == STARTED and t >= (30-win.monitorFramePeriod*0.75): #most of one frame period left
                readyPlus.setAutoDraw(False)
            
            # check if all components have finished
            if not continueRoutine:  # a component has requested a forced-end of Routine
                routineTimer.reset()  # if we abort early the non-slip timer needs reset
                break
            continueRoutine = False  # will revert to True if at least one component still running
            for thisComponent in RestComponents:
                if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                    continueRoutine = True
                    break  # at least one component has not yet finished
            
            # check for quit (the Esc key)
            if endExpNow or event.getKeys(keyList=["escape"]):
                core.quit()
            
            # refresh the screen
            if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                win.flip()
        
        #-------Ending Routine "Rest"-------
        for thisComponent in RestComponents:
            if hasattr(thisComponent, "setAutoDraw"):
                thisComponent.setAutoDraw(False)
        BlockRTs = []
        print('Criteria for next block = ' + str(crit))
        thisExp.nextEntry()
        
    # completed 3 repeats of 'seq_block_run3'
    
    thisExp.nextEntry()
    
# completed 1 repeats of 'Run3'


# set up handler to look after randomisation of conditions etc
Run4 = data.TrialHandler(nReps=1, method='sequential', 
    extraInfo=expInfo, originPath=u'/Users/steelad/Desktop/Subj_fMRI_Grouped_timedRest_nocounter_framed/Adam_SRTT_Seq.ContPun_grouped.psyexp',
    trialList=[None],
    seed=None, name='Run4')
thisExp.addLoop(Run4)  # add the loop to the experiment
thisRun4 = Run4.trialList[0]  # so we can initialise stimuli with some values
# abbreviate parameter names if possible (e.g. rgb=thisRun4.rgb)
if thisRun4 != None:
    for paramName in thisRun4.keys():
        exec(paramName + '= thisRun4.' + paramName)

for thisRun4 in Run4:
    currentLoop = Run4
    # abbreviate parameter names if possible (e.g. rgb = thisRun4.rgb)
    if thisRun4 != None:
        for paramName in thisRun4.keys():
            exec(paramName + '= thisRun4.' + paramName)
    
    #------Prepare to start Routine "RunBreak"-------
    t = 0
    RunBreakClock.reset()  # clock 
    frameN = -1
    # update component parameters for each repeat
    phrase = str("Good job, you finished run %s.  \n \nTake a breather. \n \nYou have earned money" % (Run))
    
    RunBreakText.setText(phrase)
    SpacetoMoveOn = event.BuilderKeyResponse()  # create an object of type KeyResponse
    SpacetoMoveOn.status = NOT_STARTED
    # keep track of which components have finished
    RunBreakComponents = []
    RunBreakComponents.append(RunBreakText)
    RunBreakComponents.append(SpacetoMoveOn)
    RunBreakComponents.append(ExperimenterRole)
    for thisComponent in RunBreakComponents:
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
    
    #-------Start Routine "RunBreak"-------
    continueRoutine = True
    while continueRoutine:
        # get current time
        t = RunBreakClock.getTime()
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        
        
        # *RunBreakText* updates
        if t >= 0.0 and RunBreakText.status == NOT_STARTED:
            # keep track of start time/frame for later
            RunBreakText.tStart = t  # underestimates by a little under one frame
            RunBreakText.frameNStart = frameN  # exact frame index
            RunBreakText.setAutoDraw(True)
        
        # *SpacetoMoveOn* updates
        if t >= 0.0 and SpacetoMoveOn.status == NOT_STARTED:
            # keep track of start time/frame for later
            SpacetoMoveOn.tStart = t  # underestimates by a little under one frame
            SpacetoMoveOn.frameNStart = frameN  # exact frame index
            SpacetoMoveOn.status = STARTED
            # keyboard checking is just starting
            event.clearEvents(eventType='keyboard')
        if SpacetoMoveOn.status == STARTED:
            theseKeys = event.getKeys(keyList=['space'])
            
            # check for quit:
            if "escape" in theseKeys:
                endExpNow = True
            if len(theseKeys) > 0:  # at least one key was pressed
                # a response ends the routine
                continueRoutine = False
        
        # *ExperimenterRole* updates
        if t >= 0.0 and ExperimenterRole.status == NOT_STARTED:
            # keep track of start time/frame for later
            ExperimenterRole.tStart = t  # underestimates by a little under one frame
            ExperimenterRole.frameNStart = frameN  # exact frame index
            ExperimenterRole.setAutoDraw(True)
        
        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            routineTimer.reset()  # if we abort early the non-slip timer needs reset
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in RunBreakComponents:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # check for quit (the Esc key)
        if endExpNow or event.getKeys(keyList=["escape"]):
            core.quit()
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
        else:  # this Routine was not non-slip safe so reset non-slip timer
            routineTimer.reset()
    
    #-------Ending Routine "RunBreak"-------
    for thisComponent in RunBreakComponents:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    
    
    #------Prepare to start Routine "WaitforTrigger"-------
    t = 0
    WaitforTriggerClock.reset()  # clock 
    frameN = -1
    # update component parameters for each repeat
    TriggerIn = event.BuilderKeyResponse()  # create an object of type KeyResponse
    TriggerIn.status = NOT_STARTED
    # keep track of which components have finished
    WaitforTriggerComponents = []
    WaitforTriggerComponents.append(text_4)
    WaitforTriggerComponents.append(TriggerIn)
    for thisComponent in WaitforTriggerComponents:
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
    
    #-------Start Routine "WaitforTrigger"-------
    continueRoutine = True
    while continueRoutine:
        # get current time
        t = WaitforTriggerClock.getTime()
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        
        # *text_4* updates
        if t >= 0.0 and text_4.status == NOT_STARTED:
            # keep track of start time/frame for later
            text_4.tStart = t  # underestimates by a little under one frame
            text_4.frameNStart = frameN  # exact frame index
            text_4.setAutoDraw(True)
        
        # *TriggerIn* updates
        if t >= 0.0 and TriggerIn.status == NOT_STARTED:
            # keep track of start time/frame for later
            TriggerIn.tStart = t  # underestimates by a little under one frame
            TriggerIn.frameNStart = frameN  # exact frame index
            TriggerIn.status = STARTED
            # keyboard checking is just starting
            event.clearEvents(eventType='keyboard')
        if TriggerIn.status == STARTED:
            theseKeys = event.getKeys(keyList=['5'])
            
            # check for quit:
            if "escape" in theseKeys:
                endExpNow = True
            if len(theseKeys) > 0:  # at least one key was pressed
                # a response ends the routine
                continueRoutine = False
        
        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            routineTimer.reset()  # if we abort early the non-slip timer needs reset
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in WaitforTriggerComponents:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # check for quit (the Esc key)
        if endExpNow or event.getKeys(keyList=["escape"]):
            core.quit()
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
        else:  # this Routine was not non-slip safe so reset non-slip timer
            routineTimer.reset()
    
    #-------Ending Routine "WaitforTrigger"-------
    for thisComponent in WaitforTriggerComponents:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    
    #------Prepare to start Routine "BeginRun"-------
    t = 0
    BeginRunClock.reset()  # clock 
    frameN = -1
    routineTimer.add(12.000000)
    # update component parameters for each repeat
    
    # keep track of which components have finished
    BeginRunComponents = []
    BeginRunComponents.append(Plus)
    BeginRunComponents.append(Plus_ready)
    for thisComponent in BeginRunComponents:
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
    
    #-------Start Routine "BeginRun"-------
    continueRoutine = True
    while continueRoutine and routineTimer.getTime() > 0:
        # get current time
        t = BeginRunClock.getTime()
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        
        # *Plus* updates
        if t >= 0.0 and Plus.status == NOT_STARTED:
            # keep track of start time/frame for later
            Plus.tStart = t  # underestimates by a little under one frame
            Plus.frameNStart = frameN  # exact frame index
            Plus.setAutoDraw(True)
        if Plus.status == STARTED and t >= (7-win.monitorFramePeriod*0.75): #most of one frame period left
            Plus.setAutoDraw(False)
        
        # *Plus_ready* updates
        if t >= 7 and Plus_ready.status == NOT_STARTED:
            # keep track of start time/frame for later
            Plus_ready.tStart = t  # underestimates by a little under one frame
            Plus_ready.frameNStart = frameN  # exact frame index
            Plus_ready.setAutoDraw(True)
        if Plus_ready.status == STARTED and t >= (12-win.monitorFramePeriod*0.75): #most of one frame period left
            Plus_ready.setAutoDraw(False)
        
        
        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            routineTimer.reset()  # if we abort early the non-slip timer needs reset
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in BeginRunComponents:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # check for quit (the Esc key)
        if endExpNow or event.getKeys(keyList=["escape"]):
            core.quit()
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    #-------Ending Routine "BeginRun"-------
    for thisComponent in BeginRunComponents:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    Run = Run + 1
    
    # set up handler to look after randomisation of conditions etc
    rand_block = data.TrialHandler(nReps=1, method='sequential', 
        extraInfo=expInfo, originPath=u'/Users/steelad/Desktop/Subj_fMRI_Grouped_timedRest_nocounter_framed/Adam_SRTT_Seq.ContPun_grouped.psyexp',
        trialList=data.importConditions('RandOrder.csv'),
        seed=None, name='rand_block')
    thisExp.addLoop(rand_block)  # add the loop to the experiment
    thisRand_block = rand_block.trialList[0]  # so we can initialise stimuli with some values
    # abbreviate parameter names if possible (e.g. rgb=thisRand_block.rgb)
    if thisRand_block != None:
        for paramName in thisRand_block.keys():
            exec(paramName + '= thisRand_block.' + paramName)
    
    for thisRand_block in rand_block:
        currentLoop = rand_block
        # abbreviate parameter names if possible (e.g. rgb = thisRand_block.rgb)
        if thisRand_block != None:
            for paramName in thisRand_block.keys():
                exec(paramName + '= thisRand_block.' + paramName)
        
        #------Prepare to start Routine "RandBlock"-------
        t = 0
        RandBlockClock.reset()  # clock 
        frameN = -1
        routineTimer.add(0.800000)
        # update component parameters for each repeat
        
        Stimulus_rand.setText(RandStim)
        RandResp = event.BuilderKeyResponse()  # create an object of type KeyResponse
        RandResp.status = NOT_STARTED
        # keep track of which components have finished
        RandBlockComponents = []
        RandBlockComponents.append(RandFB_trial)
        RandBlockComponents.append(Stimulus_rand)
        RandBlockComponents.append(RandResp)
        for thisComponent in RandBlockComponents:
            if hasattr(thisComponent, 'status'):
                thisComponent.status = NOT_STARTED
        
        #-------Start Routine "RandBlock"-------
        continueRoutine = True
        while continueRoutine and routineTimer.getTime() > 0:
            # get current time
            t = RandBlockClock.getTime()
            frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
            # update/draw components on each frame
            
            
            # *RandFB_trial* updates
            if t >= 0.0 and RandFB_trial.status == NOT_STARTED:
                # keep track of start time/frame for later
                RandFB_trial.tStart = t  # underestimates by a little under one frame
                RandFB_trial.frameNStart = frameN  # exact frame index
                RandFB_trial.setAutoDraw(True)
            if RandFB_trial.status == STARTED and t >= (0.0 + (0.8-win.monitorFramePeriod*0.75)): #most of one frame period left
                RandFB_trial.setAutoDraw(False)
            
            # *Stimulus_rand* updates
            if t >= 0.0 and Stimulus_rand.status == NOT_STARTED:
                # keep track of start time/frame for later
                Stimulus_rand.tStart = t  # underestimates by a little under one frame
                Stimulus_rand.frameNStart = frameN  # exact frame index
                Stimulus_rand.setAutoDraw(True)
            if Stimulus_rand.status == STARTED and t >= (0.8-win.monitorFramePeriod*0.75): #most of one frame period left
                Stimulus_rand.setAutoDraw(False)
            
            # *RandResp* updates
            if t >= 0 and RandResp.status == NOT_STARTED:
                # keep track of start time/frame for later
                RandResp.tStart = t  # underestimates by a little under one frame
                RandResp.frameNStart = frameN  # exact frame index
                RandResp.status = STARTED
                # keyboard checking is just starting
                RandResp.clock.reset()  # now t=0
                event.clearEvents(eventType='keyboard')
            if RandResp.status == STARTED and t >= (0.8-win.monitorFramePeriod*0.75): #most of one frame period left
                RandResp.status = STOPPED
            if RandResp.status == STARTED:
                theseKeys = event.getKeys(keyList=['1', '2', '3', '4'])
                
                # check for quit:
                if "escape" in theseKeys:
                    endExpNow = True
                if len(theseKeys) > 0:  # at least one key was pressed
                    if RandResp.keys == []:  # then this was the first keypress
                        RandResp.keys = theseKeys[0]  # just the first key pressed
                        RandResp.rt = RandResp.clock.getTime()
                        # was this 'correct'?
                        if (RandResp.keys == str(RandomResp)) or (RandResp.keys == RandomResp):
                            RandResp.corr = 1
                        else:
                            RandResp.corr = 0
            
            # check if all components have finished
            if not continueRoutine:  # a component has requested a forced-end of Routine
                routineTimer.reset()  # if we abort early the non-slip timer needs reset
                break
            continueRoutine = False  # will revert to True if at least one component still running
            for thisComponent in RandBlockComponents:
                if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                    continueRoutine = True
                    break  # at least one component has not yet finished
            
            # check for quit (the Esc key)
            if endExpNow or event.getKeys(keyList=["escape"]):
                core.quit()
            
            # refresh the screen
            if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                win.flip()
        
        #-------Ending Routine "RandBlock"-------
        for thisComponent in RandBlockComponents:
            if hasattr(thisComponent, "setAutoDraw"):
                thisComponent.setAutoDraw(False)
        
        # check responses
        if RandResp.keys in ['', [], None]:  # No response was made
           RandResp.keys=None
           # was no response the correct answer?!
           if str(RandomResp).lower() == 'none': RandResp.corr = 1  # correct non-response
           else: RandResp.corr = 0  # failed to respond (incorrectly)
        # store data for rand_block (TrialHandler)
        rand_block.addData('RandResp.keys',RandResp.keys)
        rand_block.addData('RandResp.corr', RandResp.corr)
        if RandResp.keys != None:  # we had a response
            rand_block.addData('RandResp.rt', RandResp.rt)
        
        #------Prepare to start Routine "RandFeedback"-------
        t = 0
        RandFeedbackClock.reset()  # clock 
        frameN = -1
        routineTimer.add(0.200000)
        # update component parameters for each repeat
        if RandResp.corr:
            BlockRTs.append(RandResp.rt)
        Color = gen_fb(Feedback,fb_block,trial)
        if RandResp.corr and RandResp.rt < crit:
        #    Color = [0,1,0]
            Earning_Trial.append(1)
        #    earning = earning + 0.05
        #    e_string = str(earning)
        else:
        #    Color = [1,1,1]
            Earning_Trial.append(0)
        FB_Rand.setFillColor([0,0,0])
        FB_Rand.setLineColor(Color)
        # keep track of which components have finished
        RandFeedbackComponents = []
        RandFeedbackComponents.append(FB_Rand)
        RandFeedbackComponents.append(ISI_rand)
        for thisComponent in RandFeedbackComponents:
            if hasattr(thisComponent, 'status'):
                thisComponent.status = NOT_STARTED
        
        #-------Start Routine "RandFeedback"-------
        continueRoutine = True
        while continueRoutine and routineTimer.getTime() > 0:
            # get current time
            t = RandFeedbackClock.getTime()
            frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
            # update/draw components on each frame
            
            
            # *FB_Rand* updates
            if t >= 0.0 and FB_Rand.status == NOT_STARTED:
                # keep track of start time/frame for later
                FB_Rand.tStart = t  # underestimates by a little under one frame
                FB_Rand.frameNStart = frameN  # exact frame index
                FB_Rand.setAutoDraw(True)
            if FB_Rand.status == STARTED and t >= (0.0 + (0.2-win.monitorFramePeriod*0.75)): #most of one frame period left
                FB_Rand.setAutoDraw(False)
            
            # *ISI_rand* updates
            if t >= 0.0 and ISI_rand.status == NOT_STARTED:
                # keep track of start time/frame for later
                ISI_rand.tStart = t  # underestimates by a little under one frame
                ISI_rand.frameNStart = frameN  # exact frame index
                ISI_rand.setAutoDraw(True)
            if ISI_rand.status == STARTED and t >= (0.0 + (.2-win.monitorFramePeriod*0.75)): #most of one frame period left
                ISI_rand.setAutoDraw(False)
            
            # check if all components have finished
            if not continueRoutine:  # a component has requested a forced-end of Routine
                routineTimer.reset()  # if we abort early the non-slip timer needs reset
                break
            continueRoutine = False  # will revert to True if at least one component still running
            for thisComponent in RandFeedbackComponents:
                if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                    continueRoutine = True
                    break  # at least one component has not yet finished
            
            # check for quit (the Esc key)
            if endExpNow or event.getKeys(keyList=["escape"]):
                core.quit()
            
            # refresh the screen
            if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                win.flip()
        
        #-------Ending Routine "RandFeedback"-------
        for thisComponent in RandFeedbackComponents:
            if hasattr(thisComponent, "setAutoDraw"):
                thisComponent.setAutoDraw(False)
        trial = trial + 1
        thisExp.nextEntry()
        
    # completed 1 repeats of 'rand_block'
    
    
    #------Prepare to start Routine "Rest"-------
    t = 0
    RestClock.reset()  # clock 
    frameN = -1
    routineTimer.add(30.000000)
    # update component parameters for each repeat
    vector = []
    count = 0
    Respvec = []
    other = []
    Keyvec = []
    trial = 0
    crit = Calc_Block_Criterion(BlockRTs,crit)
    
    makesequencestart(sequence)
    makerandom()
    
    breatherphrase = str("Good job, your earnings increased!\n\nYou finished block %s.  \n \nTake a breather. \n \n" % (block))
    block = block+1
    fb_block = block - 1
    Breather.setText(breatherphrase)
    # keep track of which components have finished
    RestComponents = []
    RestComponents.append(Breather)
    RestComponents.append(plus)
    RestComponents.append(readyPlus)
    for thisComponent in RestComponents:
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
    
    #-------Start Routine "Rest"-------
    continueRoutine = True
    while continueRoutine and routineTimer.getTime() > 0:
        # get current time
        t = RestClock.getTime()
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        
        
        # *Breather* updates
        if t >= 0.0 and Breather.status == NOT_STARTED:
            # keep track of start time/frame for later
            Breather.tStart = t  # underestimates by a little under one frame
            Breather.frameNStart = frameN  # exact frame index
            Breather.setAutoDraw(True)
        if Breather.status == STARTED and t >= (0.0 + (5-win.monitorFramePeriod*0.75)): #most of one frame period left
            Breather.setAutoDraw(False)
        
        # *plus* updates
        if t >= 5 and plus.status == NOT_STARTED:
            # keep track of start time/frame for later
            plus.tStart = t  # underestimates by a little under one frame
            plus.frameNStart = frameN  # exact frame index
            plus.setAutoDraw(True)
        if plus.status == STARTED and t >= (25-win.monitorFramePeriod*0.75): #most of one frame period left
            plus.setAutoDraw(False)
        
        # *readyPlus* updates
        if t >= 25 and readyPlus.status == NOT_STARTED:
            # keep track of start time/frame for later
            readyPlus.tStart = t  # underestimates by a little under one frame
            readyPlus.frameNStart = frameN  # exact frame index
            readyPlus.setAutoDraw(True)
        if readyPlus.status == STARTED and t >= (30-win.monitorFramePeriod*0.75): #most of one frame period left
            readyPlus.setAutoDraw(False)
        
        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            routineTimer.reset()  # if we abort early the non-slip timer needs reset
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in RestComponents:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # check for quit (the Esc key)
        if endExpNow or event.getKeys(keyList=["escape"]):
            core.quit()
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    #-------Ending Routine "Rest"-------
    for thisComponent in RestComponents:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    BlockRTs = []
    print('Criteria for next block = ' + str(crit))
    
    # set up handler to look after randomisation of conditions etc
    testseq = data.TrialHandler(nReps=1, method='sequential', 
        extraInfo=expInfo, originPath=u'/Users/steelad/Desktop/Subj_fMRI_Grouped_timedRest_nocounter_framed/Adam_SRTT_Seq.ContPun_grouped.psyexp',
        trialList=data.importConditions(seq_order_file),
        seed=None, name='testseq')
    thisExp.addLoop(testseq)  # add the loop to the experiment
    thisTestseq = testseq.trialList[0]  # so we can initialise stimuli with some values
    # abbreviate parameter names if possible (e.g. rgb=thisTestseq.rgb)
    if thisTestseq != None:
        for paramName in thisTestseq.keys():
            exec(paramName + '= thisTestseq.' + paramName)
    
    for thisTestseq in testseq:
        currentLoop = testseq
        # abbreviate parameter names if possible (e.g. rgb = thisTestseq.rgb)
        if thisTestseq != None:
            for paramName in thisTestseq.keys():
                exec(paramName + '= thisTestseq.' + paramName)
        
        #------Prepare to start Routine "trial"-------
        t = 0
        trialClock.reset()  # clock 
        frameN = -1
        routineTimer.add(0.800000)
        # update component parameters for each repeat
        Resp = event.BuilderKeyResponse()  # create an object of type KeyResponse
        Resp.status = NOT_STARTED
        #Init_rand.addData('Earnings Total', e_string)
        # keep track of which components have finished
        trialComponents = []
        trialComponents.append(FB_Seq_trial)
        trialComponents.append(Stimulus_appear)
        trialComponents.append(Resp)
        for thisComponent in trialComponents:
            if hasattr(thisComponent, 'status'):
                thisComponent.status = NOT_STARTED
        
        #-------Start Routine "trial"-------
        continueRoutine = True
        while continueRoutine and routineTimer.getTime() > 0:
            # get current time
            t = trialClock.getTime()
            frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
            # update/draw components on each frame
            
            # *FB_Seq_trial* updates
            if t >= 0.0 and FB_Seq_trial.status == NOT_STARTED:
                # keep track of start time/frame for later
                FB_Seq_trial.tStart = t  # underestimates by a little under one frame
                FB_Seq_trial.frameNStart = frameN  # exact frame index
                FB_Seq_trial.setAutoDraw(True)
            if FB_Seq_trial.status == STARTED and t >= (0.0 + (0.8-win.monitorFramePeriod*0.75)): #most of one frame period left
                FB_Seq_trial.setAutoDraw(False)
            
            # *Stimulus_appear* updates
            if t >= 0 and Stimulus_appear.status == NOT_STARTED:
                # keep track of start time/frame for later
                Stimulus_appear.tStart = t  # underestimates by a little under one frame
                Stimulus_appear.frameNStart = frameN  # exact frame index
                Stimulus_appear.setAutoDraw(True)
            if Stimulus_appear.status == STARTED and t >= (0.8-win.monitorFramePeriod*0.75): #most of one frame period left
                Stimulus_appear.setAutoDraw(False)
            if Stimulus_appear.status == STARTED:  # only update if being drawn
                Stimulus_appear.setText(Stimulus, log=False)
            
            # *Resp* updates
            if t >= 0 and Resp.status == NOT_STARTED:
                # keep track of start time/frame for later
                Resp.tStart = t  # underestimates by a little under one frame
                Resp.frameNStart = frameN  # exact frame index
                Resp.status = STARTED
                # keyboard checking is just starting
                Resp.clock.reset()  # now t=0
                event.clearEvents(eventType='keyboard')
            if Resp.status == STARTED and t >= (0.8-win.monitorFramePeriod*0.75): #most of one frame period left
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
            
            
            # check if all components have finished
            if not continueRoutine:  # a component has requested a forced-end of Routine
                routineTimer.reset()  # if we abort early the non-slip timer needs reset
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
        # store data for testseq (TrialHandler)
        testseq.addData('Resp.keys',Resp.keys)
        testseq.addData('Resp.corr', Resp.corr)
        if Resp.keys != None:  # we had a response
            testseq.addData('Resp.rt', Resp.rt)
        
        
        #------Prepare to start Routine "Feedback_ISI"-------
        t = 0
        Feedback_ISIClock.reset()  # clock 
        frameN = -1
        routineTimer.add(0.200000)
        # update component parameters for each repeat
        if Resp.corr and Resp.rt < crit:
            BlockRTs.append(Resp.rt)
        
        
        Color = gen_fb(Feedback,fb_block,trial)
        
        if Resp.corr and Resp.rt < crit:
        #    Color = [0,1,0]
            Earning_Trial.append(1)
        #    earning = earning + 0.05
        #    e_string = str(earning)
        else:
        #    Color = [1,1,1]
            Earning_Trial.append(0)
        FB_seq.setLineColor(Color)
        # keep track of which components have finished
        Feedback_ISIComponents = []
        Feedback_ISIComponents.append(FB_seq)
        Feedback_ISIComponents.append(ISI)
        for thisComponent in Feedback_ISIComponents:
            if hasattr(thisComponent, 'status'):
                thisComponent.status = NOT_STARTED
        
        #-------Start Routine "Feedback_ISI"-------
        continueRoutine = True
        while continueRoutine and routineTimer.getTime() > 0:
            # get current time
            t = Feedback_ISIClock.getTime()
            frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
            # update/draw components on each frame
            
            
            
            
            # *FB_seq* updates
            if t >= 0 and FB_seq.status == NOT_STARTED:
                # keep track of start time/frame for later
                FB_seq.tStart = t  # underestimates by a little under one frame
                FB_seq.frameNStart = frameN  # exact frame index
                FB_seq.setAutoDraw(True)
            if FB_seq.status == STARTED and t >= (0 + (.2-win.monitorFramePeriod*0.75)): #most of one frame period left
                FB_seq.setAutoDraw(False)
            
            # *ISI* updates
            if t >= 0.0 and ISI.status == NOT_STARTED:
                # keep track of start time/frame for later
                ISI.tStart = t  # underestimates by a little under one frame
                ISI.frameNStart = frameN  # exact frame index
                ISI.setAutoDraw(True)
            if ISI.status == STARTED and t >= (0.0 + (.2-win.monitorFramePeriod*0.75)): #most of one frame period left
                ISI.setAutoDraw(False)
            
            # check if all components have finished
            if not continueRoutine:  # a component has requested a forced-end of Routine
                routineTimer.reset()  # if we abort early the non-slip timer needs reset
                break
            continueRoutine = False  # will revert to True if at least one component still running
            for thisComponent in Feedback_ISIComponents:
                if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                    continueRoutine = True
                    break  # at least one component has not yet finished
            
            # check for quit (the Esc key)
            if endExpNow or event.getKeys(keyList=["escape"]):
                core.quit()
            
            # refresh the screen
            if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                win.flip()
        
        #-------Ending Routine "Feedback_ISI"-------
        for thisComponent in Feedback_ISIComponents:
            if hasattr(thisComponent, "setAutoDraw"):
                thisComponent.setAutoDraw(False)
        trial = trial + 1
        thisExp.nextEntry()
        
    # completed 1 repeats of 'testseq'
    
    
    #------Prepare to start Routine "Rest"-------
    t = 0
    RestClock.reset()  # clock 
    frameN = -1
    routineTimer.add(30.000000)
    # update component parameters for each repeat
    vector = []
    count = 0
    Respvec = []
    other = []
    Keyvec = []
    trial = 0
    crit = Calc_Block_Criterion(BlockRTs,crit)
    
    makesequencestart(sequence)
    makerandom()
    
    breatherphrase = str("Good job, your earnings increased!\n\nYou finished block %s.  \n \nTake a breather. \n \n" % (block))
    block = block+1
    fb_block = block - 1
    Breather.setText(breatherphrase)
    # keep track of which components have finished
    RestComponents = []
    RestComponents.append(Breather)
    RestComponents.append(plus)
    RestComponents.append(readyPlus)
    for thisComponent in RestComponents:
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
    
    #-------Start Routine "Rest"-------
    continueRoutine = True
    while continueRoutine and routineTimer.getTime() > 0:
        # get current time
        t = RestClock.getTime()
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        
        
        # *Breather* updates
        if t >= 0.0 and Breather.status == NOT_STARTED:
            # keep track of start time/frame for later
            Breather.tStart = t  # underestimates by a little under one frame
            Breather.frameNStart = frameN  # exact frame index
            Breather.setAutoDraw(True)
        if Breather.status == STARTED and t >= (0.0 + (5-win.monitorFramePeriod*0.75)): #most of one frame period left
            Breather.setAutoDraw(False)
        
        # *plus* updates
        if t >= 5 and plus.status == NOT_STARTED:
            # keep track of start time/frame for later
            plus.tStart = t  # underestimates by a little under one frame
            plus.frameNStart = frameN  # exact frame index
            plus.setAutoDraw(True)
        if plus.status == STARTED and t >= (25-win.monitorFramePeriod*0.75): #most of one frame period left
            plus.setAutoDraw(False)
        
        # *readyPlus* updates
        if t >= 25 and readyPlus.status == NOT_STARTED:
            # keep track of start time/frame for later
            readyPlus.tStart = t  # underestimates by a little under one frame
            readyPlus.frameNStart = frameN  # exact frame index
            readyPlus.setAutoDraw(True)
        if readyPlus.status == STARTED and t >= (30-win.monitorFramePeriod*0.75): #most of one frame period left
            readyPlus.setAutoDraw(False)
        
        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            routineTimer.reset()  # if we abort early the non-slip timer needs reset
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in RestComponents:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # check for quit (the Esc key)
        if endExpNow or event.getKeys(keyList=["escape"]):
            core.quit()
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    #-------Ending Routine "Rest"-------
    for thisComponent in RestComponents:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    BlockRTs = []
    print('Criteria for next block = ' + str(crit))
    
    # set up handler to look after randomisation of conditions etc
    rand_block2 = data.TrialHandler(nReps=1, method='sequential', 
        extraInfo=expInfo, originPath=u'/Users/steelad/Desktop/Subj_fMRI_Grouped_timedRest_nocounter_framed/Adam_SRTT_Seq.ContPun_grouped.psyexp',
        trialList=data.importConditions('RandOrder.csv'),
        seed=None, name='rand_block2')
    thisExp.addLoop(rand_block2)  # add the loop to the experiment
    thisRand_block2 = rand_block2.trialList[0]  # so we can initialise stimuli with some values
    # abbreviate parameter names if possible (e.g. rgb=thisRand_block2.rgb)
    if thisRand_block2 != None:
        for paramName in thisRand_block2.keys():
            exec(paramName + '= thisRand_block2.' + paramName)
    
    for thisRand_block2 in rand_block2:
        currentLoop = rand_block2
        # abbreviate parameter names if possible (e.g. rgb = thisRand_block2.rgb)
        if thisRand_block2 != None:
            for paramName in thisRand_block2.keys():
                exec(paramName + '= thisRand_block2.' + paramName)
        
        #------Prepare to start Routine "RandBlock"-------
        t = 0
        RandBlockClock.reset()  # clock 
        frameN = -1
        routineTimer.add(0.800000)
        # update component parameters for each repeat
        
        Stimulus_rand.setText(RandStim)
        RandResp = event.BuilderKeyResponse()  # create an object of type KeyResponse
        RandResp.status = NOT_STARTED
        # keep track of which components have finished
        RandBlockComponents = []
        RandBlockComponents.append(RandFB_trial)
        RandBlockComponents.append(Stimulus_rand)
        RandBlockComponents.append(RandResp)
        for thisComponent in RandBlockComponents:
            if hasattr(thisComponent, 'status'):
                thisComponent.status = NOT_STARTED
        
        #-------Start Routine "RandBlock"-------
        continueRoutine = True
        while continueRoutine and routineTimer.getTime() > 0:
            # get current time
            t = RandBlockClock.getTime()
            frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
            # update/draw components on each frame
            
            
            # *RandFB_trial* updates
            if t >= 0.0 and RandFB_trial.status == NOT_STARTED:
                # keep track of start time/frame for later
                RandFB_trial.tStart = t  # underestimates by a little under one frame
                RandFB_trial.frameNStart = frameN  # exact frame index
                RandFB_trial.setAutoDraw(True)
            if RandFB_trial.status == STARTED and t >= (0.0 + (0.8-win.monitorFramePeriod*0.75)): #most of one frame period left
                RandFB_trial.setAutoDraw(False)
            
            # *Stimulus_rand* updates
            if t >= 0.0 and Stimulus_rand.status == NOT_STARTED:
                # keep track of start time/frame for later
                Stimulus_rand.tStart = t  # underestimates by a little under one frame
                Stimulus_rand.frameNStart = frameN  # exact frame index
                Stimulus_rand.setAutoDraw(True)
            if Stimulus_rand.status == STARTED and t >= (0.8-win.monitorFramePeriod*0.75): #most of one frame period left
                Stimulus_rand.setAutoDraw(False)
            
            # *RandResp* updates
            if t >= 0 and RandResp.status == NOT_STARTED:
                # keep track of start time/frame for later
                RandResp.tStart = t  # underestimates by a little under one frame
                RandResp.frameNStart = frameN  # exact frame index
                RandResp.status = STARTED
                # keyboard checking is just starting
                RandResp.clock.reset()  # now t=0
                event.clearEvents(eventType='keyboard')
            if RandResp.status == STARTED and t >= (0.8-win.monitorFramePeriod*0.75): #most of one frame period left
                RandResp.status = STOPPED
            if RandResp.status == STARTED:
                theseKeys = event.getKeys(keyList=['1', '2', '3', '4'])
                
                # check for quit:
                if "escape" in theseKeys:
                    endExpNow = True
                if len(theseKeys) > 0:  # at least one key was pressed
                    if RandResp.keys == []:  # then this was the first keypress
                        RandResp.keys = theseKeys[0]  # just the first key pressed
                        RandResp.rt = RandResp.clock.getTime()
                        # was this 'correct'?
                        if (RandResp.keys == str(RandomResp)) or (RandResp.keys == RandomResp):
                            RandResp.corr = 1
                        else:
                            RandResp.corr = 0
            
            # check if all components have finished
            if not continueRoutine:  # a component has requested a forced-end of Routine
                routineTimer.reset()  # if we abort early the non-slip timer needs reset
                break
            continueRoutine = False  # will revert to True if at least one component still running
            for thisComponent in RandBlockComponents:
                if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                    continueRoutine = True
                    break  # at least one component has not yet finished
            
            # check for quit (the Esc key)
            if endExpNow or event.getKeys(keyList=["escape"]):
                core.quit()
            
            # refresh the screen
            if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                win.flip()
        
        #-------Ending Routine "RandBlock"-------
        for thisComponent in RandBlockComponents:
            if hasattr(thisComponent, "setAutoDraw"):
                thisComponent.setAutoDraw(False)
        
        # check responses
        if RandResp.keys in ['', [], None]:  # No response was made
           RandResp.keys=None
           # was no response the correct answer?!
           if str(RandomResp).lower() == 'none': RandResp.corr = 1  # correct non-response
           else: RandResp.corr = 0  # failed to respond (incorrectly)
        # store data for rand_block2 (TrialHandler)
        rand_block2.addData('RandResp.keys',RandResp.keys)
        rand_block2.addData('RandResp.corr', RandResp.corr)
        if RandResp.keys != None:  # we had a response
            rand_block2.addData('RandResp.rt', RandResp.rt)
        
        #------Prepare to start Routine "RandFeedback"-------
        t = 0
        RandFeedbackClock.reset()  # clock 
        frameN = -1
        routineTimer.add(0.200000)
        # update component parameters for each repeat
        if RandResp.corr:
            BlockRTs.append(RandResp.rt)
        Color = gen_fb(Feedback,fb_block,trial)
        if RandResp.corr and RandResp.rt < crit:
        #    Color = [0,1,0]
            Earning_Trial.append(1)
        #    earning = earning + 0.05
        #    e_string = str(earning)
        else:
        #    Color = [1,1,1]
            Earning_Trial.append(0)
        FB_Rand.setFillColor([0,0,0])
        FB_Rand.setLineColor(Color)
        # keep track of which components have finished
        RandFeedbackComponents = []
        RandFeedbackComponents.append(FB_Rand)
        RandFeedbackComponents.append(ISI_rand)
        for thisComponent in RandFeedbackComponents:
            if hasattr(thisComponent, 'status'):
                thisComponent.status = NOT_STARTED
        
        #-------Start Routine "RandFeedback"-------
        continueRoutine = True
        while continueRoutine and routineTimer.getTime() > 0:
            # get current time
            t = RandFeedbackClock.getTime()
            frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
            # update/draw components on each frame
            
            
            # *FB_Rand* updates
            if t >= 0.0 and FB_Rand.status == NOT_STARTED:
                # keep track of start time/frame for later
                FB_Rand.tStart = t  # underestimates by a little under one frame
                FB_Rand.frameNStart = frameN  # exact frame index
                FB_Rand.setAutoDraw(True)
            if FB_Rand.status == STARTED and t >= (0.0 + (0.2-win.monitorFramePeriod*0.75)): #most of one frame period left
                FB_Rand.setAutoDraw(False)
            
            # *ISI_rand* updates
            if t >= 0.0 and ISI_rand.status == NOT_STARTED:
                # keep track of start time/frame for later
                ISI_rand.tStart = t  # underestimates by a little under one frame
                ISI_rand.frameNStart = frameN  # exact frame index
                ISI_rand.setAutoDraw(True)
            if ISI_rand.status == STARTED and t >= (0.0 + (.2-win.monitorFramePeriod*0.75)): #most of one frame period left
                ISI_rand.setAutoDraw(False)
            
            # check if all components have finished
            if not continueRoutine:  # a component has requested a forced-end of Routine
                routineTimer.reset()  # if we abort early the non-slip timer needs reset
                break
            continueRoutine = False  # will revert to True if at least one component still running
            for thisComponent in RandFeedbackComponents:
                if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                    continueRoutine = True
                    break  # at least one component has not yet finished
            
            # check for quit (the Esc key)
            if endExpNow or event.getKeys(keyList=["escape"]):
                core.quit()
            
            # refresh the screen
            if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                win.flip()
        
        #-------Ending Routine "RandFeedback"-------
        for thisComponent in RandFeedbackComponents:
            if hasattr(thisComponent, "setAutoDraw"):
                thisComponent.setAutoDraw(False)
        trial = trial + 1
        thisExp.nextEntry()
        
    # completed 1 repeats of 'rand_block2'
    
    
    #------Prepare to start Routine "Rest"-------
    t = 0
    RestClock.reset()  # clock 
    frameN = -1
    routineTimer.add(30.000000)
    # update component parameters for each repeat
    vector = []
    count = 0
    Respvec = []
    other = []
    Keyvec = []
    trial = 0
    crit = Calc_Block_Criterion(BlockRTs,crit)
    
    makesequencestart(sequence)
    makerandom()
    
    breatherphrase = str("Good job, your earnings increased!\n\nYou finished block %s.  \n \nTake a breather. \n \n" % (block))
    block = block+1
    fb_block = block - 1
    Breather.setText(breatherphrase)
    # keep track of which components have finished
    RestComponents = []
    RestComponents.append(Breather)
    RestComponents.append(plus)
    RestComponents.append(readyPlus)
    for thisComponent in RestComponents:
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
    
    #-------Start Routine "Rest"-------
    continueRoutine = True
    while continueRoutine and routineTimer.getTime() > 0:
        # get current time
        t = RestClock.getTime()
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        
        
        # *Breather* updates
        if t >= 0.0 and Breather.status == NOT_STARTED:
            # keep track of start time/frame for later
            Breather.tStart = t  # underestimates by a little under one frame
            Breather.frameNStart = frameN  # exact frame index
            Breather.setAutoDraw(True)
        if Breather.status == STARTED and t >= (0.0 + (5-win.monitorFramePeriod*0.75)): #most of one frame period left
            Breather.setAutoDraw(False)
        
        # *plus* updates
        if t >= 5 and plus.status == NOT_STARTED:
            # keep track of start time/frame for later
            plus.tStart = t  # underestimates by a little under one frame
            plus.frameNStart = frameN  # exact frame index
            plus.setAutoDraw(True)
        if plus.status == STARTED and t >= (25-win.monitorFramePeriod*0.75): #most of one frame period left
            plus.setAutoDraw(False)
        
        # *readyPlus* updates
        if t >= 25 and readyPlus.status == NOT_STARTED:
            # keep track of start time/frame for later
            readyPlus.tStart = t  # underestimates by a little under one frame
            readyPlus.frameNStart = frameN  # exact frame index
            readyPlus.setAutoDraw(True)
        if readyPlus.status == STARTED and t >= (30-win.monitorFramePeriod*0.75): #most of one frame period left
            readyPlus.setAutoDraw(False)
        
        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            routineTimer.reset()  # if we abort early the non-slip timer needs reset
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in RestComponents:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # check for quit (the Esc key)
        if endExpNow or event.getKeys(keyList=["escape"]):
            core.quit()
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    #-------Ending Routine "Rest"-------
    for thisComponent in RestComponents:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    BlockRTs = []
    print('Criteria for next block = ' + str(crit))
    thisExp.nextEntry()
    
# completed 1 repeats of 'Run4'


#------Prepare to start Routine "end"-------
t = 0
endClock.reset()  # clock 
frameN = -1
# update component parameters for each repeat
phrase = str("Thanks for Participating! \n \n You earned $32 \n \n Press 1 to exit") 

E_filename = 'EarningInfo/TrialbyTrialEarning_%s.txt' %(expInfo['participant'])
E_trial_file = open(E_filename,'w')
write_E = csv.writer(E_trial_file)
write_E.writerow(Earning_Trial)

#earning_filename = 'EarningInfo/earning_subj_%s.txt'%(expInfo['participant'])
#earning = open(earning_filename,'w')
#earning.write(e_string)



Thanks.setText(phrase)
Press = event.BuilderKeyResponse()  # create an object of type KeyResponse
Press.status = NOT_STARTED
# keep track of which components have finished
endComponents = []
endComponents.append(Thanks)
endComponents.append(Press)
for thisComponent in endComponents:
    if hasattr(thisComponent, 'status'):
        thisComponent.status = NOT_STARTED

#-------Start Routine "end"-------
continueRoutine = True
while continueRoutine:
    # get current time
    t = endClock.getTime()
    frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
    # update/draw components on each frame
    
    
    # *Thanks* updates
    if t >= 0.0 and Thanks.status == NOT_STARTED:
        # keep track of start time/frame for later
        Thanks.tStart = t  # underestimates by a little under one frame
        Thanks.frameNStart = frameN  # exact frame index
        Thanks.setAutoDraw(True)
    
    # *Press* updates
    if t >= 0.0 and Press.status == NOT_STARTED:
        # keep track of start time/frame for later
        Press.tStart = t  # underestimates by a little under one frame
        Press.frameNStart = frameN  # exact frame index
        Press.status = STARTED
        # keyboard checking is just starting
        Press.clock.reset()  # now t=0
        event.clearEvents(eventType='keyboard')
    if Press.status == STARTED:
        theseKeys = event.getKeys(keyList=['1'])
        
        # check for quit:
        if "escape" in theseKeys:
            endExpNow = True
        if len(theseKeys) > 0:  # at least one key was pressed
            Press.keys = theseKeys[-1]  # just the last key pressed
            Press.rt = Press.clock.getTime()
            # a response ends the routine
            continueRoutine = False
    
    # check if all components have finished
    if not continueRoutine:  # a component has requested a forced-end of Routine
        routineTimer.reset()  # if we abort early the non-slip timer needs reset
        break
    continueRoutine = False  # will revert to True if at least one component still running
    for thisComponent in endComponents:
        if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
            continueRoutine = True
            break  # at least one component has not yet finished
    
    # check for quit (the Esc key)
    if endExpNow or event.getKeys(keyList=["escape"]):
        core.quit()
    
    # refresh the screen
    if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
        win.flip()
    else:  # this Routine was not non-slip safe so reset non-slip timer
        routineTimer.reset()

#-------Ending Routine "end"-------
for thisComponent in endComponents:
    if hasattr(thisComponent, "setAutoDraw"):
        thisComponent.setAutoDraw(False)

# check responses
if Press.keys in ['', [], None]:  # No response was made
   Press.keys=None
# store data for thisExp (ExperimentHandler)
thisExp.addData('Press.keys',Press.keys)
if Press.keys != None:  # we had a response
    thisExp.addData('Press.rt', Press.rt)
thisExp.nextEntry()





































win.close()
core.quit()
