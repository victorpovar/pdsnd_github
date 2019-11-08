import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

MONTHS = ['january', 'february', 'march', 'april', 'may', 'june']
DAY_OF_THE_WEEK = ['sunday', 'monday', 'tuesday', 'wednedsay', 'thursday', 'friday', 'saturday']
NYC = ['new york', "new york city", "ny", "nyc"]
CHICAGO = ['chicago', 'chicago il', 'chicago, il', 'chi']
WASHINGTON = ['washington', 'dc', 'washington dc', 'washington, dc', 'was']

def validation(question_text, valid_values):
    """
    Collects the user input and validations against the provided list
    """

    while True:
        print (question_text)
        user_input = input().lower()
        if (user_input == 'all' or user_input in valid_values):
            return user_input
        else:
            print ("Your entry was not recognized. Please provide a valid input.")


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')

    # get user input for city (chicago, new york city, washington).
    while 1:
        print('What city would you like to use for data exploration? (Chicago, New York or Washington)')
        city = input ().lower()
        if (city in WASHINGTON):
            city = 'washington'
            break
        elif (city in NYC):
            city = 'new york city'
            break
        elif (city in CHICAGO):
            city = 'chicago'
            break
        else:
            print ("Your entry was not recognized. Please provide a valid input.")

    # get user input for month (all, january, february, ... , june)
    month = validation ('What month would you like to use for data exploration? (all, january, february, ... , june)', MONTHS)

    # get user input for day of week (all, monday, tuesday, ... sunday)
    day = validation ('What day of the week would you like to use for data exploration? (all, monday, tuesday, ... sunday)', DAY_OF_THE_WEEK)

    print('-'*40)
    return city, month, day


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
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week and hour from Start Time to create new columns
    df['month'] =  df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    df['hour'] = df['Start Time'].dt.hour
    df ['start_end_station'] =  df ['Start Station'] +' - ' + df ['End Station']

    # filter by month if applicable
    if month != 'all':
        # use the index of the MONTHS list to get the corresponding int
        month = MONTHS.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df ['month'] == month]

    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df ['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    print ('The most common month is: {}'.format (MONTHS[int(df['month'].mode()[0])-1]).title())

    # display the most common day of week
    print ('The most common day of the week is: {}'.format (df['day_of_week'].mode()[0]))

    # display the most common start hour
    print ('The most common hour for rental starts is: {}'.format(df['hour'].mode()[0]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    print ('The most common start station is: {}'.format (df['Start Station'].mode()[0]))

    # display most commonly used end station
    print ('The most common end station is: {}'.format (df['End Station'].mode()[0]))

    # display most frequent combination of start station and end station trip
    print ('The most common combination of start and end station is: {}'.format (df['start_end_station'].mode()[0]))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    print ('The total travel time is: {}'.format (df['Trip Duration'].sum()))

    # display mean travel time
    print ('The average travel time is: {}'.format (df['Trip Duration'].mean()))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print ('The counts for each user type are:')
    print (df["User Type"].value_counts())
    print ()

    # Display counts of gender
    try:
        print ('The counts for each gender are:')
        print (df["Gender"].value_counts())
        print ()
    except KeyError:
        print ('There is no gender information in this file')

    # Display earliest, most recent, and most common year of birth
    try:
        print ('The earliest year of birth is: {}'.format (int(df['Birth Year'].min())))
        print ('The most recent year of birth is: {}'.format (int(df['Birth Year'].max())))
        print ('The most common year of birth is: {}'.format (int(df['Birth Year'].mode()[0])))
    except KeyError:
        print ('There is no birth year information in this file')
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def print_filtered_data (df, start, increment):
    """Print data within the dataframe based on the passed start position and by the specified increment."""

    print (df[start:increment])

    while True:
        print ('Would you to see more data?')
        response = input().lower()
        if (response == "yes"):
            start = start + 5
            print (df[start:start+increment])
        else:
            break

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        print_filtered_data (df, 0, 5)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
