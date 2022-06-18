from ctypes import windll

from sys_interfaces import *
from image import *
from datetime import datetime as dt
from datetime import timedelta


def main():
    # Makes program aware of DPI scaling,
    windll.user32.SetProcessDPIAware()
    hwnd = get_hwnd("bluestacks")
    win32gui.SetForegroundWindow(hwnd)
    rectangle = win32gui.GetWindowRect(hwnd)

    # arrows
    arrow = GameImage(rectangle, "assets/arrow.jpg", 0.85)
    smol_arrow = GameImage(rectangle, "assets/smol_arrow.jpg", 0.85)

    upgrade_arrow = GameImage(rectangle, "assets/upgrade_arrow.jpg", 0.95)
    upgrade_arrow2 = GameImage(rectangle, "assets/upgrade_arrow2.jpg", 0.95)
    upgrade_arrow3 = GameImage(rectangle, "assets/upgrade_arrow3.jpg", 0.9)
    stacked_up_arrow = GameImage(rectangle, "assets/stacked_upgrade_arrow2.jpg", 0.9)

    # beginning game stuff
    need_manager = GameImage(rectangle, "assets/empty_manager.jpg", 0.9)
    miner_ready = GameImage(rectangle, "assets/miner.jpg", 0.9)
    elevator_ready = GameImage(rectangle, "assets/elevator_ready.jpg", 0.9)
    warehouse_ready = GameImage(rectangle, "assets/warehouse_ready2.jpg", 0.9)

    # buttons
    new_shaft = GameImage(rectangle, "assets/new_shaft.jpg", 0.9)
    xs = (
        GameImage(rectangle, "assets/X.jpg", 0.9),
        GameImage(rectangle, "assets/X2.jpg", 0.9),
        GameImage(rectangle, "assets/X3.jpg", 0.9),
        GameImage(rectangle, "assets/X4.jpg", 0.9),
        GameImage(rectangle, "assets/X5.jpg", 0.9)
    )
    upgrade_btn = GameImage(rectangle, "assets/can_upgrade.jpg", 0.9)
    hire_manager_btn = GameImage(rectangle, "assets/hire_manager.jpg", 0.9)
    managers_btn = GameImage(rectangle, "assets/manager_btn.jpg", 0.9)
    activate_managers_btn = GameImage(rectangle, "assets/activate_manager_btn.jpg", 0.9)
    leave = GameImage(rectangle, "assets/leave_stupid_mine.jpg", 0.9)

    # rocks
    # TODO: add more rocks
    stop_scrolling = (
        GameImage(rectangle, "assets/rocks1.jpg", 0.9),
        GameImage(rectangle, "assets/rocks2.jpg", 0.9),
        GameImage(rectangle, "assets/rocks3.jpg", 0.9),
        GameImage(rectangle, "assets/new_shaft_supercash.jpg", 0.9)
        # GameImage(rectangle, "assets/skip_barrier.jpg", 0.9)
    )
    sky = GameImage(rectangle, "assets/sky2.jpg", 0.9)

    # colors
    # enough_gold_color = (255, 255, 255)
    not_enough_gold_color = (78, 87, 244)  # B, G, R

    def min_between(d1, d2):
        return int(abs((d2 - d1).seconds / 60))

    def click_at_center(rectangle_):
        click(get_center_of_rectangle(rectangle_)[0], get_center_of_rectangle(rectangle_)[1] + 20, window_rectangle)

    def get(iterator_, screenshot_):
        for item in iterator_:
            if item.find(screenshot_):
                return item.find(screenshot_)

    def find_upgrade_arrow(screenshot_):
        if upgrade_arrow2.find(screenshot_):
            return upgrade_arrow2.find(screenshot_), 0
        elif upgrade_arrow3.find(screenshot_):
            return upgrade_arrow3.find(screenshot_), 1
        # elif upg
        else:
            return

    def update_screenshot():
        screenshot_ = get_screenshot(hwnd)
        screenshot_ = np.array(screenshot_)
        return cv.cvtColor(screenshot_, cv.COLOR_RGB2BGR)

    clicked_managers = 0
    last_activated_managers = dt.now() - timedelta(minutes=7)
    # assume we start at the top
    go_down = True
    while True:
        window_rectangle = win32gui.GetWindowRect(hwnd)
        screenshot = update_screenshot()
        current_time = dt.now()

        # if miner_ready.find(screenshot):
        #     rectangle = miner_ready.find(screenshot)
        #     click_at_center(rectangle)
        # if elevator_ready.find(screenshot):
        #     rectangle = elevator_ready.find(screenshot)
        #     click_at_center(rectangle)
        # if warehouse_ready.find(screenshot):
        #     rectangle = warehouse_ready.find(screenshot)
        #     click_at_center(rectangle)
        if leave.find(screenshot):
            click_at_center(leave.find(screenshot))
            sleep(0.2)
            screenshot = update_screenshot()
            if leave.find(screenshot):
                click_at_center(leave.find(screenshot))

        elif need_manager.find(screenshot):
            rectangle = need_manager.find(screenshot)
            click(get_center_of_rectangle(rectangle)[0], get_center_of_rectangle(rectangle)[1], window_rectangle)
            sleep(0.5)
            screenshot = update_screenshot()
            rectangle = hire_manager_btn.find(screenshot)
            if rectangle:
                # may make it not spend all $ on managers lol
                if clicked_managers == 0:
                    click_at_center(rectangle)
                    clicked_managers += 1
                else:
                    clicked_managers = 0
        elif get(xs, screenshot):
            rectangle = get(xs, screenshot)
            click_at_center(rectangle)

        elif new_shaft.find(screenshot):
            click_at_center(new_shaft.find(screenshot))

        elif find_upgrade_arrow(screenshot):
            rectangle, is_elevator = find_upgrade_arrow(screenshot)
            if rectangle[1] > 600:
                scroll(False, 3)
            sleep(0.2)
            screenshot = update_screenshot()
            sleep(0.2)
            rectangle, is_elevator = find_upgrade_arrow(screenshot)
            if rectangle:
                if is_elevator == 1:
                    click(get_center_of_rectangle(rectangle)[0] - 10, get_center_of_rectangle(rectangle)[1] + 10,
                          window_rectangle)
                    # print("Found upgrade arrow2")
                else:
                    click(get_center_of_rectangle(rectangle)[0] + 10, get_center_of_rectangle(rectangle)[1] + 10,
                          window_rectangle)
                    # print("Found upgrade arrow1")
                sleep(0.2)
                do_again = True
                while do_again:
                    screenshot = update_screenshot()
                    rectangle = upgrade_btn.find(screenshot)
                    if rectangle:
                        click(get_center_of_rectangle(rectangle)[0], get_center_of_rectangle(rectangle)[1] - 5,
                              window_rectangle)
                        # print("Found upgrade btn")
                    else:
                        do_again = False
                    sleep(0.2)
        elif stacked_up_arrow.find(screenshot):
            rectangle = stacked_up_arrow.find(screenshot)
            if rectangle[1] > 600:
                scroll(False, 3)
            sleep(0.2)
            screenshot = update_screenshot()
            sleep(0.2)
            rectangle = stacked_up_arrow.find(screenshot)
            if rectangle:
                click(get_center_of_rectangle(rectangle)[0] + 5, get_center_of_rectangle(rectangle)[1] + 10,
                  window_rectangle)
            sleep(0.2)
            do_again = True
            while do_again:
                screenshot = update_screenshot()
                rectangle = upgrade_btn.find(screenshot)
                if rectangle:
                    click(get_center_of_rectangle(rectangle)[0], get_center_of_rectangle(rectangle)[1] - 5,
                          window_rectangle)
                    # print("Found upgrade btn")
                else:
                    do_again = False
                sleep(0.2)

        elif upgrade_arrow.find(screenshot):
            rectangle = upgrade_arrow.find(screenshot)
            # print(rectangle)
            if rectangle[1] > 600:
                scroll(False, 3)
            sleep(0.2)
            screenshot = update_screenshot()
            sleep(0.2)
            rectangle = upgrade_arrow.find(screenshot)
            if rectangle:
                click(get_center_of_rectangle(rectangle)[0] + 5, get_center_of_rectangle(rectangle)[1] + 10,
                      window_rectangle)
                # print("Found upgrade arrow")
                sleep(0.2)
                do_again = True
                while do_again:
                    screenshot = update_screenshot()
                    rectangle = upgrade_btn.find(screenshot)
                    if rectangle:
                        click(get_center_of_rectangle(rectangle)[0], get_center_of_rectangle(rectangle)[1] - 5,
                              window_rectangle)
                        # print("Found upgrade btn")
                    else:
                        do_again = False
                    sleep(0.2)
        else:
            # print('...')
            # pass
            _sky = sky.find(screenshot)
            _rocks = get(stop_scrolling, screenshot)
            # _rocks = stop_scrolling.find(screenshot)
            # if going down and not finding rocks
            if go_down and not _rocks:
                scroll(False, 3)
            # else if going down and rocks found
            elif go_down and _rocks:
                go_down = False
            # else if go up and sky not found
            elif not go_down and not _sky:
                scroll(True, 3)
            # else if go up and sky found
            else:
                go_down = True

        sleep(0.3)

        if min_between(last_activated_managers, current_time) >= 7:
            rectangle = managers_btn.find(screenshot)
            if rectangle:
                click_at_center(rectangle)
                sleep(0.5)
                screenshot = update_screenshot()
                rectangle = activate_managers_btn.find(screenshot)
                if rectangle:
                    click_at_center(rectangle)
                last_activated_managers = dt.now()
                print("Activated managers at %s" % last_activated_managers)


failures = 0
while True:
    try:
        main()
        # print("running")
        # sleep(0.5)
    except (Exception, KeyboardInterrupt) as e:
        if type(e) == KeyboardInterrupt:
            print("Breaking")
            break
        else:
            print("Error running main. Text: " + str(e))
            failures += 1
            print("Failures: " + str(failures))
            sleep(5)
# main()
