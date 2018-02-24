# youtube-cli
Watch Youtube videos from the command line interface (with a video player)

How to obtain a Youtube API key: https://developers.google.com/youtube/v3/getting-started

Use example:

    Call:
	./youtube-cli.py -q 'joule thief' -l 6

    Output:

	1 Supercapacitor Joule Thief
	  Previous video: https://youtu.be/WRm2oUw4owE Facebook:
	  https://www.facebook.com/greatscottlab Twitter:
	  https://twitter.com/GreatScottLab Support me for more videos:
  	  https://www.patreon.com/GreatSc...
  	  ~GreatScott!
  	  https://www.youtube.com/watch?v=jq7cqmDtZDc 

	2 How to make an authentic Joule Thief.				     
	  On the basis that it's me who actually named the Joule Thief,	     
	  it's about time I actually put up a video showing how to make	     
	  one. This video shows a version that is true to the original	     
	  design...							     
	  ~bigclivedotcom						     
	  https://www.youtube.com/watch?v=K53beWYdIpc 			     
									     
	3 How a Joule Thief Works					     
	  Step-by-step run through of how a Joule Thief circuit works.	     
	  Includes how all the parts, the 1.5 volt AA battery, the	     
	  resistor, the transistor and the ferrite core with its two coils   
	  of wire...							     
	  ~RimstarOrg							     
	  https://www.youtube.com/watch?v=0GVLnyTdqkg 			     
									     
	4 Joule Thief Battery Charger					     
	  In this project, Jason Poel Smith shows you how to make a low-     
	  voltage battery charger using a Joule Thief circuit. This	     
	  circuit lets you charge batteries using a power source whose	     
	  voltage...							     
	  ~Make:							     
	  https://www.youtube.com/watch?v=I8W20uwtJ3Y 			     
									     
	5 All You Ever Wanted To Know About The Joule Thief		     
	  All You Ever Wanted To Know About The Joule Thief - but where	     
	  afraid to ask your Mother lol.				     
	  ~Robert Murray-Smith						     
	  https://www.youtube.com/watch?v=N20gG6bDRlo

To play the 4th video from the above results list, call:

    ./youtube-cli.py -q 'joule thief' -l 6 -n 4

To play the first video from this list, call:

    ./youtube-cli.py -q 'joule thief' -l 6 -L

If you already know the number of a video and want to play it, you must
still provide original '-l' option from your previous call.

If you don't provide -q option, Youtube will response with a list of
most (recently) popular or promoted videos.

To get information about available options, call:

    ./youtube-cli.py --help

Not all use cases of this program have been tested, so some unknown bugs
are certainly still there.