# SPDX-FileCopyrightText: 2025 asfdrwe <asfdrwe@gmail.com>
# SPDX-License-Identifier: MIT
#
# Model: Wan2.2(GGUF), umt5-xxl(GGUF), wan2.1_vae, wan2.2_i2v_lightx2v_4steps_lora
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
    lora_list  = comfyutils.get_lora(server_address)
    print(lora_list)

    return [
        gr.Dropdown(choices = unet_list, label = 'WanモデルHigh', interactive = True), 
        gr.Dropdown(choices = lora_list, label = 'LoRAモデルHigh', interactive = True), 
        gr.Dropdown(choices = unet_list, label = 'WanモデルLow' , interactive = True), 
        gr.Dropdown(choices = lora_list, label = 'LoRAモデルlow', interactive = True), 
        gr.Dropdown(choices = clip_list, label = 'テキストエンコーダ' , interactive = True), 
        gr.Dropdown(choices = vae_list, label  = 'VAE' , interactive = True)
    ]

def generate(unethigh, checkboxhigh, lorahigh, strhigh, unetlow, checkboxlow, loralow, strlow, clip, vae, image, positive, width, height, length, seed, progress = gr.Progress()):
    if seed == '-1':
        seed = random.randint(0, sys.maxsize)
    else:
        seed = int(seed)
    prompt_file = open('workflow/video01.json', 'r')
    prompt = json.load(prompt_file)

    prompt['116']['inputs']['unet_name'] = unethigh
    prompt['127']['inputs']['lora_name'] = lorahigh
    prompt['127']['inputs']['strength_model'] = strhigh
    if checkboxhigh == False:
        prompt['101']['inputs']['model'] = ['116', 0]
    prompt['117']['inputs']['unet_name'] = unetlow
    prompt['128']['inputs']['lora_name'] = loralow
    prompt['128']['inputs']['strength_model'] = strlow
    if checkboxlow == False:
        prompt['102']['inputs']['model'] = ['117', 0]
    prompt['118']['inputs']['clip_name'] = clip
    prompt['90']['inputs']['vae_name']   = vae

    print(image)
    baseimage_name = comfyutils.upload_data(image, server_address)
    prompt['97']['inputs']['image'] = baseimage_name

    prompt['93']['inputs']['text'] = positive

    prompt['98']['inputs']['width'] = width
    prompt['98']['inputs']['height'] = height
    prompt['98']['inputs']['length'] = length

    prompt['86']['inputs']['seed'] = seed

    print(prompt)

    print('SERVER: ' + server_address)

    video = comfyutils.get_image(prompt, server_address)

    return video

def create(addr):
    global server_address
    server_address = addr
    print('SERVER: ' + server_address)
    with gr.Tab('開始画像と文章から動画生成(Wan2.2)'):
        with gr.Row():
            with gr.Column():
                unet_list = comfyutils.get_unetgguf(server_address)
                print(unet_list)
                lora_list  = comfyutils.get_lora(server_address)
                print(lora_list)
                clip_list = comfyutils.get_clipgguf(server_address)
                print(clip_list)
                vae_list  = comfyutils.get_vae(server_address)
                print(vae_list)

                unethigh = gr.Dropdown(choices = unet_list, label = 'WanモデルHigh', interactive = True)
                with gr.Row():
                    checkboxhigh = gr.Checkbox(label = '有効', value = False)
                    lorahigh = gr.Dropdown(choices = lora_list, label = 'LoRAモデルHigh', interactive = True)
                    strhigh = gr.Slider(label = 'LoRA強度High', value = 1.0, minimum = 0.0, maximum = 2.0, step = 0.01)
                   
                unetlow = gr.Dropdown(choices = unet_list, label = 'WanモデルLow' , interactive = True) 
                with gr.Row():
                    checkboxlow = gr.Checkbox(label = '有効', value = False)
                    loralow = gr.Dropdown(choices = lora_list, label = 'LoRAモデルLow', interactive = True) 
                    strlow = gr.Slider(label = 'LoRA強度Low', value = 1.0, minimum = 0.0, maximum = 2.0, step = 0.01)

                clip = gr.Dropdown(choices = clip_list, label = 'テキストエンコーダ' , interactive = True)
                vae = gr.Dropdown(choices = vae_list, label  = 'VAE' , interactive = True)

            refresh_button = gr.Button('モデル更新')
            refresh_button.click(fn = refresh_models, inputs = [], outputs = [unethigh, lorahigh, unetlow, loralow, clip, vae] )

        with gr.Row():
            with gr.Column():
                baseimage = gr.Image(label = '参照画像', type = 'filepath')
                positive = gr.Textbox(label = 'ポジティブプロンプト')
                width  = gr.Slider(label = '幅', minimum = 0, maximum = 2048, value = 360, step = 8, interactive = True)
                height = gr.Slider(label = '高さ', minimum = 0, maximum = 2048, value = 640, step = 8, interactive = True)
                length = gr.Slider(label = 'フレーム数(FPS=16)', minimum = 1, maximum = 161, value = 81, step = 16, interactive = True)
                seed   = gr.Textbox(label = '乱数シード(-1でランダム)', value = -1)

            with gr.Column():
                generate_button = gr.Button('動画生成')
                video = gr.Video(label = '生成動画', interactive = None, loop = True, autoplay = True)

                generate_button.click(fn = generate, inputs = [
                        unethigh, checkboxhigh, lorahigh, strhigh,
                        unetlow, checkboxlow, loralow, strlow, 
                        clip, vae, 
                        baseimage, 
                        positive,
                        width, height, length, 
                        seed], 
                    outputs = video)

print("MODULE: 20video01")
