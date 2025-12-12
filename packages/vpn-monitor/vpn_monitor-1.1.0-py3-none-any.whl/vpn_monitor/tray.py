import pystray
from PIL import Image, ImageDraw


def create_image(width=64, height=64, color1="#39c2d7", color2="white"):
    # Draw a Shield Icon
    image = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    dc = ImageDraw.Draw(image)

    # Shield shape
    dc.polygon(
        [(width // 2, height), (0, height // 3), (0, 0), (width, 0), (width, height // 3)],
        fill=color1,
    )
    # Inner Cross/Check
    m = 10
    dc.line((width // 2, m, width // 2, height - m), fill=color2, width=5)
    dc.line((m, height // 3, width - m, height // 3), fill=color2, width=5)

    return image


class TrayIcon:
    def __init__(self, on_exit, on_snooze, on_unsnooze, on_set_country, show_set_country=True):
        self.on_exit = on_exit
        self.on_snooze = on_snooze
        self.on_unsnooze = on_unsnooze
        self.on_set_country = on_set_country
        self.show_set_country = show_set_country

        self.icon = pystray.Icon(
            "VPN Monitor", create_image(), "VPN Monitor", menu=self._build_menu(is_snoozed=False)
        )

    def _build_menu(self, is_snoozed):
        if is_snoozed:
            snooze_item = pystray.MenuItem("Show Warning", self.on_unsnooze)
        else:
            snooze_item = pystray.MenuItem(
                "Hide Warning (Snooze)",
                pystray.Menu(
                    pystray.MenuItem("5 Minutes", lambda: self.on_snooze(5)),
                    pystray.MenuItem("15 Minutes", lambda: self.on_snooze(15)),
                    pystray.MenuItem("1 Hour", lambda: self.on_snooze(60)),
                    pystray.MenuItem("8 Hours", lambda: self.on_snooze(480)),
                ),
            )

        items = [snooze_item]
        if self.show_set_country:
            items.append(pystray.MenuItem("Set Country...", self.on_set_country))

        items.append(pystray.Menu.SEPARATOR)
        items.append(pystray.MenuItem("Exit", self.exit_action))

        return pystray.Menu(*items)

    def update_menu(self, is_snoozed):
        self.icon.menu = self._build_menu(is_snoozed)

    def exit_action(self, icon, item):
        self.icon.stop()
        if self.on_exit:
            self.on_exit()

    def run(self):
        self.icon.run()

    def stop(self):
        self.icon.stop()
