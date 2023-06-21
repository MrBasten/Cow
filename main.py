import algoritm
import trimesh

def main(Path, Path_to_outfile= 'Output_data'):
    input_obj = algoritm.load_trimesh_obj(Path)
    union_obj = algoritm.union_itself(input_obj)
    algoritm.manifold(Path_to_outfile) 
    algoritm.smoothing(Path_to_outfile)
    algoritm.pyacvd_process(Path_to_outfile)
    final_mesh = algoritm.assembling(Path_to_outfile)
    trimesh.exchange.export.export_mesh(final_mesh, 'Triang_rocket.obj', 'obj')
    trimesh.exchange.export.export_mesh(final_mesh, 'Triang_rocket.stl', 'stl')
        
if __name__ == '__main__':
    main(Path = 'check_obj\\correct_rocket.stl')
