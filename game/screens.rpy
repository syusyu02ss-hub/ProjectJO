init -2:
    style default:
        font "fonts/NanumGothic-Regular.ttf"
        size 22
        color "#eee6d6"
        language "korean-with-spaces"
    style button:
        padding (18, 12)
        background Solid("#ffffff08")
        hover_background Solid("#d1b98230")
    style button_text:
        size 20
        color "#ded8c8"
        hover_color "#ffffff"
        insensitive_color "#777a72"
    style frame:
        background Solid("#131c1cf2")
        padding (30, 26)
    style bar:
        xsize 340
        ysize 12
        left_bar Solid("#c8b58a")
        right_bar Solid("#43504a")
        thumb Solid("#eee4cf", xsize=12, ysize=22)
    style scrollbar:
        xsize 5
        base_bar Solid("#665c4930")
        thumb Solid("#77695588")
    style vscrollbar is scrollbar

transform soft_in:
    alpha 0.0
    linear .3 alpha 1.0

transform memory_light:
    matrixcolor TintMatrix("#fff3d8") * BrightnessMatrix(.08)

transform white_out:
    alpha 0.0
    linear 3.5 alpha .88

transform gentle_close:
    alpha 0.0
    linear 1.0 alpha 1.0

screen room_clock():
    add RoomClock() xpos 458 ypos 72
    if stage != "delivery" and stage != "judgment":
        add Solid("#b5cc94") xpos 702 ypos 32 xsize 21 ysize 5

screen say(who, what):
    window:
        id "window"
        background Solid("#101918ef")
        xpos 0 ypos 538 xsize 1280 ysize 182
        padding (112, 22)
        if who:
            text who id "who" size 17 color "#c8b58a" ypos 0
        text what id "what" xpos 0 ypos (32 if who else 17) xsize 1056 size 24 line_spacing 9
    if not skip_locked:
        text "클릭 / Enter" xpos 1095 ypos 688 size 12 color "#9caa9b"
    use quick_menu

screen quick_menu():
    zorder 90
    if not main_menu and not skip_locked:
        hbox:
            xpos 32 ypos 13 spacing 6
            textbutton "수첩" action Show("notebook") text_size 15 padding (12, 7)
            textbutton "기록" action ShowMenu("history") text_size 15 padding (12, 7)
            textbutton "저장" action ShowMenu("save") text_size 15 padding (12, 7)
            textbutton "설정" action ShowMenu("preferences") text_size 15 padding (12, 7)
            textbutton "읽은 문장 넘기기" action Skip() text_size 15 padding (12, 7)
        key "K_n" action Show("notebook")

screen main_menu():
    tag menu
    add "images/room.png" xysize (1280,720)
    add Solid("#102221aa")
    add Solid("#0b171dcc") xpos 0 ypos 0 xsize 590 ysize 720
    vbox:
        xpos 92 ypos 98 spacing 20
        text "O N G Y E O L" size 17 color "#c9b990"
        null height 10
        text "괜찮아지는 방" size 48 color "#f4ead5"
        text "이곳에서는 서두르지 않아도 됩니다." size 18 color "#b8c0ad"
        null height 42
        textbutton "처음부터" id "start_game" action Start() xsize 335
        textbutton "이어서" id "continue_game" action FileLoad("auto-1", confirm=False) sensitive FileLoadable("auto-1") xsize 335
        textbutton "기록 불러오기" action ShowMenu("load") xsize 335
        textbutton "환경 설정" action ShowMenu("preferences") xsize 335
        textbutton "나가기" action Quit(confirm=False) xsize 335
    text "온결 회복 프로그램     /     참가자 0713" xpos 94 ypos 630 size 15 color "#b7bba8"
    text "제1장 플레이 버전  ·  0.1.0" xpos 94 ypos 661 size 13 color "#9caa9b"

screen investigation():
    modal True
    default hovered_object = ""
    for key, title, x, y in OBJECTS:
        button:
            id ("inspect_" + key)
            xpos x-40 ypos max(50, y-27) xsize 85 ysize 65
            background None
            hover_background Solid("#f3e5b726")
            hovered SetScreenVariable("hovered_object", key)
            unhovered SetScreenVariable("hovered_object", "")
            action Return(key)
            vbox:
                xalign .5 spacing 4
                if persistent.show_hotspots or hovered_object == key:
                    text ("·" if key in observed else "◇") xalign .5 size 23 color ("#ccd4b5" if key in observed else "#fff4d7")
                    text title xalign .5 size 15 outlines [(2,"#1b221bcc",0,0)]
    frame:
        xpos 46 ypos 605 xsize 1188 ysize 82
        padding (22, 15)
        hbox:
            spacing 24
            vbox:
                spacing 7
                text "방 안을 살핀다" size 21
                text "물건을 클릭해 조사하세요. 서두를 필요는 없습니다." size 14 color "#a9b4a5"
            null width 310
            textbutton "수첩을 펼친다" id "open_notebook" action Show("notebook") text_size 17
            textbutton "설정" action ShowMenu("preferences") text_size 17
    key "K_n" action Show("notebook")
    key "game_menu" action ShowMenu("preferences")

screen notebook():
    modal True
    zorder 150
    default tab = note_focus
    add Solid("#081311b8")
    add Solid("#272d24") xpos 162 ypos 58 xsize 963 ysize 620
    add Solid("#d1c4a8") xpos 170 ypos 50 xsize 940 ysize 612
    add Solid("#eee4cf") xpos 182 ypos 50 xsize 925 ysize 602
    add Solid("#9c8a6538") xpos 622 ypos 64 xsize 12 ysize 576
    for y in range(171, 619, 35):
        add Solid("#86785b26") xpos 207 ypos y xsize 871 ysize 1
    text "온결  /  회복 기록" xpos 217 ypos 78 size 13 color "#777962"
    text "0713" xpos 990 ypos 76 size 22 color INK
    text "김수혁의 수첩" xpos 215 ypos 109 font HAND size 38 color INK
    text "적어 두지 않으면 불안하다." xpos 692 ypos 112 font HAND size 30 color "#7c7966"
    hbox:
        xpos 213 ypos 163 spacing 15
        textbutton "관찰" action SetScreenVariable("tab", "observations") text_color INK text_hover_color "#825c35" text_size 18
        textbutton "다음의 나에게" action SetScreenVariable("tab", "warnings") text_color INK text_hover_color "#825c35" text_size 18
    viewport:
        id "notebook_scroll"
        xpos 215 ypos 217 xsize 856 ysize 342
        mousewheel True draggable True scrollbars "vertical"
        vbox:
            xsize 821 spacing 23
            if tab == "observations":
                for key, title, content in notes:
                    vbox:
                        spacing 6
                        text title color "#7d745b" size 14
                        text content color INK font HAND size 31 line_spacing 3
                if not notes:
                    text "아직 빈 페이지다." font HAND size 32 color INK
            else:
                if not warnings:
                    text "아직 아무것도 적혀 있지 않다." font HAND size 32 color INK
                for kind, level, content in reversed(warnings):
                    vbox:
                        spacing 9
                        text "접힌 페이지" size 14 color "#81725b"
                        text content font HAND size (33 if level > 1 else 31) color "#5c3d30" line_spacing 4
    text "이 수첩은 내 손을 떠나지 않았다." xpos 217 ypos 606 font HAND size 24 color "#7b765e"
    textbutton "수첩 덮기" id "close_notebook" xpos 903 ypos 593 action Hide("notebook") text_color INK text_hover_color "#a07146" text_size 18
    key "K_n" action Hide("notebook")
    key "game_menu" action Hide("notebook")

screen handwritten(content, title="수첩에 적는다", reveal=True):
    modal True
    zorder 120
    add Solid("#0c171773")
    frame:
        xalign .5 yalign .46 xsize 795
        padding (48,34)
        background Solid(PAPER)
        vbox:
            spacing 22
            text title size 15 color "#7f765f"
            text content font HAND size 36 color INK line_spacing 7 slow_cps (18 if reveal else 0)
            textbutton "펜을 놓는다" id "finish_writing" xalign 1.0 action Return() text_size 16 text_color "#6a654e" text_hover_color "#302f24"

screen call_options():
    modal True
    frame:
        xpos 190 ypos 468 xsize 900
        vbox:
            spacing 16
            text "서랍에서 본 자국이 마음에 걸린다." size 22
            hbox:
                spacing 20
                textbutton ("누른다" + ("  ·  지워지지 않은 경고" if wrong_choice_history["A"] else "")) id "call_yes" action Return(True)
                textbutton "누르지 않는다" id "call_no" action Return(False)
                textbutton "수첩" action Show("notebook")
    key "K_n" action Show("notebook")

screen judgment():
    modal True
    frame:
        xpos 635 ypos 333 xsize 601
        padding (27,23)
        vbox:
            spacing 13
            text "직원은 등을 돌렸다." size 24
            text "문은 열려 있다. 수첩에 남긴 것을 떠올린다." size 16 color "#b7c1ac"
            null height 3
            textbutton ("01   직원에게 다가가 도와달라고 말한다." + ("  ↺" if wrong_choice_history["B"] else "")) id "judge_B" action Return("B") text_size 19 xfill True
            textbutton ("02   직원 옆을 지나 복도로 뛰어나간다." + ("  ↺" if wrong_choice_history["C"] else "")) id "judge_C" action Return("C") text_size 19 xfill True
            textbutton "03   카트 뒤에 몸을 낮추고 빠져나간다." id "judge_success" action Return("success") sensitive (has("black_button") and has("camera_cart")) text_size 19 xfill True
            hbox:
                spacing 26
                textbutton "수첩을 펼친다" action Show("notebook") text_size 15
                text "기록 저장됨" size 13 color "#a9b78e" yalign .5
    if wrong_choice_history["B"] or wrong_choice_history["C"]:
        text "↺  수첩에 경고가 남은 선택" xpos 674 ypos 679 size 13 color "#c6b593"
    key "K_n" action Show("notebook")
    key "game_menu" action ShowMenu("preferences")

screen sorting_card():
    modal True
    add Solid("#f2f0e8")
    vbox:
        xalign .5 yalign .46 spacing 26
        text "온결 회복 프로그램" color "#747e6b" size 18 xalign .5
        text "적응 안정 상담" color "#384638" size 35 xalign .5
        null height 12
        text "참가자 0713   /   상태: 평온" color "#6f7968" size 18 xalign .5
        text "정리 완료" color "#74856b" size 25 xalign .5
    timer 3.0 action Return()

screen end_chapter():
    modal True
    add Solid("#081716")
    vbox:
        xalign .5 yalign .45 spacing 26
        text "제1장  /  괜찮아지는 방" size 18 color "#a8b593" xalign .5
        text "문 하나를 지나왔다." size 39 xalign .5
        text "벽 너머에는 누군가 있다." size 22 color "#b8c2b0" xalign .5
        null height 20
        text "이번 플레이 버전은 여기까지입니다." size 15 color "#839487" xalign .5
        textbutton "수첩을 다시 읽는다" action Show("notebook") xalign .5
        textbutton "처음 화면으로" id "chapter_done" action MainMenu(confirm=False) xalign .5

screen menu_shell(title):
    add Solid("#0f1e1df7")
    text title xpos 78 ypos 55 size 35
    textbutton "돌아가기" id "menu_back" xpos 1070 ypos 50 action Return() text_size 18
    key "game_menu" action Return()
    transclude

screen preferences():
    tag menu
    use menu_shell("환경 설정"):
        hbox:
            xpos 85 ypos 159 spacing 145
            vbox:
                spacing 22
                text "화면" size 22 color ACCENT
                hbox:
                    textbutton "창 모드" action Preference("display","window")
                    textbutton "전체 화면" action Preference("display","fullscreen")
                text "글자 표시 속도" size 20
                bar value Preference("text speed")
                textbutton "조사 위치 표시" action ToggleField(persistent,"show_hotspots")
                textbutton "빛 전환 줄이기" action ToggleField(persistent,"reduced_motion")
                text "대사 넘기기: 클릭 / Enter / Space\n수첩: N   ·   설정: Esc\n읽은 문장만 빠르게: Ctrl / Tab" size 16 line_spacing 10 color "#9daea1"
            vbox:
                spacing 22
                text "소리" size 22 color ACCENT
                text "효과음 · 환경음" size 20
                bar value Preference("sound volume")
                text "안내 음악" size 20
                bar value Preference("music volume")
                textbutton "전체 음소거" action Preference("all mute", "toggle")
                text "인물 음성은 사용하지 않습니다.\n안내 음악을 끄고 플레이해도 됩니다." size 16 line_spacing 9 color "#9daea1"
                if not main_menu:
                    textbutton "처음 화면으로" action MainMenu()
                textbutton "게임 종료" action Quit()

screen save():
    tag menu
    use file_slots("기록 저장")

screen load():
    tag menu
    use file_slots("기록 불러오기")

screen file_slots(title):
    use menu_shell(title):
        vbox:
            xpos 82 ypos 142 spacing 22
            hbox:
                spacing 15
                textbutton "자동 기록" action FilePage("auto")
                for page in range(1,4):
                    textbutton str(page) action FilePage(page)
            grid 3 2:
                spacing 22
                for slot in range(1,7):
                    button:
                        id ("slot_"+str(slot))
                        xsize 349 ysize 192
                        action FileAction(slot)
                        vbox:
                            spacing 7
                            add FileScreenshot(slot) xsize 310 ysize 123
                            text FileTime(slot, format="%m월 %d일 %H:%M", empty="빈 기록") size 15

screen history():
    tag menu
    use menu_shell("지나온 문장"):
        viewport:
            xpos 98 ypos 146 xsize 1070 ysize 507 mousewheel True draggable True scrollbars "vertical" yinitial 1.0
            vbox:
                spacing 24
                for item in _history_list:
                    vbox:
                        spacing 8
                        if item.who:
                            text item.who size 15 color ACCENT
                        text item.what size 21 xsize 1020 line_spacing 5 substitute False

screen confirm(message, yes_action, no_action):
    modal True
    zorder 200
    add Solid("#07100cbb")
    frame:
        xalign .5 yalign .5 xsize 660
        vbox:
            spacing 27
            text "이대로 진행할까요?" size 26
            text "저장하지 않은 진행은 남지 않을 수 있습니다." size 18 color "#bdc5b4"
            hbox:
                spacing 25
                textbutton "진행" action yes_action
                textbutton "취소" action no_action

screen notify(message):
    zorder 200
    frame:
        xpos 37 ypos 62
        text message size 16
    timer 2.0 action Hide("notify")

screen skip_indicator():
    zorder 110
    text "읽은 문장 넘기는 중" xpos 1030 ypos 22 size 15 color ACCENT

