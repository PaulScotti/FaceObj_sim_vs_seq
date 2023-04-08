#!/usr/bin/env python

''' 
2023 Paul Scotti
Simultaneous Face-Object 3AFC Task
'''

##############################################
###        SETUP FOR THE EXPERIMENT        ###
##############################################

import time
import random
from psychopy import core, visual, monitors, data, logging, event, tools
import os  # handy system and path functions
import sys  # to get file system encoding
import numpy as np

sub_num = '999' # must be a positive number
curSubj = f'sub-{sub_num}'
experiment_type = 'simultaneous'
demo = False
fullscreen = True

parent = os.path.abspath(os.path.join(os.getcwd(), os.pardir))
root_path = parent+'/stimuli/'
face_path = root_path + 'face_triangles/'
obj_path = root_path + 'objects_seq_v_sim/object'

if demo:
    display_time = 500
    isi = 50
    iti = 50
    afc_time = 1500
    feed_iti = 1000
    num_study_repetitions = 2
    num_blocks = 2
    num_study_stim = 6
else:
    display_time = 2000
    isi = 200
    iti = 1200
    afc_time = 2500
    feed_iti = 1000
    num_study_repetitions = 2
    num_blocks = 2
    num_study_stim = 6

# increasing doppelganger_distance means more dissimilar doppelganger (min=20 max=80)
doppelganger_distance = 60

# trigger = 'equal'
ansKeys = ['1','2','3','4']

visDeg = 10
afc_visDeg = 6
fix_height = 119.46
text_height = 50.7
wrap_width = 1292
radius_dim = .1

if demo:
    print("\n\n\n--------WARNING! IN DEMO MODE--------\n\n\n")

cur_dir = os.getcwd()
print("cur_dir", cur_dir)

expName = experiment_type
expInfo = {'subjName': curSubj}
expInfo['date'] = data.getDateStr()
expInfo['expName'] = expName
filename = u'data/%s/%s_%s' % (expInfo['subjName'], expInfo['subjName'], expName) 
print(f"filename: {filename}")
print(f"\n====SUBJECT {curSubj}====\n")

# Save a log file for detail verbose info
if os.path.exists(filename+'.log') and demo==False:
    print(f"{filename}.log already exists. Make sure you are not overwriting data!")
    core.quit()
try:
    logFile = logging.LogFile(filename+'.log', level=logging.EXP, filemode='w')
except:
    os.mkdir(f"data/{curSubj}")
    logFile = logging.LogFile(filename+'.log', level=logging.EXP, filemode='w')
logging.console.setLevel(logging.WARNING)  # this outputs to the screen, not a file

# Setup the Window
# https://pni-facilities.princeton.edu/index.php/2020_changes_to_MRI_screen_distances
mon = monitors.Monitor('testMonitor')
mon.setDistance(89) # distance to screen (cm) [Skyra=89] [Prisma=107.5]
win = visual.Window(
    size=[1920,1080], fullscr=fullscreen, screen=0,
    allowGUI=True, allowStencil=False,
    monitor=mon, color=[0,0,0], colorSpace='rgb',
    blendMode='avg', useFBO=True, units='pix')
win.mouseVisible = False

# Store frame rate of monitor if we can measure it
frameRate = win.getActualFrameRate()
if frameRate != None:
    frameDur = 1.0 / round(frameRate)
else:
    frameDur = 1.0 / 60.0  # could not measure, so guess

image_stim = visual.ImageStim(
    win=win, units="deg",
    image='sin', mask=None,
    ori=0, pos=(0, 0), size=(visDeg, visDeg),
    color=[1,1,1], colorSpace='rgb', opacity=1,
    flipHoriz=False, flipVert=False,
    texRes=128, interpolate=False, depth=0.0)
image_left = visual.ImageStim(
    win=win, units="deg",
    image='sin', mask=None,
    ori=0, pos=(-visDeg/1.25, 0), size=(afc_visDeg, afc_visDeg),
    color=[1,1,1], colorSpace='rgb', opacity=1,
    flipHoriz=False, flipVert=False,
    texRes=128, interpolate=False, depth=0.0)
image_middle = visual.ImageStim(
    win=win, units="deg",
    image='sin', mask=None,
    ori=0, pos=(0, 0), size=(afc_visDeg, afc_visDeg),
    color=[1,1,1], colorSpace='rgb', opacity=1,
    flipHoriz=False, flipVert=False,
    texRes=128, interpolate=False, depth=0.0)
image_right = visual.ImageStim(
    win=win, units="deg",
    image='sin', mask=None,
    ori=0, pos=(visDeg/1.25, 0), size=(afc_visDeg, afc_visDeg),
    color=[1,1,1], colorSpace='rgb', opacity=1,
    flipHoriz=False, flipVert=False,
    texRes=128, interpolate=False, depth=0.0)
image_up = visual.ImageStim(
    win=win, units="deg",
    image='sin', mask=None,
    ori=0, pos=(0, visDeg/2.75), size=(visDeg, visDeg),
    color=[1,1,1], colorSpace='rgb', opacity=1,
    flipHoriz=False, flipVert=False,
    texRes=128, interpolate=False, depth=0.0)
left_outline = visual.Rect(
    win=win, units='deg', size=(afc_visDeg, afc_visDeg),
    ori=0, pos=(-visDeg/1.25, 0), lineWidth=20,
    colorSpace='rgb', lineColor=[-1,-1,-1],
    fillColor=None, opacity=None,
    depth=1, interpolate=False)
middle_outline = visual.Rect(
    win=win, units='deg', size=(afc_visDeg, afc_visDeg),
    ori=0, pos=(0, 0), lineWidth=20,
    colorSpace='rgb', lineColor=[-1,-1,-1],
    fillColor=None, opacity=None,
    depth=1, interpolate=False)
right_outline = visual.Rect(
    win=win, units='deg', size=(afc_visDeg, afc_visDeg),
    ori=0, pos=(visDeg/1.25, 0), lineWidth=20,
    colorSpace='rgb', lineColor=[-1,-1,-1],
    fillColor=None, opacity=None,
    depth=1, interpolate=False)
fixation = visual.TextStim(win=win, name='cross',
   text=u'+',
   font=u'Arial',
   pos=(0, 0), height=fix_height/2, wrapWidth=None, ori=0, 
   color=u'white', colorSpace='rgb', opacity=1,
   depth=0.0)
fixColor = visual.Circle(win=win, units="deg",
    radius=radius_dim,
    fillColor=[-1, -1, -1],
    lineColor=[-1, -1, -1])
wrongColor = visual.Circle(win=win, units="deg",
    radius=radius_dim,
    fillColor=[.9, 0, 0],
    lineColor=[.9, 0, 0])
rightColor = visual.Circle(win=win, units="deg",
    radius=radius_dim,
    fillColor=[0, .9, 0],
    lineColor=[0, .9, 0])
feedback_text = visual.TextStim(win=win, units="deg",
   text=u'X degrees away!',
   font=u'Arial',
   pos=(0, -visDeg/1.8), height=fix_height/120, wrapWidth=None, ori=0, 
   color=u'green', colorSpace='rgb', opacity=1,
   depth=0.0)
left_text = visual.TextStim(win=win, units="deg",
   text=u'1',font=u'Arial', bold=False,
   pos=(-visDeg/1.23,-visDeg/2.4), height=fix_height/100, wrapWidth=None, ori=0, 
   color=u'black', colorSpace='rgb', opacity=1,
   depth=0.0)
middle_text = visual.TextStim(win=win, units="deg",
   text=u'2',font=u'Arial', bold=False,
   pos=(0,-visDeg/2.4), height=fix_height/100, wrapWidth=None, ori=0, 
   color=u'black', colorSpace='rgb', opacity=1,
   depth=0.0)
right_text = visual.TextStim(win=win, units="deg",
   text=u'3',font=u'Arial', bold=False,
   pos=(visDeg/1.23,-visDeg/2.4), height=fix_height/100, wrapWidth=None, ori=0, 
   color=u'black', colorSpace='rgb', opacity=1,
   depth=0.0)

##############################################
###       CUSTOM FUNCTIONS                 ###
##############################################

def wait(ms):
    trialTimer.add(ms / 1000)
    while (trialTimer.getTime()>0):
        keys_pressed = event.getKeys()
        if "escape" in keys_pressed: core.quit()
        time.sleep(.02)

def text_and_wait(text):
    ready=False
    waiting = visual.TextStim(win, pos=[0, 0], text=text,
        height=text_height, wrapWidth=wrap_width)
    waiting.draw()
    win.flip()
    while ready==False:
        keys_pressed = event.getKeys()
        if "escape" in keys_pressed: core.quit()
        if len(np.intersect1d(keys_pressed,ansKeys)):
            ready=True
        time.sleep(.02)

def shuffle_without_backtoback(faces,objects):
    ok = True
    zipped = list(zip(faces,objects))
    random.shuffle(zipped)
    for i,(f,o) in enumerate(zipped):
        if i==0:
            past_face = f
        else:
            if np.abs(f) == np.abs(past_face):
                ok = False
            past_face = f
            
    while not ok:
        ok2 = True
        random.shuffle(zipped)
        for i,(f,o) in enumerate(zipped):
            if i==0:
                past_face = f
            else:
                if np.abs(f) == np.abs(past_face):
                    ok2 = False
                past_face = f
        ok = ok2
            
    return zipped

def afc_wait(ms,corr_loc,image_left,image_middle,image_right):
    trialTimer.add(ms / 1000)
    resp_rt = -999
    afc_resp = 'none'
    while (trialTimer.getTime()>0):
        keys_pressed = event.getKeys()
        if "escape" in keys_pressed: core.quit()
        if len(np.intersect1d(keys_pressed,ansKeys)):
            image_left.draw()
            image_middle.draw()
            image_right.draw()
            if ("1" in keys_pressed): 
                resp_rt = (ms/1000) - trialTimer.getTime()
                left_text.bold = True
                left_text.draw()
            elif ("2" in keys_pressed): 
                resp_rt = (ms/1000) - trialTimer.getTime()
                middle_text.bold = True
                middle_text.draw()
            elif ("3" in keys_pressed): 
                resp_rt = (ms/1000) - trialTimer.getTime()
                right_text.bold = True
                right_text.draw()
            if resp_rt != -999:
                if corr_loc == 0:
                    afc_resp = 'corr'
                    afc_resp = 'novel'
                    afc_resp = 'lure'
                elif corr_loc == 1:
                    afc_resp = 'lure'
                    afc_resp = 'corr'
                    afc_resp = 'novel'
                elif corr_loc == 2:
                    afc_resp = 'novel'
                    afc_resp = 'lure'
                    afc_resp = 'corr'
            left_text.draw()
            middle_text.draw()
            right_text.draw()
            win.flip()
            left_text.bold = False
            middle_text.bold = False
            right_text.bold = False
        time.sleep(.02)
    return afc_resp, resp_rt

def study_sim(faces,scenes,path):
    # increase sizes for images from default
    image_left.size=(visDeg, visDeg)
    image_right.size=(visDeg, visDeg)
    left_outline.size=(visDeg, visDeg)
    left_outline.lineWidth=40
    right_outline.size=(visDeg, visDeg)
    right_outline.lineWidth=40

    trialTimer.reset(0)
    zipped = shuffle_without_backtoback(faces,scenes)
    for face,scene in zipped:
        # Study Face
        target_loc = np.random.randint(2)
        if face>0:
            if target_loc==0: # target_loc 0 means the to-be-highlighted face will be on the left
                image_left.setImage(face_path+str(np.abs(face))+'_20.jpg')
                image_right.setImage(face_path+str(np.abs(face))+f'_{doppelganger_distance}.jpg')
            else:
                image_right.setImage(face_path+str(np.abs(face))+'_20.jpg')
                image_left.setImage(face_path+str(np.abs(face))+f'_{doppelganger_distance}.jpg')
        else:
            if target_loc==0:
                image_right.setImage(face_path+str(np.abs(face))+'_20.jpg')
                image_left.setImage(face_path+str(np.abs(face))+f'_{doppelganger_distance}.jpg')
            else:
                image_left.setImage(face_path+str(np.abs(face))+'_20.jpg')
                image_right.setImage(face_path+str(np.abs(face))+f'_{doppelganger_distance}.jpg')
        image_left.draw()
        image_right.draw()
        win.flip()
        wait(display_time)

        # Highlight time
        if face>0:
            if target_loc==0: # target_loc 0 means the to-be-highlighted face will be on the left
                image_left.setImage(face_path+str(np.abs(face))+'_20.jpg')
                image_right.setImage(face_path+str(np.abs(face))+f'_{doppelganger_distance}.jpg')
            else:
                image_right.setImage(face_path+str(np.abs(face))+'_20.jpg')
                image_left.setImage(face_path+str(np.abs(face))+f'_{doppelganger_distance}.jpg')
        else:
            if target_loc==0:
                image_right.setImage(face_path+str(np.abs(face))+'_20.jpg')
                image_left.setImage(face_path+str(np.abs(face))+f'_{doppelganger_distance}.jpg')
            else:
                image_left.setImage(face_path+str(np.abs(face))+'_20.jpg')
                image_right.setImage(face_path+str(np.abs(face))+f'_{doppelganger_distance}.jpg')
        if target_loc==0:
            left_outline.lineColor=[.5,.5,0] # yellow
            left_outline.draw()
            left_outline.lineColor=[-1,-1,-1]
        else:
            right_outline.lineColor=[.5,.5,0]
            right_outline.draw()
            right_outline.lineColor=[-1,-1,-1]
        image_left.draw()
        image_right.draw()
        win.flip()
        wait(display_time)

        # ISI
        fixColor.draw()
        win.flip()
        wait(isi)

        # Study Scene/Object
        image_stim.setImage(path+str(scene)+'.jpg')
        image_stim.draw()
        win.flip()
        wait(display_time)

        # ITI
        fixColor.draw()
        win.flip()
        wait(iti)
    # reset size for subsequent 3AFC
    image_left.size=(afc_visDeg, afc_visDeg)
    image_right.size=(afc_visDeg, afc_visDeg)
    left_outline.size=(afc_visDeg, afc_visDeg)
    left_outline.lineWidth=20
    right_outline.size=(afc_visDeg, afc_visDeg)
    right_outline.lineWidth=20

def obj_afc(faces,objects):
    trialTimer.reset(0)
    resps = np.repeat("none",len(faces))
    rts = np.zeros(faces.shape)
    zipped = shuffle_without_backtoback(faces,objects)
    for face,obj in zipped:
        ii = np.where(face==faces)[0][0]
        # Study Face
        if face>0:
            image_stim.setImage(face_path+str(face)+'_20.jpg')
        else:
            image_stim.setImage(face_path+str(-face)+f'_{doppelganger_distance}.jpg')
        image_stim.draw()
        win.flip()
        wait(display_time)

        # ISI
        fixColor.draw()
        win.flip()
        wait(isi)

        # Select Object (3AFC)
        corr_loc = np.random.randint(3)
        alt_obj = objects_all[faces_all==-face][0]
        rand_obj = objects_all[np.random.randint(len(objects_all))]
        while rand_obj == alt_obj or rand_obj == obj:
            rand_obj = objects_all[np.random.randint(len(objects_all))]
        if corr_loc==0: # correct on left
            image_left.setImage(obj_path+str(obj)+'.png')
            image_middle.setImage(obj_path+str(rand_obj)+'.png')
            image_right.setImage(obj_path+str(alt_obj)+'.png')
        elif corr_loc==1: # correct in middle
            image_left.setImage(obj_path+str(alt_obj)+'.png')
            image_middle.setImage(obj_path+str(obj)+'.png')
            image_right.setImage(obj_path+str(rand_obj)+'.png')
        elif corr_loc==2: # correct on right
            image_left.setImage(obj_path+str(rand_obj)+'.png')
            image_middle.setImage(obj_path+str(alt_obj)+'.png')
            image_right.setImage(obj_path+str(obj)+'.png')
        else:
            error
        image_left.draw()
        image_middle.draw()
        image_right.draw()
        right_text.draw()
        middle_text.draw()
        left_text.draw()
        win.flip()
        afc_resp, resp_rt = afc_wait(afc_time,corr_loc,image_left,image_middle,image_right)
        resps[ii] = afc_resp
        rts[ii] = resp_rt

        # ISI
        fixColor.draw()
        win.flip()
        wait(isi)

        # Feedback
        image_left.draw()
        image_middle.draw()
        image_right.draw()
        if corr_loc:
            right_outline.lineColor=[0,1,0]
            right_outline.draw()
            right_outline.lineColor=[-1,-1,-1]
            if not afc_resp:
                left_outline.lineColor=[1,0,0]
                left_outline.draw()
                left_outline.lineColor=[-1,-1,-1]
        else:
            left_outline.lineColor=[0,1,0]
            left_outline.draw()
            left_outline.lineColor=[-1,-1,-1]
            if not afc_resp:
                right_outline.lineColor=[1,0,0]
                right_outline.draw()
                right_outline.lineColor=[-1,-1,-1]
        win.flip()
        wait(display_time)

        # ITI
        fixColor.draw()
        win.flip()
        wait(iti)

        if results == {}:
            results['face'] = [face]
            results['obj'] = [obj]
            results['alt_obj'] = [alt_obj]
            results['rand_obj'] = [rand_obj]
            results['afc_resp'] = [afc_resp]
            results['resp_rt'] = [resp_rt]
        else:
            results['face'].append(face)
            results['obj'].append(obj)
            results['alt_obj'].append(alt_obj)
            results['rand_obj'] = [rand_obj]
            results['afc_resp'].append(afc_resp)
            results['resp_rt'].append(resp_rt)
        np.save(f"{filename}_objafc", results)
    return resps, rts

##############################################
###                   TASK                 ###
##############################################
start_time = time.time()
globalClock = core.Clock()  # global time tracking for saving expt onsets
trialTimer = core.CountdownTimer()  # (non-slip) timing for stimulus presentation
results = {}

# MAIN EXPERIMENT #
random.seed(int(sub_num))
np.random.seed(int(sub_num))
faces_all = np.arange(5,5+num_study_stim)
# faces_all = np.random.permutation(np.arange(5,5+num_study_stim))
faces_all = faces_all[:num_study_stim//2]
faces_dopp = -faces_all
objects_all = np.random.permutation(np.arange(num_study_stim*2))
objects_all = objects_all[:num_study_stim] # 3 face spaces means 6 total associations

faces_all = np.hstack((faces_all,faces_dopp)) # negative numbered faces will be doppelgangers (aka pair B)

waiting = visual.TextStim(win, pos=[0, 0], text="Loading images... (may take a minute)",name="Waiting",height=text_height, wrapWidth=wrap_width)
waiting.draw()
win.flip()

# buffer images
for j in range(5,5+num_study_stim):
    for i in [doppelganger_distance,20]:
        image_left.setImage(face_path+f'{j}_{i}.jpg')
        image_left.draw()
        image_right.setImage(face_path+f'{j}_{i}.jpg')
        image_right.draw()
    image_left.setImage(face_path+f'placeholder.jpg')
    image_left.draw()
    image_right.setImage(face_path+f'placeholder.jpg')
    image_right.draw()
    waiting = visual.TextStim(win, pos=[0, 0], text=f"Loading face images... ({(j-4)/6*100:.1f}%)",name="Waiting",height=text_height, wrapWidth=wrap_width)
    waiting.draw()
    win.flip()
for i,j in enumerate(objects_all):
    image_left.setImage(obj_path+str(j)+'.png')
    image_middle.setImage(obj_path+str(j)+'.png')
    image_right.setImage(obj_path+str(j)+'.png')
    image_middle.draw();image_right.draw();image_left.draw()

    image_left.setImage(face_path+f'placeholder.jpg')
    image_middle.setImage(face_path+f'placeholder.jpg')
    image_right.setImage(face_path+f'placeholder.jpg')
    image_right.draw();image_middle.draw();image_left.draw()

    waiting = visual.TextStim(win, pos=[0, 0], text=f"Loading object images... ({i/12*100:.1f}%)",name="Waiting",height=text_height, wrapWidth=wrap_width)
    waiting.draw()
    win.flip()

# Start experiment
for block in range(num_blocks):
    text=f'Study Task (Block {block+1}/{num_blocks})\n\nMemorize the face-object pairs. Two faces will be presented together on the screen, then one face will be highlighted.\nAn object will then appear, and the task is to\nmemorize the object paired with the highlighted face.\n\nPress any key (1/2/3) to continue.'
    text_and_wait(text)
    for repetitions in range(num_study_repetitions):
        study_sim(faces_all,objects_all,path=obj_path)
    text=f'Memory Test (Block {block+1}/{num_blocks})\n\nYou will be shown a face, followed by three objects. Select the object associated with the face using your number keys.\n\nPress any key (1/2/3) to continue.'
    text_and_wait(text)
    obj_resps, obj_rts = obj_afc(faces_all,objects_all)
    print("obj_resps",obj_resps)

##############################################
###         Fixation to the end            ###
##############################################
total_time = (time.time()-start_time)/60
print(f"\n===Finished! Total Time (min.): {total_time:.02f}===")
waiting = visual.TextStim(win, pos=[0, 0], text=\
f"Finished! Press any button to exit.",
    name="Waiting",height=text_height, wrapWidth=wrap_width)
waiting.draw()
win.flip()

while True:
    keys_pressed = event.getKeys()
    if "escape" in keys_pressed: core.quit()
    if len(np.intersect1d(keys_pressed,ansKeys)): core.quit()