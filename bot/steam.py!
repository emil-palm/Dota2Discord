class Commands(object):
    def __init__(self, client):
        if not client:
            raise ArgumentError("Client cannot be None")
        self.client = client

    def _register(client,message,disc_user,account):
        steamid = None
        if len(account) == 17:
            # We have a 64bit steamid already lets use it
            steamid = Steamid(steamid=account,success=1)
        else:
            steamid = Steamid(**DotaApi().get_steam_id(account).get('response'))

        if steamid.success == 1:
            client.send_message(message.channel, "Registered %s to %s" % (account, disc_user.mention()))
            client.dota_accounts[disc_user.id] = steamid
            store_data()
        else:
            client.send_message(message.channel, "Could not find %s" % (account))

    def register(self, *args, **kwargs):
        if len(args) != 2:
            self.client.send_message(message.channel, 'Invalid amount of arguments; !register STEAMACCOUNTNAME')
            return
   
        if args[1] in self.client.dota_accounts:
            self.client.send_message(message.channel, 'Account already registered')
            return

        self._register(client,message.author,parts[1])

    @command(pattern="!g")
    def last_game(self, *args, **kwargs):
        print "GAME TIME"
        pass
