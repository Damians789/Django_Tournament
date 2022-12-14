# Django_Tournament
Web application written for school project

Basic conception:

- A person may have the status of a coach or a player

- One Person can have many teams, and one team can have many players/coaches

- A person has their own profile to which they can assign given professions

- Each discipline (100m dash, 300m dash, long jump, etc.) has the top three athletes and their corresponding scores

- Each competitor chooses the disciplines in which he wants to compete in a given competition, he can have more than one

- The stadium has information about the capacity of the stands, its permanent address and whether it is adapted for the disabled, as well as a photo or the so-called. statistics

- Vote pozwala ocenić osobie dany stadion

- The competition has its name, time and place of the event and the time of its creation, affiliate_url, which is an alias for its name, allowing you to go to a dedicated page

and

- A list of competitors, in which the competitor is given, in which discipline he participates (there may be several), and for what competitions. The result is then filled

- Each competition also has locker rooms assigned to a given team


Not everything were achieved, such as automatically assining top three players in each categories based on their results (different models and pages)
