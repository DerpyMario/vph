bl_info = {
	"name": "Import Compile Heart MDLX (.mdl/.mdlx)",
	"description": "Import Compile Heart MDLX model data.",
	"author": "(^_^)",
	"version": (0, 0, 15),
	"blender": (2, 80, 0),
	"location": "File > Import > Compile Heart MDLX (.mdl/.mdlx)",
	"warning": "Under construction.",
	"wiki_url" : "",
	"tracker_url" : "",
	"category": "Import-Export",
}

"""
This script imports Compile Heart MDLX (.mdl/.mdlx)
"""



import bpy
import bmesh
from bpy.props import ( StringProperty, BoolProperty, EnumProperty )
import os
import struct
import mathutils
import math


string_data_size             = 0
bone_id_table_size           = 0
num_bones                    = 0
num_sub_parts                = 0
num_parts                    = 0
vertex_data_size             = 0
face_data_size               = 0
vertex_data_desc_size        = 0
morph_data_size              = 0
have_morph_data              = 0

string_data                  = []
string_offset                = []

bone_id_table                = []
bone_rotation                = []
bone_translation             = []
bone_scale                   = []
bone_names                   = []
bone_parent_ids              = []
bone_joint_orientation       = []
bone_matrix2                 = []

sub_part_num_vertices        = []
sub_part_face_vertex_index   = []
sub_part_num_face_vertices   = []
sub_part_vertex_index        = []

part_sub_part_index          = []
part_num_sub_parts           = []
part_vertex_data_offset      = []
part_vertex_data_size        = []
part_vertex_unit_size        = []
part_face_data_offset        = []
part_face_data_size          = []
part_face_data_var_type      = []
part_vertex_data_desc_index  = []
part_bone_id_table_index     = []
part_num_bone_ids            = []
part_material_id             = []

part_vertex_index            = []
part_face_index              = []

part_have_tangents           = []
part_have_binormals          = []
part_have_colors             = []
part_have_texture_uvs        = []
part_have_weights            = []

max_have_tangents            = 0
max_have_binormals           = 0
max_have_colors              = 0
max_have_texture_uvs         = 0
max_have_weights             = 0

vertex_data_offset           = 0
face_data_offset             = 0
vertex_data_desc_offset      = 0

vertex_data_desc_cont_or_end = []
vertex_data_desc_data_offset = []
vertex_data_desc_num_data    = []
vertex_data_desc_var_type    = []
vertex_data_desc_data_type   = []

mesh_vertices                = []
mesh_normals                 = []
mesh_tangent                 = []
mesh_tangent2                = []
mesh_binormal                = []
mesh_binormal2               = []
mesh_colors                  = []
mesh_colors2                 = []
mesh_texture_uv              = []
mesh_texture_uv2             = []
mesh_bone_indices            = []
mesh_weights                 = []

mesh_faces                   = []

morph_data_offset            = 0
num_shapes                   = 0
morph_num_sub_parts          = 0
morph_names                  = []
morph_sub_part_indices       = []
morph_sub_part_num_vertices  = []
morph_data                   = []

texture_cfg                  = dict()



def read_uint8(fin):
	return struct.unpack("<B", fin.read(1))[0]



def read_uint16(fin):
	return struct.unpack("<H", fin.read(2))[0]



def read_uint32(fin):
	return struct.unpack("<L", fin.read(4))[0]



def read_float(fin):
	return struct.unpack("<f", fin.read(4))[0]



def read_string(fin):
	result = ""
	while True:
		c = struct.unpack("<B", fin.read(1))[0]
		if c == 0:
			break
		result += chr(c)

	return result



def init_variables():
	global string_data_size
	global bone_id_table_size
	global num_bones
	global num_sub_parts
	global num_parts
	global vertex_data_size
	global face_data_size
	global vertex_data_desc_size
	global morph_data_size
	global have_morph_data

	global string_data
	global string_offset

	global bone_id_table
	global bone_rotation
	global bone_translation
	global bone_scale
	global bone_names
	global bone_parent_ids
	global bone_joint_orientation
	global bone_matrix2

	global sub_part_num_vertices
	global sub_part_face_vertex_index
	global sub_part_num_face_vertices
	global sub_part_vertex_index

	global part_sub_part_index
	global part_num_sub_parts
	global part_vertex_data_offset
	global part_vertex_data_size
	global part_vertex_unit_size
	global part_face_data_offset
	global part_face_data_size
	global part_face_data_var_type
	global part_vertex_data_desc_index
	global part_bone_id_table_index
	global part_num_bone_ids
	global part_material_id

	global part_vertex_index
	global part_face_index

	global part_have_tangents
	global part_have_binormals
	global part_have_colors
	global part_have_texture_uvs
	global part_have_weights

	global max_have_tangents
	global max_have_binormals
	global max_have_colors
	global max_have_texture_uvs
	global max_have_weights

	global vertex_data_offset
	global face_data_offset
	global vertex_data_desc_offset

	global vertex_data_desc_cont_or_end
	global vertex_data_desc_data_offset
	global vertex_data_desc_num_data
	global vertex_data_desc_var_type
	global vertex_data_desc_data_type

	global mesh_vertices
	global mesh_normals
	global mesh_tangent
	global mesh_tangent2
	global mesh_binormal
	global mesh_binormal2
	global mesh_colors
	global mesh_colors2
	global mesh_texture_uv
	global mesh_texture_uv2
	global mesh_bone_indices
	global mesh_weights

	global mesh_faces

	global morph_data_offset
	global num_shapes
	global morph_num_sub_parts
	global morph_names
	global morph_sub_part_indices
	global morph_sub_part_num_vertices
	global morph_data

	global texture_cfg

	string_data_size             = 0
	bone_id_table_size           = 0
	num_bones                    = 0
	num_sub_parts                = 0
	num_parts                    = 0
	vertex_data_size             = 0
	face_data_size               = 0
	vertex_data_desc_size        = 0
	morph_data_size              = 0
	have_morph_data              = 0

	string_data                  = []
	string_offset                = []

	bone_id_table                = []
	bone_rotation                = []
	bone_translation             = []
	bone_scale                   = []
	bone_names                   = []
	bone_parent_ids              = []
	bone_joint_orientation       = []
	bone_matrix2                 = []

	sub_part_num_vertices        = []
	sub_part_face_vertex_index   = []
	sub_part_num_face_vertices   = []
	sub_part_vertex_index        = []

	part_sub_part_index          = []
	part_num_sub_parts           = []
	part_vertex_data_offset      = []
	part_vertex_data_size        = []
	part_vertex_unit_size        = []
	part_face_data_offset        = []
	part_face_data_size          = []
	part_face_data_var_type      = []
	part_vertex_data_desc_index  = []
	part_bone_id_table_index     = []
	part_num_bone_ids            = []
	part_material_id             = []

	part_vertex_index            = []
	part_face_index              = []

	part_have_tangents           = []
	part_have_binormals          = []
	part_have_colors             = []
	part_have_texture_uvs        = []
	part_have_weights            = []

	max_have_tangents            = 0
	max_have_binormals           = 0
	max_have_colors              = 0
	max_have_texture_uvs         = 0
	max_have_weights             = 0

	vertex_data_offset           = 0
	face_data_offset             = 0
	vertex_data_desc_offset      = 0

	vertex_data_desc_cont_or_end = []
	vertex_data_desc_data_offset = []
	vertex_data_desc_num_data    = []
	vertex_data_desc_var_type    = []
	vertex_data_desc_data_type   = []

	mesh_vertices                = []
	mesh_normals                 = []
	mesh_tangent                 = []
	mesh_tangent2                = []
	mesh_binormal                = []
	mesh_binormal2               = []
	mesh_colors                  = []
	mesh_colors2                 = []
	mesh_texture_uv              = []
	mesh_texture_uv2             = []
	mesh_bone_indices            = []
	mesh_weights                 = []

	mesh_faces                   = []

	morph_data_offset            = 0
	num_shapes                   = 0
	morph_num_sub_parts          = 0
	morph_names                  = []
	morph_sub_part_indices       = []
	morph_sub_part_num_vertices  = []
	morph_data                   = []

	texture_cfg.clear()

	return 0



def read_string_data(fin):
	global string_data_size
	global string_data
	global string_offset

	offset = 0

	while offset < string_data_size:
		name = read_string(fin)
		if name != "":
			string_offset.append(offset)
			string_data.append(name)
			offset += len(name) + 1
		else:
			offset += 1

	print("string data")
	for i, name in enumerate(string_data):
		print("{0:08X}: [{1}]".format(string_offset[i], name))

	return 0



def string_offset_to_string(offset):
	global string_data
	global string_offset

	for i, o in enumerate(string_offset):
		if o == offset:
			return string_data[i]

	return ""



def read_bones(fin):
	global bone_id_table
	global bone_rotation
	global bone_translation
	global bone_scale
	global bone_names
	global bone_parent_ids

	if bone_id_table_size != 0:
		for i in range(bone_id_table_size // 2):
			bone_id_table.append(read_uint16(fin))

	for i in range(num_bones):
		if prop["file_type"] == 'TYPE_VTUNE' or prop["file_type"] == 'TYPE_MARY2':
			fin.seek(0x4, os.SEEK_CUR)
			string_offset   = read_uint32(fin)
			parent_id       = read_uint16(fin)
			sub_bone_id     = read_uint16(fin)
			sub_bone_id_end = read_uint16(fin)
			fin.seek(0x2, os.SEEK_CUR)
			rot = []
			rot.append(read_float(fin))
			rot.append(read_float(fin))
			rot.append(read_float(fin))
			rot.append(read_float(fin))
			trans = []
			trans.append(read_float(fin))
			trans.append(read_float(fin))
			trans.append(read_float(fin))
			scale = []
			scale.append(read_float(fin))
			scale.append(read_float(fin))
			scale.append(read_float(fin))
			fin.seek(0x8, os.SEEK_CUR)
		else:
			rot = []
			rot.append(read_float(fin))
			rot.append(read_float(fin))
			rot.append(read_float(fin))
			rot.append(read_float(fin))
			trans = []
			trans.append(read_float(fin))
			trans.append(read_float(fin))
			trans.append(read_float(fin))
			scale = []
			scale.append(read_float(fin))
			scale.append(read_float(fin))
			scale.append(read_float(fin))
			string_offset   = read_uint32(fin)
			parent_id       = read_uint16(fin)
			sub_bone_id     = read_uint16(fin)
			sub_bone_id_end = read_uint16(fin)
			fin.seek(0xE, os.SEEK_CUR)

		bone_rotation.append(rot)
		bone_translation.append(trans)
		bone_scale.append(scale)
		bone_names.append(string_offset_to_string(string_offset))
		bone_parent_ids.append(parent_id)

	for i in range(num_bones):
		row1 = []
		row2 = []
		row3 = []
		row4 = []
		row1.append(read_float(fin))
		row1.append(read_float(fin))
		row1.append(read_float(fin))
		row1.append(read_float(fin))
		row2.append(read_float(fin))
		row2.append(read_float(fin))
		row2.append(read_float(fin))
		row2.append(read_float(fin))
		row3.append(read_float(fin))
		row3.append(read_float(fin))
		row3.append(read_float(fin))
		row3.append(read_float(fin))
		row4.append(read_float(fin))
		row4.append(read_float(fin))
		row4.append(read_float(fin))
		row4.append(read_float(fin))
		bone_joint_orientation.append(mathutils.Matrix([row1, row2, row3, row4]))

	for i in range(num_bones):
		row1 = []
		row2 = []
		row3 = []
		row4 = []
		row1.append(read_float(fin))
		row1.append(read_float(fin))
		row1.append(read_float(fin))
		row1.append(read_float(fin))
		row2.append(read_float(fin))
		row2.append(read_float(fin))
		row2.append(read_float(fin))
		row2.append(read_float(fin))
		row3.append(read_float(fin))
		row3.append(read_float(fin))
		row3.append(read_float(fin))
		row3.append(read_float(fin))
		row4.append(read_float(fin))
		row4.append(read_float(fin))
		row4.append(read_float(fin))
		row4.append(read_float(fin))
		bone_matrix2.append(mathutils.Matrix([row1, row2, row3, row4]))

	if bone_id_table_size != 0:
		print("bone_id_table[{0}]".format(bone_id_table_size // 2))
		for i in range(bone_id_table_size // 2):
			print("[{0}][{1}]".format(bone_id_table[i], bone_names[bone_id_table[i]]))

	return 0



def read_sub_parts_data(fin):
	global prop

	global num_sub_parts
	global sub_part_num_vertices
	global sub_part_face_vertex_indices
	global sub_part_num_face_vertices
	global sub_part_vertex_indices

	for i in range(num_sub_parts):
		fin.seek(0x8, os.SEEK_CUR)
		sub_part_num_vertices.append(read_uint32(fin))
		sub_part_face_vertex_index.append(read_uint32(fin))
		sub_part_num_face_vertices.append(read_uint32(fin))
		sub_part_vertex_index.append(read_uint32(fin))
		if prop["file_type"] == 'TYPE_VIIR' or prop["file_type"] == 'TYPE_MARY2':
			fin.seek(0x158, os.SEEK_CUR)
		else:
			fin.seek(0x168, os.SEEK_CUR)

	print("sub parts[{0}]".format(num_sub_parts))
	for i in range(num_sub_parts):
		print("[{0}]".format(i))
		print("\t# of vertices      = {0}".format(sub_part_num_vertices[i]))
		print("\tface vertex index  = {0}".format(sub_part_face_vertex_index[i]))
		print("\t# of face vertices = {0}".format(sub_part_num_face_vertices[i]))
		print("\tvertex index       = {0}".format(sub_part_vertex_index[i]))

	return 0



def read_parts_data(fin):
	global prop

	global num_parts
	global part_sub_part_index
	global part_num_sub_parts
	global part_vertex_data_offset
	global part_vertex_data_size
	global part_vertex_unit_size
	global part_face_data_offset
	global part_face_data_size
	global part_face_data_var_type
	global part_vertex_data_desc_index
	global part_bone_id_table_index
	global part_num_bone_ids
	global part_material_id

	for i in range(num_parts):
		part_sub_part_index.append(read_uint32(fin))
		part_num_sub_parts.append(read_uint32(fin))
		part_vertex_data_offset.append(read_uint32(fin))
		part_vertex_data_size.append(read_uint32(fin))
		part_vertex_unit_size.append(read_uint32(fin))
		part_face_data_offset.append(read_uint32(fin))
		part_face_data_size.append(read_uint32(fin))
		part_face_data_var_type.append(read_uint32(fin))
		part_vertex_data_desc_index.append(read_uint32(fin))
		part_bone_id_table_index.append(read_uint32(fin))
		part_num_bone_ids.append(read_uint32(fin))
		part_material_id.append(read_uint32(fin))
		if prop["file_type"] == 'TYPE_VIIR' or prop["file_type"] == 'TYPE_MARY2':
			fin.seek(0x4, os.SEEK_CUR)
		else:
			fin.seek(0x8, os.SEEK_CUR)

	print("parts[{0}]".format(num_parts))
	for i in range(num_parts):
		print("[{0}]".format(i))
		print("\tsub part index         = {0}".format(part_sub_part_index[i]))
		print("\t# of sub parts         = {0}".format(part_num_sub_parts[i]))
		print("\tvertex data offset     = 0x{0:08X}".format(part_vertex_data_offset[i]))
		print("\tvertex data size       = 0x{0:08X}".format(part_vertex_data_size[i]))
		print("\tvertex unit size       = 0x{0:X}".format(part_vertex_unit_size[i]))
		print("\tface data offset       = 0x{0:08X}".format(part_face_data_offset[i]))
		print("\tface data size         = 0x{0:08X}".format(part_face_data_size[i]))
		print("\tface data var type     = 0x{0:08X}".format(part_face_data_var_type[i]))
		print("\tvertex data desc index = 0x{0:08X}".format(part_vertex_data_desc_index[i]))
		print("\tbone id table index    = {0}".format(part_bone_id_table_index[i]))
		print("\t# of bone ids          = {0}".format(part_num_bone_ids[i]))
		print("\tmaterial id ?          = {0}".format(part_material_id[i]))

	return 0

def read_vertex_data_desc(fin):
	global num_parts
	global part_vertex_unit_size
	global part_vertex_data_desc_index

	global part_have_tangents
	global part_have_binormals
	global part_have_colors
	global part_have_texture_uvs
	global part_have_weights

	global max_have_tangents
	global max_have_binormals
	global max_have_colors
	global max_have_texture_uvs
	global max_have_weights

	global vertex_data_desc_size
	global vertex_data_desc_offset

	global vertex_data_desc_cont_or_end
	global vertex_data_desc_data_offset
	global vertex_data_desc_num_data
	global vertex_data_desc_var_type
	global vertex_data_desc_data_type

	fin.seek(vertex_data_desc_offset, os.SEEK_SET)

	num_vertex_data_desc = vertex_data_desc_size // 8
	for i in range(num_vertex_data_desc):
		vertex_data_desc_cont_or_end.append(read_uint16(fin))
		vertex_data_desc_data_offset.append(read_uint16(fin))
		vertex_data_desc_num_data.append(read_uint8(fin))
		vertex_data_desc_var_type.append(read_uint8(fin))
		vertex_data_desc_data_type.append(read_uint16(fin))

	for i in range(num_parts):
		have_coordinate = 0
		have_weight     = 0
		have_normal     = 0
		have_color      = 0
		have_color2     = 0
		have_bone_index = 0
		have_uv         = 0
		have_uv2        = 0
		have_tangent2   = 0
		have_binormal2  = 0
		have_tangent    = 0
		have_binormal   = 0

		j = part_vertex_data_desc_index[i]
		if j < 0 or num_vertex_data_desc <= j:
			print("ERROR: part[{0}] vertex data desc index={1}".format(i, j))
			return -1

		while vertex_data_desc_cont_or_end[j] == 0x0000:
			data_size = 0

			if vertex_data_desc_data_type[j] == 0x0001:
				# weight
				if not (vertex_data_desc_var_type[j] == 0x04 and vertex_data_desc_num_data[j] == 4):
					print("ERROR: vertex data desc[{0}] data type={1:04X}, var type={2:02X}, # of data={3}".format(j, vertex_data_desc_data_type[j], vertex_data_desc_var_type[j], vertex_data_desc_num_data[j]))
					raise ValueError()
				data_size = 1
			elif vertex_data_desc_data_type[j] == 0x0003 or vertex_data_desc_data_type[j] == 0x0004:
				# color or color2
				if not (vertex_data_desc_var_type[j] == 0x14 and vertex_data_desc_num_data[j] == 4):
					print("ERROR: vertex data desc[{0}] data type={1:04X}, var type={2:02X}, # of data={3}".format(j, vertex_data_desc_data_type[j], vertex_data_desc_var_type[j], vertex_data_desc_num_data[j]))
					raise ValueError()
				data_size = 1
			elif vertex_data_desc_data_type[j] == 0x0007:
				# bone index
				if not (vertex_data_desc_var_type[j] == 0x07 and vertex_data_desc_num_data[j] == 4):
					print("ERROR: vertex data desc[{0}] data type={1:04X}, var type={2:02X}, # of data={3}".format(j, vertex_data_desc_data_type[j], vertex_data_desc_var_type[j], vertex_data_desc_num_data[j]))
					raise ValueError()
				data_size = 1
			elif vertex_data_desc_data_type[j] == 0x0008 or vertex_data_desc_data_type[j] == 0x0009:
				# uv or uv2
				if not (vertex_data_desc_var_type[j] == 0x02 and vertex_data_desc_num_data[j] == 2):
					print("ERROR: vertex data desc[{0}] data type={1:04X}, var type={2:02X}, # of data={3}".format(j, vertex_data_desc_data_type[j], vertex_data_desc_var_type[j], vertex_data_desc_num_data[j]))
					raise ValueError()
				data_size = 4
			else:
				if not (vertex_data_desc_var_type[j] == 0x02 and vertex_data_desc_num_data[j] == 3):
					print("ERROR: vertex data desc[{0}] data type={1:04X}, var type={2:02X}, # of data={3}".format(j, vertex_data_desc_data_type[j], vertex_data_desc_var_type[j], vertex_data_desc_num_data[j]))
					raise ValueError()
				data_size = 4

			data_size *= vertex_data_desc_num_data[j]
			#print("DEBUG: part_vertex_unit_size[{0}] = {1:X}".format(i, part_vertex_unit_size[i]))
			#print("DEBUG: vertex_data_desc_data_offset[{0}] = {1:X}, data_size={2:X}, {3:X}".format(j, vertex_data_desc_data_offset[j], data_size, vertex_data_desc_data_offset[j] + data_size))
			if part_vertex_unit_size[i] < vertex_data_desc_data_offset[j] + data_size:
				print("ERROR: vertex data desc[{0}] illegal offset or data size".format(j))
				raise ValueError()

			if vertex_data_desc_data_type[j] == 0x0000:
				have_coordinate = 1
			elif vertex_data_desc_data_type[j] == 0x0001:
				have_weight = 1
			elif vertex_data_desc_data_type[j] == 0x0002:
				have_normal = 1
			elif vertex_data_desc_data_type[j] == 0x0003:
				have_color = 1
			elif vertex_data_desc_data_type[j] == 0x0004:
				have_color2 = 1
			elif vertex_data_desc_data_type[j] == 0x0007:
				have_bone_index = 1
			elif vertex_data_desc_data_type[j] == 0x0008:
				have_uv = 1
			elif vertex_data_desc_data_type[j] == 0x0009:
				have_uv2 = 1
			elif vertex_data_desc_data_type[j] == 0x000C:
				have_tangent2 = 1
			elif vertex_data_desc_data_type[j] == 0x000D:
				have_binormal2 = 1
			elif vertex_data_desc_data_type[j] == 0x000E:
				have_tangent = 1
			elif vertex_data_desc_data_type[j] == 0x000F:
				have_binormal = 1
			else:
				print("ERROR: vertex data desc[{0}] unknown data type".format(j))
				raise ValueError()

			j += 1

		# tangents
		if have_tangent == 1:
			if have_tangent2 == 1:
				part_have_tangents.append(2)
			else:
				part_have_tangents.append(1)
		elif have_tangent2 == 1:
			print("ERROR: part[{0}] have tangents2 but not have tangents".format(i))
			raise ValueError()
		else:
			part_have_tangents.append(0)

		# binormals
		if have_binormal == 1:
			if have_binormal2 == 1:
				part_have_binormals.append(2)
			else:
				part_have_binormals.append(1)
		elif have_binormal2 == 1:
			print("ERROR: part[{0}] have binormals2 but not have binormals".format(i))
			raise ValueError()
		else:
			part_have_binormals.append(0)

		# colors
		if have_color == 1:
			if have_color2 == 1:
				part_have_colors.append(2)
			else:
				part_have_colors.append(1)
		elif have_color2 == 1:
			print("ERROR: part[{0}] have color2 but not have color".format(i))
			raise ValueError()
		else:
			part_have_colors.append(0)

		# uvs
		if have_uv == 1:
			if have_uv2 == 1:
				part_have_texture_uvs.append(2)
			else:
				part_have_texture_uvs.append(1)
		elif have_uv2 == 1:
			print("ERROR: part[{0}] have uv2 but not have uv".format(i))
			raise ValueError()
		else:
			part_have_texture_uvs.append(0)

		# weights
		if have_weight == 1:
			if have_bone_index == 1:
				part_have_weights.append(4)
			else:
				print("ERROR: part[{0}] have weight but not have bone index".format(i))
				raise ValueError()
		elif have_bone_index == 1:
			print("ERROR: part[{0}] have bone index but not have weight".format(i))
			raise ValueError()
		else:
			part_have_weights.append(0)

		if max_have_tangents < part_have_tangents[i]:
			max_have_tangents = part_have_tangents[i]
		if max_have_binormals < part_have_binormals[i]:
			max_have_binormals = part_have_binormals[i]
		if max_have_colors < part_have_colors[i]:
			max_have_colors = part_have_colors[i]
		if max_have_texture_uvs < part_have_texture_uvs[i]:
			max_have_texture_uvs = part_have_texture_uvs[i]
		if max_have_weights < part_have_weights[i]:
			max_have_weights = part_have_weights[i]

	return 0

def read_vertices(fin):
	global num_parts
	global part_vertex_data_offset
	global part_vertex_data_size
	global part_vertex_unit_size
	global part_vertex_index
	global part_bone_id_table_index

	global part_have_tangents
	global part_have_binormals
	global part_have_colors
	global part_have_texture_uvs
	global part_have_weights

	global max_have_tangents
	global max_have_binormals
	global max_have_colors
	global max_have_texture_uvs
	global max_have_weights

	global bone_names

	global vertex_data_desc_cont_or_end
	global vertex_data_desc_data_offset
	global vertex_data_desc_num_data
	global vertex_data_desc_var_type
	global vertex_data_desc_data_type

	global mesh_vertices
	global mesh_normals
	global mesh_tangent
	global mesh_tangent2
	global mesh_binormal
	global mesh_binormal2
	global mesh_colors
	global mesh_colors2
	global mesh_texture_uv
	global mesh_texture_uv2
	global mesh_bone_indices
	global mesh_weights

	for i in range(num_parts):
		fin.seek(vertex_data_offset + part_vertex_data_offset[i], os.SEEK_SET)

		part_vertex_index.append(len(mesh_vertices))
		num_vertices = part_vertex_data_size[i] // part_vertex_unit_size[i]

		print("[{0}] # of vertices = {1}".format(i, num_vertices))
		for j in range(num_vertices):
			vertex = []
			vertex.append(read_float(fin))
			vertex.append(read_float(fin))
			vertex.append(read_float(fin))

			normal = []
			normal.append(read_float(fin))
			normal.append(read_float(fin))
			normal.append(read_float(fin))

			tangent = []
			tangent.append(read_float(fin))
			tangent.append(read_float(fin))
			tangent.append(read_float(fin))

			tangent2 = []
			if part_have_tangents[i] == 2:
				tangent2.append(read_float(fin))
				tangent2.append(read_float(fin))
				tangent2.append(read_float(fin))
			elif max_have_tangents == 2:
				# Z軸+向き
				tangent2.append(0.0)
				tangent2.append(0.0)
				tangent2.append(1.0)

			binormal = []
			binormal.append(read_float(fin))
			binormal.append(read_float(fin))
			binormal.append(read_float(fin))

			binormal2 = []
			if part_have_binormals[i] == 2:
				binormal2.append(read_float(fin))
				binormal2.append(read_float(fin))
				binormal2.append(read_float(fin))
			elif max_have_binormals == 2:
				# X軸+向き
				binormals2.append(1.0)
				binormals2.append(0.0)
				binormals2.append(0.0)

			color = []
			color2 = []
			if part_have_colors[i] != 0:
				# red, green, blue, alpha
				color.append(read_uint8(fin))
				color.append(read_uint8(fin))
				color.append(read_uint8(fin))
				color.append(read_uint8(fin))

				if part_have_colors[i] == 2:
					# red, green, blue, alpha
					color2.append(read_uint8(fin))
					color2.append(read_uint8(fin))
					color2.append(read_uint8(fin))
					color2.append(read_uint8(fin))
				elif max_have_colors == 2:
					color2.append(0)
					color2.append(0)
					color2.append(0)
					color2.append(0)
			elif max_have_colors != 0:
				color.append(0)
				color.append(0)
				color.append(0)
				color.append(0)
				if max_have_colors == 2:
					color2.append(0)
					color2.append(0)
					color2.append(0)
					color2.append(0)

			texture_uv = []
			texture_uv.append(read_float(fin))
			texture_uv.append(read_float(fin))

			texture_uv2 = []
			if part_have_texture_uvs[i] == 2:
				texture_uv2.append(read_float(fin))
				texture_uv2.append(read_float(fin))
			elif max_have_texture_uvs == 2:
				texture_uv2.append(0.0)
				texture_uv2.append(0.0)

			bone_indices = []
			weights = []
			if part_have_weights[i] != 0:
				for k in range(4):
					bone_indices.append(read_uint8(fin))
				for k in range(4):
					weights.append(read_uint8(fin))

			mesh_vertices.append(vertex)
			mesh_normals.append(normal)

			mesh_tangent.append(tangent)
			if max_have_tangents == 2:
				mesh_tangent2.append(tangent2)

			mesh_binormal.append(binormal)
			if max_have_binormals == 2:
				mesh_binormal2.append(binormal2)

			if max_have_colors != 0:
				mesh_colors.append(color)
				if max_have_colors == 2:
					mesh_colors2.append(color2)

			mesh_texture_uv.append(texture_uv)
			if max_have_texture_uvs == 2:
				mesh_texture_uv2.append(texture_uv2)

			if part_have_weights[i] != 0:
				mesh_bone_indices.append(bone_indices)
				mesh_weights.append(weights)

	return 0


def read_faces(fin):
	global num_parts
	global part_face_data_offset
	global part_face_data_size
	global part_face_data_var_type
	global part_face_index

	global mesh_faces

	for i in range(num_parts):
		fin.seek(face_data_offset + part_face_data_offset[i], os.SEEK_SET)

		part_face_index.append(len(mesh_faces))
		if part_face_data_var_type[i] == 2:
			num_faces = part_face_data_size[i] // 12

			print("[{0}] # of faces = {1}".format(i, num_faces))
			for j in range(num_faces):
				face_verts = []
				face_verts.append(read_uint32(fin))
				face_verts.append(read_uint32(fin))
				face_verts.append(read_uint32(fin))
				mesh_faces.append(face_verts)
		else:
			num_faces = part_face_data_size[i] // 6

			print("[{0}] # of faces = {1}".format(i, num_faces))
			for j in range(num_faces):
				face_verts = []
				face_verts.append(read_uint16(fin))
				face_verts.append(read_uint16(fin))
				face_verts.append(read_uint16(fin))
				mesh_faces.append(face_verts)

	return 0



def read_morph_data(fin):
	global morph_data_offset
	global num_shapes
	global morph_num_sub_parts
	global morph_names
	global morph_sub_part_indices
	global morph_sub_part_num_vertices
	global morph_data

	fin.seek(morph_data_offset, os.SEEK_SET)

	unknown             = read_uint32(fin)
	num_shapes          = read_uint32(fin)
	morph_num_sub_parts = read_uint32(fin)

	print("{0:08X}: morph data".format(morph_data_offset))
	print("unknown        = 0x{0:08X}".format(unknown))
	print("# of shapes    = {0}".format(num_shapes))
	print("# of sub parts = {0}".format(morph_num_sub_parts))

	for i in range(num_shapes):
		morph_names.append(read_string(fin))
		print("[{0}] {1}".format(i, morph_names[i]))

	fin.seek(4 * num_shapes, os.SEEK_CUR)
	#for i in range(num_shapes):
	#	unknown = read_uint32(fin)
	#	print("0x{0:08X}".format(unknown))

	for i in range(morph_num_sub_parts):
		sub_part_index      = read_uint32(fin)
		data_size_per_shape = read_uint32(fin)
		total_data_size     = read_uint32(fin)
		unknown             = read_uint32(fin)
		num_vertices        = read_uint32(fin)

		morph_sub_part_indices.append(sub_part_index)
		morph_sub_part_num_vertices.append(num_vertices)

		print("[{0}]".format(i))
		print("\tsub part index      = {0}".format(sub_part_index))
		print("\tdata size per shape = 0x{0:08X}".format(data_size_per_shape))
		print("\ttotal data size     = 0x{0:08X}".format(total_data_size))
		print("\tunknown             = 0x{0:08X}".format(unknown))
		print("\t# of vertices       = {0}".format(num_vertices))

		sub_part_data      = []

		for j in range(num_shapes):
			#print("\t[{0}] {1}".format(j, morph_names[j]))

			shape_data      = []

			for k in range(num_vertices):
				# +00 coordinate x
				# +04 coordinate y
				# +08 coordinate z
				# +0C not used x 3
				# +18 color red   = 255.0 - vertex color red
				# +1C color green = 255.0 - vertex color green
				# +20 color blue  = 255.0 - vertex color blue
				# +24 not used x 9
				x = read_float(fin)
				y = read_float(fin)
				z = read_float(fin)
				fin.seek(0x3C, os.SEEK_CUR)

				shape_data.append([ x, y, z ])

			sub_part_data.append(shape_data)

		morph_data.append(sub_part_data)



def read_mdlx_cfg(filepath):
	global texture_cfg

	cfg_file = filepath + ".cfg"
	if not os.path.exists(cfg_file):
		return

	try:
		fin = open(cfg_file, "r")
		lines = fin.readlines()
		fin.close()

		for line in lines:
			params = line.split()
			if 2 <= len(params):
				if params[0] == "game":
					if params[1] == "viir" or params[1] == "varnir" or params[1] == "derq":
						prop["file_type"] = 'TYPE_VIIR'
					elif params[1] == "derq2":
						prop["file_type"] = 'TYPE_DERQ2'
					elif params[1] == "nepvs" or params[1] == "vtune":
						prop["file_type"] = 'TYPE_VTUNE'
					elif params[1] == "mary2":
						prop["file_type"] = 'TYPE_MARY2'
					continue
			if len(params) < 3:
				continue
			if params[1] not in [ "diffuse", "diffuse2", "occlusion", "rgb", "rgb2", "metallic", "specular", "roughness", "sheen", "clearcoat", "emission", "alpha", "normal" ]:
				continue
			img_file = params[2]

			if os.sep == "/":
				if img_file[0] != "/":
					# 相対パス
					img_file = os.path.join(os.path.dirname(filepath), img_file)
			else:
				if img_file[0] == "\\" or img_file[0] == "/":
					# ドライブ無し
					img_file = filepath[0:2] + img_file
				elif len(img_file) < 2 or img_file[1] != ":":
					# 相対パス
					img_file = os.path.join(os.path.dirname(filepath), img_file)

			if os.path.splitext(img_file)[1] == "":
				if os.path.exists(img_file + ".png"):
					img_file = img_file + ".png"
				elif os.path.exists(img_file + ".dds"):
					img_file = img_file + ".dds"
				else:
					continue
			elif not os.path.exists(img_file):
				continue
			cfg_key = params[0] + "\t" + params[1]
			texture_cfg[cfg_key] = img_file
	except:
		texture_cfg.clear()



def adjust_uv(texture_uv, i, i2):
	global sub_part_num_vertices
	global sub_part_face_vertex_index
	global sub_part_num_face_vertices
	global sub_part_vertex_index

	global part_sub_part_index
	global part_vertex_index
	global part_face_index

	global mesh_vertices
	global mesh_faces

	sub_part_index   = part_sub_part_index[i] + i2

	sub_vertex_index = sub_part_vertex_index[sub_part_index]
	vertex_index     = part_vertex_index[i] + sub_vertex_index
	num_vertices     = sub_part_num_vertices[sub_part_index]

	face_index       = part_face_index[i] + sub_part_face_vertex_index[sub_part_index] // 3
	num_faces        = sub_part_num_face_vertices[sub_part_index] // 3

	min_u = math.inf
	min_v = math.inf
	max_u = -math.inf
	max_v = -math.inf

	for j in range(num_vertices):
		u = texture_uv[vertex_index + j][0]
		v = texture_uv[vertex_index + j][1]
		if u < min_u:
			min_u = u
		if max_u < u:
			max_u = u
		if v < min_v:
			min_v = v
		if max_v < v:
			max_v = v

	floor_min_u = math.floor(min_u)
	floor_min_v = math.floor(min_v)
	ceil_max_u  = math.ceil(max_u)
	ceil_max_v  = math.ceil(max_v)

	# U座標を一括調節
	if floor_min_u != 0.0 and ceil_max_u - floor_min_u <= 1.0:
		print("INFORMATION: [{0}][{1}] sub parts[{2}] adjust texture u coordinates: u -= {3:f}".format(i, i2, sub_part_index, floor_min_u))
		for j in range(num_vertices):
			texture_uv[vertex_index + j][0] -= floor_min_u
		ceil_max_u -= floor_min_u
		floor_min_u = 0.0

	# V座標を一括調節
	if floor_min_v != 0.0 and ceil_max_v - floor_min_v <= 1.0:
		print("INFORMATION: [{0}][{1}] sub parts[{2}] adjust texture v coordinates: v -= {3:f}".format(i, i2, sub_part_index, floor_min_v))
		for j in range(num_vertices):
			texture_uv[vertex_index + j][1] -= floor_min_v
		ceil_max_v -= floor_min_v
		floor_min_v = 0.0

	# 面毎にUV座標の範囲を調べて可能であれば0.0〜1.0の範囲内に移動する
	if 1.0 < ceil_max_u - floor_min_u or 1.0 < ceil_max_v - floor_min_v:
		new_u = dict()
		new_v = dict()
		counter_u = dict()
		counter_v = dict()
		found_u = False
		found_v = False

		for j in range(num_faces):
			face_verts = mesh_faces[face_index + j]

			min_u2 = math.inf
			min_v2 = math.inf
			max_u2 = -math.inf
			max_v2 = -math.inf

			for k in range(3):
				u = texture_uv[part_vertex_index[i] + face_verts[k]][0]
				v = texture_uv[part_vertex_index[i] + face_verts[k]][1]
				if u < min_u2:
					min_u2 = u
				if max_u2 < u:
					max_u2 = u
				if v < min_v2:
					min_v2 = v
				if max_v2 < v:
					max_v2 = v

			floor_min_u2 = math.floor(min_u2)
			floor_min_v2 = math.floor(min_v2)
			ceil_max_u2  = math.ceil(max_u2)
			ceil_max_v2  = math.ceil(max_v2)

			if floor_min_u2 in counter_u.keys():
				counter_u[floor_min_u2] += 1
			else:
				counter_u[floor_min_u2] = 1

			if floor_min_v2 in counter_v.keys():
				counter_v[floor_min_v2] += 1
			else:
				counter_v[floor_min_v2] = 1

			found = False
			if 1.0 < ceil_max_u2 - floor_min_u2:
				found_u = True
				found = True
			elif floor_min_u2 != 0.0:
				for k in range(3):
					u = texture_uv[part_vertex_index[i] + face_verts[k]][0]
					new_u[part_vertex_index[i] + face_verts[k]] = u - floor_min_u2

			if 1.0 < ceil_max_v2 - floor_min_v2:
				found_v = True
				found = True
			elif floor_min_v2 != 0.0:
				for k in range(3):
					v = texture_uv[part_vertex_index[i] + face_verts[k]][1]
					new_v[part_vertex_index[i] + face_verts[k]] = v - floor_min_v2

			if found:
				print("WARNING: [{0}][{1}] sub parts[{2}] ".format(i, i2, sub_part_index), end="")
				print("faces[{0} + {1} = {2}] = [ {3} {4} {5} ]".format(face_index, j, face_index + j, face_verts[0], face_verts[1], face_verts[2]))
				for k in range(3):
					print("vertices[{0} + {1} = {2}] ".format(part_vertex_index[i], face_verts[k], part_vertex_index[i] + face_verts[k]), end="")
					co = mesh_vertices[part_vertex_index[i] + face_verts[k]]
					print("co [ {0:9.6f} {1:9.6f} {2:9.6f} ] ".format( co[0], co[1], co[2] ), end="")
					uv = texture_uv[part_vertex_index[i] + face_verts[k]]
					print("uv [ {0:9.6f} {1:9.6f} ]".format( uv[0], uv[1] ))

		# U座標を調節する
		if 1.0 < ceil_max_u - floor_min_u:
			if len(new_u) != 0 and not found_u:
				# 個別調節
				print("INFORMATION: [{0}][{1}] sub parts[{2}] adjust texture u coordinates: u -= {3:f}".format(i, i2, sub_part_index, floor_min_u))
				print("INFORMATION: vertices:", end="")
				columns = 0
				for k in new_u.keys():
					if 10 <= columns:
						columns = 0
						print("")
						print("                      ", end="")
					print(" {0:5d}".format(k - part_vertex_index[i]), end="")
					columns += 1
					texture_uv[k][0] = new_u[k]
				print("")
			else:
				# 多数値で調節
				new_floor_min_u = floor_min_u
				count = 0
				for k in counter_u.keys():
					if count < counter_u[k]:
						count = counter_u[k]
						new_floor_min_u = k

				# U座標を一括調節
				if new_floor_min_u != 0.0:
					ceil_max_u += new_floor_min_u - floor_min_u
					floor_min_u = new_floor_min_u
					print("INFORMATION: [{0}][{1}] sub parts[{2}] adjust texture u coordinates: u -= {3:f}".format(i, i2, sub_part_index, floor_min_u))
					for j in range(num_vertices):
						texture_uv[vertex_index + j][0] -= floor_min_u
					ceil_max_u -= floor_min_u
					floor_min_u = 0.0

		# V座標を調節する
		if 1.0 < ceil_max_v - floor_min_v:
			if len(new_v) != 0 and not found_v:
				# 個別調節
				print("INFORMATION: [{0}][{1}] sub parts[{2}] adjust texture v coordinates: v -= {3:f}".format(i, i2, sub_part_index, floor_min_v))
				print("INFORMATION: vertices:", end="")
				columns = 0
				for k in new_v.keys():
					if 10 <= columns:
						columns = 0
						print("")
						print("                      ", end="")
					print(" {0:5d}".format(k - part_vertex_index[i]), end="")
					columns += 1
					texture_uv[k][1] = new_v[k]
				print("")
			else:
				# 多数値で調節
				new_floor_min_v = floor_min_v
				count = 0
				for k in counter_v.keys():
					if count < counter_v[k]:
						count = counter_v[k]
						new_floor_min_v = k

				# V座標を一括調節
				if new_floor_min_v != 0.0:
					ceil_max_v += new_floor_min_v - floor_min_v
					floor_min_v = new_floor_min_v
					print("INFORMATION: [{0}][{1}] sub parts[{2}] adjust texture v coordinates: v -= {3:f}".format(i, i2, sub_part_index, floor_min_v))
					for j in range(num_vertices):
						texture_uv[vertex_index + j][1] -= floor_min_v
					ceil_max_v -= floor_min_v
					floor_min_v = 0.0

	return 0



def import_mdlx_main(filepath):
	global prop

	global string_data_size
	global bone_id_table_size
	global num_bones
	global num_sub_parts
	global num_parts
	global vertex_data_size
	global face_data_size
	global vertex_data_desc_size
	global morph_data_size
	global have_morph_data

	global sub_part_num_vertices
	global sub_part_face_vertex_index
	global sub_part_num_face_vertices
	global sub_part_vertex_index

	global part_sub_part_index
	global part_num_sub_parts
	global bone_id_table
	global bone_rotation
	global bone_translation
	global bone_scale
	global bone_names
	global bone_parent_ids

	global part_vertex_index
	global part_face_index

	global vertex_data_offset
	global face_data_offset
	global vertex_data_desc_offset

	global mesh_vertices
	global mesh_normals
	global mesh_tangent
	global mesh_tangent2
	global mesh_binormal
	global mesh_binormal2
	global mesh_colors
	global mesh_colors2
	global mesh_texture_uv
	global mesh_texture_uv2
	global mesh_bone_indices
	global mesh_weights

	global mesh_faces

	global morph_data_offset
	global num_shapes
	global morph_num_sub_parts
	global morph_names
	global morph_sub_part_indices
	global morph_sub_part_num_vertices
	global morph_data

	global texture_cfg

	init_variables()

	read_mdlx_cfg(filepath)

	fin = open(filepath, "rb")

	string_data_size      = read_uint32(fin)
	bone_id_table_size    = read_uint32(fin)
	num_bones             = read_uint32(fin)
	fin.seek(0xC, os.SEEK_CUR)
	num_sub_parts         = read_uint32(fin)
	num_parts             = read_uint32(fin)
	vertex_data_size      = read_uint32(fin)
	face_data_size        = read_uint32(fin)
	vertex_data_desc_size = read_uint32(fin)

	morph_data_size = 0
	have_morph_data = 0
	if prop["file_type"] == 'TYPE_DERQ2' or prop["file_type"] == 'TYPE_VTUNE':
		morph_data_size = read_uint32(fin)
		have_morph_data = read_uint32(fin)

	read_string_data(fin)
	if prop["file_type"] == 'TYPE_VIIR' or prop["file_type"] == 'TYPE_MARY2':
		fin.seek(0x2C + string_data_size, os.SEEK_SET)
	else:
		fin.seek(0x34 + string_data_size, os.SEEK_SET)
	read_bones(fin)
	read_sub_parts_data(fin)
	read_parts_data(fin)

	vertex_data_offset      = fin.tell()
	face_data_offset        = vertex_data_offset + vertex_data_size
	vertex_data_desc_offset = face_data_offset + face_data_size

	read_vertex_data_desc(fin)
	read_vertices(fin)
	read_faces(fin)

	if prop["file_type"] == 'TYPE_VTUNE' and morph_data_size != 0:
		morph_data_offset = vertex_data_desc_offset + vertex_data_desc_size
		read_morph_data(fin)

	fin.close()

	# 既存オブジェクトの選択を全て解除
	scene = bpy.context.scene
	for obj in scene.collection.objects:
		obj.select_set(False)

	if bpy.ops.object.mode_set.poll():
		bpy.ops.object.mode_set(mode='OBJECT')

	obj_name = bpy.path.display_name_from_filepath(filepath)

	armature = bpy.data.armatures.new(obj_name)
	a_obj = bpy.data.objects.new(armature.name, armature)
	a_obj.location = scene.cursor.location
	scene.collection.objects.link(a_obj)
	bpy.context.view_layer.objects.active = a_obj
	bpy.ops.object.mode_set(mode='EDIT', toggle=False)
	armature.display_type = 'STICK'


	# ボーン追加
	bone_transform = []
	for i in range(num_bones):
		name = bone_names[i]
		#print("bones[{0}] {1}".format(i, name))

		bone_joint_orientation[i].row[3] = [ 0.0, 0.0, 0.0, 1.0 ]

		mat = mathutils.Matrix.Identity(4)

		if not (bone_rotation[i][0] == 0.0 and bone_rotation[i][1] == 0.0 and bone_rotation[i][2] == 0.0 and bone_rotation[i][3] == 1.0):
			# 回転の向きが逆のようなので反転する
			mat = mathutils.Quaternion([bone_rotation[i][3], bone_rotation[i][0], bone_rotation[i][1], bone_rotation[i][2]]).inverted().to_matrix().to_4x4()

		mat @= bone_joint_orientation[i]

		mat.row[3][0] = bone_translation[i][0]
		mat.row[3][1] = bone_translation[i][1]
		mat.row[3][2] = bone_translation[i][2]
		mat.row[3][3] = 1.0

		if bone_parent_ids[i] != 0xFFFF:
			mat @= bone_transform[bone_parent_ids[i]]

		pos = [ mat.row[3][0], mat.row[3][1], mat.row[3][2] ]

		eb = armature.edit_bones.new(name)
		eb.transform(mat)
		bone_transform.append(mat)

		eb.head = [ pos[0], -pos[2], pos[1] ]
		eb.tail = [ pos[0], -pos[2], pos[1] + 0.001 ]

		if bone_parent_ids[i] != 0xFFFF:
			eb.parent = armature.edit_bones[bone_names[bone_parent_ids[i]]]
			eb.use_connect = False

	mesh = None
	new_obj = None
	bm = None

	material_names = dict()

	# シェープキー連動用
	ref_obj = None
	driver_data_paths = []

	loaded_images = dict()
	for i in range(num_parts):
		if part_material_id[i] not in material_names:
			material_name = obj_name + '.' + str(part_material_id[i])
			mat = bpy.data.materials.new(material_name)
			material_names[part_material_id[i]] = mat.name
			mat.use_nodes = True
			bsdf = mat.node_tree.nodes['Principled BSDF']
			mat.use_backface_culling = True
			#mat.blend_method = 'HASHED'
			mat.blend_method = 'BLEND'
			mat.shadow_method = 'HASHED'
			mat.alpha_threshold = 0.5
			mat.show_transparent_back = False

			diffuse_node = None
			diffuse_node2 = None
			occlusion_node = None
			metallic_node = None
			specular_node = None
			clearcoat_node = None
			alpha_node = None
			rgb_node = None
			rgb_node2 = None

			for texture_type in [ "diffuse", "diffuse2", "occlusion", "rgb", "rgb2", "metallic", "specular", "roughness", "sheen", "clearcoat", "emission", "alpha", "normal" ]:
				cfg_key = str(part_material_id[i]) + "\t" + texture_type
				if cfg_key in texture_cfg:
					image_file = texture_cfg[cfg_key]
					if image_file in loaded_images:
						img = loaded_images[image_file]
					else:
						try:
							img = bpy.data.images.load(image_file)
							loaded_images[image_file] = img
						except:
							print("Cannot load image {0}".format(image_file))
							continue

					img_node = mat.node_tree.nodes.new(type='ShaderNodeTexImage')
					img_node.image = img
					if texture_type == "diffuse":
						img_node.location = ( -500, 750 )
						diffuse_node = img_node
					elif texture_type == "diffuse2":
						img_node.location = ( -500, 750 )
						diffuse_node2 = img_node
					elif texture_type == "occlusion":
						img_node.location = ( -500, 450 )
						occlusion_node = img_node
					elif texture_type == "rgb":
						img_node.location = ( -500, 70 )
						rgb_node = mat.node_tree.nodes.new(type='ShaderNodeSeparateRGB')
						rgb_node.location = ( -190, 70 )
						mat.node_tree.links.new(rgb_node.inputs['Image'], img_node.outputs['Color'])
					elif texture_type == "rgb2":
						img_node.location = ( -1000, 150 )
						rgb_node2 = mat.node_tree.nodes.new(type='ShaderNodeSeparateRGB')
						rgb_node2.location = ( -690, 150 )
						mat.node_tree.links.new(rgb_node2.inputs['Image'], img_node.outputs['Color'])
					elif texture_type == "metallic":
						img_node.location = ( -1000, 450 )
						metallic_node = img_node
					elif texture_type == "specular":
						img_node.location = ( -1300, 350 )
						specular_node = img_node
					elif texture_type == "roughness":
						img_node.location = ( -1300, 50 )
						mat.node_tree.links.new(bsdf.inputs['Roughness'], img_node.outputs['Color'])
					elif texture_type == "sheen":
						img_node.location = ( -1000, -150 )
						mat.node_tree.links.new(bsdf.inputs['Sheen'], img_node.outputs['Color'])
					elif texture_type == "clearcoat":
						img_node.location = ( -1300, -450 )
						clearcoat_node = img_node
					elif texture_type == "emission":
						img_node.location = ( -1000, -450 )
						mat.node_tree.links.new(bsdf.inputs['Emission'], img_node.outputs['Color'])
					elif texture_type == "alpha":
						img_node.location = ( -700, -450 )
						alpha_node = img_node
					elif texture_type == "normal":
						img_node.location = ( -400, -450 )
						mat.node_tree.links.new(bsdf.inputs['Normal'], img_node.outputs['Color'])

			if occlusion_node is not None:
				dn = None
				if diffuse_node is not None:
					dn = diffuse_node
				elif diffuse_node2 is not None:
					dn = diffuse_node2
				if dn is not None:
					vec_node = mat.node_tree.nodes.new(type='ShaderNodeVectorMath')
					vec_node.location = ( -190, 450 )
					vec_node.operation = 'MULTIPLY'
					mat.node_tree.links.new(vec_node.inputs[0], dn.outputs['Color'])
					mat.node_tree.links.new(vec_node.inputs[1], occlusion_node.outputs['Color'])
					mat.node_tree.links.new(bsdf.inputs['Base Color'], vec_node.outputs[0])
			elif diffuse_node is not None:
				mat.node_tree.links.new(bsdf.inputs['Base Color'], diffuse_node.outputs['Color'])
			elif diffuse_node2 is not None:
				mat.node_tree.links.new(bsdf.inputs['Base Color'], diffuse_node2.outputs['Color'])

			if metallic_node is not None:
				mat.node_tree.links.new(bsdf.inputs['Metallic'], metallic_node.outputs['Color'])
			elif rgb_node2 is not None:
				mat.node_tree.links.new(bsdf.inputs['Metallic'], rgb_node2.outputs['G'])

			if specular_node is not None:
				mat.node_tree.links.new(bsdf.inputs['Specular'], specular_node.outputs['Color'])
			elif rgb_node is not None:
				mat.node_tree.links.new(bsdf.inputs['Specular'], rgb_node.outputs['R'])

			if clearcoat_node is not None:
				mat.node_tree.links.new(bsdf.inputs['Clearcoat'], clearcoat_node.outputs['Color'])
			elif rgb_node2 is not None:
				mat.node_tree.links.new(bsdf.inputs['Clearcoat'], rgb_node2.outputs['R'])

			if diffuse_node2 is not None:
				mat.node_tree.links.new(bsdf.inputs['Alpha'], diffuse_node2.outputs['Alpha'])
			elif alpha_node is not None:
				mat.node_tree.links.new(bsdf.inputs['Alpha'], alpha_node.outputs['Color'])

			if rgb_node is not None:
				#mat.node_tree.links.new(bsdf.inputs['???'], rgb_node.outputs['G'])
				pass

			if rgb_node2 is not None:
				#mat.node_tree.links.new(bsdf.inputs['???'], rgb_node2.outputs['B'])
				pass

		mat = bpy.data.materials[material_names[part_material_id[i]]]

		for i2 in range(part_num_sub_parts[i]):
			sub_part_index   = part_sub_part_index[i] + i2

			sub_vertex_index = sub_part_vertex_index[sub_part_index]
			vertex_index     = part_vertex_index[i] + sub_vertex_index
			num_vertices     = sub_part_num_vertices[sub_part_index]

			face_index       = part_face_index[i] + sub_part_face_vertex_index[sub_part_index] // 3
			num_faces        = sub_part_num_face_vertices[sub_part_index] // 3

			print("[{0}][{1}] sub parts[{2}]".format(i, i2, sub_part_index))
			print("vertex index     = {0}".format(vertex_index))
			print("sub vertex index = {0}".format(sub_vertex_index))
			print("# of vertices    = {0}".format(num_vertices))
			print("face index       = {0}".format(face_index))
			print("# of faces       = {0}".format(num_faces))

			mesh_name = obj_name + ":" + str(i) + ":" + str(i2)
			#mesh_name = obj_name + ":" + str(sub_part_index)
			mesh = bpy.data.meshes.new(mesh_name)
			new_obj = bpy.data.objects.new(mesh.name, mesh)
			new_obj.data.materials.append(mat)

			bm = bmesh.new()

			# 頂点追加
			for j in range(num_vertices):
				co = mesh_vertices[vertex_index + j]
				bm.verts.new([co[0], -co[2], co[1]])	# X軸で90度回転

				bm.verts.ensure_lookup_table()			# verts[インデックス]を使用できるようにする

			# 面追加
			for j in range(num_faces):
				#print("mesh_faces[{0} + {1} = {2}]".format(face_index, j, face_index + j))
				face_verts = mesh_faces[face_index + j]

				# 同じ頂点を複数使用した面や、重複した面を使用しているモデルがある
				try:
					bf = bm.faces.new([bm.verts[face_verts[0] - sub_vertex_index], bm.verts[face_verts[1] - sub_vertex_index], bm.verts[face_verts[2] - sub_vertex_index]])
				except ValueError as e:
					print("ERROR: {0}".format(e.args))
					print("ERROR: faces[{0} + {1} = {2}] = [ {3} {4} {5} ]".format( face_index, j, face_index + j, face_verts[0] - sub_vertex_index, face_verts[1] - sub_vertex_index, face_verts[2] - sub_vertex_index ))
					continue

			bm.to_mesh(mesh)
			bm.free()

			# UV座標調節
			# 0.0〜1.0の範囲内にないとき、可能であれば座標値を変更する
			if prop["adjust_uv_coordinates"]:
				adjust_uv(mesh_texture_uv, i, i2)
				if part_have_texture_uvs[i] == 2:
					adjust_uv(mesh_texture_uv2, i, i2)

			# UV座標
			uv_layer = mesh.uv_layers.new(name='UVMap')
			print("UV layer = [{0}]".format(uv_layer.name))
			for poly in mesh.polygons:
				#print("Polygon index: {0}, length: {1} [".format(poly.index, poly.loop_total), end="")
				for loop_index in range(poly.loop_start, poly.loop_start + poly.loop_total):
					#print(" {0:5d}".format(mesh.loops[loop_index].vertex_index), end="")
					u =       mesh_texture_uv[vertex_index + mesh.loops[loop_index].vertex_index][0]
					v = 1.0 - mesh_texture_uv[vertex_index + mesh.loops[loop_index].vertex_index][1]
					uv_layer.data[loop_index].uv = [ u, v ]
				#print(" ]")

			# UV座標2
			if part_have_texture_uvs[i] == 2:
				uv_layer2 = mesh.uv_layers.new(name='UVMap2')
				print("UV layer = [{0}]".format(uv_layer2.name))
				for poly in mesh.polygons:
					#print("Polygon index: {0}, length: {1} [".format(poly.index, poly.loop_total), end="")
					for loop_index in range(poly.loop_start, poly.loop_start + poly.loop_total):
						#print(" {0:5d}".format(mesh.loops[loop_index].vertex_index), end="")
						u =       mesh_texture_uv2[vertex_index + mesh.loops[loop_index].vertex_index][0]
						v = 1.0 - mesh_texture_uv2[vertex_index + mesh.loops[loop_index].vertex_index][1]
						uv_layer2.data[loop_index].uv = [ u, v ]
					#print(" ]")

			# 頂点カラー
			if part_have_colors[i] != 0:
				color_layer = mesh.vertex_colors.new(name='color')
				print("color layer = [{0}]".format(color_layer.name))
				for poly in mesh.polygons:
					for loop_index in range(poly.loop_start, poly.loop_start + poly.loop_total):
						c = mesh_colors[vertex_index + mesh.loops[loop_index].vertex_index]
						r = c[0] / 255.0
						g = c[1] / 255.0
						b = c[2] / 255.0
						a = c[3] / 255.0
						color_layer.data[loop_index].color = [ r, g, b, a ]

				if part_have_colors[i] == 2:
					color_layer2 = mesh.vertex_colors.new(name='color2')
					print("color layer = [{0}]".format(color_layer2.name))
					for poly in mesh.polygons:
						for loop_index in range(poly.loop_start, poly.loop_start + poly.loop_total):
							c = mesh_colors2[vertex_index + mesh.loops[loop_index].vertex_index]
							r = c[0] / 255.0
							g = c[1] / 255.0
							b = c[2] / 255.0
							a = c[3] / 255.0
							color_layer2.data[loop_index].color = [ r, g, b, a ]

			# 法線のX,Y,Z要素をR,G,B値とした頂点カラーを追加する
			if prop["set_normals_to_vertex_colors"]:
				normal_layer = mesh.vertex_colors.new(name='normal')
				print("normal layer = [{0}]".format(normal_layer.name))
				for poly in mesh.polygons:
					for loop_index in range(poly.loop_start, poly.loop_start + poly.loop_total):
						c = mesh_normals[vertex_index + mesh.loops[loop_index].vertex_index]
						r = ( c[0] + 1.0) / 2
						g = (-c[2] + 1.0) / 2
						b = ( c[1] + 1.0) / 2
						normal_layer.data[loop_index].color = [ r, g, b, 1.0 ]

			# 接線のX,Y,Z要素をR,G,B値とした頂点カラーを追加する
			if prop["set_tangents_to_vertex_colors"]:
				tangent_layer = mesh.vertex_colors.new(name='tangent')
				print("tangent layer = [{0}]".format(tangent_layer.name))
				for poly in mesh.polygons:
					for loop_index in range(poly.loop_start, poly.loop_start + poly.loop_total):
						c = mesh_tangent[vertex_index + mesh.loops[loop_index].vertex_index]
						r = ( c[0] + 1.0) / 2
						g = (-c[2] + 1.0) / 2
						b = ( c[1] + 1.0) / 2
						tangent_layer.data[loop_index].color = [ r, g, b, 1.0 ]

				if part_have_tangents[i] == 2:
					tangent_layer2 = mesh.vertex_colors.new(name='tangent2')
					print("tangent layer = [{0}]".format(tangent_layer2.name))
					for poly in mesh.polygons:
						for loop_index in range(poly.loop_start, poly.loop_start + poly.loop_total):
							c = mesh_tangent2[vertex_index + mesh.loops[loop_index].vertex_index]
							r = ( c[0] + 1.0) / 2
							g = (-c[2] + 1.0) / 2
							b = ( c[1] + 1.0) / 2
							tangent_layer2.data[loop_index].color = [ r, g, b, 1.0 ]

			# 従法線のX,Y,Z要素をR,G,B値とした頂点カラーを追加する
			if prop["set_binormals_to_vertex_colors"]:
				binormal_layer = mesh.vertex_colors.new(name='binormal')
				print("binormal layer = [{0}]".format(binormal_layer.name))
				for poly in mesh.polygons:
					for loop_index in range(poly.loop_start, poly.loop_start + poly.loop_total):
						c = mesh_binormal[vertex_index + mesh.loops[loop_index].vertex_index]
						r = ( c[0] + 1.0) / 2
						g = (-c[2] + 1.0) / 2
						b = ( c[1] + 1.0) / 2
						binormal_layer.data[loop_index].color = [ r, g, b, 1.0 ]

				if part_have_binormals[i] == 2:
					binormal_layer2 = mesh.vertex_colors.new(name='binormal2')
					print("binormal layer = [{0}]".format(binormal_layer2.name))
					for poly in mesh.polygons:
						for loop_index in range(poly.loop_start, poly.loop_start + poly.loop_total):
							c = mesh_binormal2[vertex_index + mesh.loops[loop_index].vertex_index]
							r = ( c[0] + 1.0) / 2
							g = (-c[2] + 1.0) / 2
							b = ( c[1] + 1.0) / 2
							binormal_layer2.data[loop_index].color = [ r, g, b, 1.0 ]

			new_obj.parent = a_obj
			new_obj.parent_type = 'ARMATURE'

			if part_have_weights[i] != 0:
				# 使用しているボーンだけ頂点グループに登録する
				#for j in range(part_num_bone_ids[i]):
				#	bone_id = bone_id_table[part_bone_id_table_index[i] + j]
				#	group_name = bone_names[bone_id]
				#	if group_name != "" and group_name not in new_obj.vertex_groups:
				#		new_obj.vertex_groups.new(name=group_name)
				#		print("vertex group [{0}] added".format(group_name))

				# 全ボーン頂点グループに登録する(カメラ等も登録してしまう副作用あり)
				for group_name in bone_names:
					if group_name != "" and group_name not in new_obj.vertex_groups:
						new_obj.vertex_groups.new(name=group_name)
						#print("vertex group [{0}] added".format(group_name))

				# 頂点ウェイト追加
				for j in range(sub_part_num_vertices[sub_part_index]):
					bone_indices = mesh_bone_indices[vertex_index + j]
					weights      = mesh_weights[vertex_index + j]

					for k in range(4):
						if weights[k] != 0:
							bone_id = bone_id_table[part_bone_id_table_index[i] + bone_indices[k]]
							group_name = bone_names[bone_id]
							if group_name == "":
								# ここには来ないはず
								group_name = "bone_" . str(bone_id)
							if group_name not in new_obj.vertex_groups:
								# ここには来ないはず
								new_obj.vertex_groups.new(name=group_name)
								print("vertex group [{0}] added".format(group_name))
							group = new_obj.vertex_groups[group_name]
							group.add([j], weights[k] / 255.0, 'ADD')

			for poly in mesh.polygons:
				poly.use_smooth = True

			no = []
			#for loop in mesh.loops:
			#	nx =  mesh_normals[vertex_index + loop.vertex_index][0]
			#	ny = -mesh_normals[vertex_index + loop.vertex_index][2]
			#	nz =  mesh_normals[vertex_index + loop.vertex_index][1]
			#	no.append([nx, ny, nz])
			#mesh.normals_split_custom_set(no)
			for j in range(num_vertices):
				nx =  mesh_normals[vertex_index + j][0]
				ny = -mesh_normals[vertex_index + j][2]
				nz =  mesh_normals[vertex_index + j][1]
				no.append([nx, ny, nz])
			mesh.normals_split_custom_set_from_vertices(no)
			mesh.use_auto_smooth = True

			# モーフ
			if prop["file_type"] == 'TYPE_VTUNE' and morph_data_size != 0:
				morph_data_index = -1
				for j in range(morph_num_sub_parts):
					if morph_sub_part_indices[j] == sub_part_index:
						morph_data_index = j
						print("morph_sub_part_indices[{0}] = {1}".format(j, morph_sub_part_indices[j]))
						print("morph_data_index = {0}".format(morph_data_index))
						break

				if 0 <= morph_data_index:
					new_obj.shape_key_add()
					mesh.shape_keys.key_blocks[-1].name = "Basis"
					#print("[{0}][{1}] shape key {2}".format(i, i2, mesh.shape_keys.key_blocks[-1].name))

					sub_part_data       = morph_data[morph_data_index]
					for j in range(num_shapes):
						new_obj.shape_key_add()
						key_block = mesh.shape_keys.key_blocks[-1]
						key_block.name = morph_names[j]
						#print("[{0}][{1}] morph[{2}] shape key {3}".format(i, i2, j, mesh.shape_keys.key_blocks[-1].name))
						shape_data = sub_part_data[j]

						for k in range(morph_sub_part_num_vertices[morph_data_index]):
							co = mesh_vertices[vertex_index + k]
							x =   co[0] + shape_data[k][0]
							y = -(co[2] + shape_data[k][2])
							z =   co[1] + shape_data[k][1]
							key_block.data[k].co = [ x, y, z ]

						# 最初のオブジェクトのシェープキーの値を参照するドライバーを追加する
						if prop["add_drivers_for_shape_keys"]:
							if ref_obj is None:
								driver_data_paths.append('data.shape_keys.key_blocks["{0}"].value'.format(key_block.name))
							else:
								drv = key_block.driver_add('value', -1)
								drv.driver.type = 'SCRIPTED'
								var = drv.driver.variables.new()
								var.name = 'value'
								var.type = 'SINGLE_PROP'
								var.targets[0].id = ref_obj
								var.targets[0].data_path = driver_data_paths[j]
								drv.driver.expression = 'value'

					ref_obj = new_obj

			scene.collection.objects.link(new_obj)
			new_obj.select_set(True)

	# オブジェクト登録完了

	if bpy.context.view_layer.objects.active is None or bpy.context.view_layer.objects.active.mode == 'OBJECT':
		bpy.context.view_layer.objects.active = new_obj

	bpy.ops.object.mode_set(mode='OBJECT')

	# 既存オブジェクトの選択を全て解除
	for obj in scene.collection.objects:
		obj.select_set(False)

	print("import Compile Heart MDLX ... completed")

	init_variables()



class IMPORT_OT_compile_heart_mdlx(bpy.types.Operator):
	"""Load Compile Heart MDLX"""
	bl_idname = "import_mesh.mdlx"
	bl_description = 'Import Compile Heart MDLX (.mdlx)'
	bl_label = "Import MDLX"
	bl_options = {'UNDO'}

	filepath : StringProperty(subtype='FILE_PATH')
	filter_glob : StringProperty(default="*.mdl;*.mdlx", options={'HIDDEN'})

	file_type : EnumProperty(
		name = "Game",
		description = "Specify which game file",
		items = [
			('TYPE_VIIR', "Neptunia VIIR, Dragon Star Varnir, Death end re;Quest", "Neptunia VIIR, Dragon Star Varnir, Death end re;Quest"),
			('TYPE_DERQ2', "Death end re;Quest 2", "Death end re;Quest 2"),
			('TYPE_VTUNE', "Neptunia Virtual Stars", "Neptunia Virtual Stars"),
			('TYPE_MARY2', "Mary Skelter 2", "Mary Skelter 2")
		],
		default = 'TYPE_VIIR'
	)

	adjust_uv_coordinates : BoolProperty(
		name = "Adjust UV Coordinates",
		description = "If the UV coordinates do not fall within the range of 0.0 to 1.0, adjust the coordinates if possible",
		default = True
	)

	set_normals_to_vertex_colors : BoolProperty(
		name = "Set Normals to Vertex Colors",
		description = "Set the normal X, Y, Z elements to the vertex color R, G, B elements",
		default = False
	)

	set_tangents_to_vertex_colors : BoolProperty(
		name = "Set Tangents to Vertex Colors",
		description = "Set the tangent X, Y, Z elements to the vertex color R, G, B elements",
		default = False
	)

	set_binormals_to_vertex_colors : BoolProperty(
		name = "Set Binormals to Vertex Colors",
		description = "Set the binormal X, Y, Z elements to the vertex color R, G, B elements",
		default = False
	)

	add_drivers_for_shape_keys : BoolProperty(
		name = "Add Drivers for Shape Keys",
		description = "Add drivers to link the shape key values of multiple objects.\nChanging the shape key value of the first object will set that value for other objects as well.",
		default = True
	)

	#debug_flag : BoolProperty(
	#	name = "debug flag",
	#	description = "for debugging",
	#	default = False
	#)

	def draw(self, context):
		layout = self.layout
		layout.prop(self, "file_type")
		layout.prop(self, "adjust_uv_coordinates")
		layout.prop(self, "set_normals_to_vertex_colors")
		layout.prop(self, "set_tangents_to_vertex_colors")
		layout.prop(self, "set_binormals_to_vertex_colors")
		layout.prop(self, "add_drivers_for_shape_keys")
		#layout.prop(self, "debug_flag")

	def execute(self, context):
		global prop

		prop = {}
		prop["file_type"] = self.file_type
		prop["adjust_uv_coordinates"] = self.adjust_uv_coordinates
		prop["set_normals_to_vertex_colors"] = self.set_normals_to_vertex_colors
		prop["set_tangents_to_vertex_colors"] = self.set_tangents_to_vertex_colors
		prop["set_binormals_to_vertex_colors"] = self.set_binormals_to_vertex_colors
		prop["add_drivers_for_shape_keys"] = self.add_drivers_for_shape_keys
		#prop["debug_flag"] = self.debug_flag

		import_mdlx_main(self.filepath)

		return {'FINISHED'}

	def invoke(self, context, event):
		wm = context.window_manager
		wm.fileselect_add(self)
		return {'RUNNING_MODAL'}


def menu_func(self, context):
	self.layout.operator(IMPORT_OT_compile_heart_mdlx.bl_idname, text="Compile Heart MDLX (.mdl/.mdlx)")


def register():
	bpy.utils.register_class(IMPORT_OT_compile_heart_mdlx)
	bpy.types.TOPBAR_MT_file_import.append(menu_func)


def unregister():
	bpy.utils.unregister_class(IMPORT_OT_compile_heart_mdlx)
	bpy.types.TOPBAR_MT_file_import.remove(menu_func)


if __name__ == "__main__":
	unregister()
	register()

