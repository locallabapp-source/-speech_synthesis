import json

with open('qwen3_tts_colab.ipynb', 'r', encoding='utf-8') as f:
    nb = json.load(f)

# Update download section number: cell-12 (markdown "## 6.")
nb['cells'][12]['source'] = ['## 9. 生成ファイルのダウンロード']

# New cells to insert before download (index 12)
new_cells = [
    # --- Section 7 markdown ---
    {
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "## 7. Qwen内蔵ボイスでASMRささやき生成（クローンなし）\n",
            "\n",
            "参照音声不要。Qwen3-TTS の内蔵日本語スピーカー **Chihiro** を使い、\n",
            "`instruct` パラメータだけでASMRニュアンスを指定します。\n",
            "\n",
            "- Base モデルをメモリから解放してから CustomVoice モデルをロードします\n",
            "- 初回は約3.5GB のダウンロードが発生します",
        ],
    },
    # --- Load CustomVoice model (release Base first) ---
    {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "import gc, torch\n",
            "from qwen_tts import Qwen3TTSModel\n",
            "\n",
            "# Base モデルが残っていれば解放\n",
            "if 'model_base' in dir() and model_base is not None:\n",
            "    del model_base\n",
            "    gc.collect()\n",
            "    torch.cuda.empty_cache()\n",
            "    print(f'VRAM解放後: {torch.cuda.memory_allocated() / 1024**3:.2f} GB 使用中')\n",
            "\n",
            "MODEL_CUSTOM = 'Qwen/Qwen3-TTS-12Hz-1.7B-CustomVoice'\n",
            "\n",
            "print(f'ロード中: {MODEL_CUSTOM}')\n",
            "model_custom = Qwen3TTSModel.from_pretrained(\n",
            "    MODEL_CUSTOM,\n",
            "    device_map='cuda:0',\n",
            "    dtype=torch.bfloat16,\n",
            ")\n",
            "print('ロード完了！')",
        ],
    },
    # --- Section 8 markdown ---
    {
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "## 8. 内蔵ボイスASMRバッチ生成\n",
            "\n",
            "参照音声・書き起こし不要。`INSTRUCT` と `TEXTS` だけ変更して実行できます。",
        ],
    },
    # --- CustomVoice ASMR batch ---
    {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "import soundfile as sf\n",
            "import IPython.display as ipd\n",
            "import gc, torch, glob, os, re\n",
            "\n",
            "# ============================================================\n",
            "# ★ 演技ニュアンス指定（英語で記述）\n",
            "#    instruct_presets.md にプリセット一覧あり\n",
            "# ============================================================\n",
            "INSTRUCT = (\n",
            "    'Very low-pitched, deep whispering voice, speaking directly into the ear, '\n",
            "    'extremely close-mic, slow and deliberate pace, calm and intimate'\n",
            ")\n",
            "\n",
            "# ============================================================\n",
            "# ★ 読み上げテキスト\n",
            "# ============================================================\n",
            "TEXTS = [\n",
            "    'ねえ……聞こえてる？そっと、耳を澄ませて……',\n",
            "    '今日も、お疲れ様でした……ゆっくり、息を吐いて。大丈夫ですよ。',\n",
            "    'もう少しだけ、そばにいますね……何も心配しなくていいです。',\n",
            "    '目を閉じて……ただ、私の声だけ、聞いていて。',\n",
            "    'おやすみなさい……ゆっくり、眠れますように……。',\n",
            "]\n",
            "\n",
            "# ---- 前回の出力ファイルを削除 & GPU メモリ確認 ----\n",
            "for old in glob.glob('*.wav'):\n",
            "    if old != globals().get('REF_AUDIO_PATH', ''):\n",
            "        os.remove(old)\n",
            "        print(f'削除: {old}')\n",
            "gc.collect()\n",
            "torch.cuda.empty_cache()\n",
            "print(f'VRAM: {torch.cuda.memory_allocated() / 1024**3:.2f} GB 使用中')\n",
            "\n",
            "def safe_filename(text, max_len=40):\n",
            "    name = re.sub(r\'[\\\\/:*?\"<>|]\', \'\', text)\n",
            "    name = re.sub(r\'\\s+\', \'_\', name.strip())\n",
            "    return name[:max_len] + \'.wav\'\n",
            "\n",
            "print(f'ニュアンス: {INSTRUCT}')\n",
            "print('音声生成中...')\n",
            "\n",
            "wavs, sr = model_custom.generate_custom_voice(\n",
            "    text=TEXTS,\n",
            "    language=['Japanese'] * len(TEXTS),\n",
            "    speaker='Chihiro',\n",
            "    instruct=INSTRUCT if INSTRUCT else None,\n",
            ")\n",
            "\n",
            "output_files = []\n",
            "for i, wav in enumerate(wavs):\n",
            "    path = safe_filename(TEXTS[i])\n",
            "    sf.write(path, wav, sr)\n",
            "    output_files.append(path)\n",
            "    print(f'\\n--- [{i+1}] {TEXTS[i]} ---')\n",
            "    print(f'保存: {path}')\n",
            "    ipd.display(ipd.Audio(path))\n",
            "\n",
            "print(f'\\nバッチ生成完了！ {len(output_files)}件')",
        ],
    },
]

# Insert new cells at index 12 (before download section)
for i, cell in enumerate(new_cells):
    nb['cells'].insert(12 + i, cell)

with open('qwen3_tts_colab.ipynb', 'w', encoding='utf-8') as f:
    json.dump(nb, f, ensure_ascii=False, indent=1)

print('Done. Cell count:', len(nb['cells']))
for i, c in enumerate(nb['cells']):
    src = ''.join(c['source'])[:60].replace('\n', ' ')
    print(f'  [{i:2}] {c["cell_type"]:8}  {src}')
