
**[Description](#problem-description)**                            |
**[Install Requirements](#install-requirements)**                  |
**[Tests](#tests)**                                                |         
---

# Super Simple Stock Market

## Description

This repo contains the complete source code that will:
- For a given stock instance `Stock` (`PreferredStock` instance if preferred stock), 
  - Given any price as input, calculates the dividend yield: `Stock.get_dividend_yield`
  - Given any price as input,  calculates the P/E Ratio: `Stock.get_pe_ratio`
  - Records a trade, with timestamp, quantity, buy or sell indicator and price: `Stock.add_trade_record`
  - Calculates Volume Weighted Stock Price based on trades in past  5 minutes: `Stock.get_volume_weighted_stock_price`
-	Calculates the GBCE All Share Index using the geometric mean of the Volume Weighted Stock Price for all stocks: `get_all_share_index`


Table 1. Sample Data from the Global Beverage Corporation Exchange (EBCE)

|Stock Symbol	|Type         |	Last Dividend	|Fixed Dividend|	Par Value	|
|:-------------:|:-------------:|:-------------:|:-------------:|:-------------:|
|TEA          |	Common      |	0         	|             |	100	        |
|POP          |	Common      |	8	          |	            |100	        |
|ALE          |	Common      |	23          |		          |60	          |
|GIN          |	Preferred   |	8           |	0.02        |	100       	|
|JOE          |	Common      |	13	        |	            |250	        |


The following formulas are used:

- Dividend Yield:
  - Common Stock: <img src="https://render.githubusercontent.com/render/math?math=\frac{\text{Last Dividend}}{\text{Price}}">
  - Preferred Stock: <img src="https://render.githubusercontent.com/render/math?math=\frac{\text{Fixed Dividend} \times \text{Par Value}}{\text{Price}}">
- P/E Ratio (Common/Preferred):
  -  <img src="https://render.githubusercontent.com/render/math?math=\frac{\text{Price}}{\text{Dividend}}">
- Geometric Mean (Common/Preferred):
  -  <img src="https://render.githubusercontent.com/render/math?math=\sqrt{\left( p_1 p_2 \ldots p_n \right)}^\frac{1}{n}">   
- Volume Weighted Stock Price (Common/Preferred):
  -  <img src="https://render.githubusercontent.com/render/math?math=\frac{\sum_i(\text{Traded Price}_i \times \text{Quantity}_i)}{\sum_i \text{Quantity}_i}">

For an example of the output on sample data From Table 1 execute the following command:

````
$ python example_sample_data.py
````


## Requirements
The application has been developed in Python 3. 

The code is tested on Python 3.8. 

## Tests 

Tests can be found in `test.py`. To run the tests execute the following command:
````
$ python test.py
````