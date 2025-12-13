"""
construct and analyze root 3 
"""
from geometor.model import *
from geometor.render import *
from geometor.divine import *

def rotate_list(lst, rotations=1):
    rotated_list = lst.copy()  # Making a copy to keep the original list unchanged
    for _ in range(rotations):
        rotated_list = rotated_list[1:] + rotated_list[:1]
    return rotated_list

def run():
    NAME = 'root3b'

    model = Model(NAME)
    A = model.set_point(0, 0, classes=['given'])
    B = model.set_point(1, 0, classes=['given'])

    model.construct_line(A, B)

    model.construct_circle(A, B)
    model.construct_circle(B, A)

    model.construct_line_by_labels('E', 'A')
    model.construct_line_by_labels('E', 'B')
    model.construct_line_by_labels('F', 'A', classes=['red'])
    model.construct_line_by_labels('F', 'B', classes=['red'])

    model.construct_line_by_labels('E', 'F')
    model.construct_line_by_labels('A', 'J')
    model.construct_line_by_labels('B', 'I')
    model.construct_line_by_labels('I', 'J', classes=['red'])

    model.construct_circle_by_labels('O', 'F')
    model.construct_circle_by_labels('E', 'A')

    poly_labels = ['F', 'I', 'J']
    model.set_polygon_by_labels(poly_labels, classes=['red'])

    poly_labels = ['F', 'X', 'T', 'J', 'U', 'W', 'I', 'S', 'V']
    model.set_polygon_by_labels(poly_labels)

    #  radial_pt_label = poly_labels[0]
    #  for poly_label in poly_labels[1:]:
        #  model.construct_line_by_labels(radial_pt_label, poly_label, classes=['red'])

    #  poly_labels = rotate_list(poly_labels, rotations=3)
    #  radial_pt_label = poly_labels[0]
    #  for poly_label in poly_labels[1:]:
        #  model.construct_line_by_labels(radial_pt_label, poly_label, classes=['green'])

    #  poly_labels = rotate_list(poly_labels, rotations=3)
    #  radial_pt_label = poly_labels[0]
    #  for poly_label in poly_labels[1:]:
        #  model.construct_line_by_labels(radial_pt_label, poly_label, classes=['blue'])



    #  report_sequence(model)
    #  report_group_by_type(model)
    #  report_summary(model)

    print("\nfind golden sections in model: \n")
    sections, sections_by_line = find_golden_sections_in_model(model)
    print(f"sections: {len(sections)}")
    for section in sections:
        #  print(section.lengths)
        #  print(section.ratio)
        #  print(section.min_length)
        #  #  print(section.points)
        print(section.get_labels(model))

    chain_tree = find_chains_in_sections(sections)
    chains = unpack_chains(chain_tree)
    print(f"chains: {len(chains)}")
    for chain in chains:
        labels = ["_".join(section.get_labels(model)) for section in chain.sections]
        print()
        print(labels)
        print(len(chain.sections))

        print("points: ", chain.points)
        print("lengths: ", chain.lengths)
        print("floats: ", chain.numerical_lengths)
        print("fibs: ", chain.fibonacci_labels)

    print('flow: ')
    for chain in chains:
        labels = ["_".join(section.get_labels(model)) for section in chain.sections]
        print(chain.count_symmetry_lines(), chain.flow)

    print(f"sections: {len(sections)}")
    print(f"chains: {len(chains)}")

    sequencer = Sequencer(model.name)
    #  sequencer.plot_sequence(model, extensions=['png'])
    sequencer.step_sequence(model)

    plotter = Plotter(model.name)
    plotter.plot_model(model)
    plot_all_sections(plotter, model, sections)

    plotter = Plotter(model.name)
    plotter.plot_model(model)
    plot_sections(plotter, model, sections)

    plotter = Plotter(model.name)
    plotter.plot_model(model)
    plot_chains(plotter, model, chains)

    groups = group_sections_by_points(sections)
    plotter = Plotter(model.name)
    plotter.plot_model(model)
    title = "group sections by point"
    plot_groups(plotter, model, groups, title)

    report_sequence(model)

    #  plt.show()

    #  AAA = model.get_element_by_label('AAA')
    #  ancestors = model.get_ancestors_labels(AAA)
    #  print(ancestors)

    #  dot_ancestors = generate_dot(ancestors)
    #  print(dot_ancestors)

    #  analyze_and_plot(sequencer, model)


if __name__ == '__main__':
    run()
