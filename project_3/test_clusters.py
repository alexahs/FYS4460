import numpy as np
import matplotlib.pyplot as plt
from scipy.ndimage import measurements
from pylab import *
# np.random.seed(41)


def simpleCluster():
    p = 0.5
    L = 20
    z = np.random.random((L, L))
    m = z<p
    lw, num = measurements.label(m)
    print(num)

    b = arange(lw.max() + 1)
    shuffle(b)
    shuffledLw = b[lw]

    area = measurements.sum(m, lw, index=arange(lw.max() + 1))
    areaImg = area[lw]
    imshow(areaImg, origin='lower')
    colorbar()
    show()

def clusters():
    L = 100
    pv = [0.2,0.3,0.4,0.5,0.6,0.7]
    z = rand(L,L)
    for i in range(len(pv)):
        p = pv[i]
        m = z<p
        lw, num = measurements.label(m)
        area = measurements.sum(m, lw, index=arange(lw.max() + 1))
        areaImg = area[lw]
        subplot(2,3,i+1)
        tit = 'p='+str(p)
        imshow(areaImg, origin='lower')
        title(tit)
        axis()
    show()

def Pi():
    # L = 100
    for L in (50, 100, 200):
        p = linspace(0.5,0.7,50)
        nx = len(p)
        Ni = zeros(nx)
        N = 1000
        for i in range(N):
            z = rand(L,L)
            for ip in range(nx):
                m = z<p[ip]
                lw, num = measurements.label(m)
                labelList = arange(lw.max() + 1)
                area = measurements.sum(m, lw, labelList)
                maxLabel = labelList[where(area == area.max())]
                sliced = measurements.find_objects(lw == maxLabel)
                if(len(sliced) > 0):
                    sliceX = sliced[0][1]
                    sliceY = sliced[0][0]
                    dx = sliceX.stop-sliceX.start
                    dy = sliceY.stop-sliceY.start
                    maxsize = max(dx,dy)
                    if (maxsize>=L): # Percolation
                        Ni[ip] = Ni[ip] + 1
        Pi = Ni/N
        plot(p,Pi)
    show()

def Pi2():
    # L = 100
    for L in (50, 100, 200):
        p = linspace(0.5,0.7,50)
        nx = len(p)
        Ni = zeros(nx)
        P = zeros(nx)
        N = 100
        for i in range(N):
            if (i%100==0):
                print("i = ",i)
            z = rand(L,L)
            for ip in range(nx):
                m = z<p[ip]
                lw, num = measurements.label(m)
                labelList = arange(lw.max() + 1)
                area = measurements.sum(m, lw, labelList)
                maxLabel = labelList[where(area == area.max())]
                sliced = measurements.find_objects(lw == maxLabel)
                if(len(sliced) > 0):
                    sliceX = sliced[0][1]
                    sliceY = sliced[0][0]
                    dx = sliceX.stop-sliceX.start
                    dy = sliceY.stop-sliceY.start
                    maxsize = max(dx,dy)
                    if (maxsize>=L): # Percolation
                        Ni[ip] = Ni[ip] + 1
                        P[ip] = P[ip] + area.max()
        Pi = Ni/N
        P = P/(L*L)
        subplot(2,1,1)
        plot(p,Pi, label=f"L={L}")
        subplot(2,1,2)
        plot(p,P, label=f"L={L}")
    legend()
    show()


def nsp():
    nsamp = 1000
    L = 1000
    p = 0.90
    allarea = array([])
    for i in range(nsamp):
        z = rand(L)
        m = z<p
        lw, num = measurements.label(m)
        labelList = arange(lw.max() + 1)
        area = measurements.sum(m, lw, labelList)
        allarea = append(allarea,area)
    n,sbins = histogram(allarea,bins=int(max(allarea)))
    s = 0.5*(sbins[1:]+sbins[:-1])
    nsp = n/(L*nsamp)
    sxi = -1.0/log(p)
    nsptheory = (1-p)**2*exp(-s/sxi)
    i = nonzero(n)
    semilogy(s[i],nsp[i],'o',s,nsptheory,'-')
    xlabel('$s$')
    ylabel('$n(s,p)$')
    plt.show()


def nsp2():
    nsamp = 100
    L = 200
    p = 0.58
    allarea = array([])
    for i in range(nsamp):
        z = rand(L, L)
        m = z<p
        lw, num = measurements.label(m)
        labelList = arange(lw.max() + 1)
        area = measurements.sum(m, lw, labelList)
        allarea = append(allarea,area)
    n,sbins = histogram(allarea,bins=int(max(allarea)))
    s = 0.5*(sbins[1:]+sbins[:-1])
    # nsp = n/(L*nsamp)
    # i = nonzero(n)
    # subplot(2,1,1)
    # plot(s[i],nsp[i],'o')
    # xlabel('$s$')
    # ylabel('$n(s,p)$')
    # subplot(2,1,2)
    # loglog(s[i],nsp[i],'o')
    # xlabel('$s$')
    # ylabel('$n(s,p)$')
    M = nsamp
    a = 1.2
    logamax = ceil(log(max(s))/log(a))
    logbins = a**arange(0,logamax)
    nl,nlbins = histogram(allarea,bins=logbins)
    ds = diff(logbins)
    sl = 0.5*(logbins[1:]+logbins[:-1])
    nsl = nl/(M*L**2*ds)
    loglog(sl,nsl,'.b')
    show()

nsp2()
