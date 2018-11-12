import gspread
from oauth2client.service_account import ServiceAccountCredentials
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from collections import Counter

SCOPE = ['https://spreadsheets.google.com/feeds',
                  'https://www.googleapis.com/auth/drive']
SECRETS_FILE = "secret_key.json"
SPREADSHEET = "Graduate workers need a student fee waiver. (Responses)"

def plot_make():
    # Authenticate using the signed key
    credentials = ServiceAccountCredentials.from_json_keyfile_name(SECRETS_FILE, SCOPE)
    gc = gspread.authorize(credentials)
    
    # Pull Google Sheet and convert to Pandas DataFrame
    responses = gc.open(SPREADSHEET).sheet1.get_all_records()
    
    # Get dept responses
    depts = [ elem[u'Department or program (4-letter code preferred)'] for elem in responses ]
    
    # Ditch all responses that aren't 4 letters long (or that aren't unicode strings for some reason)
    # simultaneously convert to a string
    depts = [ str(d).upper() for d in filter( lambda s: (len(s) == 4) & (type(s) == unicode), depts ) ]
    dept_totals = dict(Counter(depts))
    dept_totals = sorted([ (val, dept) for dept,val in dept_totals.items() ], reverse=True )
    cutoff = 10
    dept_totals_high = [ (dept,val) for val,dept in dept_totals if val > cutoff ]


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
    ax.tick_params( direction='in', top=False, right=False)
    ax.set_xticklabels( [dept for dept,val in dept_totals_high] )
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    
    
#    plot = plt.subplot(111)
#    plot.bar( range( len( dept_totals_high ) ),
#              [val for dept,val in dept_totals_high],
#              align='center',
#              color=(1.,170./255.,60./255.),
#              edgecolor=(1.,170./255.,60./255.)
#    )
#
#    plot.set_xticklabels([dept for dept,val in dept_totals_high])
#    #plt.setp(plot,
#    #         xticks = range( len( dept_totals_high) ),
#    #         xticklabels=[dept for dept,val in dept_totals_high]
#    #)
#    
#    plot.set_ylabel('Signatures')
#    plot.spines['right'].set_visible(False)
#    plot.spines['top'].set_visible(False)
#    #plot.spines['left'].set_position(('outward',10))
#    plot.spines['bottom'].set_position(('outward',10))
#    
   
    return plot
