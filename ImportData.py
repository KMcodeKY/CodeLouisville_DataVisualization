
# coding: utf-8

# In[1]:


import sqlite3
import pandas as pd
import numpy as np

#Compensation Change Import - Start
compChange = pd.read_excel("CompensationChange.xlsx", skiprows=15, usecols=['Year', 'Qtr1', 'Qtr2', 'Qtr3', 'Qtr4'])
compChange['Total'] = (compChange['Qtr1'] + compChange['Qtr2'] + compChange['Qtr3'] + compChange['Qtr4']).astype(float)
avgCompChange = compChange['Total'].mean()
#Compensation Change Import - End

#Variables Import - Start
stdVar = pd.read_excel("Variables.xlsx")
stdVar.loc[len(stdVar)] = ['Compensation Change', '', (avgCompChange / 100), '2017', '', 'Employment Cost Index-NAICS']
#print(stdVar)
#Variables Import - End

#Undergraduate Cost Import - Start
undCost = pd.read_excel("UndergraduateCost.xlsx", header=None, skiprows=6, skip_footer=3)
undCost = undCost.drop(undCost.columns[[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 18, 19, 20]], axis=1)
undCost.columns = ['Category', 'All_Institutions_2016']
undCost = undCost.drop(undCost[undCost.Category.str.contains("Tuition")==False].index)
undCost = undCost.dropna(subset=['Category'])
undCost = undCost[:-2]
undCost.iloc[-2, undCost.columns.get_loc('Category')] = "4-year institutions"
undCost.iloc[-1, undCost.columns.get_loc('Category')] = "2-year institutions"
#print(undCost)
#Undergraduate Cost Import - End

#Graduate Cost Import - Start
gradCost = pd.read_excel("GraduateCost.xlsx", header=None, skiprows=5, skip_footer=4)
gradCost = gradCost.drop(gradCost.columns[[2, 3, 4, 5, 6, 7, 8, 9, 10, 11]], axis=1)
gradCost.columns = ['Year', 'All_Institutions']
gradCost = gradCost.dropna(subset=['Year'])
gradCost = gradCost[:-27]

#Graduate Education Cost Change - For Doctoral Data - Start
eduGrad_2009 = gradCost.get_value(gradCost[gradCost.Year.str.contains("2008-09")].index[0], 'All_Institutions')
eduGrad_2010 = gradCost.get_value(gradCost[gradCost.Year.str.contains("2009-10")].index[0], 'All_Institutions')
eduGrad_2011 = gradCost.get_value(gradCost[gradCost.Year.str.contains("2010-11")].index[0], 'All_Institutions')
eduGrad_2012 = gradCost.get_value(gradCost[gradCost.Year.str.contains("2011-12")].index[0], 'All_Institutions')
eduGrad_2013 = gradCost.get_value(gradCost[gradCost.Year.str.contains("2012-13")].index[0], 'All_Institutions')
eduGrad_2014 = gradCost.get_value(gradCost[gradCost.Year.str.contains("2013-14")].index[0], 'All_Institutions')
eduGrad_2015 = gradCost.get_value(gradCost[gradCost.Year.str.contains("2014-15")].index[0], 'All_Institutions')
eduGrad_2016 = gradCost.get_value(gradCost[gradCost.Year.str.contains("2015-16")].index[0], 'All_Institutions')

eduChange = (eduGrad_2010 / eduGrad_2009) * (eduGrad_2011 / eduGrad_2010) * (eduGrad_2012 / eduGrad_2011) * (eduGrad_2013 / eduGrad_2012) * (eduGrad_2014 / eduGrad_2013) * (eduGrad_2015 / eduGrad_2014) * (eduGrad_2016 / eduGrad_2015)
#Graduate Education Cost Change - For Doctoral Data - End

gradCost = gradCost.drop(gradCost[gradCost.Year.str.contains("2015-16")==False].index)
gradCost.iloc[-1, gradCost.columns.get_loc('Year')] = "2016"
#print(gradCost)
#Graduate Cost Import - End

#Doctoral Cost Import - Start
docCost = pd.read_excel("DoctoralCost.xlsx", header=None, skiprows=5, skip_footer=6)
docCost = docCost.drop(docCost.columns[[2]], axis=1)
docCost.columns = ['Year','Average','Chiropractic', 'Dentistry','Medicine','Optometry','Osteopathic_Medicine','Pharmacy','Podiatry','Veterinary','Law','Theology']
docCost = docCost.drop(docCost[docCost.Year.str.contains("2008-09")==False].index)
docCost = docCost.dropna(subset=['Year'])
docCost = docCost[:-2]

#Doctoral Education Cost Change - Using Graduate Education Change - Start
docCost = docCost[['Average','Chiropractic', 'Dentistry','Medicine','Optometry','Osteopathic_Medicine','Pharmacy','Podiatry','Veterinary','Law','Theology']].multiply(eduChange, axis="index")
docCost.insert(loc=0, column='Year', value=['2016'])
#Doctoral Education Cost Change - Using Graduate Education Change - End
    
#print(docCost)
#Doctoral Cost Import - End

#Tuition Table - Start
tuiTable = pd.DataFrame(columns=['Degree','Type','Education_Years','Annual_Cost'])
tuiTable.loc[0] = ['No formal educational credential', 'All', 0, 0]
tuiTable.loc[1] = ['High school diploma or equivalent', 'All', 0, 0]
tuiTable.loc[2] = ['Some college, no degree', 'All', 1, undCost.get_value(undCost[undCost.Category.str.contains("2-year")].index[0], 'All_Institutions_2016')]
tuiTable.loc[3] = ['Postsecondary nondegree award', 'All', 1, undCost.get_value(undCost[undCost.Category.str.contains("2-year")].index[0], 'All_Institutions_2016')]
tuiTable.loc[4] = ['Associate\'s degree', 'All', 2, undCost.get_value(undCost[undCost.Category.str.contains("2-year")].index[0], 'All_Institutions_2016')]
tuiTable.loc[5] = ['Bachelor\'s degree', 'All', 4, undCost.get_value(undCost[undCost.Category.str.contains("4-year")].index[0], 'All_Institutions_2016')]
tuiTable.loc[6] = ['Master\'s degree', 'All', 6, gradCost.get_value(gradCost[gradCost.Year.str.contains("2016")].index[0], 'All_Institutions')]
tuiTable.loc[7] = ['Doctoral or professional degree', 'Average', 8, docCost.get_value(docCost[docCost.Year.str.contains("2016")].index[0], 'Average')]
tuiTable.loc[8] = ['Doctoral or professional degree', 'Chiropractic', 8, docCost.get_value(docCost[docCost.Year.str.contains("2016")].index[0], 'Chiropractic')]
tuiTable.loc[9] = ['Doctoral or professional degree', 'Dentistry', 8, docCost.get_value(docCost[docCost.Year.str.contains("2016")].index[0], 'Dentistry')]
tuiTable.loc[10] = ['Doctoral or professional degree', 'Advanced Dentistry', 10, docCost.get_value(docCost[docCost.Year.str.contains("2016")].index[0], 'Dentistry')]
tuiTable.loc[11] = ['Doctoral or professional degree', 'Medicine', 8, docCost.get_value(docCost[docCost.Year.str.contains("2016")].index[0], 'Medicine')]
tuiTable.loc[12] = ['Doctoral or professional degree', 'Optometry', 8, docCost.get_value(docCost[docCost.Year.str.contains("2016")].index[0], 'Optometry')]
tuiTable.loc[13] = ['Doctoral or professional degree', 'Pharmacy', 8, docCost.get_value(docCost[docCost.Year.str.contains("2016")].index[0], 'Pharmacy')]
tuiTable.loc[14] = ['Doctoral or professional degree', 'Podiatry', 8, docCost.get_value(docCost[docCost.Year.str.contains("2016")].index[0], 'Podiatry')]
tuiTable.loc[15] = ['Doctoral or professional degree', 'Veterinary', 8, docCost.get_value(docCost[docCost.Year.str.contains("2016")].index[0], 'Veterinary')]
tuiTable.loc[16] = ['Doctoral or professional degree', 'Law', 8, docCost.get_value(docCost[docCost.Year.str.contains("2016")].index[0], 'Law')]
#print(tuiTable)
#Tuition Table - End

def assign_misSal(row):
    if ('>=$208,000') in str(row['Median_Wage']):
        return stdVar.get_value(stdVar[stdVar.Category.str.contains(row['Employment_Title'],na=False)].index[0], 'Value') * ((1 + (avgCompChange/100))**(2016 - (stdVar.get_value(stdVar[stdVar.Category.str.contains(row['Employment_Title'],na=False)].index[0], 'Year'))))
    elif ('—') in str(row['Median_Wage']):
        return 99
    else:
        return row['Median_Wage']


#Employment Projection Import - Start
empProj = pd.read_excel("EmploymentProjections.xlsx", header=None, skiprows=3, skip_footer=4)
empProj.columns = ['Employment_Title', 'Matrix_Code', 'Occupation', 'Employment_2016', 'Employment_2026', 'Employment_Change_Number', 'Employment_Change_Percent', 'Self_Employed_Percent', 'Openings_2016_2026', 'Median_Wage', 'Education_Needed', 'Work_Experience', 'Job_Training']
empProj = empProj.drop(empProj[empProj.Occupation.str.contains("Summary")].index)
empProj = empProj.drop(empProj[empProj.Median_Wage==99].index)

empProj = empProj.assign(Median_Wage=empProj.apply (lambda row: assign_misSal (row),axis=1))
empProj.Median_Wage.dropna()
#print(empProj)
#Employment Projection Import - End

def assign_edu_fk (row):
    if row['Education_Needed'] != 'Doctoral or professional degree':
        return tuiTable.set_index('Degree').index.get_loc(row['Education_Needed'])
    elif row['Education_Needed'] == 'Doctoral or professional degree':
        test = str(row['Employment_Title']).lower()
        if ('chiropractor') in test:
            return tuiTable.set_index('Type').index.get_loc('Chiropractic')
        elif ('optometrist') in test:
            return tuiTable.set_index('Type').index.get_loc('Optometry')
        elif ('pharmacist') in test:
            return tuiTable.set_index('Type').index.get_loc('Pharmacy')
        elif ('podiatrist') in test:
            return tuiTable.set_index('Type').index.get_loc('Podiatry')
        elif ('veterinarian') in test:
            return tuiTable.set_index('Type').index.get_loc('Veterinary')
        elif any(x in test for x in ('orthodontist','prosthodontist')):            
            return tuiTable.set_index('Type').index.get_loc('Advanced Dentistry')
        elif ('dentist') in test:
            return tuiTable.set_index('Type').index.get_loc('Dentistry')
        elif any(x in test for x in ('lawyer','judge','judicial')):
            return tuiTable.set_index('Type').index.get_loc('Law')
        elif any(x in test for x in ('practitioner','pediatrician','psychiatrist','surgeon','psychologist','anesthesiologist','internist','gynecologist','audiologist','medical scientist','physical therapist')):
            return tuiTable.set_index('Type').index.get_loc('Medicine')
        else:
            return tuiTable.set_index('Type').index.get_loc('Average')
    else:
        return 999

def assign_resYears (row, rYears):
    if ((row['Education_Needed'] == "Doctoral or professional degree") and (row['Job_Training'] == 'Internship/residency')):
        return rYears
    else:
        return 0

def assign_inflow (row, tYear, careerYears, resSal):
    workYears = int(careerYears - row['Education_Years'] - row['Residency'])
    educationYears = int(row['Education_Years'])
    residencyYears = int(row['Residency'])
    midWorkYears = int(workYears/2)
    if tYear <= educationYears:
        return 0.0
    elif ((residencyYears > 0) and (tYear <= (educationYears + residencyYears))):
        return (resSal * ((1 + (avgCompChange/100))**(tYear)))
    else: 
        return ((row['Median_Wage'] * ((1 + (avgCompChange/100))**(careerYears-workYears+midWorkYears+1))) / ((1 + (avgCompChange/100))**(midWorkYears+1-(tYear-(careerYears-workYears)))))

def assign_outflow (row, tYear, careerYears, undTuition, tuitionChange, undRepay, grdRepay, undRate, grdRate):
    educationYears = int(row['Education_Years'])
    residencyYears = int(row['Residency'])
    
    if tYear <= educationYears or educationYears == 0:
        return 0.0
    elif row['Education_FK'] in [2, 3, 4, 5]:
        if tYear > (educationYears + undRepay):
            return 0.0
        else:
            tFactor = 0
            tempCount = 0
            while tempCount < educationYears:
                tFactor += ((1 + tuitionChange)**(tempCount+1))
                tempCount += 1
            totalTuition = tFactor * row['Annual_Cost']
            pmtFactor = (1-((1+(undRate/365))**(-(365*undRepay)))) / (undRate/365)
            pmtAnnual = (totalTuition / pmtFactor) * 365
            return -pmtAnnual
    else:
        if tYear > (educationYears + grdRepay):
            return 0.0
        else:
            tFactor = 0
            tempCount = 0
            while tempCount < 4:
                tFactor += ((1 + tuitionChange)**(tempCount+1))
                tempCount += 1
            totalUndTuition = tFactor * undTuition
            pmtUndFactor = (1-((1+(undRate/365))**(-(365*grdRepay)))) / (undRate/365)
            pmtUndAnnual = (totalUndTuition / pmtUndFactor) * 365        
            tFactor = 0
            while tempCount < educationYears:
                tFactor += ((1 + tuitionChange)**(tempCount+1))
                tempCount += 1
            totalGrdTuition = tFactor * row['Annual_Cost']
            pmtGrdFactor = (1-((1+(grdRate/365))**(-(365*grdRepay)))) / (grdRate/365)
            pmtGrdAnnual = (totalGrdTuition / pmtGrdFactor) * 365      
            pmtAnnual = pmtUndAnnual + pmtGrdAnnual
            return -pmtAnnual

def netPresentValue (row, tYear, discountRate):
    return ((row['CashInflow_' + str(2016 + tYear)] + row['CashOutflow_' + str(2016 + tYear)]) / ((1 + discountRate)**(tYear-1)))


def sum_NetPresentValue (row, careerYears):
    tempYear = 1
    total = 0
    while tempYear <= (careerYears):
        total += row['NetPresentValue_' + str(2016 + tempYear)]
        tempYear+=1
    return total
    
#Time Analysis - Start
undTuition = undCost.get_value(undCost[undCost.Category.str.contains("4-year")].index[0], 'All_Institutions_2016')
resYears = stdVar.get_value(stdVar[stdVar.Variable.str.contains("Residency")].index[0], 'Value').astype(int)
resSal = stdVar.get_value(stdVar[stdVar.Variable.str.contains("Average Residency Salary")].index[0], 'Value')
tuitionChange = stdVar.get_value(stdVar[stdVar.Variable.str.contains("Tuition Change")].index[0], 'Value')
undRepay = stdVar.get_value(stdVar[stdVar.Variable.str.contains("Undergraduate Repayment")].index[0], 'Value')
grdRepay = stdVar.get_value(stdVar[stdVar.Variable.str.contains("Graduate Repayment")].index[0], 'Value')
undRate = stdVar.get_value(stdVar[stdVar.Variable.str.contains("Undergraduate Loan Rate")].index[0], 'Value')
grdRate = stdVar.get_value(stdVar[stdVar.Variable.str.contains("Graduate Loan Rate")].index[0], 'Value')
careerYears = stdVar.get_value(stdVar[stdVar.Variable.str.contains("Career Years")].index[0], 'Value')
discountRate = stdVar.get_value(stdVar[stdVar.Variable.str.contains("Discount Rate")].index[0], 'Value')
desred_decimals = 2

timeAnalysis = empProj[['Employment_Title','Employment_2016', 'Employment_2026', 'Openings_2016_2026', 'Median_Wage', 'Education_Needed', 'Work_Experience', 'Job_Training']].copy()
timeAnalysis['Median_Wage'] = timeAnalysis['Median_Wage'].apply(lambda x: round(x,desred_decimals))
timeAnalysis = timeAnalysis.assign(Education_FK=timeAnalysis.apply (lambda row: assign_edu_fk (row),axis=1))
timeAnalysis = timeAnalysis.assign(Residency=timeAnalysis.apply (lambda row: assign_resYears (row, resYears),axis=1))
timeAnalysis = timeAnalysis.merge(tuiTable[['Education_Years','Annual_Cost']], left_on=['Education_FK'], right_index=True)

tYear = 1
while tYear <= (careerYears):
    timeAnalysis['CashInflow_' + str(2016 + tYear)] = timeAnalysis.apply (lambda row: assign_inflow (row,tYear,careerYears,resSal),axis=1)
    timeAnalysis['CashInflow_' + str(2016 + tYear)] = timeAnalysis['CashInflow_' + str(2016 + tYear)].apply(lambda x: round(x,desred_decimals))
    
    timeAnalysis['CashOutflow_' + str(2016 + tYear)] = timeAnalysis.apply (lambda row: assign_outflow (row,tYear,careerYears,undTuition,tuitionChange,undRepay,grdRepay,undRate,grdRate),axis=1)
    timeAnalysis['CashOutflow_' + str(2016 + tYear)] = timeAnalysis['CashOutflow_' + str(2016 + tYear)].apply(lambda x: round(x,desred_decimals))
    
    timeAnalysis['NetPresentValue_' + str(2016 + tYear)] = timeAnalysis.apply (lambda row: netPresentValue (row,tYear,discountRate),axis=1)
    timeAnalysis['NetPresentValue_' + str(2016 + tYear)] = timeAnalysis['NetPresentValue_' + str(2016 + tYear)].apply(lambda x: round(x,desred_decimals))
    tYear+=1
    
    
timeAnalysis = timeAnalysis.assign(Total_NetPresentValue=timeAnalysis.apply (lambda row: sum_NetPresentValue (row,careerYears),axis=1))
timeAnalysis['Total_NetPresentValue'] = timeAnalysis['Total_NetPresentValue'].apply(lambda x: round(x,desred_decimals))

timeAnalysis = timeAnalysis.drop('Work_Experience', 1)
timeAnalysis = timeAnalysis.drop('Job_Training', 1)
timeAnalysis = timeAnalysis.drop('Annual_Cost', 1)
    
#print(timeAnalysis)
#Time Analysis - End


#SQLITE Database setup - Start
conn = sqlite3.connect('employment_analysis.db')
cur = conn.cursor() 

timeAnalysis.to_sql('timeAnalysis', conn, if_exists='replace')
tuiTable.to_sql('tuitionCost', conn, if_exists='replace')
stdVar.to_sql('calculationVariables', conn, if_exists='replace')

cur.close()
conn.close()
#SQLITE Database setup - End