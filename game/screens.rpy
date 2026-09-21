init -2:
    style default:
        font "fonts/NanumGothic-Regular.ttf"
        size 33
        color "#dce2e5"
        language "korean-with-spaces"
    style button:
        padding (27, 18)
        background Solid("#ffffff08")
        hover_background Solid("#9ab3ba25")
    style button_text:
        size 30
        color "#c7d2d9"
        hover_color "#ffffff"
        insensitive_color "#777a72"
    style main_menu_button is button:
        background Solid("#0b121ab8")
        hover_background Solid("#9ab3ba55")
    style main_menu_button_text is button_text:
        xalign 0.5
    style menu_text is default:
        font "fonts/NanumMyeongjo.ttf"
        kerning 1.0
        outlines [(1, "#0710192b", 0, 1)]
    style menu_title is menu_text:
        kerning 1.6
    style menu_button is button:
        background Solid("#ffffff08")
        hover_background Solid("#9ab3ba25")
    style menu_button_text is button_text:
        font "fonts/NanumMyeongjo.ttf"
        kerning 1.0
        outlines [(1, "#0710192b", 0, 1)]
    style frame:
        background Solid("#101820f5")
        padding (45, 39)
    style bar:
        xsize 510
        ysize 18
        left_bar Solid("#9ab3ba")
        right_bar Solid("#334049")
        thumb Solid("#eee4cf", xsize=18, ysize=33)
    style scrollbar:
        xsize 8
        base_bar Solid("#665c4930")
        thumb Solid("#77695588")
    style vscrollbar is scrollbar

transform soft_in:
    alpha 0.0
    linear .3 alpha 1.0

transform memory_light:
    matrixcolor TintMatrix("#b4c5d1") * BrightnessMatrix(-.12)

transform white_out:
    alpha 0.0
    linear 3.5 alpha .88

transform gentle_close:
    alpha 0.0
    linear 1.0 alpha 1.0

screen room_clock():
    add Transform(RoomClock(), xysize=(104,104)) xpos 587 ypos 266
    add Solid("#8fa99a") xpos 926 ypos 237 xsize 87 ysize 5

screen say(who, what):
    # 한 장의 연속 알파 그라데이션으로 로비와 이어지되, 하단에서는 글자를 읽을 수 있게 한다.
    add Transform("images/dialogue_gradient.png", xysize=(config.screen_width, 303)) xpos 0 ypos (config.screen_height - 303)
    window:
        id "window"
        background None
        xfill True
        yalign 1.0
        ysize 303
        padding (150, 35)
        if who:
            text who id "who" size 26 color ACCENT ypos 0
        text what id "what" ypos (48 if who else 26) xsize 1620 size 36 line_spacing 15
    add Solid("#a1b9bf75") xpos 0 ypos (config.screen_height - 303) xsize config.screen_width ysize 1
    key "game_menu" action ShowMenu("pause_menu")

define diary_reader = Character(None, screen="diary_reading")

# Character의 기본 대사 입력 처리를 사용해 출력 속도와 즉시 표시를 유지한다.
screen diary_reading(who, what):
    add Solid("#060c13b8")
    add Solid("#05090b90") xpos 220 ypos 208 xsize 1496 ysize 694
    add Solid("#343b35") xpos 207 ypos 183 xsize 1506 ysize 708
    add Solid("#a7aa99") xpos 226 ypos 195 xsize 1470 ysize 672
    add Solid("#c7c8b8") xpos 237 ypos 201 xsize 1446 ysize 654
    add Solid("#777d6b60") xpos 265 ypos 219 xsize 9 ysize 612
    add Solid("#e0dfce45") xpos 280 ypos 219 xsize 3 ysize 612
    for line_y in (426, 532, 638):
        add Solid("#747d6925") xpos 321 ypos line_y xsize 1290 ysize 2
    text "서랍 안쪽에서 발견한 일기" xpos 321 ypos 263 size 24 color "#626b60"
    # 일반 say 화면의 하단 창 및 centered의 앵커를 상속하지 않는다.
    window:
        id "window"
        background None
        xpos 321 ypos 358 xanchor 0 yanchor 0
        xsize 1290 ysize 330 padding (0, 0)
        text what:
            id "what"
            xpos 0 ypos 0 xanchor 0 yanchor 0
            xsize 1290 size 44 line_spacing 50
            font "fonts/NanumPenScript-Regular.ttf"
            color "#505955"
            slow_cps True
            slow_abortable True
    key "game_menu" action ShowMenu("pause_menu")

screen main_menu():
    tag menu
    add Transform("images/menu_corridor.png", xysize=(1920,1080))
    add Solid("#07101952")
    add Transform("images/title_logo.png", xysize=(960,320), alpha=.92) xpos 480 ypos 105
    default hovered_menu_item = ""
    fixed:
        xalign .5 ypos 500 xsize 510 ysize 430
        for item_id, label, menu_action, item_ypos in (
            ("start_game", "시작하기", Start(), 0),
            ("load_game", "불러오기", ShowMenu("load"), 120),
            ("preferences", "설정", ShowMenu("preferences"), 240),
            ("quit_game", "종료", Quit(confirm=False), 360),
        ):
            button:
                id item_id
                ypos item_ypos
                xfill True ysize 70 padding (0, 0)
                background None
                hover_background None
                action menu_action
                hovered SetScreenVariable("hovered_menu_item", item_id)
                unhovered SetScreenVariable("hovered_menu_item", "")
                fixed:
                    text ("{b}" + label + "{/b}" if hovered_menu_item == item_id else label) xalign .5 yalign .45 size (38 if hovered_menu_item == item_id else 33) color ("#e4eceb" if hovered_menu_item == item_id else "#aebbbb") font "fonts/NanumMyeongjo.ttf" kerning 1.0 outlines [(1, "#0710192b", 0, 1)]

label main_menu:
    call screen main_menu
    return

screen investigation():
    modal True
    default hovered_object = ""
    for key, title, x, y in OBJECTS:
        button:
            id ("inspect_" + key)
            xpos x-63 ypos y-35 xsize 135 ysize 93
            padding (0,0)
            background None
            hover_background Solid("#b7d1e126")
            hovered SetScreenVariable("hovered_object", key)
            unhovered SetScreenVariable("hovered_object", "")
            action Return(key)
            vbox:
                xalign .5 spacing 6
                if persistent.show_hotspots or hovered_object == key:
                    text ("·" if key in observed else "◇") xalign .5 size 35 color ("#9caeb7" if key in observed else "#e5eef3")
                    text title xalign .5 size 23 outlines [(3,"#101720ee",0,0)]
    frame:
        xpos 69 ypos 900 xsize 1782 ysize 132
        padding (36, 23)
        hbox:
            spacing 36
            vbox:
                spacing 11
                text "방 안을 살핀다" size 32
                text "물건을 클릭해 조사하세요. 서두를 필요는 없습니다." size 21 color "#a9b4a5"
            null width 315
            textbutton "수첩을 펼친다" id "open_notebook" action Show("notebook") text_size 26
            textbutton "설정" action ShowMenu("preferences") text_size 26
    key "K_n" action Show("notebook")
    key "game_menu" action ShowMenu("pause_menu")

screen notebook(menu_mode=False):
    modal True
    zorder 150
    default tab = note_focus
    add Solid("#081311b8")
    add Solid("#272d24") xpos 243 ypos 87 xsize 1445 ysize 930
    add Solid("#d1c4a8") xpos 255 ypos 75 xsize 1410 ysize 918
    add Solid("#eee4cf") xpos 273 ypos 75 xsize 1388 ysize 903
    add Solid("#9c8a6538") xpos 933 ypos 96 xsize 18 ysize 864
    for y in range(257, 929, 53):
        add Solid("#86785b26") xpos 311 ypos y xsize 1307 ysize 2
    text "온결  /  회복 기록" xpos 326 ypos 117 size 20 color "#777962"
    text "0713" xpos 1485 ypos 114 size 33 color INK
    text "김수혁의 수첩" xpos 323 ypos 164 font HAND size 57 color INK
    text "적어 두지 않으면 불안하다." xpos 1038 ypos 168 font HAND size 45 color "#7c7966"
    hbox:
        xpos 320 ypos 245 spacing 23
        textbutton "관찰" action SetScreenVariable("tab", "observations") text_color INK text_hover_color "#825c35" text_size 27
        textbutton "다음의 나에게" action SetScreenVariable("tab", "warnings") text_color INK text_hover_color "#825c35" text_size 27
    viewport:
        id "notebook_scroll"
        xpos 323 ypos 326 xsize 1284 ysize 513
        mousewheel True draggable True scrollbars "vertical"
        vbox:
            xsize 1232 spacing 35
            if tab == "observations":
                for key, title, content in notes:
                    vbox:
                        spacing 9
                        text title color "#7d745b" size 21
                        text content color INK font HAND size 47 line_spacing 5
                if not notes:
                    text "아직 빈 페이지다." font HAND size 48 color INK
            else:
                if not warnings:
                    text "아직 아무것도 적혀 있지 않다." font HAND size 48 color INK
                for kind, level, content in warnings:
                    vbox:
                        spacing 14
                        text "접힌 페이지" size 21 color "#81725b"
                        text content font HAND size (50 if level > 1 else 47) color "#5c3d30" line_spacing 6
    text "이 수첩은 내 손을 떠나지 않았다." xpos 326 ypos 909 font HAND size 36 color "#7b765e"
    textbutton "수첩 덮기" id "close_notebook" xpos 1355 ypos 890 action (Return() if menu_mode else Hide("notebook")) text_color INK text_hover_color "#a07146" text_size 27
    key "K_n" action (Return() if menu_mode else Hide("notebook"))
    key "game_menu" action ShowMenu("pause_menu")

screen handwritten(content, title="수첩에 적는다", reveal=True, urgent=False):
    modal True
    zorder 120
    add Solid("#0c171773")
    frame:
        xalign .5 yalign .46 xsize 1193
        padding (72,51)
        background Solid(PAPER)
        vbox:
            spacing 33
            text title size 23 color "#7f765f"
            # True는 사용자의 "글자 표시 속도" 환경 설정을 그대로 사용한다.
            text content font HAND size (54 if urgent else 48) color ("#4d2f25" if urgent else INK) line_spacing 9 slow_cps True slow_abortable True
            textbutton "펜을 놓는다" id "finish_writing" xalign 1.0 action Return() text_size 24 text_color "#6a654e" text_hover_color "#302f24"
    key "game_menu" action ShowMenu("pause_menu")

screen call_options():
    modal True
    frame:
        xpos 285 ypos 702 xsize 1350
        vbox:
            spacing 24
            text "서랍에서 읽은 일기가 마음에 걸린다." size 33
            hbox:
                spacing 30
                textbutton ("누른다" + ("  ·  지워지지 않은 경고" if wrong_choice_history["A"] else "")) id "call_yes" action Return(True)
                textbutton "누르지 않는다" id "call_no" action Return(False)
                textbutton "수첩" action Show("notebook")
    key "K_n" action Show("notebook")
    key "game_menu" action ShowMenu("pause_menu")

screen drawer_search():
    modal True
    frame:
        xpos 285 ypos 702 xsize 1350
        vbox:
            spacing 24
            text "서랍 안쪽이 바깥에서 본 것보다 얕다." size 33
            textbutton "안쪽을 더듬는다" id "search_drawer_inner" action Return()
    key "game_menu" action ShowMenu("pause_menu")

screen judgment():
    modal True
    frame:
        xpos 953 ypos 500 xsize 902
        padding (41,35)
        vbox:
            spacing 20
            text "직원은 등을 돌렸다." size 36
            text "문은 열려 있다. 수첩에 남긴 것을 떠올린다." size 24 color "#b7c1ac"
            null height 5
            textbutton ("01   직원에게 다가가 도와달라고 말한다." + ("  ↺" if wrong_choice_history["B"] else "")) id "judge_B" action Return("B") text_size 29 xfill True
            textbutton ("02   직원 옆을 지나 복도로 뛰어나간다." + ("  ↺" if wrong_choice_history["C"] else "")) id "judge_C" action Return("C") text_size 29 xfill True
            textbutton "03   카트 뒤에 몸을 낮추고 빠져나간다." id "judge_success" action Return("success") sensitive (has("black_button") and has("camera_cart")) text_size 29 xfill True
            hbox:
                spacing 39
                textbutton "수첩을 펼친다" action Show("notebook") text_size 23
                text "기록 저장됨" size 20 color "#a9b78e" yalign .5
    if wrong_choice_history["B"] or wrong_choice_history["C"]:
        text "↺  수첩에 경고가 남은 선택" xpos 1011 ypos 1019 size 20 color "#c6b593"
    key "K_n" action Show("notebook")
    key "game_menu" action ShowMenu("pause_menu")

screen sorting_card(is_full_sort=False, kind="A"):
    modal True
    add Solid("#bfc8cc")
    vbox:
        xalign .5 yalign .46 spacing 39
        if is_full_sort:
            text FULL_SORT_CARD[0] color "#4b5b66" size 27 xalign .5
            text FULL_SORT_CARD[1] color "#4b5b66" size 27 xalign .5
            null height 12
            text FULL_SORT_CARD[2] color "#283c4a" size 42 xalign .5
            text HINT_DEFINITIONS[kind]["full_sort_detail"] color "#62707a" size 21 xalign .5
        else:
            text "온결 회복 프로그램" color "#4b5b66" size 27 xalign .5
            text "적응 안정 상담" color "#283c4a" size 53 xalign .5
            null height 18
            text "참가자 0713   /   상태: 평온" color "#4b5b66" size 27 xalign .5
            text "정리 완료" color "#455b68" size 38 xalign .5
    timer 3.0 action Return()
    key "game_menu" action ShowMenu("pause_menu")

screen end_chapter():
    modal True
    add Solid("#081716")
    vbox:
        xalign .5 yalign .45 spacing 39
        text "제1장  /  괜찮아지는 방" size 27 color "#a8b593" xalign .5
        text "문 하나를 지나왔다." size 59 xalign .5
        text "벽 너머에는 누군가 있다." size 33 color "#b8c2b0" xalign .5
        null height 30
        text "이번 플레이 버전은 여기까지입니다." size 23 color "#839487" xalign .5
        textbutton "수첩을 다시 읽는다" action Show("notebook") xalign .5
        textbutton "처음 화면으로" id "chapter_done" action MainMenu(confirm=False) xalign .5
    key "game_menu" action ShowMenu("pause_menu")

screen menu_tabs():
    style_prefix "menu"
    hbox:
        spacing 16
        if not main_menu:
            textbutton "수첩" action ShowMenu("notebook_menu") text_size 25
            textbutton "기록" action ShowMenu("history") text_size 25
            textbutton "저장" action ShowMenu("save") text_size 25
        textbutton "불러오기" action ShowMenu("load") text_size 25
        textbutton "설정" action ShowMenu("preferences") text_size 25
        if not main_menu:
            textbutton "인물" action ShowMenu("characters") text_size 25

screen menu_shell(title):
    style_prefix "menu"
    add Solid("#0f1e1df7")
    text title xpos 117 ypos 65 size 53 style "menu_title"
    textbutton ("돌아가기" if main_menu else "계속하기") id "menu_back" xpos 1605 ypos 65 action Return() text_size 27
    fixed:
        xpos 117 ypos 139 xsize 1550 ysize 70
        use menu_tabs
    key "game_menu" action Return()
    transclude

screen pause_menu():
    tag menu
    use menu_shell("메뉴"):
        vbox:
            xalign .5 ypos 380 spacing 30
            text "잠시, 숨을 고른다." font HAND size 54 color ACCENT
            textbutton "계속하기" action Return() xalign .5
            textbutton "처음 화면으로" action MainMenu() xalign .5

screen notebook_menu():
    tag menu
    use notebook(menu_mode=True)
    fixed:
        xpos 310 ypos 0 xsize 1400 ysize 70
        use menu_tabs
    key "game_menu" action Return()

screen characters():
    tag menu
    style_prefix "menu"
    default selected_person = "suhyeok"
    use menu_shell("인물"):
        vbox:
            xpos 130 ypos 270 spacing 24
            textbutton "김수혁" action SetScreenVariable("selected_person", "suhyeok")
            textbutton "윤서아" action SetScreenVariable("selected_person", "seoa")
            if has("diary_found"):
                textbutton "기록 속 인물 · 0611" action SetScreenVariable("selected_person", "0611")
        add Solid("#222e32") xpos 580 ypos 260 xsize 540 ysize 660
        if selected_person == "suhyeok":
            add Transform("images/suhyeok_profile.png", crop=(0, 0, 1024, 1250), xysize=(540, 660)) xpos 580 ypos 260
        elif selected_person == "seoa":
            add Transform("images/seoa_cutout_neutral.png", crop=(0, 0, 1122, 1370), xysize=(540, 660)) xpos 580 ypos 260
        else:
            # 신원을 암시하지 않는 임시 상반신 실루엣.
            add "images/unknown_profile.svg" xpos 580 ypos 260
            text "?" xpos 819 ypos 510 size 68 color "#7b8b8d"
        vbox:
            xpos 1190 ypos 330 xsize 590 spacing 35
            if selected_person == "suhyeok":
                text "김수혁" size 46 style "menu_title"
                text "참가 번호 0713" size 27 color ACCENT
                text "뭐든 적어 두는 사람.\n적어 두지 않으면 불안하다." size 30 line_spacing 18
            elif selected_person == "seoa":
                text "윤서아" size 46 style "menu_title"
                text "내 말을 끝까지 들어주던 사람." size 30
                text "온결의 회복 프로그램을 소개해 주었다." size 28
            else:
                text "기록 속 인물 · 0611" size 42 style "menu_title"
                text "이름과 얼굴은 아직 모른다." size 29 color ACCENT
                text "서랍 안쪽에 일기를 남겼다.\n호출 뒤의 기억이 없다고 적었다." size 28 line_spacing 18

screen preferences():
    tag menu
    style_prefix "menu"
    use menu_shell("환경 설정"):
        viewport:
            xpos 128 ypos 239 xsize 1650 ysize 790
            mousewheel True
            draggable False
            scrollbars "vertical"
            hbox:
                spacing 218
                vbox:
                    spacing 33
                    text "화면" size 33 color ACCENT
                    hbox:
                        textbutton "창 모드" action Preference("display","window")
                        textbutton "전체 화면" action Preference("display","fullscreen")
                    text "글자 표시 속도" size 30
                    bar:
                        # 0(즉시 표시)을 제외해, 가장 빠른 설정에서도 타이핑이 보인다.
                        value FieldValue(_preferences, "text_cps", min=TEXT_CPS_MIN, max=TEXT_CPS_MAX, step=1, force_step=True, style="slider")
                        xsize 510
                        ysize 24
                        left_bar Solid("#9ab3ba")
                        right_bar Solid("#334049")
                        thumb Solid("#eee4cf", xsize=20, ysize=34)
                    hbox:
                        xsize 510
                        text "느리게" size 18 color "#83949c"
                        text "빠르게" xalign 1.0 size 18 color "#83949c"
                    textbutton "조사 위치 표시" action ToggleField(persistent,"show_hotspots")
                    text "대사·기록 넘기기: 클릭 / Enter / Space\n수첩: N   ·   메뉴: Esc\n읽은 문장만 빠르게: Ctrl / Tab" size 24 line_spacing 15 color "#9daea1"
                vbox:
                    spacing 33
                    text "소리" size 33 color ACCENT
                    vbox:
                        spacing 33
                        text "효과음 · 환경음" size 30 color ("#627078" if (_preferences.get_mute("music") and _preferences.get_mute("sfx")) else "#dce2e5")
                        if _preferences.get_mute("music") and _preferences.get_mute("sfx"):
                            bar:
                                value StaticValue(_preferences.get_mixer("sfx"), 1.0)
                                xsize 510
                                ysize 24
                                left_bar Solid("#4c5b63")
                                right_bar Solid("#29343b")
                                thumb Solid("#69767b", xsize=20, ysize=34)
                        else:
                            bar:
                                value Preference("sound volume")
                                xsize 510
                                ysize 24
                                left_bar Solid("#9ab3ba")
                                right_bar Solid("#334049")
                                thumb Solid("#eee4cf", xsize=20, ysize=34)
                        hbox:
                            xsize 510
                            text "작게" size 18 color ("#58666d" if (_preferences.get_mute("music") and _preferences.get_mute("sfx")) else "#83949c")
                            text "크게" xalign 1.0 size 18 color ("#58666d" if (_preferences.get_mute("music") and _preferences.get_mute("sfx")) else "#83949c")
                        text "안내 음악" size 30 color ("#627078" if (_preferences.get_mute("music") and _preferences.get_mute("sfx")) else "#dce2e5")
                        if _preferences.get_mute("music") and _preferences.get_mute("sfx"):
                            bar:
                                value StaticValue(_preferences.get_mixer("music"), 1.0)
                                xsize 510
                                ysize 24
                                left_bar Solid("#4c5b63")
                                right_bar Solid("#29343b")
                                thumb Solid("#69767b", xsize=20, ysize=34)
                        else:
                            bar:
                                value Preference("music volume")
                                xsize 510
                                ysize 24
                                left_bar Solid("#9ab3ba")
                                right_bar Solid("#334049")
                                thumb Solid("#eee4cf", xsize=20, ysize=34)
                        hbox:
                            xsize 510
                            text "작게" size 18 color ("#58666d" if (_preferences.get_mute("music") and _preferences.get_mute("sfx")) else "#83949c")
                            text "크게" xalign 1.0 size 18 color ("#58666d" if (_preferences.get_mute("music") and _preferences.get_mute("sfx")) else "#83949c")
                    textbutton ("음소거 해제" if (_preferences.get_mute("music") and _preferences.get_mute("sfx")) else "전체 음소거") action Preference("all mute", "toggle")
                    if _preferences.get_mute("music") and _preferences.get_mute("sfx"):
                        text "전체 음소거 적용 중" size 21 color "#829199"
                    text "인물 음성은 사용하지 않습니다.\n안내 음악을 끄고 플레이해도 됩니다." size 24 line_spacing 14 color "#9daea1"
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
            xpos 123 ypos 213 spacing 33
            hbox:
                spacing 23
                textbutton "자동 기록" action FilePage("auto")
                for page in range(1,4):
                    textbutton str(page) action FilePage(page)
            grid 3 2:
                spacing 33
                for slot in range(1,7):
                    button:
                        id ("slot_"+str(slot))
                        xsize 524 ysize 288
                        action FileAction(slot)
                        vbox:
                            spacing 11
                            add FileScreenshot(slot) xsize 465 ysize 185
                            text FileTime(slot, format="%m월 %d일 %H:%M", empty="빈 기록") size 23

screen history():
    tag menu
    use menu_shell("지나온 문장"):
        viewport:
            xpos 147 ypos 219 xsize 1605 ysize 761 mousewheel True draggable True scrollbars "vertical" yinitial 1.0
            vbox:
                spacing 36
                for item in _history_list:
                    vbox:
                        spacing 12
                        if item.who:
                            text item.who size 23 color ACCENT
                        text item.what size 32 xsize 1530 line_spacing 8 substitute False

screen confirm(message, yes_action, no_action):
    modal True
    zorder 200
    add Solid("#07100cbb")
    frame:
        xalign .5 yalign .5 xsize 990
        vbox:
            spacing 41
            text message size 35
            hbox:
                spacing 38
                textbutton "진행" action yes_action
                textbutton "취소" action no_action

screen notify(message):
    zorder 200
    frame:
        xpos 56 ypos 93
        text message size 24
    timer 2.0 action Hide("notify")

screen skip_indicator():
    zorder 110
    text "읽은 문장 넘기는 중" xpos 1545 ypos 33 size 23 color ACCENT

screen memory_portrait(expression, speaking=False):
    # 대사창 뒤에 로비와 상반신을 배치한다. 수혁의 차례에는 약한 음영만 준다.
    zorder -1
    add Transform("images/lobby_day.png", xysize=(1920, 1080), matrixcolor=SaturationMatrix(.65))
    add Transform(
        "images/seoa_lobby_" + expression + ".png",
        xysize=(500, 646),
        matrixcolor=(SaturationMatrix(.8) if speaking else SaturationMatrix(.6) * BrightnessMatrix(-.12))
    ) xpos 1280 ypos 224

screen threshold_still():
    # 열린 문을 세밀하게 움직이는 대신, 가까워진 시야의 정지 화면.
    add Solid("#080f17")
    add Solid("#111e29") xpos 492 ypos 113 xsize 381 ysize 684
    add Solid("#172735") xpos 507 ypos 126 xsize 353 ysize 657
    add Solid("#23313b") xpos 525 ypos 138 xsize 3 ysize 645
    add Solid("#919078") xpos 635 ypos 84 xsize 92 ysize 5
    text "문틈에서 새어 들어오는 차가운 빛." xpos 125 ypos 687 size 24 color "#6f8796"

screen notice_page():
    modal True
    add Solid("#060c13b0")
    frame:
        xalign .5 yalign .45 xsize 1080 padding (81,60)
        background Solid("#c7cdcd")
        vbox:
            spacing 36
            text "온결   /   회복 프로그램" size 23 color "#58696e"
            text "참가자 안내" size 48 color "#293d48"
            null height 12
            text "이곳에서는 서두르지 않아도 됩니다.\n저녁 배식은 21시 10분입니다.\n안내자는 항상 두 번 노크합니다.\n불편하신 점은 호출 버튼으로 알려 주세요.\n언제든 도와드리겠습니다.\n스스로를 탓하지 마세요." size 33 color "#2c3b44" line_spacing 21 slow_cps True slow_abortable True
            textbutton "안내문에서 눈을 뗀다" id "close_notice" action Return() text_color "#465e6e" text_hover_color "#1b2e3d" xalign 1.0 text_size 24
    key "game_menu" action ShowMenu("pause_menu")
