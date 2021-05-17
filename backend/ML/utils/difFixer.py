def rreplace(s, old, new, occurrence):
    """Replace all occurrences except first"""
    li = s.rsplit(old, occurrence)
    return new.join(li)

def fix_string(arg):
    """Heuristics for OCR"""
    arg = arg.upper()
    arg = arg.strip("\n\f")
    arg = arg.replace("g", "0")
    arg = arg.replace("I", "1")
    arg = arg.replace("To", "TD")
    arg = arg.replace("£", "E")
    arg = arg.replace("s", "S")
    arg = arg.replace("TO", "TD")
    arg = arg.replace("a", "3")
    arg = arg.replace("o", "0")
    arg = arg.replace("w", "V")
    arg = arg.replace("h", "1")
    arg = arg.replace("e", "G")
    arg = arg.replace("z", "2")
    if arg.startswith("121"):
        arg = arg.replace("121","L21")
    elif arg.startswith("AL"):
        arg = arg.replace("AL","A1")
    elif not arg.startswith("c"):
        arg = arg.replace("c", "0")
    if len(arg) <= 8 and len(arg) > 1:
        arg = arg.upper()
        if arg.endswith("I"):
            arg = arg.replace("I", "1")
        elif "£" in arg:
            arg = arg.replace("£", "E")
        elif "N" in arg:
            arg = arg.replace("N", "1")
        elif "Z" in arg:
            arg = arg.replace("Z", "2")
        elif "S" in arg:
            arg = arg.replace("S", "5")
        elif arg.startswith("1"):
            arg = arg.replace("1", "L", 1)
        elif arg.endswith("T"):
            arg = arg.replace(arg, arg[:-1] + "1", 1)
        elif arg.endswith("D"):
            arg = arg.replace(arg, arg[:-1] + "0", 1)
        elif arg.endswith("A"):
            arg = arg.replace(arg, arg[:-1] + "1", 1)
        elif arg.endswith("B"):
            arg = arg.replace(arg, arg[:-1] + "8", 1)
        elif arg.endswith("L"):
            arg = arg.replace("L",1)
        elif "T" in arg[3:]:
            if arg.count("T") == 1:
                arg = arg.replace("T", "1")
            else:
                arg = rreplace(arg, "T", "1", arg.count("T") - 1)
        elif not arg.startswith("A"):
            if arg.count("A") == 1 and not arg.startswith("T"):
                arg = arg.replace("A", "4", 1)
        elif not arg.startswith("T") and not arg.startswith("B"):
            arg = arg.replace("B", "8", 1)
    return arg
