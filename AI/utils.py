from random import uniform

def weighted_choice(choices):
   total = sum( w for c, w in choices.items() )
   r = uniform(0, total)
   upto = 0
   for c, w in choices.items():
      if upto + w >= r:
         return c
      upto += w
   assert False, "Shouldn't get here"

