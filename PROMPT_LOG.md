# AI Prompt Log

> Assessment note: The PDF asks for the initial AI prompt, one real bug/formatting mistake from the first attempt, and the follow-up prompt used to fix it. Keep this log truthful to your own process; edit the example below to match what actually happened.

## Initial prompt
Write a Python script that reads a JSON file containing device IDs and average temperatures, creates a Matplotlib bar chart, adds a chart title and axis labels, avoids overlapping device labels, and saves the chart as a PNG.

## Bug or formatting issue observed
Example to use only if it matches your first attempt: the device labels overlapped when many devices were shown, making the x-axis difficult to read.

## Follow-up prompt
Update the chart code to increase the figure width based on the number of devices, rotate the x-axis labels, right-align them, and use a tight layout so the labels and title are not clipped. Keep the title and both axis labels.

## Review notes
I reviewed the generated code, checked that it reads the same JSON schema produced by `main.py`, and added handling for a missing or malformed JSON file.
