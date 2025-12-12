"""
* `Organization`:  InsightSolver Solutions Inc.
* `Project Name`:  InsightSolver
* `Module Name`:   insightsolver
* `File Name`:     visualization.py
* `Authors`:       Noé Aubin-Cadot <noe.aubin-cadot@insightsolver.com>,
                   Arthur Albo <arthur.albo@insightsolver.com>

Description
-----------
This file contains some visualization functions, some of which are integrated as a method of the InsightSolver class.

Naming conventions of the visualization functions
-------------------------------------------------
- ``draw_``: Draws the content on a specified ``plt.Axes``.
- ``make_``: Makes the ``plt.Figure`` with the content on it and return the figure.
- ``plot_``: Plots the content and show it to the user.

Utilities
---------
- ``classify_variable_as_continuous_or_categorical``: Classifies a variable as continuous or categorical.
- ``compute_feature_label``: Computes the label of a feature.
- ``truncate_label``: Truncates a label.
- ``p_value_to_p_text``: Converts the p-value to a text.
- ``load_icon``: Loads a PNG icon.
- ``wrap_text_with_word_boundary``: Wrap text on multiple lines.
- ``save_figs_in_pdf``: Stack multiple figures vertically on a page and save to PDF.

Mutual information
------------------
- ``draw_mutual_information``: Draws the mutual information on a given ``plt.Axes``.
- ``make_mutual_information``: Makes the mutual information ``plt.Figure``.
- ``plot_mutual_information``: Plots the mutual information and show it to the user.

Banner
------
- ``make_banner_img_for_i``: Makes the banner image.
- ``plot_banner_img_for_i``: Plots the banner image and show it to the user.
- ``make_banner_fig_for_i``: Makes the banner figure.
- ``plot_banner_fig_for_i``: Plots the banner figure and show it to the user.

Legend
------
- ``make_legend_img``: Makes the legend image.
- ``plot_legend_img``: Plots the legend image and show it to the user.
- ``make_legend_fig``: Makes the legend figure.
- ``plot_legend_fig``: Plots the legend figure and show it to the user.

Feature contributions
---------------------
- ``draw_feature_contributions_for_i``: Draws the feature contributions for the rule at index ``i`` on a given ``plt.Axes``.
- ``make_feature_contributions_for_i``: Makes the feature contributions for the rule at index ``i`` figures as a ``plt.Figure``.
- ``plot_feature_contributions_for_i``: Plots the feature contributions for the rule at index ``i`` and show them to the user.
- ``plot_feature_contributions_for_all``: Plots the feature contributions for all rules.

Feature distribution for feature
--------------------------------
- ``draw_feature_distribution_for_feature``: Draws the distribution for a specified feature on a given ``plt.Axes``.
- ``make_feature_distribution_for_feature``: Makes the distribution for a specified feature as a ``plt.Figure``.
- ``plot_feature_distribution_for_feature``: Plots the distribution for a specified feature and show it to the user.

Feature distributions for S
---------------------------
- ``draw_feature_distributions_for_S``: Draws the distributions of all features in a rule ``S`` on a given ``plt.Axes``.
- ``make_feature_distributions_for_S``: Makes the distributions of all features in a rule ``S`` as a ``plt.Figure``.
- ``plot_feature_distributions_for_S``: Plots the distributions of all features in a rule ``S`` and show it to the user.

Mosaic of rule vs complement for a feature for the rule i
---------------------------------------------------------
- ``draw_mosaic_rule_vs_comp_for_feature_for_i``: Draws the mosaic for a specified feature for the rule at index ``i`` on a given ``plt.Axes``.
- ``make_mosaic_rule_vs_comp_for_feature_for_i``: Makes the mosaic for a specified feature for the rule at index ``i`` as a ``plt.Figure``.
- ``plot_mosaic_rule_vs_comp_for_feature_for_i``: Plots the mosaic for a specified feature for the rule at index ``i`` and show it to the user.

Mosaics of rule vs complement for the rule i
--------------------------------------------
- ``draw_mosaics_rule_vs_comp_for_i``: Draws the mosaics for the full rule at index ``i`` and for restricted rules on a given ``plt.Axes``.
- ``make_mosaics_rule_vs_comp_for_i``: Makes the mosaics for the full rule at index ``i`` and for restricted rules on its features as a ``plt.Figure``.
- ``plot_mosaics_rule_vs_comp_for_i``: Plots the mosaics for the full rule at index ``i`` and for restricted rules on its features and show it to the user.

Mosaic of rule vs pop vs complement for the rule i
--------------------------------------------------
- ``draw_mosaic_rule_vs_pop_for_i``: Draws the mosaic plot comparing rule vs population on a given ``plt.Axes``.
- ``make_mosaic_rule_vs_pop_for_i``: Makes the mosaic plot comparing rule vs population as a ``plt.Figure``.
- ``plot_mosaic_rule_vs_pop_for_i``: Plots the mosaic plot comparing rule vs population and show it to the user.

Mosaics of rule vs pop vs complement
------------------------------------
- ``draw_mosaics_rule_vs_pop``: Draw the mosaics for all rules in the ruleset on a given ``plt.Axes``.
- ``make_mosaics_rule_vs_pop``: Makes the mosaics for all rules in the ruleset as a ``plt.Figure``.
- ``plot_mosaics_rule_vs_pop``: Plots the mosaics for all rules in the ruleset and show it to the user.

Complete plot
-------------
- ``make_all``: Makes all visualization figures and returns them as a list of tuples (name, figure).
- ``plot_all``: Plots all visualization figures and show them to the user.

Export to PDF
-------------
- ``make_pdf``: Exports a PDF of all the figures.

Export to ZIP
-------------
- ``make_zip``: Exports a ZIP of all the content related to the solver.

License
-------
Exclusive Use License - see `LICENSE <license.html>`_ for details.

----------------------------

"""

################################################################################
################################################################################
# Import some libraries

import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd

from typing import Optional, Union, Dict, Sequence, List

################################################################################
################################################################################
# Defining some global variables

# Width of the figures
FIG_WIDTH_IN = 12
# Dots per inch
DPI = 300
# InsightSolver blue
HEX_INSIGHTSOLVER = "#0530AD"

################################################################################
################################################################################
# Defining some utilities

def classify_variable_as_continuous_or_categorical(
    s: pd.Series,
    unique_ratio_threshold: float = 0.1,
    max_categories: int           = 20,
) -> str:
    """
    Classify a pandas Series as 'continuous' or 'categorical'.

    Heuristic
    ---------
    - If dtype is object/string/bool → categorical
    - If all values are equal → categorical
    - If all values are integers:
      - Few unique values (<= max_categories) → categorical
      - Low unique ratio (<= unique_ratio_threshold) → categorical
    - Otherwise → continuous

    Parameters
    ----------
    s : pd.Series
        Input series.
    unique_ratio_threshold : float, optional
        Threshold for ratio (#unique / #non-missing) to treat integers as categorical.
    max_categories : int, optional
        Absolute cap for number of unique categories to treat as categorical.

    Returns
    -------
    str
        "categorical" or "continuous"
    """

    # On vérifie le dtype
    if s.dtype in ["object", "string", "bool"]:
        return "categorical"

    # On élimine les valeurs manquantes
    s = s.dropna()

    # On regarde s'il est de longueur nulle
    if s.empty:
        return "categorical"

    # On regarde s'il est constant
    if s.nunique() == 1:
        return "categorical"

    # On regarde s'il ne contient que des entiers
    all_integers = all(s.astype(float).apply(float.is_integer))

    # Calculer le nombre de valeurs uniques
    unique_values = s.nunique()

    # Calculer la proportion de valeurs uniques sur la longueur de s
    unique_ratio = unique_values / len(s)

    if all_integers:
        if unique_values <= max_categories:
            return "categorical"
        if unique_ratio <= unique_ratio_threshold:
            return "categorical"

    return "continuous"

def compute_feature_label(
    solver,              # The solver
    feature_name: str,   # The name of the feature
    S: dict,             # The rule S
)->[str,str]:
    """
    This function computes the label of a feature in a rule S.

    Parameters
    ----------
    solver: InsightSolver
        The solver.
    feature_name: str
        The name of the feature.
    S: dict
        The rule S.

    Returns
    -------
    feature_label: str
        The label of the feature.
    feature_relationship: str
        The relationship of the feature to the constraints.
    """
    # Make sure feature_name is in S
    if feature_name not in S.keys():
        raise Exception(f"ERROR (compute_feature_label): feature_name={feature_name} is not in the keys of S.")
    # Look at the type of data
    if isinstance(S[feature_name],list):
        # If it's a continuous feature
        # Take the boundaries specified by the continuous feature
        if isinstance(S[feature_name][0],list):
            # If it's a continuous feature with NaNs
            [[rule_min,rule_max],rule_nan] = S[feature_name]
        else:
            # If it's a continuous feature without NaNS
            rule_min,rule_max = S[feature_name]
            rule_nan = None
        # Take the min and max according to the data
        min_value = solver.df[feature_name].min()
        max_value = solver.df[feature_name].max()
        # Depending on the rule and the data we compute the label
        if (rule_min==min_value)&(rule_max==max_value):
            # If both boundaries seem meaningless
            if rule_min==rule_max:
                # If only one value is legitimate
                feature_label = f"{feature_name} = {rule_max}"
                feature_relationship = '='
            else:
                feature_label = f"{feature_name} ∈ ℝ"
                feature_relationship = '∈'
        elif rule_min==min_value:
            # If only the lower boundary is meaningless
            feature_label = f"{feature_name} ≤ {rule_max}"
            feature_relationship = '≤'
        elif rule_max==max_value:
            # If only the upper boundary is meaningless
            feature_label = f"{feature_name} ≥ {rule_min}"
            feature_relationship = '≥'
        else:
            # If both boundaries are meaningful
            feature_label = f"{feature_name} ∈ {[rule_min,rule_max]}"
            feature_relationship = '∈'
        if rule_nan:
            feature_label += f", {rule_nan}"
    elif isinstance(S[feature_name],set):
        # If it's a binary or multiclass feature with at least one possible value
        feature_label = f"{feature_name} ∈ {S[feature_name]}"
        feature_relationship = '∈'
    else:
        # If it's a binary or multiclass feature with only one possible value
        feature_label = f"{feature_name} = {S[feature_name]}"
        feature_relationship = '='
    # Return the feature label and the feature relationship
    return feature_label,feature_relationship

def truncate_label(
    label,
    max_length = 30,
    asterisk   = False,
):
    """
    This function truncates a string if it exceeds a specified length, adding an ellipsis.

    Parameters
    ----------
    label: string
        the feature rule's modalities.
    max_length: int
        the maximum number of character accepted.
    asterisk: bool
        whether we want an asterisk to appear after the truncation.

    Returns
    -------
    truncated_label: str
        The truncated label.
        
    """
    if len(label) > max_length:
        truncated_label = label[:max_length-1] + '…'
        if asterisk:
            truncated_label += '*'
    else:
        truncated_label = label
    return truncated_label

def p_value_to_p_text(
    p_value,
    precision_p_values: str,
)->str:
    """
    This function converts the p-value to a string.

    Parameters
    ----------
    p_value: float or mpmath.mpf
        The p-value to convert.
    precision_p_values: str
        The precision of the p-values.

    Returns
    -------
    p_text: str
        The p_value formatted as a string.
    """
    import mpmath
    if precision_p_values=='float64':
        # If the precision is float64
        if abs(p_value) >= 0.001: # If the p_value is big
            p_text = f"{p_value:.4f}"  # normal decimals
        else:
            p_text = f"{p_value:.2e}"  # scientific notation
    elif precision_p_values=='mpmath':
        # If the precision is mpmath
        if abs(p_value) >= 0.001: # If the p_value is big
            p_text = mpmath.nstr(p_value, n=5, strip_zeros=True)
        else:
            # Scientific notation : 2 significant numbers
            p_text = mpmath.nstr(p_value, n=2, min_fixed=0, max_fixed=0)
    else:
        raise Exception(f"ERROR: precision_p_values='{precision_p_values}' is invalid. It must be either 'float64' or 'mpmath'.")
    # Return the result
    return p_text

def load_icon(
    icon_filename: str,
    assets_package: str  = "insightsolver.assets",
    subfolder: str       = "google_fonts_icons",
    size: tuple[int,int] = (80,80),
    fill_color: Union[str, tuple] = "white",
):
    """
    Load a PNG icon and return it as a PIL Image object with a specified size.

    Parameters
    ----------
    icon_filename: str
        The filename of the icon (e.g., 'icon.png').
    assets_package: str
        The Python package name where the assets are located (e.g., 'insightsolver.assets').
    subfolder: str
        The subfolder within the assets package. The function will look into a 'png' subdirectory of this folder.
    size: tuple(int, int)
        The target size (width, height) in pixels for the output PIL Image.
    fill_color: str or tuple
        The background color to use (e.g., "white", "#FFFFFF", (255, 255, 255)).

    Returns
    -------
    img : PIL.Image.Image
        The loaded image as a PIL Image object, in RGBA format.
    """

    from importlib.resources import files
    from PIL import Image, ImageOps

    # Locate the PNG file
    # We assume the structure is .../google_fonts_icons/png/icon.png
    png_file = files(assets_package) / subfolder / "png" / icon_filename
    
    with png_file.open("rb") as f:
        img = Image.open(f).convert("RGBA")
        
    # Resize to the requested size
    # We use LANCZOS for high-quality downsampling
    if img.size != size:
        img = img.resize(size, Image.Resampling.LANCZOS)
        
    # Apply fill_color
    if fill_color == "transparent":
        # Keep transparency
        pass
    else:
        # Normalize fill_color to RGBA tuple
        if isinstance(fill_color, tuple):
            if len(fill_color) == 3:
                # Add alpha channel
                fill_color_rgba = fill_color + (255,)
            else:
                fill_color_rgba = fill_color
        else:
            # It's a string color name or hex
            fill_color_rgba = fill_color
        
        # Create a solid background
        bg = Image.new("RGBA", size, fill_color_rgba)
        # Paste the icon on top (using its alpha channel as mask)
        bg.paste(img, (0, 0), mask=img)
        img = bg
    
    return img.convert("RGBA")

def wrap_text_with_word_boundary(
    text: str,                  # The original string to modify.
    max_line_length: int = 150, # The character threshold for insertion.
) -> str:
    """
    Wraps a text string into multiple lines by inserting line breaks 
    around a target character width, while preserving word boundaries 
    whenever possible.

    - If the next word would cause the line to exceed `max_line_length`,
      a line break is inserted *before* that word.
    - If a single word is longer than `max_line_length`, the word is split
      with a hyphen followed by a line break.

    Parameters
    ----------
    text : str
        The input text to wrap.
    max_line_length : int, optional
        The maximum allowed line length before wrapping occurs (default is 150).
                                           
    Returns
    -------
    str
        The wrapped string, with line breaks (and occasional hyphenation)
        inserted at appropriate positions.    
    """

    # If the text is not a string, convert it to a string
    if not isinstance(text, str):
        text = str(text)
    # If the text is empty, return an empty text
    if text=='':
        return ''
    # Take the list of words
    words = text.split()
    # Create a list of strings
    strings = []
    # The current line
    current_len = 0
    # Looping over the words
    for word in words:
        # Case 1: the word longer than a single line and needs to be chunked down
        while len(word) > max_line_length:
            # Take the first chunk
            chunk = word[:max_line_length - 1] + "-"
            # Append the first chunk
            strings.append(chunk + "\n    ")
            # Take the last part of the word (stripped from the first chunk)
            word = word[max_line_length - 1:]
            # Reset the line because we are on a new line
            current_len = 0
        # Case 2: normal situation
        if current_len == 0:
            # If we are at the start of the line
            # append the word at the start of the string
            strings.append(word)
            # We moved a bit to the right of the line
            current_len = len(word)
        elif current_len + 1 + len(word) <= max_line_length:
            # If the word is not too long
            # we append the word to the strings
            strings.append(" " + word)
            # We moved a bit to the right of the line
            current_len += 1 + len(word)
        else:
            # If the word is too long
            # Normal jump of line
            strings.append("\n    " + word)
            current_len = len(word)
    # Join the resulting strings
    string = " ".join(strings)
    # Return the resulting string
    return string

def save_figs_in_pdf(
    figs: list,
    pdf,
    do_padding: bool = True
):
    """
    Stack multiple figures vertically on a page and save to PDF.

    Parameters
    ----------
    figs : list of matplotlib.figure.Figure
        The figures to stack.
    pdf : PdfPages
        The PdfPages object to save to.
    do_padding: bool, default True
        If a padding should be present in the pdf.
    """
    import matplotlib.pyplot as plt
    from .visualization import FIG_WIDTH_IN, DPI
    dpi = DPI
    # Create a list of images
    imgs = []
    # Loop over the figures to convert them to images
    for fig in figs:
        fig.set_dpi(dpi)
        fig.canvas.draw()
        buf, (w, h) = fig.canvas.print_to_buffer()
        img = np.frombuffer(buf, dtype=np.uint8).reshape(h, w, 4)[:, :, :3]
        # Append the image in the list of images
        imgs.append(img)
        plt.close(fig)
    target_width_inch = FIG_WIDTH_IN
    target_width_px = int(target_width_inch * dpi)
    resized_imgs = []
    for img in imgs:
        scale = target_width_px / img.shape[1]
        new_h = int(img.shape[0] * scale)
        from PIL import Image
        img_pil = Image.fromarray(img, mode="RGB")
        img_resized = img_pil.resize((target_width_px, new_h), Image.LANCZOS)
        resized_imgs.append(np.array(img_resized))
    # Vertical concatenation of the figures
    combined = np.vstack(resized_imgs)
    # Create a single figure with all the images
    height_inch = combined.shape[0] / dpi
    fig_page, ax = plt.subplots(figsize=(target_width_inch, height_inch), dpi=dpi)
    ax.imshow(combined, extent=[0, target_width_inch, 0, height_inch])
    ax.set_xlim(0, target_width_inch)
    ax.set_ylim(0, height_inch)
    ax.axis("off")
    # Remove the padding
    if not do_padding:
        fig_page.subplots_adjust(left=0, right=1, top=1, bottom=0)
    # Save the figure of the page in the pdf
    pdf.savefig(fig_page)
    # Close the figure of the page
    plt.close(fig_page)

################################################################################
################################################################################
# Mutual information

def draw_mutual_information(
    ax: plt.Axes,
    s_mi: pd.Series,
    kind: str = 'barh',
) -> plt.Axes:
    """
    Draws the mutual information bar plot on the given axes.

    Parameters
    ----------
    ax : plt.Axes
        The axes to draw on.
    s_mi : pd.Series
        The mutual information series.
    kind : str
        Kind of plot ('bar' or 'barh').

    Returns
    -------
    ax : plt.Axes
        The axes with the plot.
    """
    # Determine the colors of the bars
    import matplotlib.colors as mcolors
    cmap = mcolors.LinearSegmentedColormap.from_list(
        "insightsolver_cmap",
        ["white", HEX_INSIGHTSOLVER]
    )

    # Normalize according to the values
    norm = mcolors.Normalize(
        vmin=0,
        vmax=s_mi.max()
    )

    # Color of each bar
    bar_colors = [cmap(norm(v)) for v in s_mi]

    # Draw the bar plot on the axes
    s_mi.plot(
        kind      = kind,
        edgecolor = 'black',
        color     = bar_colors,
        linewidth = 0.8, # Thinner border
        ax        = ax,
    )

    # Set the title and labels
    ax.set_title('Mutual Information between the features and the target variable')
    ax.set_xlabel('Mutual Information')
    ax.set_ylabel('Feature')

    # Rotate the x-axis labels if needed
    if kind == 'bar':
        ax.tick_params(axis='x', labelrotation=45)
        plt.setp(ax.get_xticklabels(), ha='right')
    
    # Add the values on top of the bars
    for idx, value in enumerate(s_mi):
        # Compute the position
        if kind=='bar':
            x  = idx
            y  = value + s_mi.max() * 0.01
            ha = 'center'
            va = 'bottom'
        elif kind=='barh':
            x  = value + s_mi.max() * 0.005
            y  = idx
            ha = 'left'
            va = 'center'
        # Add the value on top of the bar
        ax.text(
            x        = x, 
            y        = y,  # small offset
            s        = f"{value:.4f}", 
            ha       = ha, 
            va       = va, 
            fontsize = 8
        )
    
    # Return the axes object with the plot on it
    return ax

def make_mutual_information(
    solver,
    n_samples: Optional[int] = 1000,
    n_cols: Optional[int]    = 20,
    kind: str                = 'barh',
    fig_width: float         = FIG_WIDTH_IN,
) -> plt.Figure:
    """
    Creates a figure showing the mutual information.

    Parameters
    ----------
    solver : InsightSolver
        The solver object.
    n_samples : int
        Number of samples.
    n_cols : int
        Max number of columns.
    kind : str
        Kind of plot.
    fig_width : float
        Width of the figure.

    Returns
    -------
    fig : plt.Figure
        The created figure.
    """
    # Make sure the parameter kind is valid
    if kind not in ['bar','barh']:
        raise ValueError(f"ERROR (make_mutual_information): The parameter kind='{kind}' must be either 'bar' or 'barh'.")

    # Compute the mutual information Series
    s_mi = solver.compute_mutual_information(
        n_samples = n_samples,
    )

    # Keep only the top variables
    if n_cols and len(s_mi)>n_cols:
        s_mi = s_mi.head(n_cols)

    # For a horizontal barplot we must sort to have big values on top of the figure
    if kind=='barh':
        s_mi.sort_values(ascending=True,inplace=True)
    
    # Generate the figure
    fig, ax = plt.subplots(
        figsize = (fig_width, 6),
    )
    
    # Draw the mutual information on the axes
    draw_mutual_information(
        ax   = ax,
        s_mi = s_mi,
        kind = kind,
    )
    
    # Tight layout
    fig.tight_layout()
    
    # Return the figure
    return fig

def plot_mutual_information(
    solver,
    n_samples: Optional[int] = 1000,
    n_cols: Optional[int]    = 20,
    kind: str                = 'barh',
    fig_width: float         = FIG_WIDTH_IN,
) -> None:
    """
    Displays the mutual information plot.
    """
    fig = make_mutual_information(
        solver    = solver,
        n_samples = n_samples,
        n_cols    = n_cols,
        kind      = kind,
        fig_width = fig_width,
    )
    plt.show()

################################################################################
################################################################################
# Banner

def make_banner_img_for_i(
    solver,
    i: int,
    loss: float                = None,
    fig_width: float           = 12,   # inches
    dpi: int                   = 200,
    icon_size: tuple[int, int] = (80, 80),
):
    """
    Generate a dynamic InsightSolver banner composed of SVG icons and text.

    Parameters
    ----------
    solver : InsightSolver
        The solver containing the rules.
    i : int
        Index of the rule to display.
    loss : float, optional
        Optional loss value to display.
    fig_width : float
        Width of the banner (in inches).
    dpi : int
        DPI resolution (pixels per inch).
    icon_size : tuple
        Icon size in pixels (width, height).

    Returns
    -------
    PIL.Image
        The generated banner.
    """
    from PIL import Image, ImageDraw, ImageFont, ImageFilter
    from importlib.resources import files

    # --- Extract rule data ---
    rule_i = solver.i_to_rule(i=i)
    p_value           = rule_i["p_value"]
    purity            = rule_i["mu_rule"]
    lift              = rule_i["lift"]
    coverage_relative = rule_i["coverage"]
    coverage_absolute = rule_i["m"]
    cohen_d           = rule_i["shuffling_scores"]["p_value"]["cohen_d"]

    precision_p_values = solver.monitoring_metadata.get("precision_p_values", "float64")
    if precision_p_values == "mpmath":
        import mpmath

    p_text = p_value_to_p_text(
        p_value=p_value,
        precision_p_values=precision_p_values,
    )

    # --- Icon mapping ---
    icons_map = {
        "insight_id_text":        "network_intelligence.png",
        "p_text":                 "offline_bolt.png",
        "purity_text":            "timelapse.png",
        "lift_text":              "gondola_lift.png",
        "coverage_relative_text": "zoom_out_map.png",
        "coverage_absolute_text": "select_all.png",
        "cohen_d_text":           "shuffle.png",
        "loss_text":              "sell.png",
    }

    # --- Values to display ---
    values_all = [
        ("insight_id_text",        f"Insight #{i+1}"),
        ("p_text",                 p_text),
        ("purity_text",            f"{round(purity * 100, 2)} %"),
        ("lift_text",              f"{round(lift, 2)}"),
        ("coverage_relative_text", f"{round(coverage_relative * 100, 2)} %"),
        ("coverage_absolute_text", str(coverage_absolute)),
        ("cohen_d_text",           f"{cohen_d:.2f}"),
    ]
    if loss is not None:
        values_all.append(("loss_text", str(loss)))
        font_ratio = 0.38
    else:
        font_ratio =  0.45

    # --- Banner dimensions ---
    banner_width  = int(fig_width * dpi)
    banner_height = 120
    img_banner    = Image.new("RGBA", (banner_width, banner_height), "white")
    draw          = ImageDraw.Draw(img_banner)

    # --- Load Roboto font ---
    font_size           = int(icon_size[1] * font_ratio)
    roboto_regular_path = files("insightsolver.assets") / "google_fonts_icons" / "Roboto-Regular.ttf"
    roboto_bold_path    = files("insightsolver.assets") / "google_fonts_icons" / "Roboto-Bold.ttf"
    font_regular        = ImageFont.truetype(str(roboto_regular_path), size=font_size)
    font_bold           = ImageFont.truetype(str(roboto_bold_path), size=font_size)

    # --- Fixed horizontal layout ---
    n_blocks = len(values_all)
    margin = 20     # Margin around the cells, in pixels
    gap = margin*2  # Horizontal gap between cells, in pixels
    total_gap = gap * (n_blocks - 1)
    usable_width = banner_width - 2 * margin - total_gap
    space_per_block = usable_width / n_blocks
    x_positions = [int(margin + i * (space_per_block + gap)) for i in range(n_blocks)]

    # --- Vertical icon placement ---
    y_icon = (banner_height - icon_size[1]) // 2

    # --- Shadow parameters ---
    shadow_offset = 2            # Slight offset in x,y
    shadow_radius = 4            # Blur radius
    shadow_color = (0, 0, 0, 60) # Semi transparent black for the shadow

    # Colorisation du cohen_d
    if cohen_d>2:
        cohen_d_color = "#d4edda" # Light greed background
    elif cohen_d>0:
        cohen_d_color = "#fff3cd" # Light yellow background
    else:
        cohen_d_color = "#f8d7da" # Light red background

    # --- Draw icons and text ---
    for (key, text), x in zip(values_all, x_positions):

        # Define the bounding box of the block
        block_x0 = x
        block_x1 = int(x + space_per_block)
        pad      = 10  # Internal margin
        block_y0 = pad
        block_y1 = banner_height - pad

        # --- Draw shadow using Gaussian blur ---
        shadow = Image.new("RGBA", img_banner.size, (0, 0, 0, 0))
        shadow_draw = ImageDraw.Draw(shadow)

        # shadow rectangle coords (slightly offset)
        shadow_rect = [
            (block_x0 + shadow_offset, block_y0 + shadow_offset),
            (block_x1 + shadow_offset, block_y1 + shadow_offset),
        ]

        shadow_draw.rounded_rectangle(
            shadow_rect,
            radius = 12,
            fill   = shadow_color,
        )

        # Apply blur
        shadow = shadow.filter(
            ImageFilter.GaussianBlur(
                radius = shadow_radius,
            ),
        )

        # Paste shadow onto img_banner
        img_banner.alpha_composite(shadow)

        # --- Draw grey outline rectangle ---
        fill_color = cohen_d_color if key == "cohen_d_text" else (242, 242, 242)
        draw.rounded_rectangle(
            [(block_x0 + 2, block_y0), (block_x1 - 2, block_y1)],
            outline = (213, 213, 213),
            width   = 2,
            radius  = 12,
            fill    = fill_color,
        )

        # Draw icon
        icon = load_icon(
            icon_filename = icons_map[key],
            size          = icon_size,
            fill_color    = fill_color,
        )
        img_banner.paste(icon, (x + pad, y_icon), mask=icon)

        font = font_bold if key == "insight_id_text" else font_regular

        # --- Horizontal centering for text within the block ---
        block_text_start_x = x + icon_size[0]
        block_text_width   = block_x1 - block_text_start_x - pad
        text_width         = draw.textlength(text, font=font)
        x_text             = block_text_start_x + (block_text_width - text_width) // 2

        # --- Vertical centering using typographic metrics ---
        ascent, descent = font.getmetrics()
        text_height     = ascent + descent
        icon_center_y   = y_icon + icon_size[1] // 2
        y_text          = icon_center_y - text_height // 2

        # Draw text
        draw.text(
            (x_text, y_text),
            text,
            fill = "black",
            font = font,
        )
    
    return img_banner

def plot_banner_img_for_i(
    solver,
    i: int,
    loss: float                = None,
    fig_width: float           = 12,   # inches
    dpi: int                   = 200,
    icon_size: tuple[int, int] = (80, 80),
) -> None:
    """
    Displays the banner image of the statistics of the rule at index ``i``.

    Parameters
    ----------
    solver : InsightSolver
        The fitted solver.
    i : int
        The index of the rule to be displayed in the banner.
    loss : float
        An optional loss value to display in the banner.
    fig_width : float
        Width of the banner in inches.
    dpi : int
        DPI resolution (pixels per inch).
    icon_size : tuple[int, int]
        Icon size in pixels (width, height).
    """
    img = make_banner_img_for_i(
        solver    = solver,
        i         = i,
        loss      = loss,
        fig_width = fig_width,
        dpi       = dpi,
        icon_size = icon_size,
    )
    img.show()

def make_banner_fig_for_i(
    solver,
    i: int,
    loss: float                = None,
    fig_width: float           = 12,   # inches
    dpi: int                   = 200,
    icon_size: tuple[int, int] = (80, 80),
) -> plt.Figure:
    """
    This function generates a figure of the banner of the statistics of the rule at index ``i``.

    Parameters
    ----------
    solver: InsightSolver
        The fitted solver.
    i: int
        The index of the rule to be displayed in the banner.
    loss: float
        An optional loss value to display in the banner.
    fig_width: float
        Width of the figure in inches. Height is automatically adjusted.
    dpi: int
        Resolution (dots per inch) of the figure.
    icon_size: tuple[int, int]
        Size of the icons used in the banner image (width, height in pixels).

    Returns
    -------
    fig_banner : matplotlib.figure.Figure
        The Matplotlib Figure object containing the rule banner.
    """

    # Create the banner image
    img_banner = make_banner_img_for_i(
        solver    = solver,
        i         = i,
        loss      = loss,
        fig_width = fig_width,
        dpi       = dpi,
        icon_size = icon_size,
    )
    # Size in pixels of the banner image
    height_px = img_banner.height
    width_px  = img_banner.width
    # Take the ratio height/width
    ratio = height_px / width_px
    # Height of the banner in inches
    fig_height = fig_width * ratio
    # Create a figure for the banner
    fig_banner = plt.figure(
        figsize = (fig_width, fig_height),
        dpi     = dpi,
    )
    ax = fig_banner.add_subplot(111)
    ax.imshow(img_banner)
    ax.axis("off")
    # Return the figure of the banner
    return fig_banner

def plot_banner_fig_for_i(
    solver,
    i: int,
    loss: float                = None,
    fig_width: float           = 12,   # inches
    dpi: int                   = 200,
    icon_size: tuple[int, int] = (80, 80),
) -> None:
    """
    Displays the banner of the statistics of the rule at index ``i``.

    Parameters
    ----------
    solver : InsightSolver
        The fitted solver.
    i : int
        The index of the rule to be displayed in the banner.
    loss : float
        An optional loss value to display in the banner.
    fig_width : float
        Width of the figure in inches. Height is automatically adjusted.
    dpi : int
        Resolution (dots per inch) of the figure.
    icon_size : tuple[int, int]
        Size of the icons used in the banner image (width, height in pixels).
    """
    fig = make_banner_fig_for_i(
        solver    = solver,
        i         = i,
        loss      = loss,
        fig_width = fig_width,
        dpi       = dpi,
        icon_size = icon_size,
    )
    plt.show()

################################################################################
################################################################################
# Legend

def make_legend_img(
    do_plot_loss: bool         = True,
    fig_width: float           = 12,   # inches
    dpi: int                   = 200,
    icon_size: tuple[int, int] = (80, 80),
    language: str              = 'en',
    verbose: bool              = False,
):
    """
    Generate a legend that explains what the icons of the legend represent.

    Parameters
    ----------
    do_plot_loss : bool
        If we want to describe the symbol for the loss in the legend.
    fig_width : float
        Width of the legend (in inches).
    dpi : int
        DPI resolution (pixels per inch).
    icon_size : tuple
        Icon size in pixels (width, height).
    verbose: bool
        Verbosity.

    Returns
    -------
    PIL.Image
        The generated legend.
    """

    # Create a DataFrame of labels, icons and texts
    data = {
        "insight_id": (
            "network_intelligence.png",
            "Number of the insight, starting from 1.",
            "Numéro de l'insight, en commençant par 1.",
        ),
        "p_value": (
            "offline_bolt.png",
            "p-value.",
            "p-value.",
        ),
        "purity": (
            "timelapse.png",
            "Purity.",
            "Pureté.",
        ),
        "lift": (
            "gondola_lift.png",
            "Lift.",
            "Lift.",
        ),
        "coverage_relative": (
            "zoom_out_map.png",
            "Relative coverage.",
            "Couverture relative.",
        ),
        "coverage_absolute": (
            "select_all.png",
            "Absolute coverage.",
            "Couverture absolue.",
        ),
        "cohen_d": (
            "shuffle.png",
            "Shuffling score (Cohen's d).",
            "Score de permutations (Cohen's d).",
        ),
        "loss": (
            "sell.png",
            "Loss",
            "Coût",
        ),
    }
    columns = [
        'icon_filename',
        'en',
        'fr',
    ]
    df = pd.DataFrame.from_dict(
        data    = data,
        orient  = 'index',
        columns = columns,
    )
    df.index.name = 'label'
    # Handle the loss
    if not do_plot_loss:
        df.drop(index=['loss'],inplace=True)
    # Import libraries
    from PIL import Image, ImageDraw, ImageFont, ImageFilter
    from importlib.resources import files
    # Number of blocks, one for "Legend:" and one per row of df
    n_blocks = 1 + len(df)
    if verbose:
        print("n_blocks = ",n_blocks)
    # Legend height per block
    height_per_block = 120 # 120 pixels per block
    if verbose:
        print("height_per_block =",height_per_block)
    # Legend dimensions
    legend_width  = int(fig_width * dpi)
    legend_height = height_per_block*n_blocks
    if verbose:
        print("legend_width =",legend_width)
        print("legend_height =",legend_height)
    # Create the image
    img_legend = Image.new("RGBA", (legend_width, legend_height), "white")
    draw       = ImageDraw.Draw(img_legend)
    # Load font
    font_ratio = 0.5
    font_size  = int(icon_size[1] * font_ratio)
    font_path_regular  = files("insightsolver.assets") / "google_fonts_icons" / "Roboto-Regular.ttf"
    font_path_bold     = files("insightsolver.assets") / "google_fonts_icons" / "Roboto-Bold.ttf"
    font_regular       = ImageFont.truetype(str(font_path_regular), size=font_size)
    font_bold          = ImageFont.truetype(str(font_path_bold), size=font_size)
    if verbose:
        print("icon_size =",icon_size)
        print("font_size =",font_size)
    # Compute text height
    ascent, descent = font_regular.getmetrics()
    text_height     = ascent + descent
    if verbose:
        print("ascent =",ascent)
        print("descent =",descent)
        print("text_height =",text_height)    
    # Vertical layout
    margin          = 20          # Vertical margin around the blocks, in pixels
    gap             = margin*2    # Vertical gap between blocks, in pixels
    total_gap       = gap * (n_blocks - 1) # Total vertical gap
    usable_height   = legend_height - 2 * margin - total_gap # Usable vertical height
    usable_height_per_block = usable_height // n_blocks # Usable vertical height per block
    y_positions     = [int(margin + i * (usable_height_per_block + gap)) for i in range(n_blocks)] # Vertical positions of the blocks
    if verbose:
        print("margin =",margin)
        print("gap =",gap)
        print("total_gap =",total_gap)
        print("usable_height =",usable_height)
        print("usable_height_per_block =",usable_height_per_block)
        print("y_positions =",y_positions)
    # Add "Legend:" in bold in the first block
    x_text_legend = margin
    y_text_legend = y_positions[0] + text_height // 2
    if language=='fr':
        text_legend = "Légende :"
    else:
        text_legend = "Legend:"
    draw.text(
        xy   = (
            x_text_legend,
            y_text_legend,
        ),
        text = text_legend,
        fill = "black",
        font = font_bold,
    )
    if verbose:
        print("x_text_legend =",x_text_legend)
        print("y_text_legend =",y_text_legend)
    # Internal padding of the block
    padding = 0
    if verbose:
        print("padding =",padding)
    
    # Draw icons and text
    for i,label in enumerate(df.index):
        if verbose:
            print(f"\n{i} : {label}")
        # Take the icon and the text
        icon_filename = df.loc[label,'icon_filename']
        text = df.loc[label,language]
        # Position of the block
        x_block = margin
        y_block = y_positions[i+1]
        if verbose:
            print("x_block =",x_block)
            print("y_block =",y_block)
        # Horizontal icon placement
        x_icon = x_block + padding
        if verbose:
            print("x_icon =",x_icon)
        # Vertical icon placement
        y_icon = (int(y_block + usable_height_per_block) - icon_size[1])
        if verbose:
            print("y_icon =",y_icon)
        # Draw icon
        icon = load_icon(
            icon_filename = icon_filename,
            size          = icon_size,
            fill_color    = "white",
        )
        img_legend.paste(
            icon,
            (x_icon, y_icon),
            mask = icon,
        )
        # Position of the text within the block
        x_text = x_block + icon_size[0] + 20
        y_text  = y_block + text_height // 2 - 10
        if verbose:
            print("x_text =",x_text)
            print("y_text =",y_text)
        # Draw text
        draw.text(
            xy   = (
                x_text,
                y_text,
            ),
            text = text,
            fill = "black",
            font = font_regular,
        )
    # Return the image
    return img_legend

def plot_legend_img(
    do_plot_loss: bool         = True,
    fig_width: float           = 12,   # inches
    dpi: int                   = 200,
    icon_size: tuple[int, int] = (80, 80),
    language: str              = 'en',
    verbose: bool              = False,
) -> None:
    """
    Displays the legend image.

    Parameters
    ----------
    do_plot_loss : bool
        If True, describe the symbol for the loss in the legend.
    fig_width : float
        Width of the legend (in inches).
    dpi : int
        DPI resolution (pixels per inch).
    icon_size : tuple
        Icon size in pixels (width, height).
    language : str
        Language of the text labels ('fr' or 'en').
    verbose : bool
        If True, display verbose output.
    """
    img = make_legend_img(
        do_plot_loss=do_plot_loss,
        fig_width=fig_width,
        dpi=dpi,
        icon_size=icon_size,
        language=language,
        verbose=verbose,
    )
    img.show()

def make_legend_fig(
    do_plot_loss: bool         = False,
    fig_width: float           = 12,   # inches
    dpi: int                   = 200,
    icon_size: tuple[int, int] = (80, 80),
    language: str              = 'en',
    verbose: bool              = False,
) -> plt.Figure:
    """
    This function generates a figure of the legend which explains the meaning of the icons in the banner.
    
    Parameters
    ----------
    do_plot_loss: bool
        If True, describe the loss icon in the legend.
    fig_width: float
        The width of the figure to generate.
    dpi: int
        The dots per inch (resolution) for the figure.
    icon_size: tuple[int, int]
        The size (width, height) in pixels for the icons used within the legend image.
    language: str
        Language of the text labels in the figure legend ('fr' or 'en').
    verbose: bool
        If True, display verbose output during the legend image generation process.

    Returns
    -------
    fig_legend : matplotlib.figure.Figure
        The Matplotlib Figure object containing the legend image.
    """
    # Create the legend image
    img_legend = make_legend_img(
        do_plot_loss = do_plot_loss,
        fig_width    = fig_width,
        dpi          = dpi,
        icon_size    = icon_size,
        language     = language,
        verbose      = verbose,
    )
    # Size in pixels of the legend image
    legend_height_px = img_legend.height
    legend_width_px  = img_legend.width
    # Take the ratio height/width
    legend_ratio = legend_height_px / legend_width_px
    # Height of the legend in inches
    fig_height = fig_width * legend_ratio
    # Create a figure for the legend
    fig_legend = plt.figure(
        figsize = (fig_width, fig_height),
        dpi     = dpi,
    )
    ax_legend = fig_legend.add_subplot(111)
    ax_legend.imshow(img_legend)
    ax_legend.axis("off")
    # Return the figure of the legend
    return fig_legend

def plot_legend_fig(
    do_plot_loss: bool         = False,
    fig_width: float           = 12,   # inches
    dpi: int                   = 200,
    icon_size: tuple[int, int] = (80, 80),
    language: str              = 'en',
    verbose: bool              = False,
) -> None:
    """
    Displays the legend.

    Parameters
    ----------
    do_plot_loss: bool
        If True, describe the loss icon in the legend.
    fig_width: float
        The width of the figure to generate.
    dpi: int
        The dots per inch (resolution) for the figure.
    icon_size: tuple[int, int]
        The size (width, height) in pixels for the icons used within the legend image.
    language: str
        Language of the text labels in the figure legend ('fr' or 'en').
    verbose: bool
        If True, display verbose output during the legend image generation process.
    """
    fig = make_legend_fig(
        do_plot_loss = do_plot_loss,
        fig_width    = fig_width,
        dpi          = dpi,
        icon_size    = icon_size,
        language     = language,
        verbose      = verbose,
    )
    plt.show()

################################################################################
################################################################################
# Feature contributions

def draw_feature_contributions_for_i(
    ax: plt.Axes,
    df_feature_contributions_S: pd.DataFrame,
    language: str           = 'en',
    do_grid: bool           = True,
    do_title: bool          = False,
    i: Optional[int]        = None,
    rule_i: Optional[dict]  = None,
    precision_p_values: str = 'float64',
    bar_annotations: str    = 'p_value_ratio',
) -> plt.Axes:
    """
    Draws the feature contributions bar plot on the given axes.

    Parameters
    ----------
    ax : plt.Axes
        The axes to draw on.
    df_feature_contributions_S : pd.DataFrame
        The DataFrame containing feature contributions.
    language : str
        Language of the plot ('en' or 'fr').
    do_grid : bool
        If True, show the grid.
    do_title : bool
        If True, show the title.
    i : int, optional
        Index of the rule.
    rule_i : dict, optional
        The rule dictionary.
    precision_p_values : str
        Precision of p-values ('float64' or 'mpmath').
    bar_annotations : str
        Type of annotations on bars ('p_value_ratio', 'p_value_contribution', or None).

    Returns
    -------
    ax : plt.Axes
        The axes with the plot.
    """
    # Create the barplot
    sns.barplot(
        ax      = ax,
        data    = df_feature_contributions_S,
        x       = 'p_value_contribution',
        y       = 'feature_label',
        hue     = 'feature_label',
        palette = 'viridis',
        dodge   = False,
        legend  = False, # We do not show the legend
        zorder  = 3,     # So that the vertical lines are behind the horizontal bars
    )

    # Change the colors of the bars and their contours
    import matplotlib.colors as mcolors
    vals = df_feature_contributions_S['p_value_contribution'].values
    normalized_values = vals / vals.max()  # 0 → white, max → blue
    cmap = mcolors.LinearSegmentedColormap.from_list("white_to_blue", ["#FFFFFF", HEX_INSIGHTSOLVER])
    bar_colors = [cmap(v) for v in normalized_values]
    for bar, bar_color in zip(ax.patches, bar_colors):
        bar.set_facecolor(bar_color)
        bar.set_edgecolor('black')
        bar.set_linewidth(0.8)
    
    # Set the xlabel and the ylabel according to the language
    if language=='fr':
        ax.set_xlabel('Contribution de la variable (%)')
        ax.set_ylabel('Variable')
    elif language=='en':
        ax.set_xlabel('Feature Contribution (%)')
        ax.set_ylabel('Feature')
    # Set the xlim
    ax.set_xlim(0, 100)
    # Set the xticks
    ax.set_xticks(range(0, 101, 5))
    # Truncate the yticks labels
    locs, labels = plt.yticks() # # Get the current y-axis tick locations and labels
    truncated_labels = [truncate_label(label.get_text(), max_length=55) for label in labels] # Apply the truncation function to each label
    plt.yticks(locs, truncated_labels) # Set the new truncated labels and locations on the y-axis
    # Set the grid
    if do_grid:
        ax.grid(
            visible   = True,
            axis      = 'x',
            color     = 'gray',
            linestyle = '--',
            linewidth = 0.5,
            alpha     = 0.7,
            zorder    = 0,
        )
    # Set the title
    if do_title:
        if i==None:
            if language=='fr':
                title = "Contribution des variables"
            elif language=='en':
                title = "Contribution of the features"
            else:
                title = "Contribution of the features"
        else:
            if language=='fr':
                title  = f"Contribution de chaque variable à la puissance statistique de l'insight #{i+1}"
            elif language=='en':
                title  = f"Contribution of each variable to the statistical power of the insight #{i+1}"
            else:
                title  = f"Contribution of each variable to the statistical power of the insight #{i+1}"
            p_value    = rule_i['p_value']  # Take the p-value
            lift       = rule_i['lift']     # Take the lift
            coverage   = rule_i['coverage'] # Take the coverage
            if precision_p_values=='mpmath':
                import mpmath
                formatted_p_value = mpmath.nstr(p_value, 2, strip_zeros=False)
                title += f"\np-value : {formatted_p_value}, lift : {lift:.2f},  coverage : {coverage* 100:.2f}%"
            else:
                title += f"\np-value : {p_value:.2e}, lift : {lift:.2f},  coverage : {coverage* 100:.2f}%"
        ax.set_title(title,size=12)

    # Define a function that maps a RGB color to a level of luminosity
    def relative_luminance(rgb):
        # Ignore alpha if present
        r, g, b = rgb[:3]
        # Return the luminance (sRGB norm)
        return 0.2126*r + 0.7152*g + 0.0722*b
    
    # Add annotations
    if bar_annotations is not None:
        valid_bar_annotations = [
            'p_value_ratio',
            'p_value_contribution',
        ]
        if bar_annotations not in valid_bar_annotations:
            raise Exception(f"ERROR: valid_bar_annotations='{valid_bar_annotations}' is not a valid value. It must be either None or in {valid_bar_annotations}.")
        
        for y, (x, value, bar_color) in enumerate(zip(
                df_feature_contributions_S['p_value_contribution'],
                df_feature_contributions_S[bar_annotations],
                bar_colors, # Colors of the bars
        )):
            bar_width        = ax.transData.transform((x/100,       0))[0] - ax.transData.transform((0,     0))[0] # Width in pixels of the bar from the origin to x
            annotation_width = ax.transData.transform((x/100 + 0.1, 0))[0] - ax.transData.transform((x/100, 0))[0] # Width in pixels of the annotation to show (approximation)
            if bar_width > annotation_width:
                # If the annotation is larger than the bar, we put the annotation to the right of the tip of the bar
                ha    = 'right'
                # Handle the color of the annotation
                lum = relative_luminance(bar_color)
                if lum<0.5:
                    color = 'white'
                else:
                    color = 'black'
            else:
                # If the annotation is shorter than the bar, we put the annotation to the left of the tip of the bar
                ha    = 'left'
                # Handle the color of the annotation
                color = 'black'
            if bar_annotations=='p_value_ratio':
                if precision_p_values=='mpmath':
                    import mpmath
                    s = ' '+mpmath.nstr(value, 2, strip_zeros=False)+' '
                else:
                    s = f' {value:.2e} '
            elif bar_annotations=='p_value_contribution':
                s = f' {value:.2f} % '
            # Put the text
            ax.text(
                x        = x,
                y        = y,
                s        = s,
                color    = color,
                ha       = ha,
                va       = 'center',
                fontsize = 9,
            )
    return ax

def make_feature_contributions_for_i(
    solver,
    i: int,                        # Index of the rule to show
    a: float              = 0.5,   # Height per bar
    b: float              = 1,     # Height for the margins and other elements
    fig_width: float      = FIG_WIDTH_IN, # Width of the figure in inches
    language: str         = 'en',  # Language of the figure
    do_grid: bool         = True,  # If we want to show a vertical grid
    do_title: bool        = False, # If we want a title automatically generated
    do_banner: bool       = True,  # If we want to show the banner
    bar_annotations: str  = 'p_value_ratio', # Type of values to show at the end of the bars (can be 'p_value_ratio', 'p_value_contribution' or None)
    loss: Optional[float] = None,  # If we want to show a loss
) -> List[plt.Figure]:
    """
    Creates the feature contributions figures (banner, plot, details).

    Parameters
    ----------
    solver : InsightSolver
        The solver object.
    i : int
        Index of the rule to show.
    a : float
        Height per bar.
    b : float
        Height for the margins and other elements.
    fig_width : float
        Width of the figure in inches.
    language : str
        Language of the figure.
    do_grid : bool
        If True, show a vertical grid.
    do_title : bool
        If True, show a title automatically generated.
    do_banner : bool
        If True, show the banner.
    bar_annotations : str
        Type of values to show at the end of the bars.
    loss : float, optional
        If we want to show a loss.

    Returns
    -------
    figs : List[plt.Figure]
        A list of figures (banner, plot, details).
    """
    figs = []
    # Take the rule i
    rule_i = solver.i_to_rule(i=i)
    # Take the rule S
    S = rule_i['rule_S']
    # Take the contributions of the features
    df_feature_contributions_S = solver.i_to_feature_contributions_S(
        i                      = i,
        do_rename_cols         = False,
    )
    # Append the p_value_ratio
    d_p_value_ratios_S = rule_i['p_value_ratio_S']
    df_feature_contributions_S["p_value_ratio"] = df_feature_contributions_S.index.map(d_p_value_ratios_S)
    # Append the labels
    feature_names = df_feature_contributions_S.index.to_list() # List of features names of the rule S
    feature_labels = [] # List of feature labels
    for feature_name in feature_names:
        feature_label,_ = compute_feature_label(
            solver       = solver,
            feature_name = feature_name,
            S            = S,
        )
        feature_labels.append(feature_label)
    df_feature_contributions_S['feature_label'] = feature_labels
    # Make sure numbers are float (they can be 'mpmath')
    df_feature_contributions_S['p_value_contribution'] = df_feature_contributions_S['p_value_contribution'].astype(float)
    # Sort by p_value_contribution descending
    df_feature_contributions_S.sort_values(
        by        = 'p_value_contribution',
        ascending = False,
        inplace   = True,
    )
    # Take back the sorted feature labels
    feature_labels = df_feature_contributions_S['feature_label'].to_list()
    # Convert the p_value_contribution to percentages
    df_feature_contributions_S['p_value_contribution'] *= 100
    # Take the precision of the p-values
    if 'precision_p_values' in solver.monitoring_metadata.keys():
        precision_p_values = solver.monitoring_metadata['precision_p_values']
    else:
        precision_p_values = 'float64'
    if precision_p_values=='mpmath':
        import mpmath
    # Take the complexity of the rule
    complexity = len(S)
    # Take the dpi
    dpi = DPI
    # Create the banner as a separate figure
    if do_banner:
        fig_banner = make_banner_fig_for_i(
            solver    = solver,
            i         = i,
            loss      = loss,
            fig_width = fig_width,
            dpi       = dpi,
        )
        figs.append(fig_banner)
    # Create a bar plot as a separate figure
    fig_height_plot_inches = a * complexity + b
    fig_plot = plt.figure(
        figsize = (fig_width, fig_height_plot_inches),
        dpi     = dpi,
    )
    ax_plot = fig_plot.add_subplot(111)
    
    draw_feature_contributions_for_i(
        ax=ax_plot,
        df_feature_contributions_S=df_feature_contributions_S,
        language=language,
        do_grid=do_grid,
        do_title=do_title,
        i=i,
        rule_i=rule_i,
        precision_p_values=precision_p_values,
        bar_annotations=bar_annotations,
    )

    # Apply tight_layout to prevent truncation on the left and excess whitespace on the right
    fig_plot.tight_layout()

    figs.append(fig_plot)

    # Generating the feature labels
    if any(len(feature_label) > 55 for feature_label in feature_labels):
        # If any feature label is too long, we add this details section
        # Add a text box underneath the plot using figtext
        if language=='fr':
            details_title = 'Détails'
        elif language=='en':
            details_title = 'Details'
        else:
            details_title = 'Details'
        # Create a new list to store the modified labels
        wrapped_feature_labels = []
        for feature_label in feature_labels:
            feature_label = '• ' + feature_label
            wrapped_label = wrap_text_with_word_boundary(
                text            = feature_label,
                max_line_length = 200,
            )
            wrapped_feature_labels.append(wrapped_label)        
        # Join the title with the prepared labels, each starting on a new line
        # (the LaTeX style string is to specify that only details_title is shown in bold)
        feature_label_text = "\n".join(
            [r"$\bf{" + f"{details_title}:" + "}$"] + wrapped_feature_labels
        ) 
        # computing the number of rows the text contains
        n_rows = int(len(df_feature_contributions_S)) + int(feature_label_text.count('\n') + 1)
        fig_feature_label = plt.figure(figsize=(fig_width,  (0.05 * n_rows)))
        ax_feature_label = fig_feature_label.add_subplot(111)
        plt.figtext(
            x                 = 0.005,
            y                 = 0.005,
            s                 = feature_label_text, 
            wrap              = True,     # This helps for very long words that don't have commas
            fontsize          = 9, 
            verticalalignment = 'bottom', # Align text from the bottom edge of the figtext box
        )
        ax_feature_label.axis("off")
        figs.append(fig_feature_label)

    return figs

def plot_feature_contributions_for_i(
    solver,
    i: int,                        # Index of the rule to show
    a: float              = 0.5,   # Height per bar
    b: float              = 1,     # Height for the margins and other elements
    fig_width: float      = FIG_WIDTH_IN, # Width of the figure in inches
    language: str         = 'en',  # Language of the figure
    do_grid: bool         = True,  # If we want to show a vertical grid
    do_title: bool        = False, # If we want a title automatically generated
    do_banner: bool       = True,  # If we want to show the banner
    bar_annotations: str  = 'p_value_ratio', # Type of values to show at the end of the bars (can be 'p_value_ratio', 'p_value_contribution' or None)
    loss: Optional[float] = None,  # If we want to show a loss
) -> None:
    """
    Displays the feature contributions figures.

    Parameters
    ----------
    solver : InsightSolver
        The solver object.
    i : int
        Index of the rule to show.
    a : float
        Height per bar.
    b : float
        Height for the margins and other elements.
    fig_width : float
        Width of the figure in inches.
    language : str
        Language of the figure.
    do_grid : bool
        If True, show a vertical grid.
    do_title : bool
        If True, show a title automatically generated.
    do_banner : bool
        If True, show the banner.
    bar_annotations : str
        Type of values to show at the end of the bars.
    loss : float, optional
        If we want to show a loss.
    """
    figs = make_feature_contributions_for_i(
        solver          = solver,
        i               = i,
        a               = a,
        b               = b,
        fig_width       = fig_width,
        language        = language,
        do_grid         = do_grid,
        do_title        = do_title,
        do_banner       = do_banner,
        bar_annotations = bar_annotations,
        loss            = loss,
    )
    plt.show()

def plot_feature_contributions_for_all(
    solver,
    a:float             = 0.5,   # Height per bar
    b:float             = 1,     # Height for the margin and other elements
    fig_width:float     = FIG_WIDTH_IN, # Width of the figure in inches
    language:str        = 'en',  # Language of the figure
    do_grid:bool        = True,  # If we want to show a grid
    do_title:bool       = False, # If we want to show a title which is automatically generated
    do_banner:bool      = True,  # If we want to show the banner
    bar_annotations:str = 'p_value_ratio', # Type of values to show at the end of the bars (can be 'p_value_ratio', 'p_value_contribution' or None)
)->None:
    """
    This function generates a horizontal bar plot of the feature contributions for each rule found in a solver.

    Parameters
    ----------
    solver : InsightSolver
        The solver object.
    a : float
        Height per bar.
    b : float
        Height for the margin and other elements.
    fig_width : float
        Width of the figure in inches.
    language : str
        Language of the figure.
    do_grid : bool
        If True, show a grid.
    do_title : bool
        If True, show a title which is automatically generated.
    do_banner : bool
        If True, show the banner.
    bar_annotations : str
        Type of values to show at the end of the bars.
    """
    # Take the list of rule index available in the solver
    range_i = solver.get_range_i()
    # Looping over the index
    for i in range_i:
        # Show the contributions of the rule i
        plot_feature_contributions_for_i(
            solver          = solver,
            i               = i,
            a               = a,
            b               = b,
            fig_width       = fig_width,
            language        = language,
            do_grid         = do_grid,
            do_title        = do_title,
            do_banner       = do_banner,
            bar_annotations = bar_annotations,
        )

################################################################################
################################################################################
# Feature distribution

def draw_feature_distribution_for_feature(
    ax: plt.Axes,
    solver,
    df_filtered: pd.DataFrame,
    S: dict,
    feature_name: str,
    missing_value: bool          = False,
    language: str                = 'en',
    padding_y: int               = 5,
    do_plot_kde: bool            = False,
    do_plot_vertical_lines: bool = False,
    verbose: bool                = False,
) -> plt.Axes:
    """
    Draws the distribution of a feature on the given axes.

    Parameters
    ----------
    ax : plt.Axes
        The axes to draw on.
    solver : InsightSolver
        The solver object.
    df_filtered : pd.DataFrame
        The filtered DataFrame.
    S : dict
        The rule S.
    feature_name : str
        The name of the feature.
    missing_value : bool
        If True, plot the missing values.
    language : str
        Language of the plot ('en' or 'fr').
    padding_y : int
        Padding for the y-axis.
    do_plot_kde : bool
        If True, show the KDE plot.
    do_plot_vertical_lines : bool
        If True, show vertical lines for the rule boundaries.
    verbose : bool
        If True, print verbose output.

    Returns
    -------
    ax : plt.Axes
        The axes with the plot.
    """
    # Take the DataFrame that contains the data
    df = solver.df
    # Take the Pandas Series of the feature data
    s_unfiltered = df[feature_name]
    # Take the data without the missing values
    s_unfiltered_dropna = s_unfiltered.dropna()
    # Take the Pandas Series of the filtered feature data
    s_filtered   = df_filtered[feature_name]
    # Take the filtered data without the missing values
    s_filtered_dropna = s_filtered.dropna()
    # Take the btype of the feature
    if isinstance(S[feature_name],list):
        column_btype = 'continuous'
    else:
        column_btype = 'multiclass'
    # Determine if the variable is to be shown as a continuous (i.e. histogram) or as a categorical (i.e. bars)
    if column_btype in ['binary','multiclass']:
        categorical_or_continuous = 'categorical'
    elif column_btype=='continuous':
        categorical_or_continuous = classify_variable_as_continuous_or_categorical(
            s = s_unfiltered,
        )
    else:
        raise Exception(f"ERROR: feature_name='{feature_name}' has a btype='{column_btype}' which is illegal.")

    if verbose:
        print("column_btype =",column_btype)
        print("categorical_or_continuous =",categorical_or_continuous)

    # Look at the type of feature
    if categorical_or_continuous=='continuous':
        # If the feature is continuous

        # Calculate the inter quartile range (IQR)
        Q1 = s_unfiltered_dropna.quantile(0.25)
        Q3 = s_unfiltered_dropna.quantile(0.75)
        IQR = Q3 - Q1
        # Take the number of observations
        n_rows = len(s_unfiltered_dropna)
        # Look at the min and max values
        min_value = s_unfiltered_dropna.min()
        max_value = s_unfiltered_dropna.max()
        # Compute the widths of the bins
        if IQR>0:
            # Freedman-Diaconis formula
            step_bins = 2 * IQR * n_rows ** (-1 / 3)
        elif min_value<max_value:
            # Sturges formula
            step_bins = (max_value - min_value) / (1 + np.log2(n_rows))
        else:
            # 1 by default
            step_bins = 1
        # Calculate the number of bins based on the range and the step size
        num_bins = round((max_value - min_value) / step_bins)  # Nombre de bins correct
        if num_bins==0:
            num_bins = 1
        # Limit the total number of bins to avoid an over segmentation
        max_bins = 30
        num_bins = min(num_bins, max_bins)
        # Adjust the width of the bins to the limited number of bins
        if min_value<max_value:
            step_bins = (max_value - min_value) / num_bins
        else:
            step_bins = 1
        # Create the bin edges for the histograms
        bin_edges = np.arange(
            min_value,
            max_value + step_bins,
            step_bins,
        )

    if missing_value:
        
        # Create a Pandas Series of the missing values of the unfiltered data
        s_unfiltered_na = s_unfiltered[s_unfiltered.isna()].replace({np.nan: "nan"})
        # Create a Pandas Series of the missing values of the filtered data
        s_filtered_na   = s_filtered[s_filtered.isna()].replace({np.nan: "nan"})
        # First grey bar for the number of missing values in the original data
        sns.countplot(
            x     = s_unfiltered_na,
            color = 'grey',
            alpha = 0.6,
            ax    = ax,
        )
        # Superpose a second blue bar for the number of missing values in the filtered data
        sns.countplot(
            x     = s_filtered_na,
            color = HEX_INSIGHTSOLVER,
            alpha = 1.0,
            ax    = ax,
        )
        # Remove legend
        if ax.get_legend() is not None:
            ax.get_legend().remove()
        # Hide the title and xlabel and ylabel
        ax.set(
            title  = '',
            xlabel = '',
            ylabel = '',
        )

    else:
        # If we are not in the scenario of showing missing values

        # Look at the type of feature
        if categorical_or_continuous=='continuous':
            # First histplot for the distribution of the original variable
            sns.histplot(
                data  = s_unfiltered,
                kde   = do_plot_kde,
                bins  = bin_edges,
                color = 'grey',
                alpha = 0.6,
                ax    = ax,
            )
            # Second plot for the distribution of the filtered variable by the rule
            sns.histplot(
                data  = s_filtered,
                bins  = bin_edges,
                color = HEX_INSIGHTSOLVER,
                alpha = 1.0,
                ax    = ax,
            )
            # Rotate the bin edges
            ax.set_xticks(bin_edges)
            # Adjust the xlim
            ax.set_xlim(s_unfiltered.min() - step_bins, s_unfiltered.max()+step_bins)

        elif categorical_or_continuous=='categorical':
            # Take the Pandas Series to show in the countplot

            # If the data seems to be integers formatted as floats with useless .0, remove the .0 to improve the figure
            if pd.api.types.is_float_dtype(s_unfiltered_dropna) and np.all(s_unfiltered_dropna == s_unfiltered_dropna.astype(int)):
                s_unfiltered_dropna = s_unfiltered_dropna.astype(int).copy()
                s_filtered_dropna   = s_filtered_dropna.astype(int).copy()
            # Hangle the other modalities
            if feature_name in solver.other_modalities and len(solver.other_modalities[feature_name])>0:
                if verbose:
                    print("Other modalities found:",len(solver.other_modalities[feature_name]))
                other_mods = set(solver.other_modalities[feature_name])
                # Replace all modalities present in other_mods by "Other"
                s_unfiltered_dropna = s_unfiltered_dropna.apply(lambda x: "other" if x in other_mods else x)
                s_filtered_dropna   = s_filtered_dropna.apply(lambda x: "other" if x in other_mods else x)
            # Take the non numerical columns
            non_num_cols = df.select_dtypes(exclude='number').columns
            # If the feature is a non numerical column
            if feature_name in non_num_cols:
                # Ensure we only get unique values from the original data
                unique_categories = s_unfiltered_dropna.astype(str).unique() # Convert to string for consistent sorting
                sorted_categories = sorted(unique_categories)
            # First countplot for the distribution of the original variable
            sns.countplot(
                x     = s_unfiltered_dropna,
                color = 'grey',
                alpha = 0.6,
                label = "Unfiltered",
                order = sorted_categories if feature_name in non_num_cols else None, # Apply alphabetical order
                ax    = ax,
            )
            # Second plot for the distribution of the filtered variable by the rule
            sns.countplot(
                x     = s_filtered_dropna,
                color = HEX_INSIGHTSOLVER,
                alpha = 1.0,
                label = "Filtered",
                order = sorted_categories if feature_name in non_num_cols else None, # Apply alphabetical order
                ax    = ax,
            )
        
        if do_plot_vertical_lines:
            # Take the boundaries specified by the continuous feature
            if isinstance(S[feature_name],list):
                # Generate the feature label and the feature relationship
                _,feature_relationship = compute_feature_label(
                    solver       = solver,
                    feature_name = feature_name,
                    S            = S,
                )
                # Take the rule
                if isinstance(S[feature_name][0],list):
                    # If it's a continuous feature with NaNs
                    [[rule_min,rule_max],rule_nan] = S[feature_name]
                else:
                    # If it's a continuous feature without NaNS
                    rule_min,rule_max = S[feature_name]
                # Add a vertical line
                if feature_relationship=='≥':
                    # Add a vertical line at the lower boundary
                    ax.axvline(rule_min, color=HEX_INSIGHTSOLVER, linestyle='--', label=feature_name+' min')
                elif feature_relationship=='≤':
                    # Add a vertical line at the upper boundary
                    ax.axvline(rule_max, color=HEX_INSIGHTSOLVER, linestyle='--', label=feature_name+' max')
                elif feature_relationship=='∈':
                    # Add vertical lines at both boundaries
                    ax.axvline(rule_min, color=HEX_INSIGHTSOLVER, linestyle='--', label=feature_name+' min')
                    ax.axvline(rule_max, color=HEX_INSIGHTSOLVER, linestyle='--', label=feature_name+' max')
                   
        # Generate the title
        if language=='fr':
            title = f"Distribution de la variable: {feature_name}"
        elif language=='en':
            title = f"Distribution Plot for {feature_name}"
        else:
            title = f"Distribution Plot for {feature_name}"
        ax.set_title(title)
        # Generate the xlabel
        ax.set_xlabel(feature_name)

        # Add custom legend
        import matplotlib.patches as mpatches
        grey_patch = mpatches.Patch(
            color = "grey",
            alpha = 0.6,
            label = "Hors de la règle" if language == 'fr' else "Outside the rule",
        )
        blue_patch = mpatches.Patch(
            color = HEX_INSIGHTSOLVER,
            alpha = 1.0,
            label = "Dans la règle" if language == 'fr' else "Inside the rule",
        )
        ax.legend(handles=[grey_patch, blue_patch])

        # Get the current x-axis tick locations and labels
        locs, labels = ax.get_xticks(), ax.get_xticklabels()
        # Apply the truncation function to each label
        truncated_labels = [truncate_label(label.get_text()) for label in labels]
        # Set the xticks positions
        ax.set_xticks(locs)
        # Rotate x-axis tick labels diagonally
        ax.set_xticklabels(truncated_labels, rotation=30, ha="right")

    # Adjust the ylim so that the ylim is the same for the left and the right picture
    if categorical_or_continuous=='continuous':
        # Count the number of points per bin
        counts, _ = np.histogram(
            a    = s_unfiltered,
            bins = bin_edges,
        )
        # Take the maximum number of point found in a bin
        max_count_left = counts.max()
    elif categorical_or_continuous=='categorical':
        # If the feature is categorical
        max_count_left = s_unfiltered.value_counts().iloc[0]
    # Look at if there is any missing value in the original data    
    if s_unfiltered.isna().any():
        # Take the number of missing values
        max_count_right = s_unfiltered.isna().sum()
        # Update the maximum count
        max_count = max(max_count_left, max_count_right)
    else:
        max_count = max_count_left
    # Adjust y-lim
    ax.set_ylim(
        0,
        max_count + padding_y,
    )
    return ax

def make_feature_distribution_for_feature(
    solver,
    df_filtered: pd.DataFrame,
    S: dict,
    feature_name: str,
    missing_value: bool = False,
    language: str = 'en',
    padding_y: int = 5,
    do_plot_kde: bool = False,
    do_plot_vertical_lines: bool = False,
    fig_width: float = FIG_WIDTH_IN,
    verbose: bool = False,
) -> plt.Figure:
    """
    Creates a figure showing the distribution of a feature.

    Parameters
    ----------
    solver : InsightSolver
        The solver object.
    df_filtered : pd.DataFrame
        The filtered DataFrame.
    S : dict
        The rule S.
    feature_name : str
        The name of the feature.
    missing_value : bool
        If True, plot the missing values.
    language : str
        Language of the plot ('en' or 'fr').
    padding_y : int
        Padding for the y-axis.
    do_plot_kde : bool
        If True, show the KDE plot.
    do_plot_vertical_lines : bool
        If True, show vertical lines for the rule boundaries.
    fig_width : float
        Width of the figure.
    verbose : bool
        If True, print verbose output.

    Returns
    -------
    fig : plt.Figure
        The created figure.
    """
    # Determine if a new figure needs to be created
    if missing_value:
        fig, ax = plt.subplots(
            figsize = ((1/6)*fig_width, 4),
        )
    else:
        fig, ax = plt.subplots(
            figsize = (5/6*fig_width, 4),
        )
    
    draw_feature_distribution_for_feature(
        ax                     = ax,
        solver                 = solver,
        df_filtered            = df_filtered,
        S                      = S,
        feature_name           = feature_name,
        missing_value          = missing_value,
        language               = language,
        padding_y              = padding_y,
        do_plot_kde            = do_plot_kde,
        do_plot_vertical_lines = do_plot_vertical_lines,
        verbose                = verbose,
    )
    
    # Tight layout
    fig.tight_layout()
    return fig

def plot_feature_distribution_for_feature(
    solver,
    df_filtered: pd.DataFrame,
    S: dict,
    feature_name: str,
    missing_value: bool          = False,
    language: str                = 'en',
    padding_y: int               = 5,
    do_plot_kde: bool            = False,
    do_plot_vertical_lines: bool = False,
    fig_width: float             = FIG_WIDTH_IN,
    verbose: bool                = False,
) -> None:
    """
    Displays the distribution of a feature.

    Parameters
    ----------
    solver : InsightSolver
        The solver object.
    df_filtered : pd.DataFrame
        The filtered DataFrame.
    S : dict
        The rule S.
    feature_name : str
        The name of the feature.
    missing_value : bool
        If True, plot the missing values.
    language : str
        Language of the plot ('en' or 'fr').
    padding_y : int
        Padding for the y-axis.
    do_plot_kde : bool
        If True, show the KDE plot.
    do_plot_vertical_lines : bool
        If True, show vertical lines for the rule boundaries.
    fig_width : float
        Width of the figure.
    verbose : bool
        If True, print verbose output.
    """
    fig = make_feature_distribution_for_feature(
        solver                 = solver,
        df_filtered            = df_filtered,
        S                      = S,
        feature_name           = feature_name,
        missing_value          = missing_value,
        language               = language,
        padding_y              = padding_y,
        do_plot_kde            = do_plot_kde,
        do_plot_vertical_lines = do_plot_vertical_lines,
        fig_width              = fig_width,
        verbose                = verbose,
    )
    plt.show()

def draw_feature_distributions_for_S(
    axes_list: List[plt.Axes],
    solver,
    S: dict,
    language: str                = 'en',
    padding_y: int               = 5,
    do_plot_kde: bool            = False,
    do_plot_vertical_lines: bool = False,
) -> List[plt.Axes]:
    """
    Draws the distributions of all features in rule S on the given list of axes.

    Parameters
    ----------
    axes_list : List[plt.Axes]
        List of axes to draw on (one or two axes per feature depending on missing values).
    solver : InsightSolver
        The solver object.
    S : dict
        The rule S.
    language : str
        Language of the plot ('en' or 'fr').
    padding_y : int
        Padding for the y-axis.
    do_plot_kde : bool
        If True, show the KDE plot.
    do_plot_vertical_lines : bool
        If True, show vertical lines for the rule boundaries.

    Returns
    -------
    axes_list : List[plt.Axes]
        The list of axes with the plots.
    """
    # Take the DataFrame that contains the data
    df = solver.df
    # Filter the data to the points that are in the rule S
    df_filtered = solver.S_to_df_filtered(S=S)
    
    # Track current axes index
    ax_idx = 0
    
    # Loop over the features in the rule S
    for feature_name in S.keys():
        # Look at if the data of the feature contains any missing value
        if solver.df[feature_name].isna().any():
            # If the feature contains any missing value, use two axes
            # Plot the graph for the present values to the left
            draw_feature_distribution_for_feature(
                ax                     = axes_list[ax_idx],
                solver                 = solver,
                df_filtered            = df_filtered,
                S                      = S,
                feature_name           = feature_name,
                missing_value          = False,
                language               = language,
                padding_y              = padding_y,
                do_plot_kde            = do_plot_kde,
                do_plot_vertical_lines = do_plot_vertical_lines,
            )
            # Plot the graph for the missing values to the right
            draw_feature_distribution_for_feature(
                ax                     = axes_list[ax_idx + 1],
                solver                 = solver,
                df_filtered            = df_filtered,
                S                      = S,
                feature_name           = feature_name,
                missing_value          = True,
                language               = language,
                padding_y              = padding_y,
                do_plot_kde            = do_plot_kde,
                do_plot_vertical_lines = do_plot_vertical_lines,
            )
            ax_idx += 2
        else:
            # If the feature does not contain any missing value, use one axis
            draw_feature_distribution_for_feature(
                ax                     = axes_list[ax_idx],
                solver                 = solver,
                df_filtered            = df_filtered,
                S                      = S,
                feature_name           = feature_name,
                missing_value          = False,
                language               = language,
                padding_y              = padding_y,
                do_plot_kde            = do_plot_kde,
                do_plot_vertical_lines = do_plot_vertical_lines,
            )
            ax_idx += 1
    
    return axes_list

def make_feature_distributions_for_S(
    solver,
    S: dict,
    language: str                = 'en',
    padding_y: int               = 5,
    do_plot_kde: bool            = False,
    do_plot_vertical_lines: bool = False,
    fig_width: float             = FIG_WIDTH_IN,
) -> List[plt.Figure]:
    """
    Creates figures showing the distributions of all features in rule S.

    Parameters
    ----------
    solver : InsightSolver
        The solver object.
    S : dict
        The rule S.
    language : str
        Language of the plot ('en' or 'fr').
    padding_y : int
        Padding for the y-axis.
    do_plot_kde : bool
        If True, show the KDE plot.
    do_plot_vertical_lines : bool
        If True, show vertical lines for the rule boundaries.
    fig_width : float
        Width of the figure in inches.

    Returns
    -------
    figs : List[plt.Figure]
        A list of figures, one per feature.
    """
    # Take the DataFrame that contains the data
    df = solver.df
    # Filter the data to the points that are in the rule S
    df_filtered = solver.S_to_df_filtered(S=S)
    
    figs = []
    
    # Loop over the features in the rule S
    for feature_name in S.keys():
        # One figure will be created per feature name
        # Look at if the data of the feature contains any missing value
        if solver.df[feature_name].isna().any():
            # If the feature contains any missing value
            # Create two graphs (one for the present values and one for the missing values)
            fig, axes = plt.subplots(
                figsize     = (fig_width, 4),
                nrows       = 1,
                ncols       = 2,
                gridspec_kw = {
                    'width_ratios': [15, 1],
                },
            )
            # Plot the graph for the present values to the left
            draw_feature_distribution_for_feature(
                ax                     = axes[0], # Left figure
                solver                 = solver,
                df_filtered            = df_filtered,
                S                      = S,
                feature_name           = feature_name,
                missing_value          = False,   # Plot for the present values
                language               = language,
                padding_y              = padding_y,
                do_plot_kde            = do_plot_kde,
                do_plot_vertical_lines = do_plot_vertical_lines,
            )
            # Plot the graph for the missing values to the right
            draw_feature_distribution_for_feature(
                ax                     = axes[1], # Right figure
                solver                 = solver,
                df_filtered            = df_filtered,
                S                      = S,
                feature_name           = feature_name,
                missing_value          = True,    # Plot for the missing values
                language               = language,
                padding_y              = padding_y,
                do_plot_kde            = do_plot_kde,
                do_plot_vertical_lines = do_plot_vertical_lines,
            )
        else:
            # If the feature does not contain any missing value
            # Create a single graph for the present values
            fig, ax = plt.subplots(
                figsize = (fig_width, 4),
            )
            # Plot the graph for the present values
            draw_feature_distribution_for_feature(
                ax                     = ax,
                solver                 = solver,
                df_filtered            = df_filtered,
                S                      = S,
                feature_name           = feature_name,
                missing_value          = False, # Plot for the present values
                language               = language,
                padding_y              = padding_y,
                do_plot_kde            = do_plot_kde,
                do_plot_vertical_lines = do_plot_vertical_lines,
            )
        # Tight layout
        fig.tight_layout()
        # Append to list
        figs.append(fig)
    
    return figs

def plot_feature_distributions_for_S(
    solver,
    S: dict,
    language: str                = 'en',
    padding_y: int               = 5,
    do_plot_kde: bool            = False,
    do_plot_vertical_lines: bool = False,
    fig_width: float             = FIG_WIDTH_IN, # Width of the figure in inches
)->None:
    """
    This function generates bar plots of the distributions of the points in the specified rule S.

    Parameters
    ----------
    solver : InsightSolver
        The solver object.
    S : dict
        The rule S.
    language : str
        Language of the plot ('en' or 'fr').
    padding_y : int
        Padding for the y-axis.
    do_plot_kde : bool
        If True, show the KDE plot.
    do_plot_vertical_lines : bool
        If True, show vertical lines for the rule boundaries.
    fig_width : float
        Width of the figure in inches.
    """
    figs = make_feature_distributions_for_S(
        solver                 = solver,
        S                      = S,
        language               = language,
        padding_y              = padding_y,
        do_plot_kde            = do_plot_kde,
        do_plot_vertical_lines = do_plot_vertical_lines,
        fig_width              = fig_width,
    )
    
    # Show all figures
    for fig in figs:
        plt.show()

################################################################################
################################################################################
# Mosaic of rule vs complement for a feature for the rule i

def draw_mosaic_rule_vs_comp_for_feature_for_i(
    ax: plt.Axes,
    solver,
    i: int,
    feature_name: Optional[str] = None,
    verbose: bool               = False,
) -> plt.Axes:
    """
    Draws the mosaic plot for the rule i on the given axes.

    Parameters
    ----------
    ax : plt.Axes
        The axes to draw on.
    solver : InsightSolver
        The solver object.
    i : int
        Index of the rule.
    feature_name : str, optional
        Name of the feature to filter by.
    verbose: bool
        Verbosity

    Returns
    -------
    ax : plt.Axes
        The axes with the plot.
    """
    if verbose:
        print("\ndraw_mosaic_rule_vs_comp_for_feature_for_i :")
        print("i =",i)
        print("feature_name =",feature_name)
    # Take the rule S at position i
    S = solver.i_to_S(i=i)
    if verbose:
        print("S =",S)
    # Take the target_name
    target_name = solver.target_name
    # Take some rule statistics
    if feature_name is None:
        # Take the rule at position i
        rule_i = solver.i_to_rule(i=i)
        # Take some global statistics
        M   = solver.M
        M0  = solver.M0
        M1  = solver.M1
        # Take some rule statistics
        m   = rule_i['m']
        m0  = rule_i['m0']
        m1  = rule_i['m1']
        # Take some complement statistics
        mc  = M-m
        m0c = M0-m0
        m1c = M1-m1
    else:
        # Create a subrule
        S_feature = {feature_name:S[feature_name]}
        if verbose:
            print("S_feature =",S_feature)
        # Take the index of the points in the subrule
        index_points_in_rule = solver.S_to_index_points_in_rule(S=S_feature)
        if verbose:
            print("len(index_points_in_rule) =",len(index_points_in_rule))
            print(index_points_in_rule)
        # Take the target variable as a binary Series
        s_target = solver.convert_target_to_binary()
        # Restrict this Series to the points inside the subrule
        s_rule   = s_target.loc[index_points_in_rule]
        # Take the global statistics
        M  = len(s_target)
        M1 = s_target.sum()
        M0 = M-M1
        # Take some subrule statistics
        m  = len(s_rule)
        m1 = s_rule.sum()
        m0 = m-m1
        # Take some statistics of the complement of the subrule
        mc  = M-m
        m0c = M0-m0
        m1c = M1-m1
    if verbose:
        print("m   =",m)
        print("m0  =",m0)
        print("m1  =",m1)
        print("mc  =",mc)
        print("m0c =",m0c)
        print("m1c =",m1c)

    # Coverage
    coverage_rule = m/M if M>0 else 0
    coverage_comp = 1-coverage_rule
    # Purities
    mu1_pop  = M1/M if M>0 else 0
    mu0_rule = m0/m if m>0 else 0
    mu1_rule = m1/m if m>0 else 0
    mu0_comp = m0c/mc if mc>0 else 0
    mu1_comp = m1c/mc if mc>0 else 0
    # Create a pandas Series with a MultiIndex
    data = pd.Series(
        data  = [m1,m0,m1c,m0c],
        index = pd.MultiIndex.from_product([["Rule", "Complement"], ['1', '0']]),
    )
    # Define a coloring function
    def color_func(key):
        """
        Returns a dictionary of colors based on the key tuple.
        """
        # Define colors for each combination
        if key == ("Rule", '1'):
            # Inside the rule, class 1
            return {'color': HEX_INSIGHTSOLVER}
        elif key == ("Rule", '0'):
            # Inside the rule, class 0
            return {'color': 'grey'}
        elif key == ("Complement", '1'):
            # Outsite the rule, class 1
            return {'color': HEX_INSIGHTSOLVER, 'alpha':0.5}
        elif key == ("Complement", '0'):
            # Outside the rule, class 0
            return {'color': 'grey', 'alpha':0.5}
        else:
            # Default color
            return {}
    # Custom labelizer to show nothing
    def empty_labelizer(key):
        return ""
    # Create the plot with your existing parameters
    from statsmodels.graphics.mosaicplot import mosaic
    mosaic(
        data       = data,
        ax         = ax,
        properties = color_func,
        labelizer  = empty_labelizer,
        gap        = 0.02,
        title      = "",
        statistic  = False,
        axes_label = True,
    )
    # Edit the mosaic plot
    import matplotlib.ticker as mticker
    # Edit the xlabel and ylabel
    ax.set_xlabel("Coverage (%)", fontsize=12)
    ax.set_ylabel("Purity (%)", fontsize=12)
    # Edit the xlim and ylim
    ax.set_xlim(ax.get_xlim())
    ax.set_ylim(ax.get_xlim())
    # Edit the xticks and yticks
    ax.set_xticks(np.linspace(0, 1, 6)) # Set ticks at 0%, 20%, 40%, 60%, 80%, 100%
    ax.set_yticks(np.linspace(0, 1, 6)) # Set ticks at 0%, 20%, 40%, 60%, 80%, 100%
    # Format the ticks as percentages
    ax.xaxis.set_major_formatter(mticker.PercentFormatter(xmax=1.0))
    ax.yaxis.set_major_formatter(mticker.PercentFormatter(xmax=1.0))
    # Manually set x-axis tick locations and labels
    ticker_feature_location_in = float(coverage_rule / 2)
    ticker_feature_location_out = float((1-coverage_rule) / 2) + (ticker_feature_location_in*2)
    x_tick_locations = [ticker_feature_location_in, ticker_feature_location_out]
    x_tick_labels = ["Rule", "Complement"]
    ax_top = ax.twiny()
    ax_top.set_xticks(x_tick_locations)
    ax_top.set_xticklabels(x_tick_labels)
    # Title of the figure
    if not feature_name:
        title = f'Insight #{i + 1}'
    else:
        # Take the feature label
        feature_label, _ = compute_feature_label(
            solver       = solver,       # The solver
            feature_name = feature_name, # The name of the feature
            S            = S,            # The rule S
        )
        # Truncate the feature label
        feature_label = truncate_label(
            label      = feature_label,
            max_length = 50,
        )
        # The title is the feature_label
        title = feature_label
    ax_top.set_xlabel(
        title,
        fontsize   = 12,
        fontweight = 'bold',
    )
    #alpha = 0
    alpha = 0.2
    #alpha = 0.35
    backgroundcolor = (1,1,1,alpha)
    fontsize = 9
    if mu1_rule != 0:
        ax.text(
            coverage_rule/2,
            mu1_rule+0.02,
            f"{mu1_rule:.1%}",
            fontsize = fontsize,
            ha       = 'center',
            va       = 'center',
            backgroundcolor = backgroundcolor,
        )
    if mu1_comp != 0:
        ax.text(
            coverage_rule+(coverage_comp/2),
            mu1_comp+0.02,
            f"{mu1_comp:.1%}",
            fontsize = fontsize,
            ha       = 'center',
            va       = 'center',
            backgroundcolor = backgroundcolor,
        )
    # Add a dashed line for the purity of the population
    ax.axhline(
        y         = mu1_pop,
        linewidth = 1,
        color     = 'r',
        linestyle = ":",
    )
    # Add a text over the dashed line
    ax.text(
        x        = 0.5,
        y        = mu1_pop+0.01,
        s        = f"{mu1_pop:.1%}",
        fontsize = fontsize,
        color    = 'r',
        ha       = "center",
        backgroundcolor = backgroundcolor,
    )
    return ax

def make_mosaic_rule_vs_comp_for_feature_for_i(
    solver,
    i: int,
    feature_name: Optional[str] = None,
) -> plt.Figure:
    """
    Creates a figure showing the mosaic plot for the rule i.

    Parameters
    ----------
    solver : InsightSolver
        The solver object.
    i : int
        Index of the rule.
    feature_name : str, optional
        Name of the feature to filter by.

    Returns
    -------
    fig : plt.Figure
        The created figure.
    """
    # Make sure the solver if fitted
    if not solver._is_fitted:
        return None
    # Make sure i is valid
    if i not in range(len(solver)):
        raise Exception(f"ERROR (make_mosaic_rule_vs_comp_for_feature_for_i): i={i} is not valid.")
    
    fig, ax = plt.subplots(figsize=(4, 4))
    
    draw_mosaic_rule_vs_comp_for_feature_for_i(
        ax           = ax,
        solver       = solver,
        i            = i,
        feature_name = feature_name,
    )
    
    # Only tight_layout if showing an individual plot
    fig.tight_layout()
    return fig

def plot_mosaic_rule_vs_comp_for_feature_for_i(
    solver,
    i: int,
    feature_name: Optional[str] = None,
) -> None:
    """
    Displays the mosaic plot for the rule i.

    Parameters
    ----------
    solver : InsightSolver
        The solver object.
    i : int
        Index of the rule.
    feature_name : str, optional
        Name of the feature to filter by.
    """
    fig = make_mosaic_rule_vs_comp_for_feature_for_i(
        solver       = solver,
        i            = i,
        feature_name = feature_name,
    )
    if fig:
        plt.show()

################################################################################
################################################################################
# Mosaics of rule vs complement for the rule i

def draw_mosaics_rule_vs_comp_for_i(
    axes: list[plt.Axes],
    solver,
    i: int,
    ncols: int = 3,
) -> list[plt.Axes]:
    """
    Draws mosaics of the rule vs complement for the whole rule and each feature.

    Parameters
    ----------
    axes : list of plt.Axes
        Axes where to draw the plots.
    solver : InsightSolver
        The solver object.
    i : int
        Index of the rule.
    ncols : int
        Number of columns in the subplot grid.

    Returns
    -------
    axes : list of plt.Axes
        The axes with plots drawn.
    """
    # Feature names sorted by contribution
    feature_names = solver.i_to_feature_names(
        i       = i,
        do_sort = True,
    )
    n_features = len(feature_names)

    # Draw whole rule on the first axes
    draw_mosaic_rule_vs_comp_for_feature_for_i(
        ax           = axes[0],
        solver       = solver,
        i            = i,
        feature_name = None,
    )

    # Draw mosaics for each feature
    for k, feature_name in enumerate(feature_names):
        draw_mosaic_rule_vs_comp_for_feature_for_i(
            ax           = axes[ncols + k],
            solver       = solver,
            i            = i,
            feature_name = feature_name,
        )

    # Hide unused axes
    total_plots = n_features + 1
    for k in range(1, ncols):
        axes[k].set_visible(False)
    for k in range(total_plots + ncols - 1, len(axes)):
        axes[k].set_visible(False)

    return axes

def make_mosaics_rule_vs_comp_for_i(
    solver,
    i: int,
    ncols: int = 3,
) -> plt.Figure:
    """
    Creates a figure showing mosaics for the whole rule and each feature.

    Parameters
    ----------
    solver : InsightSolver
        The solver object.
    i : int
        Index of the rule.
    ncols : int
        Number of columns in the subplot grid.

    Returns
    -------
    fig : plt.Figure
        The created figure.
    """
    if not solver._is_fitted:
        return None
    if i not in range(len(solver)):
        raise Exception(f"ERROR (make_mosaics_rule_vs_comp_for_i): i={i} is not valid.")
    if ncols not in [1, 2, 3, 4]:
        ncols = 3

    # Feature names
    feature_names = solver.i_to_feature_names(i=i, do_sort=True)
    n_features = len(feature_names)

    # Number of rows
    nrows = 1 + (1 + (n_features - 1) // ncols)

    # Figure size
    fig_width = 12
    fig_height = 4 * nrows
    figsize = (fig_width, fig_height)
    fig, axes = plt.subplots(
        nrows   = nrows,
        ncols   = ncols,
        figsize = figsize,
    )
    axes = axes.flatten()

    # Draw all mosaics
    draw_mosaics_rule_vs_comp_for_i(
        axes   = axes,
        solver = solver,
        i      = i,
        ncols  = ncols,
    )

    fig.tight_layout()
    return fig

def plot_mosaics_rule_vs_comp_for_i(
    solver,
    i: int,
    ncols: int = 3,
) -> None:
    """
    Displays the mosaic plots of the rule at position i,
    including the whole rule and each feature.

    Parameters
    ----------
    solver : InsightSolver
        The solver object.
    i : int
        Index of the rule.
    ncols : int
        Number of columns in the subplot grid.
    """
    fig = make_mosaics_rule_vs_comp_for_i(
        solver = solver,
        i      = i,
        ncols  = ncols,
    )
    if fig:
        plt.show()

################################################################################
################################################################################
# Mosaic of rule vs pop vs complement for the rule i

def draw_mosaic_rule_vs_pop_for_i(
    ax: plt.Axes,
    solver,
    i: int,
    do_plot_comp:bool = True,
) -> plt.Axes:
    """
    Draws the mosaic plot that compares the purity of the rule at index i vs the population.

    Parameters
    ----------
    ax : plt.Axes
        The axes to draw on.
    solver : InsightSolver
        The solver object.
    i : int
        Index of the rule.
    do_plot_comp : bool
        If True, show the complement.

    Returns
    -------
    ax : plt.Axes
        The axes with the plot.
    """
    # Population statistics
    M  = solver.M
    M1 = solver.M1
    M0 = solver.M0
    # Rule statistics
    rule_i = solver.i_to_rule(i=i)
    m  = rule_i['m']
    m1 = rule_i['m1']
    m0 = rule_i['m0']
    # Complement statistics
    mc  = M-m
    m1c = M1-m1
    m0c = M0-m0

    # Computing the various purities
    mu1_pop  = M1/M if M>0 else 0
    mu0_pop  = M0/M if M>0 else 0
    mu1_rule = m1/m if m>0 else 0
    mu0_rule = m0/m if m>0 else 0
    mu1_comp = m1c/mc if mc>0 else 0
    mu0_comp = m0c/mc if mc>0 else 0

    # Create a pandas Series with a MultiIndex
    if do_plot_comp:
        data = pd.Series(
            data = [mu1_pop,mu0_pop,mu1_rule,mu0_rule,mu1_comp,mu0_comp],
            index = pd.MultiIndex.from_product([['Population', 'Rule', 'Complement'], ['1', '0']]),
        )
    else:
        data = pd.Series(
            data = [mu1_pop,mu0_pop,mu1_rule,mu0_rule],
            index = pd.MultiIndex.from_product([['Population', 'Rule'], ['1', '0']]),
        ) 

    def color_func(key):
        """
        Returns a dictionary of colors based on the key tuple.
        Key format: (in rule or not, class 0 or 1)
        """
        # Define colors for each combination
        if key == ('Population', '1'):
            return {'color': 'grey'}
        elif key == ('Population', '0'):
            return {'color': 'grey', 'alpha':0.5}
        elif key == ('Rule', '1'):
            return {'color': HEX_INSIGHTSOLVER}
        elif key == ('Rule', '0'):
            return {'color': HEX_INSIGHTSOLVER, 'alpha':0.5}
        elif key == ('Complement', '1'):
            return {'color': 'grey'}
        elif key == ('Complement', '0'):
            return {'color': 'grey', 'alpha':0.5}
        else:
            return {}

    # Custom labelizer to show nothing
    def empty_labelizer(key):
        return ""

    # Create the plot with your existing parameters
    from statsmodels.graphics.mosaicplot import mosaic
    mosaic(
        data       = data,
        ax         = ax,
        properties = color_func,
        labelizer  = empty_labelizer,
        gap        = 0.03,
        title      = "",
        statistic  = False,
        axes_label = True,
    )

    # Add title
    ax_top = ax.twiny()
    ax_top.set_xlabel(
        xlabel     = f"Insight #{i+1}",
        fontsize   = 12,
        fontweight = 'bold',
    )
    # Add a bit of distance between the title and the figure
    ax_top.xaxis.labelpad = 10

    # Edit the xlabel and ylabel
    ax.set_xlabel("Subset", fontsize=12)
    ax.set_ylabel("Class", fontsize=12)
    
    # Mask the top tickers
    fig = ax.get_figure()
    for a in fig.axes:
        if a.xaxis.get_ticks_position() == "top":
            if not any(lbl in ["Population", "Rule", "Complement"] for lbl in a.get_xticklabels()):
                a.set_xticks([])
                a.set_xticklabels([])
                a.tick_params(top=False)

    alpha = 0.2
    backgroundcolor = (1,1,1,alpha)
    fontsize = 9
    if mu1_pop != 0:
        ax.text(
            x        = 0.166 if do_plot_comp else 0.25,
            y        = mu1_pop/2,
            s        = f"{mu1_pop:.1%}",
            fontsize = fontsize,
            ha       = 'center',
            va       = 'center',
            backgroundcolor = backgroundcolor,
        )
    if mu0_pop != 0:
        ax.text(
            x        = 0.166 if do_plot_comp else 0.25,
            y        = mu1_pop+(mu0_pop/2),
            s        = f"{mu0_pop:.1%}",
            fontsize = fontsize,
            ha       = 'center',
            va       = 'center',
            backgroundcolor = backgroundcolor,
        )
    if mu1_rule != 0:
        ax.text(
            x        = 0.5 if do_plot_comp else 0.75,
            y        = mu1_rule/2,
            s        = f"{mu1_rule:.1%}",
            fontsize = fontsize,
            ha       = 'center',
            va       = 'center',
            backgroundcolor = backgroundcolor,
        )
    if mu0_rule != 0:
        ax.text(
            x        = 0.5 if do_plot_comp else 0.75,
            y        = mu1_rule+(mu0_rule/2),
            s        = f"{mu0_rule:.1%}",
            fontsize = fontsize,
            ha       = 'center',
            va       = 'center',
            backgroundcolor = backgroundcolor,
        )
    if do_plot_comp:
        if mu1_comp != 0:
            ax.text(
                x        = 0.833,
                y        = mu1_comp/2,
                s        = f"{mu1_comp:.1%}",
                fontsize = fontsize,
                ha       = 'center',
                va       = 'center',
                backgroundcolor = backgroundcolor,
            )
        if mu0_comp != 0:
            ax.text(
                x        = 0.833,
                y        = mu1_comp+(mu0_comp/2),
                s        = f"{mu0_comp:.1%}",
                fontsize = fontsize,
                ha       = 'center',
                va       = 'center',
                backgroundcolor = backgroundcolor,
            )
    return ax

def make_mosaic_rule_vs_pop_for_i(
    solver,
    i: int,
    do_plot_comp:bool = True,
) -> plt.Figure:
    """
    Creates a figure showing the mosaic plot that compares the purity of the rule at index i vs the population.

    Parameters
    ----------
    solver : InsightSolver
        The solver object.
    i : int
        Index of the rule.
    do_plot_comp : bool
        If True, show the complement.

    Returns
    -------
    fig : plt.Figure
        The created figure.
    """
    # Make sure the solver if fitted
    if not solver._is_fitted:
        return None
    # Make sure i is valid
    if i not in range(len(solver)):
        raise Exception(f"ERROR (make_mosaic_rule_vs_pop_for_i): i={i} is not valid.")
    
    fig, ax = plt.subplots(figsize=(4, 4))
    
    draw_mosaic_rule_vs_pop_for_i(
        ax=ax,
        solver=solver,
        i=i,
        do_plot_comp=do_plot_comp,
    )
    
    # Only tight_layout if showing an individual plot
    fig.tight_layout()
    return fig

def plot_mosaic_rule_vs_pop_for_i(
    solver,
    i: int,
    do_plot_comp:bool = True,
) -> None:
    """
    Displays the mosaic plot that compares the purity of the rule at index i vs the population.

    Parameters
    ----------
    solver : InsightSolver
        The solver object.
    i : int
        Index of the rule.
    do_plot_comp : bool
        If True, show the complement.
    """
    fig = make_mosaic_rule_vs_pop_for_i(
        solver=solver,
        i=i,
        do_plot_comp=do_plot_comp,
    )
    if fig:
        plt.show()

################################################################################
################################################################################
# Mosaics of rule vs pop vs complement

def draw_mosaics_rule_vs_pop(
    axes: list[plt.Axes],
    solver,
    do_plot_comp: bool = True,
) -> list[plt.Axes]:
    """
    Draws mosaics of the purity of all rules vs population (and complement if requested).

    Parameters
    ----------
    axes : list of plt.Axes
        The axes where to draw the plots.
    solver : InsightSolver
        The solver object.
    do_plot_comp : bool
        If True, show the complement.

    Returns
    -------
    axes : list of plt.Axes
        The axes with plots drawn.
    """
    range_i = solver.get_range_i()
    for i in range_i:
        k=i
        draw_mosaic_rule_vs_pop_for_i(
            ax           = axes[k],
            solver       = solver,
            i            = i,
            do_plot_comp = do_plot_comp,
        )

    # Hide remaining unused axes
    for k in range(len(range_i), len(axes)):
        axes[k].set_visible(False)

    return axes

def make_mosaics_rule_vs_pop(
    solver,
    do_plot_comp: bool = True,
    ncols: int         = 3,
    fig_width: float   = 12,
) -> plt.Figure:
    """
    Creates a figure showing mosaics of purity vs population for all rules.

    Parameters
    ----------
    solver : InsightSolver
        The solver object.
    do_plot_comp : bool
        If True, show the complement.
    ncols : int
        Number of columns in the subplot grid.
    fig_width : float
        Width of the figure in inches.

    Returns
    -------
    fig : plt.Figure
        The created figure.
    """
    if not solver._is_fitted:
        return None

    range_i = solver.get_range_i()
    n_rules = len(range_i)
    nrows = 1 + (n_rules - 1) // ncols
    width_per_plot = fig_width / ncols
    fig_height = width_per_plot * nrows
    figsize = (fig_width, fig_height)

    fig, axes = plt.subplots(
        nrows   = nrows,
        ncols   = ncols,
        figsize = figsize,
    )
    axes = axes.flatten()

    draw_mosaics_rule_vs_pop(
        axes         = axes,
        solver       = solver,
        do_plot_comp = do_plot_comp,
    )

    fig.tight_layout()
    return fig

def plot_mosaics_rule_vs_pop(
    solver,
    do_plot_comp: bool = True,
    ncols: int         = 3,
    fig_width: float   = 12,
    verbose: bool      = False,
) -> None:
    """
    Displays the mosaic plots of purity vs population for all rules.

    Parameters
    ----------
    solver : InsightSolver
        The solver object.
    do_plot_comp : bool
        If True, show the complement.
    ncols : int
        Number of columns in the subplot grid.
    fig_width : float
        Width of the figure in inches.
    verbose : bool
        If True, prints debug information.
    """
    if not solver._is_fitted:
        return None

    if verbose:
        print(f"\nplot_mosaics_rule_vs_pop : ncols={ncols}, fig_width={fig_width}")

    fig = make_mosaics_rule_vs_pop(
        solver       = solver,
        do_plot_comp = do_plot_comp,
        ncols        = ncols,
        fig_width    = fig_width,
    )

    if fig:
        plt.show()

################################################################################
################################################################################
# Complete plot

def make_all(
    solver,
    language: str = 'en',
    do_mutual_information: bool   = True,
    do_banner: bool               = True,
    do_contributions: bool        = True,
    do_distributions: bool        = True,
    do_mosaics_rule_vs_comp: bool = True,
    do_mosaics_rule_vs_pop: bool  = True,
    do_legend: bool               = True,
) -> List[tuple[str, plt.Figure]]:
    """
    Creates all visualization figures for the solver.
    
    This function generates (depending on boolean flags):
    - Mutual information plot
    - Banner for each rule
    - Feature contributions for each rule
    - Feature distributions for each rule
    - Mosaics of rule vs complement for each rule
    - Mosaics of rule vs population
    - Legend
    
    Parameters
    ----------
    solver : InsightSolver
        The fitted solver object.
    language : str
        Language for the plots ('en' or 'fr').
    do_mutual_information : bool
        Whether to generate the mutual information figure.
    do_banner : bool
        Whether to generate the banner figure for each rule.
    do_contributions : bool
        Whether to generate the feature contributions figures.
    do_distributions : bool
        Whether to generate the feature distributions figures.
    do_mosaics_rule_vs_comp : bool
        Whether to generate the mosaics of rule vs complement figures.
    do_mosaics_rule_vs_pop : bool
        Whether to generate the mosaics of rule vs population figures.
    do_legend : bool
        Whether to generate the legend figure.
    
    Returns
    -------
    figs : List[tuple[str, plt.Figure]]
        A list of tuples containing (figure_name, figure_object).
    """
    # Make sure the solver is fitted
    if not solver._is_fitted:
        return []
    
    figs = []
    
    # 1. Mutual information
    if do_mutual_information:
        fig_mi = make_mutual_information(
            solver    = solver,
            n_samples = 1000,
            n_cols    = 20,
            kind      = 'barh',
        )
        figs.append(('mutual_information', fig_mi))
    
    # Loop over all rules
    for i in solver.get_range_i():
        S = solver.i_to_S(i=i)
        
        # 2. Banner for rule i
        if do_banner:
            fig_banner = make_banner_fig_for_i(
                solver = solver,
                i      = i,
            )
            figs.append((f'rule_{i}_banner', fig_banner))
        
        # 3. Feature contributions for rule i
        if do_contributions:
            figs_contrib = make_feature_contributions_for_i(
                solver    = solver,
                i         = i,
                language  = language,
                do_banner = False,  # Already handled separately
            )
            for k, fig in enumerate(figs_contrib):
                figs.append((f'rule_{i}_contributions_{k}', fig))
        
        # 4. Feature distributions for rule i
        if do_distributions:
            figs_dist = make_feature_distributions_for_S(
                solver   = solver,
                S        = S,
                language = language,
            )
            for k, fig in enumerate(figs_dist):
                figs.append((f'rule_{i}_distributions_{k}', fig))
        
        # 5. Mosaics of rule vs complement for rule i
        if do_mosaics_rule_vs_comp:
            fig_mosaic = make_mosaics_rule_vs_comp_for_i(
                solver = solver,
                i      = i,
            )
            figs.append((f'rule_{i}_mosaics_rule_vs_comp', fig_mosaic))

    # 6. Mosaics of rule vs population
    if do_mosaics_rule_vs_pop:
        fig_mosaic_pop = make_mosaics_rule_vs_pop(
            solver       = solver,
            do_plot_comp = True,
        )
        figs.append(('mosaics_rule_vs_pop', fig_mosaic_pop))
    
    # 7. Legend
    if do_legend:
        fig_legend = make_legend_fig(
            language = language,
        )
        figs.append(('legend', fig_legend))
    
    return figs

def plot_all(
    solver,
    language: str = 'en',
    do_mutual_information: bool   = True,
    do_banner: bool               = True,
    do_contributions: bool        = True,
    do_distributions: bool        = True,
    do_mosaics_rule_vs_comp: bool = True,
    do_mosaics_rule_vs_pop: bool  = True,
    do_legend: bool               = True,
) -> None:
    """
    Displays all visualization figures for the solver.
    
    This function displays (depending on boolean flags):
    - Mutual information plot
    - Banner for each rule
    - Feature contributions for each rule
    - Feature distributions for each rule
    - Mosaics of rule vs complement for each rule
    - Mosaics of rule vs population
    - Legend
    
    Parameters
    ----------
    solver : InsightSolver
        The fitted solver object.
    language : str
        Language for the plots ('en' or 'fr').
    do_mutual_information : bool
        Whether to display the mutual information figure.
    do_banner : bool
        Whether to display the banner figure for each rule.
    do_contributions : bool
        Whether to display the feature contributions figures.
    do_distributions : bool
        Whether to display the feature distributions figures.
    do_mosaics_rule_vs_comp : bool
        Whether to display the mosaics of rule vs complement figures.
    do_mosaics_rule_vs_pop : bool
        Whether to display the mosaics of rule vs population figures.
    do_legend : bool
        Whether to display the legend figure.
    """
    # Make sure the solver is fitted
    if not solver._is_fitted:
        return
    
    # 1. Mutual information
    if do_mutual_information:
        plot_mutual_information(
            solver    = solver,
            n_samples = 1000,
            n_cols    = 20,
            kind      = 'barh',
        )
    
    # Loop over all rules
    for i in solver.get_range_i():
        S = solver.i_to_S(i=i)
        
        # 2. Banner for rule i
        if do_banner:
            plot_banner_fig_for_i(
                solver = solver,
                i      = i,
            )
        
        # 3. Feature contributions for rule i
        if do_contributions:
            plot_feature_contributions_for_i(
                solver    = solver,
                i         = i,
                language  = language,
                do_banner = False,  # Already shown separately
            )
        
        # 4. Feature distributions for rule i
        if do_distributions:
            plot_feature_distributions_for_S(
                solver   = solver,
                S        = S,
                language = language,
            )
            
        # 5. Mosaics of rule vs complement for rule i
        if do_mosaics_rule_vs_comp:
            plot_mosaics_rule_vs_comp_for_i(
                solver = solver,
                i      = i,
            )

    # 6. Mosaics of rule vs population
    if do_mosaics_rule_vs_pop:
        plot_mosaics_rule_vs_pop(
            solver       = solver,
            do_plot_comp = True,
        )
    
    # 7. Legend
    if do_legend:
        plot_legend_fig(
            language = language,
        )

################################################################################
################################################################################
# Export to PDF

def make_pdf(
    solver,
    output_file: Optional[str]    = None,
    verbose: bool                 = False,
    do_mutual_information: bool   = True,
    do_banner: bool               = True,
    do_contributions: bool        = True,
    do_distributions: bool        = True,
    do_mosaics_rule_vs_comp: bool = True,
    do_mosaics_rule_vs_pop: bool  = True,
    do_legend: bool               = True,
    language: str                 = "en",
) -> str:
    """
    Generates a PDF containing all visualization figures for the solver.

    Parameters
    ----------
    solver : InsightSolver
        The fitted solver object.
    output_file : str, optional
        If provided, export the PDF at this path.
    verbose : bool
        Verbosity.
    do_mutual_information : bool
        Include mutual information figure.
    do_banner : bool
        Include banner figures.
    do_contributions : bool
        Include contribution figures.
    do_distributions : bool
        Include distribution figures.
    do_mosaics_rule_vs_comp : bool
        Include mosaics of rule vs complement figures.
    do_mosaics_rule_vs_pop : bool
        Include mosaics of rule vs population figures.
    do_legend : bool
        Include legend figure.
    language : str
        Language for the plots ('en' or 'fr').

    Returns
    -------
    pdf_base64 : str
        PDF content encoded as base64 for in-memory use.
    """

    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.backends.backend_pdf import PdfPages
    import io
    import base64

    if verbose:
        print("Generating PDF...")

    # Generate all figures
    figs = make_all(
        solver                  = solver,
        language                = language,
        do_mutual_information   = do_mutual_information,
        do_banner               = do_banner,
        do_contributions        = do_contributions,
        do_distributions        = do_distributions,
        do_mosaics_rule_vs_comp = do_mosaics_rule_vs_comp,
        do_mosaics_rule_vs_pop  = do_mosaics_rule_vs_pop,
        do_legend               = do_legend,
    )

    # Write figures to PDF in memory
    pdf_buffer = io.BytesIO()
    with PdfPages(pdf_buffer) as pdf:
        
        # 1. Mutual information
        # Filter figures for mutual information
        figs_mi = [fig for name, fig in figs if name == 'mutual_information']
        if figs_mi:
            save_figs_in_pdf(figs_mi, pdf)
            
        # 2. Loop over rules to group figures per page
        range_i = solver.get_range_i()
        for i in range_i:
            # Collect all figures for rule i
            figs_i = []
            
            # Banner
            for name, fig in figs:
                if name == f'rule_{i}_banner':
                    figs_i.append(fig)
                    break
            
            # Contributions
            # We need to preserve order, so we iterate through figs
            for name, fig in figs:
                if name.startswith(f'rule_{i}_contributions_'):
                    figs_i.append(fig)
            
            # Distributions
            for name, fig in figs:
                if name.startswith(f'rule_{i}_distributions_'):
                    figs_i.append(fig)
            
            # Mosaics rule vs comp
            for name, fig in figs:
                if name == f'rule_{i}_mosaics_rule_vs_comp':
                    figs_i.append(fig)
                    break
            
            # Save the group of figures for rule i on one page (or stacked pages)
            if figs_i:
                save_figs_in_pdf(figs_i, pdf)
        
        # 3. Mosaics rule vs pop
        figs_pop = [fig for name, fig in figs if name == 'mosaics_rule_vs_pop']
        if figs_pop:
            save_figs_in_pdf(figs_pop, pdf)
            
        # 4. Legend
        figs_legend = [fig for name, fig in figs if name == 'legend']
        if figs_legend:
            save_figs_in_pdf(figs_legend, pdf)

    # Export to disk if requested
    if output_file is not None:
        with open(output_file, "wb") as f:
            f.write(pdf_buffer.getvalue())
        if verbose:
            print(f"PDF exported to {output_file}")

    # Return PDF as base64
    pdf_bytes = pdf_buffer.getvalue()
    pdf_base64 = base64.b64encode(pdf_bytes).decode()
    return pdf_base64

################################################################################
################################################################################
# Export to ZIP

def make_zip(
    solver,
    output_file: Optional[str] = None,
    verbose: bool              = False,
    do_png: bool               = True,
    do_csv: bool               = True,
    do_json: bool              = True,
    do_excel: bool             = True,
    do_pdf: bool               = True,
    language: str              = "en",
) -> str:
    """
    Export the solver content to a ZIP file.

    Parameters
    ----------
    solver : InsightSolver
        The fitted solver object.
    output_file : str, optional
        If provided, the ZIP will be saved to this path.
    verbose : bool
        Whether to print progress messages.
    do_png : bool
        Include PNG figures.
    do_csv : bool
        Include CSV ruleset.
    do_json : bool
        Include JSON ruleset.
    do_excel : bool
        Include Excel ruleset.
    do_pdf : bool
        Include PDF of figures.
    language : str
        Language for plots ('en' or 'fr').

    Returns
    -------
    zip_base64 : str
        ZIP content encoded as base64 for in-memory use.
    """
    import io
    import zipfile
    import base64
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    if verbose:
        print("Generating ZIP...")

    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, "w") as zip_file:

        # PNG figures
        if do_png:
            figs = []
            l_figs = []

            # Generate figures
            figs_all = make_all(
                solver,
                language                = language,
                do_mutual_information   = True,
                do_banner               = True,
                do_contributions        = True,
                do_distributions        = True,
                do_mosaics_rule_vs_comp = True,
                do_mosaics_rule_vs_pop  = True,
                do_legend               = True,
            )

            for name, fig in figs_all:
                file_name = f"{name}.png"
                l_figs.append((fig, file_name))

            for fig, file_name in l_figs:
                img_buffer = io.BytesIO()
                fig.savefig(img_buffer, format="png")
                plt.close(fig)
                img_buffer.seek(0)
                zip_file.writestr(file_name, img_buffer.read())
            if verbose:
                print("Added PNG figures")

        # CSV
        if do_csv:
            csv_content = solver.to_csv()
            zip_file.writestr("insightsolver-ruleset.csv", csv_content)
            if verbose:
                print("Added CSV")

        # JSON
        if do_json:
            json_content = solver.to_json_string()
            zip_file.writestr("insightsolver-ruleset.json", json_content)
            if verbose:
                print("Added JSON")

        # Excel
        if do_excel:
            excel_content = solver.to_excel_string()
            zip_file.writestr("insightsolver-ruleset.xlsx", excel_content)
            if verbose:
                print("Added Excel")

        # PDF
        if do_pdf:
            # use new DRY make_pdf
            pdf_base64 = make_pdf(
                solver                  = solver,
                output_file             = None,
                verbose                 = verbose,
                do_mutual_information   = True,
                do_banner               = True,
                do_contributions        = True,
                do_distributions        = True,
                do_mosaics_rule_vs_comp = True,
                do_mosaics_rule_vs_pop  = True,
                do_legend               = True,
                language                = language,
            )
            pdf_bytes = base64.b64decode(pdf_base64)
            zip_file.writestr("insightsolver-ruleset.pdf", pdf_bytes)
            if verbose:
                print("Added PDF")

    # Write to disk if requested
    if output_file is not None:
        with open(output_file, "wb") as f:
            f.write(zip_buffer.getvalue())
        if verbose:
            print(f"ZIP written to {output_file}")

    zip_bytes = zip_buffer.getvalue()
    zip_base64 = base64.b64encode(zip_bytes).decode()
    if verbose:
        print("ZIP generated in memory")
    return zip_base64

################################################################################
################################################################################
