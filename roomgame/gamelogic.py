
from random import randint

try:
	compat_input = raw_input
except NameError:
	compat_input = input

from django.shortcuts import render


def start_game():
	print("""
===

The Amazing Game in Which One Escapes a Room

A Game by Kirby

June 2017
v.0.1

===""")
	level = GameLevel()
	level.start()

class GameLevel(object):

	def __init__(self, session):
		self.session = session
		self.welcome_message = """
I can't believe it! It's a game! 

It's a game in which you pick up a key and escape a room. 
		"""
		self.silly_greeting = [
			"You must love tomato sandwiches.",
			"I like your silly socks.",
			"I think you'd look snazzy in a hat.",
			"Don't you just love coconut water?",
			"Meow! Meow!",
			"Hug the turtles when you go swimming!"
		]
		self.action_list = {
			"think": "Good thinking.",
			"look": "You look around and spot a key on the floor!",
			"sit": "The floor's pretty comfy.",
			"stand": "You stand up.",
			"dance": "I like your dancing.",
			"walk": """You walk around the room. 
	There are walls. 
	There's a floor. 
	There's a ceiling. 
	There's a door.""",
			"pick": "You pick up the key! It's super shiny.",
			"unlock": "You unlock the door with the key!",
			"open": "You escape!"
		}
		self.valid_action = True
		self.action = None
		self.set_users_name = False

	def start(self):
		print(self.welcome_message)
		username = compat_input("""
I guess that means you should select a username.

Type in your username: """)
		print("")
		print("""===

It looks like your username is {}.""".format(username))

		val = 0
		for x in username:
			val += ord(x)
		val = val % len(self.silly_greeting)
		print(self.silly_greeting[val])

		print("""
Hmm... It appears you've found yourself in a room with a locked door!
And you're late for a party!

The kind of party with nice people that you like,
and there'll be snacks you enjoy. 

You don't want to miss it!
But you're stuck!
Oh no!

You've got to figure out how to get out of the room. 
""")

		print("""
You made it! Wow!

You found a key!

And picked it up! 

And unlocked the door!

And opened it!

You escaped the room!

Have a great time at the party {}!!!""".format(username))

	def has_name(self):
		return 'name' in self.session

	def set_name(self, name):
		self.session['name'] = name
		self.set_users_name = True

	def perform_action(self, action):
		if action is None:
			self.valid_action = False
			return
		user_input = action.lower()
		words = action.split(" ")
		for word in words:
			if word in self.action_list.keys():
				self.action = word
				return
		self.valid_action = False

	def get_response(self, request):
		context = {
			"has_name": 'name' in self.session,
			"message": self.get_action_msg(),
			"has_escaped": 'has_escaped' in self.session
		}
		return render(request, 'roomgame/index.html', context)

	def get_greeting(self):
		val = 0
		for x in self.session['name']:
			val += ord(x)
		val = val % len(self.silly_greeting)
		return "It looks like your name is {}!\n".format(self.session['name']) + self.silly_greeting[val]

	def get_action_msg(self):
		if 'name' not in self.session:
			return "First we need your username, good person!"
		if self.set_users_name:
			return self.get_greeting()
		if not self.valid_action:
			return "Not a valid action, try again!"
		if self.action == "think":
			return self.action_list[self.action]
		elif self.action == "look":
			self.session["seen_key"] = True
			return self.action_list[self.action]
		elif self.action == "sit":
			if not self.session.get("sitting", False):
				self.session["sitting"] = True
				return self.action_list[self.action]
			else:
				return "You sit even more."
		elif self.action == "stand":
			if not self.session.get("sitting", False):
				return "You're already standing."
			else:
				self.session["sitting"] = False
				return self.action_list[self.action]
		elif self.action == "dance":
			if not self.session.get("sitting", False):
				return self.action_list[self.action]
			else:
				return "You have to stand up first, silly."
		elif self.action == "walk":
			if not self.session.get("sitting", False):
				return self.action_list[self.action]
			else:
				return "You have to stand up first, silly."
		elif self.action == "pick":
			if not self.session.get("seen_key", False):
				return "That doesn't work."
			elif self.session.get("has_key", False):
				return "You're already holding the key."
			else:
				self.session["has_key"] = True
				return self.action_list[self.action]
		elif self.action == "unlock":
			if not self.session.get("has_key", False):
				return "You need a key to unlock the door!"
			elif self.session.get("has_unlocked_door", False):
				return "The door's unlocked! It's just closed."
			else:
				self.session["has_unlocked_door"] = True
				return self.action_list[self.action]
		elif self.action == "open":
			if not self.session.get("has_unlocked_door", False):
				return "The door's still locked."
			else:
				self.session["has_escaped"] = True
				return self.action_list[self.action]
		else:
			return "Dunno what you're doing."

if __name__ == '__main__':
	start_game()