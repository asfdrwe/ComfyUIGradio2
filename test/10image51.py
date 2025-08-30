# SPDX-FileCopyrightText: 2025 asfdrwe <asfdrwe@gmail.com>
# SPDX-License-Identifier: MIT

import gradio as gr

import json
import random
import sys

import comfyutils

server_address = 'localhost:8188'

def refresh_checkpoint():
    checkpoint_list = comfyutils.get_checkpoint(server_address)
    print(checkpoint_list)
    return gr.Dropdown(choices = checkpoint_list, label = 'チェックポイント', interactive = True)

def generate(checkpoint, positive, negative, width, height, steps, cfg, seed, sampler, scheduler, denoise, progress = gr.Progress()):
    if seed == '-1':
        seed = random.randint(0, sys.maxsize)
    else:
        seed = int(seed)
    prompt_file = open('workflow/image51.json', 'r')
    prompt = json.load(prompt_file)

    prompt['4']['inputs']['ckpt_name'] = checkpoint

    prompt['6']['inputs']['text'] = positive
    prompt['7']['inputs']['text'] = negative

    prompt['5']['inputs']['width'] = width
    prompt['5']['inputs']['height'] = height

    prompt['3']['inputs']['steps'] = steps
    prompt['3']['inputs']['cfg'] = cfg
    prompt['3']['inputs']['seed'] = seed
    prompt['3']['inputs']['sampler_name'] = sampler
    prompt['3']['inputs']['scheduler'] = scheduler
    prompt['3']['inputs']['denoise'] = float(denoise)

    print(prompt)

    print('SERVER: ' + server_address)

    progress_data = {'4': 0.2, '5': 0.3, '6': 0.4, '7': 0.5, '3': 0.6, '8': 0.9}

    image = comfyutils.get_image_with_progress(prompt, server_address, progress, progress_data)

    return [image]

def create(addr):
    global server_address
    server_address = addr
    print('SERVER: ' + server_address)
    with gr.Tab('文章から画像を生成01'):
        with gr.Row():
            checkpoint = refresh_checkpoint()
            refresh_button = gr.Button('チェックポイント更新')
            refresh_button.click(fn = refresh_checkpoint, inputs = [], outputs = checkpoint)
        with gr.Row():
            with gr.Column():
                positive = gr.Textbox(label = 'ポジティブプロンプト')
                negative = gr.Textbox(label = 'ネガティブプロンプト')
                width  = gr.Slider(label = '幅', minimum = 0, maximum = 2048, value = 1024, step = 8, interactive = True)
                height = gr.Slider(label = '高さ', minimum = 0, maximum = 2048, value = 1024, step = 8, interactive = True)
                steps  = gr.Slider(label = 'ステップ数', minimum = 1, maximum = 50, value = 20, step = 1, interactive = True)
                cfg    = gr.Slider(label = 'CFG', minimum = 1, maximum = 20, value = 7, step = 1, interactive = True)
                denoise = gr.Slider(label = 'ノイズ除去', value = 1.0, minimum = 0.0, step = 0.01, maximum = 1.0, interactive = True)
                seed   = gr.Textbox(label = '乱数シード(-1でランダム)', value = -1)
                sampler_list = comfyutils.get_sampler(server_address)
                sampler = gr.Dropdown(choices = sampler_list, label = 'サンプラー', interactive = True, value = 'euler')
                scheduler_list = comfyutils.get_scheduler(server_address)
                scheduler = gr.Dropdown(choices = scheduler_list, label = 'スケジューラー', interactive = True, value = 'normal')

            with gr.Column():
                generate_button = gr.Button('画像生成')
                gallery = gr.Gallery(label = '生成画像', interactive = None, type = 'filepath', object_fit = 'scale-down')

                generate_button.click(fn = generate, inputs = [checkpoint, positive, negative, width, height, steps, cfg, seed, sampler, scheduler, denoise], outputs = gallery)

print("MODULE: 10image51")
