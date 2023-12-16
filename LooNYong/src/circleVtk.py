import vtk
import math

# this is the class for main python to call the modified vtk interactor style in draw circle movement
class CustomInteractorStyle(vtk.vtkInteractorStyleImage):
    def __init__(self):
        # add the observer for can draw the circle purpose
        self.AddObserver("LeftButtonPressEvent", self.LeftButtonPressEvent)
        self.AddObserver("MouseMoveEvent",self.MouseMoveEvent)
        
        # The definition for the function for normally
        # let center point to None in initial
        self.center = None 
        # let initial end point to None
        self.end_point = None 
        # For drawing purpose to detect for mouseMoveEvent todraw it
        self.drawing= False
        
    def LeftButtonPressEvent(self, obj, event):
        if self.drawing:
            # when second mouse click
            click_pos = self.GetInteractor().GetEventPosition()
            self.end_point=click_pos

            #calculate the radius between center and current position
            radius = int(math.sqrt((click_pos[0] - self.center[0])**2 + (click_pos[1] - self.center[1])**2))

            #update the circle to finalize the position of the circle
            self.circle_source.SetRadius(radius)
            self.circle_source.SetNumberOfSides(50)  # the number of sides for the circle
            self.circle_source.Update()
            
            #to show the radius in the screen
            self.display_length(radius)

            # display length on screen
            self.renderer.AddActor(self.length_text)
            self.render_window.Render()
            # back to initial
            self.drawing= False

        else:
            #for first step create circle
            self.circle_source = vtk.vtkRegularPolygonSource()
            self.circle_mapper = vtk.vtkPolyDataMapper2D()
            self.circle_actor = vtk.vtkActor2D()
            
            self.circle_mapper.SetInputConnection(self.circle_source.GetOutputPort())
            self.circle_actor.SetMapper(self.circle_mapper)
            
            # create the text for show number
            self.length_text = vtk.vtkTextActor()
            self.length_text.GetTextProperty().SetColor(1.0, 1.0, 1.0) 

            #get the position for the mouse click position
            click_pos = self.GetInteractor().GetEventPosition()
            #and save it into self.center
            self.center = click_pos
            #and trigger second click button
            self.drawing= True
        
        return self.OnLeftButtonDown()

    
    def MouseMoveEvent(self,  obj, event):
        if self.drawing:
            #after first mouse click constanly show circle until second clicked
            click_pos = self.GetInteractor().GetEventPosition()
            self.end_point=click_pos
            radius = int(math.sqrt((click_pos[0] - self.center[0])**2 + (click_pos[1] - self.center[1])**2))

            # Update the circle every movement
            self.circle_source.SetRadius(radius)
            self.circle_source.SetNumberOfSides(50)  
            self.circle_source.Update()
            self.circle_source.GeneratePolygonOff()
            self.circle_actor.SetPosition(self.center[0] , self.center[1] )
            self.display_length(radius)
      
            #add the actors to renderer      
            self.renderer.AddActor(self.length_text)
            self.renderer.AddActor(self.circle_actor)
            self.render_window.Render()
        return self.OnMouseMove()


    def set_renderer(self, renderer, render_window):
        # Get the renderer and its window to apply this modified style
        self.renderer=renderer
        self.render_window=render_window

    def display_length(self, length):
        # display the radius in screen
        self.length_text.SetInput("Radius: {:.2f}".format(length))
        self.length_text.SetDisplayPosition(self.end_point[0], self.end_point[1])
    

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
    #interactor_style.set_renderer(viewer.GetRenderer(), viewer)
    interactor_style.set_renderer(viewer.GetRenderer(), viewer)
    viewer.GetRenderer().ResetCamera()
    viewer.Render()



    renderer.AddActor(viewer.GetImageActor())
    render_window_interactor.SetInteractorStyle(interactor_style)

    viewer.Render()


    render_window_interactor.Start()
