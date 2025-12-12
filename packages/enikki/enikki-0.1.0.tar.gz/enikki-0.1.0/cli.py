#!/usr/bin/env python3
"""
enikki: メインエントリーポイント

対話型UIで設定を収集し、LLM + 画像生成AIで絵日記風マンガを生成する。
"""

import os
import platform
import subprocess
from datetime import datetime
from pathlib import Path
from typing import Optional


def open_file(path: Path) -> None:
    """Open a file with the default application (cross-platform)"""
    system = platform.system()
    try:
        if system == "Darwin":  # macOS
            subprocess.run(["open", str(path)], check=False)
        elif system == "Windows":
            subprocess.run(["start", "", str(path)], shell=True, check=False)
        else:  # Linux and others
            subprocess.run(["xdg-open", str(path)], check=False)
    except Exception:
        pass  # Silently fail if unable to open

import typer
from rich.console import Console
from rich.panel import Panel
from PIL import Image
from InquirerPy import inquirer

from ui.interactive import run_interactive_session, MangaConfig, select_style
from styles.presets import STYLE_PRESETS, list_styles_by_category
from generators.script_generator import ScriptGenerator, MockScriptGenerator
from generators.image_generator import create_image_generator
from utils.canvas import calculate_canvas_size
from utils.config import get_config, reload_config
from utils.i18n import set_language, t, translate_category, translate_style


app = typer.Typer(
    name="enikki",
    help="enikki: Generate picture-diary style manga from text",
    add_completion=False,
)
console = Console()


@app.callback()
def main_callback(
    config: Optional[Path] = typer.Option(
        None,
        "--config",
        help="Path to config file (default: config.toml)",
        exists=True,
    ),
    lang: str = typer.Option(
        "en",
        "--lang", "-l",
        help="Language for UI (en, ja)",
    ),
):
    """Global options"""
    if config:
        reload_config(config)
    set_language(lang)


@app.command(help="Generate manga in interactive mode")
def run(
    character: Optional[Path] = typer.Option(
        None,
        "--character", "-c",
        help="Character image file",
        exists=True,
    ),
    output: Optional[Path] = typer.Option(
        None,
        "--output", "-o",
        help="Output file path",
    ),
    backend: str = typer.Option(
        "gemini",
        "--backend", "-b",
        help="Image generation backend (gemini, mock)",
    ),
    dry_run: bool = typer.Option(
        False,
        "--dry-run",
        help="Skip actual image generation and use mock image",
    ),
):
    # バックエンドの設定
    if dry_run:
        backend = "mock"

    # ループ（設定に戻る場合に再実行）
    while True:
        # 対話セッションを開始
        config = run_interactive_session()

        if config is None:
            raise typer.Exit(code=1)

        # コマンドライン引数で上書き
        if character:
            config.character_image = character
        elif not config.character_image:
            # 設定ファイルのデフォルトキャラクター画像を使用
            app_config = get_config()
            if app_config.defaults.default_character:
                default_character_path = Path(app_config.defaults.default_character)
                if default_character_path.exists():
                    config.character_image = default_character_path
        if output:
            config.output_path = output

        # マンガ生成を実行
        result = _generate_manga(config, backend)

        # Noneが返されたら設定からやり直し
        if result is None:
            continue
        else:
            break


@app.command(help="Generate manga in quick mode")
def quick(
    story: str = typer.Argument(..., help="Story concept"),
    style: str = typer.Option(
        "yonkoma",
        "--style", "-s",
        help="Style ID (yonkoma, shonen, shojo, webtoon, etc.)",
    ),
    panels: int = typer.Option(
        4,
        "--panels", "-p",
        help="Number of panels",
    ),
    ratio: str = typer.Option(
        "9:16",
        "--ratio", "-r",
        help="Aspect ratio (9:16, 1:1, 16:9, etc.)",
    ),
    character: Optional[Path] = typer.Option(
        None,
        "--character", "-c",
        help="Character image file",
        exists=True,
    ),
    output: Optional[Path] = typer.Option(
        None,
        "--output", "-o",
        help="Output file path (auto-generated if omitted)",
    ),
    backend: str = typer.Option(
        "gemini",
        "--backend", "-b",
        help="Image generation backend (gemini, mock)",
    ),
):
    if style not in STYLE_PRESETS:
        console.print(f"[red]{t('error_unknown_style').format(style=style)}[/red]")
        console.print(t('error_available_styles').format(styles=', '.join(STYLE_PRESETS.keys())))
        raise typer.Exit(code=1)

    # キャラクター画像: コマンドライン引数 > 設定ファイル
    character_image = character
    if not character_image:
        app_config = get_config()
        if app_config.defaults.default_character:
            default_character_path = Path(app_config.defaults.default_character)
            if default_character_path.exists():
                character_image = default_character_path

    # 出力パス: 指定がなければ日時ベースで自動生成
    output_path = output
    if not output_path:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"enikki_{timestamp}.png"
        if app_config.defaults.default_output_dir:
            output_dir = Path(app_config.defaults.default_output_dir)
            output_dir.mkdir(parents=True, exist_ok=True)
            output_path = output_dir / filename
        else:
            output_path = Path(filename)

    config = MangaConfig(
        title="",  # 自動生成
        story_concept=story,
        style=STYLE_PRESETS[style],
        character_image=character_image,
        aspect_ratio=ratio,
        panel_count=panels,
        output_path=output_path,
    )

    _generate_manga(config, backend)


@app.command(help="Show available styles")
def styles():
    """Show available styles"""
    from rich.table import Table

    categories = list_styles_by_category()

    for category, style_list in categories.items():
        translated_category = translate_category(category)
        table = Table(title=f"📁 {translated_category}", border_style="blue")
        table.add_column("ID", style="cyan")
        table.add_column("Name", style="white")
        table.add_column("Description", style="dim")
        table.add_column("Panels", style="green")

        for s in style_list:
            style_trans = translate_style(s.id)
            table.add_row(
                s.id,
                f"{s.icon} {style_trans['name']}",
                style_trans['description'],
                str(s.default_panels),
            )

        console.print(table)
        console.print()


def _generate_manga(config: MangaConfig, backend: str):
    """Execute manga generation (with confirmation at each step)"""
    # Get API key from config
    app_config = get_config()
    api_key = app_config.api.google_api_key or os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")

    if api_key and backend != "mock":
        script_gen = ScriptGenerator(api_key)
    else:
        script_gen = MockScriptGenerator()

    # Load character image
    character_image = None
    if config.character_image:
        character_image = Image.open(config.character_image)

    # Image generator
    image_gen = create_image_generator(backend, api_key=api_key)

    # Calculate canvas size
    canvas = calculate_canvas_size(config.aspect_ratio)

    # Current story concept (may be modified by additional instructions)
    current_story = config.story_concept
    script = None
    need_script_generation = True  # Whether script generation is needed

    # Main loop (script confirmation → image generation → save)
    while True:
        # ========== Step 1: Script Generation ==========
        if need_script_generation:
            console.print(f"\n[bold cyan]━━━ {t('step1_title')} ━━━[/bold cyan]")

            with console.status(f"📝 {t('step1_generating')}"):
                script = script_gen.generate_script(
                    story_concept=current_story,
                    style=config.style,
                    panel_count=config.panel_count,
                    title=config.title if config.title != t('untitled') else None,
                )

        # ========== Script confirmation loop ==========
        while True:
            # Display script
            console.print(f"\n[bold green]✅ {t('step1_complete')}[/bold green]")
            console.print(Panel(f"[bold]{script.title}[/bold]\n{script.summary}", title="📖 Title / Summary"))

            for panel in script.panels:
                console.print(Panel(
                    f"[cyan]{t('step1_visual')}[/cyan] {panel.visual_prompt}\n\n"
                    f"[yellow]{t('step1_dialogue')}[/yellow] {panel.dialogue}\n"
                    f"[dim]{t('step1_emotion').format(emotion=panel.character_emotion, angle=panel.camera_angle)}[/dim]",
                    title=f"🖼️ {t('step1_panel_title').format(num=panel.panel_id)}"
                ))

            # Confirm
            action = inquirer.select(
                message=t('step1_confirm'),
                choices=[
                    {"value": "ok", "name": f"✅ {t('step1_ok')}"},
                    {"value": "retry", "name": f"🔄 {t('step1_retry')}"},
                    {"value": "back", "name": f"⬅️ {t('step1_back')}"},
                    {"value": "quit", "name": f"🚪 {t('step1_quit')}"},
                ],
                qmark="📝",
            ).execute()

            if action == "ok":
                break
            elif action == "retry":
                console.print(f"[dim]{t('step1_multiline_hint')}[/dim]")
                additional = inquirer.text(
                    message=t('step1_additional'),
                    qmark="💭",
                    multiline=True,
                    transformer=lambda x: "",  # Hide input after confirmation
                ).execute()
                console.print(f"[dim]{t('additional_instruction').format(text=additional[:50] + ('...' if len(additional) > 50 else ''))}[/dim]")
                current_story = f"{config.story_concept}\n\nAdditional instruction: {additional}"
                # Regenerate script
                console.print(f"\n[bold cyan]━━━ {t('regenerating_script')} ━━━[/bold cyan]")
                with console.status(f"📝 {t('step1_generating')}"):
                    script = script_gen.generate_script(
                        story_concept=current_story,
                        style=config.style,
                        panel_count=config.panel_count,
                        title=config.title if config.title != t('untitled') else None,
                    )
                # Continue loop to redisplay script
            elif action == "back":
                console.print(f"[yellow]{t('going_back_settings')}[/yellow]")
                return None  # Re-run interactive session in caller
            else:  # quit
                console.print(f"[yellow]{t('quitting')}[/yellow]")
                raise typer.Exit(code=0)

        # ========== Step 2: Image generation loop ==========
        additional_image_instruction = ""
        go_back_to_script = False

        while True:
            console.print(f"\n[bold cyan]━━━ {t('step2_title')} ━━━[/bold cyan]")

            with console.status(f"🎨 {t('step2_generating')}"):
                generated = image_gen.generate_manga(
                    script=script,
                    style=config.style,
                    character_image=character_image,
                    width=canvas.width,
                    height=canvas.height,
                    additional_instruction=additional_image_instruction,
                )

            # Save to temp file and open
            temp_path = config.output_path.with_suffix(".preview.png")
            generated.image.save(temp_path)

            console.print(f"\n[bold green]✅ {t('step2_complete')}[/bold green]")
            console.print(f"[dim]{t('step2_preview').format(path=temp_path)}[/dim]")

            # Open image
            open_file(temp_path)

            # Confirm
            action = inquirer.select(
                message=t('step2_confirm'),
                choices=[
                    {"value": "ok", "name": f"✅ {t('step2_ok')}"},
                    {"value": "retry", "name": f"🔄 {t('step2_retry')}"},
                    {"value": "style", "name": f"🎨 {t('step2_style')}"},
                    {"value": "back", "name": f"⬅️ {t('step2_back')}"},
                    {"value": "quit", "name": f"🚪 {t('step2_quit')}"},
                ],
                qmark="🎨",
            ).execute()

            if action == "ok":
                break
            elif action == "retry":
                console.print(f"[dim]{t('step1_multiline_hint')}[/dim]")
                additional_image_instruction = inquirer.text(
                    message=t('step2_additional'),
                    qmark="💭",
                    multiline=True,
                    transformer=lambda x: "",  # Hide input after confirmation
                ).execute()
                console.print(f"[dim]{t('additional_instruction').format(text=additional_image_instruction[:50] + ('...' if len(additional_image_instruction) > 50 else ''))}[/dim]")
            elif action == "style":
                # Select different style
                new_style = select_style()
                config.style = new_style
                console.print(f"[green]✓[/green] {t('step2_style_changed').format(icon=new_style.icon, name=new_style.name)}")
                additional_image_instruction = ""  # Reset additional instructions
            elif action == "back":
                # Go back to script confirmation (without regeneration)
                console.print(f"[yellow]{t('going_back_script')}[/yellow]")
                if temp_path.exists():
                    temp_path.unlink()
                go_back_to_script = True
                need_script_generation = False  # Don't regenerate script
                break
            else:  # quit
                console.print(f"[yellow]{t('quitting')}[/yellow]")
                if temp_path.exists():
                    temp_path.unlink()
                raise typer.Exit(code=0)

        # Continue main loop if going back to script
        if go_back_to_script:
            continue

        # Image generation complete → proceed to save
        break

    # ========== Step 3: Save ==========
    console.print(f"\n[bold cyan]━━━ {t('step3_title')} ━━━[/bold cyan]")

    # Move preview file to final location
    temp_path = config.output_path.with_suffix(".preview.png")
    if temp_path.exists():
        temp_path.rename(config.output_path)
    else:
        generated.image.save(config.output_path)

    # Open final image
    open_file(config.output_path)

    # Completion message
    console.print()
    console.print(f"[bold green]✅ {t('step3_complete')}[/bold green]")
    console.print(f"   {t('step3_output_title').format(title=script.title)}")
    console.print(f"   {t('step3_output_path').format(path=config.output_path)}")
    console.print()

    return config


@app.command(help="Show version info")
def version():
    """Show version info"""
    from __init__ import __version__
    console.print(f"enikki v{__version__}")


def main():
    """Main entry point"""
    app()


if __name__ == "__main__":
    main()
