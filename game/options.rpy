define config.name = "온결 · 괜찮아지는 방"
define config.version = "0.1.0"
define config.window_title = "온결 — 제1장 괜찮아지는 방"
define config.screen_width = 1280
define config.screen_height = 720
define config.save_directory = "OnGyeol-Chapter1-2026"
define config.has_sound = True
define config.has_music = True
define config.has_voice = False
define config.rollback_enabled = False
define config.autosave_on_choice = False
define config.autosave_on_quit = True
define config.autosave_frequency = 100
define config.default_text_cps = 32
define config.default_music_volume = 0.18
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

init python:
    build.name = "OnGyeol-0.1.0"
    build.executable_name = "OnGyeol"
    build.include_update = False
    build.classify("game/tests.rpy", None)
    build.classify("game/tests.rpyc", None)
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

