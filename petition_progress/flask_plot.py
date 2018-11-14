import io
from flask import Flask, Response, render_template, send_file, request
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import gc

execfile('plot_make.py')

app = Flask(__name__)

@app.route('/')
def plot_png():
    allQ = request.args.get('all')

    if allQ == 'true':
        fig = plot_make_all()

    else:
        fig = plot_make_top_ten()    

    output = io.BytesIO()
    output.seek(0)
    plt.savefig(output, format='svg')
    plt.close()
    return Response(output.getvalue(), mimetype='image/svg+xml')

