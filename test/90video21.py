# SPDX-FileCopyrightText: 2025 asfdrwe <asfdrwe@gmail.com>
# SPDX-License-Identifier: MIT
#
# Model: Wan2.2 S2V(GGUF), umt5-xxl(GGUF), wan2.1_vae, wan2.2_t2v_lightx2v_4steps_lora, wav2vec2_large_english_fp16.safetensors
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
    audioencoder_list  = comfyutils.get_audioencoder(server_address)
    print(audioencoder_list)

    return [
        gr.Dropdown(choices = unet_list, label = 'Wan S2Vモデル', interactive = True),
        gr.Dropdown(choices = clip_list, label = 'テキストエンコーダ' , interactive = True), 
        gr.Dropdown(choices = audioencoder_list, label = 'オーディオエンコーダ', interactive = True),
        gr.Dropdown(choices = vae_list, label  = 'VAE' , interactive = True)
    ]

def generate(unethigh, clip, audioencoder, vae, image, audio, positive, width, batch_count, height, batch_size,  seed, progress = gr.Progress()):
    prompt_file = open('workflow/video21.json', 'r')
    prompt = json.load(prompt_file)

    prompt['182']['inputs']['unet_name'] = unethigh
    prompt['183']['inputs']['clip_name'] = clip
    prompt['57']['inputs']['audio_encoder_name'] = audioencoder
    prompt['39']['inputs']['vae_name']   = vae

    print(image)
    baseimage_name = comfyutils.upload_data(image, server_address)
    prompt['52']['inputs']['image'] = baseimage_name
    print(audio)
    baseaudio_name = comfyutils.upload_data(audio, server_address)
    prompt['58']['inputs']['audio'] = baseaudio_name

    prompt['6']['inputs']['text'] = positive

    prompt['93']['inputs']['width'] = width
    prompt['93']['inputs']['height'] = height

    print('SERVER: ' + server_address)

    videos_output = []

    for i in range(int(batch_count)):
        if seed == '-1':
            newseed = random.randint(0, sys.maxsize)
        else:
            newseed = int(seed)
        prompt['3']['inputs']['seed'] = newseed
        print(prompt)
        videos_output.extend(comfyutils.get_images(prompt, server_address))

    return videos_output

def create(addr):
    global server_address
    server_address = addr
    print('SERVER: ' + server_address)

    with gr.Tab('開始画像と音声と文章から動画生成(Wan2.2)(5秒弱)'):
        with gr.Row():
            with gr.Column():
                unet_list = comfyutils.get_unetgguf(server_address)
                print(unet_list)
                lora_list  = comfyutils.get_lora(server_address)
                print(lora_list)
                clip_list = comfyutils.get_clipgguf(server_address)
                print(clip_list)
                audioencoder_list  = comfyutils.get_audioencoder(server_address)
                print(audioencoder_list)
                vae_list  = comfyutils.get_vae(server_address)
                print(vae_list)

                unethigh = gr.Dropdown(choices = unet_list, label = 'Wan S2Vモデル', interactive = True)
                clip = gr.Dropdown(choices = clip_list, label = 'テキストエンコーダ' , interactive = True)
                audioencoder =  gr.Dropdown(choices = audioencoder_list, label = 'オーディオエンコーダ', interactive = True)
                vae = gr.Dropdown(choices = vae_list, label  = 'VAE' , interactive = True)

            refresh_button = gr.Button('モデル更新')
            refresh_button.click(fn = refresh_models, inputs = [], outputs = [unethigh, clip, audioencoder, vae] )

        with gr.Row():
            with gr.Column():
                baseimage = gr.Image(label = '参照画像', type = 'filepath')
                baseaudio = gr.Audio(label = '参照音声', type = 'filepath')
                positive = gr.Textbox(label = 'ポジティブプロンプト')
                with gr.Row():
                    width  = gr.Slider(label = '幅', minimum = 0, maximum = 2048, value = 640, step = 8, interactive = True)
                    batch_count = gr.Slider(label = 'バッチカウント', value = 1, minimum = 1, step = 1)
                with gr.Row():
                    height = gr.Slider(label = '高さ', minimum = 0, maximum = 2048, value = 640, step = 8, interactive = True)
                    batch_size = gr.Slider(label = 'バッチサイズ', value = 1, minimum = 1, step = 1)
                seed   = gr.Textbox(label = '乱数シード(-1でランダム)', value = -1)

            with gr.Column():
                generate_button = gr.Button('動画生成')
                videos = gr.Gallery(label = '生成画像', interactive = None, object_fit = 'scale-down')

                generate_button.click(fn = generate, inputs = [
                        unethigh,
                        clip, audioencoder, vae,
                        baseimage,
                        baseaudio,
                        positive,
                        width, batch_count, height, batch_size,
                        seed], 
                    outputs = videos)

print("MODULE: 20video21")
