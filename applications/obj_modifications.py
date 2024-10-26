from src.engine.material_loader import MaterialLoader
from src.engine.relative_paths import get_path


# MaterialLoader.recenter_obj_file(
#     input_path=get_path("objects/slave/Star Wars slave.obj"),
#     output_path=get_path("objects/slave/Star Wars slave.obj")
# )

# MaterialLoader.fix_invalid_vertex_format(
#     input_path=get_path("objects/corvette/CR90_New.obj"),
#     output_path=get_path("objects/corvette/CR90_New.obj")
# )

MaterialLoader.fix_index_out_of_range(
    input_path=get_path("objects/corvette/CR90_New.obj"),
    output_path=get_path("objects/corvette/CR90_New_2.obj")
)
