from geometor.utils import *
from geometor.model import *
from geometor.render import *
from geometor.pappus import *
from itertools import permutations

sp.init_printing()

BUILD = True
ANALYZE = True

PART1 = True
PART2 = True
PART3 = False
PART4 = False
if PART1:
    print_log(f'\nPART1')
    if PART2:
        print_log('PART2')
        if PART3:
            print_log('PART3')

NAME = 'pentagons-'
NAME += input(f'\nsession name: {NAME}')
log_init(NAME)
start_time = timer()

print_log(f'\nMODEL: {NAME}')
# add starting points
A_w, A_e = begin()

# find midpoint (origin)
bisector(A_w, A_e)
B_w, B_e = pts[2], pts[3]
Cn, Cs = pts[4], pts[5]
O = pts[6]
# find perps for square
bisector(A_w, B_e)
bisector(A_e, B_w)

# squares
D_ne = pts[18]
D_se = pts[17]
D_nw = pts[32]
D_sw = pts[31]

#  add_element(line(D_nw, D_ne))
#  add_element(line(D_sw, D_se))
#  add_polygon(polygon([A_w, A_e, D_ne, D_nw]))
#  add_polygon(polygon([A_w, A_e, D_se, D_sw]))

# golden circle
last_pts_count = len(pts)
c = add_element(circle(O, D_nw, classes=['gold']))
G_w = pts[last_pts_count]
G_e = pts[last_pts_count+1]

# outer goldens
last_pts_count = len(pts)
el = add_element(circle(A_w, G_e, classes=['gold']))
#  E_ne, E_se = pts[last_pts_count+1:last_pts_count+2]
E_ne = pts[last_pts_count+1]
E_se = pts[last_pts_count+2]
F_n = pts[last_pts_count+3]
F_s = pts[last_pts_count+4]

last_pts_count = len(pts)
el = add_element(circle(A_e, G_w, classes=['gold']))
E_nw = pts[last_pts_count+1]
E_sw = pts[last_pts_count+2]

pentagon_n = polygon([A_w, A_e, E_ne, F_n, E_nw])
add_polygon(pentagon_n)

if PART1:
    add_element(line(A_w, E_nw, classes=['set2']))
    add_element(line(A_w, F_n, classes=['set1']))
    add_element(line(A_w, E_ne, classes=['set1']))

    add_element(line(A_e, E_nw, classes=['set1']))
    add_element(line(A_e, F_n, classes=['set1']))
    add_element(line(A_e, E_ne, classes=['set2']))

    add_element(line(F_n, E_nw, classes=['set2']))
    add_element(line(F_n, E_ne, classes=['set2']))
    
    add_element(line(E_nw, E_ne, classes=['set1']))
    if PART2:

        pentagon_s = polygon([A_w, A_e, E_se, F_s, E_sw])
        add_polygon(pentagon_s)

        add_element(line(F_s, E_sw, classes=['set2']))
        add_element(line(F_s, E_se, classes=['set2']))
        
        add_element(line(A_w, E_se, classes=['set1']))
        add_element(line(A_e, E_sw, classes=['set1']))

        add_element(line(E_sw, E_se, classes=['set1']))
        # inner goldens
        #  add_element(circle(A_w, G_w, classes=['gold']))
        #  add_element(circle(A_e, G_e, classes=['gold']))

        #  # half unit circle
        #  add_element(circle(pts[6], A_w))

        #  # diagonals
        #  add_element(line(D_nw, D_se, classes=['green']))
        #  add_element(line(D_sw, D_ne, classes=['green']))

        if PART3:

            add_element(line(D_nw, G_w, classes=['set1']))
            add_element(line(D_sw, G_w, classes=['set1']))

            add_element(line(D_nw, G_e, classes=['set2']))
            add_element(line(D_sw, G_e, classes=['set2']))

            add_element(line(D_se, G_w, classes=['set2']))
            add_element(line(D_ne, G_w, classes=['set2']))

            add_element(line(D_se, G_e, classes=['set1']))
            add_element(line(D_ne, G_e, classes=['set1']))

            # cross
            add_element(line(pts[293], pts[292]))
            add_element(line(pts[293], pts[291]))

            add_element(line(pts[294], pts[292]))
            add_element(line(pts[294], pts[291]))


model_summary(NAME, start_time)

# ANALYZE ***************************
if ANALYZE:
    print_log(f'\nANALYZE: {NAME}')
    goldens, groups = analyze_model()

    analyze_summary(NAME, start_time, goldens, groups)

# PLOT *********************************
print_log(f'\nPLOT: {NAME}')
limx, limy = get_limits_from_points(pts, margin=.25)
limx, limy = adjust_lims(limx, limy)
bounds = set_bounds(limx, limy)
print_log()
print_log(f'limx: {limx}')
print_log(f'limy: {limy}')

#  plt.ion()
fig, (ax, ax_btm) = plt.subplots(2, 1, gridspec_kw={'height_ratios': [10, 1]})
ax_btm.axis('off')
ax.axis('off')
ax.set_aspect('equal')
plt.tight_layout()

title = f'G E O M E T O R'
fig.suptitle(title, fontdict={'color': '#960', 'size':'small'})

print_log('\nPlot Summary')
xlabel = f'elements: {len(elements)} | points: {len(pts)}'
ax_prep(ax, ax_btm, bounds, xlabel)
plot_sequence(ax, history, bounds)
snapshot(NAME, 'sequences/summary.png')

if BUILD:
    print_log('\nPlot Build')
    build_sequence(NAME, ax, ax_btm, history, bounds)

if ANALYZE:
    print_log('\nPlot Goldens')

    bounds = get_bounds_from_sections(goldens)

    plot_sections(NAME, ax, ax_btm, history, goldens, bounds)

    print_log('\nPlot Golden Groups')
    plot_all_groups(NAME, ax, ax_btm, history, groups, bounds)

    plot_all_sections(NAME, ax, ax_btm, history, goldens, bounds)

    complete_summary(NAME, start_time, goldens, groups)

else:
    model_summary(NAME, start_time)



plt.show()

