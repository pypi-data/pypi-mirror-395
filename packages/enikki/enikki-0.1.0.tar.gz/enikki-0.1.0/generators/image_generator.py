"""
画像生成モジュール

Gemini 3 Pro Image を使用してマンガ画像を一括生成する。
"""

import io
import os
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Optional

from PIL import Image

from styles.presets import StylePreset
from generators.script_generator import MangaScript


@dataclass
class GeneratedManga:
    """生成されたマンガ画像"""
    image: Image.Image
    prompt_used: str


class ImageGeneratorBase(ABC):
    """画像生成の基底クラス"""

    @abstractmethod
    def generate_manga(
        self,
        script: MangaScript,
        style: StylePreset,
        character_image: Optional[Image.Image] = None,
        width: int = 1080,
        height: int = 1920,
        additional_instruction: str = "",
    ) -> GeneratedManga:
        """マンガ全体を1枚の画像として生成"""
        pass

    def _build_manga_prompt(self, script: MangaScript, style: StylePreset, has_character_image: bool = False, additional_instruction: str = "") -> str:
        """マンガ全体を生成するためのプロンプトを構築"""
        panel_descriptions = []
        for i, panel in enumerate(script.panels, 1):
            panel_descriptions.append(
                f"Panel {i}: {panel.visual_prompt}. "
                f"Speech bubble text: \"{panel.dialogue}\""
            )

        panels_text = "\n".join(panel_descriptions)

        # キャラクター画像がある場合の追加指示
        character_instruction = ""
        if has_character_image:
            character_instruction = """
## ⚠️ CRITICAL: REFERENCE CHARACTER IMAGE PROVIDED ⚠️
A reference photo/image of the main character is attached. This is the HIGHEST PRIORITY requirement:

### MANDATORY - Character Appearance (from reference image):
1. **FACE**: Copy the EXACT face from the reference - same face shape, eye shape, eye size, nose, mouth, jawline
2. **SKIN**: Match the exact skin tone from the reference image
3. **HAIR**: Use the EXACT hairstyle, hair color, and hair length from the reference
4. **FEATURES**: Preserve all distinguishing features (glasses, facial hair, moles, etc.)

### How to use the reference:
- Study the reference image carefully before drawing
- The character in EVERY panel must look like the SAME PERSON as in the reference
- If someone saw the reference photo and the manga, they should immediately recognize it's the same person
- Adapt to manga/illustration style but keep the person RECOGNIZABLE

### DO NOT:
- Invent a different character design
- Change the hair color or style
- Modify facial features significantly
- Use a generic anime/manga face instead of the reference
"""

        prompt = f"""Create a {len(script.panels)}-panel Japanese manga page.
{character_instruction}
## CHARACTER CONSISTENCY ACROSS PANELS
The SAME character(s) MUST appear in EVERY panel with:
- IDENTICAL face shape, eye shape, eye color (matching reference if provided)
- IDENTICAL hairstyle, hair color, hair length (matching reference if provided)
- IDENTICAL clothing, accessories
- Only facial EXPRESSION may change between panels
- Think of this as frames from an animation - the character design must be 100% consistent

## Style
- Art style: {style.prompt_prefix.strip()}
- Title: "{script.title}"

## PANEL LAYOUT - JAPANESE MANGA STYLE
Create dynamic, professional Japanese manga panel layouts:
- READING ORDER: Right-to-left, top-to-bottom (Japanese style)
- Panel 1 should be at TOP-RIGHT, final panel at BOTTOM-LEFT
- Flow naturally from upper-right corner to lower-left corner
- Vary panel sizes based on importance (key moments get larger panels)
- Use diagonal lines and irregular shapes for dynamic panels
- Panels can overlap slightly or break borders for dramatic effect
- Mix close-up shots with wide shots
- Some panels can be tall and narrow, others wide and short
- Add speed lines, emotion effects, and screen tones where appropriate
- Panel gutters (white space between panels) should be consistent
- NOT a boring grid - make it visually interesting like real Japanese manga

## Speech Bubbles
- Traditional manga speech bubbles (oval/rounded shapes)
- Thought bubbles should be cloud-shaped
- Shout/exclamation bubbles should be spiky
- VERTICAL TEXT: Japanese text must be written vertically (top to bottom, right to left)
- Text flows from top to bottom within each bubble
- Position bubbles naturally near the speaking character

## Panel Descriptions
{panels_text}

## Final Checklist
Before generating, verify:
1. If reference image provided: Character matches the reference person's appearance
2. Character face is EXACTLY the same in all panels
3. Character hair is EXACTLY the same in all panels
4. Character clothes are EXACTLY the same in all panels
5. Panel layout is dynamic and manga-style (NOT a simple grid)
6. Speech bubbles contain the exact Japanese text provided

{style.prompt_suffix}"""

        # 追加指示があれば追加
        if additional_instruction:
            prompt += f"\n\n## Additional Instructions\n{additional_instruction}"

        return prompt


class GeminiImageGenerator(ImageGeneratorBase):
    """
    Gemini 3 Pro Image を使用した画像生成
    """

    def __init__(self, api_key: str):
        """
        Args:
            api_key: Google AI API キー
        """
        from google import genai
        self.client = genai.Client(api_key=api_key)

    def generate_manga(
        self,
        script: MangaScript,
        style: StylePreset,
        character_image: Optional[Image.Image] = None,
        width: int = 1080,
        height: int = 1920,
        additional_instruction: str = "",
    ) -> GeneratedManga:
        """Gemini 3 Pro Imageでマンガ全体を1枚の画像として生成"""
        from google.genai import types

        prompt = self._build_manga_prompt(script, style, character_image is not None, additional_instruction)

        # Gemini APIがサポートするアスペクト比に変換
        # サポート: 1:1, 3:4, 4:3, 9:16, 16:9
        ratio = width / height
        if ratio > 1.5:  # 横長 (16:9 = 1.78)
            aspect_ratio = "16:9"
        elif ratio > 1.1:  # やや横長 (4:3 = 1.33)
            aspect_ratio = "4:3"
        elif ratio > 0.9:  # ほぼ正方形
            aspect_ratio = "1:1"
        elif ratio > 0.65:  # やや縦長 (3:4 = 0.75)
            aspect_ratio = "3:4"
        else:  # 縦長 (9:16 = 0.56)
            aspect_ratio = "9:16"

        # コンテンツを構築（キャラクター画像がある場合は含める）
        if character_image:
            # PIL ImageをBytesに変換
            img_byte_arr = io.BytesIO()
            character_image.save(img_byte_arr, format='PNG')
            img_byte_arr.seek(0)

            contents = [
                types.Part.from_bytes(data=img_byte_arr.getvalue(), mime_type="image/png"),
                prompt,
            ]
        else:
            contents = prompt

        response = self.client.models.generate_content(
            model="gemini-3-pro-image-preview",
            contents=contents,
            config=types.GenerateContentConfig(
                response_modalities=["TEXT", "IMAGE"],
                image_config=types.ImageConfig(
                    aspect_ratio=aspect_ratio,
                ),
            ),
        )

        # レスポンスから画像を抽出
        for part in response.parts:
            if part.inline_data is not None:
                # inline_dataから直接バイトデータを取得してPIL Imageに変換
                image_bytes = part.inline_data.data
                pil_image = Image.open(io.BytesIO(image_bytes))
                # アスペクト比を保持しながらリサイズ（潰れ防止）
                # Geminiが返した画像のアスペクト比を維持
                orig_width, orig_height = pil_image.size
                orig_aspect = orig_width / orig_height
                target_aspect = width / height

                if abs(orig_aspect - target_aspect) < 0.1:
                    # アスペクト比がほぼ同じならそのままリサイズ
                    pil_image = pil_image.resize((width, height), Image.Resampling.LANCZOS)
                else:
                    # アスペクト比が異なる場合は、アスペクト比を保持してリサイズ
                    # 指定サイズに収まるようにスケール
                    scale = min(width / orig_width, height / orig_height)
                    new_width = int(orig_width * scale)
                    new_height = int(orig_height * scale)
                    pil_image = pil_image.resize((new_width, new_height), Image.Resampling.LANCZOS)

                return GeneratedManga(
                    image=pil_image,
                    prompt_used=prompt,
                )

        raise RuntimeError("Gemini did not return an image")


class MockImageGenerator(ImageGeneratorBase):
    """テスト・デモ用のモック画像生成クラス"""

    def __init__(self, placeholder_color: str = "#CCCCCC"):
        self.placeholder_color = placeholder_color

    def generate_manga(
        self,
        script: MangaScript,
        style: StylePreset,
        character_image: Optional[Image.Image] = None,
        width: int = 1080,
        height: int = 1920,
        additional_instruction: str = "",
    ) -> GeneratedManga:
        """プレースホルダーマンガ画像を生成"""
        from PIL import ImageDraw, ImageFont

        # プレースホルダー画像を作成
        image = Image.new("RGB", (width, height), self.placeholder_color)
        draw = ImageDraw.Draw(image)

        try:
            font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 36)
            small_font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 24)
        except OSError:
            font = ImageFont.load_default()
            small_font = font

        # タイトル
        title_text = script.title
        bbox = draw.textbbox((0, 0), title_text, font=font)
        text_width = bbox[2] - bbox[0]
        draw.text(((width - text_width) // 2, 20), title_text, fill="#333333", font=font)

        # 各パネルのプレースホルダー
        panel_count = len(script.panels)
        panel_height = (height - 100) // panel_count
        y = 80

        for i, panel in enumerate(script.panels):
            # パネル枠
            draw.rectangle(
                [20, y, width - 20, y + panel_height - 10],
                outline="#666666",
                width=2,
            )
            # パネル番号
            text = f"Panel {i + 1}"
            bbox = draw.textbbox((0, 0), text, font=small_font)
            text_width = bbox[2] - bbox[0]
            draw.text(
                ((width - text_width) // 2, y + panel_height // 2 - 20),
                text,
                fill="#666666",
                font=small_font,
            )
            # セリフ
            dialogue = panel.dialogue[:20] + "..." if len(panel.dialogue) > 20 else panel.dialogue
            bbox = draw.textbbox((0, 0), dialogue, font=small_font)
            text_width = bbox[2] - bbox[0]
            draw.text(
                ((width - text_width) // 2, y + panel_height // 2 + 10),
                dialogue,
                fill="#999999",
                font=small_font,
            )
            y += panel_height

        return GeneratedManga(
            image=image,
            prompt_used=self._build_manga_prompt(script, style),
        )


def create_image_generator(
    backend: str = "mock",
    api_key: Optional[str] = None,
) -> ImageGeneratorBase:
    """
    画像生成バックエンドを作成

    Args:
        backend: "gemini" or "mock"
        api_key: APIキー

    Returns:
        ImageGeneratorBase: 画像生成クラスのインスタンス
    """
    if backend == "gemini":
        if not api_key:
            api_key = os.environ.get("GOOGLE_API_KEY")
        if not api_key:
            raise ValueError("GOOGLE_API_KEY is required for Gemini backend")
        return GeminiImageGenerator(api_key)

    elif backend == "mock":
        return MockImageGenerator()

    else:
        raise ValueError(f"Unknown backend: {backend}. Use 'gemini' or 'mock'.")
