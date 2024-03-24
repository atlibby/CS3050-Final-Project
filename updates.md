Use this to update the team on what it is you added to the repo!

2/26 this text document - Reuben


3/1  added a room class


3/4 added a Card class - Steven


3/24 edited die functionality such that the die can be clicked on to roll it.
In main, at the beginning of the initialization of the ClueGame window,
initialized the die object. In the on_draw() func in main, added Die.draw(),
and in the on_mouse_click() func in main, added the functionality for the die
to change when the mouse is within the area of the die. Also, added a bool in the 
game class called self.die_rolled which is set to false, which turns true when
the die is rolled. The die can only be rolled if die_rolled is false,
so the die can only be rolled once. This is to be tied into turns, so that die_rolled
can be false again later to reset it. - Steven

todo ( steven ):
-see if you can make the die roll for 3 seconds then stop at a number.
-make it so that die is drawn, die is rolled, then die is cleared.