#!/usr/bin/env python
# coding: utf-8

# In[1]:


import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york': 'new_york_city.csv',
              'washington': 'washington.csv' }


# In[2]:


def month_input():
    """
    Asks user to specify month

    Returns:
        (str) month
    """

    # get user input for month (all, january, february, ... , june)
    month = input("\nWhich month do you want?\nAvalible inputs: (all, January, February, March, April, May, June)\n").title().rstrip().lstrip()

    while month not in ['All', 'January', 'February', 'March', 'April', 'May', 'June']:
        print('invaild input...'.upper() + "Please choose one of these Options :\n(all, January, February, March, April, May, June)\n")
        month = input().title().rstrip().lstrip()
    return month.lower()


def day_input():
    """
    Asks user to specify day

    Returns:
        (str) day
    """

    # get user input for day of week (all, monday, tuesday, ... sunday)
    day = input("\nWhich day do you want?\nAvalible inputs: (all, Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday)\n").title().rstrip().lstrip()

    while day not in ['All', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']:
        print('invaild input...'.upper() + "Please choose one of these Options :\n(all, Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday)\n")
        day = input().title().rstrip().lstrip()
    return day.lower()


# In[3]:


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington)
    city = input("Which country do you want to know Information about?\n ( Chicago, New York or Washington )\n").lower().rstrip().lstrip()

    while city not in ['chicago', 'new york', 'washington']:
        print('invaild input...'.upper() + "Please choose one of these countries : ( Chicago , New York , Washington )")
        city = input('\n').lower().rstrip().lstrip()

    # filter options
    for_filter = input("Do you want to filter the data by month, day, both or none of them?\n Avalible inputs: ( month , day , both , none )\n").lower().rstrip().lstrip()
    while for_filter not in ['month', 'day','both', 'none']:
        print('invaild input...'.upper() + "Please choose one of these Options : ( month , day , both , none )")
        for_filter = input('\n').lower().rstrip().lstrip()

    if for_filter == 'month':
        month = month_input()
        day = None
    elif for_filter == 'day':
        month = None
        day = day_input()
    elif for_filter == 'none':
        month = None
        day = None
    elif for_filter == 'both':
        month = month_input()
        day = day_input()

    print('-'*40)

    return [city, month, day]


# In[ ]:





# In[4]:


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """

      # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'],errors='coerce')
    df['End Time'] = pd.to_datetime(df['End Time'],errors='coerce')
    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()
        #creating 'hour' column in data
    df['hour'] = df['Start Time'].dt.hour
    df_original = df

    # filter by month if applicable
    if month not in ['all', None]:
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day not in ['all', None]:
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]



    return df,df_original


# In[5]:


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    most_m = df['month'].mode()[0]
    lis = ['january', 'february', 'march', 'april', 'may', 'june']

    print(f"Most common month:    {lis[most_m-1]}")

    # display the most common day of week
    print(f"Most common day:    {df['day_of_week'].mode()[0]}")

    # display the most common start hour
    print(f"Most common start hour:    {df['hour'].mode()[0]}")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


# In[6]:


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    print(f"Most common start start station:    {df['Start Station'].mode()[0]}")

    # display most commonly used end station
    print(f"Most common start end station:    {df['End Station'].mode()[0]}")

    # display most frequent combination of start station and end station trip
    df['Combination'] ='Start station "' + df['Start Station'] + '" and End station "' + df['End Station']+'"'
    print(f"Most frequent combination of start station and end station: {df['Combination'].mode()[0]}")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


# In[7]:


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()
    df['Travel Time'] = pd.to_numeric(((df['End Time'].apply(pd.Timestamp)  - df['Start Time'].apply(pd.Timestamp)).dt.total_seconds()/60).round(),downcast='integer')

    # display total travel time
    print(f"The total travel time:    {df['Travel Time'].sum()} minutes")

    # display mean travel time
    print(f"The average traval time:    {int(df['Travel Time'].mean().round())} minutes")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


# In[8]:


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    try:
        print("\nCounts of User types:\n" +df['User Type'].value_counts().to_string())
    except:
        print('\nUser type data is not provided for this city\n')

    # Display counts of gender
    try:
        print("\nCounts of gender:\n" + df['Gender'].value_counts().to_string())

    except:
        print('\nGENDER data is not provided for this city\n')

    # Display earliest, most recent, and most common year of birth
    try:
        print(f"\nEarlist year of birth: {int(df['Birth Year'].min())}")

        #if df[df['End Time']==df['End Time'].max()]['Birth Year'].isnull().values:
            #print("Most recent year of birth: 'birth year for the recent user is not provided in this data'")

        #else:
        print(f"Most recent year of birth: {int(df['Birth Year'].max())}")
        print(f"Most common year of birth: {int(df['Birth Year'].mode()[0])}")


    except:
        print('\nBirth data is not provided for this city\n')


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


# In[9]:


def print_rows(df):
    """
    askes the user if he want to see 5 columns for n times in his filterd data
    """
    pd.set_option('display.max_rows', None)
    pd.set_option('display.max_columns', None)
    pd.set_option('display.width', 1000)
    pd.set_option('display.colheader_justify', 'center')
    pd.set_option('display.precision', 3)


    #get if user wants to see 5 raws or not
    inp = input("Do you want see 5 rows of the raw data? Yes or No    ").title().rstrip().lstrip()
    while inp not in ['Yes', 'No']:
        print('invaild input...'.upper() + "Please choose one of these Options :\n( Yes , No )\n")
        inp = input().title().rstrip().lstrip()

    try:
        if inp == "Yes" :
            #setting the loop parameters
            i = 1
            end = np.ceil(df.shape[0]/5)
            while i <= end:
                if i != end :
                    #printing 5 raws of data
                    display(df.iloc[range(5*(i-1),5*i,1)])
                    print('\n')
                else:
                    #if i is equal to end the functions prints the last rows and breaks the loop
                    display(df.iloc[range(5*(i-1), df.shape[0])])
                    print("\nthere is no more data to show+ \n".upper())
                    break
                #see if the user wants to see another 5 rows
                inp = input("Do you want see more 5 rows of the raw data? Yes or No    ").title().rstrip().lstrip()
                while inp not in ['Yes', 'No']:
                    print('invaild input...'.upper() + "Please choose one of these Options :\n( Yes , No )\n")
                    inp = input().title().rstrip().lstrip()

                if inp == 'Yes':
                    i += 1
                    continue
                else:
                    break
    except:
        if inp == "Yes" :
            #setting the loop parameters
            i = 1
            end = np.ceil(df.shape[0]/5)
            while i <= end:
                if i != end :
                    #printing 5 raws of data
                    print(df.iloc[range(5*(i-1),5*i,1)])
                    print('\n')
                else:
                    #if i is equal to end the functions prints the last rows and breaks the loop
                    print(df.iloc[range(5*(i-1), df.shape[0])])      
                    print("\nthere is no more data to show+ \n".upper())
                    break
                #see if the user wants to see another 5 rows
                inp = input("Do you want see more 5 rows of the raw data? Yes or No    ").title().rstrip().lstrip()
                while inp not in ['Yes', 'No']:
                    print('invaild input...'.upper() + "Please choose one of these Options :\n( Yes , No )\n")
                    inp = input().title().rstrip().lstrip()

                if inp == 'Yes':
                    i += 1
                    continue
                else:
                    break



# In[10]:


def main():
    while True:
        city, month, day = get_filters()
        df,df_org = load_data(city, month, day)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        print_rows(df)
        restart = input('\nWould you like to restart? Enter yes or no.\n').title().rstrip().lstrip()
        while restart not in ['Yes', 'No']:
                print('invaild input...'.upper() + "Please choose one of these Options :\n( Yes , No )\n")
                restart = input().title().rstrip().lstrip()
        print('_'*100 +'\n\n')
        if restart.lower() != 'yes':
            break



if __name__ == "__main__":
	main()
