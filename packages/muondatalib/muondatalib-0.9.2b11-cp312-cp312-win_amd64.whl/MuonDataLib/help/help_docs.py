HIST = 'histogram'
LOAD = 'load_events'
NXS = 'NeXus'
FILTER = 'filter'
TIME = 'time'
LOG = 'sample log'
MUONDATA = 'MuonData'
FIGURE = 'Figure (plotting)'
UTILS = 'utils'
PEAK = 'Peak Properties'


tags = [MUONDATA, LOAD, FIGURE, UTILS,
        HIST, FILTER, TIME, LOG, NXS, PEAK]


class Doc(object):
    def __init__(self, name, module, tags, description='',
                 param={}, optional_param={}, returns='',
                 example=[]):
        """
        A simple class for dealing with documentation.
        It stores relevant information and will then
        write it in the appropriate format (rst or MD).
        :param name: the name of the command
        :param module: the module the command belongs to
        :param tags: the tags used to label the command
        :param description: a description of the command
        :param param: the required parameters
        as a dict {name: description}
        :param optional_param: the optional parameters
        as a dict {name: [description, defaul value]}
        :param returns: the return values
        :param example: Some example code as a list.
        Each entry in the list is a new line.
        """
        self.name = name
        self.module = module
        self.tags = tags
        self.description = description
        self.param = param
        self.optional_param = optional_param
        self.returns = returns
        self.example = example

    def write_text(self, file_name, text):
        """
        Writes the text to a file
        :param file_name: the file name
        :param text: the text to write
        """
        with open(file_name, 'a') as file:
            file.write(text)

    def get_rst(self):
        """
        Generates rst style docs.
        :returns: string of rst
        """
        text = f'`{self.module}`.{self.name}\n'
        for k in range(len(text)):
            text += '-'
        text += '\n'
        text += f'{self.description} \n\n'
        space = '    '
        if len(self.param) > 0:
            tmp = '**Required Parameters:** \n'
            for info in self.param.keys():
                tmp += space + f'- `{info}`: {self.param[info]} \n'
            text += tmp

        if len(self.optional_param) > 0:
            tmp = '\n' + '**Optional Parameters:** \n'
            for info in self.optional_param.keys():
                msg = self.optional_param[info]
                value = f'- `{info}`: {msg[0]} *Default value:* `{msg[1]}`'
                tmp += space + value + '''.\n'''
            text += tmp

        if self.returns != '':
            text += '\n' + f'**Returns:** {self.returns} \n'

        if len(self.example) > 0:
            text += "\n" + "**Example:** \n\n"
            text += ".. code:: python\n \n"
            for eg in self.example:
                text += f'    {eg} \n'
        text += '\n\n'
        return text

    def get_MD(self):
        """
        Generates MD (mark down) style docs
        :returns: string of MD
        """
        text = f'''# `{self.module}`.**{self.name}** \n'''
        text += f'''{self.description} \n\n'''

        if len(self.param) > 0:
            tmp = '''**Required Parameters:** \n'''
            for info in self.param.keys():
                tmp += f'''- `{info}`: {self.param[info]} \n'''
            text += tmp

        if len(self.optional_param) > 0:
            tmp = '''\n''' + '''**Optional Parameters:** \n'''
            for info in self.optional_param.keys():
                msg = self.optional_param[info]
                value = f'''- `{info}`: {msg[0]} *Default value:* `{msg[1]}`'''
                tmp += value + '''.\n'''
            text += tmp

        if self.returns != '':
            text += '''\n''' + f'''**Returns:** {self.returns} \n'''

        if len(self.example) > 0:
            text += "\n" + """**Example:** \n\n"""
            text += """``` python\n"""
            for eg in self.example:
                text += f'''{eg} \n'''
            text += '''```\n'''
        return text
