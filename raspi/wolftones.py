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

    def set_param(self, key, value):
        if key in self.params:
            if key == 'genre':
                if int(value) in self.valid_genres.values():
                    self.params[key] = value
                    return True
            if key == 'rule_type':
                if int(value) in self.valid_rule_types:
                    self.params[key] = value
                    return True
            if key == 'rule':
                if self.rule_range[0] <= int(value) <= self.rule_range[1]:
                    self.params[key] = value
                    return True
            if key == 'cyc_bdry':
                if int(value) == 1 or int(value) == 0:
                    self.params[key] = value
                    return True
            if key == 'seed':
                if self.seed_range[0] <= int(value) <= self.seed_range[1]:
                    self.params[key] = value
                    return True
            if key == 'duration':
                if self.duration_range[0] <= int(value) <= self.duration_range[1]:
                    self.params[key] = value
                    return True
            if key == 'bpm':
                if self.bpm_range[0] <= int(value) <= self.bpm_range[1]:
                    self.params[key] = value
                    return True
            if key == 'npb':
                if self.npb_range[0] <= int(value) <= self.npb_range[1]:
                    self.params[key] = value
                    return True
            if key == 'scale':
                #if int(value) in self.valid_scales:
                    #self.params[key] = value
                    #return True
                return True
            if key == 'pitch':
                if self.pitch_min <= int(value) <= self.pitch_max:
                    self.params[key] = value
                    return True
            if key == 'inst_1' or key == 'inst_2' or key == 'inst_3' or key == 'inst_4':
                if int(value) in self.valid_inst.values():
                    self.params[key] = value
                    return True
            if key == 'role_1' or key == 'role_2' or key == 'role_3' or key == 'role_4':
                if int(value) in self.valid_roles:
                    self.params[key] = value
                    return True
            if key == 'perc':
                if int(value) in self.valid_perc:
                    self.params[key] = value
                    return True
        return False
    
    def nkm_encoded_id(self):
        enc_id = ''
        params = self.params.values()
        for val in params[:-1]:
            enc_id += val + '-'
        enc_id += params[-1]
        return enc_id

    def send_url_request(self, enc_id=None):
        if(enc_id == None):
            nkm_id = 'NKM-G-' + self.nkm_encoded_id()
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
            r = self.send_url_request(enc_id)
            self.set_params_by_id(enc_id)
        except:
            logging.debug('WolfTones failed to retrieve by genre')
            return None
        fn = self.write_file(r.content)
        md = MidiFile(fn)
        for trk in md.tracks:
            for msg in trk:
                if msg.type == 'program_change':
                    role = self.get_role(msg.program)
                    if(role):
                        trk.name = role
                    else:
                        trk.name = 'None'
                    break
        md.save(fn)
        return fn 
       
    def write_file(self, content):
        tmp = self.song_temp_path + 'dl_song-{:%m-%d-%H:%M}'.format(datetime.datetime.now()) + '.mid'
        try:
            with open(tmp, 'w+') as f:
                f.write(content)
            return tmp
        except:
            return None
 
    def set_params_by_id(self, enc_id):
        toks = enc_id.split('-')
        del toks[:2]
        i = 0
        for t in toks:
            self.params[self.params.keys()[i]] = t 
            logging.debug('toks: ' + self.params.keys()[i] + ' ' + str(t))
            i += 1

    def get_role(self, inst):
        role = None
        role_grp = None
        if(inst):
            inst += 1
            if inst == int(self.params['inst_1']):
                role = int(self.params['role_1'])
            elif inst == int(self.params['inst_2']):
                role = int(self.params['role_2'])
            elif inst == int(self.params['inst_3']):
                role = int(self.params['role_3'])
            elif inst == int(self.params['inst_4']):
                role = int(self.params['role_4'])
            elif inst == int(self.params['inst_5']):
                    role = int(self.params['role_5'])
        if(role):
            if role in self.vld.roles_generic:
                 role_grp = 'generic'
            elif role in self.vld.roles_polyphonic:
                 role_grp = 'polyphonic'
            elif role in self.vld.roles_upper_lead:
                 role_grp = 'upper_lead'
            elif role in self.vld.roles_lower_lead:
                 role_grp = 'lower_lead'
            elif role in self.vld.roles_moving_lead:
                 role_grp = 'moving_lead'
            elif role in self.vld.roles_straight_lead:
                 role_grp = 'straight_lead'
            elif role in self.vld.roles_chords:
                 role_grp = 'chords'
            elif role in self.vld.roles_bass:
                 role_grp = 'bass'
        return role_grp 

        
#obj_params = collections.OrderedDict( [ ('genre','45'), ('rule_type','15'), ('rule','10'), ('cyc_bdry','1'), ('seed','34444'), ('duration','21'), ('bpm','130'), ('npb','4'), ('scale','2050'), ('pitch','44'), ('mystery','0'), ('inst_1','31'), ('role_1','10'), ('inst_2','95'), ('role_2','135'), ('inst_3','0'), ('role_3','0'), ('inst_4','0'), ('role_4','0'), ('inst_5','0'), ('role_5','0'), ('perc','711') ] )
