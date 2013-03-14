symPy
=====

A prototype exploring player/shadow symetry interactions made using the pygame library. 

Probably largely inspired by "Braid."


#Concept

In this game we want to mess with symetry a bunch and then maybe insult space a bit.

There is a player character and a shadow character which have unified controls
however there is some sort of difference. For example the player character moves
right while the shadow moves left.

##Bi-phasic gameplay

1. The player figures out how to make the 2 charcters contact each other
2. The player figures out how to complete a level 
   ( enter both doors with characters, push a certain switch, kill the shadow 
     	  while living themselves)

Whenever contact is made between the charaters the control difference between 
the character and the shadow is changed in some way complicating the problem
or serving as a tool to complete the level.


##Advanced Mechanics

1. Wrap: Walls warp player around to another map edge making it so that symetry 
changes by flipping the player upside down or simply transporting them to a 
different location ( touching player and shadow may change the way wrap works in 
a level, right wall led to left wall changes to right wall leads to floor with the
player on their side).

2. Fall Time: fall time can be brought into the equation by allowing the player to
input commands while one of the characters is falling, resulting in a change in 
symetry-offset for the characters)


