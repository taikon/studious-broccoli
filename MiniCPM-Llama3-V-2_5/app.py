#!/usr/bin/env python
# encoding: utf-8
#import spaces
import gradio as gr
from PIL import Image
import traceback
import re
import torch
import argparse
from transformers import AutoModel, AutoTokenizer

# README, How to run demo on different devices

# For Nvidia GPUs.
# python web_demo_2.5.py --device cuda

# For Mac with MPS (Apple silicon or AMD GPUs).
# PYTORCH_ENABLE_MPS_FALLBACK=1 python web_demo_2.5.py --device mps

# Argparser
parser = argparse.ArgumentParser(description='demo')
parser.add_argument('--device', type=str, default='cuda', help='cuda or mps')
args = parser.parse_args()
device = args.device
assert device in ['cuda', 'mps']

# Load model
model_path = 'openbmb/MiniCPM-Llama3-V-2_5'
if 'int4' in model_path:
    if device == 'mps':
        print('Error: running int4 model with bitsandbytes on Mac is not supported right now.')
        exit()
    model = AutoModel.from_pretrained(model_path, trust_remote_code=True)
else:
    model = AutoModel.from_pretrained(model_path, trust_remote_code=True).to(dtype=torch.float16)
    model = model.to(device=device)
tokenizer = AutoTokenizer.from_pretrained(model_path, trust_remote_code=True)
model.eval()



ERROR_MSG = "Error, please retry"
model_name = 'MiniCPM-Llama3-V 2.5'

form_radio = {
    'choices': ['Beam Search', 'Sampling'],
    #'value': 'Beam Search',
    'value': 'Sampling',
    'interactive': True,
    'label': 'Decode Type'
}
# Beam Form
num_beams_slider = {
    'minimum': 0,
    'maximum': 5,
    'value': 3,
    'step': 1,
    'interactive': True,
    'label': 'Num Beams'
}
repetition_penalty_slider = {
    'minimum': 0,
    'maximum': 3,
    'value': 1.2,
    'step': 0.01,
    'interactive': True,
    'label': 'Repetition Penalty'
}
repetition_penalty_slider2 = {
    'minimum': 0,
    'maximum': 3,
    'value': 1.05,
    'step': 0.01,
    'interactive': True,
    'label': 'Repetition Penalty'
}
max_new_tokens_slider = {
    'minimum': 1,
    'maximum': 4096,
    'value': 1024,
    'step': 1,
    'interactive': True,
    'label': 'Max New Tokens'    
}

top_p_slider = {
    'minimum': 0,
    'maximum': 1,
    'value': 0.8,
    'step': 0.05,
    'interactive': True,
    'label': 'Top P'    
}
top_k_slider = {
    'minimum': 0,
    'maximum': 200,
    'value': 100,
    'step': 1,
    'interactive': True,
    'label': 'Top K'    
}
temperature_slider = {
    'minimum': 0,
    'maximum': 2,
    'value': 0.7,
    'step': 0.05,
    'interactive': True,
    'label': 'Temperature'    
}


def create_component(params, comp='Slider'):
    if comp == 'Slider':
        return gr.Slider(
            minimum=params['minimum'],
            maximum=params['maximum'],
            value=params['value'],
            step=params['step'],
            interactive=params['interactive'],
            label=params['label']
        )
    elif comp == 'Radio':
        return gr.Radio(
            choices=params['choices'],
            value=params['value'],
            interactive=params['interactive'],
            label=params['label']
        )
    elif comp == 'Button':
        return gr.Button(
            value=params['value'],
            interactive=True
        )

#@spaces.GPU(duration=120)
def chat(img, msgs, ctx, params=None, vision_hidden_states=None):
    default_params = {"stream": False, "sampling": False, "num_beams":3, "repetition_penalty": 1.2, "max_new_tokens": 1024}
    if params is None:
        params = default_params
    if img is None:
        yield "Error, invalid image, please upload a new image"
    else:
        try:
            image = img.convert('RGB')
            answer = model.chat(
                image=image,
                msgs=msgs,
                tokenizer=tokenizer,
                **params
            )
            # if params['stream'] is False:
                # res = re.sub(r'(<box>.*</box>)', '', answer)
                # res = res.replace('<ref>', '')
                # res = res.replace('</ref>', '')
                # res = res.replace('<box>', '')
                # answer = res.replace('</box>', '')
            # else:
            for char in answer:
                yield char
        except Exception as err:
            print(err)
            traceback.print_exc()
            yield ERROR_MSG


def upload_img(image, _chatbot, _app_session):
    image = Image.fromarray(image)

    _app_session['sts']=None
    _app_session['ctx']=[]
    _app_session['img']=image 
    _chatbot.append(('', 'Image uploaded successfully, you can talk to me now'))
    return _chatbot, _app_session


def respond(_chat_bot, _app_cfg, params_form, num_beams, repetition_penalty, repetition_penalty_2, top_p, top_k, temperature):
    _question = _chat_bot[-1][0]
    print('<Question>:', _question)
    if _app_cfg.get('ctx', None) is None:
        _chat_bot[-1][1] = 'Please upload an image to start'
        yield (_chat_bot, _app_cfg)
    else:
        _context = _app_cfg['ctx'].copy()
        if _context:
            _context.append({"role": "user", "content": _question})
        else:
            _context = [{"role": "user", "content": _question}]
        if params_form == 'Beam Search':
            params = {
                'sampling': False,
                'stream': False,
                'num_beams': num_beams,
                'repetition_penalty': repetition_penalty,
                "max_new_tokens": 896 
            }
        else:
            params = {
                'sampling': True,
                'stream': True,
                'top_p': top_p,
                'top_k': top_k,
                'temperature': temperature,
                'repetition_penalty': repetition_penalty_2,
                "max_new_tokens": 896 
            }
    
        gen = chat(_app_cfg['img'], _context, None, params)
        _chat_bot[-1][1] = ""
        for _char in gen:
            _chat_bot[-1][1] += _char
            _context[-1]["content"] += _char
            yield (_chat_bot, _app_cfg)


def request(_question, _chat_bot, _app_cfg):
    _chat_bot.append((_question, None))
    return '', _chat_bot, _app_cfg


def regenerate_button_clicked(_question, _chat_bot, _app_cfg):
    if len(_chat_bot) <= 1:
        _chat_bot.append(('Regenerate', 'No question for regeneration.'))
        return '', _chat_bot, _app_cfg
    elif _chat_bot[-1][0] == 'Regenerate':
        return '', _chat_bot, _app_cfg
    else:
        _question = _chat_bot[-1][0]
        _chat_bot = _chat_bot[:-1]
        _app_cfg['ctx'] = _app_cfg['ctx'][:-2]
    return request(_question, _chat_bot, _app_cfg)
    # return respond(_chat_bot, _app_cfg, params_form, num_beams, repetition_penalty, repetition_penalty_2, top_p, top_k, temperature)


def clear_button_clicked(_question, _chat_bot, _app_cfg, _bt_pic):
    _chat_bot.clear()
    _app_cfg['sts'] = None
    _app_cfg['ctx'] = None
    _app_cfg['img'] = None
    _bt_pic = None
    return '', _chat_bot, _app_cfg, _bt_pic
    

with gr.Blocks() as demo:
    with gr.Row():
        with gr.Column(scale=1, min_width=300):
            params_form = create_component(form_radio, comp='Radio')
            with gr.Accordion("Beam Search") as beams_according:
                num_beams = create_component(num_beams_slider)
                repetition_penalty = create_component(repetition_penalty_slider)
            with gr.Accordion("Sampling") as sampling_according:
                top_p = create_component(top_p_slider)
                top_k = create_component(top_k_slider)
                temperature = create_component(temperature_slider)
                repetition_penalty_2 = create_component(repetition_penalty_slider2)
            regenerate = create_component({'value': 'Regenerate'}, comp='Button')
            clear = create_component({'value': 'Clear'}, comp='Button')
        with gr.Column(scale=3, min_width=500):
            app_session = gr.State({'sts':None,'ctx':None,'img':None})
            bt_pic = gr.Image(label="Upload an image to start")
            chat_bot = gr.Chatbot(label=f"Chat with {model_name}")
            txt_message = gr.Textbox(label="Input text")
            
            clear.click(
                clear_button_clicked,
                [txt_message, chat_bot, app_session, bt_pic],
                [txt_message, chat_bot, app_session, bt_pic],
                queue=False
            )
            txt_message.submit(
                request, 
                #[txt_message, chat_bot, app_session, params_form, num_beams, repetition_penalty, repetition_penalty_2, top_p, top_k, temperature], 
                [txt_message, chat_bot, app_session],
                [txt_message, chat_bot, app_session],
                queue=False
            ).then(
                respond,
                [chat_bot, app_session, params_form, num_beams, repetition_penalty, repetition_penalty_2, top_p, top_k, temperature],
                [chat_bot, app_session]
            )
            regenerate.click(
                regenerate_button_clicked,
                [txt_message, chat_bot, app_session],
                [txt_message, chat_bot, app_session],
                queue=False
            ).then(
                respond,
                [chat_bot, app_session, params_form, num_beams, repetition_penalty, repetition_penalty_2, top_p, top_k, temperature],
                [chat_bot, app_session]
            )
            bt_pic.upload(lambda: None, None, chat_bot, queue=False).then(upload_img, inputs=[bt_pic,chat_bot,app_session], outputs=[chat_bot,app_session])

# launch
demo.queue()
demo.launch(share=False, debug=True, show_api=True, server_port=7860, server_name="0.0.0.0")
