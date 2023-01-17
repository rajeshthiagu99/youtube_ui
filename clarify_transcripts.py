import openai 
import time as t
import os
import textwrap

api_key = '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'
openai.api_key = api_key

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

if __name__ == '__main__':
    files = os.listdir('transcript')
    for file in files:
        if os.path.exists('clarified_transcripts/'+file):
            print('Skipping '+file)
            continue
        print('Processing '+file)

        # open transcript
        with open('transcript/'+file,'r') as f:
            transcript = f.read()

    
        chunks = textwrap.wrap(transcript, 6000)
        output = []
        for chunk in chunks:
            # open transcript
            with open('prompt_clarify_transcript.txt','r') as f:
                prompt = f.read().replace('<<TRANSCRIPT>>',chunk)
            essay = get_generated_text(prompt)
            output.append(essay)
        result = '\n\n'.join(output)
        # save result in new file in clarified_transcripts
        with open('clarified_transcript/'+file,'w') as f:
            f.write(result)
        print('\n\n***************************\n\n',result)