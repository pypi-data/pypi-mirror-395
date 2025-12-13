"""
constructs the classic 'vesica pisces'
"""
from geometor.model import *
from geometor.model.helpers import *
from geometor.render import *

from geometor.divine import *


def run():
    model = Model("vesica4a")
    A = model.set_point(0, 0, classes=["given"])
    B = model.set_point(1, 0, classes=["given"])

    model.construct_line(A, B)

    model.construct_circle(A, B)
    model.construct_circle(B, A)

    C = model.get_element_by_ID("C")
    D = model.get_element_by_ID("D")
    E = model.get_element_by_ID("E")
    F = model.get_element_by_ID("F")

    model.set_polygon([A, B, E])
    model.set_polygon([A, B, F])

    model.construct_line(E, F, classes=["red"])
    model.construct_circle(A, D)
    model.construct_circle(B, C)

    model.set_wedge(A, B, F, E)

    #  report_summary(model)
    #  report_group_by_type(model)

    sequencer = Sequencer(model.name)
    #  sequencer.plot_sequence(model, extensions=['png'])
    sequencer.step_sequence(model)
    plt.show()

    print("\nfind golden sections in model: \n")
    sections, sections_by_line = find_golden_sections_in_model(model)
    print(f"sections: {len(sections)}")
    for section in sections:
        #  print(section.lengths)
        #  print(section.ratio)
        #  print(section.min_length)
        #  #  print(section.points)
        print(section.get_IDs(model))

    chain_tree = find_chains_in_sections(sections)
    print(f"chains: {len(chain_tree)}")
    chains = unpack_chains(chain_tree)
    for chain in chains:
        IDs = ["_".join(section.get_IDs(model)) for section in chain.sections]
        print()
        print(IDs)
        print(len(chain.sections))

        print("points: ", chain.points)
        print("lengths: ", chain.lengths)
        print("floats: ", chain.numerical_lengths)
        print("fibs: ", chain.fibonacci_IDs)

    print('flow: ')
    for chain in chains:
        IDs = ["_".join(section.get_IDs(model)) for section in chain.sections]
        print(chain.count_symmetry_lines(), chain.flow)

    #  groups_by_size = group_sections_by_size(sections)
    #  print(groups_by_size)

    #  plotter = Plotter(model.name)
    #  plotter.plot_model(model)
    #  plot_sections(plotter, model, sections)
    
    #  plotter = Plotter(model.name)
    #  plotter.plot_model(model)
    #  plot_chains(plotter, model, chains)

    #  groups = group_sections_by_points(sections)
    #  plotter = Plotter(model.name)
    #  plotter.plot_model(model)
    #  title = "group sections by point"
    #  plot_groups(plotter, model, groups, title)

    #  plt.show()

    report_sequence(model)
    report_sequence_rst(model)



def report_sequence_rst(model, filename="model_report.rst"):
    """Generate a sequential RST report of the model."""
    with open(filename, 'w') as file:
        file.write(f"MODEL Report: {model.name}\n")
        file.write("=" * len(f"MODEL Report: {model.name}") + "\n\n")

        file.write(".. list-table:: Sequence\n")
        file.write("   :header-rows: 1\n\n")
        file.write("   * - Label\n     - <\n     - >\n     - Classes\n     - Parents\n     - Equation\n")

        for el, details in model.items():
            el_classes = ', '.join(details.classes.keys())
            el_parents = ', '.join(
                [f":math:`{model[parent].label}`" for parent in details.parents.keys()]
            )

            label = f":math:`{details.label}`"
            row = [
                label,
                "",
                "",
                el_classes,
                el_parents,
                "",
            ]
            if isinstance(el, spg.Point):
                row[1] = f":math:`{sp.latex(el.x)}`"
                row[2] = f":math:`{sp.latex(el.y)}`"

            elif isinstance(el, spg.Line):
                pt_1, pt_2 = el.points
                row[1] = f":math:`{model[pt_1].label or pt_1}`"
                row[2] = f":math:`{model[pt_2].label or pt_2}`"
                row[5] = f":math:`{sp.latex(el.equation())}`"

            elif isinstance(el, spg.Circle):
                pt_center = el.center
                pt_radius = details.pt_radius
                row[1] = f":math:`{model[pt_center].label or pt_center}`"
                row[2] = f":math:`{model[pt_radius].label or pt_radius}`"
                row[5] = f":math:`{sp.latex(el.equation())}`"

            elif isinstance(el, spg.Segment) or isinstance(el, spg.Polygon):
                vertices = ', '.join([f":math:`{model[pt].label or pt}`" for pt in el.vertices])
                row[1] = vertices

            file.write("   * - " + "\n     - ".join(row) + "\n")




if __name__ == "__main__":
    run()
