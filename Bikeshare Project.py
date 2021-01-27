import time
import pandas as pd
import numpy as np

CITY_DATA = {'chicago': 'chicago.csv',
             'new york city': 'new_york_city.csv',
             'washington': 'washington.csv'}


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.
    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = ''
    while city not in CITY_DATA.keys():
        print('Washington\nNew York City\nChicago')
        city = input('Please Choose a city from above to view it\'s data!').lower()
        if city not in CITY_DATA.keys():
            print('\nPlease Enter one of the cities mentioned above\n')
            continue

    # get user input for month (all, january, february, ... , june)
    months = ['January', 'February', 'March', 'April', 'May', 'June']
    print('The data is available for the following months\n{}'.format(months))
    month = ''
    while month not in months:
        month = input('Please Enter a month ').title()
        if month not in months:
            print('Please Enter a month of the mentioned above')
            continue

    # get user input for day of week (all, monday, tuesday, ... sunday)
    days = ['all', 'Saturday', 'Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
    print('The data is available for the following days\n{}'.format(days))
    day = ''
    while day not in days:
        day = input('Please Enter the day you want to data to be filtered in').title()
        if day not in days:
            print('Please Enter a day of the mentioned above')
            continue
    print('\nWe are viewing data for the day {} in month {} in {}\n'.format(day, month, city))

    print('-' * 40)
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
    # reading the data from the file
    df = pd.read_csv(CITY_DATA[city])
    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()
    # extract hour from the Start Time column to create an hour column
    df['hour'] = df['Start Time'].dt.hour

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['January', 'February', 'March', 'April', 'May', 'June']
        month = months.index(month) + 1
        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    common_month = df['month'].mode()[0]

    # display the most common day of week
    common_day = df['day_of_week'].mode()[0]

    # display the most common start hour
    common_hour = df['hour'].mode()[0]
    # display the count of the most common start hour
    hour_count = df['hour'].value_counts()[common_hour]
    print('{} is the most common hour as it was counted {} times!'.format(common_hour, hour_count))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station and its count
    common_start_station = df['Start Station'].mode()[0]
    ss_count = df['Start Station'].value_counts()[common_start_station]
    print('{} is the most commonly used start station as it was counted {} times!'.format(common_start_station, ss_count))
    # display most commonly used end station and its count
    common_end_station = df['End Station'].mode()[0]
    es_count = df['End Station'].value_counts()[common_end_station]
    print('{} is the most commonly used end station as it was counted {} times!'.format(common_end_station, es_count))

    # display most frequent combination of start station and end station trip and its count
    df['Start to End Station'] = df['Start Station'].str.cat(df['End Station'], sep='-->')
    common_start_to_end = df['Start to End Station'].mode()[0]
    ste_count = df['Start to End Station'].value_counts()[common_start_to_end]
    print('{} is the most commonly used trip line as it was counted {} times!'.format(common_start_to_end, ste_count))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_tt = df['Trip Duration'].sum()
    t_hours = total_tt / 3600
    t_minutes = (total_tt % 3600) / 60
    t_seconds = (total_tt % 3600) % 60
    print('The total travel time in {} hours, {} minutes and {} seconds'.format(int(t_hours), int(t_minutes), int(t_seconds)))

    # display mean travel time
    mean_tt = df['Trip Duration'].mean()
    m_hours = mean_tt / 3600
    m_minutes = (mean_tt % 3600) / 60
    m_seconds = (mean_tt % 3600) % 60
    if m_hours <1:
        print('The mean travel time is {} minutes and {} seconds'.format(int(m_minutes), int(m_seconds)))
    else:
        print('The mean travel time is {} minutes and {} seconds'.format(int(m_hours), int(m_minutes), int(m_seconds)))
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_type_count = df['User Type'].value_counts()
    print('The counts of user types are :\n\n{}'.format(user_type_count))
    try:
        # Display counts of gender
        gender_count = df['Gender'].value_counts()
        print('The counts of Gender are :\n\n{}'.format(gender_count))
    except:
        print('There is no "Gender" data in this city file')

    try:
        # Display earliest, most recent, and most common year of birth
        earliest_year = df['Birth Year'].min()
        recent_year = df['Birth Year'].max()
        common_year = df['Birth Year'].mode()
        print('The earliest year of birth is {},'
              '\nThe recent year of birth is {},'
              '\nThe most common year of birth is {}'.format(int(earliest_year), int(recent_year), int(common_year)))
    except:
        print('There is no Birth Year data in this city file')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def raw_data(df):
    row = 0
    see_raw_data = input("\nWould you like to see 5 lines of raw data? Please write 'yes' or 'no' \n").lower()
    while True:
        if see_raw_data == 'no':
            return
        if see_raw_data == 'yes':
            print(df[row: row + 5])
            row_index = row + 5
        see_raw_data = input("\n Would you like to see more? Please write 'yes' or 'no' \n").lower()


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        raw_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
    main()
