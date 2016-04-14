#!/usr/bin/python
## February 22, 2016
## Author: Rebecca Lovering
## Simple Event Tagger


# For this to run correctly, must follow 
# instructions:http://www.eecs.qmul.ac.uk/~dm303/stanford-dependency-parser-nltk-and-anaconda.html

import json, jsonrpclib
import re
import glob
import nltk
from primEvent import prim_Event
from nltk.tokenize import sent_tokenize

server = jsonrpclib.Server("http://127.0.0.1:8080")

filelist = glob.glob('/Users/rebecca/Desktop/MAThesis/Data/YellowFairyBook/*.txt')

outfilepath = '/Users/rebecca/Desktop/MAThesis/Data/EventsYellow.txt'
outfile = open(outfilepath,'w')

# given a PRP/NNS tag, or presence of multiple in role, assigns number to role in event
def assignNum(event,role,op):

	singular = ["i","he","him","her","it","me","she","himself","yourself","herself","myself"]
	plural = ["we","they","us","them","ourselves","themselves"]
	role=role.lower()

	if role in singular or role=="NN":
		op(event,1)
	elif role in plural or role=="NNS" or len(prim_Event.Who(event))>1:
		op(event,2)

	return event

# given a PRP tag, assigns person to role in event		
def assignPer(event,role,op):

	first = ["i","me","we","us","myself","ourselves"]
	second = ["you","yourself","yourselves"]

	if role.lower() in first:
		op(event,1)
	elif role in second:
		op(event,2)
	else:
		op(event,3)

	return event

# if the event is not showing passivization, check to passivize.
def checkPassivity(role, event):

	if len(role) > 5 and role[-4]=="pass":
		prim_Event.setActPass(event,True)

	return event

# series of checks for initial event population
def checkRole(role, entry, rels, event):

	if prim_Event.getActPass(event) == False:
		event = checkPassivity(role, event)

	# there's only one of these per event, so no need to check
	if role == "root":
		prim_Event.setRoot(event,entry)

	elif role=="prt" and rels in prim_Event.doWhat(event):
		prim_Event.setRoot(event,entry)

	# here, though, it gets tricky.
	elif role[:6] == "nsubj" or role=="nsubj":
		# because root always comes back first, 
		# root will always be fixed by the time we get here.
		if rels in prim_Event.doWhat(event):
			prim_Event.setSubject(event,entry)

	elif role=="dobj" and rels in prim_Event.doWhat(event):
			prim_Event.setDobject(event, entry)

	elif role=="ccomp":
		prim_Event.setComp(event,entry)

	# now only picks up the first time mentioned - may turn out problematic
	elif role == "tmod": 
		if prim_Event.When(event)==():
			prim_Event.setTime(event,word)

	elif role=="advmod":
		prim_Event.setManner(event,word)

	# This is problematic for sentencess with multiple verbs, some negated.
	elif role=="neg" and rels in prim_Event.doWhat(event):
		prim_Event.setNegate(event, True)

	elif role=="prep":
		if prim_Event.getPrep(event)==():
			prim_Event.setPrep(event,entry)

	elif role[:4] =="pobj" or role=="pobj":
		if rels == prim_Event.getPrep(event):
			prim_Event.setPobj(event,entry)

	elif role=="conj:and":
		if rels in prim_Event.doWhat(event):
			prim_Event.setRoot(event,entry)
		elif rels in prim_Event.Who(event):
			prim_Event.setSubject(event,entry)
		elif rels in prim_Event.Object(event):
			prim_Event.setDobject(event, entry)
		elif rels in prim_Event.toWhat(event):
			prim_Event.setPobj(event, entry)

	elif role=="xcomp" and rels in prim_Event.doWhat(event):
		prim_Event.setRoot(event, entry)

	return event

# assigns a frequency float to subject, object, indirect object
# from count dictionaries
def assignImp(event, dicts2):

	doers, affectees, iobs, tot_dict = dicts2

	subjects = prim_Event.Who(event)
	objects = prim_Event.Object(event)
	iobjects = prim_Event.toWhat(event)

	classes = [(subjects,prim_Event.setPerson,prim_Event.setNumber,doers,prim_Event.setDoerImp,prim_Event.setDoerTimp),\
	 (objects,prim_Event.setDobjectPer,prim_Event.setDobjectNum,affectees,prim_Event.setEeImp,prim_Event.setObjTimp),\
	 (iobjects,prim_Event.setPobjPer,prim_Event.setPobjNum,iobs,prim_Event.setIobImp,prim_Event.setPobjTimp)]

	for classx in classes:
		classy,opper,opnum,dix,opimp,optimp = classx
		if len(classy)>0:
			for cl in classy:
				tergz = nltk.pos_tag([cl[0]])[0][1]
				if tergz[:4]=="PRP" or tergz[:3]=="NN":
					event=assignPer(event,cl[0],opper)
					event=assignNum(event,cl[0],opnum)
				elif cl[0] in dix.keys():
					val=dix[cl[0]]
					opimp(event,val)
					tval = tot_dict[cl[0]]
					optimp(event,tval)
					if tergz=="NNS":
						opnum(event,2)

	return event

# turns a dictionary of counts into a dictionary of probabilities
def normalize(dic):

	totes = float(sum(dic.values()))

	for key in dic.keys():

		dic[key]=dic[key]/totes

	return dic

# turn sentence counts to story length proportions
def propLen(item, n):
	current = prim_Event.getSentence(item)
	prim_Event.setSent(item,(current/n))
	return item

# write all event content to outfile
def write_event(event):

	ops = [prim_Event.getSentence,\
	prim_Event.doWhat,\
	prim_Event.getComp,\
	prim_Event.Who,\
	prim_Event.WhoPerson,\
	prim_Event.whoNumber,\
	prim_Event.howImp,\
	prim_Event.Object,\
	prim_Event.objPerson,\
	prim_Event.objNumber,\
	prim_Event.Impee,\
	prim_Event.getPrep,\
	prim_Event.toWhat,\
	prim_Event.ImpIobj,\
	prim_Event.When,\
	prim_Event.How,\
	prim_Event.getActPass,\
	prim_Event.Negate,\
	prim_Event.getVibe,\
	prim_Event.getStory_Imp,\
	prim_Event.getWhy_Story_Imp]

	eventline = ""

	for op in ops:
		if (type(op(event)) == list and len(op(event))==0):
			newline = "EMPTY\t"

		else:
			info = str(op(event))
			newline = "%s\t"%(info)

		eventline=eventline+newline

	return eventline

# main 
for filename in filelist:

    print filename

    f = open(filename, 'r')
    data = f.read()
    sents2 = sent_tokenize(data)

    parseds =[]

    for sent2 in sents2:
    	try:
    		parseds.append(json.loads(server.parse(sent2))[1])
    	except:
    		print sent2


    sent_dict = {}
    n=0.0

    event_list = []
    timeline = []

    doers = {}
    affectees = {}
    indobs = {}

    for parsed in parseds: #iterating through each sentence's dictionary in the list
    	n+=1
    	deps = parsed['sentences'][0]['dependencies']

    	event=prim_Event(sentence = n,root=[], comp=[],\
		subject=[], person=3, number=1, doerImp=0,\
		dobject=[], obj_person = 3, obj_num=1, eeImp=0,\
		prep=(),pobj=[],pobjnum=1,pobjper=3, iobImp=0,time=(), manner=(), \
		actpass=False, negate=False, vibe="neutral",story_imp=0,why_story_imp="N")

    	for dep in deps:

    		role, related, relpos, word, wordpos = dep 

    		entry = (word,wordpos)

    		rels = (related,relpos)

    		tag = nltk.pos_tag([word])[0][1]

    		if tag[:2]=="NN":
    			if role == "nsubj":
    				doers.setdefault(word,0)
    				doers[word] = doers[word]+1
    			elif role =="dobj":
    				affectees.setdefault(word,0)
    				affectees[word] = affectees[word]+1
    			elif role == "pobj":
    				indobs.setdefault(word,0)
    				indobs[word] = indobs[word]+1

    		event = checkRole(role,entry,rels,event)

    	timeline.append(event)

    dicts = [doers, affectees, indobs]
    tot_dict = {}

    #normalizing counts to probabilities
    for dic in dicts:
    	for key in dic:
			tot_dict.setdefault(key,dic[key])
			tot_dict[key] = tot_dict[key]+dic[key]

	dicts2 = [doers,affectees,indobs,tot_dict]
    for dic2 in dicts2:
    	dic2 = normalize(dic2)

    print len(timeline)

    for item in timeline:
    	item = assignImp(item,dicts2)
    	item = propLen(item,n)
    	prim_Event.calcVibe(item)
    	eventline = write_event(item)+"\n"
    	outfile.write(eventline)

outfile.close()
print "All done! Check %s for your data."%(outfilepath)
