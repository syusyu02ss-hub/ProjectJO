# 장면 1의 상태와 조사 대상.
# 이 기록은 수혁이 실제로 적는 수첩이 아니라 플레이어가 확인한 사실을 다시 보는 UI용이다.

default clues = []
default observed = []
default notes = []
default stage = "intro"
default note_focus = "observations"
default chapter_complete = False
default inspected = ""

init python:
    PAPER = "#eee4cf"
    INK = "#383d36"
    ACCENT = "#9ab3ba"
    HAND = "fonts/NanumSmile.ttf"

    OBJECTS = [
        ("window", "창", 185, 371),
        ("cup", "찻잔", 582, 720),
        ("clock", "벽시계", 638, 317),
        ("door", "문", 962, 473),
        ("light", "문 위 패널", 969, 242),
        ("panel", "빈 액자", 1286, 383),
        ("button", "벽 버튼", 1166, 489),
        ("drawer", "서랍장", 1733, 660),
    ]

    # 1920×1080 기준 실제 사물 영역. 표시용 좌표(OBJECTS)와 분리한다.
    # 작은 표시점을 정확히 누르지 않아도 조사되며, 인접 대상끼리는 겹치지 않는다.
    INVESTIGATION_BOUNDS = {
        "window": (0, 60, 355, 500),
        "cup": (500, 650, 185, 150),
        "clock": (555, 235, 175, 170),
        "door": (810, 270, 310, 525),
        "light": (885, 165, 170, 100),
        "panel": (1220, 285, 170, 240),
        "button": (1120, 430, 100, 155),
        "drawer": (1590, 590, 330, 270),
    }

    REQUIRED_OBSERVATIONS = tuple(key for key, _title, _x, _y in OBJECTS)

    def has(clue):
        return clue in store.clues

    def add_record(key, title, content, flags=()):
        if not any(record[0] == key for record in store.notes):
            store.notes.append((key, title, content))
        for flag in flags:
            if flag not in store.clues:
                store.clues.append(flag)

    def mark_observed(key):
        if key not in store.observed:
            store.observed.append(key)

    def investigation_ready():
        return all(key in store.observed for key in REQUIRED_OBSERVATIONS)

    def reset_scene1_state():
        """새 게임은 이전 구설계의 단서·반복 상태를 사용하지 않는다."""
        store.clues = []
        store.observed = []
        store.notes = []
        store.stage = "intro"
        store.note_focus = "observations"
        store.chapter_complete = False
        store.inspected = ""

    def checkpoint():
        renpy.save("auto-1", extra_info="제1장 · 방 조사 후")
