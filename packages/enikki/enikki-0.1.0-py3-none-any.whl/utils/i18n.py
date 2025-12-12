"""
Internationalization (i18n) module for enikki

Provides multi-language support with English as default.
"""

from typing import Optional

# Current language setting
_current_lang: str = "en"


def set_language(lang: str) -> None:
    """Set the current language"""
    global _current_lang
    if lang in MESSAGES:
        _current_lang = lang
    else:
        _current_lang = "en"


def get_language() -> str:
    """Get the current language"""
    return _current_lang


def t(key: str) -> str:
    """Translate a message key to the current language"""
    lang_messages = MESSAGES.get(_current_lang, MESSAGES["en"])
    return lang_messages.get(key, MESSAGES["en"].get(key, key))


# Message definitions
MESSAGES = {
    "en": {
        # App description
        "app_help": "enikki: Generate picture-diary style manga from text",
        "app_welcome_title": "enikki",
        "app_welcome_subtitle": "Generate picture-diary style manga from text",

        # Commands
        "cmd_run_help": "Generate manga in interactive mode",
        "cmd_run_desc": "Enter story and style interactively, and AI generates manga.\n\nSet GOOGLE_API_KEY environment variable or create config.toml first.",
        "cmd_quick_help": "Generate manga in quick mode",
        "cmd_quick_desc": "Generate manga with command line arguments only.\nUseful when you want to skip the interactive UI.",
        "cmd_quick_example": "enikki quick \"A story about meeting a strange customer at a cafe\" --style essay --panels 4",
        "cmd_styles_help": "Show available styles",
        "cmd_version_help": "Show version info",

        # Options
        "opt_config": "Path to config file (default: config.toml)",
        "opt_character": "Character image file",
        "opt_output": "Output file path (auto-generated if omitted)",
        "opt_backend": "Image generation backend (gemini, mock)",
        "opt_dry_run": "Skip actual image generation and use mock image",
        "opt_style": "Style ID (yonkoma, shonen, shojo, webtoon, etc.)",
        "opt_panels": "Number of panels",
        "opt_ratio": "Aspect ratio (9:16, 1:1, 16:9, etc.)",
        "opt_story": "Story concept",

        # Interactive prompts
        "select_style": "Which style would you like for your manga?",
        "select_genre": "First, what genre is it?",
        "input_title": "Enter a title (leave empty for auto-generation):",
        "input_story_header": "Tell me about your manga",
        "input_story_hint": "Write a brief story concept.",
        "input_story_example": 'Example: "A story about meeting a strange customer at a cafe"',
        "input_story_prompt": "What's the story?",
        "select_ratio": "Select output size (aspect ratio)",
        "select_panels": "Select number of panels (recommended for {style}: {count} panels)",
        "select_character": "Would you like to specify a character image?",
        "character_use_default": "Use default: {filename}",
        "character_select_other": "Select another image",
        "character_none": "Don't use",
        "input_character_path": "Enter character image path:",

        # Genres
        "genre_daily": "Daily life / Essay (real experiences, diary)",
        "genre_comedy": "Comedy / Gag",
        "genre_action": "Action / Battle",
        "genre_romance": "Romance / Rom-com",
        "genre_horror": "Horror / Suspense",
        "genre_sf": "Sci-Fi / Fantasy",
        "genre_educational": "Educational / Tutorial",
        "genre_other": "Other",

        # Aspect ratios
        "ratio_9_16": "9:16 (Portrait - for SNS stories)",
        "ratio_3_4": "3:4 (Portrait - for Instagram)",
        "ratio_1_1": "1:1 (Square - versatile)",
        "ratio_4_3": "4:3 (Landscape - for presentations)",
        "ratio_16_9": "16:9 (Landscape - for YouTube)",

        # Panel counts
        "panels_1": "1 panel (single illustration)",
        "panels_2": "2 panels",
        "panels_3": "3 panels",
        "panels_4": "4 panels (classic)",
        "panels_6": "6 panels",
        "panels_8": "8 panels (long form)",

        # Config summary
        "config_summary_title": "Generation Settings",
        "config_title": "Title",
        "config_style": "Style",
        "config_ratio": "Aspect Ratio",
        "config_panels": "Panels",
        "config_character": "Character Image",
        "config_output": "Output",
        "config_none": "None",
        "config_story_concept": "Story Concept:",
        "confirm_generate": "Generate manga with these settings?",

        # Generation steps
        "step1_title": "Step 1: Script Generation",
        "step1_generating": "Generating script...",
        "step1_complete": "Script generated!",
        "step1_panel_title": "Panel {num}",
        "step1_visual": "Visual:",
        "step1_dialogue": "Dialogue:",
        "step1_emotion": "Emotion: {emotion} / Angle: {angle}",
        "step1_confirm": "Is this script OK?",
        "step1_ok": "OK, proceed to image generation",
        "step1_retry": "Add instructions and regenerate",
        "step1_back": "Go back to settings",
        "step1_quit": "Quit",
        "step1_additional": "Enter additional instructions:",
        "step1_multiline_hint": "(Multi-line input. Press Esc then Enter to confirm)",

        "step2_title": "Step 2: Manga Image Generation",
        "step2_generating": "Generating manga... (this may take a while)",
        "step2_complete": "Manga generated!",
        "step2_preview": "Preview: {path}",
        "step2_confirm": "Is this manga OK?",
        "step2_ok": "OK, save and finish",
        "step2_retry": "Add instructions and regenerate",
        "step2_style": "Regenerate with different style",
        "step2_back": "Go back to script",
        "step2_quit": "Quit (don't save)",
        "step2_additional": "Enter additional instructions for the image:",
        "step2_style_changed": "Style changed: {icon} {name}",

        "step3_title": "Step 3: Save",
        "step3_complete": "Manga saved!",
        "step3_output_title": "Title: {title}",
        "step3_output_path": "Output: {path}",

        # Status messages
        "going_back_settings": "Going back to settings.",
        "going_back_script": "Going back to script.",
        "regenerating_script": "Regenerating script",
        "quitting": "Quitting.",
        "cancelled": "Cancelled.",
        "interrupted": "Interrupted.",
        "additional_instruction": "Additional instruction: {text}",

        # Errors
        "error_unknown_style": "Error: Unknown style '{style}'",
        "error_available_styles": "Available styles: {styles}",

        # Style categories
        "category_japanese": "Japanese Manga",
        "category_web": "Web Comics",
        "category_international": "International Comics",
        "category_art": "Art / Experimental",
        "category_business": "Education / Business",

        # Untitled
        "untitled": "Untitled Manga",
    },

    "ja": {
        # App description
        "app_help": "enikki: テキスト対話から絵日記風マンガを生成するツール",
        "app_welcome_title": "enikki",
        "app_welcome_subtitle": "テキスト対話から絵日記風マンガを生成するツール",

        # Commands
        "cmd_run_help": "インタラクティブモードでマンガを生成",
        "cmd_run_desc": "対話形式でストーリーやスタイルを入力し、AIがマンガを生成します。\n\n事前に環境変数 GOOGLE_API_KEY を設定するか、config.toml を作成してください。",
        "cmd_quick_help": "クイックモードでマンガを生成",
        "cmd_quick_desc": "コマンドライン引数だけでマンガを生成します。\n対話UIをスキップしたい場合に便利です。",
        "cmd_quick_example": "enikki quick \"今日カフェで変な客に遭遇した話\" --style essay --panels 4",
        "cmd_styles_help": "利用可能なスタイル一覧を表示",
        "cmd_version_help": "バージョン情報を表示",

        # Options
        "opt_config": "設定ファイルのパス（デフォルト: config.toml）",
        "opt_character": "キャラクター画像ファイル",
        "opt_output": "出力ファイルパス（省略時は日時ベースで自動生成）",
        "opt_backend": "画像生成バックエンド (gemini, mock)",
        "opt_dry_run": "実際の画像生成をスキップしてモック画像を使用",
        "opt_style": "スタイルID (yonkoma, shonen, shojo, webtoon, etc.)",
        "opt_panels": "コマ数",
        "opt_ratio": "アスペクト比 (9:16, 1:1, 16:9, etc.)",
        "opt_story": "ストーリーの概要",

        # Interactive prompts
        "select_style": "どのスタイルでマンガを作りますか？",
        "select_genre": "まず、どんなジャンルですか？",
        "input_title": "タイトルを入力してください（空欄で自動生成）:",
        "input_story_header": "マンガの内容を教えてください",
        "input_story_hint": "ストーリーの概要を自由に書いてください。",
        "input_story_example": "例: 「今日カフェで変な客に遭遇した話」「猫が箱に入りたがる理由を解説」",
        "input_story_prompt": "どんな話ですか？",
        "select_ratio": "出力サイズ（アスペクト比）を選んでください",
        "select_panels": "コマ数を選んでください（{style}の推奨: {count}コマ）",
        "select_character": "キャラクター画像を指定しますか？",
        "character_use_default": "デフォルトを使用: {filename}",
        "character_select_other": "別の画像を指定",
        "character_none": "使用しない",
        "input_character_path": "キャラクター画像のパスを入力:",

        # Genres
        "genre_daily": "日常・エッセイ（実体験、日記など）",
        "genre_comedy": "コメディ・ギャグ",
        "genre_action": "アクション・バトル",
        "genre_romance": "恋愛・ラブコメ",
        "genre_horror": "ホラー・サスペンス",
        "genre_sf": "SF・ファンタジー",
        "genre_educational": "解説・教育系",
        "genre_other": "その他",

        # Aspect ratios
        "ratio_9_16": "9:16 (縦長・SNSストーリー向け)",
        "ratio_3_4": "3:4 (縦長・Instagram向け)",
        "ratio_1_1": "1:1 (正方形・汎用)",
        "ratio_4_3": "4:3 (横長・プレゼン向け)",
        "ratio_16_9": "16:9 (横長・YouTube向け)",

        # Panel counts
        "panels_1": "1コマ（一枚絵）",
        "panels_2": "2コマ",
        "panels_3": "3コマ",
        "panels_4": "4コマ（定番）",
        "panels_6": "6コマ",
        "panels_8": "8コマ（長編）",

        # Config summary
        "config_summary_title": "生成設定",
        "config_title": "タイトル",
        "config_style": "スタイル",
        "config_ratio": "アスペクト比",
        "config_panels": "コマ数",
        "config_character": "キャラクター画像",
        "config_output": "出力先",
        "config_none": "なし",
        "config_story_concept": "ストーリー概要:",
        "confirm_generate": "この設定でマンガを生成しますか？",

        # Generation steps
        "step1_title": "Step 1: 脚本生成",
        "step1_generating": "脚本を生成中...",
        "step1_complete": "脚本生成完了！",
        "step1_panel_title": "コマ {num}",
        "step1_visual": "視覚描写:",
        "step1_dialogue": "セリフ:",
        "step1_emotion": "感情: {emotion} / アングル: {angle}",
        "step1_confirm": "この脚本でよろしいですか？",
        "step1_ok": "OK、画像生成に進む",
        "step1_retry": "追加指示して再生成",
        "step1_back": "設定からやり直す",
        "step1_quit": "終了",
        "step1_additional": "追加の指示を入力してください:",
        "step1_multiline_hint": "（複数行入力可能。Esc → Enterで入力確定）",

        "step2_title": "Step 2: マンガ画像生成",
        "step2_generating": "マンガを生成中...（時間がかかります）",
        "step2_complete": "マンガ生成完了！",
        "step2_preview": "プレビュー: {path}",
        "step2_confirm": "このマンガでよろしいですか？",
        "step2_ok": "OK、保存して完了",
        "step2_retry": "追加指示して再生成",
        "step2_style": "別の画風で再生成",
        "step2_back": "脚本確認に戻る",
        "step2_quit": "終了（保存しない）",
        "step2_additional": "画像に関する追加指示を入力してください:",
        "step2_style_changed": "画風を変更: {icon} {name}",

        "step3_title": "Step 3: 保存",
        "step3_complete": "マンガを保存しました！",
        "step3_output_title": "タイトル: {title}",
        "step3_output_path": "出力先: {path}",

        # Status messages
        "going_back_settings": "設定画面に戻ります。",
        "going_back_script": "脚本確認に戻ります。",
        "regenerating_script": "脚本を再生成",
        "quitting": "終了します。",
        "cancelled": "キャンセルしました。",
        "interrupted": "中断されました。",
        "additional_instruction": "追加指示: {text}",

        # Errors
        "error_unknown_style": "エラー: 不明なスタイル '{style}'",
        "error_available_styles": "利用可能なスタイル: {styles}",

        # Style categories
        "category_japanese": "日本漫画",
        "category_web": "Web漫画",
        "category_international": "海外コミック",
        "category_art": "アート・実験系",
        "category_business": "教育・ビジネス",

        # Untitled
        "untitled": "無題のマンガ",
    },
}


# Category name translations
CATEGORY_TRANSLATIONS = {
    "en": {
        "日本漫画": "Japanese Manga",
        "Web漫画": "Web Comics",
        "海外コミック": "International Comics",
        "アート・実験系": "Art / Experimental",
        "教育・ビジネス": "Education / Business",
    },
    "ja": {
        "日本漫画": "日本漫画",
        "Web漫画": "Web漫画",
        "海外コミック": "海外コミック",
        "アート・実験系": "アート・実験系",
        "教育・ビジネス": "教育・ビジネス",
    },
}

# Style name and description translations
STYLE_TRANSLATIONS = {
    "en": {
        # Japanese Manga
        "yonkoma": {"name": "4-Panel Manga", "description": "Classic 4-panel format with setup-development-twist-conclusion"},
        "shonen": {"name": "Shonen Style", "description": "Dynamic compositions and powerful expressions"},
        "shojo": {"name": "Shojo Style", "description": "Delicate lines and decorative elements"},
        "seinen": {"name": "Seinen Style", "description": "Realistic art and mature themes"},
        "yuru": {"name": "Yuru-fuwa Daily", "description": "Cute deformed characters and heartwarming scenes"},
        "horror": {"name": "Horror Manga", "description": "Eerie atmosphere and fear-inducing expressions"},
        # Web Comics
        "webtoon": {"name": "Webtoon Style", "description": "Full-color vertical scroll format"},
        "sns": {"name": "SNS Manga", "description": "Simple, easy-to-read single-page format"},
        "essay": {"name": "Essay Manga", "description": "Style for depicting real-life experiences"},
        # International Comics
        "american": {"name": "American Comics", "description": "Hero comic style with bold expressions"},
        "bd": {"name": "Bande Dessinée", "description": "European artistic comic style"},
        "manhwa": {"name": "Manhwa Style", "description": "Korean manga style"},
        # Art / Experimental
        "pixel": {"name": "Pixel Art", "description": "Retro game-inspired pixel graphics"},
        "watercolor": {"name": "Watercolor", "description": "Soft watercolor brush strokes"},
        "ukiyoe": {"name": "Ukiyo-e", "description": "Traditional Japanese woodblock print style"},
        "noir": {"name": "Film Noir", "description": "High contrast black and white cinematography"},
        # Education / Business
        "infographic": {"name": "Infographic", "description": "Visual information presentation style"},
        "educational": {"name": "Educational Manga", "description": "Easy-to-understand explanatory manga"},
        "corporate": {"name": "Business Manga", "description": "Clean style for corporate use"},
    },
    "ja": {
        # 日本漫画
        "yonkoma": {"name": "4コマ漫画", "description": "起承転結の王道4コマ形式"},
        "shonen": {"name": "少年漫画風", "description": "ダイナミックな構図と迫力のある表現"},
        "shojo": {"name": "少女漫画風", "description": "繊細な線と華やかな演出"},
        "seinen": {"name": "青年漫画風", "description": "リアルな描写と深みのある表現"},
        "yuru": {"name": "ゆるふわ日常系", "description": "かわいいデフォルメとほのぼの表現"},
        "horror": {"name": "ホラー漫画風", "description": "不気味さと恐怖を演出"},
        # Web漫画
        "webtoon": {"name": "Webtoon風", "description": "フルカラー縦スクロール形式"},
        "sns": {"name": "SNS漫画風", "description": "シンプルで読みやすい1ページ完結型"},
        "essay": {"name": "エッセイ漫画風", "description": "実体験を漫画化するスタイル"},
        # 海外コミック
        "american": {"name": "アメコミ風", "description": "ヒーローコミック風の力強い表現"},
        "bd": {"name": "バンドデシネ風", "description": "ヨーロッパ風の芸術的なコミック"},
        "manhwa": {"name": "マンファ風", "description": "韓国漫画スタイル"},
        # アート・実験系
        "pixel": {"name": "ピクセルアート風", "description": "レトロゲーム風のドット絵表現"},
        "watercolor": {"name": "水彩画風", "description": "柔らかい水彩タッチの表現"},
        "ukiyoe": {"name": "浮世絵風", "description": "日本の伝統的な木版画スタイル"},
        "noir": {"name": "フィルムノワール風", "description": "モノクロの影と光のコントラスト"},
        # 教育・ビジネス
        "infographic": {"name": "インフォグラフィック風", "description": "情報を視覚的に伝えるスタイル"},
        "educational": {"name": "学習漫画風", "description": "わかりやすい解説漫画スタイル"},
        "corporate": {"name": "ビジネス漫画風", "description": "企業向けのクリーンなスタイル"},
    },
}


def translate_category(category: str) -> str:
    """Translate category name to current language"""
    translations = CATEGORY_TRANSLATIONS.get(_current_lang, CATEGORY_TRANSLATIONS["en"])
    return translations.get(category, category)


def translate_style(style_id: str) -> dict:
    """Translate style name and description to current language"""
    translations = STYLE_TRANSLATIONS.get(_current_lang, STYLE_TRANSLATIONS["en"])
    return translations.get(style_id, {"name": style_id, "description": ""})
