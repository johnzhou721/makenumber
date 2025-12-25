try:
    from toga_cocoa.dialogs import QuestionDialog, NSAlertDialog
    from toga_cocoa.libs import NSAlertStyle
    def __patch_init(self, title, message):
        NSAlertDialog.__init__(
            self,
            title=title,
            message=message,
            alert_style=NSAlertStyle.Critical,
            completion_handler=self.bool_completion_handler,
        )
    def __patch_build_dialog(self):
        okay = self.native.addButtonWithTitle("Yes")
        okay.hasDestructiveAction = True
        self.native.addButtonWithTitle("No")
    QuestionDialog.__init__ = __patch_init
    QuestionDialog.build_dialog = __patch_build_dialog
except ImportError:
    pass

try:
    from toga_iOS.dialogs import AlertDialog, QuestionDialog
    from toga_iOS.libs import UIAlertActionStyle, UIAlertAction
    from rubicon_objc import Block
    def __patch_add_destructive_response_button(self, label):
        self.native.addAction(
            UIAlertAction.actionWithTitle(
                label,
                style=UIAlertActionStyle.Destructive,
                handler=Block(self.true_response, None, objc_id),
            )
        )
    AlertDialog.add_destructive_response_button = __patch_add_destructive_response_button
    def __patch_populate_dialog(self):
        self.add_destructive_response_button("Yes")
        self.add_false_response_button("No")
    QuestionDialog.populate_dialog = __patch_populate_dialog
except ImportError:
    pass

try:
    from toga_winforms.dialogs import QuestionDialog, MessageDialog
    from System.Windows.Forms import DialogResult, MessageBoxButtons, MessageBoxIcon
    def __patch_init(self, title, message):
        MessageDialog.__init__(
            self,
            title,
            message,
            MessageBoxButtons.YesNo,
            MessageBoxIcon.Warning,
            success_result=DialogResult.Yes,
        )
    QuestionDialog.__init__ = __patch_init
except:
    pass
