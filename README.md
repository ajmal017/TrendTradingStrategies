# Stock-Analysis-and-Methods
A module consisting of various methods used to predict stocks and corresponding statistical analyses thereof.

IndicatorsStrength.py:
Consist only of the the adx indicator and the vortex indicator.
This script would be used to implement a simple trading strategy: use the vortex indicator to evaluate whether the trend is bullish,
then use the adx indicator to evaluate whether the trend is strong--buy for one day and sell the next on the basis of a risk criteria, given by the textfile 'SearchCriteria.txt'
