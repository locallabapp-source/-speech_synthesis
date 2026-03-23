# Qwen3-TTS INSTRUCT プリセット集

`generate_voice_clone()` や `generate_custom_voice()` の `instruct` パラメータに渡す英語プロンプトのまとめ。
英語で書くほど精度が高い。空文字 `""` にすると通常のボイスクローンのみ。

---

## ASMR・耳元ささやき系

### ① 低音・耳元距離感重視
```
Very low-pitched, deep whispering voice, speaking directly into the ear,
extremely close-mic, slow and deliberate pace, no breathiness, calm and intimate
```

### ② 息多め・囁き感重視
```
Hushed, breathy whisper with a low and warm tone, as if lips are touching the ear,
very slow delivery, gentle consonants, tender and soothing
```

### ③ バイノーラル・3D感重視
```
Binaural ASMR whisper, low and resonant voice, extremely close to the microphone,
soft lip sounds, slow pace, deeply relaxing and hypnotic
```

### ④ 落ち着いた低音（シンプル）
```
Low-pitched, slow, quiet voice speaking in a near whisper,
warm and deep tone, close proximity, no high frequency, minimal breath noise
```

### ⑤ 睡眠誘導系
```
Sleep-inducing voice, very low and velvety whisper, extremely slow pace,
monotone with gentle inflection, close-mic, soft and drowsy tone
```

---

## その他スタイル

### 甘々・親しみ系（通常音量）
```
Warm and tender voice, slow pace, slightly emotional, gentle and loving tone
```

### 元気・明るい系
```
Energetic and cheerful, upbeat tone, clear and bright voice
```

### プロナレーター風
```
Professional narrator, clear and neutral tone, moderate pace, well-articulated
```

---

## 使い方メモ

- 高音になりすぎる場合 → `low-pitched` や `no high frequency` を明示する
- 息が多すぎる場合 → `minimal breath noise` を追加する
- 速すぎる場合 → `very slow pace` や `deliberate pace` を追加する
- ピッチが安定しない場合 → `monotone with gentle inflection` を追加する
