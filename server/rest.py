import goslate
import cleverbot

def from_latin(to_translate):
	target_language = "en"
	source_language='la'
	gs = goslate.Goslate()
	return  gs.translate(to_translate, target_language, source_language)
def to_latin(to_translate):
	target_language = "la"
	source_language='en'
	gs = goslate.Goslate()
	return  gs.translate(to_translate, target_language, source_language)

def cbot(to_work):
	cb1 = cleverbot.Cleverbot()
	english = from_latin(to_work)
	reply = cb1.ask(english)
	reply = to_latin(reply)
	return reply

#cb1 = cleverbot.Cleverbot()
#print to_latin(cb1.ask(from_latin("Salvete")))

print cbot("Salvete Discipuli")
