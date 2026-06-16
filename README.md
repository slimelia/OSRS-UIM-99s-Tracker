> [!WARNING]
> This project is now **archived**.
> Unfortunately, necessary scraping of the Hiscores can no longer be performed because of Cloudflare anti-scraping protections.
>
> A rewrite would be necessary to bypass these restrictions, and given that this script stopped working _9 months ago_ and nobody noticed, there appears to be no demand for a fix. I am leaving this repository up as an archive in case anyone wishes to fork it in the future. A note will also be added to the related Google Sheet.

# UIM 99 Stats
The source code for the [UIM 99s](https://docs.google.com/spreadsheets/d/1HkK2r4SHCkrz-Kjy8vhfeH1isNnX4GWagwLgFN84W8A/edit?usp=sharing) sheet.

## Description
This script scrapes the Old School RuneScape hiscores and counts:
1 The number of maxed UIMs
2 The number of UIMs with 99 in each skill.

To avoid being timed out it stores the most recent count in a json file.
Positions of relevant Google Sheet cells to update are stored in `tablePositions.json`.
