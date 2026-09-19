# 실제 플레이 화면과 저장 경로를 이용하는 통합 테스트.
init python:
    _test.timeout = 20.0
    _test.screenshot_directory = "test-results/screens"

testsuite chapter_one:
    teardown:
        exit

    testcase clean_and_save:
        run MainMenu(confirm=False)
        advance until screen "main_menu" timeout 20.0
        click id "start_game"
        advance until screen "handwritten" timeout 20.0
        click id "finish_writing" until not screen "handwritten"
        advance until screen "investigation" timeout 20.0
        screenshot "investigation.png"
        click id "inspect_call"
        advance until screen "investigation" timeout 20.0
        assert eval not warnings
        click id "inspect_clock"
        advance until screen "handwritten" timeout 20.0
        click id "finish_writing" until not screen "handwritten"
        advance until screen "investigation" timeout 20.0
        click id "inspect_cup"
        advance until screen "handwritten" timeout 20.0
        click id "finish_writing" until not screen "handwritten"
        advance until screen "investigation" timeout 20.0
        click id "inspect_window"
        advance until screen "handwritten" timeout 20.0
        click id "finish_writing" until not screen "handwritten"
        advance until screen "investigation" timeout 20.0
        click id "inspect_door"
        advance until screen "handwritten" timeout 20.0
        click id "finish_writing" until not screen "handwritten"
        advance until screen "investigation" timeout 20.0
        click id "inspect_notice"
        advance until screen "notice_page" timeout 20.0
        click id "close_notice" until not screen "notice_page"
        advance until screen "handwritten" timeout 20.0
        click id "finish_writing" until not screen "handwritten"
        advance until screen "investigation" timeout 20.0
        click id "inspect_drawer"
        advance until screen "evidence_fragment" timeout 20.0
        click id "close_fragment" until not screen "evidence_fragment"
        advance until screen "handwritten" timeout 20.0
        click id "finish_writing" until not screen "handwritten"
        advance until screen "call_options" timeout 20.0
        click id "call_no"
        advance until screen "handwritten" timeout 20.0
        click id "finish_writing" until not screen "handwritten"
        advance until screen "investigation" timeout 20.0
        click id "inspect_light"
        advance until screen "handwritten" timeout 20.0
        click id "finish_writing" until not screen "handwritten"
        advance until screen "handwritten" timeout 20.0
        click id "finish_writing" until not screen "handwritten"
        advance until screen "judgment" timeout 20.0
        assert eval urgent_note_written and has("black_button") and has("camera_cart")
        screenshot "judgment.png"
        run Show("notebook")
        assert screen "notebook"
        screenshot "notebook.png"
        click id "close_notebook" until not screen "notebook"
        run ShowMenu("save")
        run FilePage("1")
        click id "slot_1"
        click id "menu_back" until not screen "save"
        click id "judge_success"
        advance until screen "handwritten" timeout 20.0
        click id "finish_writing" until not screen "handwritten"
        advance until screen "end_chapter" timeout 20.0
        assert eval chapter_complete
        assert eval any(n[0] == "escape" for n in notes)
        assert eval not warnings
        screenshot "end.png"
        run FileLoad("1-1", confirm=False)
        advance until screen "judgment" timeout 20.0
        assert eval not chapter_complete and urgent_note_written
        click id "judge_success"
        advance until screen "handwritten" timeout 20.0
        click id "finish_writing" until not screen "handwritten"
        advance until screen "end_chapter" timeout 20.0
        assert eval chapter_complete
        assert eval any(n[0] == "escape" for n in notes)

    testcase call_recovery:
        run MainMenu(confirm=False)
        advance until screen "main_menu" timeout 20.0
        click id "start_game"
        advance until screen "handwritten" timeout 20.0
        click id "finish_writing" until not screen "handwritten"
        advance until screen "investigation" timeout 20.0
        click id "inspect_notice"
        advance until screen "notice_page" timeout 20.0
        click id "close_notice" until not screen "notice_page"
        advance until screen "handwritten" timeout 20.0
        click id "finish_writing" until not screen "handwritten"
        advance until screen "investigation" timeout 20.0
        click id "inspect_drawer"
        advance until screen "evidence_fragment" timeout 20.0
        click id "close_fragment" until not screen "evidence_fragment"
        advance until screen "handwritten" timeout 20.0
        click id "finish_writing" until not screen "handwritten"
        advance until screen "call_options" timeout 20.0
        click id "call_yes"
        advance until screen "handwritten" timeout 20.0
        click id "finish_writing" until not screen "handwritten"
        advance until screen "sorting_card" timeout 20.0
        pause 3.2
        advance until screen "handwritten" timeout 20.0
        click id "finish_writing" until not screen "handwritten"
        advance until screen "call_options" timeout 20.0
        assert eval wrong_choice_history["A"] == 1
        assert eval not has("camera_cart") and not urgent_note_written
        assert eval "카트" not in latest_warning
        click id "call_yes"
        advance until screen "handwritten" timeout 20.0
        click id "finish_writing" until not screen "handwritten"
        advance until screen "sorting_card" timeout 20.0
        pause 3.2
        advance until screen "handwritten" timeout 20.0
        click id "finish_writing" until not screen "handwritten"
        advance until screen "call_options" timeout 20.0
        assert eval wrong_choice_history["A"] == 2
        assert eval not has("camera_cart") and not urgent_note_written
        assert eval "카트" not in latest_warning
        click id "call_yes"
        advance until screen "handwritten" timeout 20.0
        click id "finish_writing" until not screen "handwritten"
        advance until screen "sorting_card" timeout 20.0
        pause 3.2
        advance until screen "handwritten" timeout 20.0
        click id "finish_writing" until not screen "handwritten"
        advance until screen "call_options" timeout 20.0
        assert eval wrong_choice_history["A"] == 3
        assert eval not has("camera_cart") and not urgent_note_written
        assert eval "카트" not in latest_warning
        assert eval "신고다" in latest_warning
        assert eval "{u}" in latest_warning
        click id "call_no"
        advance until screen "handwritten" timeout 20.0
        click id "finish_writing" until not screen "handwritten"
        advance until screen "investigation" timeout 20.0
        click id "inspect_light"
        advance until screen "handwritten" timeout 20.0
        click id "finish_writing" until not screen "handwritten"
        advance until screen "handwritten" timeout 20.0
        click id "finish_writing" until not screen "handwritten"
        advance until screen "judgment" timeout 20.0
        assert eval urgent_note_written and has("black_button") and has("camera_cart")
        click id "judge_success"
        advance until screen "handwritten" timeout 20.0
        click id "finish_writing" until not screen "handwritten"
        advance until screen "end_chapter" timeout 20.0
        assert eval chapter_complete
        assert eval any(n[0] == "escape" for n in notes)

    testcase judgment_recovery:
        run MainMenu(confirm=False)
        advance until screen "main_menu" timeout 20.0
        click id "start_game"
        advance until screen "handwritten" timeout 20.0
        click id "finish_writing" until not screen "handwritten"
        advance until screen "investigation" timeout 20.0
        click id "inspect_notice"
        advance until screen "notice_page" timeout 20.0
        click id "close_notice" until not screen "notice_page"
        advance until screen "handwritten" timeout 20.0
        click id "finish_writing" until not screen "handwritten"
        advance until screen "investigation" timeout 20.0
        click id "inspect_drawer"
        advance until screen "evidence_fragment" timeout 20.0
        click id "close_fragment" until not screen "evidence_fragment"
        advance until screen "handwritten" timeout 20.0
        click id "finish_writing" until not screen "handwritten"
        advance until screen "call_options" timeout 20.0
        click id "call_no"
        advance until screen "handwritten" timeout 20.0
        click id "finish_writing" until not screen "handwritten"
        advance until screen "investigation" timeout 20.0
        click id "inspect_light"
        advance until screen "handwritten" timeout 20.0
        click id "finish_writing" until not screen "handwritten"
        advance until screen "handwritten" timeout 20.0
        click id "finish_writing" until not screen "handwritten"
        advance until screen "judgment" timeout 20.0
        assert eval urgent_note_written and has("black_button") and has("camera_cart")
        click id "judge_B"
        advance until screen "handwritten" timeout 20.0
        click id "finish_writing" until not screen "handwritten"
        advance until screen "sorting_card" timeout 20.0
        pause 3.2
        advance until screen "handwritten" timeout 20.0
        click id "finish_writing" until not screen "handwritten"
        advance until screen "handwritten" timeout 20.0
        click id "finish_writing" until not screen "handwritten"
        advance until screen "judgment" timeout 20.0
        click id "judge_C"
        advance until screen "handwritten" timeout 20.0
        click id "finish_writing" until not screen "handwritten"
        advance until screen "sorting_card" timeout 20.0
        pause 3.2
        advance until screen "handwritten" timeout 20.0
        click id "finish_writing" until not screen "handwritten"
        advance until screen "handwritten" timeout 20.0
        click id "finish_writing" until not screen "handwritten"
        advance until screen "judgment" timeout 20.0
        click id "judge_B"
        advance until screen "handwritten" timeout 20.0
        click id "finish_writing" until not screen "handwritten"
        advance until screen "sorting_card" timeout 20.0
        pause 3.2
        advance until screen "handwritten" timeout 20.0
        click id "finish_writing" until not screen "handwritten"
        advance until screen "handwritten" timeout 20.0
        click id "finish_writing" until not screen "handwritten"
        advance until screen "judgment" timeout 20.0
        click id "judge_C"
        advance until screen "handwritten" timeout 20.0
        click id "finish_writing" until not screen "handwritten"
        advance until screen "sorting_card" timeout 20.0
        pause 3.2
        advance until screen "handwritten" timeout 20.0
        click id "finish_writing" until not screen "handwritten"
        advance until screen "handwritten" timeout 20.0
        click id "finish_writing" until not screen "handwritten"
        advance until screen "judgment" timeout 20.0
        click id "judge_B"
        advance until screen "handwritten" timeout 20.0
        click id "finish_writing" until not screen "handwritten"
        advance until screen "sorting_card" timeout 20.0
        pause 3.2
        advance until screen "handwritten" timeout 20.0
        click id "finish_writing" until not screen "handwritten"
        advance until screen "handwritten" timeout 20.0
        click id "finish_writing" until not screen "handwritten"
        advance until screen "judgment" timeout 20.0
        click id "judge_C"
        advance until screen "handwritten" timeout 20.0
        click id "finish_writing" until not screen "handwritten"
        advance until screen "sorting_card" timeout 20.0
        pause 3.2
        advance until screen "handwritten" timeout 20.0
        click id "finish_writing" until not screen "handwritten"
        advance until screen "handwritten" timeout 20.0
        click id "finish_writing" until not screen "handwritten"
        advance until screen "judgment" timeout 20.0
        assert eval wrong_choice_history == {"A":0,"B":3,"C":3}
        assert eval len([n for n in notes if n[0] == "urgent"]) == 1
        assert eval "카트 뒤" in latest_warning
        assert eval all(n[2].endswith(TRUST_LINE) for n in warnings)
        assert eval clock_label(True) == "21:47"
        assert eval renpy.config.allow_skipping and not skip_locked
        run Show("notebook", tab="warnings")
        screenshot "warnings.png"
        click id "close_notebook" until not screen "notebook"
        run FileLoad("auto-1", confirm=False)
        advance until screen "judgment" timeout 20.0
        assert eval wrong_choice_history["C"] == 3
        assert eval len(warnings) == 6
        click id "judge_success"
        advance until screen "handwritten" timeout 20.0
        click id "finish_writing" until not screen "handwritten"
        advance until screen "end_chapter" timeout 20.0
        assert eval chapter_complete
        assert eval any(n[0] == "escape" for n in notes)


