from src.engine.material_loader import MaterialLoader
from src.engine.relative_paths import get_path


ml = MaterialLoader()
ml.recenter_obj_file(
    input_path=get_path("objects/imperial_shuttle/processed_imperial_shuttle_ver1.obj"),
    output_path=get_path("objects/imperial_shuttle/processed_imperial_shuttle_ver1_centered.obj")
)
