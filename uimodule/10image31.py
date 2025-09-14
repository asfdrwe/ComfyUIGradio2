# SPDX-FileCopyrightText: 2025 asfdrwe <asfdrwe@gmail.com>
# SPDX-License-Identifier: MIT
#
# Model: Qwen-Image-Edit(GGUF), Qwen2.5-VL-7B-Instruct(GGUF)、
# Qwen2.5-VL-7B-Instruct-mmproj、Qwen_Image-VAE、
# Qwen-Image-Edit-Lightning
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
        gr.Dropdown(choices = unet_list, label = 'Qwen Image Edit モデル', interactive = True), 
        gr.Dropdown(choices = lora_list, label = 'LoRAモデル', interactive = True), 
        gr.Dropdown(choices = clip_list, label = 'テキストエンコーダ' , interactive = True), 
        gr.Dropdown(choices = vae_list, label  = 'VAE' , interactive = True)
    ]

def generate(unet, checkbox, lora, strength, clip, vae, image, positive, batch_count, pixels, seed, progress = gr.Progress()):
    prompt_file = open('workflow/image31.json', 'r')
    prompt = json.load(prompt_file)

    prompt['101']['inputs']['unet_name'] = unet
    prompt['104']['inputs']['lora_name'] = lora
    prompt['104']['inputs']['strength_model'] = strength
    if checkbox == False:
        prompt['89']['inputs']['model'] = ['101', 0]
    prompt['102']['inputs']['clip_name'] = clip
    prompt['39']['inputs']['vae_name']   = vae

    print(image)
    baseimage_name = comfyutils.upload_data(image, server_address)
    prompt['78']['inputs']['image'] = baseimage_name
    prompt['76']['inputs']['prompt'] = positive
    prompt['93']['inputs']['megapixels'] = pixels
    prompt['3']['inputs']['seed'] = seed

    print('SERVER: ' + server_address)

    images_output = []

    for i in range(int(batch_count)):
        if seed == '-1':
            newseed = random.randint(0, sys.maxsize)
        else:
            newseed = int(seed)
        prompt['3']['inputs']['seed'] = newseed
        print(prompt)
        images_output.extend(comfyutils.get_images(prompt, server_address))

    return images_output

def create(addr):
    global server_address
    server_address = addr
    print('SERVER: ' + server_address)
    with gr.Tab('画像を文章に基づき編集(Qwen-Image-Edit)'):
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

                unet = gr.Dropdown(choices = unet_list, label = 'Qwen Image Edit モデル', interactive = True)
                with gr.Row():
                    checkbox = gr.Checkbox(label = '有効', value = False)
                    lora = gr.Dropdown(choices = lora_list, label = 'LoRAモデル', interactive = True)
                    strength = gr.Slider(label = 'LoRA強度', value = 1.0, minimum = 0.0, maximum = 2.0, step = 0.01)
                   
                clip = gr.Dropdown(choices = clip_list, label = 'テキストエンコーダ' , interactive = True)
                vae = gr.Dropdown(choices = vae_list, label  = 'VAE' , interactive = True)

            refresh_button = gr.Button('モデル更新')
            refresh_button.click(fn = refresh_models, inputs = [], outputs = [unet, lora, clip, vae] )

        with gr.Row():
            with gr.Column():
                baseimage = gr.Image(label = '参照画像', type = 'filepath')
                positive = gr.Textbox(label = 'ポジティブプロンプト')
                batch_count = gr.Slider(label = 'バッチカウント', value = 1, minimum = 1, step = 1)
                megapixels = gr.Slider(label = '総画素数(100万画素単位)', minimum = 0.0, maximum = 10.0, value = 1.0, step = 0.01, interactive = True)
                seed   = gr.Textbox(label = '乱数シード(-1でランダム)', value = -1)

            with gr.Column():
                generate_button = gr.Button('編集')
                images = gr.Gallery(label = '生成画像', interactive = None, object_fit = 'scale-down')

                generate_button.click(fn = generate, inputs = [
                        unet, 
                        checkbox, lora, strength,
                        clip, vae, 
                        baseimage, 
                        positive,
                        batch_count,
                        megapixels, 
                        seed], 
                    outputs = images)

print("MODULE: 10video31")
