from ctypes import windll
import cv2 as cv
import numpy as np
import win32gui

from sys_interfaces import *
from image import *


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

    # beginning game stuff
    need_manager = GameImage(rectangle, "assets/empty_manager.jpg", 0.9)
    miner_ready = GameImage(rectangle, "assets/miner.jpg", 0.9)
    elevator_ready = GameImage(rectangle, "assets/elevator_ready.jpg", 0.9)
    warehouse_ready = GameImage(rectangle, "assets/warehouse_ready2.jpg", 0.9)

    # buttons
    new_shaft = GameImage(rectangle, "assets/new_shaft.jpg", 0.9)
    X = GameImage(rectangle, "assets/X.jpg", 0.9)
    X2 = GameImage(rectangle, "assets/X2.jpg", 0.9)
    X3 = GameImage(rectangle, "assets/X3.jpg", 0.9)
    upgrade_btn = GameImage(rectangle, "assets/can_upgrade.jpg", 0.9)
    hire_manager_btn = GameImage(rectangle, "assets/hire_manager.jpg", 0.9)
    managers_btn = GameImage(rectangle, "assets/manager_btn.jpg", 0.9)
    activate_managers_btn = GameImage(rectangle, "assets/activate_manager_btn.jpg", 0.85)

    # rocks
    # TODO: add more rocks
    rocks = (
        GameImage(rectangle, "assets/rocks1.jpg", 0.9),
        GameImage(rectangle, "assets/rocks2.jpg", 0.9),
        GameImage(rectangle, "assets/rocks3.jpg", 0.9)
    )

    # colors
    # enough_gold_color = (255, 255, 255)
    not_enough_gold_color = (78, 87, 244)  # B, G, R


    def click_at_center(rectangle_):
        click(get_center_of_rectangle(rectangle_)[0], get_center_of_rectangle(rectangle_)[1] + 20, window_rectangle)

    def find_x(screenshot_):
        if X.find(screenshot_):
            return X.find(screenshot_)
        elif X2.find(screenshot_):
            return X2.find(screenshot_)
        elif X3.find(screenshot_):
            return X3.find(screenshot_)
        else:
            return

    def find_upgrade_arrow(screenshot_):
        if upgrade_arrow2.find(screenshot_):
            return upgrade_arrow2.find(screenshot_), 0
        elif upgrade_arrow3.find(screenshot_):
            return upgrade_arrow3.find(screenshot_), 1
        else:
            return

    def update_screenshot():
        screenshot_ = get_screenshot(hwnd)
        screenshot_ = np.array(screenshot_)
        return cv.cvtColor(screenshot_, cv.COLOR_RGB2BGR)

    def find_rocks(screenshot_):
        for rock in rocks:
            if rock.find(screenshot_):
                return rock.find(screenshot_)
        return

    clicked_managers = 0
    activated_managers = False
    # assume we start at the top
    go_down = True
    while True:
        window_rectangle = win32gui.GetWindowRect(hwnd)
        screenshot = update_screenshot()

        # if miner_ready.find(screenshot):
        #     rectangle = miner_ready.find(screenshot)
        #     click_at_center(rectangle)
        # if elevator_ready.find(screenshot):
        #     rectangle = elevator_ready.find(screenshot)
        #     click_at_center(rectangle)
        # if warehouse_ready.find(screenshot):
        #     rectangle = warehouse_ready.find(screenshot)
        #     click_at_center(rectangle)

        if need_manager.find(screenshot):
            rectangle = need_manager.find(screenshot)
            click(get_center_of_rectangle(rectangle)[0], get_center_of_rectangle(rectangle)[1], window_rectangle)
            sleep(1)
            screenshot = update_screenshot()
            rectangle = hire_manager_btn.find(screenshot)
            if rectangle:
                # may make it not spend all $ on managers lol
                if clicked_managers == 0:
                    click_at_center(rectangle)
                    clicked_managers += 1
                else:
                    clicked_managers = 0
        elif find_x(screenshot):
            rectangle = find_x(screenshot)
            click_at_center(rectangle)
        elif find_upgrade_arrow(screenshot):
            rectangle, is_elevator = find_upgrade_arrow(screenshot)
            if rectangle:
                if is_elevator == 1:
                    click(get_center_of_rectangle(rectangle)[0] - 10, get_center_of_rectangle(rectangle)[1] + 10,
                          window_rectangle)
                    print("Found upgrade arrow2")
                else:
                    click(get_center_of_rectangle(rectangle)[0] + 10, get_center_of_rectangle(rectangle)[1] + 10,
                          window_rectangle)
                    print("Found upgrade arrow1")
                sleep(0.2)
                do_again = True
                while do_again:
                    screenshot = update_screenshot()
                    rectangle = upgrade_btn.find(screenshot)
                    if rectangle:
                        click(get_center_of_rectangle(rectangle)[0], get_center_of_rectangle(rectangle)[1] - 5,
                              window_rectangle)
                        print("Found upgrade btn")
                    else:
                        do_again = False
                    sleep(0.2)

        elif upgrade_arrow.find(screenshot):
            rectangle = upgrade_arrow.find(screenshot)
            if rectangle:
                click(get_center_of_rectangle(rectangle)[0] + 10, get_center_of_rectangle(rectangle)[1] + 10,
                      window_rectangle)
                print("Found upgrade arrow")
                sleep(0.2)
                do_again = True
                while do_again:
                    screenshot = update_screenshot()
                    rectangle = upgrade_btn.find(screenshot)
                    if rectangle:
                        click(get_center_of_rectangle(rectangle)[0], get_center_of_rectangle(rectangle)[1] - 5,
                              window_rectangle)
                        print("Found upgrade btn")
                    else:
                        do_again = False
                    sleep(0.2)
        else:
            if not activated_managers:
                rectangle = managers_btn.find(screenshot)
                if rectangle:
                    click_at_center(rectangle)
                    rectangle = activate_managers_btn.find(screenshot)
                    if rectangle:
                        click_at_center(rectangle)
                activated_managers = True
            else:
                # if going down and not finding rocks
                if go_down and not find_rocks(screenshot):
                    scroll(False, 3)
                # else if rocks found
                elif find_rocks(screenshot):
                    go_down = False
                else:
                    scroll(True, 3)

        sleep(0.5)


main()
