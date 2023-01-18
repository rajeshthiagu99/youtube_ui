from flask import Flask, render_template, request
import os
import openai 
import time as t
import textwrap
import glob
from pytube import YouTube
import whisper
import ssl
from pathlib import Path
import torch

ssl._create_default_https_context = ssl._create_unverified_context

app = Flask(__name__,template_folder='template')

# create folders if not exists
if not os.path.exists('transcripts'):
    os.mkdir('transcripts')
if not os.path.exists('prompts'):
    os.mkdir('prompts')
if not os.path.exists('outputs'):
    os.mkdir('outputs')

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
    with open('outputs/'+transcript_file.split('/')[-1],'w') as f:
        f.write(result)
    return transcript_file.split('/')[-1]

# get list of files in transcript files
def get_transcript_files():
    return [file.split('\\')[-1] for file in glob.glob('transcripts/*.txt')]

# get list of files in prompts files
def get_prompt_files():
    return [file.split('\\')[-1] for file in glob.glob('prompts/*.txt')]

# get list of files in output files
def get_output_files():
    return [file.split('\\')[-1] for file in glob.glob('outputs/*.txt')]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/create_transcript', methods=['GET', 'POST'])
def create_transcript():
    if request.method == 'POST':
        link = request.form['youtube_link']
        yt = YouTube(link)

        # extract only audio
        video = yt.streams.filter(only_audio=True).first()

        # check for destination to save file
        destination = 'transcripts'

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
        transcript_file_status = 'File saved in this location : \n'+new_file.replace('mp3','txt')
        return render_template('create_transcript.html',youtube_link=link,transcript_file_status=transcript_file_status)
    else:
        link = ''
        transcript_file_status = ''
    
    return render_template('create_transcript.html',youtube_link=link,transcript_file_status=transcript_file_status)

@app.route('/transcript_files', methods=['GET', 'POST'])
def transcript_files():
    global global_transcript_length_dict,global_transcript_files_list
    
    if request.method == 'POST':
        global_transcript_files_list = get_transcript_files()
        global_transcript_length_dict['length'] = len(global_transcript_files_list)
    return render_template('transcript_files.html',length_dict=global_transcript_length_dict,transcript_files_list=global_transcript_files_list,transcript_download_file='',transcript_upload_file_status='',download_transcript_file_content='')

@app.route('/transcript_download_file',methods=['POST'])
def transcript_download_file():
    global global_transcript_length_dict,global_transcript_files_list

    if request.method == 'POST':
        download_file_name = request.form['download_file_name']
        global_transcript_files_list = get_transcript_files()
        global_transcript_length_dict['length'] = len(global_transcript_files_list)
        if len(download_file_name) > 0:

            # Open the file
            with open(f"transcripts/{download_file_name}", "r") as file:

                # Read the contents of the file
                contents = file.read()
            transcript_download_file = download_file_name.upper()
        else:
            transcript_download_file = ''
            contents = ''
    else:
        transcript_download_file = ''
        contents = ''
    return render_template('transcript_files.html',length_dict=global_transcript_length_dict,transcript_files_list=global_transcript_files_list,transcript_download_file=transcript_download_file,transcript_upload_file_status='',download_transcript_file_content=contents)

@app.route('/transcript_upload_file',methods=['POST'])
def transcript_upload_file():
    global global_transcript_length_dict,global_transcript_files_list

    if request.method == 'POST':
        uploaded_file = request.files['uploaded_file']
        if uploaded_file.filename != '':
            uploaded_file.save(f"transcripts\{uploaded_file.filename}")
            global_transcript_files_list = get_transcript_files()
            global_transcript_length_dict['length'] = len(global_transcript_files_list)
            transcript_upload_file_status = uploaded_file.filename.upper() + ' is uploaded successfully'
        else:
            transcript_upload_file_status = ''
    else:
        transcript_upload_file_status = ''
    return render_template('transcript_files.html',length_dict=global_transcript_length_dict,transcript_files_list=global_transcript_files_list,transcript_download_file='',transcript_upload_file_status=transcript_upload_file_status,download_transcript_file_content='')

@app.route('/gpt_text_workshop',methods=['GET', 'POST'])
def gpt_text_workshop():
    global global_transcript_length_dict,global_transcript_files_list,global_prompt_length_dict,global_prompt_files_list

    if request.method == 'POST':
        global_transcript_files_list = get_transcript_files()
        global_transcript_length_dict['length'] = len(global_transcript_files_list)
        global_prompt_files_list = get_prompt_files()
        global_prompt_length_dict['length'] = len(global_prompt_files_list)
    else:
        global_transcript_length_dict['length'] = 0
        global_prompt_length_dict['length'] = 0
    return render_template('gpt_text_workshop.html',transcript_length_dict=global_transcript_length_dict,prompt_length_dict=global_prompt_length_dict,transcript_files_list=global_transcript_files_list,prompt_files_list=global_prompt_files_list,prompt_download_file='',download_prompt_file_content='',prompt_upload_file_status='',output_file_status='')

@app.route('/prompt_files', methods=['GET', 'POST'])
def prompt_files():
    global global_transcript_length_dict,global_transcript_files_list,global_prompt_length_dict,global_prompt_files_list
    
    if request.method == 'POST':
        global_transcript_files_list = get_transcript_files()
        global_transcript_length_dict['length'] = len(global_transcript_files_list)
        global_prompt_files_list = get_prompt_files()
        global_prompt_length_dict['length'] = len(global_prompt_files_list)
    else:
        global_transcript_length_dict['length'] = 0
        global_prompt_length_dict['length'] = 0
    return render_template('gpt_text_workshop.html',transcript_length_dict=global_transcript_length_dict,prompt_length_dict=global_prompt_length_dict,transcript_files_list=global_transcript_files_list,prompt_files_list=global_prompt_files_list,prompt_download_file='',download_prompt_file_content='',prompt_upload_file_status='',output_file_status='')

@app.route('/prompt_download_file',methods=['POST'])
def prompt_download_file():
    global global_transcript_length_dict,global_transcript_files_list,global_prompt_length_dict,global_prompt_files_list

    if request.method == 'POST':
        download_file_name = request.form['download_file_name']
        global_transcript_files_list = get_transcript_files()
        global_transcript_length_dict['length'] = len(global_transcript_files_list)
        global_prompt_files_list = get_prompt_files()
        global_prompt_length_dict['length'] = len(global_prompt_files_list)
        if len(download_file_name) > 0:

            # Open the file
            with open(f"prompts/{download_file_name}", "r") as file:

                # Read the contents of the file
                contents = file.read()
            prompt_download_file = download_file_name.upper()
        else:
            prompt_download_file = ''
            contents = ''
    else:
        prompt_download_file = ''
        contents = ''
    return render_template('gpt_text_workshop.html',transcript_length_dict=global_transcript_length_dict,prompt_length_dict=global_prompt_length_dict,transcript_files_list=global_transcript_files_list,prompt_files_list=global_prompt_files_list,prompt_download_file=prompt_download_file,download_prompt_file_content=contents,prompt_upload_file_status='',output_file_status='')

@app.route('/prompt_upload_file',methods=['POST'])
def prompt_upload_file():
    global global_transcript_length_dict,global_transcript_files_list,global_prompt_length_dict,global_prompt_files_list

    if request.method == 'POST':
        uploaded_file = request.files['uploaded_file']
        if uploaded_file.filename != '':
            uploaded_file.save(f"prompts\{uploaded_file.filename}")
            global_transcript_files_list = get_transcript_files()
            global_transcript_length_dict['length'] = len(global_transcript_files_list)
            global_prompt_files_list = get_prompt_files()
            global_prompt_length_dict['length'] = len(global_prompt_files_list)
            prompt_upload_file_status = uploaded_file.filename.upper() + ' is uploaded successfully'
        else:
            prompt_upload_file_status = ''
    else:
        prompt_upload_file_status = ''
    return render_template('gpt_text_workshop.html',transcript_length_dict=global_transcript_length_dict,prompt_length_dict=global_prompt_length_dict,transcript_files_list=global_transcript_files_list,prompt_files_list=global_prompt_files_list,prompt_download_file='',download_prompt_file_content='',prompt_upload_file_status=prompt_upload_file_status,output_file_status='')

@app.route('/generate_output_text_file', methods=['GET', 'POST'])
def generate_output_text_file():
    global global_transcript_length_dict,global_transcript_files_list,global_prompt_length_dict,global_prompt_files_list

    if request.method == 'POST':
        transcript_file_name = request.form['selected_source_text_file_value']
        prompt_file_name = request.form['selected_prompt_file_value']
        global_transcript_files_list = get_transcript_files()
        global_transcript_length_dict['length'] = len(global_transcript_files_list)
        global_prompt_files_list = get_prompt_files()
        global_prompt_length_dict['length'] = len(global_prompt_files_list)
        if len(transcript_file_name) > 0 and len(prompt_file_name) > 0:
            transcript_file_name = 'transcripts/' + transcript_file_name
            prompt_file_name = 'prompts/' + prompt_file_name
            output_file_name = generate_gpt3_output(transcript_file_name,prompt_file_name)
            if len(output_file_name)>0:
                output_file_status = output_file_name.upper() + ' is generated successfully'
            else:
                output_file_status = ''
        else:
            output_file_status = ''
    else:
        output_file_status = ''
    return render_template('gpt_text_workshop.html',transcript_length_dict=global_transcript_length_dict,prompt_length_dict=global_prompt_length_dict,transcript_files_list=global_transcript_files_list,prompt_files_list=global_prompt_files_list,prompt_download_file='',download_prompt_file_content='',prompt_upload_file_status='',output_file_status=output_file_status)

@app.route('/output_file_library',methods=['GET', 'POST'])
def output_file_library():
    global global_output_length_dict,global_output_files_list

    if request.method == 'POST':
        global_output_files_list = get_output_files()
        global_output_length_dict['length'] = len(global_output_files_list)
    else:
        global_output_length_dict['length'] = 0
    return render_template('output_file_library.html',length_dict=global_output_length_dict,output_files_list=global_output_files_list,output_download_file='')

@app.route('/output_download_file',methods=['GET', 'POST'])
def output_download_file():
    global global_output_length_dict,global_output_files_list

    if request.method == 'POST':
        download_file_name = request.form['download_file_name']
        global_output_files_list = get_output_files()
        global_output_length_dict['length'] = len(global_output_files_list)
        if len(download_file_name) > 0:

            # Open the file
            with open(f"outputs/{download_file_name}", "r") as file:

                # Read the contents of the file
                contents = file.read()

            output_download_file = download_file_name.upper()
        else:
            output_download_file = ''
            contents = ''
    else:
        global_output_length_dict['length'] = 0
        output_download_file = ''
        contents = ''
    return render_template('output_file_library.html',length_dict=global_output_length_dict,output_files_list=global_output_files_list,output_download_file=output_download_file,download_output_file_content=contents)



if __name__ == '__main__': 
    global_transcript_length_dict = {}
    global_transcript_files_list = []
    global_prompt_length_dict = {}
    global_prompt_files_list = []
    global_output_length_dict = {}
    global_output_files_list = []
    app.run(host='128.199.24.112', port=8080, debug=True)