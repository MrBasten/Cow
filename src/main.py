import utils
from argparse import ArgumentParser


def main(args, path, out_path):
    input_obj = utils.load_trimesh_obj(f"{path}/input/correct_rocket.stl")
    print("input_obj Done")
    union_mesh = utils.union_itself(args, input_obj)
    print("union_itself Done")
    manifold_mesh = utils.manifold(args, union_mesh, depth=3)
    print("manifold Done")
    assembling_mesh = utils.assembling(args, manifold_mesh)
    print("assembling Done")
    pyacvd_mesh = utils.pyacvd_process(args, assembling_mesh)
    print("pyacvd_process  Done")
    utils.smoothing(pyacvd_mesh, out_path)
    print("smoothing  Done")
    print("All Done")


if __name__ == "__main__":
    parser = ArgumentParser(description="Case for mesh_tessellation")
    parser.add_argument(
        "-f",
        "--folder",
        action="store_true",
        help="Use the argument if you want to create folders with intermediate results",
    )
    args = parser.parse_args()
    print(args)
    main(
        args,
        path=r"C:\Users\HP\Desktop\work\mesh_tessellation_tool",
        out_path=r"C:\Users\HP\Desktop\work\mesh_tessellation_tool\output",
    )
