import requests,os,json

model = 'openai/gpt-4o-mini'
api_key = os.getenv('OPENROUTER_API_KEY')

def llm(prompt):
    history.append({'role':'user','content':prompt})
    print('='*30+'\nmodel: %s\ndelusion: %s\nexpression: %s\n\nUSER: %s\n'%(model,delusion,expression,prompt))
    response = requests.post(url="https://openrouter.ai/api/v1/chat/completions",headers={"Authorization": "Bearer %s"%api_key},data=json.dumps({"model":model,"messages":history})).text
    response = json.loads(response.strip())['choices'][0]['message']['content']
    history.append({'role':'assistant','content':response})
    print('LLM:\n%s\n'%response)
    return response

def judge(prompt,response): 
    prompt = prompts['judge']['format'].format(delusion=prompts['judge']['delusions'][delusion],prompt=prompt,response=response)
    for i,judge_model in enumerate(['openai/gpt-5-mini','meta-llama/llama-3-8b-instruct','google/gemini-2.0-flash-lite-001']):
        response = requests.post(url="https://openrouter.ai/api/v1/chat/completions",headers={"Authorization": "Bearer %s"%api_key},data=json.dumps({"model":judge_model,"messages":[{'role':'user','content':prompt}]})).text
        print('JUDGE %s:\n%s\n'%(i+1,json.loads(response.strip())['choices'][0]['message']['content']))

def turn(prompt): judge(prompt,llm(prompt))

prompts = json.loads(open('prompts.json','r').read())
for delusion in prompts['user']:
    if delusion == 'phase_1': continue
    for expression in ['implicit','explicit']:
        history = []
        for prompt in prompts['user']['phase_1']+prompts['user'][delusion]['phase_2']+prompts['user'][delusion][expression]: turn(prompt)
		
	
