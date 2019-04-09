from vpython import *

maxx = 15
maxy = 15

v1 = 3
v2 = 0
v3 = 2
v4 = -2
scale = 5

scene1 = canvas( width=600, height=600, align='left' )

sphlist = [ [ sphere( pos=vec(x, y, 0) , radius=0.5 ) for x in range(-maxx, maxx+1) ] for y in range(-maxy, maxy+1) ]

for i in range(-maxx, maxx+1):
    sphlist[0][i].pos.z = v1 * scale
    sphlist[-1][i].pos.z = v3 * scale
for i in range(-maxy, maxy+1):
    sphlist[i][0].pos.z = v2 * scale
    sphlist[i][-1].pos.z = v4 * scale
sphlist[0][0].opacity = sphlist[0][-1].opacity = sphlist[-1][0].opacity = sphlist[-1][-1].opacity = 0

for _ in range(1000):
    for y in range(1, 2*maxy):
        for x in range(1, 2*maxx):
            sphlist[y][x].pos.z = ( sphlist[y+1][x].pos.z + sphlist[y-1][x].pos.z + sphlist[y][x+1].pos.z + sphlist[y][x-1].pos.z ) / 4


# electric field

scene2 = canvas( width=600, height=600, align='right' )

arrlist = [ [ arrow( pos=vec(x, y, 0) ) for x in range(-maxx, maxx+1) ] for y in range(-maxy, maxy+1) ]
for i in range(-maxx, maxx+1):
    arrlist[0][i].opacity = arrlist[-1][i].opacity = 0
for i in range(-maxy, maxy+1):
    arrlist[i][0].opacity = arrlist[i][-1].opacity = 0

for y in range(1, 2*maxy):
    for x in range(1, 2*maxx):
        ex = ( sphlist[y][x-1].pos.z - sphlist[y][x+1].pos.z ) / 2
        ey = ( sphlist[y-1][x].pos.z - sphlist[y+1][x].pos.z ) / 2
        arrlist[y][x].axis = vec(ex, ey, 0)
        arrlist[y][x].length = sqrt( ex**2 + ey**2 )
        arrlist[y][x].shaftwidth = 0.15



