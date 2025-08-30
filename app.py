# SPDX-FileCopyrightText: 2025 asfdrwe <asfdrwe@gmail.com>
# SPDX-License-Identifier: MIT

import gradio as gr
import argparse
from gradio.processing_utils import PUBLIC_HOSTNAME_WHITELIST

import os
import sys
import importlib.util

base_path = os.path.dirname(os.path.realpath(__file__))
print(base_path)

sys.path.append(os.path.join(base_path, '.'))

server_address = ""

def main():
    parser = argparse.ArgumentParser(description="ComfyUIGradio: WebUI frontend for ComfyUI")
    parser.add_argument('--no-autolaunch', help="not autolaunch web browser", action='store_false')
#    parser.add_argument('--addr', help="server name (default: 127.0.0.1)", default="127.0.0.1")
#    parser.add_argument('--port', help="server port (default: 7860)", default=7860)
    parser.add_argument('--server_addr', help="ComfyUI server URL (default: localhost)", default="localhost")
    parser.add_argument('--server_port', help="ComfyUI server URL (default: 8188)", default="8188")

    args = parser.parse_args()
    server_address = args.server_addr + ":" + args.server_port;
    PUBLIC_HOSTNAME_WHITELIST.append(args.server_addr)

    custom_path = os.path.join(base_path, "uimodule")
    print(custom_path)

    # https://note.nkmk.me/python-listdir-isfile-isdir/
    files = [
        f for f in os.listdir(custom_path) if os.path.isfile(os.path.join(custom_path, f))
    ]

    files = sorted(files)
    print(files)

    with gr.Blocks() as app:
        for f in files:
            file_name = os.path.splitext(f)[0]
            print("FILE: " + file_name)
            spec = importlib.util.spec_from_file_location(file_name, os.path.join(custom_path, f))
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            print(module)
            module.create(server_address)

    app.queue()
    app.launch(inbrowser=args.no_autolaunch,
                # server_name=args.addr,
                # server_port=int(args.port),
    )

if __name__  == "__main__":
    main()
