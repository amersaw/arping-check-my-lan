def arping(pdst, timeout = 5):
    from scapy.all import srp,Ether,ARP,conf
    conf.verb=0
    ans,unans=srp(Ether(dst="ff:ff:ff:ff:ff:ff")/ARP(pdst=pdst),
        timeout=timeout)
    res = []
    for snd,rcv in ans:
        fmt = rcv.sprintf(r"%Ether.src%#%ARP.psrc%")
        res.append(fmt.split('#'))
    return res
