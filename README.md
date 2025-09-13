# ComfyUIGradio2

ComfyUIGradio2 は AI を用いて画像や動画の生成等を行う [ComfyUI](https://www.comfy.org/) を
利用して、 [Gradio](https://www.gradio.app/)による独自のユーザーフェイスを用いて、
画像生成や動画生成を行うツールです。

# [使い方等の解説はここをクリック](https://asfdrwe.github.io/ComfyUIGradio2/)

## 動作確認環境

|       OS         |             ハードウェア                            |             備考           |
|------------------|---------------------------------------------------|----------------------------|
| Windows 11 24H2  | Ryzen 5600 + DDR4 3200 16GB×2 + Geforce 3060      |                            |
| Fedora 42 (Linux)| Ryzen 5600G + DDR 3200 16GB×2 + Radeon RX 7800 XT | ComfyUI の起動オプションに工夫が必要。動画生成は動かない |

## インストール

[ComfyUI](https://www.comfy.org/download) をインストールしてください。

カスタムノードは、[ComfyUI-GGUF](https://github.com/city96/ComfyUI-GGUF)と
[ComfyUI-DepthAnythingV2](https://github.com/kijai/ComfyUI-DepthAnythingV2)
をインストールしてください。

ComfyUIGradio2本体は、`git`でインストールしてください。

```
git clone https://github.com/asfdrwe/ComfyUIGradio2
cd ComfyUIGradio2
python3.13 -m venv venv
. venv/bin/activate
pip install -r requirements.txt
```

## モデルのダウンロード
画像生成は3種類あり、一つはSD1.5 及びに SDXL のチェックポイントモデルと
その LoRA を使用できます。一つは FLUX Kontext 専用です。
もう一つは Qwen Image Edit 専用です。

動画生成は Wan 2.2 I2v Light と Wan 2.2 S2V です。

SDXL モデルは chekcpoints 以下、LoRA(DMD2やWan2.2 Lightning LoRA) は loras 以下、
FLUX-Kontext や Qwen Image Edit や Wan2.2 の GGUF は diffusion_models または
unet 以下、t5-xxl と umt5-xxl-encoder と Qwen2.5-VL-7B-Instruct の GGUF は 
clip または text_encoders 以下、FLUX-VAE と wan_2.1_vae と Qwen_Image-VAE は
vae 以下に移動させてください。

### SDXL モデルと LoRA の例

- [WAI-NSFW-illustrious-SDXL-v14.0](https://civitai.com/models/827184/wai-nsfw-illustrious-sdxl)
- [DMD2](https://huggingface.co/tianweiy/DMD2)

### FLUX Kontext dev GGUF

- [FLUX-Kontext-dev GGUF](https://huggingface.co/QuantStack/FLUX.1-Kontext-dev-GGUF)
- [t5-xxl GGUF](https://huggingface.co/city96/t5-v1_1-xxl-encoder-gguf)
- [clip_l](https://huggingface.co/comfyanonymous/flux_text_encoders/)
- [FLUX-VAE](https://huggingface.co/Comfy-Org/Lumina_Image_2.0_Repackaged)

### Wan 2.2 I2V
- [Wan2.2_I2V-A14B-GGUF](https://huggingface.co/bullerwins/Wan2.2-I2V-A14B-GGUF)
- [umt5-xxl-encoder-gguf](https://huggingface.co/city96/umt5-xxl-encoder-gguf)
- [wan_2.1_vae](https://huggingface.co/Comfy-Org/Wan_2.1_ComfyUI_repackaged))
- [Wan2.2 Lightx2v LoRA](https://huggingface.co/Comfy-Org/Wan_2.2_ComfyUI_Repackaged/tree/main/split_files/loras)

### Wan 2.2 S2V
- [Wan2.2-S2V-14B-GGUF)](https://huggingface.co/QuantStack/Wan2.2-S2V-14B-GGUF)
- [Wan2.2 Lightx2v LoRA](https://huggingface.co/Comfy-Org/Wan_2.2_ComfyUI_Repackaged/tree/main/split_files/loras)
- [wav2vec2_large_english](https://huggingface.co/Comfy-Org/Wan_2.2_ComfyUI_Repackaged/tree/main/split_files/audio_encoders)

### Qwen Image Edit
- [Qwen-Image-Edit-GGUF と Qwen_Image-VAE](https://huggingface.co/QuantStack/Qwen-Image-Edit-GGUF)
- [Qwen-Image-Edit-Lightning](https://huggingface.co/lightx2v/Qwen-Image-Lightning)
- [Qwen2.5-VL-7B-Instruct と Qwen2.5-VL-7B-Instruct-mmproj](https://huggingface.co/unsloth/Qwen2.5-VL-7B-Instruct-GGUF)

## 実行
ComfyUI を先に起動してから、ComfyUIGradio2 を 起動してください。
```
python app.py
```

### 起動オプション
ComfyUI を別のマシンで動かしている場合、次のオプションで接続できます。

- --server_addr ComfyUIのアドレス
- --server_port ComfyUIのポート番号

```
python app.py --server_addr ComfyUIのアドレス --server_port ComfyUIのポート番号
```

## 拡張とカスタマイズ
`uimodule`フォルダ以下に、`10image01.py` などと同様の形式で拡張モジュール.pyファイルを
用意すれば自動的に読み込まれます。

危険なモジュールも実行可能なので、セキュリティには気を付けてください。不用意に
`uimodule`フォルダ以下に*.pyファイルを置かないようにしてください。

拡張モジュールの開発については、[こちら]()を参照してください。

## ライセンス

ComfyUIGradio2 は MIT LICENSE に従います。

Copyright (c) 2025 asfdrwe

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the “Software”), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

## 更新履歴
- 2025/9/10
  - Qwen Image Edit 用の uimodule & workflow を追加
  - 配布パッケージを更新
- 2025/9/02
  - Wan 2.2 S2V 用の uimodule & workflow を追加
- 2025/8/31
  - 公開
