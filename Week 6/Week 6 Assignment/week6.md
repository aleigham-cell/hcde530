# C6 — Data Visualization

## Draft competency claim

I used Python and Plotly in `week6_mp1_starter.ipynb` to build charts from my Zillow / MP1 housing data. The questions behind the visuals: Are there seasonal patterns in Seattle listings and sales that affect purchase timing? How much did ZORI grow in my zip (98004) compared with Seattle metro and the U.S.? Do rent levels (ZORI) and rental demand (ZORDI) move together in Seattle metro?

I used **line charts** to compare ZORI and ZORDI trends over time and to contrast Seattle listings versus sales activity. I chose line charts because the data are monthly time series, so this chart type clearly shows trend direction and pattern changes across time. I also expanded the analysis to a 10-year window so I could contextualize neighborhood and metro comparisons more meaningfully.

**Chart-by-chart (question → type → takeaway):**

1. **Seattle listings & sales vs national (line — *comparison*):** Answers whether listed homes actually sell and how Seattle compares to the national average. Four lines over time let me **compare** regions and metrics, not just describe one series. Takeaway: listings and sales swing seasonally more than prices do—timing is about competition, not big price drops.

2. **ZORI trends + annual growth bars (line + bar — *comparison*):** Answers how 98004, Seattle metro, and U.S. ZORI changed over 10 years. The **line** panel compares rent-index **trends**; the grouped **bar** panel **compares** year-over-year growth rates side by side. Takeaway: Bellevue (98004) lagged metro and national ZORI growth even as home values rose.

3. **ZORI vs ZORDI dual-axis line (*relationship*):** Answers whether rent levels and rental listing demand move together in Seattle metro. Two series on one timeline is a **relationship** view—I am not comparing unrelated categories, I am watching whether the indexes rise or fall together. Takeaway: ZORI rose while ZORDI fell, so costs increased without matching renter demand.

*(I did not use a composition chart—nothing in this analysis was “parts of a whole”—or a distribution chart like a histogram; the data were time series and regional comparisons.)*

### Evidence
- At least one chart generated in Python using Plotly (time-series line charts).
- A written justification explaining why line charts fit the time-series structure.
- I also created a bar chart to show annual ZORI growth rates by year, which makes sense for this data because comparing year-over-year percentage changes benefits from the discrete, categorical nature of a bar chart — each bar represents one year, making it easy to spot which years had the highest growth or slowdowns at a glance.
- The notebook includes code, outputs, and markdown cells that explain what was found.
- I focused on questions about ZORI growth in my neighborhood versus metro and national trends, ZORDI changes over the same period, and added a listings versus sales chart to see whether houses listed actually sold.
