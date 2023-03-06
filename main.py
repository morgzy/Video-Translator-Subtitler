"""
Video Translator
Translates audio from video and returns new video with translated subtitles.

Still to do:
Match subtitles to audio

By Morgan Hopkins, 2022
"""

# Import standard libraries
import os
import wave
import contextlib
import math
import argparse

# Import external libraries
import speech_recognition as sr
from googletrans import Translator

# Initialise argparse and parse arguments
parser = argparse.ArgumentParser( description = "Translate and subtitle source_file." )
parser.add_argument("source_file")
parser.add_argument("source_lang")
parser.add_argument("dest_lang")
arguments = parser.parse_args()

# Get file name and use delimiter
file = arguments.source_file
fileSplit = file.split('.')
fName = fileSplit[0]

# Get OS commands for audio conversion
commandWav = "ffmpeg -i ./Videos/" + file + " ./Videos/" + fName + ".wav -y"
# Convert to wav
os.system(commandWav)
print("Audio ripped from file.")

# Get length of wav file
audioFile = "./Videos/" + fName + ".wav"
with contextlib.closing(wave.open(audioFile, 'r')) as f:
    frames = f.getnframes()
    rate = f.getframerate()
    length = math.ceil(frames / float(rate))
    print("Audio length captured.")

# Initialise Translator and Speech Recognizer
translator = Translator()
r = sr.Recognizer()

# Convert speech to text
srcLang = arguments.source_lang
destLang = arguments.dest_lang
audio = sr.AudioFile(audioFile)
snippets = []
snip = 10
segments = math.ceil((length / snip))
print(length, segments)
textSnippets = []
transText = ""

# Record audio
with audio as source:
    r.adjust_for_ambient_noise(source)
    audio_file = r.record(source)
    fullText = r.recognize_google(audio_data=audio_file, language=srcLang)

# Break audio in to snip length segments
for i in range(0, segments):
    # Set start time
    start = i-0.05
    if start < 0:
        start = 0
    segment = audio_file.get_segment(start_ms=(start*10000), end_ms=((i+1.05)*10000))
    snippets.append(segment)
print("Audio snipped.")

# Translate snippets
for i in range(0, segments):
    try:
        get = snippets[i]
        print("\nSOURCE"+str(get)+" "+str(i))
        # with audio as source:
        transText = r.recognize_google(audio_data=get, language=srcLang)
        textSnippets.append(transText)
    except:
        print("Snippet failed to translate")
        textSnippets.append("failed to translate")
print("Snippets translated.")

# Translate text
transSnippets = []
translatedText = translator.translate(fullText, src=srcLang, dest=destLang)
print(translatedText.text)
for snippet in textSnippets:
    transSnippets.append(translator.translate(snippet, src=srcLang, dest=destLang))

for snippet in transSnippets:
    print(snippet.text)

print()
print("Translation:\n"+translatedText.text)

# Create subtitles
srtName = "./SRT/"+fName+".txt"
with open(srtName, "wb") as f:
    for i in range(0, segments):
        start = (i*10) % 60
        if start == 0:
            start="00"
        else:
            start = str(start)
        end = str(((i+1)*10) % 60)
        minute = str(math.floor((i*10)/60))
        text = str(i+1)+"\n"
        f.write(text.encode())
        text = "00:0"+minute+":"+start+",00 --> 00:0"+minute+":"+end+",00\n"
        f.write(text.encode())
        text = transSnippets[i].text+"\n"
        f.write(text.encode())
        f.write("\n".encode())
    f.close()

# Convert subtitles to srt
os.system("cp ./SRT/"+fName+".txt ./SRT/"+fName+".srt")
print("Created subtitles.")

# Attach subtitles to video
sub = "ffmpeg -i ./Videos/"+file+" -vf subtitles=./SRT/"+fName+".srt ./Translated/"+fName+"_sub.mp4 -y"
os.system(sub)

print("*** VIDEO TRANSLATION SUCCESSFUL ***")

# Afrikaans af
# Basque eu
# Bulgarian bg
# Catalan ca
# Arabic (Egypt) ar-EG
# Arabic (Jordan) ar-JO
# Arabic (Kuwait) ar-KW
# Arabic (Lebanon) ar-LB
# Arabic (Qatar) ar-QA
# Arabic (UAE) ar-AE
# Arabic (Morocco) ar-MA
# Arabic (Iraq) ar-IQ
# Arabic (Algeria) ar-DZ
# Arabic (Bahrain) ar-BH
# Arabic (Lybia) ar-LY
# Arabic (Oman) ar-OM
# Arabic (Saudi Arabia) ar-SA
# Arabic (Tunisia) ar-TN
# Arabic (Yemen) ar-YE
# Czech cs
# Dutch nl-NL
# English (Australia) en-AU
# English (Canada) en-CA
# English (India) en-IN
# English (New Zealand) en-NZ
# English (South Africa) en-ZA
# English(UK) en-GB
# English(US) en-US
# Finnish fi
# French fr-FR
# Galician gl
# German de-DE
# Hebrew he
# Hungarian hu
# Icelandic is
# Italian it-IT
# Indonesian id
# Japanese ja
# Korean ko
# Latin la
# Mandarin Chinese zh-CN
# Traditional Taiwan zh-TW
# Simplified China zh-CN ?
# Simplified Hong Kong zh-HK
# Yue Chinese (Traditional Hong Kong) zh-yue
# Malaysian ms-MY
# Norwegian no-NO
# Polish pl
# Pig Latin xx-piglatin
# Portuguese pt-PT
# Portuguese (brasil) pt-BR
# Romanian ro-RO
# Russian ru
# Serbian sr-SP
# Slovak sk
# Spanish (Argentina) es-AR
# Spanish(Bolivia) es-BO
# Spanish( Chile) es-CL
# Spanish (Colombia) es-CO
# Spanish(Costa Rica) es-CR
# Spanish(Dominican Republic) es-DO
# Spanish(Ecuador) es-EC
# Spanish(El Salvador) es-SV
# Spanish(Guatemala) es-GT
# Spanish(Honduras) es-HN
# Spanish(Mexico) es-MX
# Spanish(Nicaragua) es-NI
# Spanish(Panama) es-PA
# Spanish(Paraguay) es-PY
# Spanish(Peru) es-PE
# Spanish(Puerto Rico) es-PR
# Spanish(Spain) es-ES
# Spanish(US) es-US
# Spanish(Uruguay) es-UY
# Spanish(Venezuela) es-VE
# Swedish sv-SE
# Turkish tr
# Zulu zu

