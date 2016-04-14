##!/usr/bin/python
##
## February 25, 2016
## Author: Rebecca Lovering 
## 

import nltk
import en
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet as wn
wordnet_lemmatizer = WordNetLemmatizer()

class prim_Event:

	def __init__(self,sentence = float,root=[], comp=[],\
		subject=[], person=3, number=1, doerImp=0,doerTimp=0,\
		dobject=[], obj_person = 3, obj_num=1, eeImp=0,objTimp=0,\
		prep=(),pobj=[],pobjnum=1,pobjper=3, iobImp=0,pobjTimp=0,time=(), manner=(), \
		actpass=False, negate=False, vibe="neutral",story_imp=0,why_story_imp="N"):

		self.sentence = sentence 
		self.root = root #root
		self.comp = comp #ccomp
		self.subject = subject #nsubj
		self.person = person
		self.number = number
		self.doerImp = doerImp
		self.doerTimp = doerTimp
		self.dobject = dobject
		self.obj_person = obj_person
		self.obj_num = obj_num
		self.eeImp = eeImp
		self.objTimp = objTimp
		self.prep = prep #prep
		self.pobj = pobj #pobj
		self.pobjnum = pobjnum
		self.pobjper = pobjper
		self.iobImp = iobImp
		self.pobjTimp = pobjTimp
		self.time = time
		self.manner = manner
		self.actpass = actpass
		self.negate = negate
		self.vibe = vibe
		self.story_imp = story_imp
		self.why_story_imp=why_story_imp

# set all info
	def setSent(self,num):
		self.sentence = num
	def setRoot(self,newroot):
		self.root.append(newroot)
	def setComp(self,newcomp):
		self.comp.append(newcomp)
	def setSubject(self,newsub):
		self.subject.append(newsub)
	def setPerson(self,newper):
		self.person = newper
	def setNumber(self,newnum):
		self.number = newnum
	def setDoerImp(self,newimp):
		self.doerImp = newimp
	def setDoerTimp(self,newimp):
		self.doerTimp = newimp
	def setDobject(self,newdobj):
		self.dobject.append(newdobj)
	def setDobjectPer(self,newdobjper):
		self.obj_person = newdobjper
	def setDobjectNum(self, newdobjnum):
		self.obj_num = newdobjnum
	def setEeImp(self,neweeimp):
		self.eeImp = neweeimp
	def setObjTimp(self,newobjTimp):
		self.objTimp = newobjTimp
	def setPrep(self,newprep):
		self.prep = newprep
	def setPobj(self,newpobj):
		self.pobj.append(newpobj)
	def setPobjNum(self,newnum):
		self.pobjnum = newnum
	def setPobjPer(self,newper):
		self.pobjper = newper
	def setIobImp(self,newiobimp):
		self.iobImp = newiobimp
	def setPobjTimp(self,newpobjtimp):
		self.pobjTimp = newpobjtimp
	def setTime(self,newtime):
		self.time = (newtime)
	def setManner(self,newmanner):
		self.manner = newmanner
	def setActPass(self,newvoice):
		self.actpass = newvoice
	def setNegate(self,newneg):
		self.negate = newneg
	def setVibe(self,newvibe):
		self.vibe=newvibe
	def setMoreStuff(self,more):
		self.moreStuff.append(more)

	set_role_dict = {"subject":{"person":setPerson,"number":setNumber,"imp":setDoerImp,"totimp":setDoerTimp},\
	"object":{"person":setDobjectPer,"number":setDobjectNum,"imp":setEeImp,"totimp":setObjTimp},\
	"pobject":{"person":setPobjPer,"number":setPobjNum,"imp":setIobImp,"totimp":setPobjTimp}}

	def getRoles(self):
		return set_role_dict

# retrieve all info/methods for those that must be calculated
	def getSentence(self):
		return self.sentence
	def doWhat(self):
		return self.root
	def rootWhere(self):
		return self.rootInd
	def getComp(self):
		return self.comp
	def Who(self):
		return self.subject
	def WhoPerson(self):
		return self.person
	def whoNumber(self):
		return self.number
	def howImp(self):
		return self.doerImp
	def Object(self):
		return self.dobject
	def objPerson(self):
		return self.obj_person
	def objNumber(self):
		return self.obj_num
	def Impee(self):
		return self.eeImp
	def getPrep(self):
		return self.prep
	def toWhat(self):
		return self.pobj
	def ImpIobj(self):
		return self.iobImp
	def When(self):
		return self.time
	def How(self):
		return self.manner
	def getActPass(self):
		return self.actpass
	def Negate(self):
		return self.negate
	def getVibe(self):
		return self.vibe
	def getStory_Imp(self):
		return self.story_imp
	def getWhy_Story_Imp(self):
		return self.why_story_imp

	# calculating vibe (emotional content)
	def calcVibe(self):

		
		if self.root !=[]:
			rootverb = wordnet_lemmatizer.lemmatize(self.root[0][0],pos='v')
		else:
			rootverb=""

		how = wordnet_lemmatizer.lemmatize(self.manner,pos=wn.ADV)

		if self.dobject!=[]:
			obj = wordnet_lemmatizer.lemmatize(self.dobject[0][0])
		else:
			obj=""

		bits = [(en.verb.is_emotion,rootverb),\
		(en.noun.is_emotion,rootverb),\
		(en.adverb.is_emotion,how),\
		(en.noun.is_emotion,obj)]

		vibez = []

		for bit in bits:
			if type(bit[1])==unicode:
				vibez.append(bit[0](bit[1],boolean=False))

		for vib in vibez:
			if vib!=None:
				vibez=vib

			else:
				vibez="neutral"

		if self.negate == True:
			if vibez != "neutral":
				vibez2 = en.noun.antonym(vibez)
				if len(vibez2)<1:
					vibez="negated %s"%(vibez)
				else:
					vibez = vibez2[0]

		self.vibe = vibez

	# double check number for subject, object, and indirect object
	def checkNumbers(self):
		
		if len(self.subject)>1 and self.number==1:
			self.number=2

		if len(self.dobject)>1 and self.obj_num==1:
			self.obj_num=2

		if len(self.pobj)>1 and self.pobjnum==1:
			self.pobjnum=2
