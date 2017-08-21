function [PMresults]= SRTT_PM(which_sequ, subID)
%% WRITTEN BY AINSLIE JOHNSTONE 03.01.2016
%% ADAPTED 01.03.2017 for SRTT-TMS-tDCS Experiment
%% SRTT evening test
% To run this script type SRTT_pm(participant number, sequence number) 
% Choose from the options below to change the amount of practice, type of
% task and whether you are in script test or actual task mode. 
% Some info, for example location of results to be saved, will have to be
% changed on other computers.


%Ensure that the script is running on Psychtoolbox
AssertOpenGL;

%Set the number of random trials 
no_rand=48;

%Set the number of sequence trials, 
no_sequ=15;
 
%Explicit? 0=no, 1=yes
explicit=1;

%Script Test? (this skips the instruction phase for testing) 0=no 1=yes 
ScriptTest=0;

%Which Random? (A=1, B=2 or C=3)
TypeRand=which_sequ;

AM=0;

%Navigate to folder for saving data
%THIS WILL NEED TO BE CHANGED ON ANOTHER COMPUTER
cd('C:\Users\TMSLab\Desktop\Ainslie\');

% name directory
%THIS WILL NEED TO BE CHANGED ON ANOTHER COMPUTER
folderName=['Participant_' num2str(subID) 'sequ' num2str(which_sequ)];
directory=sprintf('%s','C:\Users\TMSLab\Desktop\Ainslie\',folderName,'/');
cd(directory);

%warn if duplicate sub ID
fileName=['PMresults_' num2str(subID)];
if exist(fileName,'file')
    if ~IsOctave
        resp=questdlg({['the file' fileName 'already exists']; 'do you want to overwrite it?'},...
            'duplicate warning','cancel','ok','ok');
    else
        resp=input(['the file ' fileName ' already exists. do you want to overwrite it? [Type ok for overwrite]'], 's');
    end
    
    if ~strcmp(resp,'ok') %abort experiment if overwriting was not confirmed
        disp('experiment aborted')
        return
    end
end

%Return to folder where scripts are saved 
%THIS WILL NEED TO BE CHANGED ON ANOTHER COMPUTER
cd('C:\Users\TMSLab\Desktop\Ainslie\');
 
 
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
    Randoms=[5, 7, 1, 6, 4, 8, 3, 2;...
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
    myText = ['Welcome back to the experiment!\n' ...
              'Thank you for coming back for the evening session. \n' ...
              '\n' ...
              'We are now going to test your performance on a shortened version of the task.\n' ...
              '\n' ...
              'Press space to continue.\n' ];
    DrawFormattedText(expWin, myText, 'center', 'center');
    Screen('Flip', expWin);
    WaitSecs(7);
    KbWait(Keyz, 3);

   
    end 
     myText = [ 'If you have any questions please ask the experimenter now.\n'....
              '\n'...
              'If not, you may begin the experiment.  \n' ...
              '\n' ...
              'Press space to begin.\n' ];
    DrawFormattedText(expWin, myText, 'center', 'center');
    Screen('Flip', expWin);
    KbWait(Keyz, 3);
    


%% PM Test
% Establish file name
fileName=['PMresults_' num2str(subID) '.txt'];

% Pre-fill a matrix for results
PMlines=(no_rand*2)+(no_sequ*16);
PMresults=zeros(PMlines,7);

%Loop throught the random, then sequence SRTT
which_rand=Randoms(TypeRand, 7);
RandomSRTT(no_rand,expWin,mx, my, Keyz, which_rand);
load randresults.mat
PMresults(1:no_rand,:)=randresults;

thistime_no=no_sequ;
SequSRTTnew(thistime_no,explicit,expWin,mx, my, Keyz, which_sequ, AM) ;
load sequresults.mat
PMresults((no_rand+1):(no_rand+(thistime_no*16)),:)=sequresults;

which_rand=Randoms(TypeRand, 8);
RandomSRTT(no_rand,expWin,mx, my, Keyz, which_rand) ;
load randresults.mat
PMresults(no_rand+(thistime_no*16)+1:PMlines, :)=randresults;

%THIS WILL NEED TO BE CHANGED ON OTHER COMPUTER
cd(directory);
dlmwrite(fileName, PMresults, 'delimiter', ',', 'precision', 6);
cd('C:\Users\TMSLab\Desktop\Ainslie\');
%

%% End of Experiment
 myText = ['The experiment is now over.\n' ...
           'Thank you for taking part!\n' ];
       
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