import numpy as np
import vtk
from vtk.util import numpy_support

def numpy_to_vtk_image_data(numpy_array: np.ndarray):
    # Ensure the array is 3-dimensional
    if numpy_array.ndim != 3:
        raise ValueError("numpy_array.ndim != 3")
    
    # Get array dimensions
    depth, height, width = numpy_array.shape
    
    # Create VTK image data object
    vtk_image = vtk.vtkImageData()
    vtk_image.SetDimensions(width, height, depth)
    vtk_image.SetSpacing(1.0, 1.0, 1.0)
    vtk_image.SetOrigin(0.0, 0.0, 0.0)
    
    # Convert numpy array to VTK data array
    vtk_data = numpy_support.numpy_to_vtk(
        num_array=numpy_array.ravel(), 
        deep=True, 
        array_type=vtk.VTK_SHORT
    )
    
    # Set scalar data for VTK image data
    vtk_image.GetPointData().SetScalars(vtk_data)
    
    return vtk_image

def visualize_volume(data: np.ndarray, 
    value_rgba_color_map=[
        (-5.0, 0.0, 0.0,   0.8, 0.9), # Dark blue
        (-4.0, 0.5, 0.0,   0.5, 0.9), # Purple
        (-3.0, 1.0, 0.0,   1.0, 0.9), # Magenta
        (-2.0, 0.0, 1.0,   1.0, 0.9), # Cyan
        (-1.0, 0.0, 0.8,   0.0, 0.9), # Dark green
        ( 0.0, 0.0, 0.0,   0.0, 0.0), # Transparent
        ( 1.0, 1.0, 0.0,   0.0, 0.9), # Red
        ( 2.0, 1.0, 0.843, 0.0, 0.9), # Gold
    ], 
    back_ground_color=(0.1, 0.2, 0.3), # Dark slate blue background
    back_ground_alpha=1.0
):
    """
    Visualize a 3D numpy array using VTK with custom color mapping:
        -1 = green, +1 = red, 0 = transparent, 2 = yellow
        -2 = cyan, -3 = magenta, -4 = purple, -5 = dark blue
    
    Keyboard controls (VTK default interaction):
        q: Exit
        Left mouse button: Rotate
        Middle mouse button: Pan
        Right mouse button: Zoom
        w/s/a/d: Camera rotation
    
    Args:
        data: 3D numpy array containing values ranging from -5 to 2
    """
    # Data initialization
    image_data = numpy_to_vtk_image_data(data)

    # Create volume mapper
    volume_mapper = vtk.vtkGPUVolumeRayCastMapper()
    volume_mapper.SetInputData(image_data)

    # Create volume property
    volume_property = vtk.vtkVolumeProperty()

    # Set opacity transfer function
    opacity_transfer_function = vtk.vtkPiecewiseFunction()
    for v, _, _, _, a in value_rgba_color_map:
        opacity_transfer_function.AddPoint(v, a)
    volume_property.SetScalarOpacity(opacity_transfer_function)

    # Set color transfer function
    color_transfer_function = vtk.vtkColorTransferFunction()
    for v, r, g, b, _ in value_rgba_color_map:
        color_transfer_function.AddRGBPoint(v, r, g, b)
    volume_property.SetColor(color_transfer_function)

    # Enable shading effect
    volume_property.ShadeOn()

    # Create volume object
    volume = vtk.vtkVolume()
    volume.SetMapper(volume_mapper)
    volume.SetProperty(volume_property)

    # Create rendering components
    renderer = vtk.vtkRenderer()
    render_window = vtk.vtkRenderWindow()
    render_window.AddRenderer(renderer)
    render_window_interactor = vtk.vtkRenderWindowInteractor()
    render_window_interactor.SetRenderWindow(render_window)

    # Use VTK default interactor style
    interactor_style = vtk.vtkInteractorStyleTrackballCamera()
    render_window_interactor.SetInteractorStyle(interactor_style)

    # Add volume to renderer
    renderer.SetBackground(*back_ground_color)
    renderer.SetLayer(0)
    renderer.AddVolume(volume)
    renderer.SetBackgroundAlpha(back_ground_alpha)

    # Adjust initial camera position
    renderer.ResetCamera()
    camera = renderer.GetActiveCamera()
    camera.Elevation(30.0)
    camera.Azimuth(30.0)
    renderer.ResetCameraClippingRange()

    # Start visualization
    render_window.SetWindowName("Volume Visualization")
    render_window.SetAlphaBitPlanes(0)
    render_window.SetSize(1024, 768)
    render_window.Render()

    # Initialize interactor
    render_window_interactor.Initialize()
    render_window_interactor.Start()