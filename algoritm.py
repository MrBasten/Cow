import trimesh
#import pycork
import numpy as np
import os
from pathlib import Path
from typing import Union
import pyvista
import pyacvd
import meshio


def save_to_obj(path, file_name):
    mesh = trimesh.load(path)
    out_path = '/home/admin/Desktop/Alg_final/Output_data/{}.obj'.format(file_name)
    trimesh.exchange.export.export_mesh(mesh, out_path, 'obj')
    return out_path

def save_to_stl(path, file_name):
    mesh = trimesh.load(path)
    out_path = '/home/admin/Desktop/Alg_final/Output_data/{}.stl'.format(file_name)
    trimesh.exchange.export.export_mesh(mesh, out_path, 'stl')
    return out_path

def union_itself(mesh: trimesh.base.Trimesh) -> trimesh.base.Trimesh:
    connected_groups = mesh.split(only_watertight= False)
    verts = [m.vertices for m in connected_groups if m.is_watertight]
    tris = [m.faces for m in connected_groups if m.is_watertight]
    for m in connected_groups:
        a = 0
        if not(m.is_watertight):
            trimesh.exchange.export.export_mesh(m, 'Output_data\\{}.obj'.format(a), 'obj')
            a += 1
    vert_tmp, tris_tmp = pycork.union(verts[0], tris[0], 
                                         verts[1], tris[1])
    if len(connected_groups) == 2:
        mesh_res = trimesh.Trimesh(vertices=vert_tmp, faces=tris_tmp, process=True)
        
    elif len(connected_groups) > 2:
        for v, t in zip(verts[2:], tris[2:]):
            vert_tmp, tris_tmp = pycork.union(vert_tmp, tris_tmp, v, t)
        
        mesh_res = trimesh.Trimesh(vertices=vert_tmp, faces=tris_tmp, process=True)

    trimesh.exchange.export.export_mesh(mesh_res, 'Output_data\\out{}.obj'.format(a + 1), 'obj')


def load_trimesh_obj(path: Union[str, os.PathLike]) -> trimesh.Trimesh:
    obj = trimesh.load(path)
    if type(obj) == trimesh.base.Trimesh:
        return obj
    elif type(obj) == trimesh.scene.scene.Scene:
        yourList = obj.geometry.items()
        vertice_list = [mesh.vertices for _, mesh in yourList]
        faces_list = [mesh.faces for _, mesh in yourList]
        faces_offset = np.cumsum([v.shape[0] for v in vertice_list])
        faces_offset = np.insert(faces_offset, 0, 0)[:-1]

        vertices = np.vstack(vertice_list)
        faces = np.vstack([face + offset for face, offset in zip(faces_list, faces_offset)])

        merged__meshes = trimesh.Trimesh(vertices, faces)
        return merged__meshes
    else:
        raise Exception('Unknown type of extension!')


def manifold(Path):
    for filename in os.scandir(Path):
         if filename.is_file():
            os.system('./ManifoldPlus --input {} --output {} --depth 8'.format(filename, 'manifold_' + filename))

def smoothing(Path):
    for filename in os.scandir(Path):
        if filename.is_file() and 'manifold_' in filename:
            mesh = trimesh.load(filename)
            for i in range(10):
                trimesh.smoothing.filter_humphrey(mesh)
            mesh.export('smooth' + filename)

def pyacvd_process(Path):
    for filename in os.scandir(Path):
        a = 0
        if filename.is_file() and 'smooth' in filename:
            cow = pyvista.PolyData()
            clus = pyacvd.Clustering(cow)
            clus.subdivide(3)
            clus.cluster(20000)
            remesh = clus.create_mesh()
            pyvista.save_meshio('out_file{}.obj'.format(a), remesh, file_format='obj')
            a += 1

def assembling(Path):
    final_object = trimesh.scene.scene.Scene()
    for filename in os.scandir(Path):
        if filename.is_file() and 'out_file' in filename:
            final_object.add_geometry('{}\\{}'.format(Path, filename))
    yourList = obj.geometry.items()
    vertice_list = [mesh.vertices for _, mesh in yourList]
    faces_list = [mesh.faces for _, mesh in yourList]
    faces_offset = np.cumsum([v.shape[0] for v in vertice_list])
    faces_offset = np.insert(faces_offset, 0, 0)[:-1]
    vertices = np.vstack(vertice_list)
    faces = np.vstack([face + offset for face, offset in zip(faces_list, faces_offset)])
    merged__meshes = trimesh.Trimesh(vertices, faces)
    return merged__meshes
