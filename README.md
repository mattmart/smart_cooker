# smart_cooker
# @owner mmartinez

Checking in my work for my home grown raspberry pi
controlled sous vide cooker. Still probably needs some
work.

This project has multiple external dependencies. It
 has a dependency on rpi_strogonanoff. It has a dependency
on postgres as well, you'll probably have to create a new
user called "cooker" and then run the included 
smart_cooker.sql to create the appropriate tables that 
the app requires. This is recommended as it sets up some
constraints that would be expected.
