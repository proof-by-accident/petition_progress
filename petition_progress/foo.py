import io
from flask import Flask, Response
import matplotlib.pyplot as plt

execfile('plot_make.py')

fig = plot_make()
output = io.BytesIO()
output.truncate(0)
plt.savefig(output, format='png')


