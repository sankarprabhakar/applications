# Automatic emails on birthdays and work aniversaries.

### Problem statement
To autogenerate birthday and work anniversary greeting of colleagues on their mailbox from your personal/work email ID.

### Solution
This script to be scheduled in cron job to sends automatic greeting emails to employee on their birthdays and work anniveraries. 
Employee data about date of birth and  work anniversay need to updated in employee.csv file.

By changing the SMTP url in send_email() function it can be configured to send email from other email servers as well


### Dependent python packages:
1. pandas
2. numpy
3. csv
4. io
5. argparse
6. random
7. pillow
8. time
9. os
10. datetime
11. smtplib
12. email

### How to usage : 

1. Update the employees.csv. Date need to be in "yyyy/mm/dd"
2. Create password for gmail from https://myaccount.google.com/apppasswords. 
3. Schedule the script to be run daily from cron job with below command.
python birthday_anniversary.py --from_email="youremail@mail.com" --password="password" --to_email="youremail@mail.com" --cc_list="youremail@mail.com" --from_name="Your name'
4. Job will send out Bday greeting and Work anniversaries email. Birthday Greeting messages are taken randomly from birthday_greeting.csv.
