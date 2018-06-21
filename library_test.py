import unittest
import library

NUM_CORPUS = '''
On the 5th of May every year, Mexicans celebrate Cinco de Mayo. This tradition
began in 1845 (the twenty-second anniversary of the Mexican Revolution), and
is the 1st example of a national independence holiday becoming popular in the
Western Hemisphere. (The Fourth of July didn't see regular celebration in the
US until 15-20 years later.) It is celebrated by 77.9% of the population--
trending toward 80.                                                                
'''


class TestCase(unittest.TestCase):

    # Helper function
    def assert_extract(self, text, extractors, *expected):
        actual = [x[1].group(0) for x in library.scan(text, extractors)]
        self.assertEquals(str(actual), str([x for x in expected]))

    # First unit test; prove that if we scan NUM_CORPUS looking for mixed_ordinals,
    # we find "5th" and "1st".
    def test_mixed_ordinals(self):
        self.assert_extract(NUM_CORPUS, library.mixed_ordinals, '5th', '1st')

    # Second unit test; prove that if we look for integers, we find four of them.
    def test_integers(self):
        self.assert_extract(NUM_CORPUS, library.integers, '1845', '15', '20', '80')

    # Third unit test; prove that if we look for integers where there are none, we get no results.
    def test_no_integers(self):
        self.assert_extract("no integers", library.integers)

    def test_dates(self):
        self.assert_extract('I was born on 2015-07-25.', library.dates_iso8601, '2015-07-25')

    def test_no_incorrect_dates(self):
        self.assert_extract('Today is 2018-13-32.', library.dates_iso8601)

    def test_dates_fmt2(self):
        self.assert_extract('I was born on 25 Jan 2017.', library.dates_fmt2, '25 Jan 2017')

    def test_dates_and_timestamps_min_space_del(self):
        self.assert_extract('I was born on 2018-06-22 18:22.',
                            library.dates_iso8601_timestamps_delimiters_timezones,
                            '2018-06-22 18:22')

    def test_dates_and_timestamps_sec_space_del(self):
        self.assert_extract('I was born on 2018-06-22 18:22:19',
                            library.dates_iso8601_timestamps_delimiters_timezones,
                            '2018-06-22 18:22:19.')

    def test_dates_and_timestamps_ms_space_del(self):
        self.assert_extract('I was born on 2018-06-22 18:22:19.123.',
                            library.dates_iso8601_timestamps_delimiters_timezones,
                            '2018-06-22 18:22:19.123')

    def test_dates_and_timestamps_min_T_del(self):
        self.assert_extract('I was born on 2018-06-22T18:22.',
                            library.dates_iso8601_timestamps_delimiters_timezones,
                            '2018-06-22T18:22')

    def test_dates_and_timestamps_sec_T_del(self):
        self.assert_extract('I was born on 2018-06-22T18:22:19',
                            library.dates_iso8601_timestamps_delimiters_timezones,
                            '2018-06-22T18:22:19.')

    def test_dates_and_timestamps_ms_T_del(self):
        self.assert_extract('I was born on 2018-06-22T18:22:19.123.',
                            library.dates_iso8601_timestamps_delimiters_timezones,
                            '2018-06-22T18:22:19.123')

    def test_dates_and_timestamps_sec_space_del_UTC(self):
        self.assert_extract('I was born on 2018-06-22 18:22:19UTC',
                            library.dates_iso8601_timestamps_delimiters_timezones,
                            '2018-06-22 18:22:19UTC.')

    def test_dates_and_timestamps_ms_space_del_MDT(self):
        self.assert_extract('I was born on 2018-06-22 18:22:19.123MDT.',
                            library.dates_iso8601_timestamps_delimiters_timezones,
                            '2018-06-22 18:22:19.123MDT')

    def test_dates_and_timestamps_min_T_del_UTC(self):
        self.assert_extract('I was born on 2018-06-22T18:22UTC.',
                            library.dates_iso8601_timestamps_delimiters_timezones,
                            '2018-06-22T18:22UTC')

    def test_dates_and_timestamps_sec_T_del_MDT(self):
        self.assert_extract('I was born on 2018-06-22T18:22:19',
                            library.dates_iso8601_timestamps_delimiters_timezones,
                            '2018-06-22T18:22:19MDT.')


if __name__ == '__main__':
    unittest.main()
