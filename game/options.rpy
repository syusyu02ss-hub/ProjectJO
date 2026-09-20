define config.name = "평온의 방"
define config.version = "0.2.0"
define config.window_title = "평온의 방"
define config.screen_width = 1920
define config.screen_height = 1080
define config.save_directory = "PyeongonuiBang-2026"
define config.has_sound = True
define config.has_music = True
define config.has_voice = False
define config.rollback_enabled = False
define config.autosave_on_choice = False
define config.autosave_on_quit = False
define config.autosave_frequency = None
# 글자 출력은 2~80자/초 범위로 제한한다. 56은 최고 속도의 70%다.
define config.default_text_cps = 56
define config.default_music_volume = 0.12
define config.default_sfx_volume = 0.55
define config.default_fullscreen = False
define config.window = "auto"
define config.history_length = 180
define config.enter_transition = Dissolve(0.15)
define config.exit_transition = Dissolve(0.15)
define config.intra_transition = Dissolve(0.15)
default preferences.skip_unseen = False
default preferences.skip_after_choices = False
default persistent.reduced_motion = False
default persistent.show_hotspots = True
default persistent.text_speed_settings_version = 0

init python:
    TEXT_CPS_MIN = 2
    TEXT_CPS_MAX = 80
    TEXT_CPS_DEFAULT = 56

    def normalize_text_cps():
        """기존 속도 설정을 새 범위와 기본값으로 한 번만 옮긴다."""
        if persistent.text_speed_settings_version < 2:
            renpy.game.preferences.text_cps = TEXT_CPS_DEFAULT
            persistent.text_speed_settings_version = 2
            return

        cps = renpy.game.preferences.text_cps
        if cps == 0:
            renpy.game.preferences.text_cps = TEXT_CPS_MAX
        elif cps < TEXT_CPS_MIN:
            renpy.game.preferences.text_cps = TEXT_CPS_MIN
        elif cps > TEXT_CPS_MAX:
            renpy.game.preferences.text_cps = TEXT_CPS_MAX

    config.start_callbacks.append(normalize_text_cps)
    config.after_load_callbacks.append(normalize_text_cps)

    build.name = "PyeongonuiBang-0.2.0"
    build.executable_name = "PyeongonuiBang"
    build.include_update = False
    build.classify("game/tests.rpy", None)
    build.classify("game/tests.rpyc", None)
    build.classify("tools/**", None)
    build.classify(".git/**", None)
    build.classify(".vscode/**", None)
    build.classify("test-results/**", None)
    build.classify("game/saves/**", None)
    build.classify("game/cache/**", None)
    build.classify("**.log", None)
    build.classify("**.txt", None)
    build.classify("game/fonts/*OFL.txt", "all")
    build.classify("README.md", "all")
    build.classify("CREDITS.md", "all")
    build.classify("**.rpy", "all")
    build.classify("**.rpyc", "all")
    build.documentation("README.md")
    build.documentation("CREDITS.md")
    renpy.music.register_channel("ambience", mixer="sfx", loop=True)
    renpy.music.register_channel("foley", mixer="sfx", loop=False)

label before_main_menu:
    $ normalize_text_cps()
    return
