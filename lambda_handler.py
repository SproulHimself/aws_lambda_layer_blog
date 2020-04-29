# set the URL
url = 'https://www.vegasinsider.com/nfl/odds/futures/'

#define the dataframe; which happens to be located in the 6th index position
df = pd.read_html(url)[6]

# limit the dataframe to the 32 teams/rows we want
df = df.iloc[:32, :-1]

# label the columns
df.columns = ['team', 'odds']

# convert the fraction to American odds
df.odds = df.odds.apply(lambda x: 100*float(Fraction(x)))

# format the row into string w/ "+"
df.odds = df.odds.apply(lambda x: '+' + str('%g'%(x)))

# move the index; uncesessary, but visually pleasing
df.index += 1

# instantiate S3 object
s3 = boto3.client('s3')

# set datetime str w/ EST timezone adjustment and Daylight Savings
if datetime.now().month in range(4,11):
    day_and_time = (timedelta(hours=-4) + datetime.now())
else:
    day_and_time = (timedelta(hours=-5) + datetime.now())
day_and_time = day_and_time.strftime("%b-%d-%Y-%H%M%S")

# the two different file paths used for uploading
scraped_file_path = '/tmp/SB_odds_' + str(day_and_time) + '.csv'
path_name_for_bucket = scraped_file_path[5:]

# create csv file
output = final.to_csv(scraped_file_path, index=True)

# upload the new csv file to S3
s3.upload_file(f'{scraped_file_path}', '<YOUR_S3_BUCKET_NAME_STR>', f'{path_name_for_bucket}')

# define a simple lambda handler
def lambda_handler(event, context):
    return {
    'body': json.dumps('SUCCESS: The SB odds have been scraped!'),
    'date and time':day_and_time
}
