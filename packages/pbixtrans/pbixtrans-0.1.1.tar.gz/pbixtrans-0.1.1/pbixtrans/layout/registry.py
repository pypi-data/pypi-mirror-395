from pbixtrans.layout.visuals.actionbutton import translate_actionbutton
from pbixtrans.layout.visuals.shape import translate_shape
from pbixtrans.layout.visuals.slicer import translate_slicer
from pbixtrans.layout.visuals.textbox import translate_textbox

VISUAL_TRANSLATORS = {
    "actionButton": translate_actionbutton,
    "shape": translate_shape,
    "slicer": translate_slicer,
    "textbox": translate_textbox,
}