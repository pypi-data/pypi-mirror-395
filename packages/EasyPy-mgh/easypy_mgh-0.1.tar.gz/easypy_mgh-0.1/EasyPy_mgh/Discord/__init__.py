import discord
import os
"""EasyPy - Discord
-
hello Welcome to EasyPy -discord, We will welcome all coders!
This will make coding python Discord bot A bit more Simple"""
class bot():
    
    def __init__(self):
        """This is where you would make the bot function the heart"""
        self.intents = discord.Intents.default()
        self.intents.message_content = True
        self.client = discord.Client(intents=self.intents)
        self.TasksOnStart_M=[]
        self.ResponseMessagesReply={}
        self.ResponseMessages={}
        self.CommandsMessages={}
        self.InMessages={}
        self.RunOnStart=[]
        self.AnyMessageResponsCommand=""
        @self.client.event
        async def on_ready():
            for Task in self.TasksOnStart_M:
                await self.message(Task[0],Task[1])
            for Task in self.RunOnStart:
                await Task()

            print(f"Ready on {self.client.user}")
        @self.client.event
        async def on_message(message):
            if(message.content.lower() in self.ResponseMessagesReply) and (message.author != self.client.user):
                Reply=self.ResponseMessagesReply[message.content.lower()]
                await message.channel.send(Reply,reference=message)
            elif(message.content.lower() in self.ResponseMessages) and (message.author != self.client.user):
                Reply=self.ResponseMessages[message.content.lower()]
                await message.channel.send(Reply)
            elif(message.content.lower() in self.CommandsMessages) and (message.author != self.client.user):
                Command=self.CommandsMessages[message.content.lower()]
                await Command(message)
            for word in str(message.content).lower().split(" "):
                if (word in self.InMessages):
                    Reply=self.InMessages[word]
                    await message.channel.send(Reply)
            try:
                await self.AnyMessageResponsCommand(message)
            except:
                pass
        
            




    async def message(self,message,channel_id:int):
        channel = self.client.get_channel(channel_id)
        if(channel):

            await channel.send(message)
        else:
            print("ERROR")
        
    def RunBot_as_PlainToken(self,Token:str):
        """Runs Bot Without a Enverment Variable
        -----------
        str -> Token 
        _______________
        
        """
        self.client.run(Token)
    
    def RunBot_as_EnvToken(self,TokenEnv:str):
        """Runs Bot With a Enverment Variable
        -----------
        str -> TokenEnv
        _______________
        This will be the Enverment Variable Name
        """
        Token=os.getenv(TokenEnv)
        
        self.client.run(Token)
        
        
    def schedulemessages(self, list):
        """
        Schedule a Start Message
        _
        list: this Requres ["string",Channel ID]
        """
        self.TasksOnStart_M.append(list)
    
    def AddResponseReplyMessages(self,message,response):
        """
        Respons After Message sent (Mentions)
        _
        This will discribe the [message] varibal and if that matches with the
        [Discord message]. Then it will respond with [response]
        
        (Can only happen one par line)
        
        """
        self.ResponseMessagesReply.update({message.lower():response})
    
    def AddResponse(self,message,response):
        """
        Respons After Message sent 
        _
        This will discribe the [message] varibal and if that matches with the
        [Discord message]. Then it will respond with [response]
        
        (Can only happen one par line)
        
        """
        self.ResponseMessages.update({message.lower():response})
    
    def DoActionIf(self,message,command):
        """
        Respons a function after message==discord_message 
        _
        Runs async functions
        
        """
        self.CommandsMessages.update({message.lower():command})

    def InMessageResponse(self,word,reply):
        """Replys to a message if it have a word in it"""
        self.InMessages.update({word.lower():reply})
    def AppenedRunCommand(self,command):
        """
        Runs async functions
        _
        
        """
        self.RunOnStart.append(command)
