"""
Interactive UI: Collect manga settings through user interaction
"""

from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Optional

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from InquirerPy import inquirer
from InquirerPy.base.control import Choice
from InquirerPy.separator import Separator

from styles.presets import STYLE_PRESETS, StylePreset
from utils.config import get_config
from utils.i18n import t, translate_category, translate_style


console = Console()


@dataclass
class MangaConfig:
    """Manga generation settings"""
    title: str
    story_concept: str
    style: StylePreset
    character_image: Optional[Path]
    aspect_ratio: str
    panel_count: int
    output_path: Path


def display_welcome():
    """Display welcome message"""
    console.print()
    console.print(Panel.fit(
        f"[bold magenta]🎨 {t('app_welcome_title')}[/bold magenta]\n"
        f"[dim]{t('app_welcome_subtitle')}[/dim]",
        border_style="magenta"
    ))
    console.print()


def select_style() -> StylePreset:
    """Select manga style"""
    # Organize styles by category
    categories = {}
    for style in STYLE_PRESETS.values():
        if style.category not in categories:
            categories[style.category] = []
        categories[style.category].append(style)

    # Build choices
    choices = []
    for category, styles in categories.items():
        translated_category = translate_category(category)
        choices.append(Separator(f"── {translated_category} ──"))
        for style in styles:
            style_trans = translate_style(style.id)
            choices.append(Choice(
                value=style.id,
                name=f"{style.icon} {style_trans['name']} - {style_trans['description']}"
            ))

    style_id = inquirer.select(
        message=t('select_style'),
        choices=choices,
        default=None,
        pointer="▶",
        qmark="🎨",
    ).execute()

    return STYLE_PRESETS[style_id]


def input_story_concept() -> tuple[str, str]:
    """Input story concept"""
    console.print(f"\n[bold cyan]📝 {t('input_story_header')}[/bold cyan]\n")

    # Genre selection
    genre = inquirer.select(
        message=t('select_genre'),
        choices=[
            Choice("daily", f"📅 {t('genre_daily')}"),
            Choice("comedy", f"😂 {t('genre_comedy')}"),
            Choice("action", f"⚔️ {t('genre_action')}"),
            Choice("romance", f"💕 {t('genre_romance')}"),
            Choice("horror", f"👻 {t('genre_horror')}"),
            Choice("sf", f"🚀 {t('genre_sf')}"),
            Choice("educational", f"📚 {t('genre_educational')}"),
            Choice("other", f"✨ {t('genre_other')}"),
        ],
        pointer="▶",
        qmark="📖",
    ).execute()

    # Title input
    title = inquirer.text(
        message=t('input_title'),
        qmark="📌",
    ).execute()

    if not title:
        title = t('untitled')

    # Story input
    console.print(f"\n[dim]{t('input_story_hint')}[/dim]")
    console.print(f"[dim]{t('input_story_example')}[/dim]\n")

    story = inquirer.text(
        message=t('input_story_prompt'),
        qmark="💭",
        multiline=True,
    ).execute()

    return title, story


def select_aspect_ratio() -> str:
    """Select aspect ratio"""
    ratio = inquirer.select(
        message=t('select_ratio'),
        choices=[
            Choice("9:16", f"📱 {t('ratio_9_16')}"),
            Choice("3:4", f"📱 {t('ratio_3_4')}"),
            Choice("1:1", f"⬜ {t('ratio_1_1')}"),
            Choice("4:3", f"🖼️ {t('ratio_4_3')}"),
            Choice("16:9", f"🖥️ {t('ratio_16_9')}"),
        ],
        default="9:16",
        pointer="▶",
        qmark="📐",
    ).execute()

    return ratio


def select_panel_count(style: StylePreset) -> int:
    """Select panel count"""
    default_panels = style.default_panels

    panel_count = inquirer.select(
        message=t('select_panels').format(style=style.name, count=default_panels),
        choices=[
            Choice(1, t('panels_1')),
            Choice(2, t('panels_2')),
            Choice(3, t('panels_3')),
            Choice(4, t('panels_4')),
            Choice(6, t('panels_6')),
            Choice(8, t('panels_8')),
        ],
        default=default_panels,
        pointer="▶",
        qmark="🔢",
    ).execute()

    return panel_count


def input_character_image() -> Optional[Path]:
    """Input character image path"""
    # Get default character image from config
    config = get_config()
    default_character = config.defaults.default_character
    default_character_path = Path(default_character) if default_character else None
    has_default = default_character_path and default_character_path.exists()

    if has_default:
        # 3 choices if default exists
        choice = inquirer.select(
            message=t('select_character'),
            choices=[
                Choice("default", f"✅ {t('character_use_default').format(filename=default_character_path.name)}"),
                Choice("custom", f"📁 {t('character_select_other')}"),
                Choice("none", f"❌ {t('character_none')}"),
            ],
            default="default",
            qmark="👤",
        ).execute()

        if choice == "default":
            return default_character_path
        elif choice == "none":
            return None
        # For custom, proceed to file selection below
    else:
        # If no default, use confirm dialog
        use_character = inquirer.confirm(
            message=t('select_character'),
            default=False,
            qmark="👤",
        ).execute()

        if not use_character:
            return None

    path_str = inquirer.filepath(
        message=t('input_character_path'),
        qmark="📁",
        validate=lambda p: Path(p).exists() if p else True,
        only_files=True,
    ).execute()

    return Path(path_str) if path_str else None


def generate_output_path() -> Path:
    """Generate timestamp-based output path"""
    config = get_config()
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"enikki_{timestamp}.png"

    if config.defaults.default_output_dir:
        output_dir = Path(config.defaults.default_output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
        return output_dir / filename

    return Path(filename)


def display_config_summary(config: MangaConfig):
    """Display config summary"""
    table = Table(title=f"📋 {t('config_summary_title')}", border_style="cyan")
    table.add_column("Item", style="cyan")
    table.add_column("Value", style="white")

    style_trans = translate_style(config.style.id)
    table.add_row(t('config_title'), config.title)
    table.add_row(t('config_style'), f"{config.style.icon} {style_trans['name']}")
    table.add_row(t('config_ratio'), config.aspect_ratio)
    table.add_row(t('config_panels'), str(config.panel_count))
    table.add_row(t('config_character'), str(config.character_image) if config.character_image else t('config_none'))
    table.add_row(t('config_output'), str(config.output_path))

    console.print()
    console.print(table)
    console.print()

    console.print(f"[bold]{t('config_story_concept')}[/bold]")
    console.print(Panel(config.story_concept, border_style="dim"))


def run_interactive_session() -> Optional[MangaConfig]:
    """Run interactive session to collect settings"""
    display_welcome()

    try:
        # 1. Style selection
        style = select_style()
        style_trans = translate_style(style.id)
        console.print(f"\n[green]✓[/green] {t('config_style')}: {style.icon} {style_trans['name']}\n")

        # 2. Story input
        title, story = input_story_concept()
        console.print(f"\n[green]✓[/green] {t('config_title')}: {title}\n")

        # 3. Aspect ratio selection
        ratio = select_aspect_ratio()
        console.print(f"\n[green]✓[/green] {t('config_ratio')}: {ratio}\n")

        # 4. Panel count selection
        panels = select_panel_count(style)
        console.print(f"\n[green]✓[/green] {t('config_panels')}: {panels}\n")

        # 5. Character image (optional)
        character = input_character_image()

        # 6. Output path (auto-generated)
        output = generate_output_path()

        # Create config object
        config = MangaConfig(
            title=title,
            story_concept=story,
            style=style,
            character_image=character,
            aspect_ratio=ratio,
            panel_count=panels,
            output_path=output,
        )

        # Display summary
        display_config_summary(config)

        # Confirm
        confirmed = inquirer.confirm(
            message=t('confirm_generate'),
            default=True,
            qmark="🚀",
        ).execute()

        if confirmed:
            return config
        else:
            console.print(f"[yellow]{t('cancelled')}[/yellow]")
            return None

    except KeyboardInterrupt:
        console.print(f"\n[yellow]{t('interrupted')}[/yellow]")
        return None
