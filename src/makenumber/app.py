"""
A game where numbers are provided from which to use +, -, *, /, and parenthesis to make other numbers from.
"""

import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW, CENTER, START, END
from .generate_expression import generate_expression
from . import compat

class MakeNumber(toga.App):
    def startup(self):
        """Construct and show the Toga application.

        Usually, you would add your application to a main content box.
        We then create a main window (with a name matching the app), and
        show the main window.
        """
        main_box = toga.Box()
        self.vbox = toga.Box(style=Pack(direction=COLUMN, margin=10, gap=10, align_items=CENTER))
        
        self.opbox = toga.Box(style=Pack(direction=ROW, gap=10, justify_content=CENTER))
        for op in ['+', '-', '*', '/', '(', ')']:
            self.opbox.add(
                button := toga.Button(
                    text=op,
                    on_press=lambda widget, op=op: self.button_handler(widget, op),
                )
            )
            if toga.platform.current_platform == "android":
                # Android prioritizes touchability, and hints buttons
                # to a larger minimum size.  But it's too large, so we
                # break the rules here a bit to avoid overflow, opting for
                # a smaller yet still not "just fitting" size.
                button.width = 67

        self.numberbox = toga.Box(style=Pack(direction=ROW, gap=10, justify_content=CENTER))
        self.target = toga.Label("Target:")

        # https://pixabay.com/vectors/undo-arrow-icon-black-148064/
        self.undo_button = toga.Button(icon="resources/undo", on_press=self.on_undo)

        self.attempt_label = toga.Label("")
        self.attempt_label_cont = toga.Box(children=[self.attempt_label], direction=ROW)

        self.result_label = toga.Label("Invalid Expression")
        self.result_label_cont = toga.Box(children=[self.result_label], direction=ROW)

        self.restart = toga.Button("New Game", on_press=lambda widget: self.new_game())
        self.give_up = toga.Button("Give Up", on_press=self.on_give_up)
        self.give_up.background_color = "red"
        self.give_up.color = "white"

        self.controls_box = toga.Box(
            children=[
                toga.Box(
                    children=[self.restart],
                    flex=1,
                    direction=ROW,
                    justify_content=START,
                ),
                toga.Box(
                    children=[self.give_up],
                    flex=1,
                    direction=ROW,
                    justify_content=CENTER,
                ),
                toga.Box(
                    children=[self.undo_button],
                    flex=1,
                    direction=ROW,
                    justify_content=END,
                ),
            ],
            direction=ROW,
            align_items=CENTER
        )
        self.vbox.add(self.controls_box)
        self.vbox.add(self.numberbox)
        self.vbox.add(self.opbox)
        self.vbox.add(self.target)
        self.vbox.add(self.attempt_label_cont)
        self.vbox.add(self.result_label_cont)

        self.new_game()

        self.main_window = toga.MainWindow(title=self.formal_name)
        self.main_window.content = self.vbox
        self.main_window.show()

    async def on_give_up(self, widget):
        confirmation = toga.QuestionDialog(
            "Are you sure?",
            "Are you sure you want to give up?  "
                "Figuring out the solution yourself can be both rewarding"
                " and educational.",
        )

        if await self.main_window.dialog(confirmation):
            self.result_label.text = "The answer can be " + self.goal
            self.result_label.color = "red"
            self.game_finish()
        else:
            encouragement = toga.InfoDialog(
                "Good job for not giving up!",
                "That's the spirit!  Keep trying!"
            )
            await self.main_window.dialog(encouragement)

    def game_finish(self):
        for button in self.numberbox.children:
            button.enabled = False
        for button in self.opbox.children:
            button.enabled = False
        self.undo_button.enabled = False
        self.give_up.enabled = False
    
    def new_game(self):
        self.attempt = []
        self.attempt_label.text = ""
        goal, answer, numbers = generate_expression()
        self.goal = goal
        print(goal)
        self.target.text = "Target: " + str(int(answer))
        self.numberbox.clear()
        for number in numbers:
            number_button = toga.Button(
                text=number,
                on_press=lambda widget, number=number: self.button_handler(widget, number),
            )
            self.numberbox.add(number_button)
            if toga.platform.current_platform == "android":
                # Android prioritizes touchability, and hints buttons
                # to a larger minimum size.  But it's too large, so we
                # break the rules here a bit to avoid overflow, opting for
                # a smaller yet still not "just fitting" size.
                number_button.width = 67
        for child in self.opbox.children:
            child.enabled = True
        self.undo_button.enabled = False
        self.give_up.enabled = True
        del self.result_label.color
        self.update_intrastate()

    def update_intrastate(self):
        self.attempt_label.text = " ".join(map(str, self.attempt))
        try:
            self.result_label.text = "=" + str(eval(self.attempt_label.text))
        except SyntaxError:
            self.result_label.text = "Invalid Expression"
        except TypeError:
            self.result_label.text = "Invalid Expression"

        if (
            self.result_label.text != "Invalid Expression"
            and (
                abs(
                    float(self.result_label.text.removeprefix("="))
                    - int(self.target.text.removeprefix("Target: "))
                ) < 1e-13
            )
        ):
            self.result_label.text = "You did it!"
            self.result_label.color = "green"
            self.game_finish()
    
    def button_handler(self, widget, op):
        self.attempt.append(op)
        if widget in self.numberbox.children:
            widget.enabled = False
        self.undo_button.enabled = True
        self.update_intrastate()

    def on_undo(self, widget):
        element = self.attempt.pop()
        if not self.attempt:
            self.undo_button.enabled = False
        for button in self.numberbox.children:
            if button.text == str(element) and not button.enabled:
                button.enabled = True
                break
        self.update_intrastate()



def main():
    return MakeNumber()
