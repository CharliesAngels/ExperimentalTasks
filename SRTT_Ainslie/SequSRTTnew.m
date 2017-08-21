function [sequresults] = SequSRTTnew(thistime_no, explicit, expWin,mx, my, Keyz,which_sequ, AM)
%% Ainslie Johnstone 03.01.16
%% ADAPTED 01.03.2017 for SRTT-TMS-tDCS Experiment
% This script is references in SRTT_AM.m and SRTT_PM.m

%tag idetifies whether a press was to a random or sequence stimuli 
tag=1;
clear j
clear i
clear sequresults
DisableKeysForKbCheck([1:31,33:48,53:256]);

%Pre-specify matrix size
sequresults=zeros((thistime_no*16), 7);

%Create a for loop to run the sequence j times
%The for loop using i creates the 16 item sequence
for j=1:thistime_no;
     
    %Creates some breaks at pre-specified intervals
        if j==4 && AM==1 || j==10 && AM==1 || j==17 && AM==1 || j==23 && AM==1;
              myText = ['Time for a few seconds break'];
    DrawFormattedText(expWin, myText, 'center', 'center');
    Screen('Flip', expWin);
    WaitSecs(10);
    
     myText = ['Press space when you are ready to continue\n' ...
              'Good Luck!\n' ];
    DrawFormattedText(expWin, myText, 'center', 'center');
    Screen('Flip', expWin);
    KbWait(Keyz, 3);   
        end 
            
    
    % Loop around the sequence
    for i=1:16;
       

 %Establishes the positions of the 4 different items in the sequence. 
 % Column 5 contains the keyCodes for the responses v,b,n and m on my
 % keyboard 
 % NOTE: THIS MAY NEED TO BE CHANGED ON ANOTHER COMPUTER! 
 Sequence = [0.65*mx, my-0.05*mx, 0.75*mx, my+0.05*mx, 49;...
        0.85*mx, my-0.05*mx, 0.95*mx, my+0.05*mx,50 ; ...
        1.05*mx, my-0.05*mx, 1.15*mx, my+0.05*mx, 51; ...
        1.25*mx, my-0.05*mx, 1.35*mx, my+0.05*mx, 52];
       
  %Establishing the order of the sequence  
  AllSequ=[1,3,4,1,3,2,4,1,4,2,3,1,2,4,3,2;...
           3,2,3,4,1,2,4,3,1,4,2,1,3,2,4,1;...
           2,4,3,1,2,4,1,3,2,3,4,2,1,4,1,3;...
           1,3,2,1,4,3,1,2,4,1,3,4,2,3,2,4;...
           4,2,3,1,3,4,1,2,3,1,4,2,1,4,3,2]; 
  TestSequ=AllSequ(which_sequ,:);
  p=TestSequ(:,i);
        

    %Presenting the position dashes for 0.6 seconds 
    Screen('FillOval', expWin, [0 0 0.5], [0.69*mx, my-0.005*mx, 0.71*mx, my+0.005*mx]);
    Screen('FillOval', expWin, [0 0 0.5],  [0.89*mx, my-0.005*mx, 0.91*mx, my+0.005*mx] );
    Screen('FillOval', expWin, [0 0 0.5],  [1.09*mx, my-0.005*mx, 1.11*mx, my+0.005*mx] );
    Screen('FillOval', expWin, [0 0 0.5],  [1.29*mx, my-0.005*mx, 1.31*mx, my+0.005*mx] ); 

    Screen('Flip', expWin);
    %CHANGE THIS TO CHANGE RESPONSE-STIMULUS INTERVAL
    WaitSecs(0.6);
        
    %Creating variables which correspond to the the position coordinates
    %for this stimulus in the sequence
    rpos = Sequence(p, 1);
    tpos = Sequence(p, 2);
    lpos = Sequence(p, 3);
    bpos = Sequence(p, 4);
    
       %Setting up the colour change indicating the begining of a sequence in
   %the explicit version
%         if explicit==1 && i==1
%      Screen('FillOval', expWin, [0 0 1], [0.69*mx, my-0.005*mx, 0.71*mx, my+0.005*mx]);
%     Screen('FillOval', expWin, [0 0 1],  [0.89*mx, my-0.005*mx, 0.91*mx, my+0.005*mx] );
%     Screen('FillOval', expWin, [0 0 1],  [1.09*mx, my-0.005*mx, 1.11*mx, my+0.005*mx] );
%     Screen('FillOval', expWin, [0 0 1],  [1.29*mx, my-0.005*mx, 1.31*mx, my+0.005*mx] );
%     Screen('FillOval', expWin, [0 0 1], [rpos, tpos, lpos, bpos]);
%             
%         else 
    
    
    %Presenting the empty ovals and one filled oval. 
    Screen('FillOval', expWin, [0 0 0.5], [0.69*mx, my-0.005*mx, 0.71*mx, my+0.005*mx]);
    Screen('FillOval', expWin, [0 0 0.5],  [0.89*mx, my-0.005*mx, 0.91*mx, my+0.005*mx] );
    Screen('FillOval', expWin, [0 0 0.5],  [1.09*mx, my-0.005*mx, 1.11*mx, my+0.005*mx] );
    Screen('FillOval', expWin, [0 0 0.5],  [1.29*mx, my-0.005*mx, 1.31*mx, my+0.005*mx] );
    Screen('FillOval', expWin, [0 0 0.5], [rpos, tpos, lpos, bpos]);
    
%         end
     %Record the reaction time of this press
       secs0=GetSecs;
        Screen('Flip', expWin);
        KbQueueReserve(2,1,Keyz);
        KbQueueReserve(1,2,Keyz);
        KbQueueFlush(Keyz);
        pressed=0;
        while pressed==0
       [pressed, firstPress, ~,~,~]=KbQueueCheck(Keyz);
        end
        
if pressed==1   
        keyCol=find(firstPress>0);
        firstsecs=firstPress(keyCol);
        rt=firstsecs-secs0;
        firstKey=keyCol;
        KbQueueFlush;
        
        %calculate performance (correct/incorrect) or detect forced exit
        if keyCol==27; %esc key
            break;   %break out of trials loop, but perform all the cleanup things
                     %and give back results collected so far
        elseif keyCol== Sequence(p,5);
            anscorrect = 1;
       
        else
            anscorrect = 0;
              %ensure that the correct response is made 
        end
        
        %Wait for correct answer if incorrect is given first
       if anscorrect==0 
         nextPress=zeros(1,256);
         secondPressed=0;
         while nextPress(:,Sequence(p,5))==0 || secondPressed==0;
        [secondPressed, nextPress, ~,~,~]=KbQueueCheck(Keyz);
         end 
        
       end
      
       
heapTotalMemory = java.lang.Runtime.getRuntime.totalMemory;
heapFreeMemory = java.lang.Runtime.getRuntime.freeMemory;
if(heapFreeMemory < (heapTotalMemory*0.01))
    java.lang.Runtime.getRuntime.gc;
end
         
            
        %Identify which row data should be entered into
        row=((j-1)*16)+i;
        
        %enter results in matrix
        %tag=1 for sequence, tag=0 for random
        %j is the repeat number, i is the location in the sequence
        %p is the actual stimulus presented
        %firstKey idenfies the key pressed whether correct or incorrect (by referencing the column)
        %49=Index Finger (1); 50=Middle Finger (2); 51=Ring Finger (3);
        %52=Little Finger (4). 
        %anscorrect and rt, self-explanitory
        sequresults(row,:) = [tag,j, i, p, firstKey, anscorrect, rt]; 

        %beep if the response was incorrect
        %if anscorrect ~=1
        %   beep;
       % end

        end
    end
    clear rpos tpos lpos bpos
     
         
  save sequresults.mat sequresults  
end