"""
漫画スタイルプリセット定義

多彩な漫画スタイルを定義し、それぞれに画像生成用のプロンプト修飾子と
レイアウト設定を紐付ける。
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional


@dataclass
class StylePreset:
    """漫画スタイルのプリセット"""
    id: str
    name: str
    description: str
    category: str
    icon: str

    # 画像生成用のプロンプト修飾子
    prompt_prefix: str  # プロンプトの前に付加
    prompt_suffix: str  # プロンプトの後に付加
    negative_prompt: str  # ネガティブプロンプト

    # レイアウト設定
    default_panels: int  # デフォルトのコマ数
    panel_style: str  # コマの枠線スタイル (solid, rounded, none, irregular)
    gutter_width: int  # コマ間の余白（px）
    background_color: str  # 背景色

    # フキダシ設定
    speech_bubble_style: str  # normal, cloud, explosion, whisper, thought
    font_family: str  # フォントファミリー

    # 特殊効果
    effects: List[str] = field(default_factory=list)  # スクリーントーン、集中線など


# ========================================
# 日本漫画系スタイル
# ========================================

YONKOMA = StylePreset(
    id="yonkoma",
    name="4コマ漫画",
    description="起承転結の王道4コマ形式",
    category="日本漫画",
    icon="📰",
    prompt_prefix="4-koma manga style, simple clean lineart, ",
    prompt_suffix=", black and white manga, screentone shading",
    negative_prompt="realistic, photo, 3d render, complex background",
    default_panels=4,
    panel_style="solid",
    gutter_width=8,
    background_color="#FFFFFF",
    speech_bubble_style="normal",
    font_family="Noto Sans JP",
    effects=["screentone"],
)

SHONEN = StylePreset(
    id="shonen",
    name="少年漫画風",
    description="ダイナミックな構図と迫力のある表現",
    category="日本漫画",
    icon="⚡",
    prompt_prefix="shonen manga style, dynamic action pose, speed lines, ",
    prompt_suffix=", bold lineart, high contrast, dramatic lighting",
    negative_prompt="static, boring composition, pastel colors",
    default_panels=4,
    panel_style="irregular",
    gutter_width=4,
    background_color="#FFFFFF",
    speech_bubble_style="explosion",
    font_family="Noto Sans JP",
    effects=["speed_lines", "impact_frame", "screentone"],
)

SHOJO = StylePreset(
    id="shojo",
    name="少女漫画風",
    description="繊細な線と華やかな演出",
    category="日本漫画",
    icon="🌸",
    prompt_prefix="shojo manga style, delicate lineart, sparkles, flowers, ",
    prompt_suffix=", soft shading, beautiful eyes, romantic atmosphere",
    negative_prompt="rough lineart, dark atmosphere, violent",
    default_panels=4,
    panel_style="rounded",
    gutter_width=12,
    background_color="#FFF5F5",
    speech_bubble_style="cloud",
    font_family="Noto Serif JP",
    effects=["sparkles", "flower_overlay", "soft_glow"],
)

SEINEN = StylePreset(
    id="seinen",
    name="青年漫画風",
    description="リアルな描写と深みのある表現",
    category="日本漫画",
    icon="📖",
    prompt_prefix="seinen manga style, detailed realistic lineart, mature theme, ",
    prompt_suffix=", cinematic composition, dramatic shadows",
    negative_prompt="childish, cute, simple",
    default_panels=6,
    panel_style="solid",
    gutter_width=6,
    background_color="#F5F5F5",
    speech_bubble_style="normal",
    font_family="Noto Sans JP",
    effects=["crosshatch", "heavy_shadows"],
)

GIJINKA_YURU = StylePreset(
    id="yuru",
    name="ゆるふわ日常系",
    description="かわいいデフォルメとほのぼの表現",
    category="日本漫画",
    icon="🐱",
    prompt_prefix="cute chibi style, simple round shapes, soft pastel colors, ",
    prompt_suffix=", kawaii, cozy atmosphere, simple background",
    negative_prompt="realistic, detailed, sharp edges, dark",
    default_panels=4,
    panel_style="rounded",
    gutter_width=16,
    background_color="#FFFAF0",
    speech_bubble_style="cloud",
    font_family="Rounded Mplus 1c",
    effects=["soft_glow", "pastel_overlay"],
)

HORROR = StylePreset(
    id="horror",
    name="ホラー漫画風",
    description="不気味さと恐怖を演出",
    category="日本漫画",
    icon="👻",
    prompt_prefix="horror manga style, unsettling atmosphere, heavy shadows, ",
    prompt_suffix=", scratchy lineart, high contrast, eerie lighting",
    negative_prompt="bright, cheerful, colorful, cute",
    default_panels=4,
    panel_style="irregular",
    gutter_width=2,
    background_color="#1A1A1A",
    speech_bubble_style="whisper",
    font_family="Noto Sans JP",
    effects=["noise", "vignette", "scratch_overlay"],
)

# ========================================
# Web漫画・縦読み系スタイル
# ========================================

WEBTOON = StylePreset(
    id="webtoon",
    name="Webtoon風",
    description="フルカラー縦スクロール形式",
    category="Web漫画",
    icon="📱",
    prompt_prefix="webtoon style, full color digital art, clean cel shading, ",
    prompt_suffix=", vibrant colors, smooth gradients, modern illustration",
    negative_prompt="black and white, sketchy, traditional media",
    default_panels=4,
    panel_style="none",
    gutter_width=24,
    background_color="#FFFFFF",
    speech_bubble_style="normal",
    font_family="Noto Sans JP",
    effects=["soft_shadow", "gradient_bg"],
)

SNS_MANGA = StylePreset(
    id="sns",
    name="SNS漫画風",
    description="シンプルで読みやすい1ページ完結型",
    category="Web漫画",
    icon="📲",
    prompt_prefix="simple manga style for social media, bold outlines, ",
    prompt_suffix=", easy to read, clear composition, flat colors",
    negative_prompt="complex, detailed background, realistic",
    default_panels=4,
    panel_style="rounded",
    gutter_width=12,
    background_color="#FFFFFF",
    speech_bubble_style="normal",
    font_family="Noto Sans JP",
    effects=[],
)

ESSAY_MANGA = StylePreset(
    id="essay",
    name="エッセイ漫画風",
    description="実体験を漫画化するスタイル",
    category="Web漫画",
    icon="✍️",
    prompt_prefix="essay manga style, casual illustration, personal diary feel, ",
    prompt_suffix=", warm colors, friendly character design, relatable",
    negative_prompt="fantasy, unrealistic, dark",
    default_panels=4,
    panel_style="solid",
    gutter_width=10,
    background_color="#FFFEF5",
    speech_bubble_style="normal",
    font_family="Noto Sans JP",
    effects=["handwritten_feel"],
)

# ========================================
# 海外コミック系スタイル
# ========================================

AMERICAN_COMIC = StylePreset(
    id="american",
    name="アメコミ風",
    description="ヒーローコミック風の力強い表現",
    category="海外コミック",
    icon="🦸",
    prompt_prefix="american comic book style, bold colors, muscular figures, ",
    prompt_suffix=", dynamic poses, halftone dots, superhero aesthetic",
    negative_prompt="anime, manga, cute, chibi",
    default_panels=4,
    panel_style="solid",
    gutter_width=4,
    background_color="#FFFFFF",
    speech_bubble_style="explosion",
    font_family="Comic Sans MS",
    effects=["halftone", "bold_outline"],
)

BANDE_DESSINEE = StylePreset(
    id="bd",
    name="バンドデシネ風",
    description="ヨーロッパ風の芸術的なコミック",
    category="海外コミック",
    icon="🎨",
    prompt_prefix="bande dessinee style, European comic, artistic linework, ",
    prompt_suffix=", watercolor feel, detailed backgrounds, elegant composition",
    negative_prompt="anime, simple, childish",
    default_panels=6,
    panel_style="solid",
    gutter_width=8,
    background_color="#FAF8F5",
    speech_bubble_style="normal",
    font_family="Georgia",
    effects=["watercolor_texture"],
)

MANHWA = StylePreset(
    id="manhwa",
    name="マンファ風",
    description="韓国漫画スタイル",
    category="海外コミック",
    icon="🇰🇷",
    prompt_prefix="manhwa style, Korean webtoon, sharp features, ",
    prompt_suffix=", detailed eyes, modern fashion, full color",
    negative_prompt="chibi, super deformed, black and white",
    default_panels=4,
    panel_style="none",
    gutter_width=20,
    background_color="#FFFFFF",
    speech_bubble_style="normal",
    font_family="Noto Sans KR",
    effects=["soft_glow", "lens_flare"],
)

# ========================================
# アート・実験系スタイル
# ========================================

PIXEL_ART = StylePreset(
    id="pixel",
    name="ピクセルアート風",
    description="レトロゲーム風のドット絵表現",
    category="アート・実験系",
    icon="👾",
    prompt_prefix="pixel art style, 16-bit game graphics, limited color palette, ",
    prompt_suffix=", retro game aesthetic, chunky pixels, nostalgic",
    negative_prompt="smooth, realistic, high resolution, gradient",
    default_panels=4,
    panel_style="solid",
    gutter_width=4,
    background_color="#2C2C2C",
    speech_bubble_style="normal",
    font_family="Press Start 2P",
    effects=["pixelate", "limited_palette"],
)

WATERCOLOR = StylePreset(
    id="watercolor",
    name="水彩画風",
    description="柔らかい水彩タッチの表現",
    category="アート・実験系",
    icon="🎨",
    prompt_prefix="watercolor illustration style, soft edges, paint bleeding, ",
    prompt_suffix=", artistic, traditional media feel, muted colors",
    negative_prompt="digital, sharp edges, flat colors",
    default_panels=4,
    panel_style="none",
    gutter_width=16,
    background_color="#FFFEF8",
    speech_bubble_style="cloud",
    font_family="Noto Serif JP",
    effects=["watercolor_texture", "paper_texture"],
)

UKIYOE = StylePreset(
    id="ukiyoe",
    name="浮世絵風",
    description="日本の伝統的な木版画スタイル",
    category="アート・実験系",
    icon="🗾",
    prompt_prefix="ukiyo-e style, Japanese woodblock print, flat colors, ",
    prompt_suffix=", bold outlines, traditional Japanese art, wave patterns",
    negative_prompt="3d, realistic shading, modern",
    default_panels=3,
    panel_style="solid",
    gutter_width=12,
    background_color="#F5E6D3",
    speech_bubble_style="normal",
    font_family="Noto Serif JP",
    effects=["woodblock_texture", "limited_palette"],
)

NOIR = StylePreset(
    id="noir",
    name="フィルムノワール風",
    description="モノクロの影と光のコントラスト",
    category="アート・実験系",
    icon="🎬",
    prompt_prefix="film noir style, high contrast black and white, dramatic shadows, ",
    prompt_suffix=", cinematic lighting, detective story aesthetic, moody",
    negative_prompt="colorful, bright, cheerful, flat lighting",
    default_panels=4,
    panel_style="solid",
    gutter_width=6,
    background_color="#000000",
    speech_bubble_style="whisper",
    font_family="Courier New",
    effects=["high_contrast", "vignette", "film_grain"],
)

# ========================================
# 教育・ビジネス系スタイル
# ========================================

INFOGRAPHIC = StylePreset(
    id="infographic",
    name="インフォグラフィック風",
    description="情報を視覚的に伝えるスタイル",
    category="教育・ビジネス",
    icon="📊",
    prompt_prefix="infographic style, clean design, icon-based illustration, ",
    prompt_suffix=", flat design, professional, easy to understand",
    negative_prompt="complex, artistic, emotional",
    default_panels=4,
    panel_style="rounded",
    gutter_width=16,
    background_color="#F7F9FC",
    speech_bubble_style="normal",
    font_family="Noto Sans JP",
    effects=["flat_design"],
)

EDUCATIONAL = StylePreset(
    id="educational",
    name="学習漫画風",
    description="わかりやすい解説漫画スタイル",
    category="教育・ビジネス",
    icon="📚",
    prompt_prefix="educational manga style, clear character design, informative, ",
    prompt_suffix=", friendly illustration, easy to follow, textbook style",
    negative_prompt="complex, dark, abstract",
    default_panels=4,
    panel_style="solid",
    gutter_width=10,
    background_color="#FFFFFF",
    speech_bubble_style="normal",
    font_family="Noto Sans JP",
    effects=[],
)

CORPORATE = StylePreset(
    id="corporate",
    name="ビジネス漫画風",
    description="企業向けのクリーンなスタイル",
    category="教育・ビジネス",
    icon="💼",
    prompt_prefix="corporate illustration style, professional, clean design, ",
    prompt_suffix=", modern business aesthetic, minimal, sophisticated",
    negative_prompt="childish, colorful, fantasy",
    default_panels=4,
    panel_style="solid",
    gutter_width=12,
    background_color="#FFFFFF",
    speech_bubble_style="normal",
    font_family="Noto Sans JP",
    effects=[],
)

# ========================================
# スタイル辞書
# ========================================

STYLE_PRESETS: Dict[str, StylePreset] = {
    # 日本漫画
    "yonkoma": YONKOMA,
    "shonen": SHONEN,
    "shojo": SHOJO,
    "seinen": SEINEN,
    "yuru": GIJINKA_YURU,
    "horror": HORROR,
    # Web漫画
    "webtoon": WEBTOON,
    "sns": SNS_MANGA,
    "essay": ESSAY_MANGA,
    # 海外コミック
    "american": AMERICAN_COMIC,
    "bd": BANDE_DESSINEE,
    "manhwa": MANHWA,
    # アート・実験系
    "pixel": PIXEL_ART,
    "watercolor": WATERCOLOR,
    "ukiyoe": UKIYOE,
    "noir": NOIR,
    # 教育・ビジネス
    "infographic": INFOGRAPHIC,
    "educational": EDUCATIONAL,
    "corporate": CORPORATE,
}


def get_style(style_id: str) -> Optional[StylePreset]:
    """IDからスタイルを取得"""
    return STYLE_PRESETS.get(style_id)


def list_styles_by_category() -> Dict[str, List[StylePreset]]:
    """カテゴリ別にスタイルを整理して返す"""
    categories: Dict[str, List[StylePreset]] = {}
    for style in STYLE_PRESETS.values():
        if style.category not in categories:
            categories[style.category] = []
        categories[style.category].append(style)
    return categories
