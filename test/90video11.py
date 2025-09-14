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

def generate(unethigh,
             checkboxhigh, lorahigh, strhigh, unetlow,
             checkboxlow, loralow, strlow, clip, vae,
             image1, image2,
             positive,
             width, batch_count, height, batch_size, length, seed, progress = gr.Progress()):

    prompt_file = open('workflow/video11.json', 'r')
    prompt = json.load(prompt_file)

    prompt['98']['inputs']['unet_name'] = unethigh
    prompt['100']['inputs']['lora_name'] = lorahigh
    prompt['100']['inputs']['strength_model'] = strhigh
    if checkboxhigh == False:
        prompt['91']['inputs']['model'] = ['98', 0]
    prompt['99']['inputs']['unet_name'] = unetlow
    prompt['101']['inputs']['lora_name'] = loralow
    prompt['101']['inputs']['strength_model'] = strlow
    if checkboxlow == False:
        prompt['92']['inputs']['model'] = ['99', 0]
    prompt['97']['inputs']['clip_name'] = clip
    prompt['39']['inputs']['vae_name']   = vae

    print(image1)
    baseimage_name1 = comfyutils.upload_data(image1, server_address)
    prompt['68']['inputs']['image'] = baseimage_name1
    print(image2)
    baseimage_name2 = comfyutils.upload_data(image2, server_address)
    prompt['62']['inputs']['image'] = baseimage_name2

    prompt['6']['inputs']['text'] = positive

    prompt['67']['inputs']['width'] = width
    prompt['67']['inputs']['height'] = height
    prompt['67']['inputs']['length'] = length
    prompt['67']['inputs']['batch_size'] = batch_size

    print('SERVER: ' + server_address)

    videos_output = []

    for i in range(int(batch_count)):
        if seed == '-1':
            newseed = random.randint(0, sys.maxsize)
        else:
            newseed = int(seed)
        prompt['57']['inputs']['noise_seed'] = newseed
        print(prompt)
        videos_output.extend(comfyutils.get_images(prompt, server_address))

    return videos_output

def create(addr):
    global server_address
    server_address = addr
    print('SERVER: ' + server_address)

    with gr.Tab('開始画像と終了画像と文章から動画生成(Wan2.2)'):
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
                baseimage1= gr.Image(label = '開始画像', type = 'filepath')
                baseimage2 = gr.Image(label = '終了画像', type = 'filepath')
                positive = gr.Textbox(label = 'ポジティブプロンプト')
                with gr.Row():
                    width  = gr.Slider(label = '幅', minimum = 0, maximum = 2048, value = 360, step = 8, interactive = True)
                    batch_count = gr.Slider(label = 'バッチカウント', value = 1, minimum = 1, step = 1)
                with gr.Row():
                    height = gr.Slider(label = '高さ', minimum = 0, maximum = 2048, value = 640, step = 8, interactive = True)
                    batch_size = gr.Slider(label = 'バッチサイズ', value = 1, minimum = 1, step = 1)
                length = gr.Slider(label = 'フレーム数(FPS=16)', minimum = 1, maximum = 161, value = 81, step = 16, interactive = True)
                seed   = gr.Textbox(label = '乱数シード(-1でランダム)', value = -1)

            with gr.Column():
                generate_button = gr.Button('動画生成')
                videos = gr.Gallery(label = '生成画像', interactive = None, object_fit = 'scale-down')

                generate_button.click(fn = generate, inputs = [
                        unethigh, checkboxhigh, lorahigh, strhigh,
                        unetlow, checkboxlow, loralow, strlow, 
                        clip, vae, 
                        baseimage1, baseimage2,
                        positive,
                        width, batch_count, height, batch_size, length,
                        seed], 
                    outputs = videos)

print("MODULE: 20video02")
