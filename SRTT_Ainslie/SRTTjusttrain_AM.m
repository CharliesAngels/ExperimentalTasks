function [baseresults,trainresults,postresults]= SRTT_AM(subID)
%% WRITTEN BY AINSLIE JOHNSTONE 03.01.2016
%% SRTT Morning test and training
% To run this script type SRTT_am(participant number) 
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
no_sequ=[9;15;9];
 
%Explicit? 0=no, 1=yes
                         
explicit=1;

%Script Test? (th1s skips the instruction phase for testing) 0=no 1=yes 
ScriptTest=1;

%Which Random? (A=1, B=2 or C=3)
TypeRand=1;

%warn if duplicate sub ID
folderName=['Participant_' num2str(subID)];
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

cd('C:\Users\Presentation\Desktop\Ainslie\');

%Make a folder for the participant's data
mkdir(folderName);
 % name directory
 directory=sprintf('%s','C:\Users\Presentation\Desktop\Ainslie\',folderName,'\');
 
 
 
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
    ListenChar(2);

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

    
    Randoms=[ 1, 2, 3, 4, 5 ,6 ,7, 8;
              5, 7, 1, 6, 4, 8, 3, 2;
              3, 2, 8, 5, 6, 7, 4, 1];
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
              'Press any key to continue.\n' ];
    DrawFormattedText(expWin, myText, 'center', 'center');
    Screen('Flip', expWin);
    WaitSecs(3);
    KbWait(Keyz, 3);

    myText = ['You will see four circles appear on screen.\n' ...
              'Each circle corresponds to one of your 4 fingers. \n' ...
              '\n'....
              'The far left circle corresponds to the button below your index finger.  \n' ...
              'The far right circle corresponds to the button below your little finger. \n' ...
              '\n' ...
              'On the next screen you will see an example of these circles. \n'...
              'Press any key to continue.\n' ];
    DrawFormattedText(expWin, myText, 'center', 'center');
    Screen('Flip', expWin);
    WaitSecs(5);
    KbWait(Keyz,3);
    
    Screen('FrameOval', expWin, [000], [0.35*mx, my-0.075*mx, 0.5*mx, my+0.075*mx], 2, 2 );
    Screen('FrameOval', expWin, [000], [0.733*mx, my-0.075*mx, 0.883*mx, my+0.075*mx], 2, 2 );
    Screen('FrameOval', expWin, [000], [1.116*mx, my-0.075*mx, 1.266*mx, my+0.075*mx], 2, 2 );
    Screen('FrameOval', expWin, [000], [1.5*mx, my-0.075*mx, 1.65*mx, my+0.075*mx], 2, 2 ); 
    Screen('Flip', expWin);
    WaitSecs(2);
    
    
    myText = ['During the experiment one of these circles will become filled.\n' ...
              'You must press the button which corresponds to the filled circle. \n' ...
              '\n'....
              'Try to be as fast and accurate as possible. \n' ...
              'There will be breaks throughout the experiment, so try and stay focussed. \n'...
              '\n' ...
              'Press any key to continue.\n' ];
    DrawFormattedText(expWin, myText, 'center', 'center');
    Screen('Flip', expWin);
    WaitSecs(5);
    KbWait(Keyz, 3);
    
    if explicit==1
        myText = ['At some points during the experiment the buttons you\n' ...
              'press will be in a random order \n' ...
              '\n'....
              'At other times, the button presses will follow a sequence.  \n' ...
              'The begining of the sequence will be indicated by all 4 circles turning blue.\n' ...
              '\n' ...
              'On the next screen you will see an example of these circles. \n'...
              'Press any key to continue.\n' ];
    DrawFormattedText(expWin, myText, 'center', 'center');
    Screen('Flip', expWin);
    WaitSecs(5)
    KbWait(Keyz,3);
    
    Screen('FrameOval', expWin, [0 0 1], [0.35*mx, my-0.075*mx, 0.5*mx, my+0.075*mx], 2, 2 );
    Screen('FrameOval', expWin, [0 0 1], [0.733*mx, my-0.075*mx, 0.883*mx, my+0.075*mx], 2, 2 );
    Screen('FrameOval', expWin, [0 0 1], [1.116*mx, my-0.075*mx, 1.266*mx, my+0.075*mx], 2, 2 );
    Screen('FrameOval', expWin, [0 0 1], [1.5*mx, my-0.075*mx, 1.65*mx, my+0.075*mx], 2, 2 ); 
    Screen('Flip', expWin);
    WaitSecs(2);
    end 
    end 
     myText = ['Thank you for reading the instructions.\n' ...
              'If you have any questions please ask the experimenter now!\n'....
              '\n'...
              'If not, you may begin the experiment.  \n' ...
              '\n' ...
              'Press any key to begin.\n' ];
    DrawFormattedText(expWin, myText, 'center', 'center');
    Screen('Flip', expWin);
    KbWait(Keyz, 3);



%% Training 

fileName= ['trainresults_' num2str(subID) '.txt'];
trainlines=(no_rand*2)+(no_sequ(2,:)*12);
trainresults=zeros(trainlines,7);

which_rand=Randoms(TypeRand, 3);
RandomSRTT(no_rand,expWin,mx, my, Keyz, which_rand);
load randresults.mat
trainresults(1:no_rand,:)=randresults;

thistime_no=no_sequ(2,:);
SequSRTTnew(thistime_no,explicit,expWin,mx, my, Keyz, which_sequ) ;
load sequresults.mat
trainresults((no_rand+1):(no_rand+(thistime_no*12)),:)=sequresults;

which_rand=Randoms(TypeRand, 4);
RandomSRTT(no_rand,expWin,mx, my, Keyz, which_rand);
load randresults.mat
trainresults((no_rand+(thistime_no*12)+1:trainlines), :)=randresults;

cd(directory);
dlmwrite(fileName, trainresults, 'delimiter', ',', 'precision', 6);
cd('C:\Users\Presentation\Desktop\Ainslie\');

 %% Short Break #2
 myText = ['You are doing really well!\n' ...
           'You are 3/4 of the way through \n'...
           '\n'...
           'Take a minute break\n' ];
 DrawFormattedText(expWin, myText, 'center', 'center');
 Screen('Flip', expWin);
 WaitSecs(60)
    
 myText = ['Press space when you are ready to continue\n' ...
             'Good Luck!\n' ];
 DrawFormattedText(expWin, myText, 'center', 'center');
 Screen('Flip', expWin);
     % Wait for key stroke. This will first make sure all keys are
     % released, then wait for a keypress and release:
 KbWait(Keyz, 3);  
 
 %% Post test
fileName= ['postresults_' num2str(subID) '.txt'];
postlines=(no_rand*2)+(no_sequ(3,:)*12);
postresults=zeros(postlines,7);

which_rand=Randoms(TypeRand, 5);
RandomSRTT(no_rand,expWin,mx, my, Keyz, which_rand);
load randresults.mat
postresults(1:no_rand,:)=randresults;

thistime_no=no_sequ(3,:);
SequSRTTnew(thistime_no,explicit,expWin,mx, my, Keyz,which_sequ) ;
load sequresults.mat
postresults((no_rand+1):(no_rand+(thistime_no*12)),:)=sequresults;

which_rand=Randoms(TypeRand, 6);
RandomSRTT(no_rand,expWin,mx, my, Keyz, which_rand);
load randresults.mat
postresults((no_rand+(thistime_no*12)+1:postlines), :)=randresults;

cd(directory);
dlmwrite(fileName, postresults, 'delimiter', ',', 'precision', 6);
cd('C:\Users\Presentation\Desktop\Ainslie\');
    
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