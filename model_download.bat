:: FLUX Kontext
curl.exe -L -o models/diffusion_models/flux1-kontext-dev-Q4_K_M.gguf -# https://huggingface.co/QuantStack/FLUX.1-Kontext-dev-GGUF/resolve/main/flux1-kontext-dev-Q4_K_M.gguf
curl.exe -L -o models/clip/clip_l.safetensors -# https://huggingface.co/comfyanonymous/flux_text_encoders/resolve/main/clip_l.safetensors
curl.exe -L -o models/clip/t5-v1_1-xxl-encoder-Q4_K_M.gguf -# https://huggingface.co/city96/t5-v1_1-xxl-encoder-gguf/resolve/main/t5-v1_1-xxl-encoder-Q4_K_M.gguf
curl.exe -L -o models/vae/ae.safetensors -# https://huggingface.co/Comfy-Org/Lumina_Image_2.0_Repackaged/resolve/main/split_files/vae/ae.safetensors

:: Wan 2.2
curl.exe -L -o models/diffusion_models/wan2.2_i2v_high_noise_14B_Q4_K_M.gguf -#  https://huggingface.co/bullerwins/Wan2.2-I2V-A14B-GGUF/resolve/main/wan2.2_i2v_high_noise_14B_Q4_K_M.gguf
curl.exe -L -o models/diffusion_models/wan2.2_i2v_low_noise_14B_Q4_K_M.gguf -#  https://huggingface.co/bullerwins/Wan2.2-I2V-A14B-GGUF/resolve/main/wan2.2_i2v_low_noise_14B_Q4_K_M.gguf
curl.exe -L -o models/clip/umt5-xxl-encoder-Q4_K_M.gguf -#  https://huggingface.co/city96/umt5-xxl-encoder-gguf/resolve/main/umt5-xxl-encoder-Q4_K_M.gguf
curl.exe -L -o models/vae/wan_2.1_vae.safetensors -#  https://huggingface.co/Comfy-Org/Wan_2.1_ComfyUI_repackaged/resolve/main/split_files/vae/wan_2.1_vae.safetensors
curl.exe -L -o models/loras/wan2.2_i2v_lightx2v_4steps_lora_v1_high_noise.safetensors -#  https://huggingface.co/Comfy-Org/Wan_2.2_ComfyUI_Repackaged/resolve/main/split_files/loras/wan2.2_i2v_lightx2v_4steps_lora_v1_high_noise.safetensors
curl.exe -L -o models/loras/wan2.2_i2v_lightx2v_4steps_lora_v1_low_noise.safetensors -#  https://huggingface.co/Comfy-Org/Wan_2.2_ComfyUI_Repackaged/resolve/main/split_files/loras/wan2.2_i2v_lightx2v_4steps_lora_v1_low_noise.safetensors

:: Wan 2.2 S2V
curl.exe -L -o models/diffusion_models/Wan2.2-S2V-14B-Q4_K_M.gguf -# https://huggingface.co/QuantStack/Wan2.2-S2V-14B-GGUF/resolve/main/Wan2.2-S2V-14B-Q4_K_M.gguf
curl.exe -L -o models/loras/wan2.2_t2v_lightx2v_4steps_lora_v1.1_high_noise.safetensors -# https://huggingface.co/Comfy-Org/Wan_2.2_ComfyUI_Repackaged/resolve/main/split_files/loras/wan2.2_t2v_lightx2v_4steps_lora_v1.1_high_noise.safetensors
curl.exe -L -o models/audio_encoders/wav2vec2_large_english_fp16.safetensors -# https://huggingface.co/Comfy-Org/Wan_2.2_ComfyUI_Repackaged/resolve/main/split_files/audio_encoders/wav2vec2_large_english_fp16.safetensors

:: Qwen-Image-Edit
curl.exe -L -o models/unet/Qwen_Image_Edit-Q4_K_M.gguf -# https://huggingface.co/QuantStack/Qwen-Image-Edit-GGUF/resolve/main/Qwen_Image_Edit-Q4_K_M.gguf

curl.exe -L -o models/loras/Qwen-Image-Edit-Lightning-4steps-V1.0-bf16.safetensors -# https://huggingface.co/lightx2v/Qwen-Image-Lightning/resolve/main/Qwen-Image-Edit-Lightning-4steps-V1.0-bf16.safetensors

curl.exe -L -o models/text_encoders/Qwen2.5-VL-7B-Instruct-Q4_K_M.gguf -# https://huggingface.co/unsloth/Qwen2.5-VL-7B-Instruct-GGUF/resolve/main/Qwen2.5-VL-7B-Instruct-Q4_K_M.gguf
curl.exe -L -o models/text_encoders/Qwen2.5-VL-7B-Instruct-mmproj-BF16.gguf -# https://huggingface.co/QuantStack/Qwen-Image-Edit-GGUF/resolve/main/mmproj/Qwen2.5-VL-7B-Instruct-mmproj-BF16.gguf

curl.exe -L -o models/vae/Qwen_Image-VAE.safetensors -# https://huggingface.co/QuantStack/Qwen-Image-Edit-GGUF/resolve/main/VAE/Qwen_Image-VAE.safetensors

pause
