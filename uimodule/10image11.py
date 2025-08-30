# SPDX-FileCopyrightText: 2025 asfdrwe <asfdrwe@gmail.com>
# SPDX-License-Identifier: MIT
#
# Model: SD1.5, SDXL
# Custom Node: none

import gradio as gr

import json
import random
import sys

import comfyutils

server_address = 'localhost:8188'

def refresh_models():
    checkpoint_list = comfyutils.get_checkpoint(server_address)
    print(checkpoint_list)

    lora_list = comfyutils.get_lora(server_address)
    print(lora_list)

    return [gr.Dropdown(choices = checkpoint_list, label = 'チェックポイント', interactive = True),
            gr.Dropdown(choices = lora_list, label = 'LoRA1', interactive = True),
            gr.Dropdown(choices = lora_list, label = 'LoRA2', interactive = True)]

def generate(checkpoint, checkbox1, lora1, mstr1, cstr1, checkbox2, lora2, mstr2, cstr2, image, positive, negative, steps, cfg, seed, sampler, scheduler, denoise, progress = gr.Progress()):
    if seed == '-1':
        seed = random.randint(0, sys.maxsize)
    else:
        seed = int(seed)

    print(image)
    baseimage_name = comfyutils.upload_data(image, server_address)

    prompt_file = open('workflow/image11.json', 'r')
    prompt = json.load(prompt_file)

    prompt['4']['inputs']['ckpt_name'] = checkpoint

    prompt['20']['inputs']['lora_name'] = lora1
    prompt['20']['inputs']['strength_model'] = mstr1
    prompt['20']['inputs']['strength_clip'] = cstr1

    prompt['21']['inputs']['lora_name'] = lora2
    prompt['21']['inputs']['strength_model'] = mstr2
    prompt['21']['inputs']['strength_clip'] = cstr2

    if checkbox1 == True:
        if checkbox2 == True:
            pass
        else:
            prompt['3']['inputs']['model'] = ['20', 0]
            prompt['6']['inputs']['clip'] = ['20', 1]
            prompt['7']['inputs']['clip'] = ['20', 1]
    else:
        if checkbox2 == True:
            prompt['21']['inputs']['model'] = ['4', 0]
            prompt['21']['inputs']['clip'] = ['4', 1]
        else:
            prompt['3']['inputs']['model'] = ['4', 0]
            prompt['6']['inputs']['clip'] = ['4', 1]
            prompt['7']['inputs']['clip'] = ['4', 1]


    prompt['16']['inputs']['image'] = baseimage_name

    prompt['6']['inputs']['text'] = positive
    prompt['7']['inputs']['text'] = negative

    prompt['3']['inputs']['steps'] = steps
    prompt['3']['inputs']['cfg'] = cfg
    prompt['3']['inputs']['seed'] = seed
    prompt['3']['inputs']['sampler_name'] = sampler
    prompt['3']['inputs']['scheduler'] = scheduler
    prompt['3']['inputs']['denoise'] = float(denoise)

    print(prompt)

    print('SERVER: ' + server_address)

    image = comfyutils.get_image(prompt, server_address)

    return image

def create(addr):
    global server_address
    server_address = addr
    print('SERVER: ' + server_address)
    with gr.Tab('画像と文章から画像生成'):
        with gr.Row():
            with gr.Column():
                checkpoint_list = comfyutils.get_checkpoint(server_address)
                checkpoint = gr.Dropdown(choices = checkpoint_list, label = 'チェックポイント', interactive = True)
                lora_list = comfyutils.get_lora(server_address)
                with gr.Row():
                    checkbox1 = gr.Checkbox(label = '有効', value = False)
                    lora1 = gr.Dropdown(choices = lora_list, label = 'LoRA1', interactive = True)
                    mstr1 = gr.Slider(label = 'モデル強度', value = 1.0, minimum = 0.0, maximum = 2.0, step = 0.01)
                    cstr1 = gr.Slider(label = 'クリップ強度', value = 1.0, minimum = 0.0, maximum = 2.0, step = 0.01)
                with gr.Row():
                    checkbox2 = gr.Checkbox(label = '有効', value = False)
                    lora2 = gr.Dropdown(choices = lora_list, label = 'LoRA2', interactive = True)
                    mstr2 = gr.Slider(label = 'モデル強度', value = 1.0, minimum = 0.0, maximum = 2.0, step = 0.01)
                    cstr2 = gr.Slider(label = 'クリップ強度', value = 1.0, minimum = 0.0, maximum = 2.0, step = 0.01)

            refresh_button = gr.Button('モデル更新')
            refresh_button.click(fn = refresh_models, inputs = [], outputs = [checkpoint, lora1, lora2])
        with gr.Row():
            with gr.Column():
                baseimage = gr.Image(label = '入力画像', type = 'filepath')
                positive = gr.Textbox(label = 'ポジティブプロンプト')
                negative = gr.Textbox(label = 'ネガティブプロンプト')
                steps  = gr.Slider(label = 'ステップ数', minimum = 1, maximum = 50, value = 20, step = 1, interactive = True)
                cfg    = gr.Slider(label = 'CFG', minimum = 1, maximum = 20, value = 7, step = 1, interactive = True)
                denoise = gr.Slider(label = 'ノイズ除去', value = 0.75, minimum = 0.0, step = 0.01, maximum = 1.0, interactive = True)
                seed   = gr.Textbox(label = '乱数シード(-1でランダム)', value = -1)
                sampler_list = comfyutils.get_sampler(server_address)
                sampler = gr.Dropdown(choices = sampler_list, label = 'サンプラー', interactive = True, value = 'euler')
                scheduler_list = comfyutils.get_scheduler(server_address)
                scheduler = gr.Dropdown(choices = scheduler_list, label = 'スケジューラー', interactive = True, value = 'normal')

            with gr.Column():
                generate_button = gr.Button('画像生成')
                image = gr.Image(label = '生成画像', interactive = None, type = 'filepath')

                generate_button.click(fn = generate,
                                      inputs = [checkpoint,
                                                checkbox1, lora1, mstr1, cstr1,
                                                checkbox2, lora2, mstr2, cstr2,
                                                baseimage,
                                                positive, negative,
                                                steps, cfg, seed, sampler, scheduler, denoise],
                                      outputs = image)

print("MODULE: 10image11")
