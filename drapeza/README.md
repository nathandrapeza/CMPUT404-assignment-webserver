CMPUT404-assignment-webserver
=============================

CMPUT404-assignment-webserver

See requirements.org (plain-text) for a description of the project.

Make a simple webserver.

Contributors / Licensing
========================

Generally everything is LICENSE'D under the Apache 2 license by Abram Hindle.

server.py contains contributions from:

* Abram Hindle
* Eddie Antonio Santos
* Jackson Z Chang
* Mandy Meindersma 

But the server.py example is derived from the python documentation
examples thus some of the code is Copyright © 2001-2013 Python
Software Foundation; All Rights Reserved under the PSF license (GPL
compatible) http://docs.python.org/2/library/socketserver.html

Comments (drapeza):
- no collaboration
- os functionality to get size did not work, thus size (content length) is arbitrary
- Got a few mimetype errors that didn't make sense. I was sure I was returning either text/html\n\r or text/css\n\r, but there were assertion errors that I was doing text/plain. I failed 1 freetest and 3 (test html, test hardcode, and test css) tests from not free tests because of this. I'm not sure why I'm getting this error because I put the right mimetypes (can be checked by printing the response in the handle method).
