"""Queue SDXL renders on pompom's ComfyUI and download them. usage: comfy.py outdir"""
import json, sys, time, urllib.request
H = "http://pompom:8188"
NEG = "text, letters, watermark, logo, signature, people, person, frame, border, oversaturated, warm colors, orange, harsh contrast, lowres, jpeg artifacts"
JOBS = [
 ("hero-fog", 1536, 640, "minimal abstract fine-art landscape, layered soft mist over distant blue-gray mountain ridges, pale soft white sky, smooth tonal gradient, vast empty negative space on the left, cool steel blue and slate tones, quiet, matte, high key"),
 ("hero-arcs", 1536, 640, "minimal abstract architecture, smooth white curved concrete arcs and thin parallel lines in soft diffuse light, cool blue-gray shadows, vast negative space, clean geometry, high key, matte"),
 ("dark-lines", 1344, 704, "abstract dark background, deep midnight navy, faint thin curved lines of steel blue light arcing across, subtle gradient, minimal, vast dark negative space, matte, elegant"),
]
def run(name, w, h, prompt, seed):
    wf = {
     "1": {"class_type": "CheckpointLoaderSimple", "inputs": {"ckpt_name": "juggernautXL_ragnarokBy.safetensors"}},
     "2": {"class_type": "CLIPTextEncode", "inputs": {"clip": ["1", 1], "text": prompt}},
     "3": {"class_type": "CLIPTextEncode", "inputs": {"clip": ["1", 1], "text": NEG}},
     "4": {"class_type": "EmptyLatentImage", "inputs": {"width": w, "height": h, "batch_size": 1}},
     "5": {"class_type": "KSampler", "inputs": {"model": ["1", 0], "positive": ["2", 0], "negative": ["3", 0], "latent_image": ["4", 0], "seed": seed, "steps": 30, "cfg": 5.0, "sampler_name": "dpmpp_2m", "scheduler": "karras", "denoise": 1.0}},
     "6": {"class_type": "VAEDecode", "inputs": {"samples": ["5", 0], "vae": ["1", 2]}},
     "7": {"class_type": "SaveImage", "inputs": {"images": ["6", 0], "filename_prefix": "parlette_" + name}}}
    req = urllib.request.Request(H + "/prompt", json.dumps({"prompt": wf}).encode(), {"Content-Type": "application/json"})
    pid = json.load(urllib.request.urlopen(req))["prompt_id"]
    while True:
        hist = json.load(urllib.request.urlopen(f"{H}/history/{pid}"))
        if pid in hist: break
        time.sleep(3)
    img = hist[pid]["outputs"]["7"]["images"][0]
    url = f"{H}/view?filename={img['filename']}&subfolder={img['subfolder']}&type={img['type']}"
    open(f"{sys.argv[1]}/{name}-{seed}.png", "wb").write(urllib.request.urlopen(url).read())
    print(name, seed, flush=True)
for name, w, h, p in JOBS:
    for seed in (11, 23):
        run(name, w, h, p, seed)
