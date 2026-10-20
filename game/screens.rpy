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

screen say(who, what):
    # 거의 검정에 가까운 연속 그라데이션으로, 배경은 희미하게만 남기고 글자를 안정적으로 읽게 한다.
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
    add Solid("#b7c5c9a8") xpos 0 ypos (config.screen_height - 303) xsize config.screen_width ysize 1
    key "game_menu" action ShowMenu("pause_menu")

screen ctc():
    # Ren'Py가 글자 출력 완료 시에만 표시하고 다음 대사에서 자동으로 지운다.
    zorder 100
    text "▼" xpos 1740 ypos 1020 size 18 color "#aab8c0" outlines []

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
            padding (0, 0)
            background None
            hover_background (Solid("#b7d1e126") if config.developer else None)
            hovered SetScreenVariable("hovered_object", key)
            unhovered SetScreenVariable("hovered_object", "")
            action Return(key)
            vbox:
                xalign .5 spacing 6
                if config.developer and (persistent.show_hotspots or hovered_object == key):
                    text ("·" if key in observed else "◇") xalign .5 size 35 color ("#9caeb7" if key in observed else "#e5eef3")
                    text title xalign .5 size 23 outlines [(3, "#101720ee", 0, 0)]

    key "K_n" action Show("notebook")
    key "game_menu" action ShowMenu("pause_menu")

screen notebook(menu_mode=False):
    modal True
    zorder 150
    add Solid("#081311c8")
    add Solid("#272d24") xpos 243 ypos 87 xsize 1445 ysize 930
    add Solid("#d1c4a8") xpos 255 ypos 75 xsize 1410 ysize 918
    add Solid("#eee4cf") xpos 273 ypos 75 xsize 1388 ysize 903
    add Solid("#9c8a6538") xpos 933 ypos 96 xsize 18 ysize 864
    for y in range(257, 929, 53):
        add Solid("#86785b26") xpos 311 ypos y xsize 1307 ysize 2

    text "기록" xpos 326 ypos 117 size 20 color "#777962"
    text "확인한 사실" xpos 323 ypos 164 size 48 color INK
    text "탈출에 필요한 것만 정리한다." xpos 963 ypos 174 size 29 color "#7c7966"

    viewport:
        id "notebook_scroll"
        xpos 323 ypos 290 xsize 1284 ysize 550
        mousewheel True draggable True scrollbars "vertical"
        vbox:
            xsize 1232 spacing 35
            for key, title, content in notes:
                vbox:
                    spacing 9
                    text title color "#7d745b" size 21
                    text content color INK size 35 line_spacing 8
            if not notes:
                text "아직 정리할 만큼 확인한 것이 없다." size 35 color INK

    text "직접 확인한 사실만 남긴다." xpos 326 ypos 909 size 25 color "#7b765e"
    textbutton "기록 닫기" id "close_notebook" xpos 1355 ypos 890 action (Return() if menu_mode else Hide("notebook")) text_color INK text_hover_color "#a07146" text_size 27
    key "K_n" action (Return() if menu_mode else Hide("notebook"))
    key "game_menu" action ShowMenu("pause_menu")

screen menu_tabs():
    style_prefix "menu"
    hbox:
        spacing 16
        if not main_menu:
            textbutton "기록" action ShowMenu("notebook_menu") text_size 25
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
        add Solid("#222e32") xpos 580 ypos 260 xsize 540 ysize 660
        if selected_person == "suhyeok":
            add Transform("images/suhyeok_profile.png", crop=(0, 0, 1024, 1250), xysize=(540, 660)) xpos 580 ypos 260
        else:
            add Transform("images/seoa_cutout_neutral.png", crop=(0, 0, 1122, 1370), xysize=(540, 660)) xpos 580 ypos 260
        vbox:
            xpos 1190 ypos 330 xsize 590 spacing 35
            if selected_person == "suhyeok":
                text "김수혁" size 46 style "menu_title"
                text "회복 프로그램 참가자." size 30
            else:
                text "윤서아" size 46 style "menu_title"
                text "회복 프로그램을 소개한 사람." size 30
                text "봉사활동에서 만나 가까워졌다." size 28 color ACCENT

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
                    if config.developer:
                        textbutton "조사 위치 표시" action ToggleField(persistent,"show_hotspots")
                    text "대사·기록 넘기기: 클릭 / Enter / Space\n기록: N   ·   메뉴: Esc\n읽은 문장만 빠르게: Ctrl / Tab" size 24 line_spacing 15 color "#9daea1"
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
    # 로비 전용 서아 세트. 모든 표정은 같은 캔버스·좌표를 사용한다.
    # 수혁의 차례에는 별도 이미지를 쓰지 않고 같은 원본만 딤 처리한다.
    zorder -1
    add Transform("images/lobby_day.png", xysize=(1920, 1080), matrixcolor=SaturationMatrix(.65))
    if expression is not None:
        add Transform(
            "images/seoa_lobby_" + expression + ".png",
            xysize=(560, 840),
            matrixcolor=(SaturationMatrix(.82) if speaking else SaturationMatrix(.58) * BrightnessMatrix(-.20)),
            alpha=(1.0 if speaking else .72)
        ) xpos 1280 ypos 178

screen opened_door():
    zorder -1
    add Transform("images/door_threshold.png", xysize=(1920, 1080))

screen door_choices():
    modal True
    vbox:
        xalign .5 yalign .55 spacing 28
        for choice_id, caption in (("stay", "방 안에 머문다"), ("leave", "나간다")):
            textbutton caption:
                id ("door_" + choice_id)
                xsize 720
                text_xalign .5
                background Solid("#080b10e8")
                action Return(choice_id)
    key "game_menu" action ShowMenu("pause_menu")
