import numpy as np
import matplotlib.pyplot as plt
import scipy.io as io
import scipy as sp

plt.close('all')

# reading data
pb1 = io.loadmat('mae214A_SPR15_hw4/pb1.mat')

# (a) and (b) u at grid point (65,iz)
def umeans(iz):
    uy = pb1['u'][:,:,iz].mean(axis=1)
    ut = pb1['u'][:,65,iz]
    uyt = pb1['u'][:,:,iz].mean().repeat(uy.size)
    return ut,uy,uyt

# plotting
for iz in [2,8,20]:

    ut,uy,uyt = umeans(iz)

    fig = plt.figure(figsize=(12,6))
    plt.plot(ut,label=r'$u(t)$')
    plt.plot(uy,label=r'$<u>_y(t)$')
    plt.plot(uyt,label=r'$<u>_{yt}$')
    lg = plt.legend(loc=2)
    plt.xlabel('Time')
    plt.ylabel('u')
    plt.title('(65,'+str(iz)+')')
    plt.savefig('pb1ab_'+str(iz))

# (c) <u+>_yt
up = pb1['u'].mean(axis=(0,1))[:64]
zp = pb1['zplus']

fig = plt.figure(figsize=(8,12))
plt.semilogx(zp,up)
#plt.semilogx(zp,np.log10(zp),'k--')
plt.xlim(0.,1e3)
plt.ylim(0,20.)
plt.xlabel(r'$z^+$')
plt.ylabel(r'$u^+$')
plt.savefig('pb1c')

# (d)
up_data = np.loadtxt('mae214A_SPR15_hw4/Uplus.dat')
fig = plt.figure(figsize=(8,12))
plt.semilogx(up_data[:,0],up_data[:,1])
plt.semilogx(zp,-4.+12.*np.log10(zp),'k--')
plt.xlim(0.,1e3)
plt.ylim(0,20.)
plt.xlabel(r'$z^+$')
plt.ylabel(r'$u^+$')
plt.savefig('pb1d')

up_data = np.loadtxt('mae214A_SPR15_hw4/Uplus.dat')
fig = plt.figure(figsize=(8,12))
plt.plot(up_data[:,0],up_data[:,1])
plt.plot(zp,-4.+12.*np.log10(zp),'k--')
plt.plot(zp,zp,'m--')
plt.xlim(0.,1e3)
plt.ylim(0,20.)
plt.xlabel(r'$z^+$')
plt.ylabel(r'$u^+$')
plt.savefig('pb1d_2')

# in preparation for problem 2, calculate Reynolds stresses
def tmean(u):
    return u.mean(axis=0)

def tmean_repeat(u):
    um = tmean(u)
    um = um.T.repeat(100).reshape(130,130,100).T 
    return um

def prime(u):
    return u - tmean_repeat(u)

def rstress(u,v):
    return (u*v).mean(axis=(0,1))

# first compute u, v, and w prime
u = prime(pb1['u'])
v = prime(pb1['v'])
w = prime(pb1['w'])

# now compute Reynolds stresses as a function of z
uu = rstress(u,u)
vv = rstress(v,v)
ww = rstress(w,w)
uv = rstress(u,v)
uw = rstress(u,w)
vw = rstress(v,w)

# and the production
um = pb1['u'].mean(axis=(0,1))
zc = pb1['zc'][0,:]
dzc = np.diff(zc)
dzc = (dzc[:-1]+dzc[1:])/2.

umz = (um[2:]-um[0:-2])/dzc
prod = -uw[1:-1]*umz
prod = np.hstack([prod[0],prod,prod[-1]])/(uu.max())  # think about this normalization

# save to disk
np.savez('myrestress.npz',zp=zp,uu=uu,vv=vv,ww=ww,uv=uv,uw=uw,vw=vw,prod=prod)
