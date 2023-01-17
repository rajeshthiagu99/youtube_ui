import torch
import whisper
import openai 
import time as t
import os
import textwrap
# importing packages
from pytube import YouTube
import os
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

# create transcript_files if not exists
if not os.path.exists('transcript_files'):
    os.mkdir('transcript_files')
if not os.path.exists('prompts'):
    os.mkdir('prompts')
if not os.path.exists('output'):
    os.mkdir('output')

# Transcript generation

def genarate_transcript(link):
    yt = YouTube(link)
    # extract only audio
    video = yt.streams.filter(only_audio=True).first()
    # check for destination to save file
    destination = 'transcript_files'
    # download the file
    out_file = video.download(output_path=destination)
    # save the file
    base, ext = os.path.splitext(out_file)
    new_file = base + '.mp3'
    os.rename(out_file, new_file)
    # transcribe the audio file
    model = whisper.load_model("base.en")
    result = model.transcribe(new_file)
    with open(new_file.replace('mp3','txt'), "w+") as f:
        f.write(result["text"])
    # remove mp3 file
    os.remove(new_file)
    return new_file.replace('mp3','txt')


def get_generated_text(prompt,engine='text-davinci-003',temp=0.3,tokens=2000,top_p=1,freq_penalty=0,pres_penalty=0,stop=['asdfasdf','asdasdf']):
    result =False
    while result!=True:
        try:
            response = openai.Completion.create(
                engine=engine,
                prompt = prompt,
                temperature=temp,
                max_tokens=tokens,
                top_p=top_p,
                frequency_penalty=freq_penalty,
                presence_penalty=pres_penalty,
                stop=stop

            )
            result = True
        except Exception as e:
            print(e)
            print('Because of API error, waiting for 5 seconds')
            t.sleep(5)
    return response.choices[0].text

def generate_gpt3_output(transcript_file,prompt_file):
    # open transcript
    with open(transcript_file,'r') as f:
        transcript = f.read()
    chunks = textwrap.wrap(transcript, 6000)
    output = []
    for chunk in chunks:
        # open transcript
        with open(prompt_file,'r') as f:
            prompt = f.read().replace('<<TRANSCRIPT>>',chunk)
        essay = get_generated_text(prompt)
        output.append(essay)
    result = '\n\n'.join(output)
    # save result in new file in output
    with open('output/'+transcript_file.split('/')[-1],'w') as f:
        f.write(result)
    return 'output/'+transcript_file.split('/')[-1]

# get list of files in prompts
def get_prompt_files():
    return os.listdir('prompts')

# get list of files in transcript_files
def get_transcript_files():
    return os.listdir('transcript_files')

# get list of files in output
def get_output_files():
    return os.listdir('output')