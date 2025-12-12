import svgpathtools.path

COMMAND_RE_LENGTH = {
    'A': 7
}


def array_fix(array, command):
    result = []
    for x in array:
        if x.startswith('01'):
            result.extend(['0', '1'])
            if x[2:]:
                result.append(x[2:])
        elif x.startswith('00'):
            result.extend(['0', '0'])
            if x[2:]:
                result.append(x[2:])
        elif x[0] == '0' and not x[1:].startswith('.'):
            result.append(x[0])
            if x[1:]:
                result.append(x[1:])
        else:
            result.append(x)
    length = COMMAND_RE_LENGTH.get(command and command.upper())
    if length is not None and len(result) > length:
        result = result[:length]
    return result


def _tokenize_path(self, pathdef):
    result = []
    command_last = None
    for x in svgpathtools.path.COMMAND_RE.split(pathdef):
        if x in svgpathtools.path.COMMANDS:
            command_last = x
            result.append(x)
        result.extend(array_fix(svgpathtools.path.FLOAT_RE.findall(x), command_last))
    return result


svgpathtools.path.Path._tokenize_path = _tokenize_path
