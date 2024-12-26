Hey! This is a script that expects you to have access to the game files,
but if you'd like to test it for yourself, it's possible to do so regardless.

Simply download main.py and Blender and create a new scene. Then, create an
object you'd like to run the script on. Add it as an add-on like any other, and
then locate the added menu by dragging the arrow on the top right to the left,
same as you would to gain access to the "View," "Tool," and "Item" tabs. There
should be a new tab called "Standable Ground." Select that and make sure the object
you would like to process is selected in the editor and then click the "Process
Ground" button. That should duplicate the object, hide the original, and recolor
the new object to show which parts of the ground can be stood on!

In the interest of keeping a few things obscure until I explore it further, I won't
outline nuances and the like for the time being, but this should be enough to get
anyone started.

There is only one way to change the "sensitivity" of the ground - how far tilted the
ground can be from facing up - and that appears on the bottom left after you process an object.
Just slide the value up and down to allow for bigger or smaller angles.

For those of you curious, the angle in question is the distance between each faces' normal
and the Z axis.
