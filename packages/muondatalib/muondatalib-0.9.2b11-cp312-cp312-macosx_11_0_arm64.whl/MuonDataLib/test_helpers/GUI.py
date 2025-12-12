import time


def check_no_alert(dash_duo):
    """
    Want to check that the alert has not
    opened if everything works.
    This means that the 'error' element
    is not findable. So we use a try
    :input dash_duo:
    """
    try:
        assert (dash_duo.find_element('#error').is_enabled)
        # should not have an alert, so above should throw
        assert (False)
    except Exception:
        return


def wait_and_press_btn(dash_duo, name):
    """
    Method to wait for the loading to
    complete and then click an element
    (button).
    :param dash_duo:
    :param name: the name/ID of the button
    """
    active = False
    while not active:
        try:
            dash_duo.find_element('#' + name).click()
            active = True
        except Exception:
            time.sleep(.1)
