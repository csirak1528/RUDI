import rudi_defaults


def intin(cond, rang=[-1000, 1000]):
    ty = 0
    good = False
    while not good:
        try:
            ty = int(input(cond))
            if (ty <= rang[1]) and (ty >= rang[0]):
                good = True
        except ValueError:
            pass
    return ty


while True:
    in_ = input("r:")
    if in_ == "rcv":
        import rudi_rcv
        rudi_rcv.binder(input("r: Connection type:"))
    if in_ == "update":
        import rudi_update
        ty = intin("r: 1:ETH\n   2:WLAN\nr:", [1, 2])

        if ty == 1:

            for j, i in enumerate(rudi_defaults.ethlist):
                mainlis = rudi_defaults.ethlist

        if ty == 2:

            for j, i in enumerate(rudi_defaults.iplist):
                mainlis = rudi_defaults.iplist

        ty = intin("r: which ip:", [1, len(mainlis)])
        dir = rudi_update.getcur_dir()
        rudi_update.update(cur_dir=dir, ip=mainlis[ty-1])
