def leftright(p, left, right, font='a'):
    if font == 'a':
        p.set(font='a')
        p.textln("{:<30}{:>12}".format(left, right))
    else:
        p.set(font='b')
        p.textln("{:<44}{:>12}".format(left, right))