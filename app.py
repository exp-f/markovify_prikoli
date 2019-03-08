from time import sleep
import random
import sys
from threading import Thread
import markovify
from flask import Flask, render_template

app = Flask(__name__)

msg = ''

ch_text = open('datasets/chuvashia_facts.txt', 'r', encoding='UTF-8').read()
p_text = open('datasets/poslovicy.txt', 'r', encoding='UTF-8').read()
t_text = open('datasets/tweets.txt', 'r', encoding='UTF-8').read()

# слишком много пословиц бля, заебали
# p_text = '\n'.join(random.choices(p_text.split('\n'), k=500))
ch_model = markovify.NewlineText(ch_text)
p_model = markovify.NewlineText(p_text)
t_model = markovify.NewlineText(t_text)
congrats_text = open('datasets/congrats.txt', 'r', encoding='UTF-8').read()
c_model = markovify.NewlineText(congrats_text)
port = sys.argv[1]


def combine_models(*args, weights=(1, 1, 1)):
    global msg
    combo_model = markovify.combine(args, weights)
    msg = combo_model.make_sentence(tries=1000)


def thread_wrap():
    while True:
        weights = [random.uniform(1.0, 2.0) for _ in range(4)]
        # global c_model, p_model, t_model
        # combine_models(c_model, p_model, t_model, weights=weights)
        global msg, t_model, c_model, p_model, ch_model
        combo_model = markovify.combine([t_model, c_model, p_model, ch_model], weights=weights)
        msg = combo_model.make_short_sentence(280, tries=1000)
        sleep(3)


combine_thread = Thread(target=thread_wrap)
combine_thread.start()


@app.route('/')
def main():
    return render_template('tpl.html', msg=msg)


@app.route('/msg')
def get_msg():
    return msg


app.run(host='0.0.0.0', port=port)
