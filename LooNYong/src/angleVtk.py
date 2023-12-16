import vtk
import math

# this is the class for main python to call the modified vtk interactor style in calculate angle movement
class CustomInteractorStyle(vtk.vtkInteractorStyleImage):
    def __init__(self):
        # add the observer for can calculate the angle purpose
        self.AddObserver("LeftButtonPressEvent", self.LeftButtonPressEvent)
        self.AddObserver("MouseMoveEvent",self.MouseMoveEvent)
        
        # set all the requirement point to zero
        self.start_point = None
        self.middle_point = None
        self.end_point = None
        self.drawing= False
        
    def LeftButtonPressEvent(self, obj, event):
        # add source for the line 
        self.line_source = vtk.vtkLineSource()
        self.line_mapper = vtk.vtkPolyDataMapper2D()
        self.line_actor = vtk.vtkActor2D()
        
        self.line_mapper.SetInputConnection(self.line_source.GetOutputPort())
        self.line_actor.SetMapper(self.line_mapper)
        self.line_actor.GetProperty().SetColor(1.0, 0.0, 0.0)
        if self.start_point is None:
            #for first step, get the position when first click
            self.start_point = self.GetInteractor().GetEventPosition()
            # trigger the mouse move can show the line
            self.drawing = True
            # actor for show the angle
            self.length_text = vtk.vtkTextActor()
            self.length_text.GetTextProperty().SetColor(1.0, 1.0, 1.0)
        elif self.middle_point is None:
            #For second click, get the position
            self.middle_point = self.GetInteractor().GetEventPosition()
            # finalize the first line between two points 
            self.line_source.SetPoint1((self.start_point[0],self.start_point[1],0))
            self.line_source.SetPoint2((self.middle_point[0],self.middle_point[1],0))
            self.line_source.Update()
        else :
            #for create second line by click third line
            # create new line source
            self.line_source = vtk.vtkLineSource()
            self.line_mapper = vtk.vtkPolyDataMapper2D()
            self.line_actor = vtk.vtkActor2D()
            
            self.line_mapper.SetInputConnection(self.line_source.GetOutputPort())
            self.line_actor.SetMapper(self.line_mapper)
            self.line_actor.GetProperty().SetColor(1.0, 0.0, 0.0)
            self.end_point = self.GetInteractor().GetEventPosition()
            
            #create second line between middle point and final point
            self.line_source.SetPoint1((self.middle_point[0],self.middle_point[1],0))
            self.line_source.SetPoint2((self.end_point[0],self.end_point[1],0))
            self.line_source.Update()
            
            # reset all so can draw another
            self.drawing = False
            self.start_point = None
            self.middle_point = None
            self.end_point = None
        
        return self.OnLeftButtonDown()



    def MouseMoveEvent(self,  obj, event):
        # always show the line when triggered
        if self.drawing:
            click_pos = self.GetInteractor().GetEventPosition()
            self.end_point=click_pos
            # for first line
            if self.middle_point is None:
                self.line_source.SetPoint1((self.start_point[0],self.start_point[1],0))
            else:
                # for second line 
                self.line_source.SetPoint1((self.middle_point[0],self.middle_point[1],0))
                # after second line can show the angle between two lines
                angle = self.calculate_angle()
                self.display_length(angle)
                self.renderer.AddActor(self.length_text)
            # for create line
            self.line_source.SetPoint2((click_pos[0],click_pos[1],0))
            self.line_source.Update()
            self.line_actor.GetProperty().SetLineWidth(3)
            
            self.renderer.AddActor(self.line_actor)
            self.render_window.Render()
        return self.OnMouseMove()


    def set_renderer(self, renderer, render_window):
        # set the renderer and window from using this style
        self.renderer=renderer
        self.render_window=render_window

    def calculate_angle(self):
        # calculate angle
        if self.end_point:
            angle_radians = -math.atan2(self.middle_point[0] - self.start_point[0], self.middle_point[1] - self.start_point[1]) + math.atan2(self.end_point[0] - self.middle_point[0], self.end_point[1] - self.middle_point[1])
            angle_degrees = math.degrees(angle_radians)
            angle_degrees=angle_degrees+180
            if angle_degrees > 360:
                angle_degrees=angle_degrees-360
            elif angle_degrees < 0:
                angle_degrees=angle_degrees+360

            return angle_degrees 
        else:
            return 0.0
    
    def display_length(self, length):
        # display angle
        self.length_text.SetInput("Angle: {:.2f}".format(length))
        self.length_text.SetDisplayPosition(self.middle_point[0], self.middle_point[1])
    
if __name__ == "__main__":
    #for testing the class, for main window please proceed to the our name py
    # Usage Example:
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
    interactor_style.set_renderer(viewer.GetRenderer(), viewer)
    viewer.GetRenderer().ResetCamera()
    viewer.Render()



    renderer.AddActor(viewer.GetImageActor())
    render_window_interactor.SetInteractorStyle(interactor_style)

    viewer.Render()


    render_window_interactor.Start()
