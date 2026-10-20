# 제1장 새 설계 통합 테스트.
# 방 조사부터 복도 대화 엔딩, 도주 합류, 돌파 실패 후 재시도를 검증한다.

init python:
    _test.timeout = 20.0
    _test.screenshot_directory = "test-results/screens"

testsuite chapter_one:
    teardown:
        exit

    testcase room_to_blackout:
        # MainMenu 전환은 현재 별도의 대기 시간 초과 이슈가 있어, 장면 자체를 직접 시작한다.
        run Start()
        advance until screen "investigation" timeout 20.0

        click id "inspect_window"
        advance until screen "investigation" timeout 20.0
        click id "inspect_cup"
        advance until screen "investigation" timeout 20.0
        click id "inspect_clock"
        advance until screen "investigation" timeout 20.0
        click id "inspect_door"
        advance until screen "investigation" timeout 20.0
        click id "inspect_light"
        advance until screen "investigation" timeout 20.0
        click id "inspect_panel"
        advance until screen "investigation" timeout 20.0
        click id "inspect_button"
        advance until screen "investigation" timeout 20.0
        click id "inspect_drawer"

        advance until screen "opened_door" timeout 20.0
        advance until screen "door_choices" timeout 20.0
        click id "door_leave"
        advance until screen "corridor_choices" timeout 40.0
        assert eval stage == "corridor_choice"
        click id "corridor_speak"
        advance until screen "corridor_demo_end" timeout 20.0
        assert eval chapter_complete
        assert eval stage == "demo_complete"
        assert eval all(key in observed for key in REQUIRED_OBSERVATIONS)
        assert eval len(notes) == len(REQUIRED_OBSERVATIONS)
        run Show("notebook")
        assert screen "notebook"
        click id "close_notebook" until not screen "notebook"

    testcase door_stay_leads_outside:
        run Start("leave_room")
        advance until screen "door_choices" timeout 20.0
        assert screen "opened_door"
        click id "door_stay"
        advance until screen "corridor_choices" timeout 40.0
        assert not screen "opened_door"
        assert eval stage == "corridor_choice"
        click id "corridor_speak"
        advance until screen "corridor_demo_end" timeout 20.0
        assert eval chapter_complete

    testcase corridor_flee:
        run Start("corridor_decision")
        advance until screen "corridor_choices"
        click id "corridor_flee"
        advance until screen "corridor_demo_end" timeout 20.0
        assert eval stage == "demo_complete"
        assert eval chapter_complete

    testcase corridor_timeout_retry:
        run Start("corridor_decision")
        advance until screen "corridor_choices"
        pause 7.7
        assert not screen "corridor_choices"
        advance until screen "corridor_failure" timeout 20.0
        assert eval stage == "corridor_bad_end"
        assert eval not chapter_complete
        click id "corridor_retry"
        assert screen "corridor_choices"
        click id "corridor_speak"
        advance until screen "corridor_demo_end" timeout 20.0
        assert eval chapter_complete

    testcase corridor_grace_accepts_choice:
        run Start("corridor_decision")
        advance until screen "corridor_choices"
        pause 7.1
        assert screen "corridor_choices"
        click id "corridor_speak"
        advance until screen "corridor_demo_end" timeout 20.0
        assert eval chapter_complete

    testcase corridor_rush_retry:
        run Start("corridor_decision")
        advance until screen "corridor_choices"
        click id "corridor_rush"
        advance until screen "corridor_failure" timeout 20.0
        assert eval not chapter_complete
        click id "corridor_retry"
        assert screen "corridor_choices"
        assert eval stage == "corridor_choice"
        click id "corridor_speak"
        advance until screen "corridor_demo_end" timeout 20.0
        assert eval chapter_complete
