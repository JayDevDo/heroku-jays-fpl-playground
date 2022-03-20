#!/usr/bin/env python3
# pyFPL
# elements.py

import os
import time
import sys
import json
from urllib.request import urlopen

############################### ELEMENTS ####################################
#	In this script we deal with information	about ELEMENTS					#
#	(aka ballers / players ).												#
#  -----------------------------------------------------------------------  #
#	There are about 650 elements or footballers, players registered in FPL	#
#	Elements/players/ballers are sourced from FPL_ bootstrap_static.		#
#	Live data comes from 'fantasy.premierleague.com/api/event/{rnd}/live/'	#
#	and is only used for live.py.											#
#	Players are stored in the main global at index 3:						#
#																			#
# 		fplData = 	[														#
#						{	"rounds": [] }, #0 								#
#						{	"fixtures": [] }, #1							#
#						{	"clubs": [] }, #2								#
#	>>>					{	"players": [] }, #3						<<<		#
#						{	"ownteam": [] }, #4								#
#						{ 	"oppteam": [] }, #5								#
#						{	"LgH2h": [] }, #6								#
#						{	"LgCls": [] }, #7								#
#						{ 	"CrrntFxtrs": [] }, #8							#
#						{  	"lgManIds": [] }, #9							#
#						{   "oppId":   } #10								#
#					]														#
#																			#
#	FPL returns the following "ELEMENT" object (we call it baller):			#
#																			#
# 	{																		#
# 		"chance_of_playing_next_round": 100,								#
# 		"chance_of_playing_this_round": 100,								#
# 		"code": 446008,														#
# 		"cost_change_event": 0,												#
# 		"cost_change_event_fall": 0,										#
# 		"cost_change_start": 0,												#
# 		"cost_change_start_fall": 0,										#
# 		"dreamteam_count": 0,												#
# 		"element_type": 3,	------------->	1=GKP, 2=DEF, 3=MID, 4=FWD		#
# 		"ep_next": "4.0",													#
# 		"ep_this": "0.0",													#
# 		"event_points": 0,													#
# 		"first_name": "Bryan",												#
# 		"form": "4.0",														#
# 		"id": 96,															#
# 		"in_dreamteam": false,												#
# 		"news": "",															#
# 		"news_added": "2021-10-24T22:30:12.577421Z",						#
# 		"now_cost": 55,														#
# 		"photo": "446008.jpg",												#
# 		"points_per_game": "3.5",											#
# 		"second_name": "Mbeumo",											#
# 		"selected_by_percent": "2.4",										#
# 		"special": false,													#
# 		"squad_number": null,												#
# 		"status": "a",														#
# 		"team": 3,		------------------------> club.id					#
# 		"team_code": 94,													#
# 		"total_points": 52,													#
# 		"transfers_in": 588739,												#
# 		"transfers_in_event": 416,											#
# 		"transfers_out": 482908,											#
# 		"transfers_out_event": 704,											#
# 		"value_form": "0.7",												#
# 		"value_season": "9.5",												#
# 		"web_name": "Mbeumo",	--------> This we use most					#
# 		"minutes": 1277,													#
# 		"goals_scored": 3,													#
# 		"assists": 1,														#
# 		"clean_sheets": 4,													#
# 		"goals_conceded": 18,												#
# 		"own_goals": 0,														#
# 		"penalties_saved": 0,												#
# 		"penalties_missed": 0,												#
# 		"yellow_cards": 2,													#
# 		"red_cards": 0,														#
# 		"saves": 0,															#
# 		"bonus": 3,															#
# 		"bps": 124,															#
# 		"influence": "180.4",												#
# 		"creativity": "223.2",												#
# 		"threat": "368.0",													#
# 		"ict_index": "76.8",												#
# 		"influence_rank": 166,												#
# 		"influence_rank_type": 58,											#
# 		"creativity_rank": 66,												#
# 		"creativity_rank_type": 	47,										#
# 		"threat_rank": 36,													#
# 		"threat_rank_type": 21,												#
# 		"ict_index_rank": 46,												#
# 		"ict_index_rank_type": 29,											#
# 		"corners_and_indirect_freekicks_order": 3,							#
# 		"corners_and_indirect_freekicks_text": "",							#
# 		"direct_freekicks_order": 1,										#
# 		"direct_freekicks_text": "",										#
# 		"penalties_order": 2,												#
# 		"penalties_text": ""												#
#	}																		#
# 																			#
############################### ELEMENTS ####################################

import app.static.scripts.getData 	as mod_data
import app.static.scripts.curRound 	as mod_cr
import app.static.scripts.fixtures 	as mod_fxt
import app.static.scripts.clubs 	as mod_clb

global ballerArr
ballerArr = [];

global liveBallerArr
liveBallerArr = [];

el_cr = mod_cr.getCurrentRnd()

elmnts_file = "./app/static/data/static/elements.json"
live_ballers_file = "./app/static/data/live/active/liveBallers-" + str( el_cr ) + ".json"


def getElmnts(w):
	mod_data.infoRt(3)
	if( w =="r" ):
		data_elmnts = getRemoteElmnts()
	else:
		data_elmnts = getLocalElmnts()

	global ballerArr
	ballerArr = data_elmnts	
	return data_elmnts


def getLocalElmnts():
	global ballerArr
	if( len(ballerArr) > 100 ):
		# print("getLocalElmnts ballerArr", len( ballerArr ) )
		data_elmnts = ballerArr
	elif( os.path.exists( elmnts_file ) ):
		foelmnts = open( elmnts_file )
		data_elmnts = json.load(foelmnts)
		foelmnts.close
	else:
		# print("elmnts_file does NOT exists. using remote")
		data_elmnts = getRemoteElmnts()

	ballerArr = data_elmnts
	return data_elmnts


def getRemoteElmnts():
	response = getStatic("r")
	elf = open( elmnts_file, "w+")
	elf.write( json.dumps(response["elements"], indent=4) )
	elf.close
	mod_data.fplDataTS[3] == float(time.time())
	return response["elements"]


def getBaller(elId):
	global ballerArr
	if( len( ballerArr ) > 100 ):
		elmnts_static = ballerArr
	elif( os.path.exists( elmnts_file ) ):
		foStatic = open( elmnts_file )
		elmnts_static = json.load(foStatic)
		foStatic.close
	else:
		elmnts_static = getElmnts('r')

	if( len(elmnts_static) > 0 ):
		for b in elmnts_static:
			if( b["id"] == elId ):
				# print("elmnts_static", str(elId),"b", b)
				return b


def getBallerName(elId):
	return getBaller(elId)["web_name"]

def getBallerClub(elId):
	return getBaller(elId)["team"]

def getBallerPos(elId):
	return getBaller(elId)["element_type"]

def getLiveElements(w):
	mod_data.infoRt(11)
	if( w =="r" ):
		data_live_elmnts = getRemoteLiveBallers()
	else:
		data_live_elmnts = getLocalLiveBallers()

	global liveBallerArr
	liveBallerArr = data_live_elmnts	
	return data_live_elmnts


def getLocalLiveBallers():
	global liveBallerArr
	if( liveBallerArr ):
		# print("getLocalLiveBallers liveBallerArr", len( liveBallerArr ) )
		llbData = liveBallerArr
	elif( os.path.exists( live_ballers_file ) ):
		folvbllr = open( live_ballers_file )
		llbData = json.load(folvbllr)
		folvbllr.close
	else:
		llbData = getRemoteLiveBallers()

	return llbData


def getRemoteLiveBallers():
	doUpd = mod_data.infoRt(11)
	global liveBallerArr
	if( doUpd ):
		print("getRemoteLiveBallers infoRt 11", doUpd )
		url = "https://fantasy.premierleague.com/api/event/" + str( el_cr ) + "/live/"
		response = urlopen(url)
		data_live_elmnts = json.loads(response.read())
		liveBallerArr.clear()
		liveBallerArr = data_live_elmnts["elements"]
		relf = open( live_ballers_file, "w+")
		relf.write( json.dumps( liveBallerArr, indent=4) )
		relf.close
		mod_data.fplDataTS[11] = float(time.time())
	else:
		liveBallerArr = getLiveElements('l')

	return liveBallerArr


def getLiveBaller(elId):
	global liveBallerArr
	if( len(liveBallerArr) > 10 ):
		# print("getLiveBaller liveBallerArr", len( liveBallerArr ) )
		liveBallers = liveBallerArr
	else:
		liveBallers = getLocalLiveBallers()
	
	if( len(liveBallers) > 0 ):
		for lb in liveBallers:
			if( lb["id"] == elId ):
				# print("lb keys", lb.keys() )
				# print("lb['web_name']",  getBallerName(elId) )
				# print("lb['position']",  getBallerPos(elId) )
				# print("lb['event_points']", lb["event_points"] )
				if( ("explain" in lb.keys()) and (len(lb['explain']) > 0 ) ):
					# print("elId",elId,"lb['explain']",lb['explain'],"len",len(lb['explain']))
					if( "fixture" in lb['explain'][0].keys() ):
						return lb
					else:
						lb['explain']['fixture'] = 0
						return lb
				else:
					lb["explain"].append({'fixture': 0})
					return lb


def potentialSub(elId):
	liveInfo = getLiveBaller(elId)
	liveInfo.setdefault('explain', [{'fixture':0}] )
	liveInfo.setdefault('stats', [{'minutes':0}] )
	# print("elId", elId, "liveInfo", liveInfo )
	try:
		fxtrId = liveInfo['explain'][0]['fixture']
		mins = liveInfo['stats']['minutes']
	except Exception as e:
		# print("potentialSub", e, liveInfo)
		fxtrId = 0
		mins = 0
	finally:
		fxtrInfo = mod_fxt.getFixture( fxtrId )

	return ( ( mins<1 ) and ( fxtrInfo['finished']==True ) )
