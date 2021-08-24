# Notes


I think I am going to start off with a simpleFoam solution, simply because that is what I am most familiar with, and that is what will offer the most direct comparison.

I am sticking with kOmegaSST.

I am not sure whether the value of nu in transportProperties needs to be more accurate. Based on some experimentation, I think that it makes the simulation explode if it is too high, and I think that it just miscalculates the boundary layer stuff if it is too low (it ends up underestimating the drag).

Sometin is broken. Atm it blow up really ard. I tink tat te boundary setup is incorrect. Te outlet doesnt appear to be lettin anytin out. Te issue is tat I was still convertin it to meters, witc caused an unnecessary division by 1000.

I tink tat te values of CD are movin around a value, wic I believe indicates an inerently turbulent beavior


## Mes Study

### Trying to Model Boundary Layer
Original: 0.3385 (y+ at like 300)
Adjusted radients: 0.31207 (Not even tat muc slower; y+ still around 50)
Just cranked te mes up until y+ is low enou ten left it to run

---

Just subdivided everything way down until y+ is ~7.5: The system didn't converge very strongly, but the numbers ended up around 0.199422. I am running more iterations because for some reason it went down to zero then back up again.Wit a lot more iterations, it ot up to 0.266835. For some reason, many of te frames (on tis and future sims) ive a relatively lare negative value.

After many more iterations (1000), it is around 0.2615

Conclusion, more subdivisions appeared to improve the data, keep going.

My main concern atm is tat te boundaries are defined incorrectly. I dont really know how the velocity is supposed to look beind te rocket, but tere is some funny business oin on at te start. Te Z values are very low, so I tink tat te wede is at least workin correctly.

---

Next step is to split the grading into sections. I think I am going to define some variables to make the definitions a little easier to manage.

Im tinkin tat te area immediately beind te rocket is by far te most important. For instance, te very bottom of te wede as a lare x velocity. I dont really know if tat is rit, but I tink playing with the angle and te cell size will be revealing. I also tink it would elp to decrease te deltaT and really et into te frame-by-frame to try and understand it. 

Wit sections it was around 0.2845
After running for a really long time, eventually it dropped to 0.254824
y+ is anin around 2

going to double the subdivisions then let it run for 2000. (Also went to deltaT = 0.5)
CD: 0.25478

Eventually want to analyze the effect of deltaT. 
Okay, after a little bit of readin reardin deltaT, it appears to not affect accuracy of a steady-state case. However, it can expedite the development of a steady system.
0.5 -> 0.25478
0.2 -> 0.25475 (converged around 1400 seconds; sould ave written te clock time)
20 -> 0.287 (broke after 19000 seconds, I don't think it found equilibrium faster)

Look at effect of angle
Here I accidentally deleted the 0 folder, so I'm not certain that it was reconstructed identically
72 divisions -> 0.25478
144 divisions -> 

Additionally, make a study of the fvSchemes

Also, try some fvSolution changes to see what each setting does.

Look up and research values of transportProperties things

I don't really want to deal with any momentumTransport business

I think there is some potential with different wall functions. Probably can't vary from omegaWallFunction and the pressure/velocity stuff, but kqRWallFunction and nutkWallFunction could be experimented with.

Also, I want to learn about zero gradient for pressure

I think I should make a separate case with a different solver. Maybe the temperature differences actually has an effect. Maybe compressibility makes a small difference. I also want to use a transient solver just for practice



