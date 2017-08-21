function [randresults] = RandomSRTT(no_rand,expWin,mx, my, Keyz, which_rand)
%% Ainslie Johnstone 03.01.16
% Creates a random sequence with no repeats
clear r
clear randresults
DisableKeysForKbCheck([1:31,33:48,53:256]);

%Idenfities whether press was to a random or sequence stimuli
tag=0;
randresults= zeros(no_rand,7) ;
 for r=1:no_rand;
  
   load('RandomBlocks.mat');
   rn=RandomBlocks(which_rand, r);
    
    %show empty circles for 0.6 secs
    Screen('FillOval', expWin, [000], [0.69*mx, my-0.005*mx, 0.71*mx, my+0.005*mx]);
    Screen('FillOval', expWin, [000],  [0.89*mx, my-0.005*mx, 0.91*mx, my+0.005*mx] );
    Screen('FillOval', expWin, [000],  [1.09*mx, my-0.005*mx, 1.11*mx, my+0.005*mx] );
    Screen('FillOval', expWin, [000],  [1.29*mx, my-0.005*mx, 1.31*mx, my+0.005*mx] );
    
    Screen('Flip', expWin);
    %CHANGE THIS TO CHANGE RESPONSE-STIMULUS INTERVAL
    WaitSecs(0.6);
    
 Sequence = [0.65*mx, my-0.05*mx, 0.75*mx, my+0.05*mx, 49;...
        0.85*mx, my-0.05*mx, 0.95*mx, my+0.05*mx,50 ; ...
        1.05*mx, my-0.05*mx, 1.15*mx, my+0.05*mx, 51; ...
        1.25*mx, my-0.05*mx, 1.35*mx, my+0.05*mx, 52];
    
    %Identifying the position parameters for each of the stimuli
    rpos = Sequence(rn, 1);
    tpos = Sequence(rn, 2);
    lpos = Sequence(rn, 3);
    bpos = Sequence(rn, 4);
      
    
    %Presenting the empty ovals and one filled oval. 
    Screen('FillOval', expWin, [000], [0.69*mx, my-0.005*mx, 0.71*mx, my+0.005*mx]);
    Screen('FillOval', expWin, [000],  [0.89*mx, my-0.005*mx, 0.91*mx, my+0.005*mx] );
    Screen('FillOval', expWin, [000],  [1.09*mx, my-0.005*mx, 1.11*mx, my+0.005*mx] );
    Screen('FillOval', expWin, [000],  [1.29*mx, my-0.005*mx, 1.31*mx, my+0.005*mx] );
    Screen('FillOval', expWin, [000], [rpos, tpos, lpos, bpos]);
    
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
        elseif keyCol== Sequence(rn,5);
            anscorrect = 1;
       
        else
            anscorrect = 0;
              %ensure that the correct response is made 
        end
        
        % Wait for correct key press
       if anscorrect==0 
         nextPress=zeros(1,256);
         secondPressed=0;
         while nextPress(:,Sequence(rn,5))==0 || secondPressed==0;
        [secondPressed, nextPress, ~,~,~]=KbQueueCheck(Keyz);
        end 
       end
       
heapTotalMemory = java.lang.Runtime.getRuntime.totalMemory;
heapFreeMemory = java.lang.Runtime.getRuntime.freeMemory;
if(heapFreeMemory < (heapTotalMemory*0.01))
    java.lang.Runtime.getRuntime.gc;
end
        
        %enter results in matrix
        %tag explained above
        %1 here is to fill space to esure equal matrix size between this
        %and sequence
        %r is the number of this trial
        %rn is the actual location of the stimuli
        %firstKey is a method of idenfying key first pressed.
        %49=Index Finger (1); 50=Middle Finger (2); 51=Ring Finger (3);
        %52=Little Finger (4). 
        randresults(r,:) = [ tag,1, r, rn, firstKey, anscorrect, rt];
 
    %this is used at begining of script to ensure no repeats
   
   clear rn
       end
 end
save randresults.mat randresults
end 