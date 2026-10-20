"""Original, deterministic chapter-one sound sketches. No voices or external samples."""
from pathlib import Path
import array
import math
import random
import wave
import sys

RATE = 22050
OUT = Path(__file__).resolve().parents[1] / "game" / "audio"
OUT.mkdir(parents=True, exist_ok=True)
rng = random.Random(713)

def bed(seconds):
    return [0.0] * int(RATE * seconds)

def tone(data, start, duration, frequency, gain, decay=8, noise=0):
    for i in range(int(duration * RATE)):
        p = int(start * RATE) + i
        if p >= len(data):
            break
        t = i / RATE
        env = min(t / .004, 1) * math.exp(-decay * t)
        tail = min((duration - t) / .035, 1)
        val = math.sin(2 * math.pi * frequency * t)
        val += .22 * math.sin(2 * math.pi * frequency * 2.71 * t)
        data[p] += gain * env * tail * ((1 - noise) * val + noise * rng.uniform(-1, 1))

def save(name, data):
    if "--urgent-only" in sys.argv and name != "ticking_urgent":
        return
    if "--tension-only" in sys.argv and name not in ("step_last", "corridor_chill"):
        return
    # --corridor-only는 기존 승인 음원을 덮어쓰지 않고 신규 복도 효과음만 만든다.
    if "--corridor-only" in sys.argv and name not in ("steps_near", "steps_other", "corridor_impact"):
        return
    peak = max(abs(x) for x in data) or 1
    assert peak < .99, (name, peak)
    samples = array.array("h", (round(max(-1, min(1, x)) * 32767) for x in data))
    with wave.open(str(OUT / (name + ".wav")), "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(RATE)
        w.writeframes(samples.tobytes())

d = bed(2)
tone(d, 0, .07, 1750, .13, 75, .55)
tone(d, 1, .06, 1350, .11, 78, .55)
save("ticking", d)
for name, beats in [("knock_two", [0, .42]), ("knock_signal", [0, .65, .84])]:
    d = bed(1.7)
    for t in beats:
        tone(d, t, .19, 185 if name == "knock_two" else 270, .25, 24, .24)
    save(name, d)
for name, freq, gain in [("call", 880, .18), ("panel", 540, .1), ("cup", 1450, .14)]:
    d = bed(1.3)
    tone(d, 0, .8, freq, gain, 6)
    save(name, d)
d = bed(1.5)
for t, f in [(0, 1600), (.24, 2350), (.74, 1200)]:
    tone(d, t, .35, f, .12, 15, .15)
save("cutlery", d)
for name, beats in [("door_close", [(.05, 85), (.26, 330)]), ("door_open", [(.02, 480), (.21, 115)]), ("handle", [(.02, 650), (.21, 420), (.52, 580)])]:
    d = bed(1.2)
    for t, f in beats:
        tone(d, t, .25, f, .16, 22, .4)
    save(name, d)
for name, dur, gain in [("pen", 2.8, .045), ("drawer", 1.0, .1)]:
    d = bed(dur)
    smooth = 0
    for i in range(len(d)):
        t = i / RATE
        smooth = .82 * smooth + .18 * rng.uniform(-1, 1)
        pulse = max(0, math.sin(t * 23)) * max(0, math.sin(t * 5.7))
        d[i] = smooth * gain * pulse * min(t * 30, 1) * min((dur - t) * 10, 1)
    save(name, d)
d = bed(8)
for i in range(len(d)):
    t = i / RATE
    d[i] = .012 * math.sin(2 * math.pi * 55 * t) + rng.uniform(-.003, .003)
save("corridor", d)
d = bed(24)
for start, freq in [(0, 261.63), (4, 329.63), (8, 293.66), (12, 220), (16, 261.63), (20, 246.94)]:
    tone(d, start, 4, freq, .08, .95)
    tone(d, start + .05, 3.9, freq * 1.5, .028, 1.2)
save("guide_music", d)
for name, gain, beats in [("steps_near", .15, [0, .85, 1.8]), ("steps_other", .10, [.25, 1.35, 2.5])]:
    d = bed(3.3)
    for t in beats:
        tone(d, t, .24, 95, gain, 22, .45)
        tone(d, t + .07, .15, 260, gain * .25, 28, .8)
    save(name, d)
d = bed(1.1)
tone(d, 0, .38, 75, .30, 15, .35)
tone(d, .04, .18, 180, .10, 24, .7)
save("corridor_impact", d)
d = bed(.7)
tone(d, 0, .24, 95, .10, 22, .45)
tone(d, .07, .15, 260, .025, 28, .8)
tone(d, .16, .35, 95, .018, 12, .3)
save("step_last", d)
# 서서히 스며드는 낮은 불협화음. 갑작스러운 큰 소리는 피한다.
d = bed(2.4)
for i in range(len(d)):
    t = i / RATE
    env = math.sin(math.pi * t / 2.4) ** 2
    d[i] = env * (.055 * math.sin(2 * math.pi * 62 * t)
                 + .035 * math.sin(2 * math.pi * 65.5 * t)
                 + .014 * math.sin(2 * math.pi * 187 * t))
save("corridor_chill", d)
# 긴박한 복도 선택 전용: 기존 1초 간격 대신 0.32초마다 틱/톡.
# 기존 음원의 난수 순서와 파일은 바꾸지 않도록 마지막에 별도로 합성한다.
d = bed(.64)
tone(d, 0, .07, 1750, .13, 75, .55)
tone(d, .32, .06, 1350, .11, 78, .55)
save("ticking_urgent", d)
print("Generated selected original sound files.")
