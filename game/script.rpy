# 장면 1. 마지막 승인 원고와 수정 사항이 초기 기획서보다 우선한다.
define su = Character("나", color="#a9bac2")
define dy = Character("정다영", color="#acbdc1")
define staff = Character("직원", color="#a9b4b8")
define guide = Character("안내자", color="#b9c4c8")

image room = Transform("images/room_cold.png", xysize=(1920, 1080))
image black = Solid("#070b10")
image room_after = Transform("images/room_cold.png", xysize=(1920, 1080), matrixcolor=SaturationMatrix(.2) * BrightnessMatrix(.14))

label start:
    $ set_skip_lock(False)
    $ stage = "intro"
    scene room
    show screen room_clock
    play ambience "audio/ticking.wav"
    play music "audio/guide_music.wav" fadein 2.0
    "문이 닫혔다. 잠기는 소리는 없었다. 조용히 닫히는 문이었다."
    "방은 나쁘지 않았다. 소파, 찻잔, 벽시계. 호텔방 같기도 하고 상담실 같기도 했다."
    "다만 빛이 조금 부족했다. 천장의 흰 조명 아래, 가구의 윤곽만 서늘하게 남아 있었다."
    "휴대폰은 접수 데스크에 맡겼다. 대신 받은 건 수첩 한 권과 펜 한 자루."
    "나는 원래 뭐든 적어 두는 사람이다. 적어 두지 않으면 불안하다. 이런 곳에서는 더 그렇다."
    "수첩을 펼치자 첫 장에 참가 번호 스티커가 붙어 있다. 0713."
    "로비에서 다영이 했던 말이 떠올랐다."
    hide screen room_clock
    scene black
    show screen memory_portrait("neutral")
    "몇 달 전, 우연히 알게 된 사람. 이직 이야기가 번번이 틀어졌을 때도 다영은 내 말을 끝까지 들어줬다."
    dy "긴장한 얼굴이네. 여기 사람들 다 좋아, 진짜."
    su "너는 자주 와?"
    show screen memory_portrait("soft")
    dy "일 때문에 종종. 그리고… 전에도 도와준 사람이 있었어. 다들 잘 지내."
    "자랑하는 웃음이 아니었다. 좋은 소식을 전하는 사람의 웃음이었다."
    "온결의 사원 추천형 회복 프로그램. 직원인 다영은 외부인도 추천할 수 있다고 했다."
    show screen memory_portrait("warm")
    dy "나는 여기까지야. 거기 가면 다 괜찮아질 거야."
    su "끝나고 연락할게."
    dy "응. 잘 다녀와."
    hide screen memory_portrait
    play sound "audio/door_close.wav"
    scene room
    show screen room_clock
    "문이 닫힌다. 나는 방 안에 남았다."
    call record_note("dayoung", "로비에서", "다영: 전에도 도와준 사람이 있었어. 다들 잘 지내.", ("dayoung_line",))
    "왜 이걸 적었을까. 습관이다. 아직은."
    jump investigate

# 수첩의 모든 관찰은 작성 화면을 거친 다음에만 추가한다.
label record_note(key, title, content, flags=()):
    if not any(n[0] == key for n in notes):
        play foley "audio/pen.wav"
        call screen handwritten(content, title)
        $ add_note(key, title, content, flags)
    return

label investigate:
    $ stage = "investigation"
    window hide
    call screen investigation
    $ inspected = _return
    if inspected == "notice":
        call inspect_notice
    elif inspected == "drawer":
        call inspect_drawer
    elif inspected == "light":
        call inspect_light
    elif inspected == "door":
        call inspect_door
    elif inspected == "cup":
        call inspect_cup
    elif inspected == "window":
        call inspect_window
    elif inspected == "clock":
        call inspect_clock
    elif inspected == "call":
        call inspect_call
    if investigation_ready():
        jump delivery
    jump investigate

label inspect_notice:
    "문 옆 액자에 안내문이 걸려 있다."
    call screen notice_page
    "문장은 하나같이 친절하다. 그런데 나가는 방법은 어디에도 없다."
    call record_note("notice", "안내문", "배식 21:10 / 안내자는 두 번 노크\n불편하면 호출 버튼", ("meal_2110", "rule_knock", "call_button_rule"))
    $ mark_observed("notice")
    return

label inspect_door:
    "안쪽에는 손잡이뿐이다. 열쇠구멍도 잠금장치도 없다."
    play sound "audio/handle.wav"
    "손잡이는 돌아간다. 그런데 문은 밀리지 않는다. 잠겨 있다기보다, 열리지 않기로 되어 있는 문 같다."
    call record_note("door", "문", "손잡이는 돌아가지만 문은 안 열림")
    $ mark_observed("door")
    return

label inspect_light:
    "문 위에 손톱만 한 표시등이 있다. 초록색이다. 문의 상태를 알려 주는 것 같다."
    "그렇다면 이 방에서 문 상태를 아는 건 내가 아니라 문 쪽이다."
    call record_note("light", "문 위", "문 위 표시등: 지금은 초록", ("light_green",))
    $ mark_observed("light")
    return

label inspect_drawer:
    play sound "audio/drawer.wav"
    "첫 서랍에는 같은 표지의 새 수첩과 펜, 티슈가 들어 있다."
    "두 번째 서랍은 뻑뻑하다. 안쪽에서 뜯겨 나간 수첩 페이지의 귀퉁이가 나온다."
    "글씨는 없다. 스탠드 불빛을 비스듬히 비추자 눌린 자국이 드러난다."
    call screen evidence_fragment
    "서랍 안쪽 벽에는 이름표를 붙였다 뗀 자국이 있다. 그 위를 누군가 문질러 지운 흔적이 남아 있다."
    call record_note("drawer", "눌린 글씨", "호출 → 상담사 → 기억이 끊김\n서랍 안쪽 이름표 자리, 지워짐", ("drawer_marks", "name_tag_erased"))
    $ mark_observed("drawer")
    # 마지막 필수 조사여도 함정 조사 기회를 잃지 않도록 한 번 연결한다.
    if not call_resolved:
        "문 옆의 호출 버튼이 눈에 들어온다. 방금 읽은 자국이 마음에 걸린다."
        call inspect_call
    return

label inspect_cup:
    "김이 오른다. 들어온 뒤 아무도 차를 가져오지 않았다."
    "내가 올 시간에 맞춰 누군가 미리 부어 둔 것이다. 입에 대지 않고 내려놓는다."
    play sound "audio/cup.wav"
    call record_note("cup", "찻잔", "차는 내가 오기 전부터 준비돼 있었음")
    $ mark_observed("cup")
    return

label inspect_window:
    "빛은 들어오는데 바깥은 젖은 유리 너머처럼 흐릿하다. 만져 보니 차갑지 않고 미지근하다."
    "창이라기보다 창 모양의 조명이다. 낮인지 밤인지 알 방법이 없다. 시계만 시간을 알려 준다."
    call record_note("window", "창", "창은 열리지 않음. 시간은 시계로만 안다")
    $ mark_observed("window")
    return

label inspect_clock:
    if not sorting_experienced:
        "벽시계는 20시 58분이다. 손목시계도 20시 58분이다. 초침 위치까지 같다."
        "이게 무슨 의미인지는 모르겠지만 적어 둔다."
        call record_note("clock", "두 시계", "벽시계 = 손목시계 (20:58)", ("clock_same",))
    else:
        "벽시계보다 손목시계가 삼십칠 분 앞서 있다. 내 기억 밖에서 시간이 흘렀다."
        call record_note("clock_after", "어긋난 시간", "벽시계보다 손목시계가 37분 빠름. 시간이 되돌아간 게 아님.")
    $ mark_observed("clock")
    return

label inspect_call:
    if not has("drawer_marks"):
        "문 옆의 동그란 버튼. 안내문에는 눌러도 된다고 적혀 있다. 그런데 손끝이 멈춘다."
        "이유는 모르겠다. 일단 다른 곳부터 본다."
        return
    "호출 버튼이 은은하게 빛난다. 누르면 부드러운 알림음이 날 것 같다."
    $ stage = "call"
    $ checkpoint()
    label call_decision:
        window hide
        call screen call_options
        if _return:
            $ fail_kind = "A"
            call failure
            call restore_after_sort
            jump call_decision
    "손을 뗀다. 다음에는 망설이지 않도록 적어 둔다."
    call record_note("call_warning", "호출 버튼", "호출 버튼: 누르지 않기")
    $ call_resolved = True
    $ mark_observed("call")
    $ stage = "investigation"
    return

label delivery:
    $ stage = "delivery"
    $ wall_minutes = 1269
    stop music fadeout 1.0
    "벽시계가 21시 9분 50초를 지난다. 방 안에는 초침 소리뿐이다."
    label replay_delivery:
        $ stage = "delivery"
        play sound "audio/knock_two.wav"
        "똑, 똑."
        "두 번. 안내문 그대로다."
        play sound "audio/door_open.wav"
        $ wall_minutes = 1270
        # 직원과 카트는 지문과 소리로만 존재한다. 화면은 정지된 시야로 바뀐다.
        hide screen room_clock
        show screen threshold_still
        "문이 열린다. 온결 유니폼을 입은 젊은 직원이 은색 태그가 붙은 배식 카트를 밀고 서 있다. 표정이 평온하다."
        "그는 문 옆 패널에 손을 뻗어 오른쪽 아래의 검은 버튼을 누른다."
        play sound "audio/panel.wav"
        "문 위 표시등이 노랗게 바뀐다. 문은 열린 채 닫히지 않는다."
        "복도 천장의 작은 카메라가 카트 쪽으로 천천히 돈다. 렌즈는 사람이 아니라 카트의 태그에서 멈춘다."
        staff "저녁 드세요. 불편하신 점 없으시죠?"
        play sound "audio/cutlery.wav"
        "그는 쟁반을 들고 탁자 쪽으로 돌아선다. 카트는 문틈에 걸린 채 남아 있다."
        if not urgent_note_written:
            "직원이 등을 돌렸다. 지금밖에 없다."
            "펜 소리가 날까 봐 힘을 뺀다. 컵과 숟가락 부딪히는 소리가 이어진다. 보이는 것만 짧게 적는다."
            call record_note("urgent", "직원의 등 뒤에서", URGENT_NOTE, ("black_button", "camera_cart"))
            $ urgent_note_written = True
            "글씨가 엉망이지만 알아볼 수는 있다."
        else:
            "수첩에 적힌 그대로였다. 검은 버튼, 노란 표시등."
        $ stage = "judgment"
        $ stop_fast_skip()
        $ checkpoint()
        window hide
        call screen judgment
        if _return != "success":
            $ fail_kind = _return
            call failure
            call restore_after_sort
            jump replay_delivery
    jump escape_room

label failure:
    $ stage = "failure"
    $ stop_fast_skip()
    if fail_kind == "A":
        play sound "audio/call.wav"
        "부드러운 알림음이 울린다. 딩. 기분 좋을 만큼 작은 소리다."
        play foley "audio/knock_two.wav"
        "대답하듯 곧바로 노크가 온다. 두 번. 너무 빠르다."
        "안내자의 손에는 이미 ‘호출 접수’라고 뜬 태블릿이 들려 있다."
    elif fail_kind == "B":
        su "저기, 여기서 나가고 싶어요."
        "직원은 놀라지 않는다. 오히려 안심한 표정이다."
        staff "아, 힘드셨구나."
        "그의 손은 벌써 허리춤의 작은 단말로 가 있다."
        play sound "audio/panel.wav"
    else:
        staff "어디 가세요?"
        "직원은 뛰지 않는다. 뛸 필요가 없다는 듯이."
        "복도 끝에서 같은 유니폼 두 사람이 서두르지 않고 걸어온다."
        "나는 그들 사이로 다시 방에 들어온다. 문은 조용히 닫힌다."
    hide screen threshold_still
    scene room
    show screen room_clock
    play sound "audio/door_close.wav"
    stop music fadeout .5
    "안내자가 소파에 앉는다. 식은 찻잔을 치우고 새 잔을 내려놓는다. 김이 오른다."
    guide "많이 놀라셨죠. 괜찮아요. 아무도 화 안 났어요."
    guide "떠오르는 생각을 적어 보세요. 감정을 기록하면 편안해지거든요. 수첩은 가지고 계셔도 됩니다."
    "서랍에 눌려 있던 글씨. ‘그 뒤로 기억이…’"
    "지금 일을 잊게 된다면. 다음의 나에게 남겨야 한다."
    $ write_failure(fail_kind)
    play foley "audio/pen.wav"
    call screen handwritten(latest_warning, "다음의 나에게", reveal=True)
    hide screen room_clock
    scene room_after
    "조명이 흰색으로 바뀐다. 눈이 저절로 감긴다. 손목에 따뜻한 손이 얹힌다. 저릿하다."
    guide "천천히 내려놓으세요. 방금 있었던 일도, 오늘 있었던 일도."
    scene black
    "멀리서, 다정한 말이 들린다."
    guide "이제 괜찮아요. 잘하고 계세요."
    stop ambience
    window hide
    call screen sorting_card
    return

label restore_after_sort:
    scene room
    $ wall_minutes = 1258 if fail_kind == "A" else 1269
    $ stage = "call" if fail_kind == "A" else "delivery"
    show screen room_clock
    play ambience "audio/ticking.wav"
    "눈을 뜬다. 손에 펜이 쥐어져 있다. 무엇을 하려던 참이었지."
    if not first_dejavu_seen:
        $ set_skip_lock(True)
        "천장의 흰빛이 눈에 남아 있다. 호출 버튼 쪽을 보자 작은 알림음이 귓가에 맴도는 것 같다. 손목이 저릿하다."
        if has("clock_same"):
            "두 시계가 같다고 적어 두었다. 그런데 지금은 손목시계가 삼십칠 분 앞서 있다."
        else:
            "손목시계가 벽시계보다 삼십칠 분 앞서 있다. 기억하지 못하는 시간이 있다."
        "벽시계는 되돌려 맞춰 둔 모양이다. 내 손목에서 흐른 시간까지 돌려놓지는 못했다."
        $ set_skip_lock(False)
    if urgent_note_written:
        if not urgent_dejavu_seen:
            $ set_skip_lock(True)
        "급하게 쓴 글씨다. 내 글씨인데 쓴 기억이 없다."
        call screen handwritten(URGENT_NOTE, "이미 적혀 있는 글씨", reveal=False)
        $ urgent_dejavu_seen = True
        $ set_skip_lock(False)
    "그 아래, 접힌 페이지에 다른 글이 있다."
    call screen handwritten(latest_warning, "쓴 기억이 없는 내 글씨", reveal=False)
    "기억은 없지만 글씨는 남았다. 지금은 이 글을 믿어야 한다."
    $ first_dejavu_seen = True
    if fail_kind == "A":
        "서랍을 다시 본다. 눌린 자국은 그대로다. 호출 버튼에서 손을 뗐다가, 잠시 멈춘다."
        $ checkpoint()
    else:
        "벽시계는 21시 9분 50초를 가리킨다. 나는 수첩을 펼친 채 문을 본다."
    return

label escape_room:
    $ stage = "escape"
    "숨을 죽이고 몸을 낮춘다. 카트의 은색 태그가 복도 불빛을 받아 반짝인다. 카메라는 여전히 카트만 보고 있다."
    "카트 뒤, 한 뼘 남짓한 그림자 안으로 발을 옮긴다."
    play sound "audio/cutlery.wav"
    "컵과 숟가락 부딪히는 소리. 한 걸음. 두 걸음. 그는 끝까지 뒤돌아보지 않는다."
    hide screen threshold_still
    scene black
    stop ambience fadeout .5
    play ambience "audio/corridor.wav" fadein .5
    "문틀을 넘는다. 복도의 공기는 방보다 차갑다. 그 차가움이 이상하게 반갑다."
    "왼쪽 비품실 문이 조금 열려 있다. 몸을 밀어 넣고 문을 닫는다. 어둠."
    play sound "audio/door_close.wav"
    "수첩에 짧게 적는다. 손끝의 떨림이 조금 가라앉았다."
    call record_note("escape", "문 하나를 지나서", "방을 나옴. 카트 뒤로.")
    "그때, 벽 너머에서 소리가 들린다."
    play sound "audio/knock_signal.wav"
    "톡. 톡톡."
    $ chapter_complete = True
    $ stage = "complete"
    window hide
    call screen end_chapter
    return
