# gpe_lib/notebook/colab/__init__.py
# --- IMPORTS ---------------------------------------------------------------
import os
from google.colab import output, files

# --- DECLARATIONS ----------------------------------------------------------

# --- FUNCTIONS -------------------------------------------------------------
def settings():
    import matplotlib.pyplot as plt
    plt.rcParams["figure.figsize"] = (9,3)
    plt.rcParams["legend.title_fontsize"] = "small"
    # output.enable_custom_widget_manager()
    
# --- COMMANDS --------------------------------------------------------------
print("""import contextlib,io
with contextlib.redirect_stdout(io.StringIO()):""")
settings()