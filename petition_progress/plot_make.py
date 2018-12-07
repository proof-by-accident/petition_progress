import gspread
from oauth2client.service_account import ServiceAccountCredentials
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from collections import Counter
import pickle
import numpy
from google.appengine.api import memcache

SCOPE = ['https://spreadsheets.google.com/feeds',
                  'https://www.googleapis.com/auth/drive']
SECRETS_FILE = "secret_key.json"
SPREADSHEET = "Graduate workers need a student fee waiver. (Responses)"

def plot_make_top():
    # Authenticate using the signed key
    credentials = ServiceAccountCredentials.from_json_keyfile_name(SECRETS_FILE, SCOPE)
    gc = gspread.authorize(credentials)
    

    # Pull Google Sheet and convert to Pandas DataFrame
    # get dept responses
    try:
        responses = gc.open(SPREADSHEET).sheet1.get_all_records()
        depts = [ elem[u'Department or program (4-letter code preferred)'].strip() for elem in responses ]
        memcache.add('departments', pickle.dumps(depts))
    
    except:
        depts_pickled = memcache.get('departments')
        if depts_pickled:
            depts = pickle.loads( depts_pickled )

        else:
            saves = open('depts.pickle','rb')
            depts = pickle.load(saves)
            saves.close()
            
    # Ditch all responses that aren't 4 letters long (or that aren't unicode strings for some reason)
    # simultaneously convert to a string
    depts = [ str(d).upper() for d in filter( lambda s: (len(s) == 4) & (type(s) == unicode), depts ) ]
    dept_totals = dict(Counter(depts))
    dept_totals = sorted([ (val, dept) for dept,val in dept_totals.items() ], reverse=True )
    cutoff = 20
    dept_totals_high = [ (dept,val) for val,dept in dept_totals[:cutoff] ]
    #dept_totals_high = [ (dept,val) for val,dept in dept_totals if val > cutoff ]


    plot = plt.figure()
    ax = plot.add_subplot(1,1,1)
    ax.bar( range( len( dept_totals_high ) ),
              [val for dept,val in dept_totals_high],
              align='center',
              color=(1.,170./255.,60./255.),
              edgecolor=(1.,170./255.,60./255.)
    )

    ax.set_ylabel('Signatures')
    ax.set_xticks( range( len( dept_totals_high ) ) )
    ax.set_xlim(left=-.5, right = len(dept_totals_high) )
    ax.tick_params( direction='in', top=False, right=False)
    ax.set_xticklabels( [dept for dept,val in dept_totals_high] )
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)

    return plot

def plot_make_all():
    # Authenticate using the signed key
    credentials = ServiceAccountCredentials.from_json_keyfile_name(SECRETS_FILE, SCOPE)
    gc = gspread.authorize(credentials)
    
    # Pull Google Sheet and convert to Pandas DataFrame
    # get dept responses
    try:
        responses = gc.open(SPREADSHEET).sheet1.get_all_records()
        depts = [ elem[u'Department or program (4-letter code preferred)'].strip() for elem in responses ]
        memcache.add('departments', pickle.dumps(depts))

    except:
        depts_pickled = memcache.get('departments')
        if depts_pickled:
            depts = pickle.loads( depts_pickled )

        else:
            saves = open('depts.pickle','rb')
            depts = pickle.load(saves)
            saves.close()

        
    # Ditch all responses that aren't 4 letters long (or that aren't unicode strings for some reason)
    # simultaneously convert to a string
    depts = [ str(d).upper() for d in filter( lambda s: (len(s) == 4) & (type(s) == unicode), depts ) ]
    dept_totals = dict(Counter(depts))
    dept_totals = sorted([ (val, dept) for dept,val in dept_totals.items() ], reverse=True )
    dept_totals = [ (dept,val) for val,dept in dept_totals ]

    plot = plt.figure()
    ax = plot.add_subplot(1,1,1)
    x_vals = range(len(dept_totals))
    
    ax.bar( x_vals,
              [val for dept,val in dept_totals],
              align='center',
              color=(1.,170./255.,60./255.),
              edgecolor=(1.,170./255.,60./255.)
    )

    ax.set_ylabel('Signatures')
    ax.set_xticks( x_vals )
    ax.set_xticklabels( [dept for dept,val in dept_totals], rotation=90, size=8 )
    ax.tick_params( direction='in', top=False, right=False)
    ax.set_xlim(left=-.5, right = max(x_vals) )
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)

    return plot
