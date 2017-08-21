function [baseresults,trainresults,postresults]= SRTT_AM(which_sequ, subID)
%% WRITTEN BY AINSLIE JOHNSTONE 03.01.2016
%% ADAPTED 01.03.2017 for SRTT-TMS-tDCS Experiment
%% SRTT Morning test and training
% To run this script type SRTT_am(sequence number, participant number) 
% This script references SequSRTTnew.m and RandomSRTT.m
% RandomSRTT.m also requires RandomBlocks.mat

% Choose from the options below to change the amount of practice, type of
% task and whether you are in script test or actual task mode. 
% Some info, for example location of results to be saved, will have to be
% changed on other computers.


%Ensure that the script is running on Psychtoolbox
AssertOpenGL;

%Set the number of random trials 
no_rand=48;

%Set the number of sequence trials, 
%column 1 for baseline, column 2 for training, column 3 for post-test
no_sequ=[4;25;4];
 
%Explicit? 0=no, 1=yes
explicit=1;

%Script Test? (this skips the instruction phase for testing) 0=no 1=yes 
ScriptTest=1;

TypeRand=which_sequ;

%Create folder name and warn if duplicate sub ID
folderName=['Participant_' num2str(subID) 'sequ' num2str(which_sequ) ];
if exist(folderName,'dir')
    if ~IsOctave
        resp=questdlg({['the folder' folderName 'already exists']; 'do you want to overwrite it?'},...
            'duplicate warning','cancel','ok','ok');
    else
        resp=input(['the folder ' folderName ' already exists. do you want to overwrite it? [Type ok for overwrite]'], 's');
    end
    
    if ~strcmp(resp,'ok') %abort experiment if overwriting was not confirmed
        disp('experiment aborted')
        return
    end
end

%Navigate to folder within which data will be saved
%THIS WILL NEED TO BE CHANGED ON ANOTHER COMPUTER
cd('C:\Users\TMSLab\Desktop\Ainslie\');

%Make a folder for the participant's data
mkdir(folderName);
 % name directory
 %THIS WILL NEED TO BE CHANGED ON ANOTHER COMPUTER
 directory=sprintf('%s','C:\Users\TMSLab\Desktop\Ainslie\',folderName,'\');
 
 
 
%% Define the key presses and begin program
try 
    % Enable unified mode of KbName, so KbName accepts identical key names on
    % all operating systems (not absolutely necessary, but good practice):
    KbName('UnifyKeyNames');

    %Cache KbCheck 
    KbCheck;

    %Disable output of keypresses to Matlab. 
    %if the program crashes press CTRL-C to reenable keyboard handling 
    %then 'sca' to close screen
    %ListenChar(2);

    %Set higher DebugLevel, 
    olddebuglevel=Screen('Preference', 'VisualDebuglevel', 3);

    %Choosing the display 
    screens=Screen('Screens');
    screenNumber=max(screens);
    
    %Open Full Screen 
    [expWin,rect]=Screen('OpenWindow',0);
    %alternative: replace the above with smaller window for testing
    %[expWin,rect]=Screen('OpenWindow',screenNumber,[],[10 20 1200 700]);
  
    %Set Colour Range 
    Screen('ColorRange', expWin,[1]);
    
    %get the midpoint (mx, my) of this window, x and y
    [mx, my] = RectCenter(rect);

    %get rid of the mouse cursor, 
    HideCursor;
    
    %Prepare output
    colHeaders = { 'sequence', 'block no', 'trial no', 'position', 'button pressed', 'correct', 'RT' };

    %Find Keyboard
    [Keyz]= GetKeyboardIndices; 
    
    %The order in which random presses from RandomBlocks.mat will be used
    Randoms=[ 5, 7, 1, 6, 4, 8, 3, 2;...
              14, 15, 13, 10, 16, 12, 9, 11;...
              20, 21, 24, 22, 17, 19, 18, 23;...
              26, 29, 30, 31, 32, 27, 25, 28;...
              4, 10, 21, 25, 1, 11, 18, 20];

%% Instructions

 %Preparing and displaying the welcome screen
    % Choosing text size
    Screen('TextSize', expWin, 20);
    
    %Skip instructions if experiment is in test mode 
   if ScriptTest==0 
       
    % Instructions presented in middle of screen 
    myText = ['Welcome to the experiment!\n' ...
              ' \n' ...
              'This experiment aims to measure your reaction time, \n' ...
              'and to test whether it improves with training.\n' ...
              '\n' ...
              'Press space to continue.\n' ];
    DrawFormattedText(expWin, myText, 'center', 'center');
    Screen('Flip', expWin);
    WaitSecs(3);
    KbWait(Keyz, 3);

    myText = ['You will see four dashes appear on screen.\n' ...
              'Each dash corresponds to one of your 4 fingers. \n' ...
              '\n'....
              'The far left dash corresponds to the button below your index finger.  \n' ...
              'The far right dash corresponds to the button below your little finger. \n' ...
              '\n' ...
              'On the next screen you will see an example of these dashes. \n'...
              'Press space to continue.\n' ];
    DrawFormattedText(expWin, myText, 'center', 'center');
    Screen('Flip', expWin);
    WaitSecs(5);
    KbWait(Keyz,3);
    
   Screen('FillOval', expWin, [000], [0.69*mx, my-0.005*mx, 0.71*mx, my+0.005*mx]);
    Screen('FillOval', expWin, [000],  [0.89*mx, my-0.005*mx, 0.91*mx, my+0.005*mx] );
    Screen('FillOval', expWin, [000],  [1.09*mx, my-0.005*mx, 1.11*mx, my+0.005*mx] );
    Screen('FillOval', expWin, [000],  [1.29*mx, my-0.005*mx, 1.31*mx, my+0.005*mx] );  
    Screen('Flip', expWin);
    WaitSecs(2);
    
    
    myText = ['During the experiment a larger circle will appear at one of these positions\n' ...
              'You must press the button which corresponds to the larger circle. \n' ...
              '\n'....
              'Try to be as fast and accurate as possible. \n' ...
              'There will be breaks throughout the experiment, so try and stay focussed. \n'...
              '\n' ...
              'Press space to continue.\n' ];
    DrawFormattedText(expWin, myText, 'center', 'center');
    Screen('Flip', expWin);
    WaitSecs(5);
    KbWait(Keyz, 3);
    
    if explicit==1
        myText = ['At some points during the experiment the buttons you\n' ...
              'press will be in a random order \n' ...
              '\n'....
              'At other times, the button presses will follow a sequence.  \n' ...
              'During Random sections the circles will be black, during Sequence they will be blue.\n' ...
              '\n' ...
               'Try to learn the sequence, you will be tested on it this afternoon.\n' ...
               '\n' ...
              'On the next screen you will see an example of these dashes. \n'...
              'Press space to continue.\n' ];
    DrawFormattedText(expWin, myText, 'center', 'center');
    Screen('Flip', expWin);
    WaitSecs(5)
    KbWait(Keyz,3);
    
       Screen('FillOval', expWin, [0 0 1], [0.69*mx, my-0.005*mx, 0.71*mx, my+0.005*mx]);
    Screen('FillOval', expWin, [0 0 1],  [0.89*mx, my-0.005*mx, 0.91*mx, my+0.005*mx] );
    Screen('FillOval', expWin, [0 0 1],  [1.09*mx, my-0.005*mx, 1.11*mx, my+0.005*mx] );
    Screen('FillOval', expWin, [0 0 1],  [1.29*mx, my-0.005*mx, 1.31*mx, my+0.005*mx] );  
    Screen('Flip', expWin);
    WaitSecs(2);
    end 
    end 
     myText = ['Thank you for reading the instructions.\n' ...
              'If you have any questions please ask the experimenter now!\n'....
              '\n'...
              'If not, you may begin the experiment.  \n' ...
              '\n' ...
              'Press space to begin.\n' ];
    DrawFormattedText(expWin, myText, 'center', 'center');
    Screen('Flip', expWin);
    KbWait(Keyz, 3);
    


%% Baseline Test
% Establish file name
fileName=['baseresults_' num2str(subID) '.txt'];
AM=0;

% Pre-fill a matrix for results
baselines=(no_rand*2)+(no_sequ(1,:)*16);
baseresults=zeros(baselines,7);

%Loop throught the random, then sequence SRTT
which_rand=Randoms(TypeRand, 1);
RandomSRTT(no_rand,expWin,mx, my, Keyz, which_rand);
load randresults.mat
baseresults(1:no_rand,:)=randresults;

thistime_no=no_sequ(1,:);
SequSRTTnew(thistime_no,explicit,expWin,mx, my, Keyz, which_sequ, AM) ;
load sequresults.mat
baseresults((no_rand+1):(no_rand+(thistime_no*16)),:)=sequresults;

which_rand=Randoms(TypeRand, 2);
RandomSRTT(no_rand,expWin,mx, my, Keyz, which_rand) ;
load randresults.mat
baseresults(no_rand+(thistime_no*16)+1:baselines, :)=randresults;

%THIS WILL NEED TO BE CHANGED ON OTHER COMPUTER
cd(directory);
dlmwrite(fileName, baseresults, 'delimiter', ',', 'precision', 6);
cd('C:\Users\TMSLab\Desktop\Ainslie\')
%

%% Short Break
    myText = ['We will now use TMS and then set up the tDCS electrodes\n' ... 
           ' \n'...
           'This is TMS T2\n'];
    DrawFormattedText(expWin, myText, 'center', 'center');
    Screen('Flip', expWin);
    WaitSecs(60);
    
     myText = ['+\n'...
     '\n'...
     'Please wait until the tDCS has been set up\n' ];
    DrawFormattedText(expWin, myText, 'center', 'center');
    Screen('Flip', expWin);
    KbWait(Keyz, 3);   


%% Training 

fileName= ['trainresults_' num2str(subID) '.txt'];
trainlines=(no_rand*2)+(no_sequ(2,:)*16);
trainresults=zeros(trainlines,7);
AM=1;

which_rand=Randoms(TypeRand, 3);
RandomSRTT(no_rand,expWin,mx, my, Keyz, which_rand);
load randresults.mat
trainresults(1:no_rand,:)=randresults;

thistime_no=no_sequ(2,:);
SequSRTTnew(thistime_no,explicit,expWin,mx, my, Keyz, which_sequ, AM) ;
load sequresults.mat
trainresults((no_rand+1):(no_rand+(thistime_no*16)),:)=sequresults;

which_rand=Randoms(TypeRand, 4);
RandomSRTT(no_rand,expWin,mx, my, Keyz, which_rand);
load randresults.mat
trainresults((no_rand+(thistime_no*16)+1:trainlines), :)=randresults;

%THIS WILL NEED TO BE CHANGED ON ANOTHER COMPUTER
cd(directory);
dlmwrite(fileName, trainresults, 'delimiter', ',', 'precision', 6);
cd('C:\Users\TMSLab\Desktop\Ainslie\');

 %% Short Break #2
 myText = ['We will now remove the tDCS electrodes and use TMS again\n' ... 
           ' \n'...
           'This is TMS T3\n' ];
 DrawFormattedText(expWin, myText, 'center', 'center');
 Screen('Flip', expWin);
 WaitSecs(60)
    
 myText = ['+\n'...
     '\n'...
     'Press space to continue once TMS is complete\n' ];
 DrawFormattedText(expWin, myText, 'center', 'center');
 Screen('Flip', expWin);
     % Wait for key stroke. This will first make sure all keys are
     % released, then wait for a keypress and release:
 KbWait(Keyz, 3);  
 
 %% Post test
fileName= ['postresults_' num2str(subID) '.txt'];
postlines=(no_rand*2)+(no_sequ(3,:)*16);
postresults=zeros(postlines,7);

AM=0;
which_rand=Randoms(TypeRand, 5);
RandomSRTT(no_rand,expWin,mx, my, Keyz, which_rand);
load randresults.mat
postresults(1:no_rand,:)=randresults;

thistime_no=no_sequ(3,:);
SequSRTTnew(thistime_no,explicit,expWin,mx, my, Keyz,which_sequ, AM) ;
load sequresults.mat
postresults((no_rand+1):(no_rand+(thistime_no*16)),:)=sequresults;

which_rand=Randoms(TypeRand, 6);
RandomSRTT(no_rand,expWin,mx, my, Keyz, which_rand);
load randresults.mat
postresults((no_rand+(thistime_no*16)+1:postlines), :)=randresults;

%THIS WILL NEED TO BE CHANGED ON ANOTHER COMPUTER
cd(directory);
dlmwrite(fileName, postresults, 'delimiter', ',', 'precision', 6);
cd('C:\Users\TMSLab\Desktop\Ainslie\');
    
%% End of Experiment
 myText = ['Thank you for taking part in the experiment.\n' ...
           'We look forward to seeing you later today.\n' ...
           ' \n'....
           'Please remember: do not nap before the next session'];
       
 DrawFormattedText(expWin, myText, 'center', 'center');
 Screen('Flip', expWin);
 WaitSecs(10);
  
sca; % Screen Close All 
 ListenChar(0);
 %return to olddebuglevel
 Screen('Preference', 'VisualDebuglevel', olddebuglevel);
    
catch
    % This section is executed only in case an error happens in the
    % experiment code implemented between try and catch...
    ShowCursor;
    Screen('CloseAll'); %or sca
    ListenChar(0);
    Screen('Preference', 'VisualDebuglevel', olddebuglevel);
    %output the error message
    psychrethrow(psychlasterror);
end