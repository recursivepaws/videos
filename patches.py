import os
import typst
import janim.utils.typst_compile as tc
from janim.gui.timeline_view import TimelineView
from janim.gui.label import LazyLabelGroup, LabelGroup

# Override fonts dir to include custom fonts
font_dir = os.path.join(os.path.dirname(__file__), "fonts")
tc._typst_fonts = typst.Fonts(True, True, [font_dir])


# Recursively expand all timeline dropdowns in the GUI by default
def expand_all(label):
    if isinstance(label, LazyLabelGroup) and label._collapse:
        label.switch_collapse()  # initializes children + sets _collapse=False
    if isinstance(label, LabelGroup) and not label._collapse:
        for child in label.labels:
            expand_all(child)


if not getattr(TimelineView, "_init_label_group_patched", False):
    _orig_init_label_group = TimelineView.init_label_group

    def _patched_init_label_group(self):
        _orig_init_label_group(self)
        if self.subtimeline_label_group is not None:
            for label in self.subtimeline_label_group.labels:
                expand_all(label)

    TimelineView.init_label_group = _patched_init_label_group
    TimelineView._init_label_group_patched = True  # type: ignore[attr-defined]


# Use gui_name property on Timeline subclasses to customise the label in the GUI
if not getattr(TimelineView, "_make_subtimeline_name_patched", False):
    _orig_make_subtimeline_label_group = TimelineView.make_subtimeline_label_group

    @staticmethod
    def _patched_make_subtimeline_label_group(built):
        renames = {}
        for item in built.timeline.subtimeline_items:
            tl = item._built.timeline
            if hasattr(tl, "gui_name"):
                cls = tl.__class__
                renames[tl] = cls.__name__
                cls.__name__ = tl.gui_name
        try:
            result = _orig_make_subtimeline_label_group(built)
        finally:
            for tl, original in renames.items():
                tl.__class__.__name__ = original

        # Strip the ' at 0x... (item at 0x...)' suffix from renamed labels
        gui_names = {tl.gui_name for tl in renames}
        if result is not None:
            for label in result.labels:
                for gui_name in gui_names:
                    if label.name.startswith(gui_name + " at 0x"):
                        label.name = gui_name
                        break

        return result

    TimelineView.make_subtimeline_label_group = _patched_make_subtimeline_label_group
    TimelineView._make_subtimeline_name_patched = True  # type: ignore[attr-defined]
