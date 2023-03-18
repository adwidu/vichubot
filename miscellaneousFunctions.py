import json, discord
async def need_adminsconf_permision(ctx):
    user_id = ctx.author.id
    await ctx.send("Necesitas estar dentro del archivo admins.conf de la data del bot para usar este tipo de comandos, tu id es: " + str(user_id))
def get_memes_by_num(number,jsonString):
    jsonData = json.loads(jsonString)
    image = jsonData["meme" + str(number)]
    text = jsonData["meme" + str(number) + "text"]
    return (image, text)
def get_email_by_num(number,jsonString):
    jsonData = json.loads(jsonString)
    text = jsonData["email" + str(number+1)]
    return (text)
def get_password_by_num(number,jsonString):
    jsonData = json.loads(jsonString)
    text = jsonData["password" + str(number+1)]
    return (text)
def get_warnings(member: discord.Member, objectType): 
    warningsFile = open("warnings.wrn","r")
    for line in warningsFile.readlines():
        if(line.startswith(str(member.id))):
            data = line.split(":")[1]
            if objectType == int:
                return int(data)
            elif objectType == str:
                return str(data)
    if objectType == int:
        return int(0)
    elif objectType == str:
        return str(0)
def add_warning(member: discord.member.Member):
    warningsFile = open("warnings.wrn","r")
    lines = warningsFile.readlines()
    cline = 0
    done = False
    for line in lines:
        if(line.startswith(str(member.id))):
            data = int(line.split(":")[1])
            data += 1
            newline = "{}:{}\n".format(str(member.id),str(data))
            lines[cline] = newline
            warningsFile.close()
            done = True
        cline += 1
        warningsFile = open("warnings.wrn","w")
        warningsFile.writelines(lines) 
        warningsFile.close()
    if not done:
        warningsFile = open("warnings.wrn","w")
        warningsFile.writelines(lines)
        newline = "{}:1\n".format(str(member.id))
        warningsFile.write(newline)
        
        warningsFile.close()


class VoteList():
    _options = []
    def add(self, numberOfVotes, name):
        self._options.append([numberOfVotes, name])
    def sort(self):
        self._options.sort(reverse=True)
    def get(self, index):
        return self._options[index]