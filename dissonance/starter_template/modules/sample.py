import module

@module.respond('hi')
def hi(message):
    message.reply_to_user('Hey! Check out more about creating modules for Dissonance here: '
                          'https://github.com/jhgg/dissonance/tree/master/docs/modules')