default clues = []
default observed = []
default notes = []
default warnings = []
default urgent_note_written = False
default first_dejavu_seen = False
default sorting_experienced = False
default fail_call_count = 0
default fail_judgment_count = 0
default wrong_choice_history = {"A": 0, "B": 0, "C": 0}
default fail_kind = "A"
default latest_warning = ""
default stage = "intro"
default wall_minutes = 1258
default note_focus = "observations"
default skip_locked = False
default chapter_complete = False
default inspected = ""
default call_resolved = False
default clock_seconds = 0

init python:
    import math
    PAPER = "#eee4cf"
    INK = "#383d36"
    ACCENT = "#c8b58a"
    HAND = "fonts/NanumPenScript-Regular.ttf"
    URGENT_NOTE = "검은 버튼. 노란 표시등.\n카메라는 카트의 태그를 본다."
    TRUST_LINE = "기억이 없다면 이 글부터 믿어. 네 글씨다."
    HINTS = {
        "A": ["호출 누르지 마. 사람이 온다. 도와주는 사람 아님.",
              "노크가 너무 빨랐다. 문밖에서 기다리고 있었다.",
              "호출은 도움 요청이 아니라 신고다."],
        "B": ["직원한테 도움 청하지 마. 도와주는 사람 아님.",
              "카메라는 카트를 본다. 그럼 카트가 가리는 곳은?",
              "문이 열려 있는 동안이 틈이다. 카트 뒤."],
        "C": ["뛰지 마. 직원은 뛰지 않았다. 뛸 필요가 없어서다.",
              "카메라는 카트를 본다. 그럼 카트가 가리는 곳은?",
              "문이 열려 있는 동안이 틈이다. 카트 뒤."]
    }
    OBJECTS = [
        ("window", "창", 145, 204),
        ("cup", "찻잔", 208, 452),
        ("clock", "시계", 505, 119),
        ("door", "문", 720, 306),
        ("light", "표시등", 712, 35),
        ("notice", "안내문", 910, 177),
        ("call", "호출 버튼", 866, 278),
        ("drawer", "서랍장", 1177, 423),
    ]

    def has(clue):
        return clue in store.clues

    def add_note(key, title, content, flags=()):
        if not any(n[0] == key for n in store.notes):
            store.notes.append((key, title, content))
        for flag in flags:
            if flag not in store.clues:
                store.clues.append(flag)

    def mark_observed(key):
        if key not in store.observed:
            store.observed.append(key)

    def investigation_ready():
        return all(k in store.observed for k in ("notice", "drawer", "light"))

    def clock_label(wrist=False):
        m = store.wall_minutes + (37 if wrist and store.sorting_experienced else 0)
        return "%02d:%02d" % ((m // 60) % 24, m % 60)

    def write_failure(kind):
        store.fail_kind = kind
        store.wrong_choice_history[kind] += 1
        if kind == "A":
            store.fail_call_count += 1
            level = store.fail_call_count
        else:
            store.fail_judgment_count += 1
            level = store.fail_judgment_count
        first = HINTS[kind][0]
        if store.wrong_choice_history[kind] > 1:
            first = "{u}" + first + "{/u}"
        lines = [first] + HINTS[kind][1:min(level, 3)]
        store.latest_warning = "\n\n".join(lines + [TRUST_LINE])
        store.warnings.append((kind, level, store.latest_warning))
        store.sorting_experienced = True

    def checkpoint():
        if not renpy.is_in_test():
            renpy.save("auto-1", extra_info="제1장 · " + ("배식 직전" if store.stage == "judgment" else "방 안"))

    def stop_fast_skip():
        renpy.config.skipping = None

    class RoomClock(renpy.Displayable):
        def render(self, width, height, st, at):
            r = renpy.Render(94, 94)
            c = r.canvas()
            c.circle("#755c3f", (47, 47), 46)
            c.circle("#d4c3a2", (47, 47), 42)
            for i in range(12):
                a = i * math.pi / 6
                c.line("#5c503e", (47+math.sin(a)*35,47-math.cos(a)*35), (47+math.sin(a)*39,47-math.cos(a)*39), 2)
            minute = store.wall_minutes % 60
            hour = (store.wall_minutes // 60) % 12
            for a,l,w in ((hour*math.pi/6+minute*math.pi/360,23,3),(minute*math.pi/30,34,2)):
                c.line("#403a30", (47,47), (47+math.sin(a)*l,47-math.cos(a)*l), w)
            c.circle("#403a30", (47,47),3)
            return r

