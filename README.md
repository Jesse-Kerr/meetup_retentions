
*BACKGROUND*

* There are nearly 350,000 Meetup groups globally. Around 82% of their information is public.

* The groups are organized into 33 different categories, such as Arts and Culture, Business, or Singles. These categories have different numbers of meetup groups within them.

*QUESTION*

Can we calculate the *retention rate* of attendees to a particular Meetup group? Will this average retention rate differ based off of Meetup category?

*HYPOTHESIS*

I hypothesize that groups in different Meetup categories will have different percentages of returners. I also hypothesize that this will be inversely correlated to the 'popularity' of that category, measured either by # of groups in the category or average attendees per meetup event for the group. 

*NULL HYPOTHESIS*

There will be no difference in % returner rates per category.

*METHODS*

1. For every event for a meetup group, get a list of the member IDs who RSVP'ed YES to it. Create a list of members who returned, and a set of total members who ever attended. 

2. Divide the list of returners by the total attendees, giving us a binomial distribution of many Bernoulli trials. Each Bernoulli trial is: Did the user come back or not?

2. Take average of the groups for each Meetup category.

3. Do a t-test to compare retention rates per category. Perform Bonferroni correction to correct for multiple comparisons. 

4. Inspect whether popularity of category (measured in 3) correlates with retention rate.
