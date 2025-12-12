"""
PDF to Markdown MCP Server
使用 DeepSeek-OCR 将 PDF 转换为 Markdown，并对图片进行解析增强

功能：
1. pdf_to_markdown: 将 PDF 转换为 Markdown（图片只保留链接）
2. augment_markdown_images: 对 Markdown 中的图片链接添加解析内容
3. pdf_to_markdown_full: 一站式完成 PDF 转 Markdown 并增强图片解析
"""

import os
import sys
import argparse
import re
import io
import json
from typing import Any, Dict, Optional
from concurrent.futures import ThreadPoolExecutor

# ============================================
# 环境变量设置（必须在导入 torch 之前）
# ============================================
os.environ['VLLM_USE_V1'] = '0'

import torch
if torch.version.cuda == '11.8':
    os.environ["TRITON_PTXAS_PATH"] = "/usr/local/cuda-11.8/bin/ptxas"

# ============================================
# 添加 DeepSeek-OCR-vllm 路径到 sys.path
# 这必须在导入 DeepSeek-OCR 相关模块之前完成
# ============================================
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DEEPSEEK_OCR_PATH = os.path.join(os.path.dirname(SCRIPT_DIR), 'DeepSeek-OCR-vllm')
if DEEPSEEK_OCR_PATH not in sys.path:
    sys.path.insert(0, DEEPSEEK_OCR_PATH)

# ============================================
# 标准库和第三方库导入
# ============================================
import fitz  # PyMuPDF
import img2pdf
from PIL import Image, ImageDraw, ImageFont
import numpy as np
from tqdm import tqdm
from mcp.server.fastmcp import FastMCP

# ============================================
# 全局变量
# ============================================
_llm = None
_sampling_params = None
_sampling_params_image = None
_model_initialized = False
_deepseek_processor = None

# ============================================
# 配置参数（从 config.py 中提取，避免导入时加载 TOKENIZER）
# ============================================
MODEL_PATH = '/home/ad/tianhaoyang/vllm_model/deepseek-ai/DeepSeek-OCR'
CROP_MODE = True
MAX_CONCURRENCY = 100
NUM_WORKERS = 64
SKIP_REPEAT = True
BASE_SIZE = 1024
IMAGE_SIZE = 640
MIN_CROPS = 2
MAX_CROPS = 6

# ============================================
# 默认提示词
# ============================================
PDF_PROMPT = '<image>\n<|grounding|>Convert the document to markdown.'
IMAGE_PROMPT = (
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

# ============================================
# 正则表达式
# ============================================
IMG_PATTERN = re.compile(r'!\[[^\]]*\]\(([^)]+)\)')
REF_PATTERN = r'(<\|ref\|>(.*?)<\|/ref\|><\|det\|>(.*?)<\|/det\|>)'

# ============================================
# 创建 MCP 服务器
# ============================================
mcp = FastMCP("pdf-to-markdown")


def init_vllm(gpu_id: str = '0'):
    """初始化 vLLM 模型（延迟加载）"""
    global _llm, _sampling_params, _sampling_params_image, _model_initialized, _deepseek_processor
    
    if _model_initialized:
        return
    
    os.environ["CUDA_VISIBLE_DEVICES"] = gpu_id
    
    sys.stderr.write("🔄 正在加载 DeepSeek-OCR 模型...\n")
    
    # ============================================
    # 导入 vLLM 和 DeepSeek-OCR 相关模块
    # 这些导入会触发 config.py 的加载，所以必须确保路径已设置
    # ============================================
    from vllm import LLM, SamplingParams
    from vllm.model_executor.models.registry import ModelRegistry
    from deepseek_ocr import DeepseekOCRForCausalLM
    from process.ngram_norepeat import NoRepeatNGramLogitsProcessor
    from process.image_process import DeepseekOCRProcessor
    
    # 保存处理器引用
    _deepseek_processor = DeepseekOCRProcessor
    
    # 注册模型
    ModelRegistry.register_model("DeepseekOCRForCausalLM", DeepseekOCRForCausalLM)
    
    # 初始化 LLM
    _llm = LLM(
        model=MODEL_PATH,
        hf_overrides={"architectures": ["DeepseekOCRForCausalLM"]},
        block_size=256,
        enforce_eager=False,
        trust_remote_code=True,
        max_model_len=8192,
        swap_space=0,
        max_num_seqs=MAX_CONCURRENCY,
        tensor_parallel_size=1,
        gpu_memory_utilization=0.9,
        disable_mm_preprocessor_cache=True
    )
    
    # PDF 转换的采样参数（temperature=0.0）
    logits_processors = [
        NoRepeatNGramLogitsProcessor(
            ngram_size=20,
            window_size=50,
            whitelist_token_ids={128821, 128822}
        )
    ]
    
    _sampling_params = SamplingParams(
        temperature=0.0,
        max_tokens=8192,
        logits_processors=logits_processors,
        skip_special_tokens=False,
        include_stop_str_in_output=True,
    )
    
    # 图片解析的采样参数（temperature=0.2）
    _sampling_params_image = SamplingParams(
        temperature=0.2,
        max_tokens=2048,
        logits_processors=logits_processors,
        skip_special_tokens=False,
        include_stop_str_in_output=True,
    )
    
    _model_initialized = True
    sys.stderr.write("✅ DeepSeek-OCR 模型加载完成！\n")


def get_deepseek_processor():
    """获取 DeepseekOCRProcessor（延迟导入）"""
    global _deepseek_processor
    
    if _deepseek_processor is None:
        from process.image_process import DeepseekOCRProcessor
        _deepseek_processor = DeepseekOCRProcessor
    
    return _deepseek_processor


def pdf_to_images_high_quality(pdf_path: str, dpi: int = 144) -> list:
    """将 PDF 转换为高质量图片列表"""
    images = []
    pdf_document = fitz.open(pdf_path)
    
    zoom = dpi / 72.0
    matrix = fitz.Matrix(zoom, zoom)
    
    for page_num in range(pdf_document.page_count):
        page = pdf_document[page_num]
        pixmap = page.get_pixmap(matrix=matrix, alpha=False)
        Image.MAX_IMAGE_PIXELS = None
        
        img_data = pixmap.tobytes("png")
        img = Image.open(io.BytesIO(img_data))
        images.append(img)
    
    pdf_document.close()
    return images


def re_match(text: str):
    """匹配文本中的 ref/det 标签"""
    matches = re.findall(REF_PATTERN, text, re.DOTALL)
    
    matches_image = []
    matches_other = []
    for a_match in matches:
        if '<|ref|>image<|/ref|>' in a_match[0]:
            matches_image.append(a_match[0])
        else:
            matches_other.append(a_match[0])
    return matches, matches_image, matches_other


def extract_coordinates_and_label(ref_text, image_width: int, image_height: int):
    """从 ref 文本中提取坐标和标签"""
    try:
        label_type = ref_text[1]
        cor_list = eval(ref_text[2])
    except Exception as e:
        sys.stderr.write(f"坐标提取错误: {e}\n")
        return None
    return (label_type, cor_list)


def save_cropped_images(image: Image.Image, refs: list, output_path: str, page_idx: int):
    """保存裁剪的图片"""
    image_width, image_height = image.size
    img_idx = 0
    
    for ref in refs:
        try:
            result = extract_coordinates_and_label(ref, image_width, image_height)
            if result:
                label_type, points_list = result
                
                for points in points_list:
                    x1, y1, x2, y2 = points
                    x1 = int(x1 / 999 * image_width)
                    y1 = int(y1 / 999 * image_height)
                    x2 = int(x2 / 999 * image_width)
                    y2 = int(y2 / 999 * image_height)
                    
                    if label_type == 'image':
                        try:
                            cropped = image.crop((x1, y1, x2, y2))
                            cropped.save(f"{output_path}/images/{page_idx}_{img_idx}.jpg")
                        except Exception as e:
                            sys.stderr.write(f"图片保存错误: {e}\n")
                        img_idx += 1
        except:
            continue


def process_single_image_for_pdf(image: Image.Image, prompt: str):
    """处理单张图片用于 PDF 转换"""
    DeepseekOCRProcessor = get_deepseek_processor()
    
    cache_item = {
        "prompt": prompt,
        "multi_modal_data": {
            "image": DeepseekOCRProcessor().tokenize_with_images(
                images=[image], bos=True, eos=True, cropping=CROP_MODE
            )
        },
    }
    return cache_item


def call_deepseek_ocr_image(img_path: str, prompt: str = IMAGE_PROMPT) -> Dict[str, str]:
    """调用 DeepSeek-OCR 解析单张图片"""
    global _llm, _sampling_params_image
    
    if _llm is None:
        init_vllm()
    
    DeepseekOCRProcessor = get_deepseek_processor()
    
    # 读取图片
    with Image.open(img_path) as im:
        image = im.convert('RGB')
    
    # 准备输入
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
    outputs = _llm.generate([request], sampling_params=_sampling_params_image)
    text = outputs[0].outputs[0].text.strip()
    
    # 清理结束标记
    if '<｜end▁of▁sentence｜>' in text:
        text = text.replace('<｜end▁of▁sentence｜>', '')
    
    # 解析 DeepSeek-OCR 原生格式
    lines = []
    for line in text.splitlines():
        line = line.strip()
        if line.startswith('<|ref|>') or line.startswith('<|det|>'):
            continue
        line = re.sub(r'<\|ref\|>.*?</\|ref\|>', '', line)
        line = re.sub(r'<\|det\|>.*?</\|det\|>', '', line)
        line = line.strip()
        if line:
            lines.append(line)
    
    content_md = "\n\n".join(lines)
    caption = lines[0][:50] if lines else ""
            
    return {
        "alt": "Figure",
        "caption": caption,
        "content_md": content_md
    }


@mcp.tool()
def pdf_to_markdown(
    pdf_path: str,
    output_dir: str,
    gpu_id: str = "0"
) -> Dict[str, Any]:
    """将 PDF 文件转换为 Markdown 格式（图片只保留链接，不解析内容）
    
    Args:
        pdf_path (str): PDF 文件的完整路径 (例如: "/path/to/document.pdf")
        output_dir (str): 输出目录的完整路径 (例如: "/path/to/output")
        gpu_id (str): 使用的 GPU ID (默认: "0")
        
    Returns:
        Dict[str, Any]: 包含转换结果的字典
            - success: 是否成功
            - markdown_path: 生成的 Markdown 文件路径
            - images_dir: 图片保存目录
            - page_count: 处理的页数
            - error: 错误信息（如果失败）
    """
    try:
        # 验证输入文件
        if not os.path.exists(pdf_path):
            return {"success": False, "error": f"PDF 文件不存在: {pdf_path}"}
        
        if not pdf_path.lower().endswith('.pdf'):
            return {"success": False, "error": "输入文件必须是 PDF 格式"}
        
        # 初始化模型
        init_vllm(gpu_id)
        
        # 创建输出目录
        os.makedirs(output_dir, exist_ok=True)
        images_dir = os.path.join(output_dir, 'images')
        os.makedirs(images_dir, exist_ok=True)
        
        sys.stderr.write(f"🔄 正在加载 PDF: {pdf_path}\n")
        
        # 将 PDF 转换为图片
        images = pdf_to_images_high_quality(pdf_path)
        
        # 准备批量输入
        prompt = PDF_PROMPT
        
        def process_image(img):
            return process_single_image_for_pdf(img, prompt)
        
        with ThreadPoolExecutor(max_workers=NUM_WORKERS) as executor:
            batch_inputs = list(tqdm(
                executor.map(process_image, images),
                total=len(images),
                desc="预处理图片"
            ))
        
        # 批量生成
        sys.stderr.write("🔄 正在进行 OCR 识别...\n")
        outputs_list = _llm.generate(batch_inputs, sampling_params=_sampling_params)
        
        # 处理输出
        pdf_name = os.path.basename(pdf_path).replace('.pdf', '')
        mmd_path = os.path.join(output_dir, f'{pdf_name}.md')
        
        contents = ''
        page_idx = 0
        
        for output, img in zip(outputs_list, images):
            content = output.outputs[0].text
            
            # 清理结束标记
            if '<｜end▁of▁sentence｜>' in content:
                content = content.replace('<｜end▁of▁sentence｜>', '')
            else:
                if SKIP_REPEAT:
                    continue
            
            # 提取并保存图片
            matches_ref, matches_images, matches_other = re_match(content)
            save_cropped_images(img, matches_ref, output_dir, page_idx)
            
            # 替换图片标记为 Markdown 图片链接
            for idx, a_match_image in enumerate(matches_images):
                content = content.replace(
                    a_match_image, 
                    f'![](images/{page_idx}_{idx}.jpg)\n'
                )
            
            # 清理其他标记
            for a_match_other in matches_other:
                content = content.replace(a_match_other, '')
            
            content = content.replace('\\coloneqq', ':=')
            content = content.replace('\\eqqcolon', '=:')
            content = content.replace('\n\n\n\n', '\n\n')
            content = content.replace('\n\n\n', '\n\n')
            
            # 添加页面分隔符
            page_split = f'\n<--- Page {page_idx + 1} --->\n'
            contents += content + page_split
            
            page_idx += 1
        
        # 保存 Markdown 文件
        with open(mmd_path, 'w', encoding='utf-8') as f:
            f.write(contents)
        
        sys.stderr.write(f"✅ Markdown 文件已保存: {mmd_path}\n")
        
        return {
            "success": True,
            "markdown_path": mmd_path,
            "images_dir": images_dir,
            "page_count": page_idx,
            "message": f"成功将 PDF 转换为 Markdown，共处理 {page_idx} 页"
            }
        
    except Exception as e:
        import traceback
        traceback.print_exc(file=sys.stderr)
        return {"success": False, "error": f"转换失败: {str(e)}"}


@mcp.tool()
def augment_markdown_images(
    markdown_path: str,
    output_path: Optional[str] = None,
    image_root: Optional[str] = None,
    cache_json: Optional[str] = None,
    gpu_id: str = "0"
) -> Dict[str, Any]:
    """为 Markdown 文件中的图片链接添加解析内容
    
    Args:
        markdown_path (str): 输入的 Markdown 文件路径
        output_path (str, optional): 输出文件路径。如果不指定，会在原文件名后加 _augmented
        image_root (str, optional): 图片根目录。如果不指定，使用 Markdown 文件所在目录
        cache_json (str, optional): 缓存文件路径，用于避免重复解析相同图片
        gpu_id (str): 使用的 GPU ID (默认: "0")
        
    Returns:
        Dict[str, Any]: 包含处理结果的字典
            - success: 是否成功
            - output_path: 输出文件路径
            - images_processed: 处理的图片数量
            - error: 错误信息（如果失败）
    """
    try:
        # 验证输入文件
        if not os.path.exists(markdown_path):
            return {"success": False, "error": f"Markdown 文件不存在: {markdown_path}"}
        
        # 初始化模型
        init_vllm(gpu_id)
        
        # 设置默认路径
        md_dir = os.path.dirname(markdown_path)
        md_name = os.path.basename(markdown_path)
        
        if output_path is None:
            name_without_ext = os.path.splitext(md_name)[0]
            output_path = os.path.join(md_dir, f"{name_without_ext}_augmented.md")
        
        if image_root is None:
            image_root = md_dir
        
        # 读取 Markdown 文件
        with open(markdown_path, 'r', encoding='utf-8') as f:
            md_lines = f.read().splitlines()
        
        # 加载缓存
        cache = {}
        if cache_json and os.path.exists(cache_json):
            try:
                with open(cache_json, 'r', encoding='utf-8') as f:
                    cache = json.load(f)
            except Exception:
                cache = {}
        
        # 处理每一行
        out_lines = []
        images_processed = 0
        
        for line in md_lines:
            out_lines.append(line)
            
            # 查找图片链接
            m = IMG_PATTERN.search(line)
            if not m:
                continue
            
            img_rel = m.group(1).strip().split("?")[0]
            img_path = img_rel if os.path.isabs(img_rel) else os.path.join(image_root, img_rel)
                
            if not os.path.exists(img_path):
                out_lines.append(f"<!-- WARN: image not found: {img_rel} -->")
                continue
                            
            # 检查缓存或解析图片
            if cache_json and img_path in cache:
                result = cache[img_path]
            else:
                sys.stderr.write(f"🔄 正在解析图片: {os.path.basename(img_path)}\n")
                result = call_deepseek_ocr_image(img_path)
                if cache_json:
                    cache[img_path] = result
            
            # 添加解析内容
            alt, cap, body = result["alt"], result["caption"], result["content_md"]
            
            if cap:
                out_lines.append(f"*{cap}*")
            if body:
                out_lines.append("<details><summary>图片解析</summary>\n")
                out_lines.append(body)
                out_lines.append("\n</details>")
            
            images_processed += 1
        
        # 保存输出文件
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write("\n".join(out_lines))
                        
        # 保存缓存
        if cache_json:
            cache_dir = os.path.dirname(cache_json)
            if cache_dir:
                os.makedirs(cache_dir, exist_ok=True)
            with open(cache_json, 'w', encoding='utf-8') as f:
                json.dump(cache, f, ensure_ascii=False, indent=2)
        
        sys.stderr.write(f"✅ 增强后的 Markdown 已保存: {output_path}\n")
        
        return {
            "success": True,
            "output_path": output_path,
            "images_processed": images_processed,
            "message": f"成功处理 {images_processed} 张图片"
        }
        
    except Exception as e:
        import traceback
        traceback.print_exc(file=sys.stderr)
        return {"success": False, "error": f"处理失败: {str(e)}"}


@mcp.tool()
def pdf_to_markdown_full(
    pdf_path: str,
    output_dir: str,
    augment_images: bool = True,
    cache_json: Optional[str] = None,
    gpu_id: str = "0"
) -> Dict[str, Any]:
    """一站式将 PDF 转换为 Markdown 并解析图片内容
    
    这个工具会：
    1. 将 PDF 转换为 Markdown（提取文本和图片）
    2. 如果 augment_images=True，对每张图片进行 OCR 解析并添加到 Markdown 中
    
    Args:
        pdf_path (str): PDF 文件的完整路径 (例如: "/path/to/document.pdf")
        output_dir (str): 输出目录的完整路径 (例如: "/path/to/output")
        augment_images (bool): 是否解析图片内容 (默认: True)
        cache_json (str, optional): 图片解析缓存文件路径
        gpu_id (str): 使用的 GPU ID (默认: "0")
    
    Returns:
        Dict[str, Any]: 包含转换结果的字典
            - success: 是否成功
            - markdown_path: 基础 Markdown 文件路径
            - augmented_path: 增强后的 Markdown 文件路径（如果 augment_images=True）
            - images_dir: 图片保存目录
            - page_count: 处理的页数
            - images_processed: 解析的图片数量
            - error: 错误信息（如果失败）
    """
    try:
        # 步骤1：将 PDF 转换为 Markdown
        sys.stderr.write("=" * 50 + "\n")
        sys.stderr.write("📄 步骤 1/2: 将 PDF 转换为 Markdown\n")
        sys.stderr.write("=" * 50 + "\n")
        
        step1_result = pdf_to_markdown(pdf_path, output_dir, gpu_id)
        
        if not step1_result.get("success"):
            return step1_result
        
        result = {
            "success": True,
            "markdown_path": step1_result["markdown_path"],
            "images_dir": step1_result["images_dir"],
            "page_count": step1_result["page_count"],
        }
        
        # 步骤2：解析图片内容（如果启用）
        if augment_images:
            sys.stderr.write("\n" + "=" * 50 + "\n")
            sys.stderr.write("🖼️ 步骤 2/2: 解析图片内容\n")
            sys.stderr.write("=" * 50 + "\n")
            
            # 设置默认缓存路径
            if cache_json is None:
                cache_json = os.path.join(output_dir, "image_cache.json")
            
            step2_result = augment_markdown_images(
                markdown_path=step1_result["markdown_path"],
                output_path=None,  # 使用默认路径
                image_root=output_dir,
                cache_json=cache_json,
                gpu_id=gpu_id
            )
            
            if step2_result.get("success"):
                result["augmented_path"] = step2_result["output_path"]
                result["images_processed"] = step2_result["images_processed"]
            else:
                result["augment_warning"] = step2_result.get("error", "图片解析失败")
        
        result["message"] = f"PDF 转换完成！共 {result['page_count']} 页"
        if augment_images and "images_processed" in result:
            result["message"] += f"，解析了 {result['images_processed']} 张图片"
        
        sys.stderr.write("\n" + "=" * 50 + "\n")
        sys.stderr.write("✅ 全部处理完成！\n")
        sys.stderr.write("=" * 50 + "\n")
            
        return result
        
    except Exception as e:
        import traceback
        traceback.print_exc(file=sys.stderr)
        return {"success": False, "error": f"处理失败: {str(e)}"}


def log_stderr(msg: str):
    """将日志输出到 stderr（避免干扰 MCP stdio 通信）"""
    sys.stderr.write(f"{msg}\n")
    sys.stderr.flush()


def main():
    """MCP 服务器入口点"""
    import warnings
    warnings.filterwarnings("ignore")
    
    parser = argparse.ArgumentParser(
        description="PDF to Markdown MCP Server",
        add_help=False
    )
    
    parser.add_argument(
        '--transport', 
        default='stdio', 
        choices=['stdio', 'sse', 'streamable-http'],
        help='传输类型 (stdio, sse, 或 streamable-http)'
    )
    
    parser.add_argument(
        '--model_path',
        type=str,
        default=None,
        help='DeepSeek-OCR 模型路径'
    )
    
    parser.add_argument(
        '--gpu_id',
        type=str, 
        default='0',
        help='使用的 GPU ID'
    )
    
    try:
        args = parser.parse_args()
        
        # 更新全局配置
        global MODEL_PATH
        if args.model_path:
            MODEL_PATH = args.model_path
        
        # 使用 stderr 输出日志，避免干扰 MCP stdio 通信
        log_stderr(f"🚀 PDF to Markdown MCP Server 启动中...")
        log_stderr(f"   模型路径: {MODEL_PATH}")
        log_stderr(f"   GPU ID: {args.gpu_id}")
        log_stderr(f"   DeepSeek-OCR 路径: {DEEPSEEK_OCR_PATH}")
        
        # 运行 MCP 服务器
        mcp.run(transport=args.transport)
        
    except Exception as e:
        import traceback
        traceback.print_exc(file=sys.stderr)
        sys.stderr.write(f"启动失败: {str(e)}\n")
        sys.exit(1)


if __name__ == "__main__":
    main()
