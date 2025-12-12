"""
LLMによる漫画脚本生成モジュール

Gemini 3 Pro を使用して、ユーザーの入力から漫画の脚本（各コマの視覚的描写とセリフ）を生成する。
"""

import json
from dataclasses import dataclass
from typing import List, Optional

from styles.presets import StylePreset


@dataclass
class PanelScript:
    """1コマ分の脚本"""
    panel_id: int
    visual_prompt: str  # 画像生成用の視覚的描写（英語）
    dialogue: str  # セリフ（日本語）
    character_emotion: str  # キャラクターの感情
    camera_angle: str  # カメラアングル（wide, medium, close-up, etc.）
    action: str  # キャラクターの動作


@dataclass
class MangaScript:
    """漫画全体の脚本"""
    title: str
    panels: List[PanelScript]
    summary: str  # ストーリーの要約


class ScriptGenerator:
    """Gemini 3 Pro を使った脚本生成クラス"""

    def __init__(self, api_key: str, model_name: str = "gemini-3-pro-preview"):
        """
        Args:
            api_key: Gemini API キー
            model_name: 使用するモデル名
        """
        from google import genai
        self.client = genai.Client(api_key=api_key)
        self.model_name = model_name

    def generate_script(
        self,
        story_concept: str,
        style: StylePreset,
        panel_count: int,
        title: Optional[str] = None,
    ) -> MangaScript:
        """
        ストーリーコンセプトから漫画の脚本を生成

        Args:
            story_concept: ユーザーが入力したストーリーの概要
            style: 漫画のスタイルプリセット
            panel_count: コマ数
            title: タイトル（Noneの場合は自動生成）

        Returns:
            MangaScript: 生成された脚本
        """
        from google.genai import types

        prompt = self._build_prompt(story_concept, style, panel_count, title)

        response = self.client.models.generate_content(
            model=self.model_name,
            contents=prompt,
            config=types.GenerateContentConfig(
                temperature=0.8,
                top_p=0.9,
                response_mime_type="application/json",
            ),
        )

        return self._parse_response(response.text)

    def _build_prompt(
        self,
        story_concept: str,
        style: StylePreset,
        panel_count: int,
        title: Optional[str],
    ) -> str:
        """脚本生成用のプロンプトを構築"""

        prompt = f"""あなたは優秀な漫画原作者です。以下の条件で{panel_count}コマ漫画の脚本を作成してください。

## 入力情報

### ストーリーコンセプト
{story_concept}

### スタイル
- スタイル名: {style.name}
- 特徴: {style.description}

### 要件
- コマ数: {panel_count}コマ
- タイトル: {title if title else "自動で考案してください"}

## 出力形式

以下のJSON形式で出力してください。visual_promptは必ず英語で、画像生成AIに適した詳細な描写にしてください。

```json
{{
  "title": "漫画のタイトル",
  "summary": "ストーリーの1行要約",
  "panels": [
    {{
      "panel_id": 1,
      "visual_prompt": "A young woman with brown hair standing in front of a large exhibition hall, looking excited, wide shot, bright daylight",
      "dialogue": "ついに来ました！",
      "character_emotion": "excited",
      "camera_angle": "wide",
      "action": "standing and looking around"
    }},
    ...
  ]
}}
```

## 注意点

1. **visual_prompt** は必ず英語で、以下を含めてください:
   - キャラクターの外見と表情
   - 背景・場所の描写
   - カメラアングル（wide shot, medium shot, close-up, bird's eye view, etc.）
   - 照明や雰囲気

2. **dialogue** は日本語で、自然な会話やモノローグにしてください。吹き出しに収まる短さが理想です。

3. **{panel_count}コマで起承転結**（または適切な構成）を意識してください:
   - 1コマ目: 状況設定
   - 中間: 展開
   - 最終コマ: オチや結論

4. スタイル「{style.name}」に合った演出を心がけてください。

JSONのみを出力してください。説明文は不要です。
"""
        return prompt

    def _parse_response(self, response_text: str) -> MangaScript:
        """APIレスポンスをパースしてMangaScriptオブジェクトに変換"""
        try:
            # JSONブロックを抽出（```json ... ``` で囲まれている場合も対応）
            text = response_text.strip()
            if text.startswith("```"):
                # コードブロックを除去
                lines = text.split("\n")
                text = "\n".join(lines[1:-1])

            data = json.loads(text)

            panels = [
                PanelScript(
                    panel_id=p["panel_id"],
                    visual_prompt=p["visual_prompt"],
                    dialogue=p["dialogue"],
                    character_emotion=p.get("character_emotion", "neutral"),
                    camera_angle=p.get("camera_angle", "medium"),
                    action=p.get("action", ""),
                )
                for p in data["panels"]
            ]

            return MangaScript(
                title=data["title"],
                panels=panels,
                summary=data.get("summary", ""),
            )

        except json.JSONDecodeError as e:
            raise ValueError(f"Failed to parse LLM response as JSON: {e}\nResponse: {response_text}")


class MockScriptGenerator:
    """テスト・デモ用のモック脚本生成クラス"""

    def generate_script(
        self,
        story_concept: str,
        style: StylePreset,
        panel_count: int,
        title: Optional[str] = None,
    ) -> MangaScript:
        """モックの脚本を生成"""
        panels = []
        for i in range(panel_count):
            panels.append(
                PanelScript(
                    panel_id=i + 1,
                    visual_prompt=f"Panel {i + 1} illustration, {style.prompt_prefix}character in scene",
                    dialogue=f"セリフ {i + 1}",
                    character_emotion="neutral",
                    camera_angle="medium",
                    action="standing",
                )
            )

        return MangaScript(
            title=title or "サンプル漫画",
            panels=panels,
            summary="これはモック生成された脚本です。",
        )
