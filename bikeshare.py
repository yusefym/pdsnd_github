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
    print('\nChoose a city, month and weekday to get specified data')

    while(True):
        try:
            city = input("Type chicago, new york city or washington: ").lower()
            if city == 'chicago' or city == 'new york city' or city == 'washington':
                break;
            else:
                print('Try Again: the city that you typed is not available.\n')
        except KeyboardInterrupt:
            print('\nThere was a keboard interrupt... exiting program\n')
            exit()

    print('\nBefore We Continue Filtering... ')
    index = 0
    while(True):
        sample = input('\nWould you like to look at a sample of the data. Enter yes or no: ')
        if sample.lower() == 'yes':
            df = pd.read_csv(CITY_DATA[city])
            print(df.iloc[index:index+5], '\n')
            index += 5
        else:
            break

    while(True):
        try:
            months = ['all', 'january', 'febrduary', 'march', 'april', 'may', 'june', 'july', 'august', 'september', 'october', 'november', 'december']
            month = input("Type a month (all, january, february, ... , june): ").lower()
            if month in months:
                break;
            else:
                print('Try Again: the month that you typed is not available.\n')

        except KeyboardInterrupt:
            print('\nThere was a keboard interrupt... exiting program\n')
            exit()

    while(True):
        try:
            days = ['All', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
            day = input("Type a day of week (all, monday, tuesday, ... sunday): ").title()
            if day in days:
                break;
            else:
                print('\nTry Again: the day that you typed is not available.\n')

        except KeyboardInterrupt:
            print('\nThere was a keboard interrupt... exiting program\n')
            exit()

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

    df['Start Time'] = pd.to_datetime(df['Start Time'])

    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()

    if month != 'all':
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        df = df[df['month'] == month]

    if day != 'All':
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""
    print('\nREAD: If you specified a day or month those also will be the most common.')
    print('Calculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    df['month'] = df['Start Time'].dt.month
    popular_month = df['month'].mode()[0]
    print('Most Popular Month:', popular_month)

    df['day_of_week'] = df['Start Time'].dt.day_name()
    popular_day = df['day_of_week'].mode()[0]
    print('Most Popular Day of Week:', popular_day)

    df['hour'] = df['Start Time'].dt.hour
    popular_hour = df['hour'].mode()[0]
    print('Most Popular Start Hour:', popular_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    popular_start_station = df['Start Station'].mode()[0]
    print('Most Popular Starting Station: ', popular_start_station,'\n')

    popular_end_station = df['End Station'].mode()[0]
    print('Most Popular Ending Station: ', popular_end_station,'\n')

    df['S&E Station'] = '\nStart Station: ' + df['Start Station'] + '\nEnd Station: ' + df['End Station']
    popular_se_station = df['S&E Station'].mode()[0]
    print('Most Popular Combination of Start & End Stations: ', popular_se_station)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    total_travel_time = df['Trip Duration'].sum()
    print('Total Travel Time: ', total_travel_time)

    mean_travel_time = df['Trip Duration'].mean()
    print('Mean Travel Time: ', mean_travel_time)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    user_types = df['User Type'].value_counts()
    print("Displaying Counts of User Types...")
    print(user_types)

    try:
        print('\nDisplaying Counts of Gender...')
        gender_count = df['Gender'].value_counts()
        print(gender_count)
    except:
        print('There is no gender data in this city')
    try:
        print('\nDisplaying Birth Year Information...')
        most_common_year = df['Birth Year'].mode()[0]
        earliest_year = df['Birth Year'].min()
        recent_year = df['Birth Year'].max()
        print('Earliest Year of Birth: ', int(earliest_year))
        print('Most Recent Year of Birth: ', int(recent_year))
        print('Most Common Year of Birth: ', int(most_common_year))
    except:
        print('There is no Birth Year data on this city')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
