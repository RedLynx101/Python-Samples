# Noah Hicks
# November 2023
# A program to keep and use all of my functions for N/N, C/N, and C/C relationships using Pandas and Seaborn on CSV files.
#   Allows me to use the functions in a console window, edit and save csv files, and link csv files.
#   Also allows me to use some AI tools to help me with my analysis.
#   This file mainly hosts the menu system and the functions that are used in the menu system.
#   The functions that are used in the menu system are in the AnalysisCorrelationFunctions.py file.

import pandas as pd
from AnalysisCorrelationFunctions import *

CSV = 'https://www.dropbox.com/s/5y9r6gq3egszjnc/MovieData.csv?dl=1' # Link to the CSV file DEBUG

# Main menu has main function sections. Each section has a sub menu with the functions for that section. 
#   All sub menues are able to go back to the main menu.

# Structure:

# Main Menu
#   DF Info
#   N/N
#   C/N
#   C/C
#   Data Wrangling
#     +---Change Column Names
#     +---Change column data types
#     +---Means for colomns, along with ranges, and other info. Also tied to categories as an option. df.describe() or df['age'].describe()
#     +---Show unique column values df.age.nunique() and df.age.unique()
#   Reset DF
#   Exit

# Main Menu
def mainMenu(df):
    while True:
        print('----------------------------------------\nMain Menu')
        print('1. DF Info')
        print('2. N/N')
        print('3. C/N')
        print('4. C/C (WIP)')
        print('5. Data Wrangling')
        print('6. CSV Management')
        print('7. Reset DF')
        print('8. Exit')

        # Try to get the user's choice. Error message if it is recursive from bad functions calling mainMenu() instead of returning.
        try:
            choice = input('Enter the number of the function you would like to use: ')
        except Exception as e:
            print("\nExiting program. (Likely Recursive) Error: " + str(e))
            return  # Exit the function

        if choice == '1':
            DFInfo(df)
        elif choice == '2':
            NNMenu(df)
        elif choice == '3':
            CNMenu(df)
        elif choice == '4':
            CCMenu(df)
        elif choice == '5':
            df = DWMenu(df)
        elif choice == '6':
            df = CSVMenu(df)
        elif choice == '7':
            df = resetDF()
        elif choice == '8':
            try:
                print("Exiting program.")
                exit(0)  # Exit the program
            except Exception as e:
                print("\nExiting program. Exit Error: " + str(e))
                exit(0)  # Exit the program
        else:
            print('Invalid Input')
            mainMenu(df)


# Column Name Code
def getColumnNames(df):
    try:
        col_names = df.columns.tolist()
        col_types = df.dtypes.tolist()
        for i, (name, dtype) in enumerate(zip(col_names, col_types)):
            print(f"{i+1}. {name} ({dtype})")
        return col_names
    except Exception as e:
        print(f"An error occurred while getting the column names: {e}")
        return None


def getUserColumn(df, prompt):
    try:
        col_names = getColumnNames(df)
        choice = int(input(prompt)) - 1  # Subtract 1 to match list index
        if choice >= 0 and choice < len(col_names):
            return col_names[choice]
        else:
            print("Invalid choice. Please try again.")
            return getUserColumn(df, prompt)
    except Exception as e:
        print(f"An error occurred while getting the column: {e}")
        return None


# Column Name by Type Code
def getColumnNamesByType(df, dtype_filter=None):
    try:
        col_names = df.columns.tolist()
        col_types = df.dtypes.tolist()
        filtered_names = []
        for i, (name, dtype) in enumerate(zip(col_names, col_types)):
            if dtype_filter is None or dtype == dtype_filter:
                print(f"{len(filtered_names) + 1}. {name} ({dtype})")
                filtered_names.append(name)
        return filtered_names
    except Exception as e:
        print(f"An error occurred while getting the column names: {e}")
        return None

def getUserColumnByType(df, prompt, dtype_filter=None):
    try:
        col_names = getColumnNamesByType(df, dtype_filter)
        choice = int(input(prompt)) - 1  # Subtract 1 to match list index
        if choice >= 0 and choice < len(col_names):
            return col_names[choice]
        else:
            print("Invalid choice. Please try again.")
            return getUserColumnByType(df, prompt, dtype_filter)
    except Exception as e:
        print(f"An error occurred while getting the column: {e}")
        return None


# Column Category Code
def getUserCategory(df, column_name, prompt):
    try:
        unique_categories = df[column_name].unique().tolist()
        for i, category in enumerate(unique_categories):
            print(f"{i+1}. {category}")
        choice = int(input(prompt)) - 1  # Subtract 1 to match list index
        if choice >= 0 and choice < len(unique_categories):
            return unique_categories[choice]
        else:
            print("Invalid choice. Please try again.")
            return getUserCategory(df, column_name, prompt)
    except Exception as e:
        print(f"An error occurred while getting the category: {e}")
        return None


# N/N Menu
def NNMenu(df):
    while True:
        print('----------------------------------------\nN/N Menu')
        print('1. Print R, P, and R Squared Values (With Means)')
        print('2. Output a 2D Scatter Plot with a Linear Regression Line')
        print('3. Correlation Matrix')
        print('4. 4D Scatter Plot')
        print('5. Back')

        choice = input('Enter the number of the function you would like to use: ')

        if choice == '1':
            Col1 = getUserColumnByType(df, 'Enter the number for the first numeric column: ', 'int64')
            Col2 = getUserColumnByType(df, 'Enter the number for the second numeric column: ', 'int64')
            NNBiRelationship(df, Col1, Col2)
        elif choice == '2':
            Col1 = getUserColumnByType(df, 'Enter the number for the first numeric column: ', 'int64')
            Col2 = getUserColumnByType(df, 'Enter the number for the second numeric column: ', 'int64')
            Title = input('Enter the title of the scatter plot: ')
            ScatterPlot(df, Col1, Col2, Title)
        elif choice == '3':
            Col1 = getUserColumnByType(df, 'Enter the number for the main numeric column: ', 'int64')
            NNCorrMatrix(df, Col1)
        elif choice == '4':
            Col1 = getUserColumnByType(df, 'Enter the number for the first numeric column: ', 'int64')
            Col2 = getUserColumnByType(df, 'Enter the number for the second numeric column: ', 'int64')
            Col3 = getUserColumnByType(df, 'Enter the number for the third numeric column: ', 'int64')
            Col4 = getUserColumnByType(df, 'Enter the number for the fourth numeric column: ', 'int64')
            Title = input('Enter the title of the graph: ')
            NN4d(df, Col1, Col2, Col3, Col4, Title)
        elif choice == '5':
            return
        else:
            print('Invalid Input')


# C/N Menu
def CNMenu(df):
    while True:
        print('----------------------------------------\nC/N Menu')
        print('1. T-Test and Means')
        print('2. ANOVA Test with Tukey')
        print('3. BarPlot')
        print('4. BarPlot with Hue')
        print('5. Back')

        choice = input('Enter the number of the function you would like to use: ')

        if choice == '1':
            CatColumn = getUserColumnByType(df, 'Enter the number for the categorical column: ', 'object')
            Cat1 = getUserCategory(df, CatColumn, 'Enter the number for the first category: ')
            Cat2 = getUserCategory(df, CatColumn, 'Enter the number for the second category: ')
            NumColumn = getUserColumnByType(df, 'Enter the number for the numeric column: ', 'int64')
            TTest(df, CatColumn, Cat1, Cat2, NumColumn)
        elif choice == '2':
            CatColumn = getUserColumnByType(df, 'Enter the number for the categorical column: ', 'object')
            NumColumn = getUserColumnByType(df, 'Enter the number for the numeric column: ', 'int64')
            ANOVATest(df, CatColumn, NumColumn)
        elif choice == '3':
            CatColumn = getUserColumnByType(df, 'Enter the number for the categorical column: ', 'object')
            NumColumn = getUserColumnByType(df, 'Enter the number for the numeric column: ', 'int64')
            Title = input('Enter the title of the graph: ')
            BarPlot(df, CatColumn, NumColumn, Title)
        elif choice == '4':
            CatColumn = getUserColumnByType(df, 'Enter the number for the categorical column: ', 'object')
            NumColumn = getUserColumnByType(df, 'Enter the number for the numeric column: ', 'int64')
            HueColumn = getUserColumn(df, 'Enter the number for the hue column: ')
            Title = input('Enter the title of the graph: ')
            BarPlotHue(df, CatColumn, NumColumn, HueColumn, Title)
        elif choice == '5':
            return
        else:
            print('Invalid Input')

# C/C Menu
def CCMenu(df):
    while True:
        print('----------------------------------------\nC/C Menu')
        print('1. Pearson Chi-Square Test')
        print('2. Crosstab Analysis with Expected Values')
        print('3. Crosstab Analysis with Observed Values')
        print('4. Crosstab Analysis with Observed Values as Percentages')
        print('5. Back')

        choice = input('Enter the number of the function you would like to use: ')

        if choice == '1':
            Cat1 = getUserColumnByType(df, 'Enter the number for the first categorical column: ', 'object')
            Cat2 = getUserColumnByType(df, 'Enter the number for the second categorical column: ', 'object')
            ChiSquare(df, Cat1, Cat2)
        elif choice == '2':
            Cat1 = getUserColumnByType(df, 'Enter the number for the first categorical column: ', 'object')
            Cat2 = getUserColumnByType(df, 'Enter the number for the second categorical column: ', 'object')
            Title = input('Enter the title of the graph: ')
            CrosstabExpected(df, Cat1, Cat2, Title)
        elif choice == '3':
            Cat1 = getUserColumnByType(df, 'Enter the number for the first categorical column: ', 'object')
            Cat2 = getUserColumnByType(df, 'Enter the number for the second categorical column: ', 'object')
            Title = input('Enter the title of the graph: ')
            CrosstabObserved(df, Cat1, Cat2, Title)
        elif choice == '4':
            Cat1 = getUserColumnByType(df, 'Enter the number for the first categorical column: ', 'object')
            Cat2 = getUserColumnByType(df, 'Enter the number for the second categorical column: ', 'object')
            Title = input('Enter the title of the graph: ')
            CrosstabObservedPercent(df, Cat1, Cat2, Title)
        elif choice == '5':
            return
        else:
            print('Invalid Input')


# Data Wrangling Menu
def DWMenu(df):
    while True:
        print('----------------------------------------\nData Wrangling Menu')
        print('1. DF Info')
        print('2. Delete Column')
        print('3. Delete Column Nulls')
        print('4. Change Column Name')
        print('5. Change Column Data Type')
        print('6. Column Data Info (Range, Mean, etc.)')
        print('7. Show unique column values/How many unique values')
        print('8. Show Histplot for Column')
        print('9. Show Histplot for Column with Hue')
        print('10. (WIP) Merge DFs from CSV files on Same Column Name')
        print('11. Back')
        # Add in a menu for dataframe 1 and 2 for merging.

        choice = input('Enter the number of the function you would like to use: ')

        if choice == '1':
            DFInfo(df)
        elif choice == '2':
            Col1 = getUserColumn(df, 'Enter the number for the column: ')
            df = deleteColumn(df, Col1)
        elif choice == '3':
            Col1 = getUserColumn(df, 'Enter the number for the column: ')
            df = deleteColumnNulls(df, Col1)
        elif choice == '4':
            Col1 = getUserColumn(df, 'Enter the number for the column: ')
            Name = input('Enter the new name for the column: ')
            df = changeColumnName(df, Col1, Name)
        elif choice == '5':
            Col1 = getUserColumn(df, 'Enter the number for the column: ')
            Type = selectDataType()
            changeColumnType(df, Col1, Type)
        elif choice == '6':
            Col1 = getUserColumn(df, 'Enter the number for the column: ')
            columnDataStats(df, Col1)
        elif choice == '7':
            Col1 = getUserColumn(df, 'Enter the number for the column: ')
            columnData(df, Col1)
        elif choice == '8':
            Col1 = getUserColumn(df, 'Enter the number for the column: ')
            histPlot(df, Col1)
        elif choice == '9':
            Col1 = getUserColumn(df, 'Enter the number for the column: ')
            Hue = getUserColumn(df, 'Enter the number for the hue column: ')
            histPlotHue(df, Col1, Hue)
        elif choice == '10':
            print('***This functionality is WIP***')
            df = mergeDataframes()
        elif choice == '11':
            return df
        else:
            print('Invalid Input')

# Initialize/Reset DF
def resetDF():
    try:
        global CSV
        df = pd.read_csv(CSV)
        print('------------Data Frame Reset------------')
        return df  # Return the DataFrame
    except Exception as e:  # Catch any exception and print it
        print(f'An error occurred while resetting the data frame: {e}')
        return None  # Return None if an error occurs
    

# Show all of CSV files that are in the current directory. 
#  Allow the user to select one of the CSV files to use.
#  Allow the user to save a current df to a digital df. 
# Other things.
def CSVMenu(df):
    while True:
        print('----------------------------------------\nCSV Menu')
        print('1. Show all CSV files in the current directory')
        print('2. Load a CSV file to use from the current directory')
        print('3. Load a CSV file from a link')
        print('4. Save the current df to a CSV file')
        print('5. Back')

        choice = input('Enter the number of the function you would like to use: ')

        if choice == '1':
            showCSVFiles()
        elif choice == '2':
            df = selectCSVFile()
        elif choice == '3':
            global CSV
            CSV = input('Enter the link for the CSV file: ')
            df = importCSV(CSV)
        elif choice == '4':
            name = input('Enter the name of your new csv file: ')
            exportCSV(df, name)
        elif choice == '5':
            return df
        else:
            print('Invalid Input')


# Start Program, create df
df = resetDF()  # Creates the data frame
if df is not None:
    mainMenu(df)
else:
    print("Could not initialize DataFrame. Exiting.")