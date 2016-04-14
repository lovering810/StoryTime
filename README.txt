README - simple_event_tagger.py

REQUIRED PACKAGES:

NodeBox Library: https://www.nodebox.net/code/index.php/Linguistics#loading_the_library

NLTK: http://www.nltk.org/


SERVER SETUP:

For this to run as intended, you need to set up a miniconda server to reduce the overhead of calling up a JVM for every sentence you want to parse. Make sure you have the version of Java you need, as well as CoreNLP itself (this is BIG, so make room and make time). Then set up your server (full instructions: http://eecs.io/python-environment-for-scientific-computing.html). Once you are in your server, tell it what you want it to be doing:

$ ~/miniconda3/bin/conda create -n parser python=2.7 -y
$ . ~/miniconda3/bin/activate parser
(parser) $ conda install -c https://conda.binstar.org/dimazest stanford-corenlp-python -y

And start your server up:

(parser) $ corenlp -S stanford-corenlp-full-2015-04-20

You should see:

Serving on http://127.0.0.1:8080 (or whatever you told it to serve on, I used the default).

You’re now ready to use simple_event_tagger.py on your folder of texts!

