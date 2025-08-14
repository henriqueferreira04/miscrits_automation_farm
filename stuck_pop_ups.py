import keep_release
import mission_complete
import level_up

def check_for_stuck_popups(reader):
    value = keep_release.keep_release_miscrit(reader)
    if not value:
        value = mission_complete.mission_success(reader)

    if not value:
        value = level_up.rank_up_character(reader)

