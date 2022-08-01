# Fx_scraper

Hi let me introduce you my very first app.

Application downloads exchange rates from 4 national banks for the month choosen by user and prepares excel input files in the given format. Arisen files are ready to upload to PWC Mylaese tool.

National banks avaialble at the moment:
Polish National Bank
Czech National Bank
Bulgarian National Bank
Croatian National Bank

Application uses National Banks API or in case API doesn't exist downloads data directly from webpage.

MyLease input file requirements:
- Sheet name: Rates
- 3 column with headers:
  - Currency - 3-letter currency code
  - Valid On - date
  - Rate Value - rate
- In case national bank doesn't publish currency rate for a given day, the exchange rate from previus day should be used.
