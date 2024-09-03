# Christopher Davis
# September 2024
# File for creating all figures for the Directory html page

import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import pandas as pd
import seaborn
import os
import geopandas as gpd
from urllib.request import urlopen
import json
import matplotlib.patches as mpatches

'''
Unused but want to use at some point
* Dendogram
* Sankey Diagram
* Chord Diagram
'''

# Colors
from pypalettes import load_cmap
cmap = load_cmap('grovyle')
# groudon, grovyle, anorith, huntail, info2, nuzleaf
cmaplist = cmap.colors

# Styling
TitleLoc = 'left'
FigDPIs = 300
FigSize = (2,2.2)
FigEdgecolor = 'white'
FigFacecolor = 'white'
titlefontsize = 10.5
AxesFontSize = 6

# Fake Data
CatNames = ['A', 'B', 'C', 'D', 'E']
CatValues = [26, 34, 19, 5, 16] 
SequentialX = np.linspace(1,58,19)
SequentialY1 = [4, 7, 6, 8, 2, 1, 6, 9, 11, 12, 3, 8, 1, 15, 18, 3, 12, 23, 19]
SequentialY2 = [21, 14, 19, 17, 11, 15, 12, 19, 17, 11, 14, 8, 7, 15, 6, 3, 4, 12, 8]
BiggerData = SequentialY1 + SequentialY2
Random2D = np.random.rand(8,8)

# Barchart
fig_barchart, ax_barchart = plt.subplots(figsize=FigSize)
ax_barchart.bar(CatNames, CatValues, color=cmap.colors)
ax_barchart.set_title('Bar Chart', loc=TitleLoc, fontsize = titlefontsize)

# Line Plot
fig_linechart, ax_linechart = plt.subplots(figsize=FigSize)
ax_linechart.plot(SequentialX, SequentialY1, color=cmaplist[0])
ax_linechart.plot(SequentialX, SequentialY2, color=cmaplist[2])
ax_linechart.set_title('Line Chart', loc=TitleLoc, fontsize = titlefontsize)

# Scatter Plot
fig_scatterchart, ax_scatterchart = plt.subplots(figsize=FigSize)
ax_scatterchart.scatter(SequentialY1, SequentialY2, color=cmaplist[0])
ax_scatterchart.set_title('Scatter Plot', loc=TitleLoc, fontsize = titlefontsize)

# Heat Map
fig_heatchart, ax_heatchart = plt.subplots(figsize=FigSize)
ax_heatchart.imshow(Random2D, cmap=cmap)
ax_heatchart.set_title('Heatmap', loc=TitleLoc, fontsize = titlefontsize)

# Violin Plot
fig_violinchart, ax_violinchart = plt.subplots(figsize=FigSize)
violin_parts = ax_violinchart.violinplot([sorted(BiggerData)[10:30], sorted(BiggerData)[0:20], sorted(BiggerData)[20:38]], [0,1,2], widths = 0.75, bw_method = 0.25, showmeans = True, showextrema = False)
ax_violinchart.set_title('Violin Plot', loc=TitleLoc, fontsize = titlefontsize)
for q, vp in enumerate(violin_parts['bodies']):
    vp.set_facecolor(cmaplist[q])
    vp.set_edgecolor('black')
    vp.set_linewidth(1.5)
    vp.set_alpha(0.75)
vp = violin_parts['cmeans']
vp.set_edgecolor('black')
vp.set_linewidth(1.5)

# Choropleth
fig_chorochart, ax_chorochart = plt.subplots(1, 1, figsize = FigSize)
ax_chorochart.set_title('Choropleth', loc=TitleLoc, fontsize = titlefontsize)
gdf = gpd.read_file('https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json')
gdf = gdf.loc[gdf['STATE'] == '22']
gdf.plot(column="id", categorical=False, cmap=cmap, ax = ax_chorochart)
ax_chorochart.set_box_aspect(1)

# Network
fig_networkchart, ax_networkchart = plt.subplots(figsize=FigSize)
ax_networkchart.set_title('Network', loc=TitleLoc, fontsize = titlefontsize)
Coords = list(map(lambda x, y:(x,y), SequentialY1, SequentialY2))
for x in Coords:
    for y in Coords:
        dist = np.sqrt((abs(x[0]-y[0]))**2 + (abs(x[1]-y[1]))**2)
        if dist < 6:
            ax_networkchart.plot([x[0], y[0]],[x[1], y[1]],marker = 'o', markersize = 6, markeredgecolor = cmaplist[0], markerfacecolor=cmaplist[0], color=cmap(dist/6))


# Treemap
fig_treechart, ax_treechart = plt.subplots(figsize=FigSize)
ax_treechart.set_title('Treemap', loc=TitleLoc, fontsize = titlefontsize)
# Create the Rectangles Starts & Widths based on the five categorical proportion values.
Gap = 0.15
C1 = (Gap, Gap)
R1 = ((CatValues[0]+CatValues[1])/10-Gap*1.5, 10-Gap*2)
C2 = (R1[0]+Gap*2, Gap)
R2 = ((CatValues[2]+CatValues[3]+CatValues[4])/10 - Gap*1.5, 10-Gap*2)
C3 = (Gap*2, Gap*2); 
R3 = (R1[0]-Gap*2, 10*CatValues[0]/(CatValues[0]+CatValues[1]) - Gap*2)
C4 = (Gap*2, C3[1]+R3[1]+Gap)
R4 = (R1[0]-Gap*2, 10*CatValues[1]/(CatValues[0]+CatValues[1]) - Gap*3)
C5 = (R1[0]+Gap*3, Gap*2); 
R5 = (R2[0]-Gap*2, 10*CatValues[2]/(CatValues[2]+CatValues[3]+CatValues[4]) - Gap*2)
C6 = (R1[0]+Gap*3, C5[1]+R5[1]+Gap)
R6 = (R2[0]-Gap*2, 10*CatValues[3]/(CatValues[2]+CatValues[3]+CatValues[4]) - Gap*2)
C7 = (R1[0]+Gap*3, C6[1]+R6[1]+Gap)
R7 = (R2[0]-Gap*2, 10*CatValues[4]/(CatValues[2]+CatValues[3]+CatValues[4]) - Gap*2)
C8 = (C4[0]+Gap, C4[1]+Gap)
R8 = (R4[0]/3 - Gap*1.5, R4[1]-Gap*2)
C9 = (C8[0]+R8[0]+Gap, C4[1]+Gap)
R9 = (2*R4[0]/3 - Gap*1.5, R4[1]-Gap*2)
ax_treechart.add_artist(mpatches.Rectangle(C1, R1[0], R1[1], ec="black", fc = cmaplist[0], linewidth = 0.5))
ax_treechart.add_artist(mpatches.Rectangle(C2, R2[0], R2[1], ec="black", fc = cmaplist[1], linewidth = 0.5))
ax_treechart.add_artist(mpatches.Rectangle(C3, R3[0], R3[1], ec="black", fc = cmaplist[2], linewidth = 0.5))
ax_treechart.add_artist(mpatches.Rectangle(C4, R4[0], R4[1], ec="black", fc = cmaplist[3], linewidth = 0.5))
ax_treechart.add_artist(mpatches.Rectangle(C5, R5[0], R5[1], ec="black", fc = cmaplist[4], linewidth = 0.5))
ax_treechart.add_artist(mpatches.Rectangle(C6, R6[0], R6[1], ec="black", fc = cmaplist[5], linewidth = 0.5))
ax_treechart.add_artist(mpatches.Rectangle(C7, R7[0], R7[1], ec="black", fc = cmaplist[6], linewidth = 0.5))
ax_treechart.add_artist(mpatches.Rectangle(C8, R8[0], R8[1], ec="black", fc = cmaplist[7], linewidth = 0.5))
ax_treechart.add_artist(mpatches.Rectangle(C9, R9[0], R9[1], ec="black", fc = cmaplist[8], linewidth = 0.5))
ax_treechart.set_xlim([0,10]); ax_treechart.set_ylim([0,10])

# Stacked Density Plot
fig_stackchart, ax_stackchart = plt.subplots(figsize=FigSize)
StackInter = np.asarray(SequentialY2)+np.asarray(SequentialY1)
ax_stackchart.plot(SequentialX, SequentialY1, color='black')
ax_stackchart.plot(SequentialX, StackInter, color='black')
ax_stackchart.fill_between(SequentialX, SequentialY1, [0]*len(StackInter), color=cmaplist[0])
ax_stackchart.fill_between(SequentialX, SequentialY1, StackInter, color=cmaplist[1])
ax_stackchart.fill_between(SequentialX, StackInter, [50]*len(StackInter), color=cmaplist[2])
ax_stackchart.set_title('Stacked Density Chart', loc=TitleLoc, fontsize = titlefontsize)

# All Figure Formatting
for ax in [ax_barchart, ax_linechart, ax_scatterchart, ax_heatchart, ax_violinchart, ax_chorochart, ax_networkchart, ax_treechart, ax_stackchart]:
    ax.set_xticks([])
    ax.set_yticks([])
    
for fig in [fig_barchart, fig_linechart, fig_scatterchart, fig_heatchart, fig_violinchart, fig_chorochart, fig_networkchart, fig_treechart, fig_stackchart]:
    fig.subplots_adjust(hspace = 0.0, wspace = 0.0, left = 0.025, right = 0.975, top = 0.9, bottom = 0.025)

# Saveing & Showing
os.chdir("images")
fig_barchart.savefig('Dir_'+'fig_barchart'+'.png', edgecolor=FigEdgecolor, dpi=FigDPIs, facecolor=FigFacecolor, transparent=True)
fig_linechart.savefig('Dir_'+'fig_linechart'+'.png', edgecolor=FigEdgecolor, dpi=FigDPIs, facecolor=FigFacecolor, transparent=True)
fig_scatterchart.savefig('Dir_'+'fig_scatterchart'+'.png', edgecolor=FigEdgecolor, dpi=FigDPIs, facecolor=FigFacecolor, transparent=True)
fig_heatchart.savefig('Dir_'+'fig_heatchart'+'.png', edgecolor=FigEdgecolor, dpi=FigDPIs, facecolor=FigFacecolor, transparent=True)
fig_violinchart.savefig('Dir_'+'fig_violinchart'+'.png', edgecolor=FigEdgecolor, dpi=FigDPIs, facecolor=FigFacecolor, transparent=True)
fig_chorochart.savefig('Dir_'+'fig_chorochart'+'.png', edgecolor=FigEdgecolor, dpi=FigDPIs, facecolor=FigFacecolor, transparent=True)
fig_networkchart.savefig('Dir_'+'fig_networkchart'+'.png', edgecolor=FigEdgecolor, dpi=FigDPIs, facecolor=FigFacecolor, transparent=True)
fig_treechart.savefig('Dir_'+'fig_treechart'+'.png', edgecolor=FigEdgecolor, dpi=FigDPIs, facecolor=FigFacecolor, transparent=True)
fig_stackchart.savefig('Dir_'+'fig_stackchart'+'.png', edgecolor=FigEdgecolor, dpi=FigDPIs, facecolor=FigFacecolor, transparent=True)

#plt.show()