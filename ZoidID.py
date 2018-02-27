#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
This experiment was created using PsychoPy2 Experiment Builder (v1.83.04), March 21, 2016, at 13:35
If you publish work using this script please cite the relevant PsychoPy publications
  Peirce, JW (2007) PsychoPy - Psychophysics software in Python. Journal of Neuroscience Methods, 162(1-2), 8-13.
  Peirce, JW (2009) Generating stimuli for neuroscience using PsychoPy. Frontiers in Neuroinformatics, 2:10. doi: 10.3389/neuro.11.010.2008
"""

########
#
#    PL-Tetris
# Kevin J. O'Neill
#
########

from __future__ import division  # so that 1/3=0.333 instead of 1/3=0
from psychopy import visual, core, data, event, logging, sound, gui
from psychopy.constants import *  # things like STARTED, FINISHED
import numpy as np  # whole numpy lib is available, prepend 'np.'
from numpy import sin, cos, tan, log, log10, pi, average, sqrt, std, deg2rad, rad2deg, linspace, asarray
from numpy.random import random, randint, normal, shuffle
import os  # handy system and path functions
import sys # to get file system encoding

import random

# Toggle for a "demo" mode. If True, then trails are shortened for testing purposes.
DEBUG_MODE = False

# Ensure that relative paths start from the same directory as this script
_thisDir = os.path.dirname(os.path.abspath(__file__)).decode(sys.getfilesystemencoding())
os.chdir(_thisDir)

# Store info about the experiment session
expName = u'PL-Tetris_2'  # from the Builder filename that created this script
expInfo = {u'session': u'001', u'participant': u'0'}
dlg = gui.DlgFromDict(dictionary=expInfo, title=expName)
if dlg.OK == False: core.quit()  # user pressed cancel
expInfo['date'] = data.getDateStr()  # add a simple timestamp
expInfo['expName'] = expName

# Data file name stem = absolute path + name; later add .psyexp, .csv, .log, etc
filename = _thisDir + os.sep + u'data/%s_%s_%s' %(expInfo['participant'], expName, expInfo['date'])

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
win = visual.Window(size=(1600, 900), fullscr=True, screen=0, allowGUI=False, allowStencil=False,
    monitor=u'testMonitor', color=[0.95,0.95,0.95], colorSpace='rgb',
    blendMode='avg', useFBO=True,
    )
# store frame rate of monitor if we can measure it successfully
expInfo['frameRate']=win.getActualFrameRate()
if expInfo['frameRate']!=None:
    frameDur = 1.0/round(expInfo['frameRate'])
else:
    frameDur = 1.0/60.0 # couldn't get a reliable measure so guess

	
def update_stimuli(stimuli_entry, Zoid_Left, Zoid_Right):
    Zoid_Left.vertices =    stimuli_entry[0][0]
    Zoid_Left.ori =         stimuli_entry[0][1]
    Zoid_Right.vertices =   stimuli_entry[1][0]
    Zoid_Right.ori =        stimuli_entry[1][1]

def update_feedback_adaptive(trial_counter, wrong_counter,response_time_counter,pre_post_break_flag):
		#designed to try to keep subject within a certain accuracy range by advising response time
	speed_up = .96			#if accuracy higher than speed_up, advise increase speed
	slow_down = .94			#if accuracy lower than slow_down, advise decrease speed
							#if between speed_up and slow_down, keep same speed
	number_correct = trial_counter-wrong_counter
	percent_correct = number_correct/trial_counter
	average_time=response_time_counter/trial_counter
	accuracy_message=""
	speed_message=""
	feedback_message=""
	feedback = "You just finished block " + str(block_counter + 1) + " out of " + str(total_block_num) + "\nYour performance this block: \n"
	accuracy_message =  str(number_correct)+" correct out of "+str(trial_counter)+" rounds. \n"
	accuracy_message += str(round(percent_correct*100,2))+" percent accurate. \n"
	speed_message="Average response time: "+str(round(average_time,2))+" seconds.\n\n"
	#determine feedback
	if block_counter + 1 == total_block_num:
		feedback_message = "Thank you.\n\n"
	elif percent_correct<slow_down:
		feedback_message = "Great job! Try to take more time on each pair to bring your accuracy up!\n\n"
		feedback_message_after_break = "For this block, try to take more time on each pair to bring your accuracy up!\n\n"
	elif percent_correct>speed_up:
		feedback_message = "Good job! Try to answer more quickly to reduce your response time!\n\n"
		feedback_message_after_break = "For this block, to answer more quickly to reduce your response time!\n\n"
	else:
		feedback_message = "Great job!\n\n"
		feedback_message_after_break = "Keep the pace!"
	if block_counter + 1 == total_block_num:
		Feedback_Screen.text = feedback+accuracy_message+speed_message+feedback_message+"This is the end of the experiment. Please wait for the experimenter."
	elif (pre_post_break_flag == "pre"):
		Feedback_Screen.text = feedback+accuracy_message+speed_message+feedback_message+"You can now take a break. When you are ready to continue, place you fingers on X and M keys, then press either one.\n(Maximum break time: 5 mins)"
	elif (pre_post_break_flag == "post"):
		Feedback_Screen.text = "Your break has ended.\nGet ready for the next block. Place you fingers on X or M keys.\n\n" + feedback_message_after_break + "New block starting in 10 seconds..."
	else:
		Feedback_Screen.text = "flag_error"
	print feedback+accuracy_message+speed_message+feedback_message
		
def verts_to_name(verts):
    for pair in zoid_match:
        if pair[1] == verts:
            return pair[0]
	
def key_to_answer(key,samediff_key_map):
	if key==samediff_key_map[0]:
		return "same"
	elif key==samediff_key_map[1]:
		return "diff"
	else:
		return "ERROR: not a valid key"
		
def key_to_answer(key,samediff_key_map):
	if key==samediff_key_map[0]:
		return "same"
	elif key==samediff_key_map[1]:
		return "diff"
	else:
		return "ERROR: not a valid key"
	
#Zoid vertices - coordinates for zoids
#the .5's are so the zoids will be centered, to avoid misalignment when rotating them
vert_s=((.5,0),(1.5,0),(1.5,1),(-.5,1),(-.5,0),(-1.5,0),(-1.5,-1),(.5,-1))
vert_z=((-.5,0),(-1.5,0),(-1.5,1),(.5,1),(.5,0),(1.5,0),(1.5,-1),(-.5,-1))
vert_o=((1,1),(-1,1),(-1,-1),(1,-1))
vert_i=((2,-.5),(2,.5),(-2,.5),(-2,-.5))
vert_t=((.5,0),(1.5,0),(1.5,1),(-1.5,1),(-1.5,0),(-.5,0),(-.5,-1),(0.5,-1))
vert_l=((0,-.5),(1,-.5),(1,-1.5),(-1,-1.5),(-1,1.5),(0,1.5))
vert_j=((0,-.5),(-1,-.5),(-1,-1.5),(1,-1.5),(1,1.5),(0,1.5))

verts=[vert_s,vert_z,vert_o,vert_i,vert_t,vert_l,vert_j]

zoid_names=["s","z","o","i","t","l","j"]

zoid_match=[("s",vert_s),("z",vert_z),("o",vert_o),("i",vert_i),("t",vert_t),("l",vert_l),("j",vert_j)]

orientations=[0,90,180,270]

#make list of al possible zoid/orientation pairs
possible_stimuli=[]
   
for zoid in verts:
	if zoid==vert_l or zoid==vert_j or zoid==vert_t:
		for ori in orientations:
			pair=(zoid, ori)
			possible_stimuli.append(pair)
	elif zoid==vert_s or zoid==vert_z or zoid==vert_i:
		for ori in [orientations[0],orientations[1]]:
			pair=(zoid, ori)
			possible_stimuli.append(pair)
	elif zoid==vert_o:
		pair=(zoid, orientations[0])
		possible_stimuli.append(pair)

#list of ((left_zoid, left_orientation), (right_zoid, right_orientation))
stimuli=[]
for left in possible_stimuli:
    for right in possible_stimuli:
        pair=(left,right)
        stimuli.append(pair)

same_matches=[]
diff_matches=[]
		
#split stimuli into pairs of matched zoids, and those of different zoids
for stim in stimuli:
	if stim[0][0]==stim[1][0]:
		same_matches.append(stim)
	else:
		diff_matches.append(stim)

#make sure no correct matches got through
for stim in diff_matches:
	if stim[0][0]==stim[1][0]:
		print "ERROR: ", verts_to_name(stim[0][0]), verts_to_name(stim[1][0])
		
print "unique stimuli", len(same_matches+diff_matches)
print "  same_matches", len(same_matches)
print "  diff_matches", len(diff_matches)
#randomize the stimuli

#for testing purposes
np.random.shuffle(stimuli)

np.random.shuffle(same_matches)
np.random.shuffle(diff_matches)

#split the incorrects into 5 different blocks
#add a full copy of the corrects to each of the five blocks
#randomize each block

blocks=[]

x = 0
total_diff_match_num = 300
total_block_num = 5
if(DEBUG_MODE):
	total_block_num = 2
while x < total_block_num:
	blocks.append(diff_matches[int(x*(total_diff_match_num/total_block_num)):int((x+1)*(total_diff_match_num/total_block_num))])
	blocks[x]+=same_matches
	np.random.shuffle(blocks[x])	
	x+=1

if (DEBUG_MODE):
	blocks = [[((vert_i, 0),(vert_i, 90))],[((vert_i, 0),(vert_i, 90))]]

#confirm that it was all done correctly
print len(blocks), " blocks of lengths:"
total=0
for blo in blocks:
	print "    ",len(blo)
	total+=len(blo)
print "total stimuli: ", total
print


###
#Generate same/diff keys
samediff_key_map=["z","m"]
np.random.shuffle(samediff_key_map)
same=samediff_key_map[0]
diff=samediff_key_map[1]

if "z"==same:
	z_text = u"SAME\nZ"
	m_text = u"DIFFERENT\nM"
elif "m"==same:
	z_text = u"DIFFERENT\nZ"
	m_text = u"SAME\nM"
else:
	z_text = u"ERRORZ"
	m_text = u"ERRORM"

samediff_key_map_text = "To indicate that the two pieces are the SAME, press the " + same + " key \n\nTo indicate that the two pieces are DIFFERENT, press the " + diff + " key\n"

# l - 4
# j - 4
# t - 4
# s	- 2
# z - 2
# i - 2
# o - 1

#     19
#     19**2 = 361

# correct combinations:
# o s z l  j  t  i
# 1 4 4 16 16 16 4
#61 correct combinations

#61/361=.1689

# 300 are different

#give feedback every 19 or 38 rounds
#"work more on speed or accuracy depending"
#give a 3 second break?


# use x and m keys for same and diff
# have half of the people have same and diff for  x and m reversed
#to control for handedness
#stress accuracy because speed can be easily optimized
# by pressing "diff" for everything (~80% accuracy)

#or up the number of sames?
# up number of sames 5x

#I GOT THE MATCH WRONG
#new plan = 5 * 61 correct matches = 305
#           1 * 300 incorrect matches = 300
#    									605 total
#   so 5 blocks of 121
#   taking about 40 minutes

#maybe use a spreadsheet
#use a latin square for quadrants of rounds of spreadsheet

#or
#divide remaining 296 by 4
# put into quadrants
#put a copy of the 65 sames in each

#between quadrants, give feedback on how someone has been doing


			
# Initialize components for Routine "trial"
trialClock = core.Clock()
Orientation_Cue = visual.TextStim(win=win, ori=0, name='Orientation_Cue',
    text=u'\u25cb',    font=u'Arial',
    pos=[0, 0], height=0.1, wrapWidth=None,
    color=u'black', colorSpace='rgb', opacity=1,
    depth=0.0)
Ready_Cue = visual.TextStim(win=win, ori=0, name='Ready_Cue',
    text=u'+',    font=u'Arial',
    pos=[0, 0], height=0.1, wrapWidth=None,
    color=u'black', colorSpace='rgb', opacity=1,
    depth=-1.0)
Zoid_Left = visual.ShapeStim(win=win, name='Zoid_Left',units='cm', 
    vertices=vert_o,
    ori=0, pos=[-5, 0],
    lineWidth=1, lineColor=[1,1,1], lineColorSpace='rgb',
    fillColor=[0.05,0.05,0.05], fillColorSpace='rgb',
    opacity=1,depth=-3.0, 
interpolate=True)
Zoid_Right = visual.ShapeStim(win=win, name='Zoid_Right',units='cm', 
    vertices=vert_o,
    ori=0, pos=[5, 0],
    lineWidth=1, lineColor=[1,1,1], lineColorSpace='rgb',
    fillColor=[0.05,0.05,0.05], fillColorSpace='rgb',
    opacity=1,depth=-4.0, 
interpolate=True)
Button_Instructions = visual.TextStim(win=win, ori=0, name='Button_Instructions',
    text=samediff_key_map_text,    font=u'Arial',
    pos=[0, .5], height=0.07, wrapWidth=None,
    color=u'black', colorSpace='rgb', opacity=1,
    depth=0.0)
if samediff_key_map[0]=="z":
	z_instruction = visual.TextStim(win=win, ori=0, name='z_instruction',
		text=z_text,    font=u'Yu Gothic UI',
		pos=[-.7, -.8], height=0.1, wrapWidth=None,
		color=u'lightseagreen', colorSpace='rgb', opacity=1,
		depth=0.0)	
	m_instruction = visual.TextStim(win=win, ori=0, name='m_instruction',
		text=m_text,    font=u'Yu Gothic UI',
		pos=[.7, -.8], height=0.1, wrapWidth=None, alignHoriz = "right",
		color=u'tomato', colorSpace='rgb', opacity=1,
		depth=0.0)	
else:
	z_instruction = visual.TextStim(win=win, ori=0, name='z_instruction',
    text=z_text,    font=u'Yu Gothic UI',
    pos=[-.7, -.8], height=0.1, wrapWidth=None,
    color=u'tomato', colorSpace='rgb', opacity=1,
    depth=0.0)	
	m_instruction = visual.TextStim(win=win, ori=0, name='m_instruction',
    text=m_text,    font=u'Yu Gothic UI', alignHoriz = "right",
    pos=[.7, -.8], height=0.1, wrapWidth=None,
    color=u'lightseagreen', colorSpace='rgb', opacity=1,
    depth=0.0)

Feedback_Screen = visual.TextStim(win=win, ori=0, name='Feedback_Screen',
    text="Placeholder_text",    font=u'Arial',
    pos=[0, 0], height=0.09, wrapWidth=None,
    color=u'black', colorSpace='rgb', opacity=1,
    depth=0.0)	
	

# Create some handy timers
globalClock = core.Clock()  # to track the time since experiment started
routineTimer = core.CountdownTimer()  # to track time remaining of each (non-slip) routine 



z_instruction.setAutoDraw(True)
m_instruction.setAutoDraw(True)
Button_Instructions.setAutoDraw(True)  # automatically draw every frame
win.flip()
core.wait(5.0)
Button_Instructions.setAutoDraw(False)

#reps = len(block)
block_counter=0

for block in blocks:

	# set up handler to look after randomisation of conditions etc
	trials = data.TrialHandler(nReps=len(block), method='random', 
		extraInfo=expInfo, originPath=None,
		trialList=[None],
		seed=None, name='trials')
	thisExp.addLoop(trials)  # add the loop to the experiment
	thisTrial = trials.trialList[0]  # so we can initialise stimuli with some values
	# abbreviate parameter names if possible (e.g. rgb=thisTrial.rgb)
	if thisTrial != None:
		for paramName in thisTrial.keys():
			exec(paramName + '= thisTrial.' + paramName)

	#create trial_counter
	trial_counter=0
	wrong_counter=0
	response_time_counter=0

	
	for thisTrial in trials:
		currentLoop = trials
		# abbreviate parameter names if possible (e.g. rgb = thisTrial.rgb)
		if thisTrial != None:
			for paramName in thisTrial.keys():
				exec(paramName + '= thisTrial.' + paramName)
	
	

		
		#update zoids
		update_stimuli(block[trial_counter],Zoid_Left,Zoid_Right)
		
		
		
		#------Prepare to start Routine "trial"-------
		t = 0
		trialClock.reset()  # clock 
		frameN = -1
		# update component parameters for each repeat
		Response = event.BuilderKeyResponse()  # create an object of type KeyResponse
		Response.status = NOT_STARTED
		# keep track of which components have finished
		trialComponents = []
		trialComponents.append(Orientation_Cue)
		trialComponents.append(Ready_Cue)
		trialComponents.append(Response)
		trialComponents.append(Zoid_Left)
		trialComponents.append(Zoid_Right)
		for thisComponent in trialComponents:
			if hasattr(thisComponent, 'status'):
				thisComponent.status = NOT_STARTED
		
		#-------Start Routine "trial"-------
		continueRoutine = True
		while continueRoutine:
			# get current time
			t = trialClock.getTime()
			frameN = frameN + 1  # number of completed frames (so 0 is the first frame)			
			
			# *Orientation_Cue* updates
			if t >= 0.0 and Orientation_Cue.status == NOT_STARTED:
				# keep track of start time/frame for later
				Orientation_Cue.tStart = t  # underestimates by a little under one frame
				Orientation_Cue.frameNStart = frameN  # exact frame index
				Orientation_Cue.setAutoDraw(True)
			if Orientation_Cue.status == STARTED and t >= (0.0 + (2-win.monitorFramePeriod*0.75)): #most of one frame period left
				Orientation_Cue.setAutoDraw(False)
			
			# *Ready_Cue* updates
			if t >= 2.0 and Ready_Cue.status == NOT_STARTED:
				# keep track of start time/frame for later
				Ready_Cue.tStart = t  # underestimates by a little under one frame
				Ready_Cue.frameNStart = frameN  # exact frame index
				Ready_Cue.setAutoDraw(True)
			if Ready_Cue.status == STARTED and t >= (2.0 + (.5-win.monitorFramePeriod*0.75)): #most of one frame period left
				Ready_Cue.setAutoDraw(False)
			
			# *Response* updates
			if t >= 2.5 and Response.status == NOT_STARTED:
				# keep track of start time/frame for later
				Response.tStart = t  # underestimates by a little under one frame
				Response.frameNStart = frameN  # exact frame index
				Response.status = STARTED
				# keyboard checking is just starting
				win.callOnFlip(Response.clock.reset)  # t=0 on next screen flip
				event.clearEvents(eventType='keyboard')
			if Response.status == STARTED:
				theseKeys = event.getKeys(keyList=['z', 'm'])
				
				# check for quit:
				if "escape" in theseKeys:
					endExpNow = True
				if len(theseKeys) > 0:  # at least one key was pressed
					Response.keys = theseKeys[-1]  # just the last key pressed
					Response.rt = Response.clock.getTime()
					# was this 'correct'?
					if (Response.keys == str(u"'z'")) or (Response.keys == u"'m'"):
						Response.corr = 1
					else:
						Response.corr = 0
					# a response ends the routine
					continueRoutine = False
			
			# *Zoid_Left* updates
			if t >= 2.5 and Zoid_Left.status == NOT_STARTED:
				# keep track of start time/frame for later
				Zoid_Left.tStart = t  # underestimates by a little under one frame
				Zoid_Left.frameNStart = frameN  # exact frame index
				Zoid_Left.setAutoDraw(True)
			if Zoid_Left.status == STARTED and (Response.status==FINISHED):
				Zoid_Left.setAutoDraw(False)
			
			# *Zoid_Right* updates
			if t >= 2.5 and Zoid_Right.status == NOT_STARTED:
				# keep track of start time/frame for later
				Zoid_Right.tStart = t  # underestimates by a little under one frame
				Zoid_Right.frameNStart = frameN  # exact frame index
				Zoid_Right.setAutoDraw(True)
				if Zoid_Right.status == STARTED and (Response.status==FINISHED):
					Zoid_Right.setAutoDraw(False)
			
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
		if Response.keys in ['', [], None]:  # No response was made
			Response.keys=None
			# was no response the correct answer?!
			if str(u"'y'").lower() == 'none': Response.corr = 1  # correct non-response
			else: Response.corr = 0  # failed to respond (incorrectly)
		# store data for trials (TrialHandler)
		
		#determines what the correct answer was
		if (block[trial_counter][0][0] == block[trial_counter][1][0]):
			correct_response = same
		else:
			correct_response = diff

		#determines whether the human answer was correct
		if correct_response != Response.keys[-1]:
			wrong_counter+=1
						
		trials.addData('Block_Number',block_counter) # 5 blocks of 121 trial each
		trials.addData('Trial_Number',trial_counter) # position within a block
		trials.addData('Subject_Key',Response.keys) # subject response key press
		trials.addData('Correct_Key', correct_response) # the correct response key press
		trials.addData('Subject_Response', key_to_answer(Response.keys[-1], samediff_key_map)) # what the subject indicated by the key they pressed (same or different)
		trials.addData('Correct_Response', key_to_answer(correct_response, samediff_key_map)) #what the correct answer was
		trials.addData('Answered_Correctly', correct_response == Response.keys[-1])  # TRUE if subject answered correctly, FALSE if not
		trials.addData('Left_Zoid', verts_to_name(block[trial_counter][0][0]))
		trials.addData('Left_Zoid_Orientation', block[trial_counter][0][1])
		trials.addData('Right_Zoid', verts_to_name(block[trial_counter][1][0]))
		trials.addData('Right_Zoid_Orientation', block[trial_counter][1][1])#stimuli
		
		#iterate trial_counter
		trial_counter+=1
		
		if Response.keys != None:  # we had a response
			trials.addData('Response.rt', Response.rt)
			response_time_counter+=Response.rt
		# the Routine "trial" was not non-slip safe, so reset the non-slip timer
		routineTimer.reset()
		thisExp.nextEntry()
		
	# completed n repeats of 'trials'
	update_feedback_adaptive(trial_counter, wrong_counter, response_time_counter, "pre")
	Feedback_Screen.setAutoDraw(True)
	Feedback_Screen.tStart = t  # underestimates by a little under one frame
	Feedback_Screen.frameNStart = frameN  # exact frame index
	win.flip()
    # self-paced break (3+287+10=300s max)
	core.wait(3) # block key inputs for the first 3 seconds, avoiding accidental key press
	break_time = 290 # normal break time, can be interrupted with key press (300 - 3 - 10s)
	if(DEBUG_MODE):
		break_time = 5
	break_timer = core.Clock() 
	while(1):
		core.wait(0.5, 0.5)
		if (event.getKeys(keyList=['z', 'm'])):
			break
		if (break_timer.getTime()>break_time):
			break
	# A reminder of the breaking is ending
	update_feedback_adaptive(trial_counter, wrong_counter, response_time_counter, "post")
	win.flip()
	core.wait(10) # ending screen will be there for 7 seconds
	# clear All and loop to the next block 
	Feedback_Screen.setAutoDraw(False)
	win.flip()
	
	#iterate block counter
	block_counter+=1
	
# these shouldn't be strictly necessary (should auto-save)
thisExp.saveAsWideText(filename+'.csv')
thisExp.saveAsPickle(filename)
logging.flush()
# make sure everything is closed down
thisExp.abort() # or data files will save again on exit
win.close()
core.quit()
