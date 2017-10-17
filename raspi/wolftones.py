import collections
import requests
import random
import logging
import wolftones_validate

class WolfTones:
    
    dl_url = 'https://www.wolframcloud.com/objects/user-a13d29f3-43bf-4b00-8e9b-e55639ecde19/NKMMusicDownload?id='
    genre_url = 'https://www.wolframcloud.com/objects/user-a13d29f3-43bf-4b00-8e9b-e55639ecde19/NKMNewID?genre=' 

    #hip hop, dance, blues, experimental
    #fav_genres = [45,40,55,90]
    #Pan Flute, brazilian bell, melodic tom, 
    wildcard_inst = [76, 114, 118]


    def __init__(self):
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
            logging.debug('WolfTones nkm id: ' +  str(nkm_id))
        r = requests.get(self.dl_url + nkm_id + '&form=MIDI')
        return r
 
    def get_by_genre(self, genre=None):
        if(genre == None):
            fav_genres = ['45','40','55','60']
            rg = random.choice(fav_genres)
        else:
            rg = str(genre)
        logging.debug('random fav genre - ' + rg)
        url = self.genre_url + rg
        try:
            r = requests.get(url)
            enc_id = r.json()
            r = self.send_url_request(enc_id)
            self.set_params_by_id(enc_id)
        except:
            logging.debug('WolfTones failed to retrieve by genre')
        return r
        
    def set_params_by_id(self, enc_id):
        toks = enc_id.split('-')
        del toks[:2]
        i = 0
        for t in toks:
            self.params[self.params.keys()[i]] = t 
            i += 1


        '''
        try:
            response = wt.send_url_request()
            #logging.debug(wt.nkm_encoded_url())
            logging.debug('MIDI file requested from ' + wt.nkm_encoded_url())
            if(response.content):
                logging.debug('Got a new song from Wolftones')
                curses.echo()
                #tmp = 'songs/' + get_param("Enter song filename: ") + '.mid'
                songfile = 'songs/temp/raw_song' + '{:%m-%d}'.format(datetime.datetime.now()) + '.mid'
                with open(songfile, 'w+') as f:
                    f.write(response.content)
                curses.noecho()
                return songfile
        except:
            song_file = 'songs/save/warriorcatssong.mid'
        '''
#obj_params = collections.OrderedDict( [ ('genre','45'), ('rule_type','15'), ('rule','10'), ('cyc_bdry','1'), ('seed','34444'), ('duration','21'), ('bpm','130'), ('npb','4'), ('scale','2050'), ('pitch','44'), ('mystery','0'), ('inst_1','31'), ('role_1','10'), ('inst_2','95'), ('role_2','135'), ('inst_3','0'), ('role_3','0'), ('inst_4','0'), ('role_4','0'), ('inst_5','0'), ('role_5','0'), ('perc','711') ] )
