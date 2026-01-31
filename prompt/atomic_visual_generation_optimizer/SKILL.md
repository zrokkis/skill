---
name: atomic_visual_generation_optimizer
description: 使用 Atomic Prompting 框架（生物体、分子、原子、参数）进行高精度的 AI 绘画提示词构建。特别适用于 Midjourney、Stable Diffusion 等图像生成任务。
---

# Atomic 视觉原子化技能 (Atomic Image Skill)

本技能通过“由大到小”的聚焦过程，解决了 AI 绘画中常见的“画面容易崩坏”或“细节缺失”的问题。它强迫用户从整体构图思考到微观纹理，确保每一像素都有据可依。

## 执行流程 (Optimization Workflow)

在需要生成高质量、细节丰富的 AI 图像时，请应用以下 Atomic 逻辑：

### 1. 生物体 (Organism) - 构图定调
- **核心动作**：用广角镜头看世界。
- **操作指南**：描述画面的主体和整体氛围。“一个孤独的宇航员站在火星表面，风格压抑。”

### 2. 分子 (Molecule) - 环境搭建
- **核心动作**：用中景镜头填充内容。
- **操作指南**：添加背景元素和次要物体。“背景是巨大的红色沙尘暴，宇航员手持一面破损的旗帜。”

### 3. 原子 (Atom) - 质感雕琢
- **核心动作**：用微距镜头观察纹理。
- **操作指南**：描述材质、光泽和微小瑕疵。“宇航服上有划痕和灰尘，头盔面罩反射出沙尘暴的漩涡，光线有着颗粒感。”

### 4. 参数 (Parameters) - 渲染指令
- **核心动作**：给显卡下达指令。
- **操作指南**：指定具体的模型参数。“--ar 16:9 --v 6.0 --style raw --stylize 250”。

---

## 优化示例 (Standard Template)

**初始需求**：“画一只猫。”

**Atomic 优化后**：
- **[Organism]**：一只坐在窗台上的英国短毛猫，午后阳光风格。
- **[Molecule]**：窗外是模糊的巴黎街道，窗台上有一盆绿植和一本打开的书。
- **[Atom]**：猫咪蓝色的眼睛清晰透亮，胡须在阳光下发光，毛发呈现出蓬松的丝绒质感，书页上有细微的折痕。
- **[Parameters]**：8k resolution, cinematic lighting, photorealistic, depth of field, --ar 3:4

