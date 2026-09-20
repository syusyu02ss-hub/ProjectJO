default clues = []
default observed = []
default notes = []
default warnings = []
default urgent_note_written = False
default first_dejavu_seen = False
default urgent_dejavu_seen = False
default sorting_experienced = False
default scene_sort_count = 0
default full_sort = False
default sort_run_id = ""
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
default opening_note_key = ""
default opening_note_title = ""
default opening_note_text = ""
default opening_note_flags = ()
default returning_from_sort = False

init python:
    import math
    import uuid
    PAPER = "#eee4cf"
    INK = "#383d36"
    ACCENT = "#9ab3ba"
    HAND = "fonts/NanumSmile.ttf"
    URGENT_NOTE = "검은 버튼. 노란 표시등.\n카메라는 카트의 태그를 본다."
    DRAWER_DIARY_PAGES = (
        "{font=fonts/NanumPenScript-Regular.ttf}{color=#59615d}참가 번호 0611. 이건 잊지 말자.\n첫째 날. 차가 따뜻했다. 다들 친절하다. 오래 잤다.\n둘째 날. 어제 뭘 했더라. 수첩에 적힌 건 내 글씨가 맞다.{/color}{/font}",
        "{font=fonts/NanumPenScript-Regular.ttf}{color=#505955}셋째 날. 호출하면 사람이 온다. 온 뒤는 기억이 없다.\n이름이 뭐였지. 이름표 자리만 남았다.\n이걸 읽으면 알아둬. 여기서는 괜찮다는 말이 제일 위험하다.{/color}{/font}"
    )
    DRAWER_DIARY_MONOLOGUES = (
        "이 사람이 어떻게 됐는지는 모른다.",
        "다만 이 방에서 나갈 방법을 찾지 않으면, 나도 이 글의 다음 줄이 된다."
    )
    DRAWER_DIARY_NOTE = "이전 사람의 일기: 호출 → 사람 → 기억이 끊김\n참가 번호 0611"
    TRUST_LINE = "기억이 없다면 이 글부터 믿어. 네 글씨다."
    HINT_DEFINITIONS = {
        "A": {
            "warnings": [
                "호출 누르지 마. 사람이 온다. 도와주는 사람 아님.",
                "{u}호출은 도움 요청이 아니라 신고다. 노크가 너무 빨랐다. 누르지 마.{/u}"
            ],
            "full_sort_detail": "호출은 도움이 아니라 접수였다. 안내자는 노크보다 먼저 와 있었다."
        },
        "B": {
            "warnings": [
                "직원한테 도움 청하지 마. 도와주는 사람 아님.",
                "{u}카메라는 카트를 본다. 문이 열려 있는 동안이 틈이다. 카트 뒤.{/u}"
            ],
            "full_sort_detail": "그는 놀라지 않았다. 도움을 청하는 사람은 처음이 아니었다."
        },
        "C": {
            "warnings": [
                "뛰지 마. 직원은 뛰지 않았다. 뛸 필요가 없어서다.",
                "{u}카메라는 카트를 본다. 문이 열려 있는 동안이 틈이다. 카트 뒤.{/u}"
            ],
            "full_sort_detail": "뛴 사람은 뛰지 않고도 잡혔다. 문은 애초에 닫힐 필요가 없었다."
        }
    }
    FULL_SORT_CARD = (
        "온결 회복 프로그램 · 적응 안정 상담 3회",
        "참가자 0713 · 정리 누적 3회",
        "상태: 등록 요건 충족 → 정식 등록 완료"
    )
    SORT_MONOLOGUES = {
        "normal": (
            "눈꺼풀이 무거워진다. 펜을 놓지 않으려고 손가락에 힘을 준다.",
            "방금 쓴 글씨가 시야 끝에 남아 있다. 저건 다음의 내가 읽을 것이다.",
            "그러니 잊어도 된다. 남겨 두었다."
        ),
        "complete": (
            "펜을 잡으려 했다. 손이 말을 듣지 않는다.",
            "무엇을 적으려던 참이었더라. 생각이 어디론가 흘러간다.",
            "이상하게 편하다. 오래 애쓰던 일이 끝난 것 같다.",
            "가슴께에 이름표가 달린다. 0713.",
            "나는 여기에 오래 있었던 사람 같다."
        )
    }
    OBJECTS = [
        ("window", "창", 185, 371),
        ("cup", "찻잔", 582, 720),
        ("clock", "시계", 638, 317),
        ("door", "문", 962, 473),
        ("light", "표시등", 969, 242),
        ("notice", "안내문", 1286, 383),
        ("call", "호출 버튼", 1166, 489),
        ("drawer", "서랍장", 1733, 660),
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

    def begin_sort_run():
        """새 게임마다 독립적인 정리 횟수 기록을 시작한다."""
        store.sort_run_id = str(uuid.uuid4())
        store.scene_sort_count = 0
        store.full_sort = False
        counts = dict(getattr(persistent, "scene_sort_counts", None) or {})
        counts[store.sort_run_id] = 0
        persistent.scene_sort_counts = counts
        renpy.save_persistent()

    def scene_sort_total():
        """자동 저장을 불러와도 현재 게임의 정리 횟수는 되돌리지 않는다."""
        if not store.sort_run_id:
            store.sort_run_id = str(uuid.uuid4())
            counts = dict(getattr(persistent, "scene_sort_counts", None) or {})
            counts[store.sort_run_id] = store.scene_sort_count
            persistent.scene_sort_counts = counts
            renpy.save_persistent()
        return (getattr(persistent, "scene_sort_counts", None) or {}).get(store.sort_run_id, store.scene_sort_count)

    def set_scene_sort_total(value):
        store.scene_sort_count = value
        counts = dict(getattr(persistent, "scene_sort_counts", None) or {})
        counts[store.sort_run_id] = value
        persistent.scene_sort_counts = counts
        renpy.save_persistent()

    def write_failure(kind):
        store.fail_kind = kind
        store.wrong_choice_history[kind] += 1
        total = scene_sort_total() + 1
        set_scene_sort_total(total)
        store.sorting_experienced = True
        store.full_sort = total >= 3

        # 정리 횟수는 저장되며, 실패 뒤에는 선택 전으로 되돌릴 수 없다.
        renpy.block_rollback()

        if store.full_sort:
            return True

        level = min(total, 2)
        hint = HINT_DEFINITIONS[kind]["warnings"][level - 1]
        store.latest_warning = "\n\n".join((hint, TRUST_LINE))
        store.warnings.append((kind, level, store.latest_warning))
        return False

    def warning_page_text():
        return "\n\n".join(content for _kind, _level, content in store.warnings)

    def reset_scene_sort_count():
        set_scene_sort_total(0)
        store.full_sort = False

    def reset_scene1_state():
        """완전 정리 뒤 장면 1을 새 게임처럼 다시 시작할 상태로 돌린다."""
        set_scene_sort_total(0)
        store.sort_run_id = ""
        store.clues = []
        store.observed = []
        store.notes = []
        store.warnings = []
        store.urgent_note_written = False
        store.first_dejavu_seen = False
        store.urgent_dejavu_seen = False
        store.sorting_experienced = False
        store.full_sort = False
        store.wrong_choice_history = {"A": 0, "B": 0, "C": 0}
        store.fail_kind = "A"
        store.latest_warning = ""
        store.stage = "intro"
        store.wall_minutes = 1258
        store.note_focus = "observations"
        store.skip_locked = False
        store.chapter_complete = False
        store.inspected = ""
        store.call_resolved = False
        store.clock_seconds = 0
        store.opening_note_key = ""
        store.opening_note_title = ""
        store.opening_note_text = ""
        store.opening_note_flags = ()
        store.returning_from_sort = False

    def checkpoint():
        renpy.save("auto-1", extra_info="제1장 · " + ("열린 문" if store.stage == "judgment" else "호출 버튼"))

    def stop_fast_skip():
        renpy.config.skipping = None

    def set_skip_lock(locked):
        store.skip_locked = locked
        renpy.config.allow_skipping = not locked
        if locked:
            stop_fast_skip()

    def restore_skip_lock():
        renpy.config.allow_skipping = not store.skip_locked

    config.after_load_callbacks.append(restore_skip_lock)

    class RoomClock(renpy.Displayable):
        def render(self, width, height, st, at):
            r = renpy.Render(94, 94)
            c = r.canvas()
            c.circle("#141b20", (47, 47), 46)
            c.circle("#697375", (47, 47), 42)
            for i in range(12):
                a = i * math.pi / 6
                c.line("#20272b", (47+math.sin(a)*35,47-math.cos(a)*35), (47+math.sin(a)*39,47-math.cos(a)*39), 2)
            minute = store.wall_minutes % 60
            hour = (store.wall_minutes // 60) % 12
            for a,l,w in ((hour*math.pi/6+minute*math.pi/360,23,3),(minute*math.pi/30,34,2)):
                c.line("#20272b", (47,47), (47+math.sin(a)*l,47-math.cos(a)*l), w)
            c.circle("#20272b", (47,47),3)
            return r
