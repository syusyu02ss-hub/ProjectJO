# 복도 데모. 상대는 박도현이지만 수혁은 아직 이름과 얼굴을 모른다.
# 수혁은 자신의 정체를 안다. 마지막 반문은 낯선 상대에게 설명하기 전의 망설임이다.
define corridor_man = Character("어둠 속 목소리", color="#a9bac2")
define CORRIDOR_CHOICE_SECONDS = 7.0
define CORRIDOR_CHOICE_GRACE = 0.5

image corridor_dark = Transform("images/menu_corridor.png", xysize=(1920, 1080), matrixcolor=SaturationMatrix(.12) * BrightnessMatrix(-.30))

label corridor_demo:
    $ stage = "corridor_walk"
    hide screen opened_door
    window hide
    scene black with Dissolve(.65)
    pause .6
    scene corridor_dark with Dissolve(1.4)
    play ambience "audio/corridor.wav" volume .35 fadein 1.0
    play sound "audio/steps_near.wav"
    "몇 걸음 만에 발밑도 보이지 않는다."
    "벽에 바짝 붙는다. 손바닥에 닿는 차가운 감촉이 그나마 안심된다."
    "어떻게 이렇게 어둡지. 창문도 없나?"
    "로비에서는 분명 낮이었는데."
    "아까 시계가 몇 시였더라."
    "아니, 멈춰 있었잖아. 그걸 믿어서 뭐 해."
    play sound "audio/steps_near.wav"
    "발끝으로 바닥을 더듬는다. 갑자기 계단이라도 나오면."
    "밑창 끄는 소리가 멀리까지 울린다. 너무 큰가?"
    "숨도 조금씩 내쉰다."
    "손에 땀이 찬다. 닦고 싶어도 벽에서 떼기가 무섭다."
    "서아는 아직 기다리고 있을까."
    "설마 이런 방인 줄 알면서 보낸 건 아니겠지."
    "들어오기 전에 웃어 줬는데. 편해졌으면 좋겠다고."
    "그 애가 일부러 그랬을 리가."
    "그런데 왜 나는 여기 있지."
    play sound "audio/steps_near.wav"
    "벽을 따라 한 걸음 더."
    play foley "audio/steps_other.wav"
    "잠깐."
    "아직 발을 안 디뎠는데."
    stop sound
    "그대로 멈춘다."
    play foley "audio/step_last.wav"
    stop ambience fadeout .2
    # 빈 대사 한 번: 마지막 한 걸음이 잦아든 뒤 플레이어도 정적을 넘긴다.
    "{w=0.7}"
    stop foley
    window hide
    pause .6
    "내가 멈추니까."
    play foley "audio/corridor_chill.wav" volume .65
    "상대도 멈췄다."
    "누군가 있다."
    "등줄기가 서늘해진다."
    "메아리였나?"
    "아니야. 분명 앞에서 났어."
    "한 번만 더 걸어 봐. 어디 있는지라도 알게."
    "저쪽도 듣고 있다. 내가 움직이길 기다리는 건가?"
    "나를 보고 있나? 나는 안 보이는데."
    "침 삼키는 소리가 유난히 크다. 이것도 들렸을까."
    "방으로 돌아가야 하나. 등을 돌리는 순간 따라오면?"
    "먼저 말을 걸까. 대답은 해 줄까."
    "뭘 들고 있으면? 이렇게 안 보이는데 피할 수 있나?"
    "어떡하지."
    jump corridor_decision

label corridor_decision:
    $ stage = "corridor_choice"
    $ chapter_complete = False
    stop sound
    stop foley
    stop ambience
    scene corridor_dark
    window hide
    play ambience "audio/ticking_urgent.wav" volume .35
    call screen corridor_choices
    stop ambience
    if _return == "timeout":
        jump corridor_timeout
    elif _return == "rush":
        jump corridor_rush
    elif _return == "flee":
        jump corridor_flee
    jump corridor_speak

label corridor_flee:
    $ stage = "corridor_flee"
    "돌아가자. 방은 가까워."
    play sound "audio/steps_near.wav"
    "급히 돌아서다 벽을 놓친다."
    "어깨가 어딘가에 부딪친다. 아, 젠장."
    stop sound
    "길이 왜 막혀 있지? 방금 여기로 왔잖아."
    corridor_man "거기. 멈춰."
    "바로 뒤 같다."
    su "오지 마세요."
    corridor_man "안 가. 너도 갑자기 움직이지 마."
    "팔로 가슴을 가린 채 귀를 기울인다."
    "쫓아오는 소리는 없다. 그래도 등을 돌릴 엄두가 안 난다."
    jump corridor_question

label corridor_speak:
    $ stage = "corridor_speak"
    "목소리라도 들으면 어디 있는지 알겠지."
    su "거기, 누구 있어요?"
    "목소리가 갈라진다."
    corridor_man "움직이지 마."
    "가깝다. 이렇게 가까웠어?"
    "벽에 등을 붙인다. 더 물러날 데가 없다."
    jump corridor_question

label corridor_question:
    $ stage = "corridor_question"
    su "누구세요?"
    "대답 대신 옷깃 스치는 소리."
    su "대답 좀 해 봐요."
    corridor_man "그러는 넌?"
    "낮게 내리누른 목소리. 끝이 미세하게 떨린다."
    corridor_man "너는 누군데?"
    "날 선 질문에 대답이 목 안에서 멈춘다."
    su "내가… 누구냐고?"
    # 풀버전에서는 설명할 말을 고른 뒤 온결 프로그램 참가 경위를 밝힌다.
    window hide
    stop sound
    stop foley
    stop ambience
    scene black with Dissolve(.8)
    pause 1.2
    $ chapter_complete = True
    $ stage = "demo_complete"
    call screen corridor_demo_end
    return

label corridor_rush:
    $ stage = "corridor_bad_end"
    "지금 뛰면 지나칠 수 있을지도 몰라."
    "멈추지 말고. 그냥 쭉."
    play sound "audio/steps_near.wav"
    "벽에서 손을 떼고 내달린다."
    corridor_man "오지 마!"
    "코앞에서 뭔가 휙 스친다."
    jump corridor_struck

label corridor_timeout:
    $ stage = "corridor_bad_end"
    "뭐라도 해야 하는데."
    play sound "audio/steps_other.wav"
    "발소리가 달려든다."
    stop sound
    play foley "audio/corridor_impact.wav"
    su "크윽.."
    "머리가 깨질 것 같다."
    "눈꺼풀이 서서히 감긴다."
    scene black with Dissolve(1.2)
    su "아.. 이렇게는..."
    "안 돼. 눈 떠."
    "나 아직 여기 있는데."
    "제발."
    jump corridor_failure_finish

label corridor_struck:
    stop sound
    play foley "audio/corridor_impact.wav"
    scene black
    su "윽!"
    "머리를 얻어맞았다. 다리가 꺾인다."
    "일어나야 해."
    "팔에 힘이 안 들어간다. 바닥이 너무 차갑다."
    "조금만 가면 됐는데."
    "손끝의 감각이 희미해진다."
    jump corridor_failure_finish

label corridor_failure_finish:
    window hide
    stop foley fadeout .5
    pause 1.0
    call screen corridor_failure
    jump corridor_decision

screen corridor_choices():
    modal True
    # 바는 7초에 비고, 입력은 그 뒤 0.5초 동안 더 받는다.
    # 화면을 다시 호출하는 재도전에서는 바와 타이머가 함께 새로 시작한다.
    timer (CORRIDOR_CHOICE_SECONDS + CORRIDOR_CHOICE_GRACE) action Return("timeout")
    vbox:
        xalign .5 yalign .55 spacing 28
        for choice_id, caption in (("flee", "도망간다"), ("speak", "먼저 말을 건다"), ("rush", "달려들어 정면 돌파한다")):
            textbutton caption:
                id ("corridor_" + choice_id)
                xsize 720
                text_xalign .5
                background Solid("#080b10e8")
                action Return(choice_id)
        bar:
            id "corridor_countdown"
            value AnimatedValue(0.0, range=1.0, delay=CORRIDOR_CHOICE_SECONDS, old_value=1.0)
            xsize 720
            ysize 6
            left_bar Solid("#b9a39b")
            right_bar Solid("#24262b")
            thumb None
            thumb_shadow None
    key "game_menu" action ShowMenu("pause_menu")

screen corridor_failure():
    modal True
    add Solid("#000000")
    vbox:
        xalign .5 yalign .5 spacing 36
        text "어둠 속에서, 발소리가 끊겼다." xalign .5 size 36
        text "BAD END" xalign .5 size 22 color "#879299"
        textbutton "선택 직전부터 다시" id "corridor_retry" action Return() xalign .5
        textbutton "메인 메뉴" action MainMenu(confirm=False) xalign .5
    key "game_menu" action ShowMenu("pause_menu")

screen corridor_demo_end():
    modal True
    add Solid("#000000")
    vbox:
        xalign .5 yalign .5 spacing 36
        text "평온의 방" font "fonts/NanumMyeongjo.ttf" size 56 xalign .5
        text "이야기는 계속됩니다." size 30 color "#adb8be" xalign .5
        text "데모 버전은 여기까지입니다." size 23 color "#7c898f" xalign .5
        null height 24
        textbutton "메인 메뉴" id "demo_done" action MainMenu(confirm=False) xalign .5
    key "game_menu" action ShowMenu("pause_menu")
