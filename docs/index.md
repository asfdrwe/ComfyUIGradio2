# ComfyUIGradio2

ComfyUIGradio2 は AI を用いて画像や動画の生成等を行う [ComfyUI](https://www.comfy.org/) を
利用して、 [Gradio](https://www.gradio.app/)による独自のユーザーフェイスを用いて、
画像生成や動画生成を行うツールです。

## 動作確認環境

|       OS         |             ハードウェア                            |             備考           |
|------------------|---------------------------------------------------|----------------------------|
| Windows 11 24H2  | Ryzen 5600 + DDR4 3200 16GB×2 + Geforce 3060      |                            |
| Fedora 42 (Linux)| Ryzen 5600G + DDR 3200 16GB×2 + Radeon RX 7800 XT | ComfyUI の起動オプションに工夫が必要。動画生成は動かない |

画像生成は NVIDIA の VRAM 8GB 以上の以上のグラフィックボードとメインメモリ 16GB あれば
可能だと思います。動画生成は NVIDIA の VRAM 12GB 以上のグラフィックボードと
メインメモリ 32GB 以上ないと困難だと思います。

NVIDIA 以外の環境は基本的には Linux 上で AMD Radeon RX 7800 XT でしか動作確認していません。 Radeon では ComfyUI のオプションを細かく指定しないとうまく動かない上に、Wan による動画生成も手元では動いていないので非推奨です
