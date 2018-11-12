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
    
    plot = plt.bar( range( len( dept_totals_high ) ), [val for dept,val in dept_totals_high], align='center', color='orange')
    plt.ylabel('Signatures')
    plt.xticks( range( len( dept_totals_high) ), [dept for dept,val in dept_totals_high] )

    return plot
