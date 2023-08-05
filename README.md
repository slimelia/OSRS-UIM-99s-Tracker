# UIM 99 Stats
The source code for the [UIM 99s](https://docs.google.com/spreadsheets/d/1HkK2r4SHCkrz-Kjy8vhfeH1isNnX4GWagwLgFN84W8A/edit?usp=sharing) sheet.

## Description
This script scrapes the Old School RuneScape hiscores and counts:
1 The number of maxed UIMs
2 The number of UIMs with 99 in each skill.

To avoid being timed out it stores the most recent count in a json file.
Positions of relevant Google Sheet cells to update are stored in `tablePositions.json`.
