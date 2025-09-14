# SPDX-FileCopyrightText: 2025 asfdrwe <asfdrwe@gmail.com>
# SPDX-License-Identifier: MIT
#
# Model: FLUX Kontext
# Custom Node: ComfyUI-GGUF

import gradio as gr

import json
import random
import sys

import comfyutils

server_address = 'localhost:8188'

def refresh_models():
    unet_list = comfyutils.get_unetgguf(server_address)
    print(unet_list)
    clip_list = comfyutils.get_clipgguf(server_address)
    print(clip_list)
    vae_list  = comfyutils.get_vae(server_address)
    print(vae_list)

    return [
        gr.Dropdown(choices = unet_list, label = 'Fluxモデル', interactive = True),
        gr.Dropdown(choices = clip_list, label = 'テキストエンコーダ1' , interactive = True),
        gr.Dropdown(choices = clip_list, label = 'テキストエンコーダ2' , interactive = True),
        gr.Dropdown(choices = vae_list, label  = 'VAE' , interactive = True)
    ]

def generate(unet, clip1, clip2, vae, image1, image2, direction, positive, batch_count, steps, cfg, seed, sampler, scheduler, denoise, progress = gr.Progress()):
    print(image1)
    baseimage_name1 = comfyutils.upload_data(image1, server_address)
    print(image2)
    baseimage_name2 = comfyutils.upload_data(image2, server_address)

    prompt_file = open('workflow/image22.json', 'r')
    prompt = json.load(prompt_file)

    prompt['1']['inputs']['unet_name'] = unet
    prompt['2']['inputs']['clip_name1'] = clip1
    prompt['2']['inputs']['clip_name2'] = clip2
    prompt['3']['inputs']['vae_name']   = vae

    prompt['11']['inputs']['image'] = baseimage_name1
    prompt['14']['inputs']['image'] = baseimage_name2
    prompt['15']['inputs']['direction'] = direction

    prompt['6']['inputs']['text'] = positive

    prompt['5']['inputs']['steps'] = steps
    prompt['5']['inputs']['cfg'] = cfg
    prompt['5']['inputs']['sampler_name'] = sampler
    prompt['5']['inputs']['scheduler'] = scheduler
    prompt['5']['inputs']['denoise'] = float(denoise)

    print('SERVER: ' + server_address)

    images_output = []

    for i in range(int(batch_count)):
        if seed == '-1':
            newseed = random.randint(0, sys.maxsize)
        else:
            newseed = int(seed)
        prompt['5']['inputs']['seed'] = newseed
        print(prompt)
        images_output.extend(comfyutils.get_images(prompt, server_address))

    return images_output

def create(addr):
    global server_address
    server_address = addr
    print('SERVER: ' + server_address)
    with gr.Tab('画像2枚から画像生成(FLUX)'):
        with gr.Row():
            with gr.Column():
                [unet, clip1, clip2, vae] = refresh_models()
            refresh_button = gr.Button('モデル更新')
            refresh_button.click(fn = refresh_models, inputs = [], outputs = [unet, clip1, clip2, vae])
        with gr.Row():
            with gr.Column():
                baseimage1 = gr.Image(label = '入力画像1', type = 'filepath')
                baseimage2 = gr.Image(label = '入力画像2', type = 'filepath')
                direction = gr.Dropdown(choices = ['right', 'down', 'left', 'up'])
                positive = gr.Textbox(label = 'ポジティブプロンプト')
                batch_count = gr.Slider(label = 'バッチカウント', value = 1, minimum = 1, step = 1)
                steps  = gr.Slider(label = 'ステップ数', minimum = 1, maximum = 50, value = 20, step = 1, interactive = True)
                cfg    = gr.Slider(label = 'CFG', minimum = 1, maximum = 20, value = 1.0, step = 0.1, interactive = True)
                denoise = gr.Slider(label = 'ノイズ除去', value = 1.00, minimum = 0.0, step = 0.01, maximum = 1.0, interactive = True)
                seed   = gr.Textbox(label = '乱数シード(-1でランダム)', value = -1)
                sampler_list = comfyutils.get_sampler(server_address)
                sampler = gr.Dropdown(choices = sampler_list, label = 'サンプラー', interactive = True, value = 'euler')
                scheduler_list = comfyutils.get_scheduler(server_address)
                scheduler = gr.Dropdown(choices = scheduler_list, label = 'スケジューラー', interactive = True, value = 'normal')

            with gr.Column():
                generate_button = gr.Button('画像生成')
                images = gr.Gallery(label = '生成画像', interactive = None, object_fit = 'scale-down')

                generate_button.click(fn = generate,
                                      inputs = [unet, clip1, clip2, vae,
                                                baseimage1, baseimage2, direction,
                                                positive,
                                                batch_count,
                                                steps, cfg, seed, sampler, scheduler, denoise],
                                      outputs = images)

print("MODULE: 10image22")
