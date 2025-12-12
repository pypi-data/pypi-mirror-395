"""
融合版本：
- 使用 test_13.py 的逻辑（图片增强、解析逻辑）
- 使用 run_dpsk_ocr_image.py 的离线 vLLM 启动方式
"""

import os, re, io, base64, json
from PIL import Image
import torch

# 设置环境变量
if torch.version.cuda == '11.8':
    os.environ["TRITON_PTXAS_PATH"] = "/usr/local/cuda-11.8/bin/ptxas"
os.environ['VLLM_USE_V1'] = '0'
os.environ["CUDA_VISIBLE_DEVICES"] = '0'

import sys
sys.path.insert(0, '/home/ad/tianhaoyang/deepseek_ocr/DeepSeek-OCR/DeepSeek-OCR-master/DeepSeek-OCR-vllm')

from vllm import LLM, SamplingParams
from vllm.model_executor.models.registry import ModelRegistry
from deepseek_ocr import DeepseekOCRForCausalLM
from process.ngram_norepeat import NoRepeatNGramLogitsProcessor
from process.image_process import DeepseekOCRProcessor

# 配置
MODEL_PATH = '/home/ad/tianhaoyang/vllm_model/deepseek-ai/DeepSeek-OCR'
CROP_MODE = True

# 默认提示词（与 test_13.py 一致）
DEFAULT_PROMPT = (
    "You are an OCR & document understanding assistant.\n"
    "Analyze this image region and produce:\n"
    "1) ALT: a very short alt text (<=12 words).\n"
    "2) CAPTION: a 1-2 sentence concise caption.\n"
    "3) CONTENT_MD: if the image contains a table, output a clean Markdown table;"
    "   if it contains a formula, output LaTeX ($...$ or $$...$$);"
    "   otherwise provide 3-6 bullet points summarizing key content, in Markdown.\n"
    "Return strictly in the following format:\n"
    "ALT: <short alt>\n"
    "CAPTION: <one or two sentences>\n"
    "CONTENT_MD:\n"
    "<markdown content here>\n"
)

IMG_PATTERN = re.compile(r'!\[[^\]]*\]\(([^)]+)\)')

# 全局变量
_llm = None
_sampling_params = None

def init_vllm():
    """初始化 vLLM（参考 run_dpsk_ocr_image.py）"""
    global _llm, _sampling_params
    
    if _llm is not None:
        return
    
    print("🔄 正在加载模型...")
    
    # 注册模型
    ModelRegistry.register_model("DeepseekOCRForCausalLM", DeepseekOCRForCausalLM)
    
    # 初始化 LLM
    _llm = LLM(
        model=MODEL_PATH,
        hf_overrides={"architectures": ["DeepseekOCRForCausalLM"]},
        block_size=256,
        max_model_len=8192,
        enforce_eager=False,
        trust_remote_code=True,
        tensor_parallel_size=1,
        gpu_memory_utilization=0.9,
        disable_mm_preprocessor_cache=True
    )
    
    # 配置采样参数
    logits_processors = [
        NoRepeatNGramLogitsProcessor(
            ngram_size=20,
            window_size=50,
            whitelist_token_ids={128821, 128822}
        )
    ]
    
    _sampling_params = SamplingParams(
        temperature=0.2,
        max_tokens=2048,
        logits_processors=logits_processors,
        skip_special_tokens=False,
        include_stop_str_in_output=True,
    )
    
    print("✅ 模型加载完成！")


def call_deepseek_ocr_image(img_path, temperature=0.2, max_tokens=2048, prompt=DEFAULT_PROMPT):
    """调用 DeepSeek-OCR 进行图片解析（与 test_13.py 逻辑一致）"""
    global _llm, _sampling_params
    
    if _llm is None:
        init_vllm()
    
    # 读取图片
    with Image.open(img_path) as im:
        image = im.convert('RGB')
    
    # 准备输入（参考 run_dpsk_ocr_image.py）
    full_prompt = f"<image>\n{prompt}"
    image_features = DeepseekOCRProcessor().tokenize_with_images(
        images=[image],
        bos=True,
        eos=True,
        cropping=CROP_MODE
    )
    
    request = {
        "prompt": full_prompt,
        "multi_modal_data": {"image": image_features}
    }
    
    # 生成
    outputs = _llm.generate([request], sampling_params=_sampling_params)
    text = outputs[0].outputs[0].text.strip()
    
    # 清理结束标记
    if '<｜end▁of▁sentence｜>' in text:
        text = text.replace('<｜end▁of▁sentence｜>', '')
    
    # 调试：打印模型原始输出
    print(f"\n{'='*60}")
    print(f"图片: {os.path.basename(img_path)}")
    print(f"模型输出:\n{text[:500]}")  # 打印前500个字符
    print(f"{'='*60}\n")
    
    # 解析 DeepSeek-OCR 原生格式
    import re
    
    # 方法1：逐行处理，移除包含标记的行，保留实际内容
    lines = []
    for line in text.splitlines():
        line = line.strip()
        # 跳过只包含标记的行
        if line.startswith('<|ref|>') or line.startswith('<|det|>'):
            continue
        # 移除行内的标记
        line = re.sub(r'<\|ref\|>.*?</\|ref\|>', '', line)
        line = re.sub(r'<\|det\|>.*?</\|det\|>', '', line)
        line = line.strip()
        if line:  # 只保留非空行
            lines.append(line)
    
    content_md = "\n\n".join(lines)  # 用双换行分隔，使 Markdown 格式更清晰
    
    # 生成简单的 caption（取第一行或前50个字符）
    caption = lines[0][:50] if lines else ""
    
    result = {
        "alt": "Figure",
        "caption": caption,
        "content_md": content_md
    }
    
    # 调试：打印解析结果
    print(f"解析结果: ALT='{result['alt']}', CAPTION='{result['caption'][:50] if result['caption'] else '(空)'}', CONTENT_MD长度={len(result['content_md'])}")
    
    return result


def augment_markdown(md_path, out_path,
                     temperature=0.2, max_tokens=2048,
                     image_root=".",
                     cache_json=None):
    """增强 Markdown（与 test_13.py 完全一致）"""
    with open(md_path, "r", encoding="utf-8") as f:
        md_lines = f.read().splitlines()

    cache = {}
    if cache_json and os.path.exists(cache_json):
        try:
            cache = json.load(open(cache_json, "r", encoding="utf-8"))
        except Exception:
            cache = {}

    # 初始化模型
    init_vllm()

    out_lines = []
    for line in md_lines:
        out_lines.append(line)
        m = IMG_PATTERN.search(line)
        if not m:
            continue

        img_rel = m.group(1).strip().split("?")[0]
        img_path = img_rel if os.path.isabs(img_rel) else os.path.join(image_root, img_rel)

        if not os.path.exists(img_path):
            out_lines.append(f"<!-- WARN: image not found: {img_rel} -->")
            continue

        if cache_json and img_path in cache:
            result = cache[img_path]
        else:
            result = call_deepseek_ocr_image(img_path, temperature, max_tokens)
            if cache_json:
                cache[img_path] = result

        alt, cap, body = result["alt"], result["caption"], result["content_md"]

        if cap:
            out_lines.append(f"*{cap}*")
        if body:
            out_lines.append("<details><summary>解析</summary>\n")
            out_lines.append(body)
            out_lines.append("\n</details>")

    with open(out_path, "w", encoding="utf-8") as f:
        f.write("\n".join(out_lines))

    if cache_json:
        with open(cache_json, "w", encoding="utf-8") as f:
            json.dump(cache, f, ensure_ascii=False, indent=2)

    print(f"✅ 已写入增强后的 Markdown：{out_path}")


# 运行
augment_markdown(
    md_path="/home/ad/tianhaoyang/deepseek_ocr/image_output_2/pdf_to_markdown/0.LangChain技术生态介绍.md",
    out_path="/home/ad/tianhaoyang/deepseek_ocr/image_output_2/pdf_to_markdown_augmented/0.LangChain技术生态介绍_augmented.md",
    image_root="/home/ad/tianhaoyang/deepseek_ocr/image_output_2/pdf_to_markdown",
    cache_json="/home/ad/tianhaoyang/deepseek_ocr/image_output_2/pdf_to_markdown_augmented/image_cache.json"
)

