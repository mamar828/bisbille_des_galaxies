from src.engine.material_loader import MaterialLoader
from src.engine.relative_paths import get_path


input_path = get_path("objects/a_wing/a_wing.obj")
output_path = get_path("objects/a_wing/a_wing.obj")

MaterialLoader.recenter_obj_file(
    input_path=input_path,
    output_path=output_path,
)

# MaterialLoader.fix_invalid_vertex_format(
#     input_path=input_path,
#     output_path=output_path,
# )

# MaterialLoader.fix_index_out_of_range(
#     input_path=input_path,
#     output_path=input_path,
# )
