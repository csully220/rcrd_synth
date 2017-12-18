import collections
import requests
import random
import logging
import os
from validator import Validator
import mido
from mido import MidiFile
from mido import Message
from mido import MetaMessage
import datetime

class WolfTonesSong:
    
    dl_url = 'https://www.wolframcloud.com/objects/user-a13d29f3-43bf-4b00-8e9b-e55639ecde19/NKMMusicDownload?id='
    genre_url = 'https://www.wolframcloud.com/objects/user-a13d29f3-43bf-4b00-8e9b-e55639ecde19/NKMNewID?genre=' 

    #hip hop, dance, blues, experimental
    #fav_genres = [45,40,55,90]
    #Pan Flute, brazilian bell, melodic tom, 
    wildcard_inst = [76, 114, 118]
    fav_genres = ['25', '45','40','55','60'] # ambient,hip hop, dance, blues, R&B

    def __init__(self):
        self.key = 60
        self.scale = []
        self.vld = Validator()
        #self.chan_roles = [0 for i in range(10)]
        self.ticks_per_beat = 0

        self.params = collections.OrderedDict( [
            ('genre','45'),   
            ('rule_type','15'),
            ('rule','10'),
            ('cyc_bdry','1'),
            ('seed','34444'),
            ('duration','21'),
            ('bpm','130'),
            ('npb','4'),
            ('scale','2050'),
            ('pitch','44'),
            ('mystery','0'),
            ('inst_1','31'),
            ('role_1','10'),
            ('inst_2','95'),
            ('role_2','135'),
            ('inst_3','0'),
            ('role_3','0'),
            ('inst_4','0'),
            ('role_4','0'),
            ('inst_5','0'),
            ('role_5','0'),
            ('perc','711')
        ] )

        self.filename = ''

    def set_param(self, key, value):
        if self.validate(key, value):
            self.params[key] = value
            return True
        return False
    
    def _nkm_encoded_id(self):
        enc_id = ''
        params = self.params.values()
        for val in params[:-1]:
            enc_id += val + '-'
        enc_id += params[-1]
        return enc_id

    def _send_url_request(self, enc_id=None):
        if(enc_id == None):
            nkm_id = 'NKM-G-' + self._nkm_encoded_id()
        else:
            nkm_id = enc_id 
            #logging.debug('WolfTones nkm id: ' +  str(nkm_id))
        r = requests.get(self.dl_url + nkm_id + '&form=MIDI')
        return r
 
    def get_by_genre(self, save_path='', genre=None):
        if(genre == None):
            rg = random.choice(self.fav_genres)
        else:
            rg = str(genre)
        url = self.genre_url + rg
        try:
            r = requests.get(url)
            enc_id = r.json()
            r = self._send_url_request(enc_id)
            self.set_params_by_id(enc_id)
        except:
            logging.debug('WolfTones failed to retrieve by genre')
            return None
       
        fn = self.write_file(r.content, save_path)
        logging.debug('filename : '+ fn)
        self.analyze(fn)
        return fn 

    def analyze(self, filename):
        #logging.debug('adding track info')
        with MidiFile(filename) as md:
            self.key = self.params['pitch']
            sc_prm = self.params['scale']
            if(sc_prm in self.vld.scales_notes):
                self.scale = self.vld.scales_notes[sc_prm]
            else:
                self.scale = [0]
            logging.debug(self.scale)
            #self.chan_roles = [0 for i in range(10)]
            for trk in md.tracks:
                #logging.debug('PARSING NEW TRACK '+ str(i))
                for msg in trk:
                    try:
                        #role_enc = 0
                        if(msg.type == 'program_change'):
                            inst = msg.program
                            chan = int(msg.channel)
                            role = None 
                            inst += 1
                            #logging.debug('inst: ' + str(inst))
                            #logging.debug('chan: ' + str(chan))
                            if inst == int(self.params['inst_1']):
                                role_enc = int(self.params['role_1'])
                            if inst == int(self.params['inst_2']):
                                role_enc = int(self.params['role_2'])
                            if inst == int(self.params['inst_3']):
                                role_enc = int(self.params['role_3'])
                            if inst == int(self.params['inst_4']):
                                role_enc = int(self.params['role_4'])
                            if inst == int(self.params['inst_5']):
                                role_enc = int(self.params['role_5'])
                            
                            if(chan is not 9):
                                role = self.vld.get_role(role_enc)
                            else:
                                role = 'perc'
                            trk.name = str(chan) + ':' + role
                            #self.chan_roles[chan] = role
                            break
                    except:
                        pass
            trk = md.tracks[0]
            trk.insert(0, MetaMessage('text', text = self._nkm_encoded_id()))
            md.save(filename)
        
    def write_file(self, content, save_path):
        fn = 'tmp_song-{:%m-%d-%H:%M}'.format(datetime.datetime.now()) + '.mid'
        #fn = self._nkm_encoded_id() + '.mid'
        #here we strip out any path elements, keeping only the filename so we only write in the saved song directory
        fn = save_path + fn 
        if(content):
            with open(fn, 'w+') as f:
                f.write(content)
        return fn
 
    def set_params_by_id(self, enc_id, load=False):
        toks = enc_id.split('-')
        if(not load):
            del toks[:2]
        i = 0
        for t in toks:
            self.params[self.params.keys()[i]] = t 
            #logging.debug('toks: ' + self.params.keys()[i] + ' ' + str(t))
            i += 1

# filename - full path filname
    def load_file(self, filename):
        #fn = filename.split('/')
        #fn = fn[-1]
        #fn = filename.split('.')
        #enc_id = fn[0]
        #self.set_params_by_id(enc_id)
        with MidiFile(filename) as md:
            trk = md.tracks[0]
            enc_id = 0
            for msg in trk: 
                if(msg.type == 'text'):
                    enc_id = msg.text
                    #logging.debug('before mangled ' +  enc_id)
                    break
            if(enc_id):
                self.set_params_by_id(enc_id, True)
            self.analyze(filename)
