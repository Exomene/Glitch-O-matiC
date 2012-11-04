#!/usr/bin/python2
#-*- encoding: utf-8 -*-

"""
Glitch-O-matiC by Exomène

This work is licensed under the Creative Commons Attribution-NonCommercial-ShareAlike 3.0 Unported License. To view a copy of this license, visit http://creativecommons.org/licenses/by-nc-sa/3.0/.

This script requires external softwares
    gphoto: http://www.gphoto.org/ that fires a digital camera from the computer
    imagemagick: http://www.imagemagick.org/ that enhance the images
    The Eye Of Gnome: http://projects.gnome.org/eog/ that displays the images (but could be replaced by the "display" command from imagemagick)
It uses two sounds from freesound (http://www.freesound.org/)
    "clean modem beep" by the_semen_incident (http://www.freesound.org/people/the_semen_incident/sounds/39013/)
    "Camera Shutter" by ThompsonMan (http://www.freesound.org/people/ThompsonMan/sounds/166500/)
"""

#Chemin du dossier en variable globale
cheminInitial='~/GlitchOmatiC/'

#modules
import binascii
import time
import subprocess
import commands
import random
import shutil
import itertools
import os
import datetime
import asciiArt

def glitcheur(stream):
    iterateur=set(range(0, len(stream)))
    i=random.choice(list(iterateur))
    random.seed(i)
    #isoler substring
    randStartString=random.randint(0,len(stream))
    i=random.choice(list(iterateur))
    random.seed(i)
    startString=random.randint(randStartString,len(stream))
    endString=len(stream)-startString
    #Spécifique à l'EOS 7D, ligne à modifier en fonction de l'APN utilisé
    endString=startString+int(len(stream)*0.001)
    #On isole une sous-chaîne
    substring=stream[startString:endString]
    substring=substring.replace(chr(random.randint(0,255)), chr(random.randint(25,255)), random.randint(0, len(substring)))
    #Deplacement
    i=random.choice(list(iterateur))
    random.seed(i)
    #Spécifique à l'EOS 7D, ligne à modifier en fonction de l'APN utilisé
    startString=int(random.randint(randStartString,len(stream))/15)
    stream=stream[0:startString]+substring+stream[startString+len(substring):len(stream)]
    return stream

def imageur(repName):
    #On affiche l'image originale
    viewer = subprocess.Popen(['eog', "-f", repName+"/0.jpg"])
    #récupération des données
    iteration=str(len(os.walk(repName).next()[2])-1)
    #Ouverture d'un fichier, puis lecture avec read
    with open(repName+'/'+iteration+'.jpg','rb') as f:
        byteList = f.read()
    #Séparation du fichier en header, stream, footer
    separations = byteList.split(binascii.unhexlify('ffda'))
    header = separations[0]
    stream = binascii.unhexlify('ffda').join(separations[1:])
    separations = stream.split(binascii.unhexlify('ffd9'))
    footer = separations[-1]
    footer = binascii.unhexlify('ffd9')+footer
    stream = binascii.unhexlify('ffd9').join(separations[:-1])
    stream = binascii.unhexlify('ffda')+stream
    stream = bytearray(stream)
    #Manipulation du stream
    iNteration=int(str(len(os.walk(repName).next()[2])))
    while iNteration<3:
        iteration=str(len(os.walk(repName).next()[2]))
        iNteration=int(iteration)
        #Remplacer, Déplacer, intervertir, dupliquer des séquences
        for _ in itertools.repeat(None, 1+(iNteration)) :
            stream=glitcheur(stream)
        #Recomposition du fichier
        image=header+stream+footer
        #Écriture du fichier
        iteration=str(len(os.walk(repName).next()[2]))
        imageFile=open(repName+'/'+iteration+".jpg", "w")
        imageFile.write(image)
        imageFile.close()
        #Affichage du fichier
        viewer.terminate()
        viewer.kill()
        #Amélioration de l'image (contraste et luminosité automatique)
        commands.getstatusoutput("mogrify -normalize -auto-gamma -quiet "+repName+"/"+iteration+".jpg")
        viewer = subprocess.Popen(['eog', "-f", repName+"/"+iteration+".jpg"])
        commands.getstatusoutput('play '+cheminInitial+'166500__thompsonman__camera-shutter.wav')
        time.sleep(10)
    time.sleep(10)
    viewer.terminate()
    viewer.kill()
    detecteur(cheminInitial, repName)

#Déclencher l'APN
def declencheur(repname):
    baseName=repname
    baseName=baseName+datetime.datetime.now().strftime("%Y-%m-%d_%H:%M:%S")
    commands.getstatusoutput('gphoto2 --capture-image-and-download --force-overwrite')
    os.mkdir(baseName)
    shutil.copyfile('~/capt0000.jpg',baseName+'/0.jpg')
    shutil.copystat('~/capt0000.jpg',baseName+'/0.jpg')
    imageur(baseName)

def detecteur(repname, madeDir):
    os.system('clear')
    print('Last dir: '+madeDir)
    print(asciiArt.asciiName)
    raw_input(asciiArt.asciiStart+asciiArt.asciiSit)
    for counter in range(4, -1, -1):
        os.system('clear')
        print(asciiArt.asciiName+asciiArt.asciiPic+asciiArt.asciiNum[counter])
        commands.getstatusoutput('play '+cheminInitial+'39013__the-semen-incident__clean-modem-beep.wav')
        time.sleep(1)
    declencheur(repname)
###################### Début ##########################
detecteur(cheminInitial, '')