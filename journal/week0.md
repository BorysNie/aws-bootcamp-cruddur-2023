# Week 0 — Billing and Architecture

## ToDo Checklist<p>

### Watch videos
- [Week 0 - Livestream](https://www.youtube.com/watch?v=SG8blanhAOg&list=PLBfufR7vyJJ7k25byhRXJldB5AiwgNnWv&index=12)<br>
- [Week 0 - Spend Considerations](https://www.youtube.com/watch?v=OVw3RrlP-sI&list=PLBfufR7vyJJ7k25byhRXJldB5AiwgNnWv&index=13)<br>
- [Week 0 - Security Consuderations](https://www.youtube.com/watch?v=4EMWBYVggQI&list=PLBfufR7vyJJ7k25byhRXJldB5AiwgNnWv&index=15)<br>

### AWS inital configuration<p>

- Create Admin User
  - Navigate to IAM
  - Add users
  - Provide a user name and enable console access (optional)
  - Next
  - Permission options, add user to a group
  - Create group, tick AdministratorAccess Policy and click create user group
  - Tick the newly created group under user groups and click next
  - Lastly tag user for resource tracking and create user
<br>

- Create AWS Credential keys
  - Navigate to IAM, Users, click the newly created user
  - Under the Summary, click Security credentials and scroll down to Access keys
  - Create an access key for the Command Line Interface (CLI)
<br>

- Create AWS Budget
  - Navigate to the Billing service
  - Click Budgets from the left hand menu
  - Create a budget, use a template, monthly cost budget
  - Name the budget and enter the month usage limit
  - Finally create the budget
<br>

- Create AWS Cloudwatch billing alarm
  - Go to Cloudwatch service, create an alarm, select metric
  - Click Billing, click on Total Estimated Charge
  - Tick the USD value and click Select metric
  - Next set the period at which the check's should occur
  - Select threshold type as static and make sure to use Greater/Equal (>=) threshold
  - Input the value in USD it shouldn't exceed and proceed
  - In the notification tab, create a new topic and provide your email address<p>
  It will use your email address to notify you whether you are reaching the threshold specified
  - Finally name the alarm and create it<p>
  Once created make sure to confirm the alert which you should receive within your email mailbox

- Use CloudShell
  - Serverless Bash environment with access to the AWS CLI built-in
<br>

### Lucid charts<p>
- [Week 0 - Lucid charts Napkin diagram](https://lucid.app/lucidchart/3b2a2614-d9da-459a-8416-63596c6f58d2/edit?invitationId=inv_53b32dfe-39e9-44d6-a8a8-c7bac168f0cd)<br>
- [Week 0 - Lucid charts Architectual diagram](https://lucid.app/lucidchart/fadd43a0-2824-49fc-b00d-62a8e1ad5da2/edit?invitationId=inv_96d3fde1-71d4-4744-b9b9-0e917663468d)<br>
