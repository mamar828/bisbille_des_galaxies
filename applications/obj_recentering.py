from src.engine.material_loader import MaterialLoader
from src.engine.relative_paths import get_path


ml = MaterialLoader()
ml.recenter_obj_file(
    input_path=get_path("objects/tie_fighter/processed_tie_c.obj"),
    output_path=get_path("objects/tie_fighter/processed_tie.obj")
)
