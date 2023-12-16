import vtk


# this is the class for main python to call the modified vtk interactor style in paint
class CustomInteractorStyle(vtk.vtkInteractorStyleImage):
    def __init__(self):
        # add the observer for can paint purpose
        self.AddObserver("LeftButtonPressEvent", self.LeftButtonPressEvent)
        self.AddObserver("MouseMoveEvent", self.MouseMoveEvent)
        self.AddObserver("LeftButtonReleaseEvent", self.LeftButtonReleaseEvent)

        # point for detect and save the position after draw and next position
        self.point = None
        self.drawing = False


    def LeftButtonPressEvent(self, obj, event):
        # click and get the initial point
        self.point = self.GetInteractor().GetEventPosition()
        self.drawing=True
        return self.OnLeftButtonDown()

    def MouseMoveEvent(self, obj, event):
        if self.drawing:
            # constanly draw before the mouse click relased
            # get the position every move
            click_pos = self.GetInteractor().GetEventPosition()

            #cretae the line and draw it
            self.line_source = vtk.vtkLineSource()
            self.line_mapper = vtk.vtkPolyDataMapper2D()
            self.line_actor = vtk.vtkActor2D()
            
            self.line_mapper.SetInputConnection(self.line_source.GetOutputPort())
            self.line_actor.SetMapper(self.line_mapper)
            self.line_actor.GetProperty().SetColor(1.0, 0.0, 0.0)
            
            self.line_source.SetPoint1((self.point[0],self.point[1],0))
            self.line_source.SetPoint2((click_pos[0],click_pos[1],0))
            self.line_source.Update()
            self.line_actor.GetProperty().SetLineWidth(3)
            self.point=click_pos

            # Add the actor to the renderer
            self.renderer.AddActor(self.line_actor)
            self.render_window.Render()
        

    def LeftButtonReleaseEvent(self, obj, event):
        # after release the movement, reset all the things
        self.point = None
        self.drawing=False
        return self.OnLeftButtonUp()


    def set_renderer(self, renderer, render_window):
        #set the renderer and its window
        self.renderer = renderer
        self.render_window = render_window



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
