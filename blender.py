import bpy
from mathutils import Color
import os

obdata = bpy.context.object
obdata = bpy.context.selected_objects # Comment out to export all objects, not just selected ones

all_objects = [ o for o in bpy.context.scene.objects]
all_objects = [ o for o in bpy.context.selected_objects] # Comment out to export all objects, not just selected ones
objects=[]

for object in all_objects:
    for s in object.material_slots:
        material=object.material_slots[0].material
        nodes=material.node_tree.nodes
        principled=next(n for n in nodes if n.type == 'BSDF_PRINCIPLED')
        base_color = principled.inputs['Base Color']
        value = base_color.default_value
        color = Color((value[0], value[1], value[2])).hsv
    
    vertices=[]
    edges=[]
    faces=[]

    for v in object.data.vertices:
        vertices.append([v.co.x,v.co.z,-v.co.y])

    for f in object.data.polygons:
        face=[]
        for v in f.vertices:
            face.append(vertices[int(format(v))])
        faces.append(face)
    faces.append([object.name,object.location,color])
    objects.append(faces)

f = open('desmos_file.txt','w')
    
for object in objects:
    f.write('[\n')
    position = object[-1][1]
    color=object[-1][2]
    for face in object[:-1]:
        f.write('[1,{},{},{},\n'.format(round(color[0]*360,3),round(color[1],3),round(color[2],3)))
        i = 0
        face.reverse()
        for vertex in face:
            x_coord = round(vertex[0]+position[2],3)
            y_coord = round(vertex[1]+position[2],3)
            z_coord = round(vertex[2]+position[2],3)
            if i != len(face)-1:
                f.write('{},{},{},\n'.format(x_coord,y_coord,z_coord))
            else:
                f.write('{},{},{}],'.format(x_coord,y_coord,z_coord))
            i += 1
    f.seek(0, os.SEEK_END)
    f.seek(f.tell()-1, os.SEEK_SET)
    f.truncate()
    f.write('\n]')
f.close()
