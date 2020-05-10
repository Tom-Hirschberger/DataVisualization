# ===========================================================================
#   rsshow.py ---------------------------------------------------------------
# ===========================================================================

#   import ------------------------------------------------------------------
# ---------------------------------------------------------------------------
from rsvis.__init__ import _logger
from rsvis.utils import imgtools
import rsvis.utils.imgio
import rsvis.utils.objindex

import rsvis.tools.options
import rsvis.tools.rsshowui


#   function ----------------------------------------------------------------
# ---------------------------------------------------------------------------
def run(
        files, 
        param_specs, 
        param_in,
        param_out=dict(),
        param_classes=list(),
        param_show=dict(),  
    ):
        
    _logger.debug("Start training multi task classification and regression model with settings:\nparam_specs:\t{}\nparam_in:\t{}\nparam_out:\t{}\nparam_classes:\t{}\nparam_show:\t{}".format(param_specs, param_in, param_out, param_classes, param_show))

    #   settings ------------------------------------------------------------
    # -----------------------------------------------------------------------
    param_label = dict((str(c["label"][0]), c["label"][1]) for c in param_classes if "label" in c)
    
    rsio = rsvis.utils.rsioobject.RSIOObject(files, param_specs, param_in, param_out, param_show, label=param_label
    )

    ui = rsvis.tools.rsshowui.RSShowUI(
        rsio,
        options = rsvis.tools.options.get_lecture_options(
            param_specs, param_label=param_label
        ), 
        classes = param_classes,
        objects = rsio,
        logger = _logger,
        **param_show)

    ui.imshow(wait=True)