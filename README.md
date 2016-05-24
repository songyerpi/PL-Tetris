# PL-Tetris

##Installation

You'll need PsychoPy and its dependencies to run PL-Tetris.

To install, go [here,](http://www.psychopy.org/installation.html) and choose your OS's installation.  This will install the standalone GUI editor, as well as the python libraries.  The program was initially made in the GUI editor, but has been edited beyond it to get extra functionality the GUI editor does not support.  The GUI editor itself cannot load or run the PL-Tetris python script.  

To run the program, either run it from the command line, or run it from within PsychoPy's script editor.  The second option should probably work even if the first does not.  

##Documentation

PL-Tetris is a perceptual learning task where you are presented with two Tetris pieces, or zoids, and are asked to determine whether they are the same block, or are two different blocks.  One tetris piece is considered to be identical to another if it can be rotated to be the same as the other piece, as can be done in the actual game of Tetris.  Pieces which are mirror images of each other (i.e. L and J, or S and Z) are not identical.  

For each presentation of stimuli, the subject will be presented with three screens in sequence:

| Screen | Presented | Duration |
|:----|:----|:----|
| orientation cue | + | 2.0 seconds |
| ready cue | ○ | 0.5 seconds |
| stimuli | two Tetris zoids | until the user presses a key |

When the subject sees the stimuli, they will indicate whether the two Tetris pieces are the same or different by pressing either the "m" or the "x" key on your keyboard.  Which key corresponds to which answer is randomized for every subject to eliminate it as a confounding factor.  

The task consists of 5 blocks of 121 stimuli pairs.  There are 305 matching pairs, and 300 disparate pairs.  Each block contains a randomized ordering of 60 disparate pairs (one-fifth of the set of possible non-matching pairs) and 61 matching pairs (there are 61 possible distinguishable matching pairs, and the full set of matching pairs is added to each block).  There will be no repeats among the non-matching pairs, and each matching pair should appear once per block.  

Repeats have been allowed among the matching pairs to ensure that there is an even balance of matches and non-matches presented.  If each stimuli pair was only presented once, a subject would get ~80% accuracy simply by indicating "different" each time.  

After each of the five blocks, a feedback screen is presented.  It gives the accuracy percentage (number correct/total) and the average response time (in seconds) for that block.  If the subject scored higher than 96% accuracy, they will be told to focus on decreasing their response speed.  If they score lower than 94% accuracy, they will be told to take more time on each stimuli pair to increase their accuracy.  If they score between 94% and 96%, they will simply be told "Good job!"

The threshhold values can be changed in the `update_feedback_adaptive` function (the variables are `speed_up` and `slow_down`)

The tetris pieces are generated using a list of vertices, which are specified for each shape.  Currently the vertices use a centimeter as the "unit" size, and are 5 cm from the center of the screen.  These values were arbitrarily determined, and should probably be changed to percentage of monitor size.  To change these values, change the `units` value under where `Zoid_Right` and `Zoid_Left` are initialized, the `pos` value which specifies where the stimuli is placed on the screen, and multiply the values in the list of vertices by a coefficient that gives you the desired dimensions.  
