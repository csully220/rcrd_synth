import collections
import requests
import random
import logging
from wolftones_validate import WolfTonesValidate
import mido
from mido import MidiFile
import datetime

class WolfTones:
    
    dl_url = 'https://www.wolframcloud.com/objects/user-a13d29f3-43bf-4b00-8e9b-e55639ecde19/NKMMusicDownload?id='
    genre_url = 'https://www.wolframcloud.com/objects/user-a13d29f3-43bf-4b00-8e9b-e55639ecde19/NKMNewID?genre=' 
    song_save_path = '/home/pi/rcrd_synth/raspi/songs/save/'
    song_temp_path = '/home/pi/rcrd_synth/raspi/songs/temp/'

    #hip hop, dance, blues, experimental
    #fav_genres = [45,40,55,90]
    #Pan Flute, brazilian bell, melodic tom, 
    wildcard_inst = [76, 114, 118]
    fav_genres = ['25', '45','40','55','60'] # ambient,hip hop, dance, blues, R&B

    def __init__(self):
        self.vld = WolfTonesValidate()
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
 
    def get_by_genre(self, genre=None):
        if(genre == None):
            rg = random.choice(self.fav_genres)
        else:
            rg = str(genre)
        #logging.debug('random fav genre - ' + rg)
        url = self.genre_url + rg
        try:
            r = requests.get(url)
            enc_id = r.json()
            r = self._send_url_request(enc_id)
            self.set_params_by_id(enc_id)
        except:
            logging.debug('WolfTones failed to retrieve by genre')
            return None
        
        fn = self.write_file(r.content)
        self.add_track_info(fn)
        return fn 

    def add_track_info(self, filename):
        #logging.debug('adding track info')
        md = MidiFile(filename)
        i = 0
        for trk in md.tracks:
            i += 1
            #logging.debug('PARSING NEW TRACK '+ str(i))
            for msg in trk:
                try:
                    if msg.type == 'program_change':
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
                        
                        #try:
                            #logging.debug('getting role')
                        role = self.vld.get_role(role_enc)
                        if(chan == 9 or inst == 1):
                            role = 'perc'
                        trk.name = str(chan) + ':' + role
                        #logging.debug('Added channel  ' + trk.name)
                        #except:
                        #    trk.name = 'Fail'
                        break
                except:
                    pass        
        #logging.debug('inst1: ' + self.params['inst_1'])
       # logging.debug('role1: ' + self.params['role_1'])
       # logging.debug('inst2: ' + self.params['inst_2'])
       # logging.debug('role2: ' + self.params['role_2'])
       # logging.debug('inst3: ' + self.params['inst_3'])
       # logging.debug('role3: ' + self.params['role_3'])
       # logging.debug('inst4: ' + self.params['inst_4'])
       # logging.debug('role4: ' + self.params['role_4'])
       # logging.debug('inst5: ' + self.params['inst_5'])
       # logging.debug('role5: ' + self.params['role_5'])
        md.save(filename)
        
    def write_file(self, content):
        filename = None
        temp = True
        if(not filename):
            #fn = 'dl_song-{:%m-%d-%H:%M}'.format(datetime.datetime.now()) + '.mid'
            fn = self._nkm_encoded_id() + '.mid'
        else:
            #here we strip out any path elements, keeping only the filename so we only write in the saved song directory
            fn = filename.split('/')
            fn = fn[-1]
            fn = fn[0]
            fn += self.song_save_path
        if(temp):
        #save in the temp song folder
            fn = self.song_temp_path + fn
        else:
        #save in the permanent folder
            fn = self.song_save_path + fn 
        if(content):
            with open(fn, 'w+') as f:
                f.write(content)
            return fn
 
    def set_params_by_id(self, enc_id):
        toks = enc_id.split('-')
        del toks[:2]
        i = 0
        for t in toks:
            self.params[self.params.keys()[i]] = t 
            #logging.debug('toks: ' + self.params.keys()[i] + ' ' + str(t))
            i += 1

    def load_file(self, filename):
        fn = filename.split('/')
        fn = fn[-1]
        fn = filename.split('.')
        enc_id = fn[0]
        self.set_params_by_id(enc_id)
        self.add_track_info(filename)
 

#obj_params = collections.OrderedDict( [ ('genre','45'), ('rule_type','15'), ('rule','10'), ('cyc_bdry','1'), ('seed','34444'), ('duration','21'), ('bpm','130'), ('npb','4'), ('scale','2050'), ('pitch','44'), ('mystery','0'), ('inst_1','31'), ('role_1','10'), ('inst_2','95'), ('role_2','135'), ('inst_3','0'), ('role_3','0'), ('inst_4','0'), ('role_4','0'), ('inst_5','0'), ('role_5','0'), ('perc','711') ] )
