import vtkmodules.vtkRenderingOpenGL2
from vtkmodules.vtkCommonColor import vtkNamedColors
from vtkmodules.vtkIOImage import vtkDICOMImageReader
from vtkmodules.vtkInteractionImage import vtkImageViewer2
from vtkmodules.vtkRenderingCore import vtkRenderWindowInteractor
from vtk import *

class DicomCall:
    def __init__(self, path) -> None:
        self.pathName= path

    def dicomFileCall(self):

        #input filename
        filename= self.pathName

        # Read the DICOM file
        reader = vtkDICOMImageReader()
        reader.SetFileName(filename)
        reader.Update()

        image_viewer = vtkImageViewer2()
        image_viewer.SetInputConnection(reader.GetOutputPort())
        

        return reader, image_viewer
    
    def dicomFolderCall(self):
        # call all the folder
        # input folder name
        foldername= self.pathName
        reader = vtkDICOMImageReader()
        reader.SetDirectoryName(foldername)
        reader.Update()

        image_viewer = vtkImageViewer2()
        image_viewer.SetInputConnection(reader.GetOutputPort())

        return reader, image_viewer
    
    def dicom3DCall(self):
        foldername= self.pathName
        reader = vtkDICOMImageReader()
        self.volumeMapper = vtkSmartVolumeMapper() 
        self.volumeProperty = vtkVolumeProperty() 
        self.gradientOpacity = vtkPiecewiseFunction() 
        self.scalarOpacity = vtkPiecewiseFunction() 
        self.color = vtkColorTransferFunction() 
        self.volume = vtkVolume()
        
        reader.SetDirectoryName(foldername)
        reader.SetDataScalarTypeToUnsignedShort() 
        reader.UpdateWholeExtent() 
        reader.Update()
        imageData= vtkImageData() 
        imageData.ShallowCopy(reader.GetOutput())

        self.volumeMapper.SetBlendModeToComposite() 
        self.volumeMapper.SetRequestedRenderModeToGPU() 
        self.volumeMapper.SetInputData(imageData) 
        self.volumeProperty.ShadeOn() 
        self.volumeProperty.SetInterpolationTypeToLinear() 
        self.volumeProperty.SetAmbient(0.1) 
        self.volumeProperty.SetDiffuse(0.9) 
        self.volumeProperty.SetSpecular(0.2) 
        self.volumeProperty.SetSpecularPower(10.0) 
        self.gradientOpacity.AddPoint(0.0, 0.0) 
        self.gradientOpacity.AddPoint(2000.0, 1.0) 
        self.volumeProperty.SetGradientOpacity(self.gradientOpacity)  
        self.scalarOpacity.AddPoint(-800.0, 0.0) 
        self.scalarOpacity.AddPoint(-750.0, 1.0) 
        self.scalarOpacity.AddPoint(-350.0, 1.0) 
        self.scalarOpacity.AddPoint(-300.0, 0.0) 
        self.scalarOpacity.AddPoint(-200.0, 0.0) 
        self.scalarOpacity.AddPoint(-100.0, 1.0) 
        self.scalarOpacity.AddPoint(1000.0, 0.0) 
        self.scalarOpacity.AddPoint(2750.0, 0.0) 
        self.scalarOpacity.AddPoint(2976.0, 1.0) 
        self.scalarOpacity.AddPoint(3000.0, 0.0) 
        self.volumeProperty.SetScalarOpacity(self.scalarOpacity) 
        self.color.AddRGBPoint(-750.0, 0.08, 0.05, 0.03) 
        self.color.AddRGBPoint(-350.0, 0.39, 0.25, 0.16)  
        self.color.AddRGBPoint(-200.0, 0.80, 0.80, 0.80) 
        self.color.AddRGBPoint(2750.0, 0.70, 0.70, 0.70) 
        self.color.AddRGBPoint(3000.0, 0.35, 0.35, 0.35) 
        self.volumeProperty.SetColor(self.color)
        
        self.volume.SetMapper(self.volumeMapper) 
        self.volume.SetProperty(self.volumeProperty)

        return reader, self.volume
    
if __name__=="__main__":
    #for testing the class, for main window please proceed to the our name py
    '''image_viewer = vtkImageViewer2()
    colors = vtkNamedColors()
    #file only
    #image_viewer= DicomCall(r'Assignment2\Pelvis\vhm.401.dcm').dicomFileCall()
    #folder
    image_viewer= DicomCall('Assignment2\Pelvis').dicomFolderCall()
    render_window_interactor = vtkRenderWindowInteractor()
    image_viewer.SetupInteractor(render_window_interactor)
    image_viewer.Render()
    image_viewer.GetRenderer().SetBackground(colors.GetColor3d("SlateGray"))
    image_viewer.GetRenderWindow().SetWindowName("ReadDICOM")
    image_viewer.GetRenderer().ResetCamera()
    image_viewer.Render()
    
    render_window_interactor.Start()'''

    renderWindow = vtkRenderWindow() 
    renderer = vtkRenderer()
    interactorStyle = vtkInteractorStyleTrackballCamera() 
    renderWindowInteractor = vtkRenderWindowInteractor() 

    volume = DicomCall('Assignment2\Pelvis').dicom3DCall()
    renderer.AddVolume(volume) 
    renderer.SetBackground(0.1, 0.2, 0.3) 
    renderWindow.AddRenderer(renderer) 
    renderWindow.SetSize(500, 500) 
    renderWindowInteractor.SetInteractorStyle(interactorStyle) 
    renderWindowInteractor.SetRenderWindow(renderWindow)

    renderWindowInteractor.Start()


