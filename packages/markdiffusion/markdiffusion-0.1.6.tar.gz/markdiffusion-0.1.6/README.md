<div align="center">

<img src="https://raw.githubusercontent.com/THU-BPM/markdiffusion/main/img/markdiffusion-color-1.jpg" style="width: 65%;"/>

# An Open-Source Toolkit for Generative Watermarking of Latent Diffusion Models

[![Homepage](https://img.shields.io/badge/Homepage-5F259F?style=for-the-badge&logo=homepage&logoColor=white)](https://generative-watermark.github.io/)
[![Paper](https://img.shields.io/badge/Paper-A42C25?style=for-the-badge&logo=arxiv&logoColor=white)](https://arxiv.org/abs/2509.10569)
[![HF Models](https://img.shields.io/badge/HF--Models-%23FFD14D?style=for-the-badge&logo=huggingface&logoColor=black)](https://huggingface.co/Generative-Watermark-Toolkits) 
</div>

> 🔥 **As a new released project, We welcome PRs!** If you have implemented a LDM watermarking algorithm or are interested in contributing one, we'd love to include it in MarkDiffusion. Join our community and help make generative watermarking more accessible to everyone!

## Contents
- [An Open-Source Toolkit for Generative Watermarking of Latent Diffusion Models](#an-open-source-toolkit-for-generative-watermarking-of-latent-diffusion-models)
  - [Contents](#contents)
  - [🔥 Updates](#-updates)
  - [Introduction to MarkDiffusion](#introduction-to-markdiffusion)
    - [Overview](#overview)
    - [Key Features](#key-features)
    - [Implemented Algorithms](#implemented-algorithms)
    - [Evaluation Module](#evaluation-module)
      - [Evaluation Pipelines](#evaluation-pipelines)
  - [Installation](#installation)
    - [Prerequisites: Install PyTorch](#prerequisites-install-pytorch)
    - [Option 1: Install from PyPI (Recommended)](#option-1-install-from-pypi-recommended)
    - [Option 2: Install from Source](#option-2-install-from-source)
    - [Requirements](#requirements)
  - [Quick Start](#quick-start)
  - [How to Use the Toolkit](#how-to-use-the-toolkit)
    - [Generating and Detecting Watermarked Media](#generating-and-detecting-watermarked-media)
      - [Cases for Generating and Detecting Watermarked Media](#cases-for-generating-and-detecting-watermarked-media)
    - [Visualizing Watermarking Mechanisms](#visualizing-watermarking-mechanisms)
      - [Cases for Visualizing Watermarking Mechanism](#cases-for-visualizing-watermarking-mechanism)
    - [Evaluation Pipelines](#evaluation-pipelines-1)
      - [Cases for Evaluation](#cases-for-evaluation)
  - [Citation](#citation)


## 🔥 Updates
🎯 **(2025.10.10)** Add *Mask, Overlay, AdaptiveNoiseInjection* image attack tools, thanks Zheyu Fu for his PR!

🎯 **(2025.10.09)** Add *VideoCodecAttack, FrameRateAdapter, FrameInterpolationAttack* video attack tools, thanks Luyang Si for his PR!

🎯 **(2025.10.08)** Add *SSIM, BRISQUE, VIF, FSIM* image quality analyzer, thanks Huan Wang for her PR!

✨ **(2025.10.07)** Add [SFW](https://arxiv.org/pdf/2509.07647) watermarking method, thanks Huan Wang for her PR!

✨ **(2025.10.07)** Add [VideoMark](https://arxiv.org/abs/2504.16359) watermarking method, thanks Hanqian Li for his PR!

✨ **(2025.9.29)** Add [GaussMarker](https://arxiv.org/abs/2506.11444) watermarking method, thanks Luyang Si for his PR!

## Introduction to MarkDiffusion

### Overview

MarkDiffusion is an open-source Python toolkit for generative watermarking of latent diffusion models. As the use of diffusion-based generative models expands, ensuring the authenticity and origin of generated media becomes critical. MarkDiffusion simplifies the access, understanding, and assessment of watermarking technologies, making it accessible to both researchers and the broader community. *Note: if you are interested in LLM watermarking (text watermark), please refer to the [MarkLLM](https://github.com/THU-BPM/MarkLLM) toolkit from our group.*

The toolkit comprises three key components: a unified implementation framework for streamlined watermarking algorithm integrations and user-friendly interfaces; a mechanism visualization suite that intuitively showcases added and extracted watermark patterns to aid public understanding; and a comprehensive evaluation module offering standard implementations of 24 tools across three essential aspects—detectability, robustness, and output quality, plus 8 automated evaluation pipelines.

<img src="https://raw.githubusercontent.com/THU-BPM/markdiffusion/main/img/fig1_overview.png" alt="MarkDiffusion Overview" style="zoom:50%;" />

### Key Features

- **Unified Implementation Framework:** MarkDiffusion provides a modular architecture supporting eight state-of-the-art generative image/video watermarking algorithms of LDMs.

- **Comprehensive Algorithm Support:** Currently implements 8 watermarking algorithms from two major categories: Pattern-based methods (Tree-Ring, Ring-ID, ROBIN, WIND) and Key-based methods (Gaussian-Shading, PRC, SEAL, VideoShield).

- **Visualization Solutions:** The toolkit includes custom visualization tools that enable clear and insightful views into how different watermarking algorithms operate under various scenarios. These visualizations help demystify the algorithms' mechanisms, making them more understandable for users.

- **Evaluation Module:** With 20 evaluation tools covering detectability, robustness, and impact on output quality, MarkDiffusion provides comprehensive assessment capabilities. It features 5 automated evaluation pipelines: Watermark Detection Pipeline, Image Quality Analysis Pipeline, Video Quality Analysis Pipeline, and specialized robustness assessment tools.

### Implemented Algorithms

| **Algorithm** | **Category** | **Target** | **Reference** |
|---------------|-------------|------------|---------------|
| Tree-Ring | Pattern | Image | [Tree-Ring Watermarks: Fingerprints for Diffusion Images that are Invisible and Robust](https://arxiv.org/abs/2305.20030) |
| Ring-ID | Pattern | Image | [RingID: Rethinking Tree-Ring Watermarking for Enhanced Multi-Key Identification](https://arxiv.org/abs/2404.14055) |
| ROBIN | Pattern | Image | [ROBIN: Robust and Invisible Watermarks for Diffusion Models with Adversarial Optimization](https://arxiv.org/abs/2411.03862) |
| WIND | Pattern | Image | [Hidden in the Noise: Two-Stage Robust Watermarking for Images](https://arxiv.org/abs/2412.04653) |
| SFW | Pattern | Image | [Semantic Watermarking Reinvented: Enhancing Robustness and Generation Quality with Fourier Integrity](https://arxiv.org/abs/2509.07647) |
| Gaussian-Shading | Key | Image | [Gaussian Shading: Provable Performance-Lossless Image Watermarking for Diffusion Models](https://arxiv.org/abs/2404.04956) |
| GaussMarker | Key | Image | [GaussMarker: Robust Dual-Domain Watermark for Diffusion Models](https://arxiv.org/abs/2506.11444) |
| PRC | Key | Image | [An undetectable watermark for generative image models](https://arxiv.org/abs/2410.07369) |
| SEAL | Key | Image | [SEAL: Semantic Aware Image Watermarking](https://arxiv.org/abs/2503.12172) |
| VideoShield | Key | Video | [VideoShield: Regulating Diffusion-based Video Generation Models via Watermarking](https://arxiv.org/abs/2501.14195) |
| VideoMark | Key | Video | [VideoMark: A Distortion-Free Robust Watermarking Framework for Video Diffusion Models](https://arxiv.org/abs/2504.16359) |

### Evaluation Module
#### Evaluation Pipelines

MarkDiffusion supports eight pipelines, two for detection (WatermarkedMediaDetectionPipeline and UnWatermarkedMediaDetectionPipeline), and six for quality analysis. 
## Installation

### Prerequisites: Install PyTorch

MarkDiffusion requires PyTorch. Please install it first according to your system and CUDA version:

```bash
# Visit https://pytorch.org/get-started/locally/ for the recommended command
# Example for CUDA 11.8:
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu118

# Example for CPU only:
pip install torch torchvision --index-url https://download.pytorch.org/whl/cpu
```

### Option 1: Install from PyPI (Recommended)

```bash
pip install markdiffusion
```

### Option 2: Install from Source

```bash
git clone https://github.com/THU-BPM/MarkDiffusion.git
cd MarkDiffusion
pip install -e .
```

### Requirements

- Python 3.10+
- PyTorch

*Note:* Some algorithms may require additional setup steps. Please refer to individual algorithm documentation for specific requirements.

## Quick Start

Here's a simple example to get you started with MarkDiffusion:

```python
import torch
from markdiffusion.watermark import AutoWatermark
from markdiffusion.utils import DiffusionConfig
from diffusers import StableDiffusionPipeline, DPMSolverMultistepScheduler

# Device setup
device = 'cuda' if torch.cuda.is_available() else 'cpu'

# Configure diffusion pipeline
MODEL_PATH = "stabilityai/stable-diffusion-2-1-base"
scheduler = DPMSolverMultistepScheduler.from_pretrained(MODEL_PATH, subfolder="scheduler")
pipe = StableDiffusionPipeline.from_pretrained(
    MODEL_PATH,
    scheduler=scheduler,
    torch_dtype=torch.float16 if device == "cuda" else torch.float32,
).to(device)

diffusion_config = DiffusionConfig(
    scheduler=scheduler,
    pipe=pipe,
    device=device,
    image_size=(512, 512),
    num_inference_steps=50,
    guidance_scale=7.5,
    gen_seed=42,
    inversion_type="ddim"
)

# Load watermark algorithm
watermark = AutoWatermark.load('TR', diffusion_config=diffusion_config)

# Generate watermarked media
prompt = "A beautiful sunset over the ocean"
watermarked_image = watermark.generate_watermarked_media(prompt)

# Detect watermark
detection_result = watermark.detect_watermark_in_media(watermarked_image)
print(f"Watermark detected: {detection_result}")
```

## How to Use the Toolkit

We provide extensive examples in `MarkDiffusion_demo.ipynb`.

### Generating and Detecting Watermarked Media

#### Cases for Generating and Detecting Watermarked Media

```python
import torch
from markdiffusion.watermark import AutoWatermark
from markdiffusion.utils import DiffusionConfig

# Load watermarking algorithm
mywatermark = AutoWatermark.load(
    'GS',
    diffusion_config=diffusion_config
)

# Generate watermarked image
watermarked_image = mywatermark.generate_watermarked_media(
    input_data="A beautiful landscape with a river and mountains"
)

# Visualize the watermarked image
watermarked_image.show()

# Detect watermark
detection_result = mywatermark.detect_watermark_in_media(watermarked_image)
print(detection_result)
```

### Visualizing Watermarking Mechanisms

The toolkit includes custom visualization tools that enable clear and insightful views into how different watermarking algorithms operate under various scenarios. These visualizations help demystify the algorithms' mechanisms, making them more understandable for users.

<img src="https://raw.githubusercontent.com/THU-BPM/markdiffusion/main/img/fig2_visualization_mechanism.png" alt="Watermarking Mechanism Visualization" style="zoom:40%;" />

#### Cases for Visualizing Watermarking Mechanism

```python
from markdiffusion.visualize import AutoVisualizer

# Get data for visualization
data_for_visualization = mywatermark.get_data_for_visualize(watermarked_image)

# Load Visualizer
visualizer = AutoVisualizer.load('GS',
                                data_for_visualization=data_for_visualization)

# Draw diagrams on Matplotlib canvas
fig = visualizer.visualize(rows=2, cols=2,
                          methods=['draw_watermark_bits',
                                  'draw_reconstructed_watermark_bits',
                                  'draw_inverted_latents',
                                  'draw_inverted_latents_fft'])
```

### Evaluation Pipelines

#### Cases for Evaluation

1. **Watermark Detection Pipeline**

```python
from markdiffusion.evaluation.dataset import StableDiffusionPromptsDataset
from markdiffusion.evaluation.pipelines.detection import (
    WatermarkedMediaDetectionPipeline,
    UnWatermarkedMediaDetectionPipeline,
    DetectionPipelineReturnType
)
from markdiffusion.evaluation.tools.image_editor import JPEGCompression
from markdiffusion.evaluation.tools.success_rate_calculator import DynamicThresholdSuccessRateCalculator

# Dataset
my_dataset = StableDiffusionPromptsDataset(max_samples=200)

# Set up detection pipelines
pipeline1 = WatermarkedMediaDetectionPipeline(
    dataset=my_dataset,
    media_editor_list=[JPEGCompression(quality=60)],
    show_progress=True, 
    return_type=DetectionPipelineReturnType.SCORES
)

pipeline2 = UnWatermarkedMediaDetectionPipeline(
    dataset=my_dataset,
    media_editor_list=[],
    show_progress=True, 
    return_type=DetectionPipelineReturnType.SCORES
)

# Configure detection parameters
detection_kwargs = {
    "num_inference_steps": 50,
    "guidance_scale": 1.0,
}

# Calculate success rates
calculator = DynamicThresholdSuccessRateCalculator(
    labels=labels, 
    rule=rules,
    target_fpr=target_fpr
)

results = calculator.calculate(
    pipeline1.evaluate(my_watermark, detection_kwargs=detection_kwargs),
    pipeline2.evaluate(my_watermark, detection_kwargs=detection_kwargs)
)
print(results)
```

2. **Image Quality Analysis Pipeline**

```python
from markdiffusion.evaluation.dataset import StableDiffusionPromptsDataset, MSCOCODataset
from markdiffusion.evaluation.pipelines.image_quality_analysis import (
    DirectImageQualityAnalysisPipeline,
    ReferencedImageQualityAnalysisPipeline,
    GroupImageQualityAnalysisPipeline,
    RepeatImageQualityAnalysisPipeline,
    ComparedImageQualityAnalysisPipeline,
    QualityPipelineReturnType
)
from markdiffusion.evaluation.tools.image_quality_analyzer import (
    NIQECalculator, CLIPScoreCalculator, FIDCalculator,
    InceptionScoreCalculator, LPIPSAnalyzer, PSNRAnalyzer
)

# Different quality metrics examples:

# NIQE (No-Reference Image Quality Evaluator)
if metric == 'NIQE':
    my_dataset = StableDiffusionPromptsDataset(max_samples=max_samples)
    pipeline = DirectImageQualityAnalysisPipeline(
        dataset=my_dataset,
        watermarked_image_editor_list=[],
        unwatermarked_image_editor_list=[],
        analyzers=[NIQECalculator()],
        show_progress=True,
        return_type=QualityPipelineReturnType.MEAN_SCORES
    )

# CLIP Score
elif metric == 'CLIP':
    my_dataset = MSCOCODataset(max_samples=max_samples)
    pipeline = ReferencedImageQualityAnalysisPipeline(
        dataset=my_dataset,
        watermarked_image_editor_list=[],
        unwatermarked_image_editor_list=[],
        analyzers=[CLIPScoreCalculator()],
        unwatermarked_image_source='generated',
        reference_image_source='natural',
        show_progress=True,
        return_type=QualityPipelineReturnType.MEAN_SCORES
    )

# FID (Fréchet Inception Distance)
elif metric == 'FID':
    my_dataset = MSCOCODataset(max_samples=max_samples)
    pipeline = GroupImageQualityAnalysisPipeline(
        dataset=my_dataset,
        watermarked_image_editor_list=[],
        unwatermarked_image_editor_list=[],
        analyzers=[FIDCalculator()],
        unwatermarked_image_source='generated',
        reference_image_source='natural',
        show_progress=True,
        return_type=QualityPipelineReturnType.MEAN_SCORES
    )

# IS (Inception Score)
elif metric == 'IS':
    my_dataset = StableDiffusionPromptsDataset(max_samples=max_samples)
    pipeline = GroupImageQualityAnalysisPipeline(
        dataset=my_dataset,
        watermarked_image_editor_list=[],
        unwatermarked_image_editor_list=[],
        analyzers=[InceptionScoreCalculator()],
        show_progress=True,
        return_type=QualityPipelineReturnType.MEAN_SCORES
    )

# LPIPS (Learned Perceptual Image Patch Similarity)
elif metric == 'LPIPS':
    my_dataset = StableDiffusionPromptsDataset(max_samples=10)
    pipeline = RepeatImageQualityAnalysisPipeline(
        dataset=my_dataset,
        prompt_per_image=20,
        watermarked_image_editor_list=[],
        unwatermarked_image_editor_list=[],
        analyzers=[LPIPSAnalyzer()],
        show_progress=True,
        return_type=QualityPipelineReturnType.MEAN_SCORES
    )

# PSNR (Peak Signal-to-Noise Ratio)
elif metric == 'PSNR':
    my_dataset = StableDiffusionPromptsDataset(max_samples=max_samples)
    pipeline = ComparedImageQualityAnalysisPipeline(
        dataset=my_dataset,
        watermarked_image_editor_list=[],
        unwatermarked_image_editor_list=[],
        analyzers=[PSNRAnalyzer()],
        show_progress=True,
        return_type=QualityPipelineReturnType.MEAN_SCORES
    )

# Load watermark and evaluate
my_watermark = AutoWatermark.load(
    f'{algorithm_name}',
    algorithm_config=f'config/{algorithm_name}.json',
    diffusion_config=diffusion_config
)

print(pipeline.evaluate(my_watermark))
```

3. **Video Quality Analysis Pipeline**

```python
from markdiffusion.evaluation.dataset import VBenchDataset
from markdiffusion.evaluation.pipelines.video_quality_analysis import DirectVideoQualityAnalysisPipeline
from markdiffusion.evaluation.tools.video_quality_analyzer import (
    SubjectConsistencyAnalyzer,
    MotionSmoothnessAnalyzer,
    DynamicDegreeAnalyzer,
    BackgroundConsistencyAnalyzer,
    ImagingQualityAnalyzer
)

# Load VBench dataset
my_dataset = VBenchDataset(max_samples=200, dimension=dimension)

# Initialize analyzer based on metric
if metric == 'subject_consistency':
    analyzer = SubjectConsistencyAnalyzer(device=device)
elif metric == 'motion_smoothness':
    analyzer = MotionSmoothnessAnalyzer(device=device)
elif metric == 'dynamic_degree':
    analyzer = DynamicDegreeAnalyzer(device=device)
elif metric == 'background_consistency':
    analyzer = BackgroundConsistencyAnalyzer(device=device)
elif metric == 'imaging_quality':
    analyzer = ImagingQualityAnalyzer(device=device)
else:
    raise ValueError(f'Invalid metric: {metric}. Supported metrics: 
                    subject_consistency, motion_smoothness, dynamic_degree,
                    background_consistency, imaging_quality')

# Create video quality analysis pipeline
pipeline = DirectVideoQualityAnalysisPipeline(
    dataset=my_dataset,
    watermarked_video_editor_list=[],
    unwatermarked_video_editor_list=[],
    watermarked_frame_editor_list=[],
    unwatermarked_frame_editor_list=[],
    analyzers=[analyzer],
    show_progress=True,
    return_type=QualityPipelineReturnType.MEAN_SCORES
)

print(pipeline.evaluate(my_watermark))
```

## Citation
```
@article{pan2025markdiffusion,
  title={MarkDiffusion: An Open-Source Toolkit for Generative Watermarking of Latent Diffusion Models},
  author={Pan, Leyi and Guan, Sheng and Fu, Zheyu and Si, Luyang and Wang, Zian and Hu, Xuming and King, Irwin and Yu, Philip S and Liu, Aiwei and Wen, Lijie},
  journal={arXiv preprint arXiv:2509.10569},
  year={2025}
}
```
