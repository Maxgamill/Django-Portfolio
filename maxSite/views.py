from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render
from django.views.decorators.clickjacking import xframe_options_exempt
from maxSite.project_scripts import switchboard as scripts_switchboard
import matplotlib.pyplot as plt
import io
import base64, urllib
import os

def index(request):
    return render(request, 'index.html')

def switchboard(request):
    if request.method == 'POST':
        if list(request.POST.keys())[0] == 'testMessage':
            message = request.POST['testMessage']
            newMessage = scripts_switchboard.test(message)
            httprep = HttpResponse(newMessage)

        elif list(request.POST.keys())[0] == 'NNMessage':
            img_bytes = request.POST['NNMessage']
            #data_file = '/var/www/djangoSite/maxSite/neuralNet/number.png'
            data_file = os.getcwd() + '/maxSite/neuralNet/number.png'
            temp = open(data_file, 'wb')
            temp.write(base64.b64decode((img_bytes[22:])))
            temp.close()
            newMessage = scripts_switchboard.trainedNetwork(data_file)
            httprep = HttpResponse(newMessage)

        elif list(request.POST.keys())[0] == 'population':
            pop = request.POST['population']
            fract = request.POST.get('fraction')
            recovr = request.POST['recovery']
            infections = request.POST['infect']
            numd = request.POST['days']
            reps = request.POST['repeats']
            reinfect = request.POST['reinfection']
            
            fig = scripts_switchboard.sod(pop,fract,recovr,infections,numd,reps,reinfect)
            
            buffer = io.BytesIO()
            plt.savefig(buffer, format='png')
            buffer.seek(0)
            string = base64.b64encode(buffer.read())
            uri = urllib.parse.quote(string)
            httprep = HttpResponse(uri)
            plt.close(fig)
        
        elif list(request.POST.keys())[0] == 'N':
            sites = request.POST['N']
            T = request.POST.get('T')
            mag = request.POST['B']
            mom = request.POST['m']
            calc = request.POST['c']
            points = request.POST['p']

            fig = scripts_switchboard.ising(sites,T,mag,mom,calc,points)

            buffer = io.BytesIO()
            plt.savefig(buffer, format='png')
            buffer.seek(0)
            string = base64.b64encode(buffer.read())
            uri = urllib.parse.quote(string)
            httprep = HttpResponse(uri)
            plt.close(fig)

        else:
            pass
    return httprep

@xframe_options_exempt
def canvas(request):
    return render(request, 'canvas.html')