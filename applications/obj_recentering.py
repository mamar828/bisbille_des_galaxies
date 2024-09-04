from src.engine.material_loader import MaterialLoader
from src.engine.relative_paths import get_path


ml = MaterialLoader()
ml.recenter_obj_file(
    input_path=get_path("objects/corvette/Star wars CORVETTE.obj"),
    output_path=get_path("objects/corvette/Star Wars CORVETTE centered.obj")
)
