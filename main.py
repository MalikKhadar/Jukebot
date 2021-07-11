from keep_alive import keep_alive
import discord
import os
import vibes
import random
from replit import db

client = discord.Client()

if "vibes" not in db.keys():
  db["vibes"] = vibes.compendium

if "prompt" not in db.keys():
  db["prompt"] = "I don't have a prompt yet. Set one using $prompt <some text>"

if "most_recently_chosen" not in db.keys():
  db["most_recently_chosen"] = ""

well_wishes = ["Good luck!", "Have fun!", "Sounds like a tough one!", "You've got this!", "Knock 'em dead!", "Best of luck!", "What a combo!", "This should be interesting!", "Now that'll sound unique!", "Interesting!", "Not sure if anyone's ever gone for that before!", "Let me know how it went!", "Now this is gonna be big!", "I'm rootin' for ya.", "Come on! You can do it!!!!11!!1!", "Go get 'em tiger!", "It's worth a shot.", "The sky's the limit!", "Don't forget to save frequently!", "Let's gooooooooooooooooooooo", "Let's do this!", "You can do iiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiit!"]

def get_challenge(prompt):
  response = prompt
  if "I don't have a prompt yet" in response:
    return response
  else:
    response += " that sounds "
    vibe = random.choice(db["vibes"])
    response += vibe
    db["most_recently_chosen"] = vibe
    response += ". "
    response += random.choice(well_wishes)
    return response

def add_vibe(vibe):
  if "vibes" in db.keys():
    vibes = db["vibes"]
    vibes.append(vibe)
    db["vibes"] = vibes
  else:
    db["vibes"] = [vibe]

def remove_vibe(vibe):
  vibes = db["vibes"]
  if vibe in vibes:
    vibes.remove(vibe)
  db["vibes"] = vibes

def recall_vibe():
  vibes = db["vibes"]
  if len(vibes) > 0:
    del vibes[-1]
  db["vibes"] = vibes

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    msg = message.content

    if msg.startswith('$challenge'):
        if len(db["vibes"]) < 1:
            await message.channel.send("Wait a minute... who deleted all of the vibes? I start off with almost 200! Not cool.")
        else:
            response = get_challenge(db["prompt"])
            await message.channel.send(response)

    if msg.startswith('$prompt'):
        prompt = msg.split("$prompt ",1)
        if len(prompt) < 2:
            await message.channel.send("Current prompt: " + db["prompt"])
        else:
            db["prompt"] = prompt[1]
            await message.channel.send("Updated prompt!")

    if msg.startswith('$add'):
        vibe = msg.split("$add ",1)
        if len(vibe) < 2:
            await message.channel.send("Adding requires some text after $add")
        else:
            add_vibe(vibe[1])
            await message.channel.send("New vibe has been added to the compendium.")

    if msg.startswith('$remove'):
        if db["most_recently_chosen"] != "":
            remove_vibe(db["most_recently_chosen"])
            await message.channel.send("Vibe successfully yeeted.")
        else:
            await message.channel.send("$challenge must be used at least once before $remove. Are you trying to break me or something?")

    if msg.startswith('$recall'):
        if "vibes" in db.keys():
            recall_vibe()
        await message.channel.send("Vibe successfully yoinked.")

keep_alive()
client.run(os.getenv('TOKEN'))