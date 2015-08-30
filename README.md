# smart_cooker
# @owner mmartinez

<h2>
Overview
</h2>
<br/>
Checking in my work for my home grown raspberry pi
controlled sous vide cooker. Still probably needs some
work.
<br/>
This project has multiple external dependencies. It 
has a dependency on rpi_strogonanoff (until I figure 
out how to do repo dependency in git, I'll just include 
a link), linked below.
https://github.com/dmcg/raspberry-strogonanoff

Additionally, it has a dependency on postgres as well, 
you'll probably have to create a new user called 
"cooker" and then run the included smart_cooker.sql 
to create the appropriate tables that the app requires. 
This is recommended as it sets up some constraints that 
would be expected.

Lastly, it also has a dependency on plot.ly - you'll have
to follow the directions here: 
https://plot.ly/python/getting-started/
to work with it. It's actually a really good (and free)
graphing utility to create graphs that you can share.

