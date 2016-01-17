# Dota2 Discord Bot

This is a basic structure for a Discord bot, it currently serves Dota2 match information for registered steamids.

It will be polling the STEAMAPI every 10 seconds asking for new Dota2 games played on the accounts registered, might give you some grief from the API team though.

### Since this is a work in progress im going to write the down commands below

* !register STEAMNAME/STEAMID - Registers a steam account to the sending users discord id
* !g - Gives you some dota2 stats about the last game played by sending user.
* !g DISCORDUSER - gives you info about that discord nicknames last game. Also works with mentions and without
* !unregister - Removes the steamid for the sending user.

### Setup
Create a file called evilbot.json in the cloned repository.
With the following content
<pre>
{
       "steam": {
                    "apikey" : "XXXXX"
       },
       "bot": {
                    "metacache_data_file" : "evilbot.cache",
                    "discord_username":"email@example.org",
                    "discord_password":"supersecretpassword",
                    "template_folders":["templates/"],
                    "admins" : [ "yourdiscordnick" ]
        }
}
</pre>

run
<pre>
pip install -r requirements.txt
</pre>
