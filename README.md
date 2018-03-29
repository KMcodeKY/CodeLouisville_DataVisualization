# CodeLouisville_DataVisualization

This project was set up to utilize a Bureau of Labor Statistics [employment projections file](https://data.bls.gov/projections/occupationProj) to calculate the estimated net present value of each position type. My hypothesis was that medical positions would carry a higher net present value even after the higher education costs. To visualize my results, I thought that a bar graph where the bars are each position type and ranked in descending order based on total net present value. I thought using a hover display would help to show the position types (which can be wordy) as well as the total net present value and the education and residency years. Additionally, a slider widget was used to dynamically show more or fewer columns.

## Data assumptions included:
* the time series analysis was calculated assuming 45 years (total years for education and working/earning) starting with the year 2017
* for those positions that originally had a median salary of '>=208,000' in the employment projection file, I utilized the individual career profiles on the Bureau of Labor Statistics site to find these specific median salaries. Examples include [physicians and surgeons](https://www.bls.gov/ooh/healthcare/physicians-and-surgeons.htm#tab-5), [oral surgeons](https://www.bls.gov/oes/current/oes291022.htm), and [orthodondists](https://www.bls.gov/oes/current/oes291023.htm#nat)
* that all education costs were borrowed and average [associates](https://nces.ed.gov/programs/digest/d16/tables/dt16_330.40.asp?current=yes), [undergraduate](https://nces.ed.gov/programs/digest/d16/tables/dt16_330.40.asp?current=yes), [graduate](https://nces.ed.gov/programs/digest/d16/tables/dt16_330.50.asp?current=yes), and [doctoral/professional](https://nces.ed.gov/programs/digest/d10/tables/dt10_348.asp) tuition rates were used
* that education costs were paid back according to federal [interest rates](https://studentaid.ed.gov/sa/types/loans/interest-rates) and average [repayment years](https://studentaid.ed.gov/sa/repay-loans/understand/plans)
* that tuition would escalate each year calculated using the available 5 year average of a [constant dollar comparison](https://nces.ed.gov/programs/digest/d16/tables/dt16_330.40.asp?current=yes)
* that compensation would escalate each year calculated using a 10 year average of the [employment cost index](https://nces.ed.gov/programs/digest/d16/tables/dt16_330.40.asp?current=yes)
* based on the availablity of data variables by year (ex: doctoral/professional tuition), these were escalated appropriately by analysis year
* For those medical and advanced dentistry occupations that required a residency (as indicated in the employment projections file) I utilized [average residency years and salary](https://www.medscape.com/features/slideshow/public/residents-salary-and-debt-report-2016#page=2)
* that the median salary in the projection file was assumed to be earned at the midpoint of working years (escalated appropriately)
* that the discount rate in the net present value calculation would be the [30 year Treasury rate](https://www.treasury.gov/resource-center/data-chart-center/interest-rates/Pages/TextView.aspx?data=yield) as of 3/27/18

## Running the program
To run the analysis, download all files to the same folder location. The program has been written in a jupyter notebook, which requires jupyter, pandas, bokeh and the python3 language.

1. Jupyter can be started from the console by typing (and navigating to the folder location to open the jupyter notebook):
>jupyter notebook

Once the jupyter environment has been opened navigate to the folder where all of the files have been saved and open the 'Employment_NPV_Notebook.ipynb' jupyter notebook. The notebook can be run by selecting Cell -> Run All. When the program has finished running in the Kernel the 'employment_analysis.db' and 'Employment_NPV_Analysis.html' files will show an updated date and time in the folder where all of the files were saved. Open the Employment_NPV_Analysis.html file in a browser (utilize the slider to narrow or expand the number of columns/positions displayed and the hover functionality to see the position information, positions have been arranged in descending order based on the total net present value).

2. The jupyter notebook can be run from the console (after navigating to the folder location where all of the files have been saved) by typing:
>jupyter nbconvert --to notebook --execute Employment_NPV_Notebook.ipynb

When the program has finished running the 'employment_analysis.db' and 'Employment_NPV_Analysis.html' files will show an updated date and time in the folder where all of the files were saved. Open the Employment_NPV_Analysis.html file in a browser (utilize the slider to narrow or expand the number of columns/positions displayed and the hover functionality to see the position information, positions have been arranged in descending order based on the total net present value).
