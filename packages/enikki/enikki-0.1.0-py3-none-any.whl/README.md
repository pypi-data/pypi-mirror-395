# enikki

A CLI tool to generate picture-diary style manga from text conversations. Uses Gemini 3 for script and image generation.

[日本語版 README はこちら](README.ja.md)

## Features

- **Interactive UI**: Enter story, style, panel count, etc. through an interactive interface
- **19 Style Presets**: 4-panel manga, shonen, shojo, webtoon, American comics, and more
- **One-shot Generation with Gemini 3**: Generate a single manga image with consistent character appearance
- **Step-by-step Confirmation**: Review and regenerate at each step (script and image)
- **Character Image Reference**: Specify a character image for better consistency

## API Usage Costs

enikki uses the Google Gemini API. Here are the approximate costs per manga generation:

### Models and Pricing

| Process | Model | Input Price | Output Price |
|---------|-------|-------------|--------------|
| Script Generation | gemini-3-pro-preview | $2.00/1M tokens | $12.00/1M tokens |
| Image Generation | gemini-3-pro-image-preview | $2.00/1M tokens | $120.00/1M tokens (image) |

*Image output consumes approximately 1,120 tokens per image

### Estimated Cost per Generation (4-panel manga)

| Process | Input Tokens | Output Tokens | Cost |
|---------|--------------|---------------|------|
| Script Generation | ~1,500 | ~500 | ~$0.009 |
| Image Generation | ~800 | ~1,120 (1 image) | ~$0.14 |
| **Total** | - | - | **~$0.15** |

*Regeneration will incur additional costs
*Character image input adds approximately 560 tokens ($0.001)

### Tips to Reduce Costs

- Review the script before proceeding to image generation (image generation is more expensive)
- Write specific additional instructions to minimize regeneration attempts

For details, see the [Gemini API Pricing Page](https://ai.google.dev/gemini-api/docs/pricing).

## Quick Start

1. Get a Google AI API key: https://aistudio.google.com/app/apikey

2. Set your API key:
```bash
export GEMINI_API_KEY="your-api-key-here"
```

3. Run with uvx (no installation required):
```bash
uvx enikki run
```

That's it! For Japanese UI, add `--lang ja`:
```bash
uvx enikki --lang ja run
```

> Note: Both `GEMINI_API_KEY` and `GOOGLE_API_KEY` environment variables are supported.

## Installation (Optional)

### Using pip

```bash
pip install enikki
enikki run
```

### From source

```bash
git clone https://github.com/kentaro/enikki.git
cd enikki
pip install -e .
enikki run
```

## Usage

### Interactive Mode (Recommended)

```bash
uvx enikki run
# or if installed via pip
enikki run
```

Global options:
- `--config`: Path to config file (default: `config.toml` or `~/.config/enikki/config.toml`)
- `--lang, -l`: Language for UI (`en` or `ja`, default: `en`)

Interactive prompts will guide you through:
1. Style selection
2. Story concept input
3. Aspect ratio selection
4. Panel count selection
5. Character image specification (optional)

Generation flow:
- **Step 1: Script Generation** → Review → OK / Add instructions and regenerate / Go back / Quit
- **Step 2: Image Generation** → Preview → OK / Add instructions and regenerate / Go back / Quit
- **Step 3: Save** → Open completed image

### Quick Mode

```bash
uvx enikki quick "A story about meeting a strange customer at a cafe" --style essay --panels 4
```

Options:
- `--style, -s`: Style ID (default: yonkoma)
- `--panels, -p`: Number of panels (default: 4)
- `--ratio, -r`: Aspect ratio (default: 9:16)
- `--character, -c`: Character image file
- `--output, -o`: Output file (auto-generated with timestamp if omitted)
- `--backend, -b`: Backend (gemini / mock)

### Show Available Styles

```bash
uvx enikki styles
```

## Available Styles

### Japanese Manga
| ID | Name | Description |
|----|------|-------------|
| yonkoma | 4-Panel Manga | Classic 4-panel format with setup-development-twist-conclusion |
| shonen | Shonen Style | Dynamic compositions and powerful expressions |
| shojo | Shojo Style | Delicate lines and decorative elements |
| seinen | Seinen Style | Realistic art and mature themes |
| yuru | Yuru-fuwa Daily | Cute deformed characters and heartwarming scenes |
| horror | Horror Manga | Eerie atmosphere and fear-inducing expressions |

### Web Comics
| ID | Name | Description |
|----|------|-------------|
| webtoon | Webtoon Style | Full-color vertical scroll format |
| sns | SNS Manga | Simple, easy-to-read single-page format |
| essay | Essay Manga | Style for depicting real-life experiences |

### International Comics
| ID | Name | Description |
|----|------|-------------|
| american | American Comics | Hero comic style with bold expressions |
| bd | Bande Dessinée | European artistic comic style |
| manhwa | Manhwa Style | Korean manga style |

### Art / Experimental
| ID | Name | Description |
|----|------|-------------|
| pixel | Pixel Art | Retro game-inspired pixel graphics |
| watercolor | Watercolor | Soft watercolor brush strokes |
| ukiyoe | Ukiyo-e | Traditional Japanese woodblock print style |
| noir | Film Noir | High contrast black and white cinematography |

### Education / Business
| ID | Name | Description |
|----|------|-------------|
| infographic | Infographic | Visual information presentation style |
| educational | Educational Manga | Easy-to-understand explanatory manga |
| corporate | Business Manga | Clean style for corporate use |

## Author

[Kentaro Kuribayashi](https://kentarokuribayashi.com/)

## License

MIT License
