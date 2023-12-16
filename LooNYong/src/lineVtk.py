import vtk
import math

# this is the class for main python to call the modified vtk interactor style in draw line and measure
class CustomInteractorStyle(vtk.vtkInteractorStyleImage):
    def __init__(self):
        # add the observer for can calculate the measure purpose
        self.AddObserver("LeftButtonPressEvent", self.LeftButtonPressEvent)
        self.AddObserver("MouseMoveEvent",self.MouseMoveEvent)
        
        # set initial 
        self.start_point = None
        self.end_point = None 
        self.drawing= False
        
    def LeftButtonPressEvent(self, obj, event):
        if self.drawing:
            #get position when clicked second time
            click_pos = self.GetInteractor().GetEventPosition()
            self.end_point=click_pos

            # create the finalize line
            self.line_source.SetPoint1((self.start_point[0],self.start_point[1],0))
            self.line_source.SetPoint2((self.end_point[0],self.end_point[1],0))
            self.line_source.Update()
            
            # get the length between two line and show the length
            length = self.calculate_length()
            self.display_length(length)
            
            # add actor 
            self.renderer.AddActor(self.line_actor)
            self.renderer.AddActor(self.length_text)
            self.render_window.Render()
            self.drawing= False
            self.start_point = None

        else:
            # start drawing from here
            self.line_source = vtk.vtkLineSource()
            self.line_mapper = vtk.vtkPolyDataMapper2D()
            self.line_actor = vtk.vtkActor2D()
            
            self.line_mapper.SetInputConnection(self.line_source.GetOutputPort())
            self.line_actor.SetMapper(self.line_mapper)
            self.line_actor.GetProperty().SetColor(1.0, 0.0, 0.0)

            self.length_text = vtk.vtkTextActor()
            self.length_text.GetTextProperty().SetColor(1.0, 1.0, 1.0) 
            click_pos = self.GetInteractor().GetEventPosition()
            self.start_point = click_pos
            self.drawing= True
        
        return self.OnLeftButtonDown()

    
    def MouseMoveEvent(self,  obj, event):
        if self.drawing:
            # to constanly show line after first mouse click
            click_pos = self.GetInteractor().GetEventPosition()
            self.end_point=click_pos
        
            self.line_source.SetPoint1((self.start_point[0],self.start_point[1],0))
            self.line_source.SetPoint2((click_pos[0],click_pos[1],0))
            self.line_source.Update()
            self.line_actor.GetProperty().SetLineWidth(3)
            
            length = self.calculate_length()
            self.display_length(length)
      
            
            self.renderer.AddActor(self.length_text)
            self.renderer.AddActor(self.line_actor)
            self.render_window.Render()
        return self.OnMouseMove()


    def set_renderer(self, renderer, render_window):
        #set the renderer
        self.renderer=renderer
        self.render_window=render_window

    def calculate_length(self):
        # calculate the points between start and end
        if self.end_point:
            ans= math.sqrt((self.start_point[0] - self.end_point[0])**2 + (self.start_point[1] - self.end_point[1])**2)
            return ans
        else:
            return 0.0
    
    def display_length(self, length):
        #display the length at the end position
        self.length_text.SetInput("Length: {:.2f}".format(length))
        self.length_text.SetDisplayPosition(self.start_point[0], self.start_point[1])



    
if __name__ =="__main__":
    # Usage Example:
    #for testing the class, for main window please proceed to the our name py
    foldername= r"Assignment2\Pelvis\vhm.519.dcm"
    reader = vtk.vtkDICOMImageReader()
    reader.SetFileName(foldername)
    reader.Update()
    # Load your DICOM or any image data here using vtk reader
    renderer = vtk.vtkRenderer()
    render_window = vtk.vtkRenderWindow()
    #render_window.AddRenderer(renderer)

    viewer = vtk.vtkImageViewer2()
    viewer.SetInputConnection(reader.GetOutputPort())


    render_window_interactor = vtk.vtkRenderWindowInteractor()
    render_window_interactor.SetRenderWindow(render_window)
    viewer.SetRenderWindow(render_window)
    interactor_style = CustomInteractorStyle()
    #interactor_style.set_renderer(viewer.GetRenderer(), viewer)
    interactor_style.set_renderer(viewer.GetRenderer(), viewer)
    viewer.GetRenderer().ResetCamera()
    viewer.Render()



    renderer.AddActor(viewer.GetImageActor())
    render_window_interactor.SetInteractorStyle(interactor_style)

    viewer.Render()


    render_window_interactor.Start()
