"""
MoiCmap colormaps

The name of colormaps are composed of two parts: `name` and `suffix`, and
connected by a `_`.
  - `name`: the name of the colormap.
  - `suffix`: the suffix indicating the properties of the colormap.

Colormap name suffix:
  - `mono`: mono luminance colormap, which the luminances of the colors are
    nearly equal.
  - `vl`: for variance luminance colormap, that is, the luminances of the
    colors are changing quickly. This type of colormaps are unfriendly to
    colorblind people, and also not so good for human perception in the magnitude.
  - `l`: lightened colormap, the hue of the colormap is more variant than
    the normal one to distinguish the magnitude.
  - `d`: darkened colormap.

"""
MOI_CMAP = {
    # div，正常亮度，两侧 L = 40
    # Rd: "#bd1200", Bu: "#1c50dd"
    "RdBu": ["#bd1200", "#db7362", "#f2baaf", "#ffffff", "#b0c8f9", "#6590ed", "#1c50dd"],
    "RdBu2": ["#a90401", "#c94c1f", "#e57d42", "#f7aa7b", "#fdd5bd", "#ffffff", "#bcdefb", "#77bcf5", "#3d96e8", "#236dd3", "#203fbd"],
    "RdGn": ["#b5242a", "#d5766f", "#eebab5", "#ffffff", "#b2ceaf", "#679e62", "#036e02"],
    "BuGn": ["#2c57c4", "#6e91db", "#b5c8ef", "#ffffff", "#b2ceaf", "#679e62", "#036e02"],
    "GnPu": ["#036e02", "#679e62", "#b2ceaf", "#ffffff", "#debbe6", "#bb78cb", "#962aae"],
    "BuPu": ["#1c50dd", "#6590ed", "#b0c8f9", "#ffffff", "#e3b9e8", "#c473cf", "#a112b3"],
    "BrGn": ["#742e25", "#99513d", "#bc775b", "#dea184", "#f3cfbd", "#ffffff", "#afe2d5", 
             "#64c1af", "#319b8e", "#0e746c", "#00504a"],

    # div
    "GYPu": ["#036e02", "#408a28", "#68a645", "#95c478", "#cae2bc", "#ffffff", "#f7cef1", "#eb9de2", "#da70c9", "#c548a7", "#b01083"],
    "GnPu2": ["#066b4e", "#0b916a", "#41b78d", "#91dcbd", "#ccf1e1", "#ffffff", "#f1e4ff", "#ddc2f7", 
 "#be93de", "#a267c8", "#8638b5"],
    "prec_div": ["#a00549", "#c65a5f", "#e69877", "#f5caa5", "#ffffff", "#9ce8b7", "#1cbdc5", "#008bd1", "#1e58c3"],
    "prec_div2": ["#b61362", "#cf6b6f", "#eb9583", "#f6c9ab", "#ffffff", "#aadedb", "#48b8d6", "#008bd1", "#1e58c3"],
    "garden": ["#d62b10", "#ea4914", "#f9711f", "#fda748", "#ffd39c",
               "#ffffff", "#cde5a6", "#9acd5e", "#6ab63d", "#4c9e24", "#3b860a"],
    "onion": ["#8224bb", "#b435c8", "#e34ad3", "#fd7fe1", "#ffc2f0",
              "#ffffff", "#e3f6b5", "#c0ec67", "#95db2f", "#65c421", "#29ac16"],
    "OrCy": ["#ba431a", "#d45c20", "#ee7626", "#ff9c57", "#ffcdaa",
             "#ffffff", "#c4f4ee", "#80e8dd", "#47d6cd", "#32c1be", "#18acae"],
    "humidity_d": ["#912e00", "#ad5522", "#c67b40", "#daa65d", "#f0d1a4",
                 "#ffffff", "#afe7eb", "#5dcad8", "#23a4c4", "#007ca9", "#035487"],
    "RdOrCyBu": ["#c12926", "#da6238", "#e78f47", "#edb463", "#f6d698",
                 "#ffffff", "#93eff1", "#35d7f4", "#00b6fd", "#1e87f3", "#5848c3"],
    "hotcold": ["#050f76", "#006acc", "#52a2f2", "#afd6d8", "#d2edf6",
                "#ffffff", "#fbeac0", "#ffb244", "#fe7026", "#d90000", "#7c0600"],
    
    # 多色
    "jet": ["#2a64d8", "#008cdf", "#20abd4", "#00bfcc", "#2ecfb4",
             "#1ac185", "#37b14d", "#2fba3d", "#29c227", "#6ecc2d",
             "#9ad53a", "#bedd33", "#e2e430", "#ecce25", "#f2b825",
             "#ed9105", "#e46701", "#db4400", "#d00101"],
    "jet2": ["#3c45cc", "#2258c1", "#0665b3", "#0079ae", "#008ea9",
             "#00a0a0", "#00b085", "#4bb94e", "#94b119", "#c1a700", 
             "#d39600", "#d98000", "#da6800", "#d74600", "#d10f04"],
    "jet3": ["#4042e6", "#1979cf", "#229fc6", "#14c3d0", "#26e1cc", 
             "#17f5a1", "#80f069", "#a6e143", "#d0c11c", "#d59c06", 
             "#e46701", "#d00101"],
    "jet4": ["#3b4f8e", "#21669f", "#007ba9", "#008fa5", "#00a090", 
             "#4ca67f", "#75ab70", "#869c56", "#938b44", "#957536", 
             "#935f2f", "#924c32", "#8c3b39"],
    "jet5": ["#3d51c1", "#0075cf", "#0091ce", "#00a7c8", "#00b29a", 
             "#38b441", "#8ea300", "#c58b00", "#d36a0f", "#be481b", 
             "#a52620"],
    "jet_vl": ["#1600bd","#0566e6","#00aaff","#00ffee","#7FFFD4","#02ed3d",
            "#00cc03","#9fed02","#ffed29","#f7b602","#e46701","#d00101"],
    "wysiwygcont": ["#400f4a", "#000bca", "#004bc0", "#0c6daa", "#20819f", 
                    "#009691", "#32a844", "#59bc04", "#94b206", "#bdad24", 
                    "#fbae5f", "#fcbdb6", "#fed0e6", "#fedffd", "#fffeff"],
    "humidity": ["#f9e19d", "#e6dd8d", "#cdda81", "#a9da80", "#7ad485",
                 "#39ca8f", "#04bbb3", "#32a6b7", "#1f8da9", "#066a92", "#144373"],
    "humidity2": ["#fcf9f2", "#e8ecd7", "#c9e1c3", "#a2dcbf", "#6fd5c8", 
                  "#42c6cf", "#03b5d5", "#00a6d6", "#2097d3", "#277fca", "#4364bb"],
    "humidity3": ["#ffffff", "#f5f1cb", "#e7e397", "#d8db79", "#c6d765", 
                  "#add455", "#88d04c", "#57cb49", "#00c286", "#00b3a8", 
                  "#00a4b6", "#0096be", "#0084c3", "#006eca", "#2250c6"],
    "humidity_vl": ["#c06b24", "#eaa559", "#e6d03e", "#9cb637", "#62a043",
                    "#29b626", "#4ed1a6", "#45ecf6", "#5ec8ed", "#389cd1",
                    "#1e45ad"],

}