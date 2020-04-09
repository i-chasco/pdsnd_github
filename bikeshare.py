import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # Get user input for city (chicago, new york city, washington):

    city = ""
    while city not in ("chicago", "new york city", "washington"):
        try:
            city = input('Please tell me which city you are interested in exploring: (Chicago, New York City, Washington)\n').lower()
        except:
            print("There was a problem with the name of the city, please introduce 'Chicago', 'New York City' o 'Washington'\n")
    # Get user input for month (all, january, february, ... , june)
    month = ""
    while month.lower() not in ['all','january','february','march','april','may','june']:
        try:
            month = input('Please tell me the data of which month you want to see:\n (all, January, February, March, April, May, June)\n').lower()
        except:
            print("There was a problem with the name of the month, please introduce one of the following options:\n (all, January, February, March, April, May, June)\n")

    # Get user input for day of week (all, monday, tuesday, ... sunday)
    day = ""
    while day.lower() not in ['all','monday','tuesday','wednesday','thursday','friday','saturday','sunday']:
        try:
            day = input('Please tell me the data of which day you want to see:\n (all, Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday)\n').lower()
        except:
            print("There was a problem with the name of the day, please introduce one of the following options:\n (all, Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday)\n")



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

    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month_name()
    df['day_of_week'] = df['Start Time'].dt.weekday_name

    # filter by month if applicable
    if month != 'all':
        # filter by month to create the new dataframe
        df = df[df['month'] == month.title()]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # Display the most common month
    most_common_month = df['month'].mode()[0]
    print("The most common month to use the bikeshare service in this city in the selected period is {}".format(most_common_month))
    # Display the most common day of week
    most_common_weekday = df['day_of_week'].mode()[0]
    print("The most common day to use the bikeshare service in this city in the selectec period is {}".format(most_common_weekday))
    # Display the most common start hour
    most_common_hour = df['Start Time'].dt.hour.mode()[0]
    print("The most common hour to use the bikeshare service in this city in the selected period is {}".format(most_common_hour))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # Display most commonly used start station
    most_common_start_st = df['Start Station'].mode()[0]
    print("The most commonly used start station is: {}" .format(most_common_start_st))

    # Display most commonly used end station
    most_common_end_st = df['End Station'].mode()[0]
    print("The most commonly used end station is: {}" .format(most_common_end_st))

    # Display most frequent combination of start station and end station trip
    df['combination_stations'] = df['Start Station'] + " - " + df['End Station']
    most_common_combination = df['combination_stations'].mode()[0]
    print("The most frequent combination of start and end stations is: {}".format(most_common_combination))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    def convert_time(time_sec):
        '''Takes time in seconds and returns a string with time in hours, minutes and seconds'''
        time_hours = round(time_sec // 3600)
        time_mins = round((time_sec % 3600) // 60)
        time_seconds = round(((time_sec % 3600) % 60))

        return "{} hours, {} minutes and {} seconds".format(time_hours, time_mins, time_seconds)

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # Display total travel time
    total_time = df['Trip Duration'].sum()
    print('The total travel time for all the users during the selected period is: ' + convert_time(total_time))

    # Display mean travel time
    mean_time = df['Trip Duration'].mean()
    print("The mean travel time for the users during the selected period is: " + convert_time(mean_time))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    total_users = df['User Type'].count()
    print("The total users in this period were: {}\n\nThe users were divided as follows:\n".format(total_users))

    user_type_count = df['User Type'].value_counts()
    print(user_type_count)

    # Display counts of gender
    try:
        print("\nThis is how the users were divided, according to gender: \n")
        gender_count = df['Gender'].value_counts()
        print(gender_count)

    # if the user chose Washington as the city, we will have a KeyError because the
    # Washington database does not contain that information. Instead of the infotmation we
    # will display a message:
    except KeyError:
        print("There is no information on gender to display about Washington")


    # TO DO: Display oldest user, younguest, and most common year of birth
    try:
        oldest = round(df['Birth Year'].min())
        print("\nThe oldest user of the service was born in the year: {}".format(oldest))

        youngest = round(df['Birth Year'].max())
        print("The younguest user of the service was born in the year: {}".format(youngest))

        most_common = round(df['Birth Year'].mode()[0])
        print("The most common birth year between the users is: {}".format(str(most_common)[:4]))

    # if the user chose Washington as the city, we will have a KeyError because the
    # Washington database does not contain that information. Instead of the infotmation we
    # will display a message:
    except KeyError:
        print("There is no information on user age to display about Washington")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def raw_data(df):
    '''Ask the user to see 5 lines of raw data at a time every time the input is "yes". Stops when input is "no"'''
    more_rows = input("Do you want to see some raw single-trip data?: (Y)es/(N)o")
    first_display_row = 0
    while more_rows[0] != 'n':
        chunk = df.iloc[first_display_row : first_display_row+5]
        print(chunk)
        first_display_row += 5
        more_rows = input("Do you want to see 5 more lines of raw single-trip data?: (Y)es/(N)o")


def main():
    ''' Uses the previously defined functions to interactively explore
    US Bikeshare Databases'''
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        raw_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower()[0] != 'y':
            print("Thank you for using this app! And see you soon!")
            break


if __name__ == "__main__":
    main()
