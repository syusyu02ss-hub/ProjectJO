# 장면 1 · 새 설계 전환
# 방 탐색 → 정전 → 열린 문 → 복도 데모로 연결.

define su = Character("나", color="#a9bac2")
define seo = Character("윤서아", color="#d3bcc0")

image room = "images/room_cold_fhd.png"
image black = Solid("#070b10")
image room_after = Transform(
    "images/room_cold_fhd.png",
    xysize=(1920, 1080),
    matrixcolor=SaturationMatrix(.16) * BrightnessMatrix(-.42)
)

label start:
    $ reset_scene1_state()
    $ stage = "lobby"

    # 로비는 현재의 서아를 보여 주는 짧은 프롤로그다.
    # 이후 연구소 안에서는 별도의 인물 세트를 사용한다.
    show screen memory_portrait(None)
    "조금 전, 온결 로비."
    "햇빛이 로비 바닥에 길게 드리워져 있다. 그 끝에서 서아가 돌아본다."
    "처음 만난 날에도 저렇게 소매를 걷고 있었다. 봉사활동이 끝나고, 둘이 남아 물품 상자를 정리하던 날."
    "잘하던 일이 손에 잡히지 않아 쉬기로 했었다. 막상 집에 있으니 못 끝낸 일만 자꾸 생각났다."
    "봉사활동은 밖에 나갈 핑계였다."
    "상자를 나르는 동안에는 눈앞의 일만 하면 됐다. 다음 주에도 나오겠다고, 어느새 내가 먼저 말하고 있었다."
    "서아와는 자주 같은 일을 맡았다. 처음에는 잘 웃는 사람이라고만 생각했다."
    "웃음을 참다가 눈가부터 풀리는 표정이 좋았다. 그걸 보려고 괜히 말을 건 적도 있다."
    "한번은 일이 잘 안 풀린다는 얘기까지 꺼냈다. 서아는 상자를 내려놓고 내 옆에 앉았다."
    "말이 끊겨도 재촉하지 않았다. 덕분에 생각보다 많은 얘기를 했다."
    "그 뒤로는 토요일에 눈을 뜨는 일이 조금 수월해졌다."

    show screen memory_portrait("soft", speaking=True)
    seo "많이 긴장했어?"

    show screen memory_portrait("neutral", speaking=False)
    "휴대폰을 도로 주머니에 넣는다. 아까 봤을 때랑 겨우 일 분 차이다."
    su "조금. 이런 데는 처음이라."
    su "막상 오니까 무슨 말을 해야 할지도 모르겠고."

    show screen memory_portrait("warm", speaking=True)
    seo "그냥 방금 나한테 한 얘기부터 해 봐."

    show screen memory_portrait("neutral", speaking=False)
    "서아가 웃는다. 나도 따라 웃고 나니 조금 낫다."
    "이 프로그램을 권한 것도 서아였다. 지나가듯 말한 잠 얘기를 기억해 줬다."
    su "이거 끝나면 좀 나아지려나."

    show screen memory_portrait("soft", speaking=True)
    seo "조금이라도 편해졌으면 좋겠어."

    show screen memory_portrait("neutral", speaking=False)
    "고개를 끄덕인다. 이 애 앞에서는 괜찮은 척하지 않아도 된다."
    su "다녀올게. 오래 걸리면 먼저 가도 돼."

    show screen memory_portrait("soft", speaking=True)
    seo "괜찮아. 여기서 기다릴게."

    show screen memory_portrait("soft", speaking=False)
    "돌아보니 서아가 손을 흔든다. 나도 작게 흔들어 준다."

    hide screen memory_portrait
    $ stage = "intro"
    scene room

    "눈부셔."
    "눈을 가늘게 뜬다. 흐릿한 조명이 천천히 모양을 잡는다."
    "등이 배긴다. 몸을 뒤척이자 차가운 소파에 맨팔이 닿는다."
    "잠깐, 여기가 어디야."
    "낯선 탁자, 식은 찻잔. 맞은편에는 문이 닫혀 있다."
    "일어나려는데 머리가 욱신거린다."
    "온결. 프로그램 받으러 왔었지."
    "서아랑 얘기하고 접수하러 갔는데."
    "얼마나 잔 거지. 서아가 기다리고 있을 텐데."
    "주머니에 손을 넣는다. 비어 있다."
    "반대쪽에도 없다."
    "떨어졌나."
    "소파 틈을 뒤지고 아래도 들여다본다. 먼지만 손에 묻어난다."
    "로비에서 시간까지 확인했잖아."
    su "...젠장."
    "문으로 다가가 손잡이를 내린다."
    play sound "audio/handle.wav"
    "철컥. 안 열린다."
    "당기는 건가?"
    "어깨를 대고 밀어도 꼼짝없다."
    "귀를 대 본다. 내 숨소리뿐이다."
    "휴대폰도 없고 문도 안 열린다."
    "왜 잠가 놨지?"
    "다른 데를 보자. 나갈 방법이 있을 거야."

    jump investigate

label investigate:
    $ stage = "investigation"
    window hide
    call screen investigation
    $ inspected = _return

    if inspected == "window":
        call inspect_window
    elif inspected == "cup":
        call inspect_cup
    elif inspected == "clock":
        call inspect_clock
    elif inspected == "door":
        call inspect_door
    elif inspected == "light":
        call inspect_light
    elif inspected == "panel":
        call inspect_panel
    elif inspected == "button":
        call inspect_button
    elif inspected == "drawer":
        call inspect_drawer

    if investigation_ready():
        jump blackout
    jump investigate

label inspect_window:
    "유리에 얼굴을 가까이 댄다. 밖은 뿌옇기만 하다."
    "손잡이가 없다. 테두리를 더듬어도 벌어지는 틈 하나 없다."
    "밀어 봐도 소용없다."
    "창문 맞아, 이거?"
    $ add_record("window", "창", "바깥이 보이지 않는다. 열리지 않는다.")
    $ mark_observed("window")
    return

label inspect_cup:
    "잔이 차갑다."
    "목이 마르다. 한 모금만 마셨으면."
    "누가 놓고 간 거지. 내가 마셨던 건가."
    "그냥 내려놓는다. 달그락, 작은 소리에도 흠칫한다."
    $ add_record("cup", "찻잔", "언제 놓였는지 알 수 없는 식은 차.")
    $ mark_observed("cup")
    return

label inspect_clock:
    "초침이 멎어 있다."
    "하나, 둘, 셋."
    "움직이지 않는다."
    "얼마나 잔 건지 이것마저 못 알려 주네."
    $ add_record("clock", "벽시계", "초침이 멎어 있다. 시간을 알 수 없다.")
    $ mark_observed("clock")
    return

label inspect_door:
    "잠금을 푸는 게 어디 있지?"
    play sound "audio/handle.wav"
    "손잡이를 끝까지 내리고 당긴다. 문틀만 삐걱거린다."
    "안에서 여는 게 있어야 하잖아."
    "문 아래까지 살펴도 걸쇠 하나 없다."
    $ add_record("door", "문", "손잡이는 움직이지만 문은 열리지 않는다.")
    $ mark_observed("door")
    return

label inspect_light:
    "문 위에 작은 패널이 있다. 아무 표시도 없다."
    "고장 난 건가?"
    "손잡이를 움직여 봐도 불은 들어오지 않는다."
    $ add_record("light", "문 위 패널", "검은 패널. 표시가 없다.")
    $ mark_observed("light")
    return

label inspect_panel:
    "안내문인가 싶어 다가간다."
    "빈 액자다."
    "연락처라도 좀 적어 놓지. 여기가 어딘지도 모르겠는데."
    $ add_record("panel", "빈 액자", "글자 없는 액자. 안내문은 없다.")
    $ mark_observed("panel")
    return

label inspect_button:
    "이걸 누르면 열리나?"
    "버튼에는 글자도 화살표도 없다."
    "누군가를 부르는 거면 어떡하지."
    "이 문을 잠근 사람이 오면?"
    "뻗던 손을 거둔다. 이건 누르지 말자."
    $ add_record("button", "벽 버튼", "용도를 알 수 없는 버튼. 누르지 않았다.")
    $ mark_observed("button")
    return

label inspect_drawer:
    play sound "audio/drawer.wav"
    "덜컥. 나도 모르게 문 쪽을 돌아본다."
    "조용하다. 다시 서랍 안을 들여다본다."
    "빈칸. 그 아래도 빈칸."
    "안쪽까지 손을 넣어 본다. 휴대폰은커녕 종이 한 장 없다."
    $ add_record("drawer", "서랍장", "비어 있다. 개인 물건도, 쓸 도구도 없다.")
    $ mark_observed("drawer")
    return

label blackout:
    $ stage = "blackout"
    $ checkpoint()
    "더 볼 곳이 없다. 결국 다시 문 앞이다."
    "자꾸 주머니로 손이 간다. 없다고. 아까 확인했잖아."

    stop music fadeout .2
    play sound "audio/panel.wav"
    scene black
    "딱."
    "불이 꺼졌다."
    "몸이 굳는다. 눈앞에 하얀 잔상만 어른거린다."
    "웅웅거리던 소리마저 끊겼다."
    "왜 꺼졌지."

    play sound "audio/door_open.wav"
    "문 쪽에서 철컥, 소리가 난다."

    scene room_after
    "어둠에 익숙해지자 문 윤곽이 겨우 보인다."
    "손을 뻗어 손잡이를 찾는다."
    play sound "audio/handle.wav"
    "이번에도 안 열리면."
    play sound "audio/door_open.wav"
    "당기던 문이 움직인다."
    "열렸다."
    "닫히지 않게 잡고 있어야 해."

    jump leave_room

label leave_room:
    $ stage = "corridor"
    scene black
    show screen opened_door
    with Dissolve(.6)
    "문틈으로 찬 공기가 밀려온다."
    "밖은 더 어둡다. 문턱을 넘으려다 멈춘다."
    play ambience "audio/corridor.wav" fadein .4
    "바닥만 희미하게 보인다. 복도 끝은 보이지 않는다."
    "귀를 기울여도 조용하다."
    "여기로 나가도 되는 걸까."
    window hide
    call screen door_choices

    if _return == "stay":
        "한 발 물러선다. 조금만 기다려 볼까."
        "문이 따라 닫히려 하자 얼른 붙잡는다."
        "아니야."
        "다시 잠기면 어떡하려고."
        "휴대폰도 없는데 여기 앉아서 뭘 기다려."
        "열렸을 때 나가자."
    else:
        "기다리는 건 그만하자."
        "그냥 프로그램이면, 방에서 나갔다고 뭐라고 하진 않겠지."
        "그래. 잘못한 것도 없잖아."

    "문을 조금 더 당겨 틈으로 빠져나간다."
    "손잡이 대신 벽을 짚는다. 여기서 나가자."

    jump corridor_demo
