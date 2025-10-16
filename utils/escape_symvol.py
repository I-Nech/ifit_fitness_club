def escape_symvol(text):
    text = text.replace('_', '\\_')
    text = text.replace('!', '\\!')
    text = text.replace('.', '\\.')
    return text

# print(escape_symvol('Привет. Хочешь гайд?'))