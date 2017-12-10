
class Validator():
    valid_genres = {'Classical':'15',
                    'Piano':'10',
                    'Guitar':'11',
                    'Ambient':'25',
                    'Rock/Pop':'30',
                    'Dance':'40',
                    'Hip Hop':'45',
                    'R&B':'60',
                    'Blues':'55',
                    'Jazz':'50',
                    'Country':'65',
                    'Latin':'70',
                    'World':'80',
                    'Experimental':'90',
                    'Signaling':'95'}
        
    valid_rule_types = [7,15,31,55,61,62,79,91,103,110,157,167,773,1047,1585]
    rule_range = [1, 4294967295]
    seed_range = [1, 67108863]
    duration_range = [4, 240]
    bpm_range = [60, 288]
    npb_range = [2, 16]
    height_range = [5, 25]
    valid_scales = []
    pitch_min = 24
    pitch_max = 72
    valid_inst = {'None':0,
                  'Grand Piano':1,
                  'Grand Piano (Electric)':3,
                  'Bright Piano':2,
                  'Honky-Tonk Piano':4,
                  'Electric Piano 1':5,
                  'Electric Piano 2':6,
                  'Harpsichord':7,
                  'Clavi':8,
                  'Celest':9,
                  'Harp':47,
                  'Tinkle Bell':113,
                  'Vibraphone':12,
                  'Marimba':13,
                  'Xylophone':14,
                  'Woodblock':116,
                  'Tubular Bells':15,
                  'Drawbar Organ':17,
                  'Percussive Organ':18,
                  'Rock Organ':19,
                  'Church Organ':20,
                  'Reed Organ':21,
                  'Harmonica':23,
                  'Accordion':22,
                  'Tango Accordion':24,
                  'Guitar (Nylon)':25,
                  'Guitar (Steel)':26,
                  'Guitar (Jazz)':27,
                  'Guitar (Clean)':28,
                  'Guitar (Muted)':29,
                  'Guitar (Overdriven)':30,
                  'Guitar (Distortion)':31,
                  'Guitar (Harmonics)':32,
                  'Acoustic Bass':33,
                  'Electric Bass (Finger)':34,
                  'Electric Bass (Pick)':35,
                  'Electric Bass (Fretless)':36,
                  'Slap Bass 1':37,
                  'Slap Bass 2':38,
                  'Synth Bass 1':39,
                  'Synth Bass 2':40,
                  'Violin':41,
                  'Viola':42,
                  'Cello':43,
                  'Contrabass':44,
                  'Strings':49,
                  'Strings (Legato)':50,
                  'Strings (Tremolo)':45,
                  'Strings (Pizzicato':46,
                  'Synth Strings 1':51,
                  'Synth Strings 2':52,
                  'Voice (Aahs)':53,
                  'Voice (Oohs)':54,
                  'Voice (Synth)':55,
                  'French Horn':61,
                  'Trumpet':57,
                  'Trumpet (Muted)':60,
                  'Trombone':58,
                  'Tuba':59,
                  'Brass Section':62,
                  'Synth Brass 1':63,
                  'Synth Brass 2':64,
                  'Sax (Soprano)':65,
                  'Sax (Alto)':66,
                  'Sax (Tenor)':67,
                  'Sax (Baritone)':68,
                  'Piccolo Flute':73,
                  'Flute':74,
                  'Oboe':69,
                  'English Horn':70,
                  'Clarinet':72,
                  'Bassoon':71,
                  'Synth Lead 1 (Square)':81,
                  'Synth Lead 2 (Sawtooth)':82,
                  'Synth Lead 3 (Calliope)':83,
                  'Synth Lead 4 (Chiff)':84,
                  'Synth Lead 5 (Charang)':85,
                  'Synth Lead 6 (Voice)':86,
                  'Synth Lead 7 (Fifths)':87,
                  'Synth Lead 8 (Bass + Lead)':88,
                  'Synth Pad 1 (New Age)':89,
                  'Synth Pad 2 (Warm)':90,
                  'Synth Pad 3 (Polysynth)':91,
                  'Synth Pad 4 (Choir)':92,
                  'Synth Pad 5 (Bowed)':93,
                  'Synth Pad 6 (Metallic)':94,
                  'Synth Pad 7 (Halo)':95,
                  'Synth Pad 8 (Sweep)':96,
                  'Synth FX 1 (Rain)':97,
                  'Synth FX 2 (Soundtrack)':98,
                  'Synth FX 3 (Crystal)':99,
                  'Synth FX 4 (Atmosphere)':100,
                  'Synth FX 5 (Brightness)':101,
                  'Synth FX 6 (Goblins)':102,
                  'Synth FX 7 (Echoes)':103,
                  'Synth FX 8 (Sci-Fi)':104,
                  'Sitar':105,
                  'Banjo':106,
                  'Fiddle':111,
                  'Shamisen (Japanese Lute)':107,
                  'Koto (Japanese Zither)':108,
                  'Kalimba (African)':109,
                  'Bag Pipe':110,
                  'Dulcimer':16,
                  'Pan Flute':76,
                  'Shakuhachi (Japanese Flute)':78,
                  'Recorder':75,
                  'Ocarina (Peruvian Wind)':80,
                  'Shanai (Indian Reed)':112,
                  'Timpani (Kettle Drums)':48,
                  'Agogo (Brazilian Bell)':114,
                  'Steel Drums':115,
                  'Taiko (Japanese Drum)':117,
                  'Melodic Tom':118,
                  'Synth Drum':119,
                  'Glockenspiel':10,
                  'Music Box':11,
                  'Reverse Cymbal':120}
                           
    roles_generic = [0,1,10,16,20,21,51,52]
    
    roles_polyphonic = [901,907,912,913,914,915,916,922,923,924,932]
    
    roles_upper_lead = [101,201,202,102,203,206,103,104,105,107,108,209,110,109,111]
    
    roles_lower_lead = [121,204,205,122,207,208,210,123,124,127,128,129,130,132,131]
    
    roles_moving_lead = [135,136,137]
        
        #several types of "lead" in here. Too lazy to separate
    roles_straight_lead = [144,140,149,141,142,143,145,151,153,154,161,162,163,169,170,180,183,181,182]
    
    roles_chords = [302,316,301,303,304,305,313,306,307,314,315,340,341,312,308,309,310,311,317,350,351]
    
    roles_bass = [501,515,516,502,520,521,503,511,545,504,505,544,512,541,542,543,513,510,514,570,536,540,552,551,537,538,561,562]
    
    valid_roles = [0,1,10,16,20,21,51,52,901,907,912,913,914,915,916,922,923,924,932,101,201,202,102,203,206,103,104,105,107,108,209,110,109,111,121,204,205,122,207,208,210,123,124,127,128,129,130,132,131,135,136,137,144,140,149,141,142,143,145,151,153,154,161,162,163,169,170,180,183,181,182,302,316,301,303,304,305,313,306,307,314,315,340,341,312,308,309,310,311,317,350,351,501,515,516,502,520,521,503,511,545,504,505,544,512,541,542,543,513,510,514,570,536,540,552,551,537,538,561,562]
                  
    valid_perc = [0,1,101,102,121,122,123,127,128,129,131,132,133,301,311,322,323,325,321,324,361,362,331,332,333,334,341,342,343,344,345,346,347,348,349,351,352,353,501,401,402,403,404,431,432,433,434,551,552,553,555,554,556,571,572,573,574,575,576,577,578,579,584,586,581,582,583,585,112,113,114,115,451,452,453,454,455,456,457,458,459,460,461,462,463,651,652,681,682,711,712,713,714,601,715,721,722,723,801,803,804,805,807,808,809,810,821,822,823,830,901,911] 
                           
    def get_role(self, role = None):
        role_grp = None
        if role in self.roles_generic:
             role_grp = 'generic'
        elif role in self.roles_polyphonic:
             role_grp = 'poly' #polyphonic
        elif role in self.roles_upper_lead:
             role_grp = 'upr_ld' #upper_lead
        elif role in self.roles_lower_lead:
             role_grp = 'lwr_ld' #lower_lead
        elif role in self.roles_moving_lead:
             role_grp = 'mov_ld' #moving_lead 
        elif role in self.roles_straight_lead:
             role_grp = 'str_ld' #straight_lead
        elif role in self.roles_chords:
             role_grp = 'chords' #chords
        elif role in self.roles_bass:
             role_grp = 'bass' #bass
        elif not role:
             role_grp = 'perc' #bass
        return role_grp


    def validate_param(self, key, value):
        if key == 'genre':
            if int(value) in self.valid_genres.values():
                return True
        elif key == 'rule_type':
            if int(value) in self.valid_rule_types:
                return True
        elif key == 'rule':
            if self.rule_range[0] <= int(value) <= self.rule_range[1]:
                return True
        elif key == 'cyc_bdry':
            if int(value) == 1 or int(value) == 0:
                return True
        elif key == 'seed':
            if self.seed_range[0] <= int(value) <= self.seed_range[1]:
                return True
        elif key == 'duration':
            if self.duration_range[0] <= int(value) <= self.duration_range[1]:
                return True
        elif key == 'bpm':
            if self.bpm_range[0] <= int(value) <= self.bpm_range[1]:
                return True
        elif key == 'npb':
            if self.npb_range[0] <= int(value) <= self.npb_range[1]:
                return True
        elif key == 'scale':
            #if int(value) in self.valid_scales:
                #return True
            return True
        elif key == 'pitch':
            if self.pitch_min <= int(value) <= self.pitch_max:
                return True
        elif key == 'inst_1' or key == 'inst_2' or key == 'inst_3' or key == 'inst_4':
            if int(value) in self.valid_inst.values():
                return True
        elif key == 'role_1' or key == 'role_2' or key == 'role_3' or key == 'role_4':
            if int(value) in self.valid_roles:
                return True
        elif key == 'perc':
            if int(value) in self.valid_perc:
                return True
        return False

    scales_notes = {
        '3926':[0,1,1,1,2,2,2,1,2],
        '2477':[0,3,1,2,2,1,2,1],
        '2937':[0,0,2,1,2,1,1,1,3,1],
        '3156':[0,1,4,2,2,3],
        '3456':[0,1,2,1,8],
        '2772':[0,2,2,1,2,2,3],
        '2184':[0,4,4,4],
        '3248':[0,1,3,2,1,5],
        '3285':[0,1,3,1,2,2,2,1],
        '2322':[0,3,4,3,2],
        '2418':[0,3,2,1,1,3,2],
        '3510':[0,1,2,1,2,1,2,1,2],
        '2964':[0,2,1,1,3,2,3],
        '3062':[0,2,1,1,1,1,1,2,1,2],
        '2422':[0,3,2,1,1,2,1,2],
        '2930':[0,2,1,2,1,1,3,2],
        '2934':[0,2,1,2,1,1,2,1,2],
        '3872':[0,1,1,1,3,6],
        '2386':[0,3,2,2,3,2],
        '3442':[01,2,2,1,1,3,2],
        '2419':[0,3,2,1,1,3,1,1],
        '2504':[0,3,1,1,3,4],
        '2896':[0,2,1,2,2,5],
        '2634':[0,2,3,3,2,2],
        '3799':[0,1,1,2,1,2,2,1,1,1],
        '4092':[0,1,1,1,1,1,1,1,1,1,3],
        '3934':[0,1,1,1,2,2,1,1,1,2],
        '3676':[0,1,1,3,2,1,1,3],
        '2515':[0,3,1,1,2,3,1,1],
        '4064':[0,1,1,1,1,1,1,6],
        '4032':[0,1,1,1,1,1,7],
        '2972':[0,2,1,1,3,1,1,3],
        '2510':[0,3,1,1,3,1,1,2],
        '3257':[0,1,3,2,1,1,3,1],
        '3305':[0,1,3,1,1,2,3,1],
        '3700':[0,1,1,3,1,1,2,3],
        '3301':[0,1,3,1,1,3,2,1],
        '3385':[0,1,2,3,1,1,3,1],
        '3698':[0,1,1,3,1,1,3,2],
        '2675':[0,2,3,1,1,3,1,1],
        '4088':[0,1,1,1,1,1,1,1,1,4],
        '4080':[0,1,1,1,1,1,1,1,5],
        '3968':[0,1,1,1,1,8],
        '3805':[0,1,1,2,1,2,1,1,2,1],
        '2507':[0,3,1,1,3,2,1,1],
        '3740':[0,1,1,2,3,1,1,3],
        '3840':[0,1,1,1,9],
        '3584':[0,1,1,10],
        '4094':[0,1,1,1,1,1,1,1,1,1,1,2],
        '2336':[0,3,3,6],
        '2925':[0,2,1,2,1,2,1,2,1],
        '2340':[0,3,3,3,3],
        '2775':[0,2,2,1,2,2,1,1,1],
        '2706':[0,2,2,3,3,2],
        '2902':[0,2,1,2,2,2,1,2],
        '2910':[0,2,1,2,2,1,1,1,2],
        '2918':[0,2,1,2,1,3,1,2],
        '2836':[0,2,1,4,2,3],
        '3392':[0,1,2,2,7],
        '3290':[0,1,3,1,2,1,2,2],
        '3428':[0,1,2,2,1,3,3],
        '2729':[0,2,2,2,2,3,1],
        '2704':[0,2,2,3,5],
        '2911':[0,2,1,2,2,1,1,1,1,1],
        '3549':[0,1,2,1,1,2,1,1,2,1],
        '2805':[0,2,2,1,1,1,2,2,1],
        '2640':[0,2,3,2,5],
        '2130':[0,5,2,3,2],
        '2261':[0,4,1,2,2,2,1],
        '3292':[0,1,3,1,2,1,1,3],
        '2870':[0,2,1,3,1,2,1,2],
        '3449':[0,1,2,2,1,1,1,3,1],
        '2648':[0,2,3,2,1,4],
        '2777':[0,2,2,1,2,1,3,1],
        '2905':[0,2,1,2,2,1,3,1],
        '3286':[0,1,3,1,2,2,1,2],
        '2848':[0,2,1,3,6],
        '3929':[0,1,1,1,2,2,1,3,1],
        '2837':[0,2,1,4,2,2,1],
        '2840':[0,2,1,4,1,4],
        '3426':[0,1,2,2,1,4,2],
        '3038':[0,2,1,1,1,2,1,1,1,2],
        '2517':[0,3,1,1,2,2,2,1],
        '2486':[0,3,1,2,1,2,1,2],
        '2765':[0,2,2,1,3,1,2,1],
        '3170':[0,1,4,1,4,2],
        '3376':[0,1,2,3,1,5],
        '2901':[0,2,1,2,2,2,2,1],
        '3414':[0,1,2,2,2,2,1,2],
        '2942':[0,2,1,2,1,1,1,1,1,2],
        '3154':[0,1,4,2,3,2],
        '2724':[0,2,2,2,3,3],
        '3434':[0,1,2,2,1,2,2,2],
        '2921':[0,2,1,2,1,2,3,1],
        '3436':[0,1,2,2,1,2,1,3],
        '3430':[0,1,2,2,1,3,1,2],
        '3424':[0,1,2,2,1,6],
        '2741':[0,2,2,2,1,2,2,1],
        '2733':[0,2,2,2,2,1,2,1],
        '2869':[0,2,1,3,1,2,2,1],
        '2709':[0,2,2,3,2,2,1],
        '2746':[0,2,2,2,1,1,2,2],
        '2736':[0,2,2,2,1,5],
        '2485':[0,3,1,2,1,2,2,1],
        '2453':[0,3,1,3,2,2,1],
        '3501':[0,1,2,1,2,2,1,2,1],
        '2773':[0,2,2,1,2,2,2,1],
        '3039':[0,2,1,1,1,2,1,1,1,1,1],
        '2781':[0,2,2,1,2,1,1,2,1],
        '2716':[0,2,2,3,1,1,3],
        '2192':[0,4,3,5],
        '3289':[0,1,3,1,2,1,3,1],
        '2794':[0,2,2,1,1,2,2,2],
        '2778':[0,2,2,1,2,1,2,2],
        '2768':[0,2,2,1,2,5],
        '2708':[0,2,2,3,2,3],
        '2049':[0,11,1],
        '2052':[0,9,3],
        '2752':[0,2,2,1,7],
        '2176':[0,4,8],
        '3291':[0,1,3,1,2,1,2,1,1],
        '3558':[0,1,2,1,1,1,3,1,2],
        '3253':[0,1,3,2,1,2,2,1],
        '3386':[0,1,2,3,1,1,2,2],
        '2739':[0,2,2,2,1,3,1,1],
        '2489':[0,3,1,2,1,1,3,1],
        '3260':[0,1,3,2,1,1,1,3],
        '3379':[0,1,2,3,1,3,1,1],
        '3673':[0,1,1,3,2,1,3,1],
        '2521':[0,3,1,1,2,1,3,1],
        '3388':[0,1,2,3,1,1,1,3],
        '3283':[0,1,3,1,2,3,1,1],
        '3642':[0,1,3,1,2,3,1,1],
        '3641':[0,1,1,4,1,1,2,2],
        '2908':[0,2,1,2,2,1,1,3],
        '2490':[0,3,1,2,1,1,2,2],
        '2748':[0,2,2,2,1,1,1,3],
        '2745':[0,2,2,2,1,1,3,1],
        '3669':[0,1,1,3,2,2,2,1],
        '2780':[0,2,2,1,2,1,1,3],
        '2771':[0,2,2,1,2,3,1,1],
        '3258':[0,1,3,2,1,1,2,2],
        '3638':[0,1,1,4,1,2,1,2],
        '2867':[0,2,1,3,1,3,1,1],
        '3637':[0,1,1,4,1,2,2,1],
        '2522':[0,3,1,1,2,1,2,2],
        '3635':[0,1,1,4,1,3,1,1],
        '2483':[0,3,1,2,1,3,1,1],
        '3674':[0,1,1,3,2,1,2,2],
        '3411':[0,1,2,2,2,3,1,1],
        '3382':[0,1,2,3,1,2,1,2],
        '3644':[0,1,1,4,1,1,1,3],
        '2874':[0,2,1,3,1,1,2,2],
        '3420':[0,1,2,2,2,1,1,3],
        '2492':[0,3,1,2,1,1,1,3],
        '3381':[0,1,2,3,1,2,2,1],
        '2876':[0,1,1,3,2,3,1,1],
        '3667':[0,1,1,3,2,3,1,1],
        '3670':[0,1,1,3,2,2,1,2],
        '2899':[0,2,1,2,2,3,1,1],
        '3251':[0,1,3,2,1,3,1,1],
        '2524':[0,3,1,1,2,1,1,3],
        '3822':[0,1,1,2,1,1,2,1,1,2],
        '3003':[0,2,1,1,2,1,1,2,1,1],
        '3900':[0,1,1,1,3,1,1,1,3],
        '2535':[0,3,1,1,1,3,1,1,1],
        '3640':[0,1,1,4,1,1,4],
        '2275':[0,4,1,1,4,1,1],
        '3770':[0,1,1,2,2,1,1,2,2],
        '2795':[0,2,2,1,1,2,2,1,1],
        '4030':[0,1,1,1,1,2,1,1,1,1,2],
        '3055':[0,2,1,1,1,1,2,1,1,1,1],
        '3380':[0,1,2,3,1,2,3],
        '3276':[0,1,3,1,3,1,3],
        '2457':[0,3,1,3,1,3,1],
        '3120':[0,1,5,1,5],
        '2145':[0,5,1,5,1],
        '2600':[0,2,4,2,4],
        '2210':[0,4,2,4,2],
        '2906':[0,2,1,2,2,1,2,2],
        '2388':[0,3,2,2,2,3],
        '3030':[0,2,1,1,1,2,2,1,2],
        '2966':[0,2,1,1,3,2,1,2],
        '2320':[0,3,4,5],
        '2873':[0,2,1,3,1,1,3,1],
        '2898':[0,2,1,2,2,3,2],
        '2922':[0,2,1,2,1,2,2,2],
        '3063':[0,2,1,1,1,1,1,2,1,1,1],
        '2050':[0,10,2],
        '2056':[0,8,4],
        '2304':[0,3,9],
        '2816':[0,2,1,9],
        '2774':[0,2,2,1,2,2,1,2],
        '2790':[0,2,2,1,1,3,1,2],
        '2646':[0,2,3,2,2,1,2],
        '2258':[0,2,3,2,2,1,2],
        '2766':[0,2,2,1,3,1,1,2],
        '3547':[0,1,2,1,1,2,1,2,1,1],
        '3413':[0,1,2,2,2,2,2,1],
        '3417':[0,1,2,2,2,1,3,1],
        '3756':[0,1,1,2,2,2,1,3],
        '3387':[0,1,2,3,1,1,2,1,1],
        '2669':[0,2,3,1,2,1,2,1],
        '3302':[0,1,3,1,1,3,1,2],
        '3680':[0,1,1,3,1,6],
        '2742':[0,2,2,2,1,2,1,2],
        '3352':[0,1,2,4,1,4],
        '2064':[0,7,5],
        '2112':[0,5,7],
        '3418':[0,1,2,2,2,1,2,2],
        '3930':[0,1,1,1,2,2,1,2,2],
        '3482':[0,1,2,1,3,1,2,2],
        '2394':[0,3,2,2,1,2,2],
        '3450':[0,1,2,2,1,1,1,2,2],
        '2880':[0,2,1,2,7],
        '3328':[0,1,2,9],
        '3435':[0,1,2,2,1,2,2,1,1],
        '2726':[0,2,2,2,3,1,2],
        '3238':[0,1,3,2,3,1,2],
        '2916':[0,2,1,2,1,3,3],
        '2884':[0,2,1,2,4,3],
        '2865':[0,2,1,3,1,4,1],
        '2888':[0,2,1,2,3,4],
        '2886':[0,2,1,2,4,1,2],
        '3225':[0,1,3,3,1,3,1],
        '2514':[0,3,1,1,2,3,2],
        '3317':[0,1,3,1,1,1,2,2,1],
        '2628':[0,2,3,4,3],
        '3370':[0,1,2,3,2,2,2],
        '2649':[0,2,3,2,1,3,1],
        '2245':[0,4,1,4,2,1],
        '2712':[0,2,2,3,1,4],
        '2180':[0,4,5,3],
        '2737':[0,2,2,2,1,4,1],
        '3636':[0,1,1,4,1,2,3],
        '2374':[0,3,2,4,1,2],
        '2377':[0,3,2,3,3,1],
        '2373':[0,3,2,4,2,1],
        '3368':[0,1,2,3,2,4],
        '3400':[0,1,2,2,3,4],
        '2878':[0,2,1,3,1,1,1,1,2],
        '3097':[0,1,6,1,3,1],
        '2641':[0,2,3,2,4,1],
        '2137':[0,5,2,1,3,1],
        '3256':[0,1,3,2,1,1,4],
        '2800':[0,2,2,1,1,1,5],
        '2257':[0,4,1,2,4,1],
        '3410':[0,1,3,1,2,4,1],
        '3281':[0,1,4,2,4,1],
        '3153':[0,2,1,2,3,3,1],
        '2889':[0,2,3,4,1,2],
        '2630':[0,1,2,3,2,3,1],
        '2705':[0,2,2,3,4,1],
        '3237':[0,1,3,2,3,2,1],
        '2757':[0,2,2,1,4,2,1],
        '2346':[0,3,3,2,2,2],
        '2632':[0,2,3,3,4],
        '3244':[0,1,3,2,2,1,3],
        '2213':[0,4,2,3,2,1],
        '3250':[0,1,3,2,1,3,2],
        '2618':[0,2,4,1,1,2,2],
        '2402':[0,3,2,1,4,2],
        '2355':[0,3,3,1,3,1,1],
        '2234':[0,4,2,1,1,2,2],
        '3228':[0,1,3,3,1,1,3],
        '3164':[0,1,4,2,1,1,3],
        '3284':[0,1,3,1,2,2,3],
        '2266':[0,4,1,2,1,2,2],
        '3354':[0,1,2,4,1,2,2],
        '2246':[0,4,1,4,1,2],
        '2262':[0,4,1,2,2,1,2],
        '2392':[0,3,2,2,1,4],
        '3145':[0,1,4,3,3,1],
        '3593':[0,1,1,6,3,1],
        '2721':[0,2,2,2,5,1],
        '2134':[0,5,2,2,1,2],
        '2713':[0,2,2,3,1,3,1],
        '3144':[0,1,4,3,4],
        #omitting a bunch of raga scales cuz who cares...
        '3402':[0,1,2,2,3,2,2],
        '2518':[0,3,1,1,2,2,1,2],
        '2249':[0,4,1,3,3,1],
        '3254':[0,1,3,2,1,2,1,2],
        '2970':[0,2,1,1,3,1,2,2],
        '3160':[0,1,4,2,1,4],
        '2114':[0,5,5,2],
        '2644':[0,2,3,2,2,3],
        '3220':[0,1,3,3,2,3],
        '3072':[0,1,11],
        '3509':[0,1,2,1,2,1,2,2,1],
        '3562':[0,1,2,1,1,1,2,2,2],
        '3520':[0,1,2,1,1,7],
        '3546':[0,1,2,1,1,2,1,2,2],
        '3498':[0,1,2,1,2,2,2,2],
        '2642':[0,2,3,2,3,2],
        '3835':[0,1,1,2,1,1,1,1,2,1,1],
        '2807':[0,2,2,1,1,1,2,1,1,1],
        '2857':[0,2,1,3,2,3,1],
        '2858':[0,2,1,3,2,2,2],
        '2080':[0,6,6],
        '4095':[0,1,1,1,1,1,1,1,1,1,1,1,1],
        '3500':[0,1,2,1,2,2,1,3],
        '2048':[0,12],
        '2306':[0,3,7,2],
        '2907':[0,2,1,2,2,1,2,1,1],
        '3307':[0,1,3,1,1,2,2,1,1],
        '3243':[0,1,3,2,2,2,1,1],
        '3275':[0,1,3,1,3,2,1,1],
        '2818':[0,2,1,7,2],
        '2560':[0,2,10],
        '2730':[0,2,2,2,2,2,2],
        '2731':[0,2,2,2,2,2,1,1],
        '2720':[0,2,2,2,6],
        '2688':[0,2,2,8],
        '3830':[0,1,1,2,1,1,1,2,1,2],
        '2909':[0,2,1,2,2,1,1,2,1]
        }

    scales_names = {
        '0':'None',
        '3926':'Adonai Malakh (Israel)',
        '2477':'Aeolian Flat 1',
        '2937':'Algerian',
        '3156':'Altered Pentatonic',
        '3456':'Alternating Tetramirror',
        '2772':'Arezzo Major Diatonic Hexachord',
        '2184':'Augmented Chord',
        '3248':'Balinese Pentachord',
        '3285':'Bhairubahar Thaat (India)',
        '2322':'Bi Yu (China)',
        '2418':'Blues',
        '3510':'Blues Diminished',
        '2964':'Blues Dorian Hexatonic',
        '3062':'Blues Enneatonic',
        '2422':'Blues Heptatonic',
        '2930':'Blues Modified',
        '2934':'Blues Octatonic',
        '3872':'Blues Pentacluster',
        '2386':'Blues Pentatonic',
        '3442':'Blues Phrygian',
        '2419':'Blues With Leading Tone',
        '2504':'Center-Cluster Pentamirror',
        '2896':'Chad Gadyo (Israel)',
        '2634':'Chaio (China)',
        '3799':'Chromatic Bebop',
        '4092':'Chromatic Decamirror',
        '3934':'Chromatic Diatonic Dorian',
        '3676':'Chromatic Dorian',
        '2515':'Chromatic Dorian Inverse',
        '4064':'Chromatic Heptamirror',
        '4032':'Chromatic Hexamirror',
        '2972':'Chromatic Hypodorian',
        '2510':'Chromatic Hypodorian Inverse',
        '3257':'Chromatic Hypolydian',
        '3305':'Chromatic Hypolydian Inverse',
        '3700':'Chromatic Hypophrygian Inverse',
        '3301':'Chromatic Lydian',
        '3385':'Chromatic Lydian Inverse',
        '3698':'Chromatic Mixolydian',
        '2675':'Chromatic Mixolydian Inverse',
        '4088':'Chromatic Nonamirror',
        '4080':'Chromatic Octamirror',
        '3968':'Chromatic Pentamirror',
        '3805':'Chromatic Permuted Diatonic Dorian',
        '2507':'Chromatic Phrygian',
        '3740':'Chromatic Phrygian Inverse',
        '3840':'Chromatic Tetramirror',
        '3584':'Chromatic Trimirror',
        '4094':'Chromatic Undecamirror',
        '2336':'Diminished Chord',
        '2925':'Diminished Scale',
        '2340':'Diminished Seventh Chord',
        '2775':'Dominant Bebop',
        '2706':'Dominant Pentatonic',
        '2902':'Dorian',
        '2910':'Dorian Aeolian',
        '2918':'Dorian Flat 5',
        '2836':'Dorian Pentatonic',
        '3392':'Dorian Tetrachord',
        '3290':'Dorico Flamenco',
        '3428':'Double-Phrygian Hexatonic',
        '2729':'Eskimo Hexatonic 2 (North America)',
        '2704':'Eskimo Tetratonic (North America)',
        '2911':'Full Minor',
        '3549':'Genus Chromaticum',
        '2805':'Genus Diatonicum Veterum Correctum',
        '2640':'Genus Primum',
        '2130':'Genus Primum Inverse',
        '2261':'Genus Secundum',
        '3292':'Gipsy Hexatonic',
        '2870':'Gnossiennes',
        '3449':'Half-Diminished Bebop',
        '2648':'Han-kumoi (Japan)',
        '2777':'Harmonic Major',
        '2905':'Harmonic Minor',
        '3286':'Harmonic Minor Inverse',
        '2848':'Harmonic Minor Tetrachord',
        '3929':'Harmonic Neapolitan Minor',
        '2837':'Hawaiian',
        '2840':'Hira-joshi (Japan)',
        '3426':'Honchoshi Plagal Form (Japan)',
        '3038':'Houseini (Greece)',
        '2517':'Houzam (Greece)',
        '2486':'Hungarian Major',
        '2765':'Ionian Sharp 5',
        '3170':'Iwato (Japan)',
        '3376':'Javanese Pentachord',
        '2901':'Jazz Minor',
        '3414':'Jazz Minor Inverse',
        '2942':'Kiourdi (Greece)',
        '3154':'Kokin-joshi, Miyakobushi (Japan)',
        '2724':'Kung (China)',
        '3434':'Locrian',
        '2921':'Locrian 2',
        '3436':'Locrian Double-Flat 7',
        '3430':'Locrian Natural 6',
        '3424':'Locrian Pentamirror',
        '2741':'Lydian',
        '2733':'Lydian Augmented',
        '2869':'Lydian Diminished',
        '2709':'Lydian Hexatonic',
        '2746':'Lydian Minor',
        '2736':'Lydian Pentachord',
        '2485':'Lydian Sharp 2',
        '2453':'Lydian Sharp 2 Hexatonic',
        '3501':'Magen Abot (Israel)',
        '2773':'Major',
        '3039':'Major And Minor Mixed',
        '2781':'Major Bebop',
        '2716':'Major Bebop Hexatonic',
        '2192':'Major Chord',
        '3289':'Major Gipsy',
        '2794':'Major Locrian',
        '2778':'Major Minor',
        '2768':'Major Pentachord',
        '2708':'Major Pentatonic',
        '2049':'Major Seventh Interval',
        '2052':'Major Sixth Interval',
        '2752':'Major Tetrachord',
        '2176':'Major Third Interval',
        '3291':'Maqam Hijaz (Arabia)',
        '3558':'Maqam Shaddaraban (Arabia)',
        '3253':'Marva Thaat (India)',
        '3386':'Mela Bhavapriya (India)',
        '2739':'Mela Citrambari (India)',
        '2489':'Mela Dhatuvardhani (India)',
        '3260':'Mela Dhavalambari (India)',
        '3379':'Mela Divyamani (India)',
        '3673':'Mela Ganamurti (India)',
        '2521':'Mela Gangeyabhusani (India)',
        '3388':'Mela Gavambodhi (India)',
        '3283':'Mela Hatakambari (India)',
        '3642':'Mela Jalarnava (India)',
        '3641':'Mela Jhalavarali (India)',
        '2908':'Mela Jhankaradhvani (India)',
        '2490':'Mela Jyotisvarupini (India)',
        '2748':'Mela Kantamani (India)',
        '2745':'Mela Latangi (India)',
        '3669':'Mela Manavati (India)',
        '2780':'Mela Mararanjani (India)',
        '2771':'Mela Naganandini (India)',
        '3258':'Mela Namanarayani (India)',
        '3638':'Mela Navanitam (India)',
        '2867':'Mela Nitimati (India)',
        '3637':'Mela Pavani (India)',
        '2522':'Mela Ragavardhani (India)',
        '3635':'Mela Raghupriya (India)',
        '2483':'Mela Rasikapriya (India)',
        '3674':'Mela Ratnangi (India)',
        '3411':'Mela Rupavati (India)',
        '3382':'Mela Sadvidhamargini (India)',
        '3644':'Mela Salaga (India)',
        '2874':'Mela Sanmukhapriya (India)',
        '3420':'Mela Senavati (India)',
        '2492':'Mela Sucaritra (India)',
        '3381':'Mela Suvarnangi (India)',
        '2876':'Mela Syamalangi (India)',
        '3667':'Mela Tanarupi (India)',
        '3670':'Mela Vanaspati (India)',
        '2899':'Mela Varunapriya (India)',
        '3251':'Mela Visvambhari (India)',
        '2524':'Mela Yagapriya (India)',
        '3822':'Messiaen Mode 3',
        '3003':'Messiaen Mode 3 Inverse',
        '3900':'Messiaen Mode 4',
        '2535':'Messiaen Mode 4 Inverse',
        '3640':'Messiaen Mode 5',
        '2275':'Messiaen Mode 5 Inverse',
        '3770':'Messiaen Mode 6',
        '2795':'Messiaen Mode 6 Inverse',
        '4030':'Messiaen Mode 7',
        '3055':'Messiaen Mode 7 Inverse',
        '3380':'Messiaen Truncated Mode 2',
        '3276':'Messiaen Truncated Mode 3',
        '2457':'Messiaen Truncated Mode 3 Inverse',
        '3120':'Messiaen Truncated Mode 5',
        '2145':'Messiaen Truncated Mode 5 Inverse',
        '2600':'Messiaen Truncated Mode 6',
        '2210':'Messiaen Truncated Mode 6 Inverse',
        '2906':'Minor',
        '2388':'Minor Added Sixth Pentatonic',
        '3030':'Minor Bebop',
        '2966':'Minor Bebop Hexatonic',
        '2320':'Minor Chord',
        '2873':'Minor Gipsy',
        '2898':'Minor Hexatonic',
        '2922':'Minor Locrian',
        '3063':'Minor Pentatonic With Leading Tones',
        '2050':'Minor Seventh Interval',
        '2056':'Minor Sixth Interval',
        '2304':'Minor Third Interval',
        '2816':'Minor Trichord',
        '2774':'Mixolydian',
        '2790':'Mixolydian Flat 5',
        '2646':'Mixolydian Hexatonic',
        '2258':'Mixolydian Pentatonic',
        '2766':'Mixolydian Sharp 5',
        '3547':'Moorish Phrygian',
        '3413':'Neapolitan Major',
        '3417':'Neapolitan Minor',
        '3756':'Neapolitan Minor Mode',
        '3387':'Neveseri (Greece)',
        '2669':'Nohkan (Japan)',
        '3302':'Oriental',
        '3680':'Oriental Pentacluster',
        '2742':'Overtone',
        '3352':'Pelog (Bali)',
        '2064':'Perfect Fifth Interval',
        '2112':'Perfect Forth Interval',
        '3418':'Phrygian',
        '3930':'Phrygian Aeolian',
        '3482':'Phrygian Flat 4',
        '2394':'Phrygian Hexatonic',
        '3450':'Phrygian Locrian',
        '2880':'Phrygian Tetrachord',
        '3328':'Phrygian Trichord',
        '3435':'Prokofiev Scale',
        '2726':'Prometheus',
        '3238':'Prometheus Neapolitan',
        '2916':'Pyramid Hexatonic',
        '2884':'Raga Abhogi (India)',
        '2865':'Raga Amarasenapriya (India)',
        '2888':'Raga Audav Tukhari (India)',
        '2886':'Raga Bagesri, Sriranjani, Kapijingla (India)',
        '3225':'Raga Bauli (India)',
        '2514':'Raga Bhanumanjari (India)',
        '3317':'Raga Bhatiyar (India)',
        '2628':'Raga Bhavani (India)',
        '3370':'Raga Bhavani (India)',
        '2649':'Raga Bhinna Pancama (India)',
        '2245':'Raga Bhinna Shadja, Hindolita (India)',
        '2712':'Raga Bhupeshwari, Janasammodini (India)',
        '2180':'Raga Bilwadala (India)',
        '2737':'Raga Caturangini (India)',
        '3636':'Raga Chandrajyoti (India)',
        '2374':'Raga Chandrakauns Kafi, Surya (India)',
        '2377':'Raga Chandrakauns Kiravani (India)',
        '2373':'Raga Chandrakauns Modern, Marga Hindola (India)',
        '3368':'Raga Chhaya Todi (India)',
        '3400':'Raga Chitthakarshini (India)',
        '2878':'Raga Cintamani (India)',
        '3097':'Raga Deshgaur (India)',
        '2641':'Raga Desh (India)',
        '2137':'Raga Devaranjani (India)',
        '3256':'Raga Dhavalangam (India)',
        '2800':'Raga Dipak (India)',
        '2257':'Raga Gambhiranata (India)',
        '3410':'Raga Gandharavam (India)',
        '3281':'Raga Gaula (India)',
        '3153':'Raga Gauri (India)',
        '2889':'Raga Ghantana (India)',
        '2630':'Raga Guhamanohari (India)',
        '2705':'Raga Hamsadhvani (India)',
        '3237':'Raga Hamsanandi, Puriya (India)',
        '2757':'Raga Hamsa Vinodini (India)',
        '2346':'Raga Harikauns (India)',
        '2632':'Raga Haripriya (India)',
        '3244':'Raga Hejjajji (India)',
        '2213':'Raga Hindol (India)',
        '3250':'Raga Indupriya (India)',
        '2618':'Raga Jaganmohanam (India)',
        '2402':'Raga Jayakauns (India)',
        '2355':'Raga Jivantini, Gaurikriya (India)',
        '2234':'Raga Jyoti (India)',
        '3228':'Raga Kalagada (India)',
        '3164':'Raga Kalakanthi (India)',
        '3284':'Raga Kalavati, Ragamalini (India)',
        '2266':'Raga Kamalamanohari (India)',
        '3354':'Raga Kashyapi (India)',
        '2246':'Raga Khamaji Durga (India)',
        '2262':'Raga Khamas, Baduhari (India)',
        '2392':'Raga Kokil Pancham (India)',
        '3145':'Raga Kshanika (India)',
        '3593':'Raga Kumarapriya (India)',
        '2721':'Raga Kumurdaki (India)',
        '2134':'Raga Kuntvarali (India)',
        '2713':'Raga Latika (India)',
        '3144':'Raga Lavangi (India)',
        '2358':'Raga Madhukauns (India)',
        '2263':'Raga Madhuri (India)',
        '2194':'Raga Mahathi (India)',
        '3288':'Raga Malahari (India)',
        '2611':'Raga Malarani (India)',
        '3222':'Raga Malayamarutam (India)',
        '2378':'Raga Malkauns (India)',
        '2197':'Raga Mamata (India)',
        '3218':'Raga Manaranjani (India)',
        '2838':'Raga Manavi (India)',
        '3249':'Raga Mandari, Gamakakriya (India)',
        '2260':'Raga Mand (India)',
        '2390':'Raga Manohari (India)',
        '2582':'Raga Matha Kokila (India)',
        '3265':'Raga Megharanji (India)',
        '2643':'Raga Megh (India)',
        '2903':'Raga Mian Ki Malhar, Bahar (India)',
        '2452':'Raga Mohanangi (India)',
        '2725':'Raga Mruganandana (India)',
        '2353':'Raga Multani (India)',
        '3632':'Raga Nabhomani (India)',
        '2645':'Raga Nagagandhari (India)',
        '2769':'Raga Nalinakanti, Kedaram (India)',
        '2385':'Raga Nata, Madhuranjani (India)',
        '2650':'Raga Navamanohari (India)',
        '2860':'Raga Neelangi (India)',
        '2693':'Raga Neroshta (India)',
        '2209':'Raga Nigamagamini (India)',
        '2613':'Raga Nishadi (India)',
        '2096':'Raga Ongkari (India)',
        '3161':'Raga Padi (India)',
        '2783':'Raga Pahadi (India)',
        '2265':'Raga Paraju, Simhavahini (India)',
        '3162':'Raga Phenadyuti (India)',
        '2633':'Raga Priyadharshini (India)',
        '2133':'Raga Puruhutika, Purvaholika (India)',
        '3596':'Raga Putrika (India)',
        '2758':'Raga Rageshri, Nattaikurinji (India)',
        '2759':'Raga Ragesri (India)',
        '3031':'Raga Ramdasi Malhar (India)',
        '3321':'Raga Ramkali (India)',
        '2853':'Raga Ranjani, Rangini (India)',
        '2481':'Raga Rasamanjari (India)',
        '3158':'Raga Rasavali (India)',
        '2629':'Raga Rasranjani (India)',
        '3224':'Raga Reva, Revagupti (India)',
        '3270':'Raga Rudra Pancama (India)',
        '3346':'Raga Rukmangi (India)',
        '3350':'Raga Salagavarali (India)',
        '2354':'Raga Samudhra Priya (India)',
        '2761':'Raga Sarasanana (India)',
        '2614':'Raga Sarasvati (India)',
        '2268':'Raga Saravati (India)',
        '2128':'Raga Sarvasri (India)',
        '3128':'Raga Saugandhini, Yashranjani (India)',
        '3293':'Raga Saurashtra (India)',
        '2330':'Raga Shailaja (India)',
        '2612':'Raga Shri Kalyan (India)',
        '2597':'Raga Shubravarni (India)',
        '2866':'Raga Simharava (India)',
        '4059':'Raga Sindhi Bhairavi (India)',
        '2897':'Raga Sindhura Kafi (India)',
        '2770':'Raga Siva Kambhoji, Vivardhini (India)',
        '3273':'Raga Sohini (India)',
        '2647':'Raga Sorati (India)',
        '2900':'Raga Suddha Bangala (India)',
        '3660':'Raga Suddha Mukhari (India)',
        '3416':'Raga Suddha Simantini (India)',
        '2593':'Raga Sumukam (India)',
        '2872':'Raga Syamalam (India)',
        '2393':'Raga Takka (India)',
        '2259':'Raga Tilang, Savitri (India)',
        '2842':'Raga Trimurti (India)',
        '2609':'Raga Vaijayanti (India)',
        '2198':'Raga Valaji (India)',
        '3274':'Raga Vasantabhairavi (India)',
        '3269':'Raga Vasanta, Chayavati (India)',
        '2868':'Raga Vijayanagari (India)',
        '3633':'Raga Vijayasri (India)',
        '2227':'Raga Vijayavasanta (India)',
        '3401':'Raga Viyogavarali (India)',
        '2230':'Raga Vutari (India)',
        '2740':'Raga Yamuna Kalyani (India)',
        '2264':'Raga Zilaf (India)',
        '3402':'Ritsu (Japan)',
        '2518':'Rock n Roll',
        '2249':'Romanian Bacovia',
        '3254':'Romanian Major',
        '2970':'Sabach (Greece)',
        '3160':'Sakura Pentatonic (Japan)',
        '2114':'Sansagari (Japan)',
        '2644':'Scottish Pentatonic',
        '3220':'Scriabin',
        '3072':'Semitone Interval',
        '3509':'Shostakovich Scale',
        '3562':'Spanish Octatonic',
        '3520':'Spanish Pentacluster',
        '3546':'Spanish Phrygian',
        '3498':'Super Locrian',
        '2642':'Suspended Pentatonic',
        '3835':'Symmetrical Decatonic',
        '2807':'Taishikicho, Ryo (Japan)',
        '2857':'Takemitsu Tree Line Mode 1',
        '2858':'Takemitsu Tree Line Mode 2',
        '2080':'Tritone Interval',
        '4095':'Twelve-Tone Chromatic',
        '3500':'Ultra Locrian',
        '2048':'Unison',
        '2306':'Ute Triunic (North America)',
        '2907':'Utility Minor',
        '3307':'Verdi Enigmatic',
        '3243':'Verdi Enigmatic Ascending',
        '3275':'Verdi Enigmatic Descending',
        '2818':'Warao Tetratonic (South America)',
        '2560':'Wholetone Interval',
        '2730':'Wholetone Scale',
        '2731':'Wholetone Scale With Leading Tone',
        '2720':'Wholetone Tetramirror',
        '2688':'Wholetone Trichord',
        '3830':'Youlan Scale (China)',
        '2909':'Zirafkend (Arabia)'
        }


