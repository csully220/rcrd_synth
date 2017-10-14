valid_genres = {'Classical':15,
                'Piano':10,
                'Guitar':11,
                'Ambient':25,
                'Rock/Pop':30,
                'Dance':40,
                'Hip Hop':45,
                'R&B':60,
                'Blues':55,
                'Jazz':50,
                'Country':65,
                'Latin':70,
                'World':80,
                'Experimental':90,
                'Signaling':95}

valid_rule_types = {7,15,31,55,61,62,79,91,103,110,157,167,773,1047,1585}
rule_range = [1, 4294967295]
rule_min = 1
rule_max = 4294967295
seed_min = 1
seed_max = 67108863
duration_min = 4 
duration_max = 240
bpm_min = 60
bpm_max = 288
npb_min = 2
npb_max = 16
height_min = 5
height_max = 25
valid_scales = {}
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
                   
valid_roles = {0,1,10,16,20,21,51,52,901,907,912,913,914,915,916,922,923,924,932,101,201,202,102,203,206,103,104,105,107,108,209,110,109,111,121,204,205,122,207,208,210,123,124,127,128,129,130,132,131,135,136,137,144,140,149,141,142,143,145,151,153,154,161,162,163,169,170,180,183,181,182,302,316,301,303,304,305,313,306,307,314,315,340,341,312,308,309,310,311,317,350,351,501,515,516,502,520,521,503,511,545,504,505,544,512,541,542,543,513,510,514,570,536,540,552,551,537,538,561,562}
                   
valid_perc = {0,1,101,102,121,122,123,127,128,129,131,132,133,301,311,322,323,325,321,324,361,362,331,332,333,334,341,342,343,344,345,346,347,348,349,351,352,353,501,401,402,403,404,431,432,433,434,551,552,553,555,554,556,571,572,573,574,575,576,577,578,579,584,586,581,582,583,585,112,113,114,115,451,452,453,454,455,456,457,458,459,460,461,462,463,651,652,681,682,711,712,713,714,601,715,721,722,723,801,803,804,805,807,808,809,810,821,822,823,830,901,911} 
                   